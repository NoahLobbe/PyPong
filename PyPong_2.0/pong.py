import pygame
import random
from paddle import Paddle
from puck import Puck


#DEV_CONTROL = (True, 10)

DEBUG_PRINT = False
def dprint(*args, **kwargs):
    if DEBUG_PRINT:
        print( " ".join(str(i) for i in args),  kwargs) #make a list of strings and then .join()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)

class Pong:
    """Game completely AI played"""

    def __init__(self):
        pygame.init()
        pygame.font.init()

        ##general variables
        #core general vars
        self.app_name = "Pong"
        self.win_size = (858, 525) #858x525
        self.FPS = 60
        self.font = pygame.font.SysFont("Courier New", 64)
        self.margin = 10

        ##flags
        self.running = False
        self.pause = False

        #collision vars/flags
        self.collision_enacted = False
        self.impend_zone_collisions = []

        #scoring vars/flags
        self.prev_R_paddle_score = None
        self.prev_L_paddle_score = None
        self.R_paddle_score = 0
        self.L_paddle_score = 0
        self.scored = False
        

        #display vars
        self.bg = (0,0,0)
        self.image = pygame.image.load("background.jpg")
        self.objects_border_width = 2
        
        
        ##objects 
        #core
        self.Window = pygame.display.set_mode(self.win_size)
        self.Clock = pygame.time.Clock()

        #Paddles
        self.paddle_speed = 7#int(self.FPS/10)
        self.paddle_size = (25, 100)
        self.paddle_L_origin = (self.margin + self.paddle_size[0]/2,
                                int(self.win_size[1]/2))
        self.paddle_R_origin = (int(self.win_size[0] - self.margin - self.paddle_size[0]/2),
                                int(self.win_size[1]/2))
        
        self.Paddle_L = Paddle(self.paddle_size, self.paddle_L_origin,
                               self.paddle_speed, RED,
                               self.objects_border_width)
        self.Paddle_R = Paddle(self.paddle_size, self.paddle_R_origin,
                               self.paddle_speed, BLUE,
                               self.objects_border_width)

        #Puck
        self.puck_rad = 10
        self.generatePuck()

    def getRandomVel(self, start_range, end_range):
        """start_range must be < end_range"""
        if start_range >= end_range:
            raise ValueError("start_range must be < end_range")
        
        total_range = list(range(start_range, end_range))
        del total_range[total_range.index(0)] #remove zero
        return random.choice(total_range)

    def generatePuck(self):
        self.puck_x_vel = self.getRandomVel(-4, 4)
        self.puck_y_vel = self.getRandomVel(-2, 2)
        self.puck_origin = (int(self.win_size[0]/2), int(self.win_size[1]/2))

        self.Puck = Puck(self.puck_rad, self.puck_origin,
                         self.puck_x_vel, self.puck_y_vel,
                         GREEN, self.objects_border_width )


    def _keydownEvents(self, event):
        if event.key == pygame.K_w:
            self.Paddle_L.up = True

        elif event.key == pygame.K_s:
            self.Paddle_L.down = True

        elif event.key == pygame.K_UP:
            self.Paddle_R.up = True

        elif event.key == pygame.K_DOWN:
            self.Paddle_R.down = True
                
    def _keyupEvents(self, event):
        if event.key == pygame.K_ESCAPE: 
            #Esc toggles pause
            if self.pause:
                self.pause = False
            else:
                self.pause = True

            dprint("'esc' pressed, self.pause:", self.pause)

        elif event.key == pygame.K_w:
            self.Paddle_L.up = False

        elif event.key == pygame.K_s:
            self.Paddle_L.down = False

        elif event.key == pygame.K_UP:
            self.Paddle_R.up = False

        elif event.key == pygame.K_DOWN:
            self.Paddle_R.down = False

    def _checkEvents(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit(f"Exiting {self.app_name}")

            elif event.type == pygame.KEYDOWN:
                self._keydownEvents(event)

            elif event.type == pygame.KEYUP:
                self._keyupEvents(event)


    def addVectors(self, puck, paddle):

        resultant_x = puck.x_vel + paddle.x_vel
        resultant_y = puck.y_vel + paddle.y_vel

        dprint("Resolving vectors | curr puck V:", puck.x_vel, puck.y_vel,
              " | paddle V:", paddle.x_vel, paddle.y_vel,
              " | resultant puck V:", resultant_x, resultant_y)
        puck.x_vel = resultant_x
        puck.y_vel = resultant_y
        

    def collidePaddle(self, puck, paddle):
        paddle_rect = paddle.rect

        dprint("top", puck.puckTopZoneCollision(paddle_rect),
              " | right", puck.puckRightZoneCollision(paddle_rect),
              " | bottom", puck.puckBottomZoneCollision(paddle_rect),
              " | left", puck.puckLeftZoneCollision(paddle_rect))

        if self.impend_zone_collisions == []:
            if puck.future_top_zone_collision:
                self.impend_zone_collisions.append("top")

            if puck.future_right_zone_collision:
                self.impend_zone_collisions.append("right")

            if puck.future_bottom_zone_collision:
                self.impend_zone_collisions.append("bottom")

            if puck.future_left_zone_collision:
                self.impend_zone_collisions.append("left")
           
        
        if puck.rect.colliderect(paddle_rect):
            dprint("\n__COLLISION__ | self.collision_enacted:",
                  self.collision_enacted, end="")

            if self.collision_enacted == False:
                self.addVectors(puck, paddle)

                dprint(" | self.impend_zone_collisions:", self.impend_zone_collisions)

                if "right" in self.impend_zone_collisions:
                    puck.flipX()
            
                if "left" in self.impend_zone_collisions:
                    puck.flipX()
            
                if "top" in self.impend_zone_collisions:
                    puck.flipY()
            
                if "bottom" in self.impend_zone_collisions:
                    puck.flipY()

                self.collision_enacted = True
        else:
            self.collision_enacted = False



    def puckBoundaryCollision(self, puck):
        
        if puck.rect.x <= 0:
            #if not self.scored:
            self.prev_R_paddle_score = self.R_paddle_score
            self.R_paddle_score += 1
            self.scored = True

        elif puck.rect.right >= self.win_size[0]:
            #if not self.scored:
            self.prev_L_paddle_score = self.L_paddle_score
            self.L_paddle_score += 1
            self.scored = True

        else:
            self.scored = False
            
        if (puck.rect.y < 0) or (puck.rect.bottom > self.win_size[1]): #top/bottom walls
            puck.y_vel *= -1
    
    
    def _drawScores(self):

        #only update as neccasiry
        if self.R_paddle_score != self.prev_R_paddle_score:
            R_score = self.font.render(str(self.R_paddle_score), False, self.Paddle_R.color)
            x_pos = self.win_size[0] - self.margin - R_score.get_width()
            self.Window.blit(R_score, (x_pos, self.margin))
                    
        if self.L_paddle_score != self.prev_L_paddle_score:
            L_score = self.font.render(str(self.L_paddle_score), False, self.Paddle_L.color)
            self.Window.blit(L_score, (self.margin, self.margin))

    def render(self):
        
        #self.Window.fill(self.bg)
        self.Window.blit(self.image, ( (0,0), self.win_size))

        self.Paddle_L.draw(self.Window)
        self.Paddle_R.draw(self.Window)
        self.Puck.draw(self.Window, draw_zones=False)

        self._drawScores()
           
        if self.pause:
            #https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
            self.pause_surf = pygame.Surface(self.win_size, pygame.SRCALPHA)
            alpha = 255*0.6
            self.pause_surf.fill( (255,255,255,alpha) )
            self.Window.blit(self.pause_surf, (0,0))
            

    def run(self):
        self.running = True
        while self.running:
            ##Inputs
            self._checkEvents()

            ##Calculations
            if not self.pause:
                if self.scored:
                    self.generatePuck()
                #update positions
                self.Paddle_L.update(self.win_size)
                self.Paddle_R.update(self.win_size)
                self.Puck.move(self.win_size)

                #check collisions
                self.puckBoundaryCollision(self.Puck)

                #only check relevant possible collisions
                if self.Puck.rect.x <= self.win_size[0]/2: #self.Paddle_L.rect.right:
                    dprint("checking Left Paddle, puck pos ",
                          self.Puck.rect.topleft, end="")
                    dprint(" | curr puck V:", self.Puck.x_vel, self.Puck.y_vel)
                    self.collidePaddle(self.Puck, self.Paddle_L)
                    
                elif self.Puck.rect.right >= self.win_size[0]/2: # self.Paddle_R.rect.x:
                    dprint("checking Right Paddle, puck pos ",
                          self.Puck.rect.topleft, end="")
                    dprint(" | curr puck V:", self.Puck.x_vel, self.Puck.y_vel)
                    self.collidePaddle(self.Puck, self.Paddle_R)
                
            ##Renders
            self.render()

            pygame.display.flip()
            self.Clock.tick(self.FPS)


if __name__ == "__main__":

    Game = Pong()
    Game.run()
            
        
