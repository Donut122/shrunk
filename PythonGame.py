from tkinter.constants import S
from typing import Counter
import pygame
import os
import random
import time
import tkinter as tk
import win32gui, win32con
from pathlib import Path

path = Path(os.getcwd())

The_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(The_program_to_hide , win32con.SW_HIDE)


time.sleep(1)

root= tk.Tk()

root.geometry('500x300')
root.title("configuration ")

world_size = tk.Entry(root)
world_size.place(x=190, y=50)

def start():
    global x1
    x1 = world_size.get()
    root.destroy()
    
button1 = tk.Button(text='start game', command=start)
button1.place(x=220, y=250)

label_1 = tk.Label(root, text="world size:",width=20,font=("bold", 10))
label_1.place(x=170, y=25)

label_2 = tk.Label(root, text="world size is capped at 1,000. recommended 500",width=40,font=("bold", 10))
label_2.place(x=80, y=75)

x1 = world_size.get()
root.mainloop()

x1 = int(x1)
world_size = x1
world_size /= 2
world_size = round(world_size)

time.sleep(1)

width, height = 1500, 1000
fps = 60
WIN = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Game running @ " + str(width) + " x" + str(height))
clock = pygame.time.Clock()

pygame.display.init()

x = 725
xvel = 0

fall_checker = 0

blocks = []

y = 1500
yvel = 0

speed = 0.2
map = pygame.Rect(0, 0, 1, 1)

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
bg = pygame.Rect(0, 0, 1, 1)
run = True
class select:
    def __init__(self, rect):
        self.in_use = False
        self.rect = rect

selection = select(pygame.Rect(0, 0, 56, 56))

