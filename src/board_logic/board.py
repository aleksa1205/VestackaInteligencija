from typing import List
import pygame
from math import sqrt

from src.board_logic.board_utility import get_right_peg, get_bot_right_peg, get_bot_left_peg
from src.board_logic.ui_elements.board_background import BoardBackground
from src.board_logic.game_state import GameState
from src.board_logic.ui_elements.rubber_band_utils import RubberBandUtils
from src.board_logic.ui_elements.triangle_utils import TriangleUtils
from src.states.game_config import GameConfig
from src.ui_components.colors import rubber_band_color, player1_color, player2_color
from src.board_logic.ui_elements.stub import Stub
from src.states.transparent import Transparent

class Board:
    def __init__(self, game, game_config : GameConfig, shared_data):
        self.game = game
        self.game_config = game_config
        self.board_size = game_config.board_size
        self.d = 0
        self.init_d()
        self.h = self.d * sqrt(3) / 2
        self.stub_radius = 6
        self.shared_data = shared_data
        self.x_start = (self.game.SCREEN_WIDTH - (((self.board_size - 1) * 2) * self.d)) / 2
        self.y_start = (self.game.SCREEN_HEIGHT - (((self.board_size - 1) * 2) * self.h)) / 2
        self.y_start = self.y_start if self.board_size < 8 else self.y_start + 50
        self.board_bg = BoardBackground(self)

        self.message_start_time = None
        # Funckionalnosti
        self.pegs = []
        # pamti samo indekse board-a, koristi se da bi prosledio game state-u
        self.peg_indexes = []
        self.pegs_init()
        self.selected_pegs : List[Stub] = []

        self.game_state = GameState(self.board_size, self.peg_indexes, game_config.current_player)

    # Metode klase
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and len(self.selected_pegs) == 1:
                    self.selected_pegs[0].reset_clicked()
                    self.selected_pegs.clear()

        for peg in self.pegs:
            if peg.check_click(player1_color if self.game_state.current_player == 1 else player2_color):
                self.selected_pegs.append(peg)

        # Izabrana su 2 stuba, znaci odigraj potez
        if len(self.selected_pegs) == 2:
            self.make_move(self.selected_pegs[0].index, self.selected_pegs[1].index)
            # Izbrisemo selektovane stubove
            self.selected_pegs[0].reset_clicked()
            self.selected_pegs[1].reset_clicked()
            self.selected_pegs.clear()

    def render(self, surface):
        self.board_bg.render(surface)
        for stub in self.pegs: stub.render()

        RubberBandUtils.draw_rubber_bands(surface, self.game_state.paths, self, self.stub_radius, rubber_band_color)

        TriangleUtils.draw_triangles(surface, self)

        # crtanje povlacenje gumice
        if len(self.selected_pegs) == 1:
            mouse_pos = pygame.mouse.get_pos()
            RubberBandUtils.draw_rubber_band(surface, self.selected_pegs[0].pos, mouse_pos, self.stub_radius, rubber_band_color)

    # Pomocne metode
    def init_d(self):
        if self.board_size == 4: self.d = 60
        elif self.board_size == 5: self.d = 55
        elif self.board_size == 6: self.d = 50
        elif self.board_size == 7: self.d = 43
        elif self.board_size == 8: self.d = 40
        else: self.d = 45

    def pegs_init(self):
        for i in range(2 * self.board_size - 1):
            for j in range(2 * self.board_size - 1 - abs(self.board_size - 1 - i)):
                self.pegs.append(Stub(self.game, (i, j), self.stub_radius, self.board_size, self.d, self.h, self.x_start, self.y_start))
                self.peg_indexes.append((i, j))
        self.shared_data['pegs'] = self.pegs

    def get_end_peg(self, start, direction):
        curr_peg = start
        path = [start]

        for i in range(3):
            curr_peg = direction(self.board_size, curr_peg)
            path.append(curr_peg)

        return tuple(path), curr_peg

    def check_length(self, stub1: tuple, stub2: tuple):
        x = abs(stub2[0] - stub1[0])
        y = abs(stub2[1] - stub1[1])
        return True if x == 3 or y == 3 else False

    def is_valid_input(self, start_peg, end_peg):
        if self.check_length(start_peg, end_peg) is False:
            return False, "Rubber band must go through 4 pegs!"

        # Idemo u sva tri pravca: desno, dole desno i dole levo
        # funkcija nam vraca zadnji stub i putanju do tog stuba
        right_path, right_end_peg = self.get_end_peg(start_peg, get_right_peg)
        bot_right_path, bot_right_end_peg = self.get_end_peg(start_peg, get_bot_right_peg)
        bot_left_path, bot_left_end_peg = self.get_end_peg(start_peg, get_bot_left_peg)

        # proveravamo da li je drugi selektovan stub jedan on pronadjenih
        if end_peg == right_end_peg: result = right_path
        elif end_peg == bot_right_end_peg: result = bot_right_path
        elif end_peg == bot_left_end_peg: result = bot_left_path
        else: return False, "You can only stretch in those directions: Right, Down Right and Down Left"

        # da li gumica vec razvucena izmedju izabrana dva stuba
        if result in self.game_state.paths:
            return False, "There is already rubber band on those pegs!"

        return result, ''

    def make_move(self, start_peg: tuple, end_peg: tuple):
        # Provaravamo da li je validan input.
        peg_path, error_msg = self.is_valid_input(start_peg, end_peg)

        # Ako nije javljamo gresku
        if not peg_path:
            error_state = Transparent(self.game, error_msg, self.pegs)
            error_state.enter_state()
            return

        # Ako je validan input funkcija nam je vratila korektnu putanju do end_peg.
        # Sa tom informacijom mozemo da promenimo Game State
        self.game_state.update_state(peg_path)

        # Renderujemo novi state za uspesno odigran potez
        self.shared_data['turn_played'] = True

        # Generismo sve moguce poteze za minmax algo koji ce nam kasnije biti potreban
        all_moves = self.game_state.generate_all_possible_states()
        print(self.game_state.paths)
        print()
        for move in all_moves:
            print(move.player_points)