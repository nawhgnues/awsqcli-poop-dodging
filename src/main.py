"""
똥피하기 게임 메인 파일
SVG 그래픽을 사용한 구현
"""
import pygame
import sys
import os
import random
import time

# 필요한 모듈 가져오기
from svg_utils import SVGAssetManager

# 게임 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 게임 상태
MENU = 0
PLAYING = 1
GAME_OVER = 2

# 게임 난이도 설정
INITIAL_POOP_SPEED = 3
POOP_ACCELERATION = 0.1
POOP_SPAWN_RATE = 1.0  # 초당 생성 개수
PLAYER_SPEED = 5

class Particle:
    """충돌 효과를 위한 파티클 클래스"""
    
    def __init__(self, x, y, color=(139, 69, 19)):
        """
        파티클 초기화
        
        Args:
            x (int): 시작 x 좌표
            y (int): 시작 y 좌표
            color (tuple): 파티클 색상 (R, G, B)
        """
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-7, -2)
        self.gravity = 0.3
        self.life = 30  # 파티클 수명 (프레임 수)
        
    def update(self):
        """파티클 상태 업데이트"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity
        self.life -= 1
        
        # 크기 감소
        if self.size > 0.2:
            self.size -= 0.1
            
    def draw(self, screen):
        """
        파티클 그리기
        
        Args:
            screen (pygame.Surface): 그릴 화면
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
        
    def is_dead(self):
        """
        파티클이 수명을 다했는지 확인
        
        Returns:
            bool: 수명이 다했으면 True
        """
        return self.life <= 0

class Player:
    """플레이어 클래스"""
    
    def __init__(self, asset_manager):
        """
        플레이어 초기화
        
        Args:
            asset_manager (SVGAssetManager): SVG 애셋 관리자
        """
        self.asset_manager = asset_manager
        self.image = asset_manager.get_asset("player_normal")
        self.original_image = self.image.copy()  # 원본 이미지 저장
        self.rect = self.image.get_rect()
        
        # 화면 하단 중앙에 위치하도록 설정
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20  # 바닥에서 약간 띄움
        
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.direction = 0  # -1: 왼쪽, 0: 정지, 1: 오른쪽
        
        # 충돌 효과 관련 변수
        self.is_hit = False
        self.hit_time = 0
        self.hit_duration = 1.0  # 충돌 효과 지속 시간 (초)
        self.hit_flash_interval = 0.1  # 깜빡임 간격 (초)
        self.last_flash_time = 0
        self.is_visible = True
        self.shake_offset = 0
        self.shake_direction = 1
        
    def update(self):
        """플레이어 상태 업데이트"""
        current_time = time.time()
        
        # 충돌 효과 처리
        if self.is_hit:
            # 깜빡임 효과 - 완전히 사라지지 않고 투명도만 변경
            if current_time - self.last_flash_time > self.hit_flash_interval:
                self.is_visible = not self.is_visible
                self.last_flash_time = current_time
                
            # 흔들림 효과
            self.shake_offset = self.shake_direction * 2
            self.shake_direction *= -1
            
            # 충돌 효과 종료 체크
            if current_time - self.hit_time > self.hit_duration:
                self.is_hit = False
                self.is_visible = True
                self.shake_offset = 0
                # 원래 방향에 맞는 이미지로 복원
                self.update_direction_image()
        
        # 이전 방향 저장
        prev_direction = self.direction
        self.direction = 0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1
            
        # 방향에 따라 이미지 변경
        if not self.is_hit and self.direction != prev_direction:
            self.update_direction_image()
            
        # 화면 경계 처리
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def update_direction_image(self):
        """방향에 따라 이미지 업데이트"""
        old_center = self.rect.center
        
        if self.direction == -1:
            self.image = self.asset_manager.get_asset("player_left")
        elif self.direction == 1:
            self.image = self.asset_manager.get_asset("player_right")
        else:
            self.image = self.asset_manager.get_asset("player_normal")
            
        self.original_image = self.image.copy()
        
        # 이미지가 변경되어도 위치는 유지
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def hit_by_poop(self):
        """똥에 맞았을 때 호출되는 메서드"""
        if not self.is_hit:  # 이미 맞은 상태가 아닐 때만 처리
            self.is_hit = True
            self.hit_time = time.time()
            self.last_flash_time = self.hit_time
            self.is_visible = True  # 완전히 사라지지 않도록 수정
            
            # 맞았을 때 이미지 효과 (똥색 틴트)
            self.apply_hit_effect()
            
    def apply_hit_effect(self):
        """맞았을 때 이미지에 효과 적용 - 고양이만 똥색으로 변하게 함"""
        # 현재 이미지의 복사본 생성
        hit_image = self.original_image.copy()
        
        # 똥색 (갈색) 오버레이 생성
        overlay = pygame.Surface(hit_image.get_size(), pygame.SRCALPHA)
        overlay.fill((139, 69, 19, 100))  # 반투명 똥색
        
        # 오버레이를 이미지에 합성
        hit_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.image = hit_image
            
    def draw(self, screen):
        """
        플레이어 그리기
        
        Args:
            screen (pygame.Surface): 그릴 화면
        """
        if self.is_visible:
            # 흔들림 효과 적용 - rect 사용하여 정확한 위치에 그리기
            draw_pos = self.rect.copy()
            draw_pos.x += self.shake_offset
            screen.blit(self.image, draw_pos)
        else:
            # 깜빡임 효과 - 완전히 사라지지 않고 반투명하게 표시
            temp_img = self.image.copy()
            temp_img.set_alpha(128)  # 반투명 설정
            draw_pos = self.rect.copy()
            draw_pos.x += self.shake_offset
            screen.blit(temp_img, draw_pos)

