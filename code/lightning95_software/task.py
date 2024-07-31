from lightning import *

def task_searching(frame):
    global frames_without_line
    global sure
    
    # Measuring distance from ultrasonic sensors
    front_distance = utils_measure_distance(TRIG_PIN_1, ECHO_PIN_1)
    back_distance = utils_measure_distance(TRIG_PIN_2, ECHO_PIN_2)
    
    if(front_distance == None): front_distance = 255
    if(back_distance == None): back_distance = 255

    # Converting to OpenCV BGR frame
    bgr_frame = cudaAllocMapped(width = frame.width, height = frame.height, format = 'bgr8')
    cudaConvertColor(frame, bgr_frame)
    cudaDeviceSynchronize()
    cv_frame = cudaToNumpy(bgr_frame)

    black_line_frame = utils_black_line(cv_frame)
    c_x, c_y = utils_find_line_center(black_line_frame)

    if(front_distance <= 15):
        platform.robot.backward(0.9)
        time.sleep(0.05)
        platform.robot.stop()
      
    elif(back_distance <= 15):
        platform.robot.forward(0.9)
        time.sleep(0.05)
        platform.robot.stop()
                
    if(c_x != None and c_y != None):        
        platform.system.system_state = SystemState.EN_SYSTEM_LINE_FOLLOWING
        
        lightning_update_db_values()
        
        frames_without_line = 0
        
        sure += 1

    else:
        platform.robot.left(0.9)
        time.sleep(0.1)
        platform.robot.stop()
        time.sleep(0.02)