player = pygame.Rect(width // 2, height // 2, 50, 50)
class cube:
    def __init__(self, xpos, ypos, xcor, ycor, type, texture, rect):
        self.xpos = xpos
        self.ypos = ypos
        self.xcor = xcor
        self.ycor = ycor
        self.type = type
        self.texture = texture
        self.rect = rect
        self.loaded = True
        
world_negative = 0 - world_size
world_positive = world_size
block_tx_width, block_tx_height = 50, 50
bg_texture = pygame.image.load(os.path.join('Textures', 'background.png'))
bg_texture = pygame.transform.scale(bg_texture, (height * 3.69230769231, height))
bg = pygame.Rect(0, 0, 0, 0)
grass_texture = pygame.image.load(os.path.join('Textures', 'grass.png'))
grass_texture = pygame.transform.scale(grass_texture, (block_tx_width, block_tx_height))
compact_dirt_texture = pygame.image.load(os.path.join('Textures', 'compact dirt.png'))
compact_dirt_texture = pygame.transform.scale(compact_dirt_texture, (block_tx_width, block_tx_height))
stone_texture = pygame.image.load(os.path.join('Textures', 'stone.png'))
stone_texture = pygame.transform.scale(stone_texture, (block_tx_width, block_tx_height))
fall_checker = world_negative
layer = 0
has_below = []
empty_next = False
x_occu = 0
ran = 0
count = 0

grass_frames = []
stone_frames = []

grass_animation_path = str(path) + "/Textures/animations/dirt animation/frame "
stone_animation_path = str(path) + "/Textures/animations/stone animation/frame "
while True:
    count += 1
    frame = pygame.image.load(Path(grass_animation_path + str(count) + ".png"))
    frame = pygame.transform.scale(frame, (block_tx_width, block_tx_height))
    grass_frames.append(frame)
    if count == 6:
        break
count = 0
while True:
    count += 1
    frame = pygame.image.load(Path(stone_animation_path + str(count) + ".png"))
    frame = pygame.transform.scale(frame, (block_tx_width, block_tx_height))
    stone_frames.append(frame)
    if count == 7:
        break

count = 0


while True:
    if layer > -1 and layer < 6:
        block = cube(0, 0, fall_checker * 50, layer * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50))
        blocks.append(block)
        fall_checker += 1
        if fall_checker == world_positive:
            fall_checker = world_negative
            layer += 1

    if layer == 6:
        ran = random.randint(0, 2)
        if ran == 1:
            block = cube(0, 0, fall_checker * 50, layer * 50, "compact dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50))
        else:
            block = cube(0, 0, fall_checker * 50, layer * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50))

        blocks.append(block)
        fall_checker += 1
        if fall_checker == world_positive:
            fall_checker = world_negative
            layer += 1

    if layer == 7:
        ran = random.randint(0, 1)
        if ran == 1:
            block = cube(0, 0, fall_checker * 50, layer * 50, "compact dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50))
        else:
            block = cube(0, 0, fall_checker * 50, layer * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50))

        blocks.append(block)
        fall_checker += 1
        if fall_checker == world_positive:
            fall_checker = world_negative
            layer += 1
    
    if layer == 8 or layer == 9:
        block = cube(0, 0, fall_checker * 50, layer * 50, "compact dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50))
        blocks.append(block)
        fall_checker += 1
        if fall_checker == world_positive:
            fall_checker = world_negative
            layer += 1

    if layer == 10:
        ran = random.randint(0, (4 - count))
        if ran == 1:
            block = cube(0, 0, fall_checker * 50, layer * 50, "compact dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50))
            blocks.append(block)
            has_below.append(fall_checker)
            fall_checker += 1
            block = cube(0, 0, fall_checker * 50, layer * 50, "compact dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50))
            blocks.append(block)
            has_below.append(fall_checker)
            fall_checker += 1
            block = cube(0, 0, fall_checker * 50, layer * 50, "compact dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50))
            blocks.append(block)
            has_below.append(fall_checker)
            if count == 0:
                count = 3
            if count == 3:
                count = 0
        else:
            block = cube(0, 0, fall_checker * 50, layer * 50, "grass", grass_texture, pygame.Rect(50, 50, 50, 50))
            blocks.append(block)

        fall_checker += 1
        if fall_checker > (world_positive - 1):
            fall_checker = world_negative
            layer += 1
            count = 0

    if layer == 11:
        if fall_checker in has_below:
            block = cube(0, 0, fall_checker * 50, layer * 50, "grass", grass_texture, pygame.Rect(50, 50, 50, 50))
            blocks.append(block)
        fall_checker += 1
        if fall_checker == world_positive:
            fall_checker = 0
            break
pygame.init()
ragdoll = 0
xcor = 0
ycor = 0
filedat = ""
black = (0, 0, 0)

font = pygame.font.Font('freesansbold.ttf', 32)

xtext = font.render('xcor goes here', True, black)
xrect = xtext.get_rect()
xrect.y = 0
xrect.x = 0

ytext = font.render('ycor goes here', True, black)
yrect = ytext.get_rect()
yrect.y = 0
yrect.x = xrect.width * 1.2

ftext = font.render('fps goes here', True, black)
frect = ftext.get_rect()
frect.y = 0
frect.x = width / 2

def draw_graphics(player, blocks, selection):
    WIN.fill(white)
    WIN.blit(bg_texture, bg)
    pygame.draw.rect(WIN, black, player)
    if selection.in_use:
        pygame.draw.rect(WIN, black, selection.rect)

    for block in blocks:
        if block.loaded:
            WIN.blit(block.texture, (block.xpos, block.ypos))

    WIN.blit(xtext, xrect)
    WIN.blit(ytext, yrect)
    WIN.blit(ftext, frect)
    pygame.display.update()

standing = False
while run:
    draw_graphics(player, blocks, selection)

    clock.tick(fps)

    frect = ftext.get_rect()
    frect.x = (width - frect.width) - 5
    ftext = font.render("fps: " + str(round(clock.get_fps())), True, black, white)

    selection.in_use = False
    
    bg.x = 0 - (xcor + (world_positive) + bg.width) 
    xcor = 0 - round(x // 50)
    ycor = round(y // 50)

    xtext = font.render("x: " + str(xcor), True, black, white)
    xrect = xtext.get_rect()
    yrect.x = xrect.width * 1.3
    ytext = font.render("y: " + str(ycor), True, black, white)

    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_LEFT] and xvel < 3:
        if ragdoll < 1:
            xvel += speed
        else:
            ragdoll -= 1
            xvel /= 1.1

    elif key_pressed[pygame.K_RIGHT] and xvel > -3:
        if ragdoll < 1:
            xvel -= speed
        else:
            ragdoll -= 1
            xvel /= 1.1
    else:
        if xvel > 0.1:
            xvel -= 0.4
        elif xvel < -0.1:
            xvel += 0.4
        else:
            xvel = 0

    x += xvel
    y += yvel

    x = round(x)
    y = round(y)




    bg_texture = pygame.transform.scale(bg_texture, (height * 3.69230769231, height))
    mouse_pressed = pygame.mouse.get_pressed()

    for block in blocks:
        if x - block.xcor > 1800:
            block.loaded = False

        elif x - block.xcor < -200:
            block.loaded = False

        else:
            block.loaded = True
            block.xpos = x - block.xcor
            block.rect.x = block.xpos + 1
            block.ypos = y - block.ycor
            block.rect.y = block.ypos + 1

            if block.rect.colliderect(player):
                if abs(player.bottom - block.rect.top) < 40:
                    standing = True
                    fall_checker = 3
                elif abs(player.left - block.rect.right) < 30:
                    xvel = 0 - xvel
                    ragdoll = 7
                elif abs(player.right - block.rect.left) < 30:
                    xvel = 0 - xvel
                    ragdoll = 5
                elif abs(player.top - block.rect.bottom) < 30:
                    yvel = 0 - yvel
                    ragdoll = 7
            if block.rect.collidepoint(pygame.mouse.get_pos()):
                selection.in_use = True
                selection.rect.x = (block.rect.x - 4)
                selection.rect.y = (block.rect.y - 4)

                if (mouse_pressed[0]):
                    if block.type == "grass":
                        for frame in grass_frames:
                            block.texture = frame
                            draw_graphics(player, blocks, selection)
                            time.sleep(0.1)

                    if block.type == "stone":
                        for frame in stone_frames:
                            block.texture = frame
                            draw_graphics(player, blocks, selection)
                            time.sleep(0.1)
                    blocks.remove(block)
                    del block

 

    if fall_checker == 0:
        if standing:
            standing = False

    if fall_checker < 1:
        fall_checker = 0
    else:
        fall_checker -= 1

    if standing == False:
        if yvel - 0.4 > -10:
            yvel -= 0.4
    else:
        yvel = 0  

    width = WIN.get_width()
    height = WIN.get_height()

    player.x = width // 2
    player.y = height // 1.6

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ragdoll < 1:
                    if standing == True:
                        yvel = 10
                        standing = False
                        fall_checker = 0
                else:
                    ragdoll = 0