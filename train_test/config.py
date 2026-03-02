# config.py
from typing import Tuple, List, Dict

# 动作配置
ACTIONS: List[str] = ["闪避", "格挡", "招架", "轻击", "破防", "重击"]
ACTION_PROPS: Dict[int, Tuple[int, int]] = {
    0: (2, 1),  # 闪避：速度加成、体力消耗
    1: (3, 0),  # 格挡：速度加成、体力消耗
    2: (2, 2),  # 招架：速度加成、体力消耗
    3: (2, 1),  # 轻击：速度加成、体力消耗
    4: (2, 1),  # 破防：速度加成、体力消耗
    5: (1, 2)   # 重击：速度加成、体力消耗
}

# 状态空间配置
HP_RANGE = [1, 2, 3, 4, 5]
STA_RANGE = [1, 2, 3, 4, 5]
SPD_RANGE = [1, 2, 3]
SPD_TAGS = ["自己快", "对方慢", "无"]

# 训练超参数
DEFAULT_ALPHA = 0.2
DEFAULT_GAMMA = 0.95
DEFAULT_EPSILON = 1.0
EPSILON_DECAY = 0.0025
EPSILON_MIN = 0.015
MAX_TURNS = 50
TRAIN_EPISODES = 500

# 奖励体系
WIN_REWARD = 100
LOSE_PENALTY = -80
SMALL_REWARD = 2.0
SMALL_PENALTY = -2.0
DEFENSE_NO_ATTACK_PENALTY = -0.5  # 防御无攻击惩罚

# 文件路径
Q_TABLE_PATH = "q_table.pkl"
TRAIN_CURVE_PATH = "training_curve_500.png"
