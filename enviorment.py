from enum import Enum


class Tile:
  def __init__(self, state, pixle,character):
    self.state = state
    self.pxile = pixle
    self.character=character

class Character(Enum):
    QBERT = 1
    GREENGUY = 2
    SPTRINGY = 3
    EMPTY = 0

enviorment= [
            [None,None,None,None,None,None,None,None],
            [None,None,None,None,None,None,Tile(0,[34,77],Character.EMPTY),None],
            [None,None,None,None,None,Tile(0,[62,65],Character.EMPTY),Tile(0,[62,93],Character.EMPTY),None],
            [None,None,None,None,Tile(0,[91,53],Character.EMPTY),Tile(0,[91,77],Character.EMPTY),Tile(0,[91,105],Character.EMPTY),None],
            [None,None,None,Tile(0,[120,41],Character.EMPTY),Tile(0,[120,65],Character.EMPTY),Tile(0,[120,93],Character.EMPTY),Tile(0,[120,117],Character.EMPTY),None],
            [None,None,Tile(0,[149,29],Character.EMPTY),Tile(0,[149,53],Character.EMPTY),Tile(0,[149,77],Character.EMPTY),Tile(0,[149,105],Character.EMPTY),Tile(0,[139,129],Character.EMPTY),None],
            [None,Tile(0,[178,17],Character.EMPTY),Tile(0,[178,41],Character.EMPTY),Tile(0,[178,65],Character.EMPTY),Tile(0,[178,93],Character.EMPTY),Tile(0,[178,117],Character.EMPTY),Tile(0,[178,141],Character.EMPTY),None],
            [None,None,None,None,None,None,None,None],
            ]
