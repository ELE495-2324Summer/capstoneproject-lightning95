from jetbot import Robot
from utils import *
from database import *

import time
import schedule

databaseURL = 'https://lightning95-selfparking-default-rtdb.europe-west1.firebasedatabase.app/'
credPath = './service-account-key/sak.json'

class Lightning:
    def __init__(self):
        self.robot = Robot()
        self.system = self.System()
        self.database = Database(credPath = credPath, databaseURL = databaseURL)

    class System():
        def __init__(self):
            self.crossed_red_line = 0
            self.parking_state = ParkingState.EN_PARKING_NOT_COMPLETED
            self.plate = 0
            self.system_in_progress = SystemProgress.EN_SYSTEM_NOT_IN_PROGRESS
            self.system_state = SystemState.EN_SYSTEM_SEARCHING

def lightning_read_data():
    sub_root = platform.database.read_database('platform')
    
    platform.system.plate = sub_root['plate']

    if(sub_root['system-in-progress'] == SystemProgress.EN_SYSTEM_NOT_IN_PROGRESS.name): 
        platform.system.system_in_progress = SystemProgress.EN_SYSTEM_NOT_IN_PROGRESS
        
    else: 
        platform.system.system_in_progress = SystemProgress.EN_SYSTEM_IN_PROGRESS
        
    if(sub_root['system-state'] == SystemState.EN_SYSTEM_SEARCHING.name): 
        platform.system.system_state = SystemState.EN_SYSTEM_SEARCHING
        
    if(sub_root['system-state'] == SystemState.EN_SYSTEM_RESET.name):
        platform.system.system_state = SystemState.EN_SYSTEM_RESET
        
def lightning_write_data():
    platform.database.update('platform')
    
def lightning_update_db_values():
    platform.database.values.crossed_red_line = platform.system.crossed_red_line
    platform.database.values.parking_state = platform.system.parking_state.name
    platform.database.values.system_state = platform.system.system_state.name

platform = Lightning()

schedule.every(5).seconds.do(lightning_read_data)
schedule.every(5).seconds.do(lightning_write_data)

frames_without_line = 0
flag = 0
one_frame = 0
frame_count = 0
frame_count_plate = 1
sure = 0
start_time = 0
detected_numbers = set()
plate = 0
number_found = False
red_count = 0
previous_red_left = False
previous_red_right = False
