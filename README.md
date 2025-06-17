# 똥피하기 게임 (Poop Dodge Game)

SVG 그래픽을 활용한 Pygame 기반의 똥피하기 게임입니다.

## 게임 설명

플레이어는 화면 하단에서 좌우로 이동하며 위에서 떨어지는 똥을 피해야 합니다. 
똥에 맞으면 생명이 줄어들고, 생명이 모두 소진되면 게임이 종료됩니다.
시간이 지날수록 똥의 속도와 개수가 증가하여 난이도가 올라갑니다.

## 설치 방법

1. 필요한 패키지 설치:
```
pip install -r requirements.txt
```

2. 게임 실행:
```
python src/main.py
```

## 조작 방법

- **왼쪽 화살표**: 왼쪽으로 이동
- **오른쪽 화살표**: 오른쪽으로 이동
- **스페이스바**: 게임 시작/재시작
- **ESC**: 게임 종료

## 파일 구조

```
poop_dodge/
│
├── assets/
│   └── svg/
│       ├── wireframes/      # 와이어프레임 SVG
│       ├── player/          # 플레이어 캐릭터 SVG
│       ├── obstacles/       # 장애물(똥) SVG
│       ├── ui/              # UI 요소 SVG
│       └── background/      # 배경 요소 SVG
│
├── src/
│   ├── main.py             # 메인 게임 파일
│   └── svg_utils.py        # SVG 유틸리티 모듈
│
├── README.md               # 게임 설명
└── requirements.txt        # 필요한 패키지 목록
```

## 기술 스택

- Python 3.x
- Pygame
- CairoSVG (SVG를 Pygame에서 사용하기 위한 변환 라이브러리)

## 주의사항

- 이 게임은 SVG 그래픽을 사용하므로 `cairosvg` 라이브러리가 필요합니다.
- Cairo 라이브러리 설치가 필요할 수 있습니다:
  - Ubuntu/Debian: `sudo apt-get install libcairo2-dev`
  - macOS: `brew install cairo`
  - Windows: 별도의 설치 과정이 필요할 수 있습니다.

## 확장 가능한 기능

- 아이템 추가 (방패, 속도 증가, 생명 회복 등)
- 다양한 배경과 난이도 선택
- 최고 점수 기록 저장
- 다양한 플레이어 캐릭터 선택 옵션
