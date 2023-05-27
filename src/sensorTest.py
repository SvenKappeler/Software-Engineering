# Sensor on A1 Port

from gopigo import *
import time

distance_to_stop = 20  # Distance from obstacle where the GoPiGo should stop
print ("Press ENTER to start")
raw_input()  # Wait for input to start
fwd()  # Start moving

while True:
    dist = us_dist(15)  # Find the distance of the object in front
    print ("Dist:", dist, 'cm')
    if dist < distance_to_stop:  # If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
        print ("Stopping")
        stop()  # Stop the GoPiGo
        break
    time.sleep(.1)

