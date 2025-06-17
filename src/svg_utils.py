"""
SVG 파일을 Pygame에서 사용하기 위한 유틸리티 모듈
"""
import pygame
import io
import os
from cairosvg import svg2png

class SVGAssetManager:
    """SVG 애셋을 관리하는 클래스"""
    
    def __init__(self):
        """SVG 애셋 관리자 초기화"""
        self.assets = {}
        
    def load_svg(self, name, filepath, width=None, height=None):
        """
        SVG 파일을 로드하여 Pygame 표면으로 변환
        
        Args:
            name (str): 애셋 이름
            filepath (str): SVG 파일 경로
            width (int, optional): 원하는 너비
            height (int, optional): 원하는 높이
            
        Returns:
            bool: 로드 성공 여부
        """
        try:
            if not os.path.exists(filepath):
                print(f"Error: SVG file not found at {filepath}")
                return False
                
            # SVG를 PNG로 변환
            if width and height:
                png_data = svg2png(url=filepath, write_to=None, 
                                  output_width=width, output_height=height)
            else:
                png_data = svg2png(url=filepath, write_to=None)
                
            # PNG 데이터를 Pygame 표면으로 변환
            byte_io = io.BytesIO(png_data)
            self.assets[name] = pygame.image.load(byte_io)
            return True
            
        except Exception as e:
            print(f"Error loading SVG {filepath}: {e}")
            self._create_fallback_asset(name, width, height)
            return False
    
    def _create_fallback_asset(self, name, width, height):
        """
        SVG 로딩에 실패한 경우 대체 이미지 생성
        
        Args:
            name (str): 애셋 이름
            width (int): 이미지 너비
            height (int): 이미지 높이
        """
        if width is None:
            width = 30
        if height is None:
            height = 30
            
        # 대체 이미지 생성
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if "poop" in name:
            # 똥 모양 대체 이미지
            color = (139, 69, 19)  # 갈색
            pygame.draw.ellipse(surface, color, (0, 0, width, height))
            pygame.draw.ellipse(surface, (color[0]-20, color[1]-20, color[2]-20), 
                               (width//4, height//4, width//2, height//2))
        else:
            # 기본 대체 이미지 (빨간색 X 표시)
            pygame.draw.line(surface, (255, 0, 0), (0, 0), (width, height), 2)
            pygame.draw.line(surface, (255, 0, 0), (0, height), (width, 0), 2)
        
        self.assets[name] = surface
    
    def get_asset(self, name):
        """
        저장된 애셋 가져오기
        
        Args:
            name (str): 애셋 이름
            
        Returns:
            pygame.Surface: 애셋 표면 또는 None
        """
        return self.assets.get(name)
    
    def load_player_assets(self, base_path="assets/svg/player", size=(50, 50)):
        """플레이어 관련 SVG 애셋 로드"""
        self.load_svg("player_normal", f"{base_path}/player_normal.svg", size[0], size[1])
        self.load_svg("player_left", f"{base_path}/player_left.svg", size[0], size[1])
        self.load_svg("player_right", f"{base_path}/player_right.svg", size[0], size[1])
    
    def load_obstacle_assets(self, base_path="assets/svg/obstacles"):
        """장애물(똥) 관련 SVG 애셋 로드"""
        self.load_svg("poop_small", f"{base_path}/poop_small.svg", 30, 30)
        self.load_svg("poop_medium", f"{base_path}/poop_medium.svg", 40, 40)
        self.load_svg("poop_large", f"{base_path}/poop_large.svg", 50, 50)
    
    def load_ui_assets(self, base_path="assets/svg/ui"):
        """UI 관련 SVG 애셋 로드"""
        # 한글 버튼 로드
        korean_buttons_loaded = True
        if not self.load_svg("start_button", f"{base_path}/start_button.svg", 200, 60):
            korean_buttons_loaded = False
        if not self.load_svg("restart_button", f"{base_path}/restart_button.svg", 200, 60):
            korean_buttons_loaded = False
            
        # 한글 버튼 로드 실패 시 영어 버튼 로드
        if not korean_buttons_loaded:
            print("Loading English buttons instead")
            self.load_svg("start_button", f"{base_path}/start_button_en.svg", 200, 60)
            self.load_svg("restart_button", f"{base_path}/restart_button_en.svg", 200, 60)
            
        # 기타 UI 요소 로드
        self.load_svg("pause_button", f"{base_path}/pause_button.svg", 40, 40)
        self.load_svg("life_icon", f"{base_path}/life_icon.svg", 30, 30)
        self.load_svg("score_icon", f"{base_path}/score_icon.svg", 30, 30)
    
    def load_background_assets(self, base_path="assets/svg/background", screen_size=(800, 600)):
        """배경 관련 SVG 애셋 로드"""
        self.load_svg("background", f"{base_path}/background_elements.svg", 
                     screen_size[0], screen_size[1])
        self.load_svg("background_pattern", f"{base_path}/background_pattern.svg", 100, 100)
    
    def load_all_assets(self, screen_size=(800, 600)):
        """모든 SVG 애셋 로드"""
        self.load_player_assets()
        self.load_obstacle_assets()
        self.load_ui_assets()
        self.load_background_assets(screen_size=screen_size)
