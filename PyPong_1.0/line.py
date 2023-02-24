
DEBUG_PRINT = True
def dprint(*args):
    if DEBUG_PRINT:
        print( " ".join(str(i) for i in args) ) #make a list of strings and then .join()


class Line:
    """Equation of a straight line is: y = mx + b"""

    def __init__(self, endpoint1, endpoint2):

        self.point1 = endpoint1
        self.point2 = endpoint2

        #determine top and bottom (y coords) values
        if self.point1[1] < self.point2[1]:
            self.top = self.point1[1]
            self.bottom = self.point2[1]
        else:
            self.top = self.point2[1]
            self.bottom = self.point1[1]

        #determine left and right (x coords) values
        if self.point1[0] < self.point2[0]:
            self.left = self.point1[0]
            self.right = self.point2[0]
        else:
            self.left = self.point2[0]
            self.right = self.point1[0]

        #horizontal and vertical checks to prevent division by zero with slope
        if self.point1[1] == self.point2[1]:
            self.isHorizontal = True
        else:
            self.isHorizontal = False
        
        if self.point1[0] == self.point2[0]:
            self.isVertical = True
        else:
            self.isVertical = False

        if not self.isVertical: #vertical? prevents division by zero
            self.delta_y = self.point2[1] - self.point1[1]
            self.delta_x = self.point2[0] - self.point1[0]
            self.m = self.delta_y / self.delta_x

            #b = y - mx
            self.b = self.point1[1] - (self.m * self.point1[0])

            #dprint(f"Equation: y = {self.m}x + {self.b}")


    def solveForX(self, y_input):
        """returns: x = (y - b)/m"""
        if self.isVertical:
            if (y_input >= self.top) and (y_input <= self.bottom):
                return self.point1[0]
            else:
                return None
            
        elif self.isHorizontal:
            if (y_input == self.point1[1]):
                return list(range(self.left, self.right+1))
            else:
                return None
        else:
            return (y_input - self.b) / self.m

    def solveForY(self, x_input):
        """returns: y = mx + b"""
        if self.isVertical:
            dprint("solveForY, self.isVertical:", self.isVertical)
            if (x_input == self.point1[0]):
                return list(range(self.top, self.bottom+1))
            else:
                return None
        elif self.isHorizontal:
            dprint("solveForY, self.isHorizontal:", self.isHorizontal)
            if (x_input >= self.left) and (x_input <= self.right):
                return self.point1[1]
            else:
                return None
        else:
            return (self.m * x_input) + self.b

    def intersectsVerticalLine(self, _Line):
        """Returns bool and intersection point"""
        if _Line.point1[0] != _Line.point2[0]:
            raise ValueError("_Line is not vertical")

        else:
            y_intersection = self.solveForY(_Line.point1[0])
            dprint("y_intersection:", y_intersection)

            if y_intersection == None:
                return False, None
            elif (y_intersection >= _Line.top) and (y_intersection <= _Line.bottom):
                return True, (self.solveForX(y_intersection), y_intersection)
            else:
                return False, None


    def intersectsHorizontalLine(self, _Line):
        """Returns bool and intersection point"""
        if _Line.point1[1] != _Line.point2[1]:
            raise ValueError("_Line is not horizontal")

        else:
            x_intersection = self.solveForX(_Line.point1[1])
            dprint("x_intersection:", x_intersection)
            
            if x_intersection == None:
                return False, None
            elif (x_intersection >= _Line.left) and (x_intersection <= _Line.right):
                return True, (self.solveForY(x_intersection), x_intersection)
            else:
                return False, None


if __name__ == "__main__":

    Line_1 = Line((12,7), (8,11))
    Line_2 = Line((10,4), (7,10))
    Vertical_Line = Line((9,8), (9, 11))
    Hor_Line = Line((4,8), (9,8))

    print("Line_1.intersectsVerticalLine(Vertical_Line):",
          Line_1.intersectsVerticalLine(Vertical_Line))

    print("Line_1.intersectsHorizontalLine(Hor_Line):",
          Line_1.intersectsHorizontalLine(Hor_Line))

    print("Line_2.intersectsVerticalLine(Vertical_Line):",
          Line_2.intersectsVerticalLine(Vertical_Line))

    print("Line_2.intersectsHorizontalLine(Hor_Line):",
          Line_2.intersectsHorizontalLine(Hor_Line))
