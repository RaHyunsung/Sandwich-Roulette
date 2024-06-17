from threading import Thread
import pygame
import sys
import time
import os
import random

pygame.init()

# Set font
TITLE_FONT = pygame.font.Font(None, 200)
FONT = pygame.font.Font(None, 74)
SMALL_FONT = pygame.font.Font(None, 50)

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)
TRANSPARENT_WHITE = (255, 255, 255, 128)

# Credits
Credits = {
    "Core Programmer"   : "Hyunsung Ra & Roy Xu",
    "UI Programmer"     : "Hyunsung Ra",
    "Game Idea"         : "Hyunsung Ra & Roy Xu",
    "Designing"         : "Brian Pramana Saputra & John Carlo Arbuez",
    "Background Music"  : "Cyberpunk Gaming Sport by Infraction [No Copyright Music] / 130 Dopa"
}

# ---------- GAME OBJECTS ----------

class MTI_Injector:
    def __init__(self):
        self.heal_amount = 1
    def visual_effect(self):
        _stop = False
        def show_image():
            while not _stop:
                screen.blit(MTI_Image, MTI_rect)
        Thread(target=show_image, daemon=Thread).start()
        origin_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(1)
        time.sleep(15)
        _stop = True
        pygame.mixer.music.set_volume(origin_volume)
    def main(self, **kwargs):
        player_object = kwargs["TARGET"]
        player_max_health = player_object.max_health
        player_health = player_object.health
        if player_health + self.heal_amount >= player_max_health:
            player_object.health = player_max_health
        elif player_health + self.heal_amount < player_max_health:
            player_object.health += self.heal_amount
        Thread(target=self.visual_effect, daemon=True).start()
        

class Player:
    def __init__(self):
        self.health = 3
        self.max_health = 3
        self.items = []

# ---------- PARTICLES ----------

class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, TRANSPARENT_WHITE, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = -1

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += random.randint(-1, 1)
        if self.rect.bottom < 0:
            self.kill()

# ---------- UI RENDERER ----------

