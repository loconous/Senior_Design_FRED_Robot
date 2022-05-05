#OK!
#Author: Luis A. Gonzalez Villalobos
#Date: 3/28/2022
#Project: MindSparkBots - FRED Logic

##==================================================================================
## Libraries
##==================================================================================
from platform import freedesktop_os_release
from random import randint
from time import sleep
from  pycreate2 import Create2
import firebase_admin
from firebase_admin import credentials, firestore

##==================================================================================
## STATES
##==================================================================================
'''
Create new states in here 
Template:
        class new_state_name(State):
            def Execute(self):
                logic here
Finally, make sure to add new states and their transitions in main down below
'''

# Create a State base class
State = type("State", (object,), {})

# State to turn robot on
class RobotOn(State):
    def Execute(self):
        # Start the Create 2
        #bot.start()
        print("Robot is On!")

# State to turn robot off
class RobotOff(State):
    def Execute(self):
        print("Robot is Off!")

# State to make robot go dock itself
class Wait(State):
    def Execute(self):
        print("Robot is waiting...")

# State of robot when charging
class Camera(State):
    def Execute(self):
        print("Robot has camera On!")

# State of robot when user is in a game
class Gaming(State):
    def Execute(self):
        print("Let's Play!")

# State to make robot do celebration dance
class Dance(State):
    def Execute(self):
        print("Let's Dance!")

##==================================================================================
## TRANSITION
##==================================================================================
'''
Nothing needs to be added in here so far..
If needed, logic may be implemented in the print statement
This will print everytime there is a change in state
'''
class Transition(object):
    # When contructing, we pass it a toState
    # which is going to transition to
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print("Transitioning...")

##==================================================================================
## FINITE STATE MACHINE
##==================================================================================

class FSM(object):
    def __init__(self, char):
        self.char = char
        # Store all states and transitions in dictionaries
        self.states = {}
        self.transitions = {}
        # Initialize current state and current transition to none
        self.currState = None
        self.trans = None
    
    # This will look for whatever state we pass through the dictionary
    # This will set the current state to the pass in state
    def SetState(self, stateName):
        self.currState = self.states[stateName]

    # Functions to set up the transition states
    # Similar to the previous function for state
    def Transition(self, transName):
        self.trans = self.transitions[transName]

    # If there is a transition stored
    # We will execute the transition
    # We then change states and reset transition to none
    # Finally, execute current state
    def Execute(self):
        if(self.trans):
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None
        self.currState.Execute()

##==================================================================================
## CHARACTER CLASS
##==================================================================================

# This will hold all of the robot's attributes
class Char(object):
    def __init__(self):
        # Create an instance of the FSM
        self.FSM = FSM(self)
        # Store this property
        self.RobotOn = True
        self.RobotOff = False
        self.RobotWait = False
        self.RobotDocked = False 
        self.RobotCharging = False
        self.RobotCamera = False
        self.RobotGame = False
        self.RobotDance = False

##==================================================================================
## MAIN
##==================================================================================

if __name__== "__main__":
    # Setup to Communicate with Firestore Database
    cred = credentials.Certificate("robotServiceAccountKey.json")
    firebase_admin.initialize_app(cred)

    # Mark the beggining of the code and verify authentication with Firebase
    print("Database Initialized and Access Granted! Press CTRL+C to exit")
 
    # Create a Create2.
    #port = "/dev/ttyUSB0"  # locations for out serial
    #bot = Create2(port)

    # Create an instance of the character
    FRED0 = Char()
 
    # Create states
    FRED0.FSM.states["On"] = RobotOn()
    FRED0.FSM.states["Off"] = RobotOff()
    FRED0.FSM.states["Wait"] = Wait()
    FRED0.FSM.states["Camera"] = Camera()  
    FRED0.FSM.states["Gaming"] = Gaming()
    FRED0.FSM.states["Dance"] = Dance()  

    # Create transitions
    FRED0.FSM.transitions["toOn"] = Transition("On")
    FRED0.FSM.transitions["toOff"] = Transition("Off")
    FRED0.FSM.transitions["toWait"] = Transition("Wait")
    FRED0.FSM.transitions["toCamera"] = Transition("Camera")
    FRED0.FSM.transitions["toGaming"] = Transition("Gaming")
    FRED0.FSM.transitions["toDance"] = Transition("Dance")

    FRED0.FSM.SetState("On")

    for i in range(20):
        sleep(1)
        if(FRED0.RobotOn):
            FRED0.FSM.Transition("toOff")
            FRED0.RobotOn = False
            FRED0.RobotOff = True
        elif(FRED0.RobotOff):
            FRED0.FSM.Transition("toWait")
            FRED0.RobotOff = False
            FRED0.RobotWait = True
        elif(FRED0.RobotWait):
            FRED0.FSM.Transition("toCamera")
            FRED0.RobotWait = False
            FRED0.RobotCamera = True
        elif(FRED0.RobotCamera):
            FRED0.FSM.Transition("toGaming")
            FRED0.RobotCamera = False
            FRED0.RobotGame = True
        elif(FRED0.RobotGame):
            FRED0.FSM.Transition("toDance")
            FRED0.RobotGame = False
            FRED0.RobotDance = True
        elif(FRED0.RobotDance):
            FRED0.FSM.Transition("toOn")
            FRED0.RobotDance = False
            FRED0.RobotOn = True
        else:
            print("Error invalid state, check wtf..")
        FRED0.FSM.Execute()