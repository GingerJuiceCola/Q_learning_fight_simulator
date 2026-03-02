# q_agent.py
import numpy as np
import pickle
import os
from typing import Tuple, Dict
from config import *


class QLearningAgent:
    """Q学习核心类：处理Q表管理和动作选择"""
    def __init__(self):
        # 初始化Q表
        self.q_table: Dict = {}
        self._init_q_table()
        
        # 探索率
        self.epsilon = DEFAULT_EPSILON

    def _init_q_table(self):
        """初始化/加载Q表"""
        if os.path.exists(Q_TABLE_PATH):
            with open(Q_TABLE_PATH, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"加载Q表：{Q_TABLE_PATH}")
        else:
            # 生成全状态空间的Q表
            for s_hp in HP_RANGE:
                for s_sta in STA_RANGE:
                    for s_spd in SPD_RANGE:
                        for o_hp in HP_RANGE:
                            for o_sta in STA_RANGE:
                                for o_spd in SPD_RANGE:
                                    for tag in SPD_TAGS:
                                        self.q_table[(s_hp, s_sta, s_spd, o_hp, o_sta, o_spd, tag)] = [0.0] * 6

    def save_q_table(self):
        """保存Q表"""
        with open(Q_TABLE_PATH, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"保存Q表：{Q_TABLE_PATH}")

    def select_action(self, state: Tuple, is_agent=True) -> int:
        """动作选择：ε-贪心（智能体）/规则化随机（敌方）"""
        if is_agent:
            # 智能体：ε-贪心策略
            if np.random.rand() < self.epsilon:
                return np.random.choice(6)
            return np.argmax(self.q_table[state])
        else:
            # 敌方：规则化随机策略
            o_hp, o_sta, o_spd = state
            probs = np.array([0.15, 0.15, 0.15, 0.2, 0.2, 0.15])
            if o_hp <= 2:
                probs[[0, 1, 2]] *= 1.8
                probs[[3, 4, 5]] *= 0.5
            if o_spd == 3:
                probs[5] *= 2.0
            if o_sta <= 2:
                probs[[2, 5]] *= 0.1
            probs /= probs.sum()  # 概率归一化
            return np.random.choice(6, p=probs)

    def decay_epsilon(self):
        """探索率衰减"""
        self.epsilon = max(EPSILON_MIN, self.epsilon - EPSILON_DECAY)
