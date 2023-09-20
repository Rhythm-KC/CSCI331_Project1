from enum import Enum

import numpy as np


class Tile:
  def __init__(self, state, pixle, character):
      self.state = state
      self.pxile = pixle
      self.character = character


class Character(Enum):
	QBERT = 1
	GREENGUY = 2
	SPRINGY = 3
	EMPTY = 0


enviorment = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, Tile(0, [34, 77], Character.EMPTY), None],
            [None, None, None, None, None, Tile(0, [62, 65], Character.EMPTY), Tile(0, [62, 93], Character.EMPTY), None],
            [None, None, None, None, Tile(0, [91, 53], Character.EMPTY), Tile(0, [91, 77], Character.EMPTY), Tile(0, [91, 105], Character.EMPTY), None],
            [None, None, None, Tile(0, [120, 41], Character.EMPTY), Tile(0, [120, 65], Character.EMPTY), Tile(0, [120, 93], Character.EMPTY), Tile(0, [120, 117], Character.EMPTY), None],
            [None, None, Tile(0, [149, 29], Character.EMPTY), Tile(0, [149, 53], Character.EMPTY), Tile(0, [149, 77], Character.EMPTY), Tile(0, [149, 105], Character.EMPTY), Tile(0, [139, 129], Character.EMPTY), None],
            [None, Tile(0, [178, 17], Character.EMPTY), Tile(0, [178, 41], Character.EMPTY), Tile(0, [178, 65], Character.EMPTY), Tile(0, [178, 93], Character.EMPTY), Tile(0, [178, 117], Character.EMPTY), Tile(0, [178, 141], Character.EMPTY), None],
            [None, None, None, None, None, None, None, None],
            ]


def updateTile(tile: Tile, frame, baseColor):
    if (tile==None):
        return
    if(frame[tile.pxile[0]][tile.pxile[1]]==baseColor).all():
        tile.state=0
    else:
        tile.state=1
    
    qbert_color = [181, 83, 40]
    springy_color = [146, 70, 192]
    greenGuy_color = [50, 132, 50]
    coordinate = tile.pxile.copy()
    coordinate[0] -= 7  # 4 is the height
    list_of_coordinates = [coordinate, [coordinate[0], coordinate[1] + 1], [coordinate[0], coordinate[1] - 1]]
    for coordinate in  list_of_coordinates:
        row, col = coordinate
        if (frame[row][col] == qbert_color).all():
            print(f"found qbert at {coordinate[0], coordinate[1]}")
            tile.character = Character.QBERT
            return
        if (frame[row+2][col] == springy_color).all():
            print(f"found springy at {coordinate[0], coordinate[1]}")
            tile.character=Character.SPRINGY
            return
        if (frame[row][col] == greenGuy_color).all():
            print(f"found greenGuy at {coordinate[0], coordinate[1]}")
            tile.character=Character.GREENGUY
            return
        tile.character=Character.EMPTY
        
        