def task_line_following(frame):
    global frames_without_line
    global sure
    
    # Measuring distance from ultrasonic sensors
    front_distance = utils_measure_distance(TRIG_PIN_1, ECHO_PIN_1)
    back_distance = utils_measure_distance(TRIG_PIN_2, ECHO_PIN_2)
    
    if(front_distance == None): front_distance = 255
    if(back_distance == None): back_distance = 255

    # Converting to OpenCV BGR frame
    bgr_frame = cudaAllocMapped(width = frame.width, height = frame.height, format = 'bgr8')
    cudaConvertColor(frame, bgr_frame)
    cudaDeviceSynchronize()
    cv_frame = cudaToNumpy(bgr_frame)

    black_line_frame = utils_black_line(cv_frame)
    c_x, c_y = utils_find_line_center(black_line_frame)
    
    if(c_x != None and c_y != None):
        if(front_distance <= 99.3 and front_distance >= 96.6 and back_distance <= 24.3 and back_distance >= 22.7 and sure >= 2):
            platform.robot.stop()

            platform.system.system_state = SystemState.EN_SYSTEM_TEMP_STATE
            
            lightning_update_db_values()
           
        if(front_distance <= 82.5 and front_distance >= 80.1 and back_distance <= 40.8 and back_distance >= 39.1 and sure >= 2):
            platform.robot.stop()

            platform.system.system_state = SystemState.EN_SYSTEM_TEMP_STATE
            
            lightning_update_db_values()

        if(front_distance <= 63 and front_distance >= 61.1 and back_distance <= 59.4 and back_distance >= 57.4 and sure >= 2):
            platform.robot.stop()
            
            platform.system.system_state = SystemState.EN_SYSTEM_TEMP_STATE
            
            lightning_update_db_values()
            
        if(front_distance <= 47.5 and front_distance >= 45.7 and back_distance <= 76.5 and back_distance >= 73.5 and sure >= 2):
            platform.robot.stop()
            
            platform.system.system_state = SystemState.EN_SYSTEM_TEMP_STATE
            
            lightning_update_db_values()
            
        if(front_distance <= 30.1 and front_distance >= 28.6 and back_distance <= 93.8 and back_distance >= 89 and sure >= 2):
            platform.robot.stop()
            
            platform.system.system_state = SystemState.EN_SYSTEM_TEMP_STATE
            
            lightning_update_db_values()
        
        else:            
            frames_without_line = 0
            
            height, width, _ = frame.shape
            
            deviation = (c_x - width // 2) / (width // 2)
            
            if deviation < -0.17:
                platform.robot.left(0.8)
                time.sleep(0.06)
                platform.robot.stop()
            
            elif deviation > 0.17:
                platform.robot.right(0.8)
                time.sleep(0.06)
                platform.robot.stop()
            
            else:
                platform.robot.forward(0.9)
            
            if(len(detected_numbers) == 9):
                platform.robot.stop()
                
                platform.system.parking_state = ParkingState.EN_PARKING_PLATE_NOT_FOUND
                
                platform.system.system_state = SystemState.EN_SYSTEM_COMPLETED
                
                lightning_update_db_values()
    else:
        frames_without_line += 1

        if frames_without_line >= 20:
            platform.system.system_state = SystemState.EN_SYSTEM_SEARCHING

        platform.robot.stop()

def task_temp_state(frame):
    start_time = time.time()
    
    while (time.time() - start_time) < 0.49: # TODO: Demodan once tekrar bakilacak. 
        platform.robot.left(1.6)
    
    platform.robot.stop()
        
    platform.system.system_state = SystemState.EN_SYSTEM_NUMBER_DETECTED
    
    lightning_update_db_values()
    
def task_number_detected(frame):
    global flag
    global one_frame
    global frame_count
    global frame_count_plate
    global detected_numbers
    global number_found
    global plate
    
    plate = platform.system.plate

    if(platform.system.plate == 10):
        plate = 1
        
    else:
        plate += 1
        
    numpy_image = cudaToNumpy(frame)
    
    c_x, c_y = frame.width // 2, frame.height // 2
    
    zoom_factor = 1.82
    crop_width = int(frame.width // zoom_factor)
    crop_height = int(frame.height // zoom_factor)
    
    left = max(c_x - crop_width // 2, 0)
    top = max(c_y - crop_height // 2, 0)
    right = min(c_x + crop_width // 2, frame.width)
    bottom = min(c_y + crop_height // 2, frame.height)
    
    cropped_image = numpy_image[top:bottom, left:right]
    
    resized_image = cv2.resize(cropped_image, (frame.width, frame.height), interpolation=cv2.INTER_LINEAR)
    
    if(plate != 5):
        additional_crop = int(frame.width * 0.17)
        final_cropped_image = resized_image[:, additional_crop:-additional_crop]
        resized_image = cv2.resize(final_cropped_image, (frame.width, frame.height), interpolation=cv2.INTER_LINEAR)
    
    cuda_image = cudaFromNumpy(resized_image)
    
    detections = net.Detect(cuda_image, overlay = 'box,labels,conf')
    
    if frame_count_plate >= 1:
        frame_count_plate += 1
        number_found = False
        
        for detection in detections:
            if(plate == 2):
                if detection.ClassID == 1:
                    number_found = False
                    detected_numbers.add(detection.ClassID)
                    
                elif(detection.ClassID != 2):
                    detected_numbers.add(detection.ClassID)
                    
                if(detection.ClassID == 2):
                    one_frame += 1
                    number_found = True
                    
                if(one_frame >= 20):
                    number_found = True
                    
                    platform.system.system_state = SystemState.EN_SYSTEM_RED_LINE
                    
                    lightning_update_db_values()
                    
            elif(plate == 1):
                detected_numbers.add(detection.ClassID)
                
                if(detection.ClassID == 1):
                    number_found = True
                    
                    platform.system.system_state = SystemState.EN_SYSTEM_RED_LINE
                    
                    lightning_update_db_values()
                
                else:
                    frame_count += 1
                    number_found = True
                    
                if frame_count >= 20:
                    number_found = False 
                
            elif(plate == 5):
                detected_numbers.add(detection.ClassID)
                
                height, width, _ = frame.shape
                
                if(width * 0.3 <= detection.Center[0] and detection.Center[0] <= width * 0.7 and detection.ClassID == 5):
                    number_found = True
                    
                    frame_count_plate = 20
                    
                    platform.system.system_state = SystemState.EN_SYSTEM_RED_LINE
                    
                    lightning_update_db_values()
                    
                    break
                    
            elif(detection.ClassID == plate):
                number_found = True
                
                frame_count_plate = 20
                
                platform.system.system_state = SystemState.EN_SYSTEM_RED_LINE
                
                lightning_update_db_values()
                
                break
                
            else:
                detected_numbers.add(detection.ClassID)
                
        if(frame_count_plate == 20):
            frame_count_plate = 0
            
    else:
        frame_count_plate = 1
        
        if(flag == 0 and number_found == False):
            flag = 1
            
            platform.system.system_state = SystemState.EN_SYSTEM_BACKWARD_TURN
        
        elif(flag == 1 and number_found == False):
            flag=0
            
            start_time = time.time()
            
            while (time.time() - start_time) < 0.5:
                platform.robot.left(1.6)
            
            platform.robot.stop()
            
            start_time = time.time()
            
            while (time.time() - start_time) < 0.25:
                platform.robot.forward(0.95)
            
            platform.robot.stop()
            
            platform.system.system_state = SystemState.EN_SYSTEM_LINE_FOLLOWING
            
            lightning_update_db_values()

def task_backward_turn(frame):
    start_time = time.time()
    
    while (time.time() - start_time) <0.895:
        platform.robot.left(1.6)
        
    platform.robot.stop()
    
    frame_count = 0
    one_frame = 0
    
    platform.system.system_state = SystemState.EN_SYSTEM_NUMBER_DETECTED
    
    lightning_update_db_values()

def task_red_line(frame):
    # Measuring distance from ultrasonic sensors
    front_distance = utils_measure_distance(TRIG_PIN_1, ECHO_PIN_1)
    back_distance = utils_measure_distance(TRIG_PIN_2, ECHO_PIN_2)
    
    if(front_distance == None): front_distance = 255
    if(back_distance == None): back_distance = 255

    # Converting to OpenCV BGR frame
    bgr_frame = cudaAllocMapped(width = frame.width, height = frame.height, format = 'bgr8')
    cudaConvertColor(frame, bgr_frame)
    cudaDeviceSynchronize()
    cv_frame = cudaToNumpy(bgr_frame)

    x_1, y_1, x_2, y_2 = utils_red_line(cv_frame)
    
    image_width = frame.width

    red_left = utils_read_color(S2_LEFT, S3_LEFT, OUT_LEFT)
    red_right = utils_read_color(S2_RIGHT, S3_RIGHT, OUT_RIGHT)
    kirmizi_algilandi_sol = red_left < 200
    kirmizi_algilandi_sag = red_right < 200
        
    if kirmizi_algilandi_sol and not previous_red_left:
        red_count += 1
        platform.system.crossed_red_line = red_count
        previous_red_left = True
        
        lightning_update_db_values()

        if(not kirmizi_algilandi_sol):
            previous_red_left = False
            
        if(kirmizi_algilandi_sag and not previous_red_right):
            red_count += 1
            platform.system.crossed_red_line = red_count
            previous_red_right = True
            
            lightning_update_db_values()

        if(not kirmizi_algilandi_sag):
            previous_red_right = False

    if(front_distance > 6):
        if(x_2 < image_width * 0.43):
            platform.robot.left()
            time.sleep(0.1)
            platform.robot.stop()

        elif(x_2 > image_width * 0.57):
            platform.robot.right(0.8)
            time.sleep(0.1)
            platform.robot.stop()

        else:
            platform.robot.forward(0.8)
            time.sleep(0.2)
            platform.robot.stop()    
    
    else:
        platform.robot.stop()
        
        platform.system.parking_state = ParkingState.EN_PARKING_COMPLETED
        
        platform.system.system_state = SystemState.EN_SYSTEM_COMPLETED
        
        lightning_update_db_values()

def task_completed():
    platform.system.parking_state = ParkingState.EN_PARKING_COMPLETED
    
    platform.system.system_state = SystemState.EN_SYSTEM_COMPLETED
    
    lightning_update_db_values()
    
def task_reset():
    global frames_without_line
    global flag
    global one_frame
    global frame_count
    global frame_count_plate
    global sure
    global start_time
    global detected_numbers
    global plate
    global number_found
    global red_count
    global previous_red_left
    global previous_red_right
    
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
    
    platform.system.crossed_red_line = 0
    platform.system.parking_state = ParkingState.EN_PARKING_NOT_COMPLETED
    platform.system.plate = 0
    platform.system.system_in_progress = SystemProgress.EN_SYSTEM_NOT_IN_PROGRESS
    platform.system.system_state = SystemState.EN_SYSTEM_SEARCHING

    lightning_update_db_values()
    