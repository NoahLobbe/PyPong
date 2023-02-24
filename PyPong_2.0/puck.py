import pygame
#import random
from math import sqrt

DEBUG_PRINT = False
def dprint(*args, **kwargs):
    if DEBUG_PRINT:
        print( " ".join(str(i) for i in args), kwargs) #make a list of strings and then .join()

class Puck(pygame.sprite.Sprite):

    def __init__(self, radius, origin,
                 x_vel, y_vel, color, border ):
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
        
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.speed = sqrt( (self.x_vel**2) + (self.y_vel**2) )
        self.zone_ext_factor = 2
        self._updateZones()
        
        self.color = color
        self.border_w = border

        # flags
        self.future_top_zone_collision = False
        self.future_right_zone_collision = False
        self.future_bottom_zone_collision = False
        self.future_left_zone_collision = False

    def _updateZones(self):
        #adjust size
        new_dimension = self.speed * self.zone_ext_factor 
        self.zones["top"].height = new_dimension
        self.zones["right"].width = new_dimension
        self.zones["bottom"].height = new_dimension
        self.zones["left"].width = new_dimension

        #re-position
        self.zones["top"].bottomleft = self.rect.topleft
        self.zones["right"].topleft = self.rect.topright
        self.zones["bottom"].topleft = self.rect.bottomleft
        self.zones["left"].topright = self.rect.topleft


    def flipX(self):
        dprint("flipping X")
        self.x_vel *= -1

    def flipY(self):
        dprint("flipping X")
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
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self._updateZones()


    def draw(self, surfaceObj, draw_zones=False):
        
        pygame.draw.circle(surfaceObj,
                           self.color,
                           self.rect.center,
                           self.radius,
                           self.border_w)
        
        #pygame.draw.rect(surfaceObj, self.color, self.rect)

        if draw_zones:
            for k,v in self.zones.items():
                pygame.draw.rect(surfaceObj, (255,255,255), v, width=1)
