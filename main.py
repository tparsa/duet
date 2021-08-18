# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
import random

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 700], pygame.SRCALPHA)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameObject(pygame.sprite.Sprite):
    def __init__(self, originX, originY, color):
        super().__init__()
        self.origin = Point(originX, originY)
        self.color = color
        self.move_to(originX, originY)
    
    def move_to(self, x, y):
        self.origin.x = x
        self.origin.y = y
        self.rect.center = (x, y)

    def move_relativly(self, dX, dY):
        self.origin.x += dX
        self.origin.y += dY
        self.rect.x += dX
        self.rect.y += dY


class CircleGameObject(GameObject):
    def __init__(self, radius, *args, **kwargs):
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.radius = radius
        super().__init__(*args, **kwargs)
        pygame.draw.circle(self.surface, self.color, (radius, radius), self.radius)


class RectangleGameObject(GameObject):
    def __init__(self, lengthX, lengthY, *args, **kwargs):
        self.surface = pygame.Surface((lengthX, lengthY))
        self.rect = self.surface.get_rect()
        self.lengthX = lengthX
        self.lengthY = lengthY
        super().__init__(*args, **kwargs)
        self.surface.fill(self.color)

angle = 0
angle_velocity = 0

class ParticlePrinciple:
    def __init__(self, father, particle_type="circle"):
        self.particles = []
        self.father = father
        self.color = (*self.father.color, 128)
        self.particle_type = particle_type
    
    def emit(self, surface):
        cur_angle = angle
        if self.particles:
            self.delete_particles()
            if self.particle_type == "circle":
                first_half_points = []
                second_half_points = []
                for particle in self.particles[::-1]:
                    first_half_points.append(tuple([int(particle[0][0] + math.cos(cur_angle) * particle[1]), int(particle[0][1] + math.sin(cur_angle) * particle[1])]))
                    second_half_points.append(tuple([int(particle[0][0] + math.cos(cur_angle + math.pi) * particle[1]), int(particle[0][1] + math.sin(cur_angle + math.pi) * particle[1])]))
                    cur_angle -= (math.pi / 20) * angle_velocity
                if len(self.particles) > 2:
                    pygame.draw.polygon(surface, self.color, first_half_points + second_half_points[::-1])
            else:
                for particle in self.particles:
                    particle[1][0] -= 1
                    particle[1][1] -= 1
                    particle[3][3] -= 5
                    placement = list(particle[0] + particle[1])
                    placement[0] = int(particle[0][0] - particle[1][0]/2)
                    placement[1] = int(particle[0][1] - particle[1][1]/2)
                    pygame.draw.rect(surface, particle[3], placement)
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                if self.particle_type == "circle":
                    particle[1] -= 1


    def add_particles(self):
        pos_x = int(self.father.origin.x)
        pos_y = int(self.father.origin.y)
        direction_y = 0
        if self.particle_type == "circle":
            direction_x = 5
            radius = self.father.radius
            particle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        else:
            direction_x = 1
            lengthX = self.father.lengthX - 2
            lengthY = self.father.lengthY - 2
            particle = [[pos_x, pos_y], [lengthX, lengthY], [direction_x, direction_y], [*self.father.color, 100]]
        self.particles.append(particle)

    def delete_particles(self):
        if self.particle_type == "circle":
            particle_copy = [particle for particle in self.particles if particle[1] > 0]
        else:
            particle_copy = [particle for particle in self.particles if particle[1][0] > 0 and particle[1][1] > 0 and particle[3][3] > 0]
        self.particles = particle_copy

frame = 0
running = False
quit_game = False

screen.fill((0, 0, 0))

blue_circle = CircleGameObject(originX=350, originY=550, color=(0, 200, 255), radius=15)
red_circle = CircleGameObject(originX=150, originY=550, color=(150, 0, 0), radius=15)
red_circle_trace = []
obsticles = [
    RectangleGameObject(originX=+(random.choice([1.5, 2, 2.5]) * 100), originY=100 - i * random.choice([3, 4, 5]) * 100, color=(255, 255, 255), lengthX=150 + (random.choice([-2, -1, 0, 1])) * 5, lengthY=30)
    for i in range(20)
]

player_sprites = pygame.sprite.Group()
player_sprites.add(blue_circle)
player_sprites.add(red_circle)

obsticle_sprites = pygame.sprite.Group()

pygame.draw.circle(screen, (200, 200, 200), (250, 550), 100, 1)

screen.blit(blue_circle.surface, blue_circle.rect)
screen.blit(red_circle.surface, red_circle.rect)
for obsticle in obsticles:
    obsticle_sprites.add(obsticle)
    screen.blit(obsticle.surface, obsticle.rect)
pygame.display.flip()

while not running and not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
            break
        elif event.type == pygame.KEYDOWN:
            running = True
            break
        elif event.type == pygame.KEYUP:
            running = True
            break

particle_blue = ParticlePrinciple(blue_circle)
particle_red = ParticlePrinciple(red_circle)
obsticle_particles = [
    ParticlePrinciple(obsticle, particle_type="rectangle")
    for obsticle in obsticles
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle_velocity = -1
            elif event.key == pygame.K_RIGHT:
                angle_velocity = 1
        elif event.type == pygame.KEYUP:
            angle_velocity = 0
    screen.fill((0, 0, 0))
    surface = pygame.Surface([500, 700], pygame.SRCALPHA)
    surface.set_alpha(128)

    if angle_velocity:
        blue_circle.move_to(250 + math.cos(angle) * 100, 550 + math.sin(angle) * 100)
        red_circle.move_to(250 + math.cos(angle + math.pi) * 100, 550 + math.sin(angle + math.pi) * 100)
    particle_blue.add_particles()
    particle_red.add_particles()
    
    if frame % 2 == 0:
        pygame.draw.circle(screen, (200, 200, 200), (250, 550), 100, 1)
        particle_blue.emit(surface)
        particle_red.emit(surface)
        for obsticle_particle in obsticle_particles:
            obsticle_particle.emit(surface)
        screen.blit(blue_circle.surface, blue_circle.rect)
        screen.blit(red_circle.surface, red_circle.rect)
        for obsticle in obsticles:
            obsticle.move_relativly(0, 5)
            if obsticle.origin.y > -1 and obsticle.origin.y < 700:
                screen.blit(obsticle.surface, obsticle.rect)
                for obsticle_particle in obsticle_particles:
                    obsticle_particle.add_particles()
        angle += (math.pi / 20) * angle_velocity
        screen.blit(surface, (0, 0))
        pygame.display.flip()

    if pygame.sprite.groupcollide(player_sprites, obsticle_sprites, False, False):
        screen.blit(blue_circle.surface, blue_circle.rect)
        screen.blit(red_circle.surface, red_circle.rect)
        for obsticle in obsticles:
            screen.blit(obsticle.surface, obsticle.rect)
        running = False
        print("Game Over")
        break
    frame += 1
    pygame.time.wait(10)

# Done! Time to quit.
pygame.quit()