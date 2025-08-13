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
    h = Direction.NORTH
    for direction in Direction:
        #print("name:",name)
        r, c = direction.value

        print("val:",r)
