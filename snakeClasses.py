import random

def signFunction(x):
    # returns the sign of x
    if (x >= 0):
        return 1
    else:
        return -1

def abs(x):
    # returns the abs value of x
    if (isinstance(x, int)):
        return int((x**2)**0.5)
    else:
        return (x**2)**0.5

def roundHalfUp(d):
    # rounding function for floats
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class coordinate:
    # reprents a grid in the app
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return str((self.x, self.y))

    def __eq__(self, z):
        if (isinstance(z, self.__class__) and 
            self.x == z.x and 
            self.y == z.y):
            return True
        else:
            False
    
    def __hash__(self):
        return hash((self.x, self.y))

class velocity(coordinate):
    # same methods as coordinate
    pass

class direction(velocity):
    def __init__(self, x, y):
        # this snake does not move diagonally
        #  so only one vector should be none zero
        if (x != 0 and y != 0):
            print("invalid direction")
        elif(x == 0 and y == 0):
            x = x
            y = y
        else:
            # calclate unit vectors
            if (x != 0):
                x = int(signFunction(x)*x/x)
                y = y
            else:
                y = int(signFunction(y)*y/y)
                x = x
        super().__init__(x, y)

    def vert(self):
        # returns True if the y unit vector is non-zero
        #  the snake is travelling up and down
        if (self.x == 0 and self.y == 0):
            return print("neither")
        elif (self.y != 0):
            return True
        else:
            return False

class segment():
    # each segment will be a turning point in the body of the snake

    def __init__(self, 
                 coordinate: coordinate = None, 
                 direction: direction = None,
                 size: int = 1):

        # x, y needs to be a valid coordinate or both None
        if not ((coordinate is None) ^ (direction is None)):
            self.coordinate = coordinate
            self.direction = direction
            self.size = size
            self.next = None
            self.prev = None
        else:
            print ("invalid segment")
           
    def move(self, speed = 1):
        # update coordinates based on velocity
        if (self.coordinate is None ):
            print("Segment can't be moved")
        s = speed
        self.coordinate = coordinate(self.x+self.dx*s, 
                                     self.y+self.dy*s)

    def __repr__(self):
        return str(((self.coordinate),(self.direction)))

    def __eq__(self, seg):
        if (isinstance(seg, segment)):
            return (self.coordinate == seg.coordinate 
                 and self.direction == seg.direction)
        
    @property 
    def x(self):
        return self.coordinate.x
    
    @x.setter
    def x(self, newX):
        y = self.coordinate.y
        self.coordinate = coordinate(newX, y)

    @property 
    def y(self):
        return self.coordinate.y
    
    @y.setter
    def y(self, newY):
        x = self.coordinate.x
        self.coordinate = coordinate(x, newY)

    @property 
    def dx(self):
        return self.direction.x
    
    @dx.setter
    def dx(self, newX):
        y = self.direction.y
        self.direction = direction(newX, y)

    @property 
    def dy(self):
        return self.direction.y
    
    @dy.setter
    def dy(self, newY):
        x = self.direction.x
        self.direction = direction(x, newY)


class apple(segment):
   
    def __init__(self, 
                 coordinate: coordinate = None, 
                 size: int = 5):
        super().__init__(coordinate, direction(0, 0), size)
        self.colour = 'red'
    
    def spawnApple(size, width, height, boundary):
            s = size
            (ax0, ax1, ay0, ay1) = (0 + s + boundary, width - s - boundary,
                                    0 + s + boundary, height - s - boundary)
            x = roundHalfUp(boundary + random.random() * (ax1 - ax0))
            y = roundHalfUp(boundary + random.random() * (ay1 - ay0))
            return apple(coordinate(x, y), size)
    
