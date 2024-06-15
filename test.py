import pygame
import time

# Pygame 초기화
pygame.init()

# 전체 화면 모드 설정
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# 배경색 설정
background_color = (0, 0, 0)

# 배경 음악 파일 로드
pygame.mixer.music.load("bgm.mp3")

# 배경 음악 볼륨 설정 (0.5 = 50%)
pygame.mixer.music.set_volume(0.5)

# 배경 음악 재생 (6초 동안 페이드 인)
pygame.mixer.music.play(-1, fade_ms=6000)

# 페이드 인 효과를 위한 시간 설정
fade_in_duration = 6  # 6초
start_time = time.time()

running = True
screen.fill((255, 255, 255))
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    # 페이드 인 효과를 위해 화면 밝기를 조절
    if elapsed_time < fade_in_duration:
        alpha = int(255 * (elapsed_time / fade_in_duration))
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill(background_color)
        fade_surface.set_alpha(255 - alpha)  # 점점 투명하게
        screen.blit(fade_surface, (0, 0))
    else:
        # 페이드 인 완료 후 배경색으로 채우기
        screen.fill((255, 255, 255))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

# Pygame 종료
pygame.quit()
