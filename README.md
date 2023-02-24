# PyPong
My re-creation of the classic Pong game but (**super** simple) with the Pygame module (https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation).
Going for the retro look, the paddles and puck have coloured outlines, no fill. This can be adjusted with `self.borderwidth` from PyPong under PyPong.py where 0=fill, 1>= is the thickness (integer).

### pong_v1.0 
This version has bugs but has many different iterations of failed collision detection and resolving, commented out.

### pong_v2.0 
This version uses zones around the puck to determine impending collisions and then only enact them; this prevents the order of `if` statements to affect the puck's motion. Additionally, a form of spin is included in this version. If a paddle is moving when the puck collides with it then vector addition is at play.

Puck's motion is acquired through `x_vel` and `y_vel` members, which allows for simple reflections; flip the vector component (x or y) by multiplying by -1.
