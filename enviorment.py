from env_info import Enviorment
from env_info import Tile
from env_info import Character
from env_info import moves_to_position
from env_info import available_moves
from env_info import pos_to_moves

import numpy as np
import random


class GameState:

    def __init__(self):
        self.qbert_color = [181, 83, 40]
        self.environment = np.array(Enviorment, dtype="object")
        self.__baseColor = []
        self.__playablestate = False
        self.ready = False
        self.__baseColor = []
        self.__knowbaseColor = False

    def __updateBaseColor(self, frame):
        x, y = self.environment[1][6].pxile
        self.__baseColor = frame[x][y]
        self.__knowbaseColor = True
        assert (len(self.__baseColor) == 3)

    def __waitForQbet(self, frame):
        if not self.ready:
            coordinate = self.environment[1][6].pxile.copy()
            list_of_coordinates = [coordinate, [coordinate[0], coordinate[1] + 1], [coordinate[0], coordinate[1] - 1]]
            for coordinate in list_of_coordinates:
                row, col = coordinate
                if (frame[row][col] == self.qbert_color).all():
                    self.ready = True
                    return

    def __updateTile(self, tile: Tile, frame):

        if not tile:
            return
        if (frame[tile.pxile[0]][tile.pxile[1]] == self.__baseColor).all():
            tile.state = 0
        else:
            tile.state = 1

        qbert_color = [181, 83, 40]
        springy_color = [146, 70, 192]
        greenGuy_color = [50, 132, 50]
        coordinate = tile.pxile.copy()
        coordinate[0] -= 7  # 4 is the height
        list_of_coordinates = [coordinate, [coordinate[0], coordinate[1] + 1], [coordinate[0], coordinate[1] - 1]]
        for coordinate in list_of_coordinates:
            row, col = coordinate
            if (frame[row][col] == qbert_color).all():
                tile.character = Character.QBERT
                return
            if (frame[row+2][col] == springy_color).all():
                tile.character = Character.SPRINGY
                return
            if (frame[row][col] == greenGuy_color).all():
                tile.character = Character.GREENGUY
                return
            tile.character = Character.EMPTY

    def update_tiles(self, frame):

        if not self.__knowbaseColor:
            self.__updateBaseColor(frame)

        if not self.ready:
            self.__waitForQbet(frame)

        if self.ready:
            for i in range(len(self.environment)):
                for j in range(len(self.environment[0])):
                    self.__updateTile(self.environment[i][j], frame)

    def __getCharacter(self, character):
        for i in range(len(self.environment)):
            for j in range(len(self.environment[0])):
                box = Enviorment[i][j]
                if not box:
                    continue
                if box.character == character:
                    return (i, j)

    def __findnextpostion(self, current_postion, moves):
        positions = set()
        for move in moves:
            x, y = current_postion
            dx, dy = moves_to_position[move]
            positions.add((x + dx, y + dy))
        return positions

    def __position_to_moves(self, current_pos, other_pos):
        actions = []
        for pos in other_pos:
            moves = (pos[0] - current_pos[0],   pos[1] - current_pos[1])
            actions.append(pos_to_moves[moves])
        return actions

    def __position_to_move(self, current_pos, other_pos):
        move = (other_pos[0] - current_pos[0],   other_pos[1] - current_pos[1])
        return pos_to_moves[move]

    def __isAllColorNotBase(self, positions):
        for position in positions:
            x, y = position
            if self.environment[x][y].state == 0:
                return False
        return True

    def __getnextmove(self):

        qbert_pos = self.__getCharacter(Character.QBERT)
        springy_pos = self.__getCharacter(Character.SPRINGY)
        qberts_possible_position = set()
        springy_possible_position = set()

        springy_moves = []
        if qbert_pos:
            qbert_moves = available_moves[qbert_pos]
            qberts_possible_position = self.__findnextpostion(qbert_pos, qbert_moves)
        if springy_pos:
            springy_possible_position = self.__findnextpostion(springy_pos, springy_moves)
            springy_possible_position.add(tuple(springy_pos))

        safe_moves = list(qberts_possible_position.difference(springy_possible_position))
        if not safe_moves:
            return 0
        safe_moves = sorted(safe_moves, key=lambda x: self.environment[x[0]][x[1]].state)
        move_selector = 0
        if self.__isAllColorNotBase(safe_moves):
            move_selector = random.randint(0, len(safe_moves)-1)

        action = self.__position_to_move(qbert_pos, safe_moves[move_selector])
        return action

    def playgame(self, frame):
        self.update_tiles(frame)
        if self.ready:
            return self.__getnextmove()
        else:
            return 0
