from lightning import *
from task import *

def system_execute(frame):
    print(platform.system.system_state)
    
    if(platform.system.system_state == SystemState.EN_SYSTEM_SEARCHING):
        
        task_searching(frame)

    elif(platform.system.system_state == SystemState.EN_SYSTEM_LINE_FOLLOWING):

        task_line_following(frame)
    
    elif(platform.system.system_state == SystemState.EN_SYSTEM_TEMP_STATE):
        
        task_temp_state(frame)

    elif(platform.system.system_state == SystemState.EN_SYSTEM_NUMBER_DETECTED):
        
        task_number_detected(frame)

    elif(platform.system.system_state == SystemState.EN_SYSTEM_BACKWARD_TURN):
        
        task_backward_turn(frame)
        
    elif(platform.system.system_state == SystemState.EN_SYSTEM_RED_LINE):
        
        task_red_line(frame)

    elif(platform.system.system_state == SystemState.EN_SYSTEM_COMPLETED):
        
        task_completed()
        
    elif(platform.system.system_state == SystemState.EN_SYSTEM_RESET):
        
        task_reset()
