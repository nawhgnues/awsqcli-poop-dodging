# 똥피하기 게임 파일 구조

```
poop_dodge/
│
├── assets/                  # 게임에 필요한 모든 자산 파일
│   ├── images/              # 이미지 파일
│   │   ├── player.png       # 플레이어 캐릭터 이미지
│   │   ├── poop.png         # 똥 이미지
│   │   ├── background.png   # 배경 이미지
│   │   └── game_over.png    # 게임 오버 화면 이미지
│   │
│   ├── sounds/              # 사운드 파일
│   │   ├── background.mp3   # 배경 음악
│   │   ├── collision.wav    # 충돌 효과음
│   │   ├── game_over.wav    # 게임 오버 효과음
│   │   └── start.wav        # 게임 시작 효과음
│   │
│   └── fonts/               # 폰트 파일
│       └── game_font.ttf    # 게임에서 사용할 폰트
│
├── src/                     # 소스 코드 파일
│   ├── main.py              # 메인 게임 실행 파일
│   ├── player.py            # 플레이어 클래스
│   ├── poop.py              # 똥 객체 클래스
│   ├── game.py              # 게임 로직 클래스
│   ├── ui.py                # UI 관련 클래스
│   └── settings.py          # 게임 설정 상수 및 변수
│
├── README.md                # 게임 설명 및 실행 방법
└── requirements.txt         # 필요한 패키지 목록 (pygame 등)
```

## 주요 파일 설명

### 1. main.py
- 게임의 진입점
- 게임 루프 실행
- 화면 초기화 및 게임 상태 관리

### 2. player.py
- 플레이어 캐릭터 클래스
- 이동 로직 및 입력 처리
- 플레이어 상태 관리

### 3. poop.py
- 똥 객체 클래스
- 생성 및 낙하 로직
- 크기 및 속도 변화

### 4. game.py
- 게임 상태 관리
- 충돌 감지
- 점수 계산
- 난이도 조절

### 5. ui.py
- 게임 UI 요소 렌더링
- 메뉴 화면
- 점수 및 생명 표시

### 6. settings.py
- 화면 크기, 색상 등 상수 정의
- 게임 설정 변수
- 난이도 관련 매개변수
