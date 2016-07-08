import pygame
import time
import random

pygame.init()

driving_sound = pygame.mixer.Sound('sound/racing01.ogg')
crashed_sound = pygame.mixer.Sound('sound/crash03.ogg')
pygame.mixer.music.load('sound/Movin.ogg')

screen_size = pygame.display.Info()
display_w = screen_size.current_w
display_h = screen_size.current_h

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
dark_green = (0,100,0)
green = (0,255,0)
blue = (0,0,255)
light_red = (200,0,0)
light_green = (0,200,0)

largeText = pygame.font.SysFont('DejaVuSansMono-Bold.ttf',90)
smallText = pygame.font.SysFont("DejaVuSansMono-Bold.ttf",25)

# according to the Pygame's doc, the icon should be set before set_mode()
icon = pygame.image.load('pics/car_icon.png')
pygame.display.set_caption('Racing Car')
pygame.display.set_icon(icon)

#gameDisplay = pygame.display.set_mode((display_w,display_h), pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((display_w,display_h))
clock = pygame.time.Clock()

# loading other cars
cars = {}
for i in range(0,9):
    img_path = 'pics/car_'+str(i+1)+'.png'
    cars[i] = pygame.image.load(img_path)

car_w, car_h = cars[0].get_rect().size

def obs_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, white)
    gameDisplay.blit(text,(0,0))

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def mycar(x,y):
    gameDisplay.blit(cars[0],(x,y))

def show_cars(para):
    x,y,w,h,n = para
    gameDisplay.blit(cars[n],(x,y))

def cars_init(band):
    x0 = random.randrange(band,display_w - car_w - band)
    y0 = -display_h
    number = random.randrange(2,9)
    w, h = cars[0].get_rect().size
    speed = 10

    return (x0,y0,w,h,number), speed

def cars_update(para, speed, band):
    x,y,w,h,n = para
    y += speed
    if y > display_h:
        y = -h
        x = random.randrange(band,display_w - car_w - band)
        n = random.randrange(2,9)

    return (x,y,w,h,n)

def dodge_detect(mycar, othercar, speed):
    collide = bool(mycar.colliderect(othercar))
    if(collide is True):
        return False
    elif(collide is False and
            othercar[1] > display_h - speed):
        return True
    else:
        return None

def collision_detect(car, obs, speed):
    car_lc = (car[0], car[1])
    car_rc = (car[0] + car_w, car[1])
    obs_lc = (obs[0], obs[1] + obs[3])
    obs_rc = (obs[0] + obs[2], obs[1] + obs[3])

    if (obs_lc[1] > car_lc[1] and 
            (obs_rc[0] > car_lc[0] and obs_lc[0] < car_rc[0])
            ):
        return True
    elif (obs[1] > display_h-speed and 
            not(obs_rc[0] > car_lc[0] and obs_lc[0] < car_rc[0])
            ):
        return False
    else:
        return None

def crashed(final_score):
    pygame.mixer.music.stop()
    driving_sound.stop()
    
    pygame.mixer.Sound.play(crashed_sound)

    textImg, textPos = text_objects('Crashed!', largeText)
    textPos.center = (display_w*0.5, display_h*0.3)
    gameDisplay.blit(textImg, textPos)
    textImg, textPos = text_objects('Score: '+str(final_score), largeText)
    textPos.center = (display_w*0.5, display_h*0.5)
    gameDisplay.blit(textImg, textPos)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        butt_w, butt_h = 100, 50
        add_button((250,display_h-150,butt_w,butt_h),green,"Replay",game_loop)
        add_button((display_w-butt_w-250,display_h-150,butt_w,butt_h),red,"EXIT",quit_game)
        
        pygame.display.update()
        clock.tick(10)


