import pygame
import sys
from logic import Game2048
from strategies import load_strategies

# Colors (Standard 2048 Palette)
COLOR_BG = (187, 173, 160)
COLOR_EMPTY = (205, 193, 180)
COLOR_TEXT = (119, 110, 101)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

class Renderer:
    def __init__(self, cell_size=80, margin=10):
        self.cell_size = cell_size
        self.margin = margin
        self.font_small = pygame.font.SysFont("arial", 20, bold=True)
        self.font_large = pygame.font.SysFont("arial", 36, bold=True)

    def draw_board(self, screen, game, offset_x, offset_y, name=""):
        board_size = game.size * self.cell_size + (game.size + 1) * self.margin
        pygame.draw.rect(screen, COLOR_BG, (offset_x, offset_y, board_size, board_size), border_radius=5)

        for r in range(game.size):
            for c in range(game.size):
                val = game.grid[r][c]
                color = TILE_COLORS.get(val, (60, 58, 50))
                x = offset_x + self.margin + c * (self.cell_size + self.margin)
                y = offset_y + self.margin + r * (self.cell_size + self.margin)
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size), border_radius=3)

                if val != 0:
                    text_color = (249, 246, 242) if val >= 8 else COLOR_TEXT
                    text = self.font_small.render(str(val), True, text_color)
                    rect = text.get_rect(center=(x + self.cell_size / 2, y + self.cell_size / 2))
                    screen.blit(text, rect)

        # Draw Score
        score_text = self.font_small.render(f"{name} Score: {game.score}", True, (50, 50, 50))
        screen.blit(score_text, (offset_x, offset_y + board_size + 10))

        if game.game_over:
            overlay = pygame.Surface((board_size, board_size), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 150))
            screen.blit(overlay, (offset_x, offset_y))
            msg = self.font_small.render("GAME OVER", True, (0, 0, 0))
            rect = msg.get_rect(center=(offset_x + board_size / 2, offset_y + board_size / 2))
            screen.blit(msg, rect)

from cv_controller import GestureController

def run_manual(use_cv=False):
    pygame.init()
    game = Game2048()
    renderer = Renderer()
    board_px = 4 * 80 + 5 * 10
    screen = pygame.display.set_mode((board_px + 40, board_px + 80))
    pygame.display.set_caption("2048 Manual Mode")
    clock = pygame.time.Clock()

    cv_ctrl = None
    if use_cv:
        cv_ctrl = GestureController()
        cv_ctrl.start()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: game.move('UP')
                    if event.key == pygame.K_DOWN: game.move('DOWN')
                    if event.key == pygame.K_LEFT: game.move('LEFT')
                    if event.key == pygame.K_RIGHT: game.move('RIGHT')
                    if event.key == pygame.K_r: game.reset()
                    if event.key == pygame.K_ESCAPE: return

            if cv_ctrl:
                move = cv_ctrl.get_move()
                if move:
                    game.move(move)

            screen.fill((250, 248, 239))
            renderer.draw_board(screen, game, 20, 20, "Manual")
            pygame.display.flip()
            clock.tick(60)
    finally:
        if cv_ctrl:
            cv_ctrl.stop()
        pygame.quit()

def run_auto(strategies):
    if len(strategies) < 2:
        print("Need at least 2 strategies for comparison.")
        return

    pygame.init()
    game1 = Game2048()
    game2 = Game2048()
    s1, s2 = strategies[0], strategies[1]
    renderer = Renderer()

    board_px = 4 * 80 + 5 * 10
    width = board_px * 2 + 60
    height = board_px + 100
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"2048 Comparison: {s1.name} vs {s2.name}")
    clock = pygame.time.Clock()

    move_delay = 10 # ms
    last_move = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_r:
                    game1.reset()
                    game2.reset()

        now = pygame.time.get_ticks()
        if now - last_move > move_delay:
            if not game1.game_over:
                # The strategy only gives a preference, we must try until one works
                for m in s1.priority_list:
                    if game1.move(m): break
            if not game2.game_over:
                for m in s2.priority_list:
                    if game2.move(m): break
            last_move = now

        screen.fill((250, 248, 239))
        renderer.draw_board(screen, game1, 20, 20, s1.name)
        renderer.draw_board(screen, game2, board_px + 40, 20, s2.name)

        pygame.display.flip()
        clock.tick(60)
