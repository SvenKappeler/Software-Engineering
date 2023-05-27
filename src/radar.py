import pygame
import picamera
import io
import math
import time
import colors
import sys
from target import *
from display import*
from gopigo import *
from collections import Counter


# initialize the program
x = pygame.init()

pygame.font.init()

defaultFont = pygame.font.get_default_font()

fontRenderer = pygame.font.Font(defaultFont, 20)

radarDisplay = pygame.display.set_mode((1400, 800))
    
pygame.display.set_caption('Radar Screen')


def us_map():
    delay=.02
    debug =0                    #True to print all raw values
    num_of_readings=45          #Number of readings to take 
    incr=180/num_of_readings    #increment of ang in servo
    ang_l=[0]*(num_of_readings+1)   #list to hold the ang's of readings
    dist_l=[0]*(num_of_readings+1)  #list to hold the distance at each ang
    x=[0]*(num_of_readings+1)   #list to hold the x coordinate of each point
    y=[0]*(num_of_readings+1)   #list to hold the y coordinate of each point
    buf=[0]*40
    ang=15
    lim=1000     #maximum limit of distance measurement (any value over this which be initialized to the limit value)
    index=0
    sample=2
    targets = {}
    enable_servo()
    servo_pos=160
    running = 1
    turnTime = .305
    driveTime = .305
    j = 0

    while True:
        for i in range(sample): 
            dist=us_dist(15)
            if dist<lim and dist>=0:
                buf[i]=dist
            else:
                buf[i]=lim
                
        if dist < 2:
            stop()
            running = 0
            
            
        max=Counter(buf).most_common()  
        rm=-1
        for i in range (len(max)):
            if max[i][0] <> lim and max[i][0] <> 0:
                rm=max[i][0]
            break
        if rm==-1:
            rm=lim
        
        if debug==1:
            print index,ang,rm
        
        if running == 1:
            servo(ang)  
            time.sleep(delay)
            ang+=incr
            

            if dist != -1 and dist <= 50:
                targets[ang] = Target(ang, dist)
            
            draw(radarDisplay, targets, ang, dist, fontRenderer)
        
            if ang>165:
                ang =25
                servo(90)
                running = 0

            
        for ev in pygame.event.get():      
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RIGHT:
                        right()
                        time.sleep(turnTime)
                        for angle in targets.keys():
                            if targets[angle].angle >= 330:
                                targets[angle].angle = targets[angle].angle - 330
                                print targets[angle].angle
                            elif targets[angle].angle < 330:
                                targets[angle].angle = targets[angle].angle + 30
                                print targets[angle].angle
                        
                    if ev.key == pygame.K_LEFT:
                        left()
                        time.sleep(turnTime)
                        
                                
                        for angle in targets.keys():
                            if targets[angle].angle >= 30:
                                targets[angle].angle = targets[angle].angle - 30
                                print targets[angle].angle
                            elif targets[angle].angle < 30:
                                targets[angle].angle = targets[angle].angle + 330
                                print targets[angle].angle
                    if ev.key == pygame.K_UP:
                        fwd()
                        time.sleep(driveTime)
                        for angle in targets.keys():
                                targets[angle].distance = targets[angle].distance - 10
                        
                    if ev.key == pygame.K_DOWN:
                        bwd()
                        time.sleep(driveTime)
                        for angle in targets.keys():
                                targets[angle].distance = targets[angle].distance + 10

                        
                    if ev.key == pygame.K_1:
                        exit()
                    if ev.key == pygame.K_0:
                        running = 1
                        
                    if ev.key == pygame.K_2:
                        for angle in targets.keys():
                            targets[angle].distance = None                            
                        
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_LEFT or ev.key == pygame.K_RIGHT or ev.key == pygame.K_UP or ev.key == pygame.K_DOWN:
                        stop()
                       
        
while True:
    enable_com_timeout(2000)
    enc_tgt(1,1,18) #Set encoder targetting. Stop after 4 rotations of both the wheels
    time.sleep(.2)
    while True:
        enc=read_enc_status()
        ts=read_timeout_status()
        time.sleep(.05)
        if enc == 0:    #Stop when target is reached
            break
        if  ts==0:
            break
    if us_map() <20:    #If any obstacle is closer than 20 cm, stop
        break
    
    disable_servo()
        # detect if close is pressed to stop the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise KeyboardInterrupt
            
disable_servo()
pygame.quit()
sys.exit()
