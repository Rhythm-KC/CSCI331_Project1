from env_info import Enviorment
from env_info import Tile
from env_info import Character
from env_info import moves_to_position
from env_info import available_moves
from env_info import pos_to_moves

import numpy as np


class GameState:

    def __init__(self):
        self.qbert_color = [181, 83, 40]
        self.environment = np.array(Enviorment, dtype="object")
        self.__playablestate = False
        self.ready = False
        self.__baseColor = []
        self.__knowbaseColor = False
        self.__totalreward = 0
        self.__uncheckedbox = set()
        self._counter=0

    def __updateBaseColor(self, frame):
        x, y = self.environment[5][5].pxile
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

    def __updateTile(self, tile: Tile, frame, tilePos):

        if not tile:
            return
        if (frame[tile.pxile[0] + 2][tile.pxile[1]] == self.__baseColor).all():
            tile.state = 0
            self.__uncheckedbox.add(tilePos)
        else:
            tile.state = 1
            if tilePos in self.__uncheckedbox:
                self.__uncheckedbox.remove(tilePos)

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
            if ((frame[row+2][col] == springy_color).all()
                    or (frame[row + 3][col] == springy_color).all()
                    or (frame[row + 4][col] == springy_color).all()
                    or (frame[row - 1][col] == springy_color).all()
                    or (frame[row - 2][col] == springy_color).all()
                    or (frame[row - 3][col] == springy_color).all()):
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
                    self.__updateTile(self.environment[i][j], frame, (i, j))

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

    def __finddistance(self, qbertspos, set_of_other_points):
        points = set()
        for point in set_of_other_points:
            dis = np.linalg.norm(np.array(list(qbertspos)) - np.array(list(point)))
            points.add((point, dis))
        return points

    def __getNudges(self, qbertposition, boxtogo):
        bestposition = set()
        q_x, q_y = qbertposition
        x, y = boxtogo

        val = 0
        if x > q_x and y < q_y:
            val = 1
            dx, dy = moves_to_position[5]
            bestposition.add((q_x + dx, q_y + dy))
        if x > q_x and y >= q_y:
            val = 2
            dx, dy = moves_to_position[3]
            bestposition.add((q_x + dx, q_y + dy))
        if x < q_x and y > q_y:
            val = 3
            dx, dy = moves_to_position[2]
            bestposition.add((q_x + dx, q_y + dy))
        if x < q_x and y <= q_y:
            val = 4
            dx, dy = moves_to_position[4]
            bestposition.add((q_x + dx, q_y + dy))
        if x == q_x and q_y < y:
            val = 5
            dx, dy = moves_to_position[2]
            bestposition.add((q_x + dx, q_y + dy))
            dx, dy = moves_to_position[3]
            bestposition.add((q_x + dx, q_y + dy))
        if x == q_x and q_y > y:
            val = 6
            dx, dy = moves_to_position[4]
            bestposition.add((q_x + dx, q_y + dy))
            dx, dy = moves_to_position[5]
            bestposition.add((q_x + dx, q_y + dy))
        return bestposition

    def __nudgeqbert(self, qbertspostion):
        distances = self.__finddistance(qbertspostion, self.__uncheckedbox)
        sorted_distance = sorted(distances, key=lambda x: x[1])
        bestposition = set()
        if len(sorted_distance) == 0:
            return bestposition
        for distance in sorted_distance:
            for val in self.__getNudges(qbertspostion, distance[0]):
                bestposition.add(val)
        return bestposition

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
            springy_moves = available_moves[springy_pos]
            springy_possible_position = self.__findnextpostion(springy_pos, springy_moves)
            springy_possible_position.add(tuple(springy_pos))

        safe_moves = qberts_possible_position
        if self.__isAllColorNotBase(qberts_possible_position) and qbert_pos:
            boxes_nudge = self.__nudgeqbert(qbert_pos)
            valid_nudges = boxes_nudge.intersection(safe_moves)
            valid_nudges = list(set(valid_nudges).difference(springy_possible_position))
            if len(valid_nudges) != 0:
                action = self.__position_to_move(qbert_pos, valid_nudges[0])
                return action
        
        
        
        safe_moves = list(set(safe_moves).difference(springy_possible_position))
        safe_moves = sorted(safe_moves, key=lambda x: self.environment[x[0]][x[1]].state)

        if not safe_moves:
            return 0

        action = self.__position_to_move(qbert_pos, safe_moves[0])
        return action

    def playgame(self, frame, reward):
        if reward == 100:
            self._counter=5
            self.ready = False
        if self._counter != 0:
            self._counter -= 1
            self.__knowbaseColor = False

        else:
            self.update_tiles(frame)
        if self.ready:
            toReturn = self.__getnextmove()
            return toReturn
        else:
            return 0
