import pygame
import os
import math
import random

#sets the screen to the top left corner of the monitor
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (5, 5)
pygame.init()

wS = 500

window = pygame.display.set_mode((wS, wS), 0, 0)

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

showInfo = False

class Obstacle:
    def __init__(self, position, velocity, radius, elasticity, mass, color):
        self.position = position
        self.velocity = velocity
        self.radius = radius
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
        if self.position[0] > wS or self.position[0] < 0:
            self.position[0] += wS * sign(self.position[0]) * -1
        if self.position[1] > wS or self.position[1] < 0:
            self.position[1] += wS * sign(self.position[1]) * -1


    def softCollisions(self, obs):
        loc = self.position
        rad = self.radius
        newV = self.velocity

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



                    dispX = (oP[0] - loc[0])
                    dispY = (oP[1] - loc[1])
                    mag = dist(dispX, dispY)
                    angA = math.atan(dispY / dispX)
                    angB = math.acos(dispX / mag)
                    t = math.cos(angB) / math.fabs(math.cos(angB))



                    pull = -(math.e / 10) / ((d) ** 2)


                    instances += 1
                    sumPull += pull
                    avgPull = sumPull / instances

                    if math.fabs(pull) < math.fabs(minPull):
                        minPull = pull
                    if math.fabs(pull) > math.fabs(maxPull):
                        maxPull = pull

                    newV[0] += pull * math.cos(angA) * scalar * t
                    newV[1] += pull * math.sin(angA) * scalar * t


        return newV








def Obstacles(obs):

    newVs = []
    for i in range(len(obs)):

        position = obs[i].getPosition()
        color = obs[i].getColor()
        radius = obs[i].getRadius()
        #collisions, newV = obs[i].isColliding(obs)
        #newVs.append(newV)
        newVs.append(obs[i].softCollisions(obs))

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


        global avgPull
        global maxPull
        global minPull



        WHITE = (250, 250, 250)



        avg = font.render("Average pull: " + str(avgPull), False, WHITE)
        maX = font.render("Max pull: " + str(maxPull), False, WHITE)
        miN = font.render("Min pull: " + str(minPull), False, WHITE)
        window.blit(avg, (wS - 200, 2))
        window.blit(maX, (wS - 200, 20))
        window.blit(miN, (wS - 200, 38))








def run():
    clock = pygame.time.Clock()

    numOfObs = 20
    obstacles = []
    maxR = 7
    minR = 2
    maxV = 0.1
    maxE = 1
    maxM = 1
    minM = 1


    for i in range(numOfObs):
        overlapping = True
        pos = [0, 0]
        while overlapping and len(obstacles) > 0:
            pos = [rand(0, wS), rand(0, wS)]
            for u in range(len(obstacles)):
                if dist(pos, obstacles[u].getPosition()) > 80:
                    overlapping = False

        obstacles.append(Obstacle(pos, [rand(-maxV, maxV), rand(-maxV, maxV)], rand(minR, maxR), rand(0.2, maxE), rand(minM, maxM), (int(rand(0, 250)), int(rand(0, 250)), int(rand(0, 250)))))


    global showInfo

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

        Obstacles(obstacles)
        hud(clock.get_fps())
        pygame.display.flip()

def main():
    run()

main()








pygame.quit()
quit()