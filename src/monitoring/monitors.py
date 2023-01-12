import pygame
from pygame.locals import *
from core.constants import BLOCK_TYPE_INPUT, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_TRANSMITTER

from src.monitoring.constants import BLOCK_HEIGHT, BLOCK_WIDTH, COLOR_BLACK


class ConsoleMonitor:
    pass


class GUIMonitor:
    
    color_map = {
        BLOCK_TYPE_TRANSMITTER: (),
        BLOCK_TYPE_OUTPUT: (),
        BLOCK_TYPE_INPUT: (),
    }
    
    def __init__(self):
        pygame.init()
        FramePerSec = pygame.time.Clock()
        pygame.display.set_caption("Example")
        self.is_surface_created = False
    
    def render(self, map_state):
        if not self.is_surface_created:
            self.surface = pygame.display.set_mode((self._map._width * BLOCK_WIDTH, self._map._height * BLOCK_HEIGHT))
            self.surface.fill(COLOR_BLACK)
        
        self.surface.fill(COLOR_BLACK)
        for cords, block in map_state.get_map_state():
            pygame.draw.rect(
                self.surface,
                self._convert_color(block),
                (*(self._map.convert_cords((x, y))),
                BLOCK_WIDTH, BLOCK_HEIGHT))
            
    def _convert_color(self, block):
        return self.color_map.get(block.get_type())
            
        