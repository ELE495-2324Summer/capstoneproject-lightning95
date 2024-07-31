from system import *

def main():
    while 1:
        if(platform.system.system_in_progress == SystemProgress.EN_SYSTEM_IN_PROGRESS):
            schedule.run_pending()
            
            frame = videoSource.Capture()
            
            if frame is None:
                continue
                            
            system_execute(frame)
            
        if(platform.system.system_in_progress == SystemProgress.EN_SYSTEM_NOT_IN_PROGRESS):
            schedule.run_pending()
            
            platform.robot.stop()
            
if __name__ == '__main__':
    
    main()
