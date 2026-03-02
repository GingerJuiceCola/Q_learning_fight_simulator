# fight_core.py
import numpy as np
from typing import Tuple
from config import *


class FightCore:
    """格斗核心类：处理单步对抗逻辑和状态更新"""
    def __init__(self):
        # 奖励配置
        self.win_reward = WIN_REWARD
        self.lose_penalty = LOSE_PENALTY
        self.small_reward = SMALL_REWARD
        self.small_penalty = SMALL_PENALTY
        self.defense_no_attack_penalty = DEFENSE_NO_ATTACK_PENALTY

    def fight_step(self, state: Tuple, a_act: int, o_act: int, q_table: Dict) -> Tuple[float, Tuple, bool]:
        """单步对抗：输入状态和动作，输出奖励、下一状态、是否结束"""
        s_hp, s_sta, s_spd, o_hp, o_sta, o_spd, tag = state
        reward = 0.0
        done = False
        
        # 1. 防御无攻击惩罚判定
        defense_actions = [0, 1, 2]
        attack_actions = [3, 4, 5]
        if (a_act in defense_actions) and (o_act not in attack_actions) and (ACTION_PROPS[a_act][1] > 0):
            reward += self.defense_no_attack_penalty

        # 2. 基础属性计算
        s_sta_consume = ACTION_PROPS[a_act][1]
        o_sta_consume = ACTION_PROPS[o_act][1]
        s_sta_new = max(1, s_sta - s_sta_consume)
        o_sta_new = max(1, o_sta - o_sta_consume)
        
        # 体力耗尽判定（用于伤害加成）
        s_sta_exhausted = (s_sta - s_sta_consume) <= 0
        o_sta_exhausted = (o_sta - o_sta_consume) <= 0
        
        # 最终速度
        s_final_spd = s_spd + ACTION_PROPS[a_act][0]
        o_final_spd = o_spd + ACTION_PROPS[o_act][0]
        
        # 临时血量
        s_hp_temp, o_hp_temp = s_hp, o_hp

        # 3. 对抗规则
        if a_act == o_act and s_final_spd == o_final_spd:
            if a_act == 3:  # 双方轻击
                base_dmg = 1
                s_hp_temp -= base_dmg + (1 if s_sta_exhausted else 0)
                o_hp_temp -= base_dmg + (1 if o_sta_exhausted else 0)
            elif a_act == 5:  # 双方重击
                base_dmg = 2
                s_hp_temp -= base_dmg + (1 if s_sta_exhausted else 0)
                o_hp_temp -= base_dmg + (1 if o_sta_exhausted else 0)
        else:
            # 智能体攻击逻辑
            if a_act == 5:  # 重击
                if o_act in [3, 4] and o_final_spd >= s_final_spd:
                    reward += self.small_penalty
                elif o_act == 1:
                    base_dmg = 1
                    o_hp_temp -= base_dmg + (1 if o_sta_exhausted else 0)
                    reward += self.small_reward
                elif s_final_spd >= o_final_spd + 1:
                    base_dmg = 2
                    o_hp_temp -= base_dmg + (1 if o_sta_exhausted else 0)
                    reward += self.small_reward * 2
            elif a_act == 2 and o_act in [3, 5] and s_final_spd >= o_final_spd:
                base_dmg = 1
                o_hp_temp -= base_dmg + (1 if o_sta_exhausted else 0)
                reward += self.small_reward * 2
            elif a_act == 0 and o_act in [3, 5] and s_final_spd >= o_final_spd:
                reward += self.small_reward * 1.5
            elif a_act == 4:  # 破防
                if (o_act in [2, 0, 5] and s_final_spd >= o_final_spd) or (o_act == 3 and s_final_spd > o_final_spd):
                    reward += self.small_reward * 2

            # 敌方攻击逻辑
            if o_act == 3 and o_final_spd > s_final_spd:
                base_dmg = 1
                s_hp_temp -= base_dmg + (1 if s_sta_exhausted else 0)
                reward += self.small_penalty
            elif o_act == 5 and o_final_spd >= s_final_spd + 1:
                base_dmg = 2
                s_hp_temp -= base_dmg + (1 if s_sta_exhausted else 0)
                reward += self.small_penalty * 2
            elif o_act == 2 and a_act in [3, 5] and o_final_spd >= s_final_spd:
                base_dmg = 1
                s_hp_temp -= base_dmg + (1 if s_sta_exhausted else 0)
                reward += self.small_penalty

            # 格挡重击规则
            if a_act == 1 and o_act == 5:
                s_sta_new = max(1, s_sta_new - 2)
                base_dmg = 1
                s_hp_temp -= base_dmg + (1 if (s_sta - s_sta_consume - 2) <= 0 else 0)
                reward += self.small_penalty * 2
            if o_act == 1 and a_act == 5:
                o_sta_new = max(1, o_sta_new - 2)
                base_dmg = 1
                o_hp_temp -= base_dmg + (1 if (o_sta - o_sta_consume - 2) <= 0 else 0)
                reward += self.small_reward * 2

        # 4. 体力回复
        s_sta_new = min(5, s_sta_new + 1)
        o_sta_new = min(5, o_sta_new + 1)

        # 5. 胜负判定
        s_hp_final = max(0, s_hp_temp)
        o_hp_final = max(0, o_hp_temp)
        if s_hp_final <= 0:
            reward += self.lose_penalty
            done = True
        if o_hp_final <= 0:
            reward += self.win_reward
            done = True

        # 6. 速度标签生成
        next_tag = "无"
        if a_act == 4:
            if (o_act in [2, 0, 5] and s_final_spd >= o_final_spd) or (o_act == 3 and s_final_spd > o_final_spd):
                next_tag = "自己快"
        elif a_act == 2 and o_act in [3, 5] and s_final_spd >= o_final_spd:
            next_tag = "对方慢"
        elif o_act == 2 and a_act in [3, 5] and o_final_spd >= s_final_spd:
            next_tag = "对方慢"
        elif a_act == 5 and s_final_spd >= o_final_spd + 1 and o_act != 1:
            next_tag = "自己快"

        # 速度更新
        s_spd_next, o_spd_next = s_spd, o_spd
        if next_tag == "自己快":
            s_spd_next = 3
            o_spd_next = np.random.choice(SPD_RANGE)
        elif next_tag == "对方慢":
            s_spd_next = np.random.choice(SPD_RANGE)
            o_spd_next = 1
        else:
            s_spd_next = np.random.choice(SPD_RANGE)
            o_spd_next = np.random.choice(SPD_RANGE)

        # 7. 下一状态
        next_state = (
            int(s_hp_final), int(s_sta_new), int(s_spd_next),
            int(o_hp_final), int(o_sta_new), int(o_spd_next),
            next_tag
        )
        next_state = next_state if next_state in q_table else state

        return reward, next_state, done
