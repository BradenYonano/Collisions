import pygame
import os
import math
import random

#sets the screen to the top left corner of the monitor
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (5, 5)
pygame.init()

wS = 600

window = pygame.display.set_mode((wS, wS), 0, 0)

center = [wS/2, wS/2]
centerMass = 100000000000
G = 0.0000000000667408
pi = math.pi

scalar = 4
avgPull = 0
instances = 0
maxPull = 0
minPull = 10
sumPull = 0
avgNumerator = 0
sumNumerator = 0
maxNum = 0
minNum = 1000
density = 10

showInfo = False
gravEnabled = False

class Obstacle:
    def __init__(self, position, velocity, radius, elasticity, mass, color):
        self.position = position
        self.velocity = velocity
        self.radius = (mass / density)
        self.color = color
        self.angle = math.atan(velocity[1]/velocity[0])
        self.elasticity = elasticity
        self.mass = mass



    def getPosition(self):
        return self.position

    def getVelocity(self):
        return self.velocity

    def getRadius(self):
        return self.radius

    def getElasticity(self):
        return self.elasticity

    def getMass(self):
        return self.mass
    def getColor(self):
        return self.color

    def setVelocity(self, velocity):
        self.velocity = velocity
        self.angle = math.atan(velocity[1]/velocity[0])

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[0] %= wS
        self.position[1] %= wS


    def softCollisions(self, obs):
        loc = self.position
        rad = self.radius
        newV = self.velocity
        m = self.mass

        for i in range(len(obs)):

            if not obs[i] == self:
                oP = obs[i].getPosition()
                oR = obs[i].getRadius()
                d = dist(loc, oP)
                if d <= (rad + oR):
                    global scalar
                    global avgPull
                    global sumPull
                    global minPull
                    global maxPull
                    global instances

                    #the percent of the net mass (both masses combined) that the other object is
                    oM = obs[i].getMass()
                    tM = m + oM
                    opM = oM/tM

                    dispX = (oP[0] - loc[0])
                    dispY = (oP[1] - loc[1])
                    mag = dist(dispX, dispY)
                    angA = math.atan(dispY / dispX)
                    angB = math.acos(dispX / mag)
                    t = math.cos(angB) / math.fabs(math.cos(angB))

                    pull = -(math.e / 10) / ((d) ** 2)

                    newV[0] += pull * math.cos(angA) * scalar * t * opM
                    newV[1] += pull * math.sin(angA) * scalar * t * opM
                    newV[0] *= obs[i].getElasticity()
                    newV[1] *= obs[i].getElasticity()


        return newV

    def gravity(self):
        global center
        global centerMass
        global G

        pos = self.position

        dif = [pos[0] - center[0], pos[1] - center[1]]
        cAng = math.atan(dif[1]/dif[0])
        mag = dist(dif[0], dif[1])
        bAng = math.acos(dif[0] / mag)
        t = math.cos(bAng)/math.fabs(math.cos(bAng))

        d = dist(pos, center)

        newV = self.getVelocity()

        newV[0] -= ((centerMass * G)/(d ** 2)) * math.cos(cAng) * t
        newV[1] -= ((centerMass * G)/(d ** 2)) * math.sin(cAng) * t



        pygame.draw.circle(window, (250, 250, 250), (int(center[0]), int(center[1])), 10)

        return newV







def Obstacles(obs):

    newVs = []
    for i in range(len(obs)):

        position = obs[i].getPosition()
        color = obs[i].getColor()
        radius = obs[i].getRadius()

        newVs.append(obs[i].softCollisions(obs))
        if gravEnabled:
            newVs.pop(len(newVs) - 1)
            newVs.append(obs[i].gravity())


        pygame.draw.circle(window, (int(color[0]), int(color[1]), int(color[2])), (int(position[0]), int(position[1])), int(radius))

    for i in range(len(obs)):
        obs[i].setVelocity(newVs[i])
        obs[i].move()






def dist(pos1, pos2):
    if type(pos1) == list:
        return math.sqrt((((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2)))
    elif type(pos1) == int or type(pos1) == float:
        return math.sqrt((pos1 ** 2) + (pos2 ** 2))


def rand(mi, ma):
    r = random.random()
    return (mi + (r * (ma - mi)))

def sign(input):
    return (input/math.fabs(input))

def hud(fps):
    global showInfo
    if showInfo:

        font = pygame.font.SysFont('arial', 10)

        frames = font.render("FPS: " + str(math.floor(fps)), False, (250, 250, 250))
        window.blit(frames, (2, 2))

def run():
    clock = pygame.time.Clock()

    numOfObs = 30
    obstacles = []
    maxR = 7
    minR = 2
    maxV = 1
    maxE = 1
    minE = 0.9
    maxM = 100
    minM = 1


    for i in range(numOfObs):
        overlapping = True
        pos = [0, 0]
        while overlapping and len(obstacles) > 0:
            pos = [rand(0, wS), rand(0, wS)]
            for u in range(len(obstacles)):
                if dist(pos, obstacles[u].getPosition()) > 80:
                    overlapping = False

        obstacles.append(Obstacle(pos, [rand(-maxV, maxV), rand(-maxV, maxV)], rand(minR, maxR), rand(minE, maxE), rand(minM, maxM), (int(rand(0, 250)), int(rand(0, 250)), int(rand(0, 250)))))


    global showInfo
    global gravEnabled

    while True:
        window.fill((0, 0, 0))
        clock.tick()


        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pass
        if keys[pygame.K_ESCAPE]:
            break

        if keys[pygame.K_i]:
            showInfo = True
        else:
            showInfo = False

        if keys[pygame.K_g]:
            gravEnabled = True
        else:
            gravEnabled = False


        Obstacles(obstacles)
        hud(clock.get_fps())
        pygame.display.flip()

def main():
    run()

main()








pygame.quit()
quit()