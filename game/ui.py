# ui.py
import pygame
import time
import numpy as np
from fighter import QLearningFighter

# 颜色常量
BLACK = (0,0,0)
RED = (220,20,60)
GREEN = (50,205,50)
BLUE = (30,144,255)
GRAY = (128,128,128)
LIGHT = (200,200,200)
DARK_RED = (139,0,0)
DARK_GREEN = (0,100,0)
YELLOW = (255,215,0)

def draw_bar(surf, x, y, w, h, val, maxv, bg, fg):

def draw_text(surf, text, font, x, y, color, center=False):

def draw_stickman(surf, x, y, action, side, color=BLACK, dashed=False):

def show_menu(screen, font_large, font_med):
    """显示简单开始菜单"""
    screen.fill(LIGHT)
    draw_text(screen, "Q-learning Agent vs Rule-based Opponent", font_large, 450, 250, BLACK, center=True)
    draw_text(screen, "Press any key to start", font_med, 450, 350, BLACK, center=True)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def run_demo(fighter: QLearningFighter):
    pygame.init()
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Q-learning Fighting Demo")
    clock = pygame.time.Clock()

    # 字体
    try:
        font_large = pygame.font.SysFont('Arial', 32)
        font_med = pygame.font.SysFont('Arial', 24)
        font_small = pygame.font.SysFont('Arial', 20)
    except:
        font_large = pygame.font.Font(None, 32)
        font_med = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)

    # 显示菜单
    show_menu(screen, font_large, font_med)

    # 英文动作映射
    action_en = ["Dodge", "Block", "Parry", "Light", "Break", "Heavy"]
    tag_en = {"自己快": "Self Fast", "对方慢": "Opp Slow", "无": "None"}

    def reset():
        s_spd = np.random.choice(fighter.SPD_RANGE)
        o_spd = np.random.choice(fighter.SPD_RANGE)
        return (5,5,s_spd,5,5,o_spd,"无"), 0.0, 0, False

    state, total_score, turn, done = reset()
    last_score = 0.0
    agent_act_name = "Waiting"
    opp_act_name = "Waiting"
    running = True
    pause = 0.8
    last_step = time.time()
    fighter.epsilon = 0.0  # 利用模式

    while running:
        now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state, total_score, turn, done = reset()
                    last_score = 0.0
                    agent_act_name = "Waiting"
                    opp_act_name = "Waiting"
                elif event.key == pygame.K_q:
                    running = False

        if not done and (now - last_step) >= pause:
            agent_act = np.argmax(fighter.q_table[state])
            opp_act = fighter.select_action((state[3], state[4], state[5]), is_agent=False)
            r, next_state, done = fighter.fight_step(state, agent_act, opp_act)
            total_score += r
            turn += 1
            last_score = r
            agent_act_name = action_en[agent_act]
            opp_act_name = action_en[opp_act]
            state = next_state
            last_step = now

        # 绘制界面
        screen.fill(LIGHT)
        s_hp, s_sta, s_spd, o_hp, o_sta, o_spd, tag = state

        draw_text(screen, "Q-learning Fighting (Exhaustion: +1 damage)", font_large, 450, 30, BLACK, center=True)
        draw_text(screen, f"Turn: {turn}", font_med, 100, 70, BLACK)
        draw_text(screen, f"Total Score: {total_score:.1f}", font_med, 300, 70, BLACK)
        tag_show = tag_en.get(tag, tag)
        draw_text(screen, f"Tag: {tag_show}", font_med, 600, 70, DARK_RED)

        # 左侧智能体
        draw_text(screen, "Agent", font_med, 150, 120, BLUE, center=True)
        draw_bar(screen, 50, 150, 200, 20, s_hp, 5, GRAY, RED)
        draw_text(screen, f"HP:{s_hp}/5", font_small, 160, 150, BLACK, center=True)
        draw_bar(screen, 50, 180, 200, 15, s_sta, 5, GRAY, GREEN)
        draw_text(screen, f"Stamina:{s_sta}/5", font_small, 160, 180, BLACK, center=True)
        draw_text(screen, f"Speed:{s_spd}", font_med, 160, 210, BLACK, center=True)
        draw_text(screen, f"Action:{agent_act_name}", font_med, 160, 240, DARK_GREEN, center=True)

        # 右侧对手
        draw_text(screen, "Opponent", font_med, 750, 120, RED, center=True)
        draw_bar(screen, 650, 150, 200, 20, o_hp, 5, GRAY, RED)
        draw_text(screen, f"HP:{o_hp}/5", font_small, 750, 150, BLACK, center=True)
        draw_bar(screen, 650, 180, 200, 15, o_sta, 5, GRAY, GREEN)
        draw_text(screen, f"Stamina:{o_sta}/5", font_small, 750, 180, BLACK, center=True)
        draw_text(screen, f"Speed:{o_spd}", font_med, 750, 210, BLACK, center=True)
        draw_text(screen, f"Action:{opp_act_name}", font_med, 750, 240, DARK_RED, center=True)

        # 本回合得分
        scolor = YELLOW if last_score >= 0 else RED
        draw_text(screen, f"Turn Score: {last_score:+.1f}", font_large, 450, 280, scolor, center=True)

        # 火柴人（左右各一）
        if agent_act_name == 'Dodge':
            draw_stickman(screen, 150, 400, agent_act_name, 'left', dashed=True)
            draw_stickman(screen, 130, 400, agent_act_name, 'left', color=BLACK)
        else:
            draw_stickman(screen, 150, 400, agent_act_name, 'left', color=BLACK)

        if opp_act_name == 'Dodge':
            draw_stickman(screen, 750, 400, opp_act_name, 'right', dashed=True)
            draw_stickman(screen, 770, 400, opp_act_name, 'right', color=BLACK)
        else:
            draw_stickman(screen, 750, 400, opp_act_name, 'right', color=BLACK)

        if done:
            result = "You Win!" if o_hp <= 0 else "You Lose!" if s_hp <= 0 else "Game Over"
            draw_text(screen, result, font_large, 450, 500, DARK_RED, center=True)
            draw_text(screen, "Press R to restart | Q to quit", font_med, 450, 550, BLACK, center=True)

        draw_text(screen, "Auto battle", font_small, 450, 620, GRAY, center=True)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
