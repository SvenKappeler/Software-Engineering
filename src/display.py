import colors
import colorsys
import pygame
import picamera
import math
import time
from gopigo import *
import sys
from collections import Counter
distance_to_stop = 20
import io
from radar import *

'''
camera = picamera.PiCamera()

camera.resolution = (320, 180)
    
camera.crop = (0.0, 0.0, 1.0, 1.0)

screen = pygame.display.set_mode((0,0))

'''
def hsv2rgb(h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
        
def hsv3rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def draw(radarDisplay, targets, angle, distance, fontRenderer):
     # draw initial screen
    radarDisplay.fill(colors.black)
    
    pygame.draw.circle(radarDisplay, colors.green, (630,700), 600, 3)

    pygame.draw.circle(radarDisplay, colors.green, (630,700), 500, 3)

    pygame.draw.circle(radarDisplay, colors.green, (630,700), 400, 3)

    pygame.draw.circle(radarDisplay, colors.green, (630,700), 300, 3)

    pygame.draw.circle(radarDisplay, colors.green, (630,700), 200, 3)

    pygame.draw.circle(radarDisplay, colors.green, (630,700), 100, 3)

    radarDisplay.fill(colors.black, [0, 785, 1400, 20])
    
    


    # 45 degree line
    pygame.draw.line(radarDisplay, colors.green, (630, 750),(205, 285), 3)

    # 90 degree line
    pygame.draw.line(radarDisplay, colors.green, (630, 750), (630, 115), 3)

    # 135 degree line
    pygame.draw.line(radarDisplay, colors.green, (630, 750), (1090, 285), 3)

    # draw stastics board
    pygame.draw.rect(radarDisplay, colors.blue, [30, 30, 250, 160], 2)

    # write the 0 degree
    text = fontRenderer.render("0", 1, colors.green)
    radarDisplay.blit(text,(10,680))

    #write the 45 degree
    text = fontRenderer.render("45", 1, colors.green)
    radarDisplay.blit(text,(175,270))

    # write the 90 degree
    text = fontRenderer.render("90", 1, colors.green)
    radarDisplay.blit(text,(640,80))

    # write the 135 degree
    text = fontRenderer.render("135", 1, colors.green)
    radarDisplay.blit(text,(1100,285))

    # write the 180 degree
    text = fontRenderer.render("180", 1, colors.green)
    radarDisplay.blit(text,(1230,680))
    
 

    # draw the moving line
    a = math.sin(math.radians(angle)) * 700.0
    b = math.cos(math.radians(angle)) * 700.0
    pygame.draw.line(radarDisplay, colors.green, (630, 700), (700 - int(b), 630 - int(a)), 3)

    # write the current angle
    #text = fontRenderer.render("Angle : " + str(angle), 1, colors.white)
    if angle > 166:
        text = fontRenderer.render("Angle : 90 " , 1, colors.white)
    else:
        text = fontRenderer.render("Angle : " + str(angle), 1, colors.white)
    radarDisplay.blit(text,(40,40))
    
    text = fontRenderer.render("Forward : " + str('Up Arrow'), 1, colors.white)
    radarDisplay.blit(text, (40,60))
    

    text = fontRenderer.render("Backward : " + str('Down Arrow'), 1, colors.white)    
    radarDisplay.blit(text, (40,80))
    
    
    text = fontRenderer.render("Left : " + str('Left Arrow'), 1, colors.white)
    radarDisplay.blit(text, (40,100))
    
    text = fontRenderer.render("Right : " + str('Right Arrow'), 1, colors.white)     
    radarDisplay.blit(text, (40,120))
    
    text = fontRenderer.render("Radar Sweep : " + str('0'), 1, colors.white)
    radarDisplay.blit(text, (40,140))
    
    
    text = fontRenderer.render("Exit : " + str('1'), 1, colors.white)
    radarDisplay.blit(text, (40,160))

    # draw targets
    for angle in targets.keys():
        # calculate the coordinates and the remoteness of the target
        c = math.sin(math.radians(targets[angle].angle)) * 800.0
        d = math.cos(math.radians(targets[angle].angle)) * 800.0
        # change the scale if the range is changed
        e = math.sin(math.radians(targets[angle].angle)) * (700 / 50) * targets[angle].distance
        f = math.cos(math.radians(targets[angle].angle)) * (700 / 50) * targets[angle].distance
        

#        if targets[angle].distance < 15:
#            color = colors.red
#        elif 35 >= targets[angle].distance >= 15:
#            color = colors.orange
#        elif targets[angle].distance > 35:
#            color = colors.green
        if 0 < targets[angle].distance < 30 :
            color = hsv3rgb((((abs(targets[angle].distance) ** 1.1) / 360)), 1, 1)
        if targets[angle].distance <= 0 or targets[angle].distance >= 30:
            color = colors.green

        # draw the line indicating the target
        pygame.draw.circle(radarDisplay, color, (700 - int(f), 780 - int(e)), 10)
        print color
        
        #pygame.draw.line(radarDisplay, targets[angle].color, (700 - int(f), 780 - int(e)), (700 - int(d), 780 - int(c)), 3)

        # Scaled Display
        #camera
        
        


    # update the screen
    pygame.display.update()
