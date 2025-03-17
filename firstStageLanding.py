import pygame
import math
import random
import time

groundPixelY = 750
rollRateFalcon = 0.02
gravity = 0.01
landingPad = pygame.image.load("landingPad.png")
landingPad  = pygame.transform.scale(landingPad,(200,50))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (100, 255, 100)
DGREEN = (0, 100, 0)
BLUE = (0, 0, 255)
BROWN = (139,69,19)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
LORANGE = (255, 140, 0)
LYELLOW = (255, 255, 140)
LRED = (255, 140, 140)

smoke = []


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Falcon 9 Landing")

def updateObjects():
    falcon9STG1.changeAngle(falcon9STG1.angle + falcon9STG1.deltaAngle)
    falcon9STG1.deltaAngle *= 0.99999  # Slow down the rotation
    falcon9STG1.velocityY += gravity  # Gravity
    falcon9STG1.velocityX *= 0.99999  # Slow down the horizontal velocity
    if falcon9STG1.gasLeft > 0:
        falcon9STG1.velocityX -= falcon9STG1.throttlePercent * 0.02 * math.sin(math.radians(falcon9STG1.angle))  # Thrust
        falcon9STG1.velocityY -= falcon9STG1.throttlePercent * 0.02 * math.cos(math.radians(falcon9STG1.angle))  # Thrust
    else:
        falcon9STG1.throttlePercent = 0

    falcon9STG1.gasLeft -= falcon9STG1.throttlePercent * 0.0015
    falcon9STG1.yTopLeft += falcon9STG1.velocityY
    falcon9STG1.xTopLeft += falcon9STG1.velocityX

    # Calculate the bottom of the rocket using trigonometry
    bottom_x = falcon9STG1.xTopLeft + falcon9STG1.CG_x + falcon9STG1.original_image.get_height() * (1 - falcon9STG1.percentCG) * math.sin(math.radians(falcon9STG1.angle))
    bottom_y = falcon9STG1.yTopLeft + falcon9STG1.CG_y + falcon9STG1.original_image.get_height() * (1 - falcon9STG1.percentCG) * math.cos(math.radians(falcon9STG1.angle))

    if bottom_y > groundPixelY + 25 and not falcon9STG1.landed and not falcon9STG1.crashed:
        if falcon9STG1.velocityX < 1.2 and falcon9STG1.velocityY < 1.2 and falcon9STG1.angle < 8 and falcon9STG1.angle > -8 and bottom_x > screen_width/2-100 and bottom_x < screen_width/2+100:
            falcon9STG1.landed = True
            falcon9STG1.landedX = bottom_x
            falcon9STG1.landedY = bottom_y

        else:
            falcon9STG1.crashed = True
            falcon9STG1.crashedX = bottom_x
            falcon9STG1.crashedY = bottom_y

    if falcon9STG1.landed:
        falcon9STG1.xTopLeft = falcon9STG1.landedX - falcon9STG1.CG_x
        falcon9STG1.yTopLeft = falcon9STG1.landedY - falcon9STG1.image.get_height()
        falcon9STG1.throttlePercent = 0

    if falcon9STG1.yTopLeft > 500:
        #switch to "falcon9STG1Legs.png"
        falcon9STG1.original_image = pygame.image.load("falcon9STG1Legs.png")
        falcon9STG1.original_image = pygame.transform.scale(falcon9STG1.original_image, (int(falcon9STG1.original_image.get_width() * .5), int(falcon9STG1.original_image.get_height() * .5)))
        falcon9STG1.image = falcon9STG1.original_image
    
    for i in range(0, random.randint(0, int(3*falcon9STG1.throttlePercent))):
        smoke.append([random.uniform(-10, 10) + bottom_x, random.uniform(-10, 20) + bottom_y])

