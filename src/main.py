import pygame
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from src.Game_Menus.main_menu import main_menu

main_menu()