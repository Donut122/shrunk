import os
import random
import time
import tkinter as tk
from sre_constants import NOT_LITERAL
from tkinter.constants import S
from typing import Counter
import pygame
import win32con
import win32gui
from win32api import GetSystemMetrics
from perlin_noise import PerlinNoise
path = os.getcwd()
string = ""
string2 = ""

time.sleep(1)

root= tk.Tk()

black_alpha = (0, 0, 0, 10)

root.geometry('500x300')
root.title("world config")

world_seed = tk.Entry(root)
world_seed.place(x=190, y=200)

world_name = tk.Entry(root)
world_name.place(x=190, y=50)
def start():
    global x1
    global x2
    x1 = world_seed.get()
    x2 = world_name.get()
    root.destroy()
    
button1 = tk.Button(text='start game', command=start)
button1.place(x=220, y=250)

label_1 = tk.Label(root, text="world name:",width=20,font=("bold", 10))
label_1.place(x=170, y=25)

label_2 = tk.Label(root, text="world size (in blocks):",width=20,font=("bold", 10))
label_2.place(x=170, y=175)

label_3 = tk.Label(root, text="put the world name of a previously saved world to load it",width=40,font=("bold", 10))
label_3.place(x=80, y=80)

x1 = world_name.get()
x2 = world_seed.get()

root.mainloop()

if(len(x1)):
    x1 = int(x1)
    world_size = x1
    world_size /= 2
    world_size = round(world_size)
else:
    world_size = 20
world_name = x2

time.sleep(1)

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
fps = 60

x = 1000
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
class placer:
    def __init__(self, rect, xcor, ycor, xpos, ypos):
        self.rect = rect
        self.xcor = xcor
        self.ycor = ycor
        self.xpos = xpos
        self.ypos = ypos
        self.waiting = False
        self.approval = False

selection = select(pygame.Rect(0, 0, 56, 56))
hitbox = placer(pygame.Rect(0, 0, 25, 25), 0, 0, 0, 0)

player = pygame.Rect(width // 2, height // 2, 50, 100)
class cube:
    def __init__(self, xpos, ypos, xcor, ycor, type, texture, rect, hardness):
        self.xpos = xpos
        self.ypos = ypos
        self.xcor = xcor
        self.ycor = ycor
        self.type = type
        self.texture = texture
        self.rect = rect
        self.loaded = True
        self.hardness = hardness
        self.frames = []
        if type == "grass":
            for frame in grass_frames:
                self.frames.append(frame)
        if type == "stone":
            for frame in stone_frames:
                self.frames.append(frame)
        if type == "compact_dirt":
            for frame in compact_dirt_frames:
                self.frames.append(frame)
        self.break_stage = hardness
        self.count = len(self.frames)
        self.lightlevel = 0
        self.surface = pygame.Surface((50, 50))
        self.surface.set_alpha(self.lightlevel)

class health:
    def __init__(self, min_range, max_range, rect):
        self.min = min_range
        self.max = max_range
        self.rect = rect
        self.visible = True
        self.truepos = self.rect.y

class hotbar:
    def __init__(self, rect, texture):
        self.rect = rect
        self.item = "empty"
        self.texture = texture
        self.selected = False
        self.waiting = False
        self.hardness = 0

class item:
    def __init__(self, rect, type, xpos, ypos, xcor, ycor, texture, hardness):
        self.rect = rect
        self.type = type
        self.xpos = xpos
        self.ypos = ypos
        self.xcor = xcor
        self.ycor = ycor
        self.standing = False
        self.fall_checker = 0
        self.xvel = 0
        self.yvel = 0
        self.texture = texture
        self.hardness = hardness
        
world_negative = 0 - world_size
world_positive = world_size
block_tx_width, block_tx_height = 50, 50

loading_screen = pygame.image.load(os.path.join('Textures', 'loading_screen.png'))
loading_screen = pygame.transform.scale(loading_screen, (width, height))

WIN = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Game running @ " + str(width) + " x" + str(height))
clock = pygame.time.Clock()
pygame.display.init()
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 100)