class MovingObject:
    def __init__(self, imageName, size, percentCG, xTopLeft, yTopLeft, angle=0, flame=False, throttleHas=False, gasLeft=1):  # percentCG is the percentage of the object's length from the top to CG
        self.original_image = pygame.image.load(imageName)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * size), int(self.original_image.get_height() * size)))
        self.image = self.original_image  # This will hold the rotated image
        self.percentCG = percentCG
        self.angle = angle
        self.deltaAngle = 0

        self.landed = False
        self.crashed = False

        self.throttleHas = throttleHas
        self.throttlePercent = 0

        self.gasLeft = gasLeft

        self.velocityX = 0
        self.velocityY = 0
        
        # Initial position and calculations
        self.xTopLeft = xTopLeft
        self.yTopLeft = yTopLeft
        
        # Calculate the offset of CG from top left corner
        self.CG_x = self.original_image.get_width() / 2
        self.CG_y = self.original_image.get_height() * self.percentCG
        
        # Distance from the center of gravity to top-left corner
        self.distanceCGtoTopLeft = math.sqrt(self.CG_x**2 + self.CG_y**2)
        self.angleCGtoTopLeft = math.degrees(math.atan2(self.CG_y, self.CG_x))

        self.hasFlame = flame

        self.crashedX = 0
        self.crashedY = 0

        self.landedX = 0
        self.landedY = 0

        
    def draw(self, screen):

        if self.landed:
            #draw static booster
            rotated_rect = self.image.get_rect(center=(self.xTopLeft + self.CG_x, self.yTopLeft + self.CG_y))
            screen.blit(self.image, rotated_rect.topleft)

        elif self.crashed:
            #draw explosion with built in draw
            pygame.draw.circle(screen, RED, (int(self.crashedX), int(self.crashedY)), 50)
            pygame.draw.circle(screen, ORANGE, (int(self.crashedX), int(self.crashedY)), 40)
            pygame.draw.circle(screen, YELLOW, (int(self.crashedX), int(self.crashedY)), 30)
            pygame.draw.circle(screen, WHITE, (int(self.crashedX), int(self.crashedY)), 20)
            pygame.display.flip()
            time.sleep(.1)
            pygame.draw.circle(screen, LRED, (int(self.crashedX), int(self.crashedY)), 40)
            pygame.draw.circle(screen, LORANGE, (int(self.crashedX), int(self.crashedY)), 30)
            pygame.draw.circle(screen, LYELLOW, (int(self.crashedX), int(self.crashedY)), 20)


        else:
            # Rotate the image
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # Calculate new top-left position after rotation to center on CG
            rotated_rect = self.image.get_rect(center=(self.xTopLeft + self.CG_x, self.yTopLeft + self.CG_y))
            screen.blit(self.image, rotated_rect.topleft)

            # Draw flame at the bottom of the booster, adjusted for rotation
            if self.hasFlame:
                flame = pygame.image.load("flame1.png")
                flame = pygame.transform.scale(flame, (int(self.throttlePercent*(self.original_image.get_width())), int(self.throttlePercent*(self.original_image.get_height() / 2))))
                flame = pygame.transform.rotate(flame, self.angle)
                
                # Calculate position for the flame to appear at the bottom of the booster
                bottom_y_offset = self.original_image.get_height() * (1 - self.percentCG)  # Distance from CG to bottom of image
                flame_x = self.xTopLeft + self.CG_x + bottom_y_offset *(.8 + self.throttlePercent)* math.sin(math.radians(self.angle))
                flame_y = self.yTopLeft + self.CG_y + bottom_y_offset *(.8 + self.throttlePercent)* math.cos(math.radians(self.angle))
                
                flame_rect = flame.get_rect(center=(flame_x, flame_y))
                screen.blit(flame, flame_rect.topleft)

            if self.throttleHas:
                pygame.draw.rect(screen, RED, (screen_width - 150, 50, 100*self.throttlePercent, 25))
                pygame.draw.rect(screen, BLACK, (screen_width - 150, 50, 100, 25), 2)
                #draw the gas left display
                pygame.draw.rect(screen, BLUE, (screen_width - 150, 100, 100*self.gasLeft, 25))
                pygame.draw.rect(screen, BLACK, (screen_width - 150, 100, 100, 25), 2)
            
    def changeAngle(self, newAngle):
        self.angle = newAngle


# Load and scale the background image
sky = pygame.image.load("skyStock.jpg")
screen_width, screen_height = screen.get_size()
sky = pygame.transform.scale(sky, (screen_width, screen_height))

#generate random darker spot of grass
grass = []
for i in range(0, 100):
    grass.append([random.randint(0, screen_width), random.randint(groundPixelY, screen_height), random.randint(-3,3)])

trees = []
for i in range(0, 5):
    trees.append([random.randint(0, screen_width/2 -100), random.randint(groundPixelY, screen_height)])
