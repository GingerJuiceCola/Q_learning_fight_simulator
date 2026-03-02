# main.py
from trainer import QTrainer


def main():
    """程序入口：启动Q学习训练"""
    trainer = QTrainer()
    trainer.train()


if __name__ == "__main__":
    main()