loading_text = font.render("loading textures....", True, black)
loading_rect = loading_text.get_rect()
loading_rect.x = width / 2 - (loading_rect.width / 2)
loading_rect.y = height / 1.1

WIN.blit(loading_screen, (0, 0))
WIN.blit(loading_text, loading_rect)
pygame.display.update()
pointer_path = str(path) + "/Textures/pointers/"
normal_pointer = pygame.image.load(pointer_path + "pointer.png")
normal_pointer = pygame.transform.scale(normal_pointer, (25, 25))
grass_pointer = pygame.image.load(pointer_path + "grass pointer.png")
grass_pointer = pygame.transform.scale(grass_pointer, (25, 25))
dirt_pointer = pygame.image.load(pointer_path + "dirt pointer.png")
dirt_pointer = pygame.transform.scale(dirt_pointer, (25, 25))
stone_pointer = pygame.image.load(pointer_path + "stone pointer.png")
stone_pointer = pygame.transform.scale(stone_pointer, (25, 25))
tree_pointer = pygame.image.load(pointer_path + "tree pointer.png")
tree_pointer = pygame.transform.scale(tree_pointer, (25, 25))

grass_texture = pygame.image.load(os.path.join('Textures', 'grass.png'))
grass_texture = pygame.transform.scale(grass_texture, (block_tx_width, block_tx_height))
compact_dirt_texture = pygame.image.load(os.path.join('Textures', 'compact dirt.png'))
compact_dirt_texture = pygame.transform.scale(compact_dirt_texture, (block_tx_width, block_tx_height))
stone_texture = pygame.image.load(os.path.join('Textures', 'stone.png'))
stone_texture = pygame.transform.scale(stone_texture, (block_tx_width, block_tx_height))
tree_texture = pygame.image.load(os.path.join('Textures', 'tree.png'))
tree_texture = pygame.transform.scale(tree_texture, (block_tx_width * 5, block_tx_height * 5))
heart_full = pygame.image.load(os.path.join('Textures', 'heart_full.png'))
heart_full = pygame.transform.scale(heart_full, (block_tx_width, block_tx_height))
heart_empty = pygame.image.load(os.path.join('Textures', 'heart_empty.png'))
heart_empty = pygame.transform.scale(heart_empty, (block_tx_width, block_tx_height))
inv_slot = pygame.image.load(os.path.join('Textures', 'inv slot.png'))
inv_slot = pygame.transform.scale(inv_slot, (block_tx_width, block_tx_height))
player_tx_left = pygame.image.load(os.path.join('Textures', 'character_left.png'))
player_tx_left = pygame.transform.scale(player_tx_left, (50, 100))
player_tx_right = pygame.image.load(os.path.join('Textures', 'character_right.png'))
player_tx_right = pygame.transform.scale(player_tx_right, (50, 100))
button_tx = pygame.image.load(os.path.join('Textures', 'menu button.png'))

rig = []

class rig_part:
    def __init__(self, texture, locationx, locationy):
        self.texture = texture
        self.x = locationx
        self.y = locationy
        self.location = (locationx + width / 2 + 25, locationy + height / 2 + 102)
