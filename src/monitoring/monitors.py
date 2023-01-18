import pygame
from pygame.locals import *
from src.core.individual import Individual
from src.core.constants import BLOCK_TYPE_INPUT, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_REGULATOR, \
    BLOCK_TYPE_TRANSMITTER, BLOCK_TYPE_TRIGGER
from src.monitoring.constants import BLOCK_HEIGHT, BLOCK_WIDTH, COLOR_BLACK
import time

class ConsoleMonitor:
    pass


class GUIMonitor:
    
    def __init__(self, bot_count):
        pygame.init()
        FramePerSec = pygame.time.Clock()
        pygame.display.set_caption("Example")
        
        self.surface = pygame.display.set_mode(
            (Individual.DEFAULT_MAP_WIDTH * bot_count * BLOCK_WIDTH, Individual.DEFAULT_MAP_HEIGHT * bot_count * BLOCK_HEIGHT))
        self.surface.fill(COLOR_BLACK)
    
    def render_map(self, uuid, map_state):
        self.surface.fill(COLOR_BLACK)
        
        for cords, block in map_state.get_map_state().items():
            pygame.draw.rect(
                self.surface,
                self._convert_color(block),
                pygame.Rect(*self.convert_cords(uuid, cords), BLOCK_WIDTH, BLOCK_HEIGHT)
            )
        pygame.display.update()
            
    def convert_cords(self, uuid, cords):
        return cords[0] * BLOCK_WIDTH, cords[1] * BLOCK_HEIGHT
    
    def _convert_color(self, block):
        if block.get_type() == BLOCK_TYPE_INPUT:
            if block.is_active():
                return (255, 241, 0)
            else:
                return (128, 124, 55)
 
        elif block.get_type() == BLOCK_TYPE_OUTPUT:
            if block.is_active():
                return (200, 0, 255)
            else:
                return (129, 70, 145)
        
        elif block.get_type() == BLOCK_TYPE_TRANSMITTER:
            if block.is_active():
                return (17, 12, 242)
            elif block.is_fading():
                return (149, 147, 250)
            else:
                return (255, 255, 255)
        
        elif block.get_type() == BLOCK_TYPE_REGULATOR:
            if block.is_active():
                return (255, 0, 0)
            else:
                return (0, 255, 26)

        elif block.get_type() == BLOCK_TYPE_TRIGGER:
            if block.is_active():
                return (219, 142, 48)
            else:
                return (59, 38, 12)