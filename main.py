import pygame,sys,random
from pygame.math import Vector2 #lets me type 'Vector2' instead of pygame.math.Vector2

#SNAKE CLASS
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #3 side by side blocks to start
        self.direction = Vector2(1,0) #moves to the right
        self.new_block = False

    def draw_snake(self):
        for block in self.body: #cycle through block list in self.body and...
            #create rectangle
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            #draw rectangle
            pygame.draw.rect(screen, (63, 183, 252),block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] #copy the whole body
            body_copy.insert(0,body_copy[0] + self.direction) #add 1 block to the copy
            self.body = body_copy[:] #change body to new copied body
            self.new_block = False
        else:
            body_copy = self.body[:-1]  #only grab first 2 blocks of body
            body_copy.insert(0, body_copy[0] + self.direction) #add 1 block to the copy
            self.body = body_copy[:]  #change body to new copied body

    def add_block(self):
        self.new_block = True

#FRUIT CLASS
class FRUIT:
    def __init__(self):
        self.randomizePos()

    def draw_fruit(self):
        #create rectangle
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        #draw the rectangle
        pygame.draw.rect(screen, (255, 77, 64), fruit_rect)#surface,color,item

    def randomizePos(self):
        # create an X and Y pos on grid
        self.x = random.randint(0, cell_number - 1)  # generates random grid position -1 to fit on screen
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)

#MAIN CLASS
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_elements(self):
        self.fruit.draw_fruit()  # draws object
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        fruitCount = 0
        if self.fruit.pos == self.snake.body[0]: #if head of snake touches fruit
            fruitCount = fruitCount+1
            print("fruit eaten")
            #reposition fruit
            self.fruit.randomizePos()
            #add another block to snake
            self.snake.add_block()

        for block in self.snake.body[1:]: #if fruit is located in same pos as body (not head) of snake, randomize its position again
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        #check if outside of screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        #check if head hits any part of snake
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3) #score = snake length - 3
        score_surface = game_font.render(score_text, True, (50, 168, 82))
        score_x = int(cell_size * cell_number -40) #60px from right of screen
        score_y = int(cell_size * cell_number -40) #40px from bottom of screen
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)

pygame.init() #initialize pygame
cell_size = 30
cell_number = 20
dimension = cell_size * cell_number
screen = pygame.display.set_mode((dimension,dimension)) #create new 400x500 screen
clock = pygame.time.Clock() #create clock for tracking time
game_font = pygame.font.Font(None, 50)



#timer that triggers every 150ms
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100) #triggered every 150ms

main_game = MAIN()

while True:
    for event in pygame.event.get(): #closing pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        #look for keyboard input
        if event.type == pygame.KEYDOWN: #check for key press
            if event.key == pygame.K_UP: #if pressing up key
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:  # if pressing down key
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:  # if pressing left key
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:  # if pressing right key
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)


    screen.fill((214, 240, 255)) #add color to the screen
    main_game.draw_elements()
    pygame.display.update() #update the screen
    clock.tick(60) #add 60 ticks to the clock per loop