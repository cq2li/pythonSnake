from cmu_112_graphics import *
import cmu_112_graphics as cmu

import snakeClasses as s
def roundHalfUp(d):
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

##
def drawApple(canvas, apple):
    x = apple.x
    y = apple.y
    s = apple.size
    canvas.create_oval(x - s, y + s, x + s, y - s, 
                       fill = 'red', width = 0.2)

def drawSnakeCorner(canvas, seg1, seg2):
    s = seg2.size
    if (seg2.dx == 0):
        dy = seg2.dy
        if (dy > 0):
            y1 = seg1.y + dy * s
            y0 = seg1.y
        
        else:
            y1 = seg1.y
            y0 = seg1.y + dy * s
        # print(seg1.x - s, y0, seg1.x + s, y1)
        canvas.create_rectangle(seg1.x - s, y0,
                                seg1.x + s, y1, fill = 'black')
    else:
        dx = seg2.dx
        if (dx > 0):
            x1 = seg1.x + dx * s
            x0 = seg1.x
        else:
            x1 = seg1.x
            x0 = seg1.x + dx * s
        
        # print(x0, seg1.y - s, x1, seg1.y + s, f's: {s}')
        canvas.create_rectangle(x0, seg1.y - s,
                                x1, seg1.y + s, fill = 'black')

def drawPlayArea(canvas,boundary, width, height):
        canvas.create_line(boundary, boundary, 
                            width-boundary, boundary)
        canvas.create_line(width-boundary, boundary, 
                            width-boundary, height - boundary)
        canvas.create_line(boundary, height - boundary,
                            width-boundary, height - boundary)
        canvas.create_line(boundary, boundary, 
                            boundary, height - boundary)

def drawSnake(canvas, snake):
    s = snake.size
    if (snake.len() == 1):
        body = snake.head.next
        canvas.create_rectangle(body.x - s, body.y - s, 
                                body.x + s, body.y + s,
                                fill = 'black')
    else:
        seg2 = snake.head.next
        seg1 = snake.head
        while (seg2.next != None):
            #advance
            seg1 = seg2
            seg2 = seg2.next
            # draw corners for connecting segments
            drawSnakeCorner(canvas, seg1, seg2)
            # draw line connecting segments
            canvas.create_line(seg1.x, seg1.y, seg2.x, seg2.y, 
                               width = snake.width)

def initialiseSnake(app):
    app.player = s.snake()
    app.player.addToBeginning(
        s.segment(s.coordinate(roundHalfUp(app.width//2),
                            roundHalfUp(app.height//2)), 
                s.direction(0,1), 
                app.player.size))
    return app.player

def initialiseApple(app):
    return s.apple.spawnApple(5, app.width, app.height, app.boundary+20)

# model
def  appStarted(app):
    app.gameState = "Game Start"
    app.boundary = 10
    app.player = initialiseSnake(app)
    app.apple = initialiseApple(app)
    app.timerDelay = 30
    app.v = 2
    app.paused = True

#view
def redrawAll(app, canvas):
    if (app.gameState == "Game Over"):
        canvas.create_text(app.width//2, app.height//2, 
                           text = "W A S T E D", 
                           font='Arial 30 bold')
        canvas.create_text(app.width//2, app.height//5, 
                           text = "Press Space to Restart", 
                           font='Arial 10 bold')
        canvas.create_text(app.width//2, 0.3 * app.height, 
                           text = f"Score: {(len(app.player.points))//10}", 
                           font='Arial 10 bold')       
    elif(app.gameState == "Game On"):
        try: 
            drawPlayArea(canvas, app.boundary, app.width, app.height)
            drawApple(canvas, app.apple)
            drawSnake(canvas, app.player)
        except:
            pass
    else:
        canvas.create_text(app.width//2, app.height//2, 
                           text = "Press Space to Start", font='Arial 30 bold')
    

    
def doStep(app):
    app.player.move(app.v)
    app.player.outtaBounds(app.boundary, app.boundary,
                           app.width - app.boundary, app.height - app.boundary)
    if (app.player.touching(app.apple, app.apple.size + app.v)):
        app.player.grow(app.apple.size)
        app.v = 2 + len(app.player.points)//20
        app.apple = s.apple.spawnApple(5, app.width, app.height, app.boundary)


def timerFired(app):
    if (app.gameState == "Game On"):
        if (app.player.dead == True):
            app.gameState = "Game Over"
            app.score = app.player.len()
            app.paused = True
        else:
            if (not app.paused):
                doStep(app)

#controller
def keyPressed(app, event):
    if(event.key == 'Left'): 
        app.player.changeDirections(s.direction(-1,0))
    elif (event.key == 'Right'):
        app.player.changeDirections(s.direction(1,0))
    elif (event.key == 'Up'):
        app.player.changeDirections(s.direction(0,-1))
    elif (event.key == 'Down'):
        app.player.changeDirections(s.direction(0,1))
    elif (event.key == 'p' and app.gameState != 'Game Over'):
        app.paused = not app.paused
    elif (event.key == 's' and app.paused):
        doStep(app)
    elif (event.key == 'Space' and app.gameState == 'Game On'):
        app.v += 1
    elif (event.key == 'Space' and app.gameState == 'Game Start'):
        app.paused = not app.paused
        app.gameState = 'Game On'
    elif (event.key == 'Space' and app.gameState == 'Game Over'):
        app.gameState = 'Game On'
        app.player = initialiseSnake(app)
        app.apple = initialiseApple(app)
        app.v = 2
        app.paused = not app.paused
    else:
        return



runApp(width=500, height=500)