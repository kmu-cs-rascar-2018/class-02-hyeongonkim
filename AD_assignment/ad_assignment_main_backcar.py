#########################################################################
# Date: 2018/11/26
# file name: 3rd_assignment_main_backcar.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time
import RPi.GPIO as GPIO

class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform Second Assignment
    # =======================================================================
    def car_startup(self):
        # 출발 전 차량세팅
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(31, GPIO.OUT)
        self.car.steering.center_alignment()
        time.sleep(1)
        self.car.accelerator.ready()
        self.car.accelerator.stop()
        self.car.steering.turning_max = 40
        speed = 50
        target_distance = 30

        # do-while의 구조를 취하기 위해 while True 사용
        while True:
            # 라인감지 시작
            detector = self.car.line_detector.read_digital()
            ultrasonic = self.car.distance_detector.get_distance()
            rgb = self.car.color_getter.get_raw_data()
            GPIO.output(31, False)

            # 초음파센서가 앞차량을 감지
            if 10 < ultrasonic < 40:
                # 앞차량을 감지했다고 최종 판단하면 속도 조절 시작
                if ultrasonic < target_distance:
                    speed -= 5
                elif ultrasonic > target_distance:
                    speed += 5
                elif ultrasonic < 20:
                    self.car.accelerator.stop()
                    while True:
                        ultrasonic = self.car.distance_detector.get_distance()
                        if ultrasonic > 30:
                            break

            # 거리가 35보다 멀어지면 정상속도로 가속
            if ultrasonic > 40:
                speed = 60

            # 속도가 30 미만으로 떨어지면 모터 작동에 문제가 생기므로 최소값 고정
            if speed < 30:
                speed = 30
            if speed > 60:
                speed = 60

            # RGB Red감지시 3초 정지
            if rgb[0] > 250 and rgb[1] < 200 and rgb[2] < 200:
                self.car.accelerator.stop()
                self.car.steering.center_alignment()
                time.sleep(3)
                self.car.accelerator.go_forward(50)
                time.sleep(0.3)

            # 라인이 정중앙에 있을 때 직진
            if detector == [0, 0, 1, 0, 0]:
                self.car.steering.center_alignment()

            # 추월구간시작(0번, 4번 센서에 라인이 동시감지)이 감지되었을 때 추월
            elif detector[0] == 1 and detector[3] == 1 and detector[4] == 1:
                if ultrasonic < 30:
                    self.car.steering.turn_right(130)
                    self.car.accelerator.go_forward(50)
                    GPIO.output(31, True)
                    self.car.steering.turn_right(130)
                    time.sleep(0.9)
                    self.car.steering.turn_left(50)
                    while True:
                        detector = self.car.line_detector.read_digital()
                        if detector[3] == 1:
                            GPIO.output(31, False)
                            self.car.steering.turn_right(130)
                            time.sleep(0.4)
                            break
                else:
                    continue

            # 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
            elif detector == [0, 0, 0, 0, 0]:
                self.car.accelerator.stop()
                while True:
                    self.car.steering.turn_left(55)
                    time.sleep(0.1)
                    self.car.accelerator.go_backward(50)
                    detector = self.car.line_detector.read_digital()
                    if detector[4] == 1 or detector[3] == 1:
                        self.car.accelerator.stop()
                        self.car.steering.turn_right(125)
                        time.sleep(0.1)
                        self.car.accelerator.go_forward(50)
                        break

            # T자 후진주차 코드
            elif detector[0] == 0 and detector[2] == 1 and detector[4] == 1:
                while True:
                    detector = self.car.line_detector.read_digital()
                    if detector[2] == 1 and detector[4] == 1:
                        continue
                    elif detector[0] == 0 and detector[4] == 0 and detector[2] == 1:
                        # 최적의 주차 속도/조향 산출
                        self.car.accelerator.go_forward(40)
                        time.sleep(0.3)
                        self.car.steering.turn_left(60)
                        time.sleep(0.6)
                        self.car.accelerator.stop()
                        self.car.steering.turn_right(120)
                        self.car.accelerator.go_backward(40)
                        time.sleep(1.8)
                        self.car.steering.center_alignment()
                        time.sleep(0.25)
                        self.car.accelerator.stop()
                        time.sleep(3)
                        self.car.steering.turn_right(125)
                        time.sleep(0.2)
                        self.car.accelerator.go_forward(40)
                        time.sleep(2.5)
                        
                    else: break

            # 좌회전을 위한 코드
            elif detector == [0, 1, 1, 0, 0]:
                self.car.steering.turn_left(75)
            elif detector == [0, 1, 0, 0, 0]:
                self.car.steering.turn_left(70)
            elif detector == [1, 1, 0, 0, 0]:
                self.car.steering.turn_left(60)
            elif detector == [1, 0, 0, 0, 0]:
                self.car.steering.turn_left(55)

            # 우회전을 위한 코드
            elif detector == [0, 0, 1, 1, 0]:
                self.car.steering.turn_right(105)
            elif detector == [0, 0, 0, 1, 0]:
                self.car.steering.turn_right(110)
            elif detector == [0, 0, 0, 1, 1]:
                self.car.steering.turn_right(120)
            elif detector == [0, 0, 0, 0, 1]:
                self.car.steering.turn_right(125)
            
            # 값이 튀면 현재 경로 유지
            else: continue
            
            # 계산된 속도를 전진으로 입력
            self.car.accelerator.go_forward(speed)

        pass


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()