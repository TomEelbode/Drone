import pygame
import time
import socket
import pickle
import sys

# Define adress of rpi
TCP_IP = '192.168.0.100'
TCP_PORT = 5005

class JoyStickState:
    def __init__(self):
        self.button = [0]*9 # value can be 0 or 1 (1 for pressed)
        self.axis = [0.0]*4 # value is between -1 and 1

    def getState(self):
        result = self.button + self.axis
        return result

    def resetState(self):
        self.button = [0]*9 # value can be 0 or 1 (1 for pressed)
        self.axis = [0.0]*4 # value is between -1 and 1

    def setButton(self, button, value):
        self.button[button] = value

    def setAxis(self, axis, value):
        self.axis[axis] = 2 + value

    def getShutdown(self):
        if (self.button[7] == 1):
            return True
        else:
            return False

pygame.init()
 
#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get count of joysticks
joystick_count = pygame.joystick.get_count()

if (joystick_count == 0):
    print("No joystick was recognised.")
elif (joystick_count > 1):
    print("There's more than one joystick connected.")
else:
    # intialize the connected joystick
    joystick = pygame.joystick.Joystick(0) # joystick number 0
    joystick.init()
    name = joystick.get_name()
    print(name + " is connected.")
    
# Initialize joystickstate
joystickState = JoyStickState()

# Connect to rpi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print('Connected to server...')

# -------- Main Program Loop -----------
while done==False:
    # Get the event
    pygame.event.get()        
    
    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()   
    for i in range( axes ):
        axis = joystick.get_axis( i )
        joystickState.setAxis(i,axis)
        
    buttons = joystick.get_numbuttons()

    for i in range( buttons ):
        button = joystick.get_button( i )
        joystickState.setButton(i,button)
        
    # Hat switch. All or nothing for direction, not like joysticks.
    # Value comes back in an array.
    hats = joystick.get_numhats()

#    for i in range( hats ):
#        hat = joystick.get_hat( i )
#        joystickState.setHat(hat[0], hat[1])

    # Limit to 20 frames per second
    clock.tick(20)

    message = joystickState.getState()
    print(message)
    print(sys.getsizeof(message))
    print(len(pickle.dumps(message)))
    s.send('#' + pickle.dumps(message) + '%')

    if (joystickState.getShutdown()):
        done = True
	s.send('X')

s.close()
print("Connection closed.")    
pygame.quit ()