def add_button(dimensions, color, text, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    x,y,w,h = dimensions
    if (x < mouse[0] < x+w and
            y < mouse[1] < y+h):
        pygame.draw.rect(gameDisplay, color, dimensions)
        if (click[0] == 1 and action != None):
            action()
    else:
        light_color = tuple(color[i] - 50 if color[i] >50 else color[i] for i in range(len(color)))
        pygame.draw.rect(gameDisplay, light_color, dimensions)

    textImg, textPos = text_objects(text, smallText)
    textPos.center = (x + 0.5*w, y + 0.5*h)
    gameDisplay.blit(textImg, textPos)

def quit_game():
    pygame.quit()
    quit()

def cont():
    pygame.mixer.music.unpause()
    paused(False)

def paused(pause):

    paused.pause = pause # use function's attribute as a static variable

    gameDisplay.fill(black)
    textImg, textPos = text_objects('PAUSED', largeText)
    textPos.center = (display_w*0.5, display_h*0.5)
    gameDisplay.blit(textImg, textPos)
    
    while paused.pause:
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        butt_w, butt_h = 100, 50
        add_button((250,display_h-150,butt_w,butt_h),green,"Cont.",cont)
        add_button((display_w-butt_w-250,display_h-150,butt_w,butt_h),red,"EXIT",quit_game)

        pygame.display.update()
        clock.tick(10)


def game_intro():
    driving_sound.play(loops=1)
    
    textImg, textPos = text_objects('1. Use arrow keys                 ', largeText)
    textPos.center = (display_w*0.5, display_h*0.3)
    gameDisplay.blit(textImg, textPos)
    textImg, textPos = text_objects('   to dodge the other cars.', largeText)
    textPos.center = (display_w*0.5, display_h*0.4)
    gameDisplay.blit(textImg, textPos)
    textImg, textPos = text_objects('2. Use p key to pause.         ', largeText)
    textPos.center = (display_w*0.5, display_h*0.5)
    gameDisplay.blit(textImg, textPos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        butt_w, butt_h = 100, 50
        add_button((250,display_h-150,butt_w,butt_h),green,"GO!",game_loop)
        add_button((display_w-butt_w-250,display_h-150,butt_w,butt_h),red,"EXIT",quit_game)
        
        pygame.display.update()
        clock.tick(10)

def game_loop():
    pygame.mixer.music.play(loops=-1)

    x = (display_w * 0.45)
    y = (display_h * 0.70)

    dx = 0
    dy = 0

    band = 100
    max_band = (display_w - 5.0*car_w) * 0.5

    cars_para, speed = cars_init(band)

    gameExit = False
    dodged_count = 0

    while not gameExit:
        gameDisplay.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -speed
                if event.key == pygame.K_RIGHT:
                    dx = speed
                if event.key == pygame.K_UP:
                    dy = -speed
                if event.key == pygame.K_DOWN:
                    dy = speed
                if event.key == pygame.K_p:
                    paused(True)

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or 
                        event.key == pygame.K_RIGHT or
                        event.key == pygame.K_UP or
                        event.key == pygame.K_DOWN
                        ):
                    dx = 0
                    dy = 0

        # lateral boundaries of mycar
        pygame.draw.rect(gameDisplay, dark_green, [0,0,band,display_h])
        pygame.draw.rect(gameDisplay, dark_green, [display_w-band,0,band,display_h])
        boundary = [0+band, display_w - car_w - band]
        if x > boundary[1]:
            x = boundary[1]
        elif x < boundary[0]:
            x = boundary[0]
        elif y > display_h - car_h:
            y =  display_h - car_h
        elif y < 0:
            y = 0
        else:
            x += dx
            y += dy

        mycar(x,y)

        cars_para = cars_update(cars_para, speed, band)
        show_cars(cars_para)

        mycarRect = pygame.Rect(x,y,car_w,car_h)
        othercarRect = pygame.Rect(cars_para[0:4])
        dodged = dodge_detect(mycarRect, othercarRect, speed)

        if (dodged is True):
            dodged_count += 1
            obs_dodged(dodged_count)
            if (dodged_count%5 == 0):
                band += int(500/dodged_count)
                if (band > max_band): 
                    band = max_band
                    speed += 1

        elif (dodged is False):
            crashed(dodged_count)
        else:
            pass

        obs_dodged(dodged_count)

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
quit_game()
