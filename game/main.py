# main.py
from fighter import QLearningFighter
from ui import run_demo

if __name__ == "__main__":
    q_table_path = r"C:\Users\JYJ\@ai_asg\ml_asg\q_table.pkl"
    fighter = QLearningFighter(
        q_table_path=q_table_path,
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
        defense_no_attack_penalty=-0.5
    )
    run_demo(fighter)