class Poop:
    """똥 클래스"""
    
    def __init__(self, asset_manager, speed):
        """
        똥 초기화
        
        Args:
            asset_manager (SVGAssetManager): SVG 애셋 관리자
            speed (float): 떨어지는 속도
        """
        # 랜덤하게 크기 선택
        size = random.choice(["small", "medium", "large"])
        self.image = asset_manager.get_asset(f"poop_{size}")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = speed
        self.size = size  # 크기 정보 저장
        
    def update(self):
        """똥 상태 업데이트"""
        self.rect.y += self.speed
        
    def is_offscreen(self):
        """
        화면 밖으로 나갔는지 확인
        
        Returns:
            bool: 화면 밖이면 True
        """
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, screen):
        """
        똥 그리기
        
        Args:
            screen (pygame.Surface): 그릴 화면
        """
        screen.blit(self.image, self.rect)

class Button:
    """버튼 클래스"""
    
    def __init__(self, image, x, y):
        """
        버튼 초기화
        
        Args:
            image (pygame.Surface): 버튼 이미지
            x (int): x 좌표
            y (int): y 좌표
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    def is_clicked(self, pos):
        """
        버튼이 클릭되었는지 확인
        
        Args:
            pos (tuple): 마우스 위치 (x, y)
            
        Returns:
            bool: 클릭되었으면 True
        """
        return self.rect.collidepoint(pos)
        
    def draw(self, screen):
        """
        버튼 그리기
        
        Args:
            screen (pygame.Surface): 그릴 화면
        """
        screen.blit(self.image, self.rect)

class Game:
    """게임 클래스"""
    
    def __init__(self):
        """게임 초기화"""
        # Pygame 초기화
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("똥피하기 게임")
        self.clock = pygame.time.Clock()
        
        # 애셋 관리자 초기화
        self.asset_manager = SVGAssetManager()
        
        # 게임 상태 초기화
        self.state = MENU
        self.player = None
        self.poops = []
        self.particles = []  # 파티클 리스트 추가
        self.score = 0
        self.poop_speed = INITIAL_POOP_SPEED
        self.last_spawn_time = 0
        self.spawn_interval = 1.0 / POOP_SPAWN_RATE
        self.use_english_text = False  # 기본값은 한글 사용
        
        # 버튼 초기화
        self.start_button = None
        self.restart_button = None
        
        # 애셋 로드
        self.load_assets()
        
    def load_assets(self):
        """게임에 필요한 애셋 로드"""
        # SVG 애셋 로드
        self.asset_manager.load_all_assets((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 폰트 설정
        self.setup_font()
        
        # 버튼 생성
        self.start_button = Button(
            self.asset_manager.get_asset("start_button"),
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        
        self.restart_button = Button(
            self.asset_manager.get_asset("restart_button"),
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100
        )
        
        # 사운드 로드
        try:
            self.collision_sound = pygame.mixer.Sound('assets/sounds/collision.wav')
        except:
            print("Warning: Could not load collision sound.")
            self.collision_sound = None
            
        try:
            self.game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')
        except:
            print("Warning: Could not load game over sound.")
            self.game_over_sound = None
    
    def setup_font(self):
        """한글 폰트 설정"""
        # 폰트 초기화 - 한글 지원 폰트 사용
        font_loaded = False
        
        # 1. 시스템에 설치된 Noto Sans CJK 폰트 사용 시도
        try:
            self.font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 36)
            self.ui_font = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)  # UI용 작은 폰트
            font_loaded = True
            print("Using NotoSansCJK font")
        except:
            pass
            
        # 2. 시스템 기본 폰트 중 한글 지원 폰트 찾기
        if not font_loaded:
            try:
                available_fonts = pygame.font.get_fonts()
                korean_fonts = [f for f in available_fonts if f in ["notosanscjk", "malgun gothic", "gulim", "batang", "dotum"]]
                
                if korean_fonts:
                    self.font = pygame.font.SysFont(korean_fonts[0], 36)
                    self.ui_font = pygame.font.SysFont(korean_fonts[0], 24)  # UI용 작은 폰트
                    font_loaded = True
                    print(f"Using system font: {korean_fonts[0]}")
            except:
                pass
                
        # 3. 모두 실패하면 기본 폰트 사용하고 한글 텍스트를 영어로 대체
        if not font_loaded:
            print("Warning: Could not load Korean font. Using English text instead.")
            self.font = pygame.font.Font(None, 36)
            self.ui_font = pygame.font.Font(None, 24)  # UI용 작은 폰트
            self.use_english_text = True
        else:
            self.use_english_text = False
        
    def start_game(self):
        """게임 시작"""
        self.state = PLAYING
        self.player = Player(self.asset_manager)
        self.poops = []
        self.particles = []
        self.score = 0
        self.poop_speed = INITIAL_POOP_SPEED
        self.last_spawn_time = time.time()
        
        # 배경 음악 재생
        try:
            pygame.mixer.music.load('assets/sounds/background.mp3')
            pygame.mixer.music.play(-1)
        except:
            print("Warning: Could not load background music.")
        
    def create_particles(self, x, y, count=20, color=(139, 69, 19)):
        """
        파티클 생성
        
        Args:
            x (int): 파티클 생성 x 좌표
            y (int): 파티클 생성 y 좌표
            count (int): 생성할 파티클 수
            color (tuple): 파티클 색상 (R, G, B)
        """
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
        
    def update(self):
        """게임 상태 업데이트"""
        if self.state == PLAYING:
            self.player.update()
            
            # 똥 생성
            current_time = time.time()
            if current_time - self.last_spawn_time > self.spawn_interval:
                self.poops.append(Poop(self.asset_manager, self.poop_speed))
                self.last_spawn_time = current_time
                
            # 똥 업데이트 및 충돌 체크
            for poop in self.poops[:]:
                poop.update()
                
                # 화면 밖으로 나간 똥 제거 및 점수 증가
                if poop.is_offscreen():
                    self.poops.remove(poop)
                    self.score += 1
                    
                # 충돌 체크
                if self.player.rect.colliderect(poop.rect):
                    # 충돌 위치에 파티클 생성
                    collision_x = (self.player.rect.centerx + poop.rect.centerx) // 2
                    collision_y = (self.player.rect.top + poop.rect.bottom) // 2
                    
                    # 똥 크기에 따라 파티클 수 조절
                    if poop.size == "small":
                        particle_count = 10
                    elif poop.size == "medium":
                        particle_count = 15
                    else:  # large
                        particle_count = 20
                        
                    self.create_particles(collision_x, collision_y, particle_count)
                    
                    # 플레이어 충돌 효과 적용
                    self.player.hit_by_poop()
                    
                    # 충돌 사운드 재생
                    if self.collision_sound:
                        self.collision_sound.play()
                    
                    # 똥 제거 및 생명력 감소
                    self.poops.remove(poop)
                    self.player.lives -= 1
                    
                    if self.player.lives <= 0:
                        self.game_over()
            
            # 파티클 업데이트
            for particle in self.particles[:]:
                particle.update()
                if particle.is_dead():
                    self.particles.remove(particle)
            
            # 난이도 증가
            self.poop_speed += POOP_ACCELERATION / FPS
            
    def draw(self):
        """게임 화면 그리기"""
        # 배경 그리기
        self.screen.blit(self.asset_manager.get_asset("background"), (0, 0))
        
        if self.state == MENU:
            # 메뉴 화면 그리기
            title_text = "똥피하기 게임" if not self.use_english_text else "Poop Dodge Game"
            title = self.font.render(title_text, True, BLACK)
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
            
            # 시작 버튼 그리기
            self.start_button.draw(self.screen)
            
        elif self.state == PLAYING:
            # 게임 화면 그리기
            self.player.draw(self.screen)
            
            # 똥 그리기
            for poop in self.poops:
                poop.draw(self.screen)
                
            # 파티클 그리기
            for particle in self.particles:
                particle.draw(self.screen)
                
            # UI 그리기
            score_text = self.ui_font.render("점수: " + str(self.score) if not self.use_english_text else "Score: " + str(self.score), True, BLACK)
            lives_text = self.ui_font.render("HP: " + str(self.player.lives), True, RED)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
            
            # 생명 아이콘 그리기
            life_icon = self.asset_manager.get_asset("life_icon")
            for i in range(self.player.lives):
                self.screen.blit(life_icon, (SCREEN_WIDTH - 40 - i * 35, 50))
            
        elif self.state == GAME_OVER:
            # 게임 오버 화면 그리기
            game_over_text = self.font.render("게임 오버!" if not self.use_english_text else "Game Over!", True, RED)
            score_text = self.ui_font.render("최종 점수: " + str(self.score) if not self.use_english_text else "Final Score: " + str(self.score), True, BLACK)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            
            # 재시작 버튼 그리기
            self.restart_button.draw(self.screen)
            
    def game_over(self):
        """게임 오버 처리"""
        self.state = GAME_OVER
        
        # 배경 음악 중지
        pygame.mixer.music.stop()
        
        # 게임 오버 사운드 재생
        if self.game_over_sound:
            self.game_over_sound.play()
        
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                    
                if event.key == pygame.K_SPACE:
                    if self.state == MENU or self.state == GAME_OVER:
                        self.start_game()
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if self.state == MENU and self.start_button.is_clicked(pos):
                    self.start_game()
                    
                if self.state == GAME_OVER and self.restart_button.is_clicked(pos):
                    self.start_game()
                    
        return True
        
    def run(self):
        """게임 실행"""
        running = True
        
        while running:
            # 이벤트 처리
            running = self.handle_events()
            
            # 게임 업데이트
            self.update()
            
            # 화면 그리기
            self.draw()
            
            # 화면 업데이트
            pygame.display.flip()
            
            # FPS 설정
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    # 필요한 디렉토리 확인
    if not os.path.exists("assets/svg"):
        print("Error: assets/svg directory not found!")
        print("Please make sure all SVG assets are in the correct location.")
        sys.exit(1)
        
    # 게임 실행
    game = Game()
    game.run()
