# trainer.py
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from q_agent import QLearningAgent
from fight_core import FightCore
from config import *


class QTrainer:
    """训练管理器：整合Q表和格斗核心，处理训练循环"""
    def __init__(self):
        self.agent = QLearningAgent()
        self.fight_core = FightCore()
        self.train_rewards: List[float] = []

    def train(self):
        """启动训练循环"""
        print(f"\n开始训练{TRAIN_EPISODES}轮（每10轮打印一次）")
        print(f"防御无攻击惩罚值：{self.fight_core.defense_no_attack_penalty} | 体力耗尽仅伤害+1")
        
        for ep in range(TRAIN_EPISODES):
            # 初始化每轮状态
            s_spd_init = np.random.choice(SPD_RANGE)
            o_spd_init = np.random.choice(SPD_RANGE)
            state = (5, 5, s_spd_init, 5, 5, o_spd_init, "无")
            total_r = 0.0
            turns = 0
            done = False

            # 单轮格斗
            while not done and turns < MAX_TURNS:
                turns += 1
                a_act = self.agent.select_action(state)
                o_act = self.agent.select_action((state[3], state[4], state[5]), is_agent=False)
                r, next_state, done = self.fight_core.fight_step(state, a_act, o_act, self.agent.q_table)
                total_r += r

                # Q表更新
                self.agent.q_table[state][a_act] += DEFAULT_ALPHA * (
                    r + DEFAULT_GAMMA * np.max(self.agent.q_table[next_state]) - self.agent.q_table[state][a_act]
                )
                state = next_state

            # 探索率衰减
            self.agent.decay_epsilon()
            self.train_rewards.append(total_r)

            # 打印日志
            if (ep + 1) % 10 == 0:
                avg_r = np.mean(self.train_rewards[-10:])
                print(f"轮次：{ep+1:4d} | 近10轮平均奖励：{avg_r:6.2f} | 探索率：{self.agent.epsilon:.3f}")

        # 保存Q表+绘制曲线
        self.agent.save_q_table()
        self.plot_curve()

    def plot_curve(self):
        """绘制训练曲线"""
        # 中文配置
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
        plt.rcParams["axes.unicode_minus"] = False

        plt.figure(figsize=(12, 6))
        # 10轮滑动平均
        window = 10
        if len(self.train_rewards) >= window:
            smooth_rewards = np.convolve(self.train_rewards, np.ones(window)/window, mode="valid")
            plt.plot(range(window-1, len(self.train_rewards)), smooth_rewards, 
                     color='#0000CD', linewidth=2.5, label='10轮滑动平均奖励')
        # 单轮奖励
        plt.plot(self.train_rewards, color='#B0C4DE', alpha=0.5, label='单轮奖励', linewidth=1)
        # 0奖励线
        plt.axhline(y=0, color='#FF4500', linestyle='--', alpha=0.8, label='奖励阈值(0)')

        # 图表标注
        plt.xlabel('训练轮次', fontsize=12)
        plt.ylabel('总奖励', fontsize=12)
        plt.title(
            f'Q学习格斗游戏训练奖励曲线（{TRAIN_EPISODES}轮）- 体力耗尽仅伤害+1 | 防御无攻击惩罚={self.fight_core.defense_no_attack_penalty}',
            fontsize=14, fontweight='bold'
        )
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, linestyle='-')
        plt.tight_layout()

        # 保存图片
        plt.savefig(TRAIN_CURVE_PATH, dpi=300, bbox_inches='tight')
        print(f"\n✅ 训练曲线已保存：{TRAIN_CURVE_PATH}")
        plt.show()
