# 똥피하기 게임 구현 가이드라인

## 1. 개발 환경 설정
- Python 3.x 설치
- Pygame 라이브러리 설치: `pip install pygame`
- 필요한 에셋(이미지, 사운드) 준비

## 2. 주요 클래스 및 기능 구현

### settings.py
```python
# 게임 기본 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 게임 난이도 설정
INITIAL_POOP_SPEED = 3
POOP_ACCELERATION = 0.1
POOP_SPAWN_RATE = 1.0  # 초당 생성 개수
PLAYER_SPEED = 5

# 게임 상태
MENU = 0
PLAYING = 1
GAME_OVER = 2
```

### player.py
```python
import pygame
from settings import *

class Player:
    def __init__(self):
        self.image = pygame.image.load('assets/images/player.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 3
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # 화면 경계 처리
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
```

### poop.py
```python
import pygame
import random
from settings import *

class Poop:
    def __init__(self, speed):
        self.image = pygame.image.load('assets/images/poop.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = speed
        
    def update(self):
        self.rect.y += self.speed
        
    def is_offscreen(self):
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
```

### game.py
```python
import pygame
import random
import time
from settings import *
from player import Player
from poop import Poop

class Game:
    def __init__(self):
        self.state = MENU
        self.player = None
        self.poops = []
        self.score = 0
        self.poop_speed = INITIAL_POOP_SPEED
        self.last_spawn_time = 0
        self.spawn_interval = 1.0 / POOP_SPAWN_RATE
        self.font = pygame.font.Font('assets/fonts/game_font.ttf', 36)
        
        # 사운드 로드
        self.collision_sound = pygame.mixer.Sound('assets/sounds/collision.wav')
        self.game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')
        
    def start_game(self):
        self.state = PLAYING
        self.player = Player()
        self.poops = []
        self.score = 0
        self.poop_speed = INITIAL_POOP_SPEED
        self.last_spawn_time = time.time()
        pygame.mixer.music.load('assets/sounds/background.mp3')
        pygame.mixer.music.play(-1)
        
    def update(self):
        if self.state == PLAYING:
            self.player.update()
            
            # 똥 생성
            current_time = time.time()
            if current_time - self.last_spawn_time > self.spawn_interval:
                self.poops.append(Poop(self.poop_speed))
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
                    self.poops.remove(poop)
                    self.player.lives -= 1
                    self.collision_sound.play()
                    
                    if self.player.lives <= 0:
                        self.game_over()
            
            # 난이도 증가
            self.poop_speed += POOP_ACCELERATION / FPS
            
    def draw(self, screen):
        # 배경 그리기
        screen.fill(WHITE)
        
        if self.state == MENU:
            # 메뉴 화면 그리기
            title = self.font.render("똥피하기 게임", True, BLACK)
            start_text = self.font.render("시작하려면 SPACE를 누르세요", True, BLACK)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))
            
        elif self.state == PLAYING:
            # 게임 화면 그리기
            self.player.draw(screen)
            for poop in self.poops:
                poop.draw(screen)
                
            # UI 그리기
            score_text = self.font.render(f"점수: {self.score}", True, BLACK)
            lives_text = self.font.render(f"생명: {self.player.lives}", True, RED)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
            
        elif self.state == GAME_OVER:
            # 게임 오버 화면 그리기
            game_over_text = self.font.render("게임 오버!", True, RED)
            score_text = self.font.render(f"최종 점수: {self.score}", True, BLACK)
            restart_text = self.font.render("다시 시작하려면 SPACE를 누르세요", True, BLACK)
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
            
    def game_over(self):
        self.state = GAME_OVER
        pygame.mixer.music.stop()
        self.game_over_sound.play()
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state == MENU or self.state == GAME_OVER:
                    self.start_game()
```

### main.py
```python
import pygame
import sys
from settings import *
from game import Game

# Pygame 초기화
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("똥피하기 게임")
clock = pygame.time.Clock()

# 게임 객체 생성
game = Game()

# 게임 루프
while True:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_events(event)
    
    # 게임 업데이트
    game.update()
    
    # 화면 그리기
    game.draw(screen)
    
    # 화면 업데이트
    pygame.display.flip()
    
    # FPS 설정
    clock.tick(FPS)
```

## 3. 구현 시 주의사항

1. **에셋 준비**: 게임에 필요한 이미지와 사운드 파일을 미리 준비하고 적절한 폴더에 배치합니다.

2. **충돌 감지**: 정확한 충돌 감지를 위해 이미지의 투명한 부분을 고려한 마스크 충돌 감지를 구현할 수 있습니다.

3. **난이도 조절**: 게임이 너무 쉽거나 어렵지 않도록 똥의 생성 속도와 낙하 속도를 적절히 조절합니다.

4. **최적화**: 화면 밖으로 나간 객체는 메모리에서 제거하여 성능을 최적화합니다.

5. **확장성**: 코드를 모듈화하여 나중에 기능을 추가하기 쉽게 구성합니다.

## 4. 추가 기능 구현 아이디어

1. **아이템 시스템**: 방패, 속도 증가, 생명 회복 등의 아이템 추가

2. **다양한 똥**: 크기와 속도가 다른 여러 종류의 똥 추가

3. **레벨 시스템**: 시간이 지남에 따라 레벨이 올라가고 난이도가 증가

4. **최고 점수 기록**: 로컬 파일에 최고 점수를 저장하고 표시

5. **일시정지 기능**: ESC 키를 눌러 게임을 일시정지할 수 있는 기능