class snake:
    # implement snake to be a doubly linked list of turning points and
    #  let the game draw the connecting lines beteween the points
    # when turning, add a segment to be the new head with new directions
    # when moving, move the last segment. If the last segment meets the second
    #  last segment, pop the last segment
    # It's easier to pop and add to both ends with doubly linked list
    # Keep track of both the head and the tail so we can quickly access
    def __init__(self):
        self.head = segment() # first head will be an empty segment
        self.tail = None
        self.speed = 1
        self.width = 11
        self.size = self.width//2
        self.points = set()
        self.dead = False
    
    def len(self):
        counter = 0
        curNode = self.head
        while curNode.next != None:
            counter += 1
            curNode = curNode.next
        return counter

    def addToBeginning(self, seg):
        if (not isinstance(seg, segment)):
            print("invalid head")
        head = self.head
        if (head.next != None):
            curHead = head.next
            seg.prev = head
            seg.next = curHead
            curHead.prev = seg
        else:
            # if snake is empty update tail to be seg as well
            self.tail = seg
            seg.prev = head
        head.next = seg
        self.updatePoints()

    def addToEnd(self, seg):
        if (not isinstance(seg, segment)):
            print("invalid tail")
        head = self.head
        curTail = self.tail
        if (curTail != None):
            curTail.next = seg
            seg.prev = curTail
        else:
            # if snake is empty
            head.next = seg
            seg.prev = head
        self.tail = seg
        self.updatePoints()

    def __repr__(self):
        # print snake as a list for debugging
        snakePrint = []
        curNode = self.head
        while curNode.next != None:
            curNode = curNode.next
            snakePrint.append([curNode.coordinate,curNode.direction])
        return str(snakePrint)
    
    def __eq__(self, snk):
        # two snakes are equal if same type, lenth, and segments
        if (isinstance(snk,snake)) and self.len() == snk.len():
            curXHead = self.head
            curYHead = snk.head
            counter = self.len()
            while counter > 0:
                xSeg = curXHead.next
                ySeg = curYHead.next
                if (xSeg != ySeg):
                    return False
                counter -= 1
            
            return True

    def popTail(self):
        self.pop(self.len())

    def popFromEnd(self, n, l):
        # for large pop index, counts from the end of the list
        #  unnecessary for small snake but faster for large
        n = l - n + 1
        prevTail = self.tail
        tail = None
        while n > 0:
            tail = prevTail
            prevTail = prevTail.prev
            n -= 1
        if (tail.next is None):
            prevTail.next = None
            self.tail = prevTail
            tail.prev = None
        else:
            tail.next.prev = prevTail
            prevTail.next = tail.next
            tail.next = None
            tail.prev = None

    def popFromBeginning(self, n):
        # pop segment, counting from beginning
        head = None
        nextHead = self.head
        while n > 0:
            head = nextHead
            nextHead = nextHead.next
            n -= 1
        if (nextHead.next is None):
            head.next = None
            nextHead.prev = None
            self.tail = nextHead
        else:
            head.next = nextHead.next
            nextHead.next.prev = head
            nextHead.next = None
            nextHead.prev = None

    def pop(self, n):
        # pop nth segment and count from beginning or the end
        #  based on which end n is closer to
        l = self.len()
        if n < 1 or n > l:
            print('n not valid')
        else:
            if (n > l//2):
                self.popFromEnd(n, l)
            else:
                self.popFromBeginning(n)
        self.updatePoints()

    def move(self, v = 1):
        # update the coordinate of the snake when moving
        head = self.head.next
        tail = self.tail
        head.move(v)
        # update the coordinates of the snake
        self.updatePoints
        # check if snake died
        self.ateMyself()
        if (self.dead == True):
            return
        if (not head is tail):
            # snake has >1 segment so move the tail as well
            if (tail.direction.vert()):
                # pop the tail if it moves to or past the second last segment
                if (abs(tail.y - tail.prev.y) <= abs(tail.dy*v)):
                    self.popTail()
                else:
                    tail.move(v)
            else:
                # pop the tail if it moves to or past the second last segment
                if (abs(tail.x - tail.prev.x) <= abs(tail.dx*v)):
                    self.popTail()
                else:
                    tail.move(v)
        self.updatePoints()

    def moveSteps(self, n = 1):
        # for testing purposes
        for _ in range(0,n):
            self.move()
            print(x)

    def changeDirections(self, direction):
        d = direction
        head = self.head.next
        Vx, Vy = head.dx, head.dy
        if ((d.x == 0 and d.y == 0) or (d.x != 0 and d.y != 0)):
            return # invalid direction for directional change
        elif ((Vx == 0 and d.x !=0) or (Vy == 0 and d.y != 0)):
            # only allows change if the dx and dy before and after are diff
            #  will not allow reversing of snake
            if (self.len() == 1):
                head.direction = d
            else:
                newHead = segment(head.coordinate, d, self.size)
                head.direction = newHead.direction
                self.addToBeginning(newHead)
        else:
            return
    
    def grow(self, appleSize):
        # when snake eats the apple
        s = appleSize
        sHead = self.head.next
        if (sHead is self.tail):
            self.addToBeginning(
                segment(coordinate(sHead.x + sHead.dx*s, 
                                   sHead.y + sHead.dy*s),
                        direction(sHead.dx, sHead.dy),
                        self.size)
            )
        else:
            sHead.coordinate = coordinate(
                                        sHead.x + sHead.dx*s,
                                        sHead.y + sHead.dy*s)
            self.updatePoints()

    def touching(self, thing, radius):
        # returns true when snake head is within certain radius of thing
        r = radius
        c = thing.coordinate
        sHead = self.head.next
        if (((sHead.x - c.x)**2 + 
             (sHead.y - c.y)**2)**0.5 
            <= r):
            return True
        else:
            return False

    def updatePoints(self):
        # extrapolates all coordinates of snake from the key segments
        #  used for checking death
        if self.len() < 1:
            return print("snake of 0 length")
        updatedSet = set()
        seg2 = self.head.next
        seg1 = self.head
        while seg2.next != None:
            seg1 = seg2
            seg2 = seg2.next
            if(seg2.direction.vert() == True):
                for i in range(seg1.y, seg2.y, -seg2.dy):
                    updatedSet.add(coordinate(seg2.x, i))
            else:
                for i in range(seg1.x, seg2.x, -seg2.dx):
                    updatedSet.add(coordinate(i, seg2.y))
            updatedSet.add(seg2.coordinate)
            self.points = updatedSet
 
    def dead(self):
        return self.dead
    
    def outtaBounds(self, x0, y0, x1, y1):
        head = self.head.next
        if (head.x <= x0 or head.x >= x1 or head.y <= y0 or head.y >= y1):
            self.dead = True

    def ateMyself(self):
        if (self.head.next.coordinate in self.points):
            self.dead = True




if (__name__ == '__main__'):

    print('testing')
    def segmentTest():
        x = segment(coordinate(3,4), direction(0,-1))
        print(x.coordinate)
        print(x.direction)

    segmentTest()

    xn1 = segment(coordinate(0,0), direction(0,-1))
    xn2 = segment(coordinate(0,2), direction(0,-1))
    xn3 = segment(coordinate(4,2), direction(-1,0))

    x = snake()
    x.addToEnd(xn1)
    x.addToEnd(xn2)
    x.addToEnd(xn3)

    print(x)
    x.moveSteps(3)
    x.move()
    x.changeDirections(direction(-1,0))
    print(x)
    x.moveSteps()
    x.changeDirections(direction(-1,0))
    x.moveSteps()
    # dont add head
    print('no change')
    x.changeDirections(direction(-1,0))
    x.moveSteps()
    # dont add head in opposite direction
    print('no change')
    x.changeDirections(direction(1,0))
    x.moveSteps()
    # invalid change
    print('no change')
    x.changeDirections(direction(1,1))
    x.moveSteps()
    x.changeDirections(direction(0,1))
    x.moveSteps()
    x.changeDirections(direction(1,0))
    x.moveSteps()
    x.changeDirections(direction(0,-1))
    x.moveSteps(6)

    x = snake()
    x.addToBeginning(segment(coordinate(1,3), direction(0,1)))
    x.moveSteps()
    apple1 = apple(coordinate(1,5))
    x.touching(apple1,2)
    print(x)
    apple2 = apple(coordinate(1,6))
    x.touching(apple2, 2)
    print(x)
    x.touching(apple2, 3)
    print(x)

    n1 = segment(coordinate(0,0),direction(0,-1))
    n2 = segment(coordinate(0,2),direction(0,-1))
    n3 = segment(coordinate(4,2),direction(-1,0))

    y = snake()
    y.addToBeginning(n3)
    y.addToBeginning(n2)
    y.addToBeginning(n1)


    z = snake()
    z.addToBeginning(n2)
    z.addToBeginning(n1)
    z.addToEnd(n3)

    z2 = snake()
    z2.addToEnd(n2)
    z2.addToBeginning(n1)
    z2.addToEnd(n3)

    def snakeTest():
        assert(snake().len() == 0)
        assert(y == z == z2)

    snakeTest()
    
    xn1 = segment(coordinate(0,0), direction(0,-1))
    xn2 = segment(coordinate(0,2), direction(0,-1))
    xn3 = segment(coordinate(4,2), direction(-1,0))

    x = snake()
    x.addToEnd(xn1)
    x.addToEnd(xn2)
    x.addToEnd(xn3)

    for i in range(1,2,0):
        print(i)