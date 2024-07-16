from enum import Enum
from jetson_inference import *
from jetson_utils import *

import cv2
import numpy as np
import time
import Jetson.GPIO as GPIO

# Ultrasonic Sensors Pin Definitions
TRIG_PIN_1 = 22
ECHO_PIN_1 = 23
TRIG_PIN_2 = 6
ECHO_PIN_2 = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN_1, GPIO.OUT)
GPIO.setup(ECHO_PIN_1, GPIO.IN)
GPIO.setup(TRIG_PIN_2, GPIO.OUT)
GPIO.setup(ECHO_PIN_2, GPIO.IN)

# Color Detection Sensors Pin Definitions
S0_LEFT = 17  # GPIO17 - Physical Pin 11
S1_LEFT = 27  # GPIO27 - Physical Pin 13
S2_LEFT = 4   # GPIO4 - Physical Pin 7
S3_LEFT = 5   # GPIO5 - Physical Pin 29
OUT_LEFT = 24 # GPIO24 - Physical Pin 18

S0_RIGHT = 19  # GPIO19 - Physical Pin 35
S1_RIGHT = 26  # GPIO26 - Physical Pin 37
S2_RIGHT = 13  # GPIO13 - Physical Pin 33
S3_RIGHT = 21  # GPIO21 - Physical Pin 40
OUT_RIGHT = 20 # GPIO20 - Physical Pin 38

GPIO.setmode(GPIO.BCM)
GPIO.setup(S0_LEFT, GPIO.OUT)
GPIO.setup(S1_LEFT, GPIO.OUT)
GPIO.setup(S2_LEFT, GPIO.OUT)
GPIO.setup(S3_LEFT, GPIO.OUT)
GPIO.setup(OUT_LEFT, GPIO.IN)

GPIO.setup(S0_RIGHT, GPIO.OUT)
GPIO.setup(S1_RIGHT, GPIO.OUT)
GPIO.setup(S2_RIGHT, GPIO.OUT)
GPIO.setup(S3_RIGHT, GPIO.OUT)
GPIO.setup(OUT_RIGHT, GPIO.IN)

GPIO.output(S0_LEFT, GPIO.LOW)
GPIO.output(S1_LEFT, GPIO.HIGH)
GPIO.output(S0_RIGHT, GPIO.LOW)
GPIO.output(S1_RIGHT, GPIO.HIGH)

SystemState = Enum('SystemState', ['EN_SYSTEM_SEARCHING', 'EN_SYSTEM_LINE_FOLLOWING', 'EN_SYSTEM_NUMBER_DETECTED', 'EN_SYSTEM_BACKWARD_TURN', 'EN_SYSTEM_TEMP_STATE', 'EN_SYSTEM_RED_LINE', 'EN_SYSTEM_COMPLETED', 'EN_SYSTEM_RESET'])
SystemProgress = Enum('SystemProgress', ['EN_SYSTEM_NOT_IN_PROGRESS', 'EN_SYSTEM_IN_PROGRESS'])
ParkingState = Enum('ParkingState', ['EN_PARKING_NOT_COMPLETED', 'EN_PARKING_COMPLETED', 'EN_PARKING_PLATE_NOT_FOUND'])

class SystemState(Enum):
    EN_SYSTEM_SEARCHING = 0
    EN_SYSTEM_LINE_FOLLOWING = 1
    EN_SYSTEM_NUMBER_DETECTED = 2
    EN_SYSTEM_BACKWARD_TURN = 3
    EN_SYSTEM_TEMP_STATE = 4
    EN_SYSTEM_RED_LINE = 5
    EN_SYSTEM_COMPLETED = 6
    EN_SYSTEM_RESET = 7

class SystemProgress(Enum):
    EN_SYSTEM_NOT_IN_PROGRESS = 0
    EN_SYSTEM_IN_PROGRESS = 1

class ParkingState(Enum):
    EN_PARKING_NOT_COMPLETED = 0
    EN_PARKING_COMPLETED = 1
    EN_PARKING_PLATE_NOT_FOUND = 2


def utils_red_line(np_image):
    image = cv2.medianBlur(np_image, 1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lower_gray = 60
    upper_gray = 80

    mask = cv2.inRange(gray, lower_gray, upper_gray)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    nearest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    start_points = []
    end_points = []

    for contour in nearest_contours:        
        min_point = min(contour, key=lambda point: point[0][1])[0]
        start_points.append((min_point[0], min_point[1]))

        max_point = max(contour, key=lambda point: point[0][1])[0]
        end_points.append((max_point[0], max_point[1]))

    x_1 = (start_points[0][0] + start_points[1][0])/2
    y_1 = (start_points[0][1] + start_points[1][1])/2

    x_2 = (end_points[0][0] + end_points[1][0])/2
    y_2 = (end_points[0][1] + end_points[1][1])/2

    cv2.line(image, (int(x_1), int(y_1)), (int(x_2), int(y_2)), (255, 0, 0), 5)
        
    return x_1, y_1, x_2, y_2

def utils_black_line(frame):
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 80])

    height, width, _ = frame.shape

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    thresh = cv2.inRange(hsv, lower_black, upper_black)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))

    thresh = thresh[3 * height // 4:height, 0:width]

    return thresh

def utils_find_line_center(thresh):
    M = cv2.moments(thresh)

    if M["m00"] == 0:
        return None, None
    
    center_x = int(M["m10"] / M["m00"])
    center_y = int(M["m01"] / M["m00"])

    return center_x, center_y

def utils_measure_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, False)
    time.sleep(0.01)
    
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    
    GPIO.output(trig_pin, False)
    
    pulse_start = time.time()
    
    timeout = pulse_start + 1
    
    while GPIO.input(echo_pin) == 0 and time.time() < timeout:
        pulse_start = time.time()
    
    if time.time() >= timeout:
        return None
    
    pulse_end = time.time()
    
    timeout = pulse_end + 1
    
    while GPIO.input(echo_pin) == 1 and time.time() < timeout:
        pulse_end = time.time()
    
    if time.time() >= timeout:
        return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    return distance

def utils_read_frequency(sensor_out):
    start_time = time.time()
    pulse_count = 0
    duration = 0.1 
    end_time = start_time + duration

    while time.time() < end_time:
        if(GPIO.input(sensor_out) == GPIO.HIGH):

            pulse_count += 1

            while GPIO.input(sensor_out) == GPIO.HIGH:
                pass
    
    return pulse_count / duration

def utils_read_color(sensor_S2, sensor_S3, sensor_out):
    GPIO.output(sensor_S2, GPIO.LOW)
    GPIO.output(sensor_S3, GPIO.LOW)

    red = read_frequency(sensor_out)
    
    return red

videoSource = videoSource('csi://0', options = {'width': 640, 'height': 480, 'framerate': 30})
videoOutput = videoOutput('rtp://192.168.79.8:1234')

net = detectNet('ssd-mobilenet-v2', model='./network/az_ocr/az_ocr_ssdmobilenetv1_2.onnx', labels='./network/az_ocr/labels.txt', input_blob='input_0', output_cvg='scores', output_bbox='boxes', threshold=0.45)

def utils_video_capture():
    return videoSource.Capture()

def utils_output_render(frame):
    videoOutput.Render(frame)

def utils_cuda_to_numpy(frame):
    return cudaToNumpy(frame)

def utils_cuda_from_numpy(np_frame):
    return cudaFromNumpy(np_frame)
