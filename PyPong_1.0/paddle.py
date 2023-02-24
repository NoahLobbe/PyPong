import pygame

class Paddle(pygame.sprite.Sprite):

    def __init__(self, size, origin, speed, color, border):
        super().__init__()

        self.rect = pygame.Rect((0,0), size)
        self.rect.center = origin
        
        self.color = color
        self.border_w = border
        self.border_rad = 7

        self.x_vel = 0 #no support
        self.y_vel_original = speed
        self.y_vel = 0

        #flags
        self.up = False
        self.down = False
        

    def update(self, boundary_size):
        

        if (self.up == False) and (self.down == False): #no up or down
            self.y_vel = 0
        else:
            if self.up:
                print("paddle up")
                self.y_vel = -abs(self.y_vel_original) #make sure y_vel is up
            
            if self.down:
                self.y_vel = abs(self.y_vel_original) #make sure y_vel is bottom

        self.rect.y += self.y_vel



        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.right > boundary_size[0]:
            self.rect.right = boundary_size[0]

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.bottom > boundary_size[1]:
            self.rect.bottom = boundary_size[1]

    def draw(self, surfaceObj):
        pygame.draw.rect(surfaceObj,
                         self.color,
                         self.rect,
                         self.border_w,
                         self.border_rad)