for i in range(0, 5):
    trees.append([random.randint(screen_width/2 +100, screen_width), random.randint(groundPixelY, screen_height)])

# Create the Falcon 9 booster as a MovingObject, with CG at 50% (center) vertically
falcon9STG1 = MovingObject("falcon9STG1.png", .5, 0.5, screen_width/2, 300, 0, True, True)
# Randomly generate a realistic starting position for the Falcon 9 booster
# Assume the booster starts at a random horizontal position near the center and a high altitude
initial_x = screen_width / 2 + random.uniform(-screen_width / 2, screen_width / 2)
initial_y = random.uniform(50, 150)

if initial_x < screen_width / 2:
    initial_vel_x = random.uniform(0, 2)
else:
    initial_vel_x = random.uniform(-2, 0)
initial_vel_y = random.uniform(-1, 1)
falcon9STG1.velocityX = initial_vel_x
falcon9STG1.velocityY = initial_vel_y

# Update the Falcon 9 booster with the new initial position
falcon9STG1.xTopLeft = initial_x
falcon9STG1.yTopLeft = 0

#make falcon point +- 10 degrees in its velocity vector
falcon9STG1.angle = 180 - math.degrees(math.atan2(initial_vel_x, -initial_vel_y)) + random.uniform(-10, 10)


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                #reset the falcon
                smoke = []
                falcon9STG1 = MovingObject("falcon9STG1.png", .5, 0.5, screen_width/2, 300, 0, True, True)
                initial_x = screen_width / 2 + random.uniform(-screen_width / 2, screen_width / 2)
                initial_y = random.uniform(50, 150)
                if initial_x < screen_width / 2:
                    initial_vel_x = random.uniform(0, 2)
                else:
                    initial_vel_x = random.uniform(-2, 0)
                initial_vel_y = random.uniform(-1, 1)
                falcon9STG1.velocityX = initial_vel_x
                falcon9STG1.velocityY = initial_vel_y
                falcon9STG1.xTopLeft = initial_x
                falcon9STG1.yTopLeft = 0
                falcon9STG1.angle = 180 - math.degrees(math.atan2(initial_vel_x, -initial_vel_y)) + random.uniform(-10, 10)


    keys = pygame.key.get_pressed()

    

    if keys[pygame.K_RIGHT]:
        falcon9STG1.deltaAngle += -rollRateFalcon
        print(falcon9STG1.deltaAngle)

    if keys[pygame.K_LEFT]:
        falcon9STG1.deltaAngle += rollRateFalcon
        print(falcon9STG1.deltaAngle)

    if keys[pygame.K_UP]:
        falcon9STG1.throttlePercent += 0.01
        if falcon9STG1.throttlePercent > 1:
            falcon9STG1.throttlePercent = 1
        
    if keys[pygame.K_DOWN]:
        falcon9STG1.throttlePercent -= 0.01
        if falcon9STG1.throttlePercent < 0:
            falcon9STG1.throttlePercent = 0

    

    # Draw background and Falcon 9 booster
    screen.blit(sky, (0, 0))#draw the sky
    pygame.draw.rect(screen, GREEN, (0,groundPixelY,screen_width,screen_height-groundPixelY))    #draw the ground
    #draw the throttle display
    
    #draw the grass
    for i in range(0, 100):
        pygame.draw.rect(screen, DGREEN, (grass[i][0], grass[i][1], 2, 8))
        pygame.draw.rect(screen, DGREEN, (grass[i][0]-grass[i][2], grass[i][1]-1, grass[i][2], 2))

    #draw the trees
    for i in range(0, 10):
        pygame.draw.rect(screen, BROWN, (trees[i][0], trees[i][1], 10, 50))
        pygame.draw.circle(screen, DGREEN, (trees[i][0]+5, trees[i][1]-5), 15)


    screen.blit(landingPad, (screen_width/2-100, groundPixelY))#draw the landing pad

    
    for i in range(0, len(smoke)):
        pygame.draw.circle(screen, (100, 100, 100), (int(smoke[i][0]), int(smoke[i][1])), 1)
        smoke[i][1] -= 1

    falcon9STG1.draw(screen)

    updateObjects()

    pygame.display.flip()
    clock.tick(100)

pygame.quit()