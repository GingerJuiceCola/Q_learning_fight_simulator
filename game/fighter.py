# fighter.py
import numpy as np
import pickle
import os
from typing import Tuple, List, Dict

class QLearningFighter:
    """Q学习格斗智能体（完整保留修正后的逻辑）"""
    ACTIONS: List[str] = ["闪避", "格挡", "招架", "轻击", "破防", "重击"]
    ACTION_PROPS: Dict[int, Tuple[int, int]] = {
        0: (2, 1),  # 闪避
        1: (3, 0),  # 格挡
        2: (2, 2),  # 招架
        3: (2, 1),  # 轻击
        4: (2, 1),  # 破防
        5: (1, 2)   # 重击
    }
    HP_RANGE = [1, 2, 3, 4, 5]
    STA_RANGE = [1, 2, 3, 4, 5]
    SPD_RANGE = [1, 2, 3]
    SPD_TAGS = ["自己快", "对方慢", "无"]

    def __init__(self,
                 q_table_path="q_table.pkl",
                 alpha=0.2,
                 gamma=0.95,
                 epsilon=1.0,
                 epsilon_decay=0.0025,
                 epsilon_min=0.015,
                 max_turns=50,
                 win_reward=100,
                 lose_penalty=-80,
                 small_reward=2.0,
                 small_penalty=-2.0,
                 defense_no_attack_penalty=-0.5):
        # 参数赋值...
        self.q_table_path = q_table_path
        self.q_table: Dict = {}
        self.train_rewards: List[float] = []
        self._init_q_table()

    def _init_q_table(self):
        # 初始化/加载Q表
        if os.path.exists(self.q_table_path):
            with open(self.q_table_path, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"Loaded Q-table: {self.q_table_path}")
        else:
            # 生成全状态Q表
            for s_hp in self.HP_RANGE:
                for s_sta in self.STA_RANGE:
                    for s_spd in self.SPD_RANGE:
                        for o_hp in self.HP_RANGE:
                            for o_sta in self.STA_RANGE:
                                for o_spd in self.SPD_RANGE:
                                    for tag in self.SPD_TAGS:
                                        self.q_table[(s_hp, s_sta, s_spd, o_hp, o_sta, o_spd, tag)] = [0.0]*6

    def save_q_table(self):
        # 保存Q表
        with open(self.q_table_path, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Saved Q-table: {self.q_table_path}")

    def select_action(self, state: Tuple, is_agent=True) -> int:
        # 动作选择（智能体/敌方）
        # ...（完整代码，与之前一致）

    def fight_step(self, state: Tuple, a_act: int, o_act: int) -> Tuple[float, Tuple, bool]:
        # 核心对抗逻辑
        # ...（完整代码，与之前一致）