body_rig = pygame.image.load(os.path.join('Textures', 'left leg.png'))
body_rig = rig_part(pygame.transform.scale(body_rig, (16, 40)), -22, 85)
rig.append(body_rig)
body_rig = pygame.image.load(os.path.join('Textures', 'left arm.png'))
body_rig = rig_part(pygame.transform.scale(body_rig, (16, 40)), -22, 58)
rig.append(body_rig)
body_rig = pygame.image.load(os.path.join('Textures', 'body.png'))
body_rig = rig_part(pygame.transform.scale(body_rig, (30, 46)), -15, 46)
rig.append(body_rig)
body_rig = pygame.image.load(os.path.join('Textures', 'head.png'))
body_rig = rig_part(pygame.transform.scale(body_rig, (66, 37)), -33, 13)
rig.append(body_rig)
body_rig = pygame.image.load(os.path.join('Textures', 'right leg.png'))
body_rig = rig_part(pygame.transform.scale(body_rig, (16, 40)), 5, 85)
rig.append(body_rig)
body_rig = pygame.image.load(os.path.join('Textures', 'right arm.png'))
body_rig = rig_part(pygame.transform.scale(body_rig, (16, 40)), 5, 58)
rig.append(body_rig)

class player_stats:
    def __init__(self):
        self.facing = "left"

fall_checker = 0
ran = 0
count = 0
day_delay = 60

grass_frames = []
stone_frames = []
compact_dirt_frames = []
time_frames = []
player_inv = []



print("loading joe mamas textures")

grass_animation_path = str(path) + "/Textures/animations/dirt animation/frame "
stone_animation_path = str(path) + "/Textures/animations/stone animation/frame "
compact_dirt_animation_path = str(path) + "/Textures/animations/compact dirt animation/frame "
day_night_path = str(path) + "/Textures/animations/day_night cycle/frame "
while True:
    count += 1
    frame = pygame.image.load(grass_animation_path + str(count) + ".png")
    frame = pygame.transform.scale(frame, (block_tx_width, block_tx_height))
    grass_frames.append(frame)
    if count == 6:
        break
count = 0
while True:
    count += 1
    frame = pygame.image.load(stone_animation_path + str(count) + ".png")
    frame = pygame.transform.scale(frame, (block_tx_width, block_tx_height))
    stone_frames.append(frame)
    if count == 7:
        break

count = 0

while True:
    count += 1
    frame = pygame.image.load(compact_dirt_animation_path + str(count) + ".png")
    frame = pygame.transform.scale(frame, (block_tx_width, block_tx_height))
    compact_dirt_frames.append(frame)
    if count == 3:
        break

count = 0

while True:
    count += 1
    if count == 145:
        count += 38
    frame = pygame.image.load(day_night_path + str(count) + ".png")
    frame = pygame.transform.scale(frame, (width, height))
    time_frames.append(frame)
    if count == 296:
        break

count = 0
def menu_graphics(fill):
    if fill:
        WIN.fill(white)
    else:
        WIN.blit(loading_screen, (0, 0))
        WIN.blit(loading_text, loading_rect)
    WIN.blit(darkness, (0, 0))
    pygame.display.update()

print("finished loading joes textures")
darkness = pygame.Surface((width, height))
def fadeout():
    darkness.set_alpha(1)
    for x in range(127):
        darkness.set_alpha(darkness.get_alpha() + 2)
        menu_graphics(fill=False)
def fadein():
    for x in range(255):
        darkness.set_alpha(darkness.get_alpha() - 1)
        menu_graphics(fill=False)
if os.path.exists(world_name + ".txt"):
    print("world save under the name '" + world_name + "' detected, loading world")
    fadeout()
    time.sleep(1)
    loading_screen = pygame.image.load(os.path.join('Textures', 'loading_screen(2).png'))
    loading_screen = pygame.transform.scale(loading_screen, (width, height))
    loading_text = font.render("analysing world data...", True, black)
    fadein()
    loading_rect = loading_text.get_rect()
    loading_rect.x = width / 2 - (loading_rect.width / 2)
    loading_rect.y = height / 1.1

    WIN.blit(loading_screen, (0, 0))
    WIN.blit(loading_text, loading_rect)
    pygame.display.update()
    time.sleep(1)
    file = open(world_name + ".txt", "r")
    exec(file.read())
    file.close()
