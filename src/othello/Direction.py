from enum import Enum
class Direction(Enum):
    NORTH     = (-1,0)
    NORTHEAST = (-1,1)
    NORTHWEST = (-1,-1)
    WEST      = (0,-1)
    EAST      = (0,1)
    SOUTH     = (1,0)
    SOUTHEAST = (1,1)
    SOUTHWEST = (1,-1)

if __name__ == "__main__":
    for i in Direction:
        print(i.value)