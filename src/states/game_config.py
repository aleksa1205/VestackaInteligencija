import enum

class GameConfig:
    def __init__(self):
        self.current_player = 1
        self.mode = GameMode.P_VS_AI
        self.board_size = 4

class GameMode(enum.Enum):
    P_VS_AI = 1,
    PVP = 2