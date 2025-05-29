'''
Punch Jiasing Sai Grade8 Computerscience

This is a simple snake game using Python and tkinter for the graphics.
'''

import tkinter
import random  

# Initial game setup
ROWS = 25
COLS = 25
TILE_SIZE = 25

# Initialize window size based on grid settings
WINDOW_WIDTH = TILE_SIZE * COLS #25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS #25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

#  Set up the main drawing area for the game
canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/4) - (window_width/4))
window_y = int((screen_height/4) - (window_height/4))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] #multiple snake tiles
game_over = False
score = 0

#game loop
def change_direction(e): #e = event
    #  Handle direction change from keyboard input
    global velocityX, velocityY, game_over
    if (game_over):
        return #edit this code to reset game variables to play again

    # Change direction according to arrow key input
    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0


def move():
    '''TODO: moves whats on the screen'''
    global snake, food, snake_body, game_over, score
    
    if (game_over):
        return

    # Check if the snake collides with the wall
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return

    # Check for self-collision
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    #collision
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    #update snake body (more detail)
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    '''Comment'''
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'white')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'light blue')

    # Sketch every section of the snake’s body.
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'light blue')

    # Show Game Over message and current score
    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "red")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "light blue")
    
    window.after(100, draw) #call draw again every 100ms (1/10 of a second) = 10 frames per second

draw()
window.bind("<KeyRelease>", change_direction) #when you press on any key and then let go
window.mainloop() #used for listening to window events like key presses
