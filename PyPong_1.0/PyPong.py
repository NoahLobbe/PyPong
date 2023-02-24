import pygame
import random
from paddle import Paddle
from puck import Puck
from line import Line


DEV_CONTROL = (False, 10)

DEBUG_PRINT = True
def dprint(*args):
    if DEBUG_PRINT:
        print( " ".join(str(i) for i in args) ) #make a list of strings and then .join()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)

class PyPong:
    """Game completely AI played"""

    def __init__(self):
        pygame.init()

        ##general variables
        #core vars
        self.app_name = "Pong"
        self.win_size = (600, 400)
        self.FPS = 60

        #flags
        self.running = False
        self.pause = False
        

        #display vars
        self.bg = (0,0,0)
        self.objects_border_width = 0
        
        
        ##objects 
        #core
        self.Window = pygame.display.set_mode(self.win_size)
        self.Clock = pygame.time.Clock()

        #Paddles
        self.paddle_speed = 5#int(self.FPS/10)
        self.paddle_size = (25, 100)
        self.paddle_L_origin = (50, int(self.win_size[1]/2))
        self.paddle_R_origin = (int(self.win_size[0]-50), int(self.win_size[1]/2))
        self.paddle_L_color = RED
        self.paddle_R_color = BLUE
        
        self.Paddle_L = Paddle(self.paddle_size, self.paddle_L_origin,
                               self.paddle_speed, self.paddle_L_color,
                               self.objects_border_width)
        self.Paddle_R = Paddle(self.paddle_size, self.paddle_R_origin,
                               self.paddle_speed, self.paddle_R_color,
                               self.objects_border_width)

        #Puck
        self.boost_amount = 1
        self.puck_x_vel = 3#$random.randint(-10, 10)
        self.puck_y_vel = 1#random.randint(-10, 10)
        self.puck_rad = 10
        self.puck_origin = (int(self.win_size[0]/2), int(self.win_size[1]/2))
        self.puck_color = YELLOW

        self.Puck = Puck(self.puck_rad, self.puck_origin,
                         self.puck_x_vel, self.puck_y_vel,
                         self.puck_color, self.objects_border_width,
                         DEV_CONTROL=DEV_CONTROL)
        self.puck_vectors = []

        #goals
        #self.goal_height = 100
        #self.Goal_L = pygame.Rect((0,0), (10, self.goal_height))
        #self.Goal_L.y = int( (self.win_size[1]/2) - (self.goal_height/2) )

    def _keydownEvents(self, event):
        if event.key == pygame.K_w:
            self.Paddle_L.up = True

        elif event.key == pygame.K_s:
            self.Paddle_L.down = True

        elif event.key == pygame.K_UP:
            self.Paddle_R.up = True

        elif event.key == pygame.K_DOWN:
            self.Paddle_R.down = True

        if DEV_CONTROL[0]:
            if event.key == pygame.K_u:
                self.Puck.up = True

            elif event.key == pygame.K_k:
                self.Puck.right = True

            elif event.key == pygame.K_j:
                self.Puck.down = True

            elif event.key == pygame.K_h:
                self.Puck.left = True
                
                
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

        if DEV_CONTROL[0]:
            if event.key == pygame.K_u:
                self.Puck.up = False

            elif event.key == pygame.K_k:
                self.Puck.right = False

            elif event.key == pygame.K_j:
                self.Puck.down = False

            elif event.key == pygame.K_h:
                self.Puck.left = False
            
        

    def _checkEvents(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit(f"Exiting {self.app_name}")

            elif event.type == pygame.KEYDOWN:
                self._keydownEvents(event)

            elif event.type == pygame.KEYUP:
                self._keyupEvents(event)

    '''
    def _getPreviousPoint(self, point, vector):
        """Returns resultant point"""
        
        ans = (point[0] - vector[0], point[1] - vector[1])
        print(f"_getPreviousPoint({point}) ->", ans)
        return ans
    
    def puckRectCollision(self, target_rect, _Puck):
        print("Puck Rect:", self.Puck.rect, " | target_rect:", target_rect)
        """
        ##puck vectors 
        #bottomleft vector
        puck_vector_endpoint1 = _Puck.bottomleft
        puck_vector_endpoint2 = (_Puck.left - _Puck.x_vel,
                                 _Puck.bottom - _Puck.y_vel)
        #line equation y = mx + b
        puck_delta_y = puck_vector_endpoint2[1] - puck_vector_endpoint1[1]
        puck_delta_x = puck_vector_endpoint2[0] - puck_vector_endpoint1[0]
        puck_vector_m = puck_delta_y / puck_delta_x
        #b = y - mx of given (x,y)
        puck_vector_b = puck_vector_endpoint1[1] - (puck_vector_m * puck_vector_endpoint1[0])
        """
        ##Rect lines
        TopLine = Line(target_rect.topleft, target_rect.topright)
        RightLine = Line(target_rect.topright, target_rect.bottomright)
        BottomLine = Line(target_rect.bottomleft, target_rect.bottomright)
        LeftLine = Line(target_rect.topleft, target_rect.bottomleft)

        ##Puck vector lines
        puckVector = (_Puck.x_vel, _Puck.y_vel)
        print("Puck vector:", puckVector)
        
        PuckTopLeftVector = Line(_Puck.rect.topleft,
                                 self._getPreviousPoint(_Puck.rect.topleft,
                                                        puckVector) )
        PuckTopRightVector = Line(_Puck.rect.topright,
                                  self._getPreviousPoint(_Puck.rect.topright,
                                                         puckVector) )
        PuckBottomRightVector = Line(_Puck.rect.bottomright,
                                     self._getPreviousPoint(_Puck.rect.bottomright,
                                                            puckVector) )
        PuckBottomLeftVector = Line(_Puck.rect.bottomleft,
                                    self._getPreviousPoint(_Puck.rect.bottomleft,
                                                           puckVector) )

        self.puck_vectors = [PuckTopLeftVector, PuckTopRightVector,
                             PuckBottomRightVector, PuckBottomLeftVector]

        ##Check collisions with intersects of vectors and lines
        #check top
        top_collision_answers = (PuckBottomLeftVector.intersectsHorizontalLine(TopLine),
                                 PuckBottomRightVector.intersectsHorizontalLine(TopLine))
                                 
        right_collision_answers = (PuckTopLeftVector.intersectsVerticalLine(RightLine),
                                   PuckBottomLeftVector.intersectsVerticalLine(RightLine))

        bottom_collision_answers = (PuckTopLeftVector.intersectsHorizontalLine(BottomLine),
                                    PuckTopRightVector.intersectsHorizontalLine(BottomLine))

        left_collision_answers = (PuckTopRightVector.intersectsVerticalLine(LeftLine),
                                  PuckBottomRightVector.intersectsVerticalLine(LeftLine))

        print("COLLISION ANSWERS",
              " | top:", top_collision_answers,
              " | right:", right_collision_answers,
              " | bottom:", bottom_collision_answers,
              " | left:", left_collision_answers)
        

        #check top
        if top_collision_answers[0][0] or top_collision_answers[1][0]:
            print("TOP COLLISION")
            _Puck.y_vel *= -1
            _Puck.rect.bottom = target_rect.top - abs(_Puck.y_vel)

        if right_collision_answers[0][0] or right_collision_answers[1][0]:
            print("RIGHT COLLISION")
            _Puck.x_vel *= -1
            _Puck.rect.left = target_rect.right + abs(_Puck.x_vel)

        if bottom_collision_answers[0][0] or bottom_collision_answers[1][0]:
            print("BOTTOM COLLISION")
            _Puck.y_vel *= -1
            _Puck.rect.top = target_rect.bottom + abs(_Puck.y_vel)

        if left_collision_answers[0][0] or left_collision_answers[1][0]:
            print("LEFT COLLISION")
            _Puck.x_vel *= -1
            _Puck.rect.right = target_rect.left - abs(_Puck.x_vel)

        """
        #top and bottom of paddle_rect
        if ( (self.Puck.rect.right > target_rect.left) \
             and (self.Puck.rect.right < target_rect.right) ) \
           or ( (self.Puck.rect.left > target_rect.left) \
                 and (self.Puck.rect.left < target_rect.right) ) :

            ##############Print each condition

            if self.Puck.y_vel > 0: #positive
                print(f"Puck {self.Puck.rect} hitting top of {target_rect}", end="")

                print("Puck.top:", self.Puck.rect.y,
                      " | bottom:", self.Puck.rect.bottom,
                      "puck rect:", self.Puck.rect,
                      "Rect.top:", target_rect.top,
                      " | bottom:", target_rect.bottom )
                self.Puck.rect.bottom = target_rect.top - 1

                
                
            elif self.Puck.y_vel < 0: #negative
                print(f"Puck {self.Puck.rect} hitting bottom of {target_rect}", end="")

                print("Puck.top:", self.Puck.rect.y,
                      " | bottom:", self.Puck.rect.bottom,
                      "puck rect:", self.Puck.rect,
                      "Rect.top:", target_rect.top,
                      " | bottom:", target_rect.bottom )
                self.Puck.rect.top = target_rect.bottom + 1

            
            self.Puck.y_vel *= -1
            

        #left and right of paddle_rect
        if (self.Puck.rect.bottom > target_rect.top) \
               and (self.Puck.rect.top < target_rect.bottom):

            if self.Puck.x_vel > 0: #positive
                print(f"Puck {self.Puck.rect} hitting left side of {target_rect}")
                
            elif self.Puck.x_vel < 0: #negative
                print(f"Puck {self.Puck.rect} hitting right side of {target_rect}")

            self.Puck.x_vel *= -1

       """     
    
    def puckCollisions(self):

        dprint("#1 self.Puck.x_vel", self.Puck.x_vel,
              " | self.Puck.y_vel", self.Puck.y_vel,
              "| Puck.rect:", self.Puck.rect)

        #walls
        if (self.Puck.rect.x < 0) or (self.Puck.rect.right > self.win_size[0]): #left/right walls
            self.Puck.x_vel *= -1
        if (self.Puck.rect.y < 0) or (self.Puck.rect.bottom > self.win_size[1]): #top/bottom walls
            self.Puck.y_vel *= -1

        
        
        #paddles
        if pygame.sprite.collide_rect(self.Puck, self.Paddle_L) \
               or pygame.sprite.collide_rect(self.Puck, self.Paddle_R):
            dprint("collision with L paddle")

            ##self.puckRectCollision(self.Paddle_L.rect, self.Puck)


            ##Bouncing off top of a paddle is unexpected chances
            self.Puck.x_vel *= -1

        #check if the puck is inside the paddle
        #if (self.Puck.x >= self.Paddle_L.x) and (self.Puck.right <= self.Paddle_L.right)
            

            """
            if (self.Puck.rect.left <= self.Paddle_L.rect.right) \
                   and (self.Puck.rect.left <= self.Paddle_L.rect.right): #collision on paddle right
                #print("self.Puck.rect.left", self.Puck.rect.x,
                      #"| self.Paddle_L.rect.right", self.Paddle_L.rect.right)
                
                if (self.Puck.rect.bottom < self.Paddle_L.rect.top): #collision on paddle top
                    self.Puck.y_vel *= -1
                    self.Puck.rect.bottom = self.Paddle_L.rect.top - 1
                    print("top")
                else:
                    self.Puck.x_vel *= -1
                

                #print("#2 self.Puck.x_vel", self.Puck.x_vel,
                      #" | self.Puck.y_vel", self.Puck.y_vel)
                    print("right")
            
            if (self.Puck.rect.right < self.Paddle_L.rect.left): #collision on paddle left
                self.Puck.x_vel *= -1
                print("left")
            
            if (self.Puck.rect.bottom < self.Paddle_L.rect.top): #collision on paddle top
                self.Puck.y_vel *= -1
                #self.Puck.rect.bottom = self.Paddle_L.rect.top - 1
                print("top")

            if (self.Puck.rect.top < self.Paddle_L.rect.bottom) and (self.Puck.rect.top > self.Paddle_L.rect.top): #collision on paddle bottom
                self.Puck.y_vel *= -1
                self.Puck.rect.top = self.Paddle_L.rect.bottom + 1
                print("puck hitting paddle top")
            """
            '''

    def resolveVectors(self, puck, paddle):

        resultant_x = puck.x_vel + paddle.x_vel
        resultant_y = puck.y_vel + paddle.y_vel

        print("Resolving vectors | curr puck V:", puck.x_vel, puck.y_vel,
              " | paddle V:", paddle.x_vel, paddle.y_vel,
              " | resultant puck V:", resultant_x, resultant_y)
        puck.x_vel = resultant_x
        puck.y_vel = resultant_y

    def collidePaddle(self, puck, paddle):
        paddle_rect = paddle.rect

        if (not puck.future_top_zone_collision) \
               and (not puck.future_right_zone_collision) \
               and (not puck.future_bottom_zone_collision) \
               and (not puck.future_left_zone_collision):
            #only check impending zone collisions if there are no past ones
           
            print("top", self.Puck.puckTopZoneCollision(paddle_rect))
            print("right", self.Puck.puckRightZoneCollision(paddle_rect))
            print("bottom", self.Puck.puckBottomZoneCollision(paddle_rect))
            print("left", self.Puck.puckLeftZoneCollision(paddle_rect))

        
        if puck.rect.colliderect(paddle_rect):
            print("__COLLISION__")
            self.resolveVectors(puck, paddle)

            #if paddle.rect.x < self.win_size[0]/2: # if left paddle
                #print("Left paddle")
            if puck.future_left_zone_collision: #hits right side of paddle
                print("left zone collision")
                puck.flipX()
                    
            #elif paddle.rect.x > self.win_size[0]: # if right paddle
                #print("Right paddle")
            if puck.future_right_zone_collision: #hits left side of paddle
                print("right zone collision")
                puck.flipX()
                
            if puck.future_top_zone_collision: #hits bottom of paddle
                print("top zone collision")
                puck.flipY()
            elif puck.future_bottom_zone_collision: #hits top of paddle
                print("bottom zone collision")
                puck.flipY()

        


    """

    def collidePaddle(self, paddle):
        dprint("Puck Rect:", self.rect, " | paddle_rect:", paddle.rect)
        #right side is most frequent collision
        if self.Puck.puckLeftCollision(paddle.rect): #hits right of paddle
            dprint("Puck right zone collision")
            self.Puck.flipX()
            return True

        elif self.Puck.puckRightCollision(paddle.rect): #hits left of paddle
            self.Puck.flipX()
            return True
        
        if self.Puck.puckTopCollision(paddle.rect): #hits bottom of paddle
            dprint("Puck top zone collision")
            '''if self.Puck.y_vel > 0: #if already going down
                self.Puck.y_vel += self.boost_amount #boost puck
            else:'''
            self.Puck.flipY()
            return True
        
        elif self.Puck.puckBottomCollision(paddle.rect): #hits top of paddle
            dprint("Puck bottom zone collision")
            '''if self.Puck.y_vel < 0: #if already going down
                self.Puck.y_vel += self.boost_amount #boost puck
            else:'''
            self.Puck.flipY()
            return True
    """

    def render(self):
        
        self.Window.fill(self.bg)

        #pygame.draw.rect(self.Window, WHITE, self.Goal_L, self.objects_border_width)

        self.Paddle_L.draw(self.Window)
        self.Paddle_R.draw(self.Window)
        self.Puck.draw(self.Window, draw_zones=True)

        #for i in self.puck_vectors:
            #pygame.draw.line(self.Window, GREEN, i.point1, i.point2)
            
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
                self.Paddle_L.update(self.win_size)
                self.Paddle_R.update(self.win_size)
            
                self.Puck.move(self.win_size)

                #only check relevant possible collisions
                if self.Puck.rect.x <= self.Paddle_L.rect.right:
                    print("checking Left Paddle, puck pos ",
                          self.Puck.rect.topleft, end="")
                    print(" | curr puck V:", self.Puck.x_vel, self.Puck.y_vel)
                    self.collidePaddle(self.Puck, self.Paddle_L)
                    
                elif self.Puck.rect.right >= self.Paddle_R.rect.x:
                    print("checking Right Paddle, puck pos ",
                          self.Puck.rect.topleft, end="")
                    print(" | curr puck V:", self.Puck.x_vel, self.Puck.y_vel)
                    self.collidePaddle(self.Puck, self.Paddle_R)
                #self.puckCollisions()
            

            ##Renders
            self.render()

            pygame.display.flip()
            self.Clock.tick(self.FPS)


if __name__ == "__main__":

    Game = PyPong()
    Game.run()
            
        