def render_text(text, font, color, bg, transparent=False):
    if transparent == False: text_surface = font.render(text, True, color, bg)
    else: text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def render_message_box():
    global message_box_selected
    box_width = message_box_size[0]
    box_height = message_box_size[1]
    box_x = (screen.get_width() - box_width) // 2
    box_y = (screen.get_height() - box_height) // 2
    pygame.draw.rect(screen, DARK_GRAY, (box_x, box_y, box_width, box_height))

    lines = message_box_title.split("\n")

    current_y = 0

    for i in range(len(lines)):
        text_surface, text_rect = render_text(lines[i], SMALL_FONT, WHITE, DARK_GRAY)
        text_rect.center = (box_x + box_width // 2, box_y + 50 + i * 50)
        current_y += i * 50
        screen.blit(text_surface, text_rect)

    for i, item in enumerate(message_box_items):
        if i == message_box_selected:
            text_color = DARK_GRAY
            bg_color = WHITE
        else:
            text_color = WHITE
            bg_color = DARK_GRAY
        text_surface, text_rect = render_text(item, SMALL_FONT, text_color, bg_color)
        text_rect.center = (box_x + box_width // 2, box_y + 50 + (i + 1) * 50 + current_y)
        screen.blit(text_surface, text_rect)

def load_image(image_path, size):
    try:
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Error loading image: {image_path}")
        raise SystemExit(e)

def load_assets():
    for asset_folder in os.listdir("assets"):
        folder = f"./assets/{asset_folder}"
        GAME_ASSETS[asset_folder] = {}
        for asset in os.listdir(folder):
            asset_name, extension = os.path.splitext(asset)
            asset_name = asset_name.upper()
            asset_path = f"{folder}/{asset}"
            GAME_ASSETS[asset_folder][asset_name] = asset_path
            print(f"[+] Asset Loaded. [TYPE: {folder}] [PATH: {asset_path}] [KEY: {asset_name}]")

# ---------- MENU FUNCTIONS ----------

def quit_game():
    pygame.quit()
    sys.exit()

def close_msgbox():
    global message_box_active
    message_box_active = False

def blank():
    pass

class MainMenu:
    def __init__(self):
        self.message_box_active = False
        self.message_box_items = []
        self.message_box_selected = 0
        self.message_box_title = ""
        self.message_box_size = (400, 200)
        self.message_box_functions = []
    
    def _update(self):
        global selected_item
        global message_box_active
        global message_box_selected
        global message_box_title
        global message_box_items
        global message_box_size
        global message_box_functions

        message_box_active = self.message_box_active
        message_box_items = self.message_box_items
        message_box_selected = self.message_box_selected
        message_box_title = self.message_box_title
        message_box_size = self.message_box_size
        message_box_functions = self.message_box_functions

    def start_game(self):
        self.message_box_size = (1000, 250)
        self.message_box_title = "Please choose the game mode to play"
        self.message_box_items = ["PVP", "PVE", "Cancel"]
        self.message_box_functions = [blank, blank, close_msgbox]
        self.message_box_active = True
        self.message_box_selected = 0
        self._update()

    def exit_game(self):
        self.message_box_size = (800, 200)
        self.message_box_title = "Do you wish to exit the game?"
        self.message_box_functions = [quit_game, close_msgbox]
        self.message_box_items = ["Yes", "No"]
        self.message_box_active = True
        self.message_box_selected = 0
        self._update()

    def show_credits(self):
        self.message_box_size = (1800, 800)
        self.message_box_title = '\n'.join([str(f"{key}: {value}") for key, value in Credits.items()])
        self.message_box_functions = [close_msgbox]
        self.message_box_items = ["Confirm"]
        self.message_box_active = True
        self.message_box_selected = 0
        self._update()

def main():
    global selected_item
    global message_box_active
    global message_box_selected
    global message_box_title
    global message_box_items
    global message_box_size
    global message_box_functions

    global color_tick

    while True:
        screen_width, screen_height = screen.get_size()
        screen.fill(BLACK)

        title_text_surface, title_text_rect = render_text("Sandwich", TITLE_FONT, WHITE, BLACK, transparent=True)
        title_text_rect.topright = (screen_width - 50, 50)

        title_2_text_surface, title_2_text_rect = render_text("Roulette", TITLE_FONT, WHITE, BLACK, transparent=True)
        title_2_text_rect.topright = (screen_width - 50, TITLE_FONT.get_height() + 50)

        credit_1_surface, credit_1_rect = render_text("Present By Roy, Hyunsung, Brian, John", SMALL_FONT, WHITE, BLACK, transparent=True)
        credit_1_rect.topright = (screen_width - 50, TITLE_FONT.get_height() + 200)

        screen.blit(Blood1_Image, Blood1_rect)

        screen.blit(title_text_surface, title_text_rect)
        screen.blit(title_2_text_surface, title_2_text_rect)
        screen.blit(credit_1_surface, credit_1_rect)

        screen.blit(PG_Panel_Image, PG_Panel_rect)
        screen.blit(Blood2_Image, Blood2_rect)

        # Render texts
        for i, item in enumerate(menu_items):
            if i == selected_item:
                color = BLACK
                bg = WHITE
            else:
                color = WHITE
                bg = BLACK
            text_surface, text_rect = render_text(item["TEXT"].ljust(30), SMALL_FONT, color, bg)
            text_rect.topleft = (20, 20 + i * 50)
            screen.blit(text_surface, text_rect)

        if message_box_active:
            render_message_box()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not message_box_active:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        menu_items[selected_item]["FUNC"]()
                    elif event.key == pygame.K_f:
                        print(MAIN_CHAR.health)
                        injector = MTI_Injector()
                        injector.main(TARGET=MAIN_CHAR)
                        print(MAIN_CHAR.health)
                else:
                    if event.key == pygame.K_UP:
                        message_box_selected = (message_box_selected - 1) % len(message_box_items)
                    if event.key == pygame.K_DOWN:
                        message_box_selected = (message_box_selected + 1) % len(message_box_items)
                    elif event.key == pygame.K_RETURN:
                        message_box_functions[message_box_selected]()
                    elif event.key == pygame.K_ESCAPE:
                        message_box_active = False

        pygame.display.flip()

if __name__ == "__main__":
    MAIN_CHAR = Player()
    MAIN_CHAR.health -= 2
    # Set screen size & captions
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("SANDWICH-ROULETTE")

    # Assets
    GAME_ASSETS = {}
    load_assets()

    # Main Menu Loader
    MAIN_MENU = MainMenu()

    # Set menu items
    menu_items = [
        {"TEXT" : "Start Game", "FUNC" : MAIN_MENU.start_game},
        {"TEXT" : "Settings", "FUNC" : blank},
        {"TEXT" : "Credits", "FUNC" : MAIN_MENU.show_credits},
        {"TEXT" : "Exit", "FUNC" : MAIN_MENU.exit_game}
    ]
    selected_item = 0

    message_box_active = False
    message_box_items = []
    message_box_selected = 0
    message_box_title = ""
    message_box_size = (400, 200)
    message_box_functions = []

    # PG-13 Image
    PG_Panel_size = (300, 150)
    PG_Panel_Image = load_image(GAME_ASSETS["images"]["PG-13"], PG_Panel_size)
    PG_Panel_rect = PG_Panel_Image.get_rect()
    PG_Panel_rect.bottomleft = (20, screen.get_height() - 20)

    # Blood 1
    Blood1_size = (800, 400)
    Blood1_Image = load_image(GAME_ASSETS["images"]["BLOOD1"], Blood1_size)
    Blood1_rect = Blood1_Image.get_rect()
    Blood1_rect.topright = (screen.get_width() - 20, 20)

    # Blood 2
    Blood2_size = (200, 200)
    Blood2_Image = load_image(GAME_ASSETS["images"]["BLOOD2"], Blood2_size)
    Blood2_rect = Blood2_Image.get_rect()
    Blood2_rect.bottomleft = (130, screen.get_height())

    # MTI Item
    MTI_size = (200, 200)
    MTI_Image = load_image(GAME_ASSETS["images"]["MTI"], MTI_size)
    MTI_rect = MTI_Image.get_rect()
    MTI_rect.center = (screen.get_width() / 2, screen.get_height() / 2)

    clock = pygame.time.Clock()
    FPS = 30

    pygame.mixer.music.load(GAME_ASSETS["sounds"]["BGM"])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    main()