else:
    print("no world under the name " + world_name + " detected, genorating new world")
    fadeout()
    time.sleep(1)
    loading_screen = pygame.image.load(os.path.join('Textures', 'loading_screen(2).png'))
    loading_screen = pygame.transform.scale(loading_screen, (width, height))
    loading_text = font.render("genorating new world...", True, black)
    fadein()
    loading_rect = loading_text.get_rect()
    loading_rect.x = width / 2 - (loading_rect.width / 2)
    loading_rect.y = height / 1.1

    WIN.blit(loading_screen, (0, 0))
    WIN.blit(loading_text, loading_rect)
    pygame.display.update()
    time.sleep(1)
    fall_checker = 0
    xpos = world_negative
    ypos = 1

    while True:
        if ypos == 1:
            block = cube(0, 0, xpos * 50, ypos * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50), 7)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative
        
        if ypos > 1 and ypos < 6:
            block = cube(0, 0, xpos * 50, ypos * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50), 7)
            blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative

        if ypos == 6:
            block = cube(0, 0, xpos * 50, ypos * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50), 7)
            blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative

        if ypos == 7:
            ran = random.randint(0, 2) 
            if ran == 0:
                block = cube(0, 0, xpos * 50, ypos * 50, "compact_dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50), 3)
                blocks.append(block)
            else:
                block = cube(0, 0, xpos * 50, ypos * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50), 7)
                blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative

        if ypos == 8:
            ran = random.randint(0, 1) 
            if ran == 0:
                block = cube(0, 0, xpos * 50, ypos * 50, "compact_dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50), 3)
                blocks.append(block)
            else:
                block = cube(0, 0, xpos * 50, ypos * 50, "stone", stone_texture, pygame.Rect(50, 50, 50, 50), 7)
                blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative

        if ypos > 8 and ypos < 11:
            block = cube(0, 0, xpos * 50, ypos * 50, "compact_dirt", compact_dirt_texture, pygame.Rect(50, 50, 50, 50), 3)
            blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative

        if ypos == 11:
            block = cube(0, 0, xpos * 50, ypos * 50, "grass", grass_texture, pygame.Rect(50, 50, 50, 50), 6)
            blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative
                break
        if ypos == 12:
            ran = random.randint(0, 4)
            if ran == 1:
                block = cube(0, 0, xpos * 50, ypos * 50, "tree", tree_texture, pygame.Rect(50, 50, 50, 50), 1)
                blocks.append(block)
            xpos += 1
            if xpos == world_positive + 1:
                ypos += 1
                xpos = world_negative
fadeout()
time.sleep(1)
paused = False
ragdoll = 0
xcor = 0
ycor = 0
filedat = ""
black = (0, 0, 0)

crusor = pygame.Rect(25, 25, 25, 25)

pygame.mouse.set_visible(False)

player_health = 40

hearts = []
slots = []
items = []
entity = []

slot = hotbar(pygame.Rect(width / 2, height - 60, 50, 50), "")
slots.append(slot)
slot = hotbar(pygame.Rect((width / 2) - 50, height - 60, 50, 50), "")
slots.append(slot)
slot = hotbar(pygame.Rect((width / 2) + 50, height - 60, 50, 50), "")
slots.append(slot)

heart = health(20, 30, pygame.Rect((width / 2) + 50, height - 120, 40, 40))
hearts.append(heart)
heart = health(10, 20, pygame.Rect((width / 2), height - 120, 40, 40))
hearts.append(heart)
heart = health(0, 10, pygame.Rect((width / 2) - 50, height - 120, 40, 40))
hearts.append(heart)
game_time = 0
gtime = -90

font = pygame.font.Font('freesansbold.ttf', 32)

xtext = font.render('xcor goes here', True, black, white)
xrect = xtext.get_rect()
xrect.y = 0
xrect.x = 0

ytext = font.render('ycor goes here', True, black, white)
yrect = ytext.get_rect()
yrect.y = 0
yrect.x = xrect.width * 1.2

ftext = font.render('fps goes here', True, black, white)
frect = ftext.get_rect()
frect.y = 0
frect.x = width / 2

quit_text = font.render('quit game (without saving)', True, black)
quit_button = quit_text.get_rect()
quit_button.centerx = height / 1.8
quit_button.centery = width / 2
quit_button_tx = pygame.transform.scale(button_tx, (quit_button.width, quit_button.height))
resume_text = font.render('resume game', True, black)
resume_button = ftext.get_rect()
resume_button.centery = height / 2.2
resume_button.centerx = width / 2
resume_button_tx = pygame.transform.scale(button_tx, (resume_button.width, resume_button.height))
save_quit_text = font.render('save and quit', True, black)
save_quit_button = ftext.get_rect()
save_quit_button.centery = height / 1.5
save_quit_button.centerx = width / 2
save_quit_button_tx = pygame.transform.scale(button_tx, (save_quit_button.width, save_quit_button.height))

def select_pointer(selected_pointer):
    if selected_pointer == "grass":
        selected_pointer = grass_pointer
    elif selected_pointer == "compact_dirt":
        selected_pointer = dirt_pointer
    elif selected_pointer == "stone":
        selected_pointer = stone_pointer
    else:
        selected_pointer = normal_pointer
    return selected_pointer
def save(blocks):
    file = open(world_name + ".txt", "w")
    for block in blocks:
        file.write("block = cube(" + str(block.xpos) + ", " + str(block.ypos) + ", " + str(block.xcor) + ", " + str(block.ycor) + ", '" + str(block.type) + "', " + str(block.type) + "_texture" + ", " + "pygame.Rect(50, 50, 50, 50)" + ", " + str(block.hardness) + ")\nblocks.append(block)\n")
    file.write("\nx = " + str(x) + "\ny = " + str(y) + "\ngame_time = " + str(game_time) + "\ngtime = " + str(gtime))
    file.close()



def freeze():
    global run
    global paused
    while True:
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crusor.x = mouse_x
        crusor.y = mouse_y
        clock.tick(fps)
        if quit_button.collidepoint(pygame.mouse.get_pos()):
            if (mouse_pressed[0]):
                pygame.display.quit()
                pygame.quit()
                run = False
                break

        if save_quit_button.collidepoint(pygame.mouse.get_pos()):
            if (mouse_pressed[0]):
                save(blocks)
                pygame.display.quit()
                pygame.quit()
                run = False
                break

        if resume_button.collidepoint(pygame.mouse.get_pos()):
            if (mouse_pressed[0]):
                paused = False
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                run = False
        draw_graphics(player, blocks, selection, game_time, time_frames)
selected_pointer = normal_pointer
player_info = player_stats()
def draw_graphics(player, blocks, selection, game_time, time_frames):
    WIN.blit(time_frames[game_time], (0, 0))
    if player_info.facing == "left":
        WIN.blit(player_tx_left, player)
    else:
        WIN.blit(player_tx_right, player)
    if selection.in_use:
        pygame.draw.rect(WIN, black, selection.rect)

    for block in blocks:
        if block.loaded:
            if block.type == "tree":
                WIN.blit(block.texture, (block.xpos - block_tx_width * 2.5, block.ypos - block_tx_height * 3))
            else:
                WIN.blit(block.texture, (block.xpos, block.ypos))
                WIN.blit(block.surface, (block.xpos, block.ypos))

    for drop in entity:
        WIN.blit(drop.texture, (drop.xpos, drop.ypos))
    WIN.blit(xtext, xrect)
    WIN.blit(ytext, yrect)
    WIN.blit(ftext, frect)
    for heart in hearts:
        if heart.visible:
            WIN.blit(heart_full, heart.rect)
        else:
            WIN.blit(heart_empty, heart.rect)
    for slot in slots:
        WIN.blit(inv_slot, slot.rect)
        if not slot.item == "empty":
            WIN.blit(pygame.transform.scale(slot.texture, (25, 25)), (slot.rect.x + 12, slot.rect.y + 12))

    if paused:
        WIN.blit(quit_button_tx, quit_button)
        WIN.blit(quit_text, quit_button)
        WIN.blit(resume_button_tx, resume_button)
        WIN.blit(resume_text, resume_button)
        WIN.blit(save_quit_button_tx, save_quit_button)
        WIN.blit(save_quit_text, save_quit_button)
    WIN.blit(selected_pointer, crusor)

    pygame.display.update()

standing = False
for x in range(255):
    darkness.set_alpha(darkness.get_alpha() - 1)
    WIN.fill(white)
    menu_graphics(fill=True)
while run:
    draw_graphics(player, blocks, selection, game_time, time_frames)
    clock.tick(fps)
    selected_pointer = select_pointer(selected_pointer)

    frect = ftext.get_rect()
    frect.x = (width - frect.width) - 5
    ftext = font.render("fps: " + str(round(clock.get_fps())), True, black, white)

    selection.in_use = False
    xcor = 0 - round(x // 50)
    ycor = round(y // 50)
    cor = (xcor, ycor)

    xtext = font.render("x: " + str(xcor), True, black, white)
    xrect = xtext.get_rect()
    yrect.x = xrect.width * 1.3
    ytext = font.render("y: " + str(ycor), True, black, white)

    key_pressed = pygame.key.get_pressed()

    for heart in hearts:
        if heart.min < player_health:
            heart.visible = True
            if heart.max > player_health:
                heart.rect.y += 3
                if heart.rect.y > heart.truepos + 9:
                    heart.rect.y = heart.truepos - 9

        else:
            heart.visible = False

    if key_pressed[pygame.K_LEFT] and xvel < 3:
        player_info.facing = "left"
        if ragdoll < 1:
            xvel += speed
        else:
            ragdoll -= 1
            xvel /= 1.1

    elif key_pressed[pygame.K_RIGHT] and xvel > -3:
        player_info.facing = "right"
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

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    crusor.x = mouse_x
    crusor.y = mouse_y


    for slot in slots:
        taken_slots = 0
        for drop in items:
            if slot.item == "empty":
                slot.item = drop.type
                slot.texture = drop.texture
                slot.hardness = drop.hardness
                items.remove(drop)
        if not slot.item == "empty":
            taken_slots += 1

        if slot.waiting:
            slot.waiting = False
            hitbox.waiting = False
            if hitbox.approval:
                if slot.item == "grass":
                    slot.texture = grass_texture
                elif slot.item == "compact_dirt":
                    slot.texture = compact_dirt_texture
                else:
                    slot.texture = stone_texture
                block = cube(0, 0, hitbox.xcor, hitbox.ycor, slot.item, slot.texture, pygame.Rect(50, 50, 50, 50), slot.hardness)
                blocks.append(block)
                slot.item = "empty"
        if slot.rect.collidepoint(pygame.mouse.get_pos()) and (mouse_pressed[2]):
            slot.item = "empty"
        elif slot.rect.collidepoint(pygame.mouse.get_pos()) and (mouse_pressed[0]):
            slot.selected = True
        elif not slot.rect.collidepoint(pygame.mouse.get_pos()) and (mouse_pressed[0]):
            if slot.selected and not slot.item == "empty":
                hitbox.rect.x = mouse_x
                hitbox.rect.y = mouse_y
                hitbox.xcor = round(x - (round(mouse_x / 50) * 50))
                hitbox.ycor = round(y - (round(mouse_y / 50) * 50))
                hitbox.waiting = True
                hitbox.approval = True
                slot.waiting = True
            elif slot.selected:
                slot.selected = False
                
    day_delay -= 1
    if day_delay == 0:
        day_delay = 60
        game_time += 1
        gtime += 2
        if game_time == len(time_frames):
            game_time = 0
        if game_time == 6:
            gtime = -90

    for block in blocks:
        if x - block.xcor > width + 100:
            block.loaded = False

        elif x - block.xcor < -50:
            block.loaded = False

        else:
            block.loaded = True
            block.xpos = x - block.xcor
            block.rect.x = block.xpos + 1
            block.ypos = y - block.ycor
            block.rect.y = block.ypos + 1

            if gtime > -1 and gtime < 256:
                block.lightlevel = gtime

            else:
                if gtime < 0:
                    block.lightlevel = 0
                if gtime > 255:
                    block.lightlevel = 255

            block.surface.set_alpha(block.lightlevel)
            

            if block.rect.colliderect(player):
                if not block.type == "tree":
                    if abs(player.bottom - block.rect.top) < 40:
                        standing = True
                        fall_checker = 3
                    elif abs(player.left - block.rect.right) < 30:
                        xvel = 0 - (xvel + 1.5) 
                        ragdoll = 7
                    elif abs(player.right - block.rect.left) < 30:
                        xvel = 0 - (xvel - 1.5)
                        ragdoll = 5
                    elif abs(player.top - block.rect.bottom) < 30:
                        yvel = 0 - yvel
                        ragdoll = 7

                for drop in items:
                    if block.rect.colliderect(drop.rect):
                        if abs(drop.rect.bottom - block.rect.top) < 40:
                            drop.standing = True
                            drop.fall_checker = 3
                        elif abs(drop.rect.left - block.rect.right) < 30:
                            drop.xvel = 0 - (xvel + 1.5) 
                        elif abs(drop.rect.right - block.rect.left) < 30:
                            drop.xvel = 0 - (xvel - 1.5)

            if block.rect.collidepoint(pygame.mouse.get_pos()):
                selection.in_use = True
                selection.rect.x = (block.rect.x - 4)
                selection.rect.y = (block.rect.y - 4)
                selected_pointer = block.type
                selected_pointer = select_pointer(selected_pointer)

                if (mouse_pressed[2]):
                    if block.count == 0:
                        block.count = block.hardness
                        block.texture = block.frames[0 - (block.break_stage - 1)]
                        block.break_stage -= 1
                        if block.break_stage == 0:
                            block.texture = pygame.transform.scale(block.texture, (20, 20))
                            drop = item(pygame.Rect(20, 20, 20, 20), block.type, block.xcor - 15, block.ycor - 15, block.xcor - 15, block.ycor - 15, block.texture, block.hardness)
                            entity.append(drop)
                            blocks.remove(block)
                            del block
                    else:
                        block.count -= 1

            if hitbox.waiting == True:
                if block.rect.colliderect(hitbox.rect):
                    hitbox.approval = False
                    blocks.remove(block)
                    del block

    mouse_position = pygame.mouse.get_pos()


    if fall_checker == 0:
        if standing:
            standing = False

    if fall_checker < 1:
        fall_checker = 0
    else:
        fall_checker -= 1

    if standing == False:
        if yvel - 0.4 > -5:
            yvel -= 0.4
    else:
        yvel = 0  


    player.x = width // 2
    player.y = height // 1.6

    for drop in entity:
        drop.xpos = x - drop.xcor
        drop.ypos = y - drop.ycor
        drop.rect.x = drop.xpos
        drop.rect.y = drop.ypos
        if taken_slots <= len(slots):
            if drop.rect.colliderect(player):
                if abs(player.bottom - drop.rect.top) < 40:
                    items.append(drop)
                    entity.remove(drop)
                    del drop
                elif abs(player.left - drop.rect.right) < 30:
                    items.append(drop)
                    entity.remove(drop)
                    del drop
                elif abs(player.right - drop.rect.left) < 30:
                    items.append(drop)
                    entity.remove(drop)
                    del drop

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

            if event.key == pygame.K_ESCAPE:
                paused = True
                freeze()

            if event.key == pygame.K_q:
                save(blocks)
