import pygame
import random

DEBUG_PRINT = True
def dprint(*args):
    if DEBUG_PRINT:
        print( " ".join(str(i) for i in args) ) #make a list of strings and then .join()

class Puck(pygame.sprite.Sprite):

    def __init__(self, radius, origin,
                 x_vel, y_vel, color, border,
                 DEV_CONTROL=(False, 10) ):
        super().__init__()

        self.radius = radius
        self.rect = pygame.Rect((0,0), (2*self.radius, 2*self.radius))
        self.rect.center = origin
        zone_dist = 2*self.radius
        self.zones = {"top": pygame.Rect((0,0), (2*self.radius, zone_dist)),
                      "right": pygame.Rect((0,0), (zone_dist, 2*self.radius)),
                      "bottom": pygame.Rect((0,0), (2*self.radius, zone_dist)),
                      "left": pygame.Rect((0,0), (zone_dist, 2*self.radius))
                      }
        self._updateZones()

        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.border_w = border
        self.DEV_CONTROL = DEV_CONTROL
        if self.DEV_CONTROL[0]:
            self.speed = self.DEV_CONTROL[1]
            self.up = False
            self.right = False
            self.down = False
            self.left = False

        # flags
        self.future_top_zone_collision = False
        self.future_right_zone_collision = False
        self.future_bottom_zone_collision = False
        self.future_left_zone_collision = False

    def _updateZones(self):
        self.zones["top"].bottomleft = self.rect.topleft
        self.zones["right"].topleft = self.rect.topright
        self.zones["bottom"].topleft = self.rect.bottomleft
        self.zones["left"].topright = self.rect.topleft


    def flipX(self):
        print("flipping X")
        self.x_vel *= -1

    def flipY(self):
        print("flipping X")
        self.y_vel *= -1

    def puckTopZoneCollision(self, target_rect):
        if target_rect.colliderect(self.zones["top"]):
            self.future_top_zone_collision = True
            return True
        else:
            self.future_top_zone_collision = False
            return False
        

    def puckRightZoneCollision(self, target_rect):
        if target_rect.colliderect(self.zones["right"]):
            self.future_right_zone_collision = True
            return True
        else:
            self.future_right_zone_collision = False
            return False

    def puckBottomZoneCollision(self, target_rect):
        if target_rect.colliderect(self.zones["bottom"]):
            self.future_bottom_zone_collision = True
            return True
        else:
            self.future_bottom_zone_collision = False
            return False

    def puckLeftZoneCollision(self, target_rect):
        if target_rect.colliderect(self.zones["left"]):
            self.future_left_zone_collision = True
            return True
        else:
            self.future_left_zone_collision = False
            return False       

    

    def move(self, boundary_size):
        #print("PUCK.MOVE: self.x_vel", self.x_vel,
              #" | self.y_vel", self.y_vel)
        if self.DEV_CONTROL[0]:
            if self.up:
                self.rect.y -= self.speed
                
            elif self.down:
                self.rect.y += self.speed
                
            elif self.right:
                self.rect.x += self.speed
                
            elif self.left:
                self.rect.x -= self.speed
        else:
            self.rect.x += self.x_vel
            self.rect.y += self.y_vel

        self._updateZones()

        
        if (self.rect.x < 0) or (self.rect.right > boundary_size[0]): #left/right walls
            self.x_vel *= -1
        if (self.rect.y < 0) or (self.rect.bottom > boundary_size[1]): #top/bottom walls
            self.y_vel *= -1

        #print("self.x_vel", self.x_vel, " | self.y_vel", self.y_vel)
    

    def draw(self, surfaceObj, draw_zones=False):
        """
        pygame.draw.circle(surfaceObj,
                           self.color,
                           self.rect.center,
                           self.radius,
                           self.border_w)
        """
        pygame.draw.rect(surfaceObj, self.color, self.rect)

        if draw_zones:
            for k,v in self.zones.items():
                pygame.draw.rect(surfaceObj, (255,255,255), v, width=1)
