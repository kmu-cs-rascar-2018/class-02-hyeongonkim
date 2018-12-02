#########################################################################
# Date: 2018/11/26
# file name: ad_assignment_main_frontcar.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


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
        self.car.steering.center_alignment()
        time.sleep(1)
        self.car.accelerator.ready()
        self.car.accelerator.stop()
        speed = 80
        out = False

        # 최대조향각 40도로 설정
        self.car.steering.turning_max = 35

        # do-while의 구조를 취하기 위해 while True 사용
        while True:
            # 라인감지 시작
            detector = self.car.line_detector.read_digital()
            ultrasonic = self.car.distance_detector.get_distance()

            # 초음파센서가 앞차량을 감지
            if 10 < ultrasonic < 35:
                # 앞차량을 감지했다고 최종 판단하면 정지
                self.car.accelerator.stop()
                while True:
                    ultrasonic = self.car.distance_detector.get_distance()
                    if ultrasonic > 35:
                        break

            # 라인이 정중앙에 있을 때 직진
            if detector == [0, 0, 1, 0, 0]:
                self.car.steering.center_alignment()
                self.car.accelerator.go_forward(speed)
                out = False

            # 추월구간시작(1번, 4번 센서에 라인이 동시감지)이 감지되었을 때 양보
            elif detector[0] == 1 and detector[4] == 1:
                self.car.steering.center_alignment()
                time.sleep(1.5)
                self.car.accelerator.stop()
                while True:
                    ultrasonic = self.car.distance_detector.get_distance()
                    if 10 < ultrasonic < 50:
                        break

            # 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
            elif detector == [0, 0, 0, 0, 0] and out == True:
                self.car.accelerator.stop()
                while True:
                    self.car.steering.turn_left(55)
                    time.sleep(0.1)
                    self.car.accelerator.go_backward(60)
                    detector = self.car.line_detector.read_digital()
                    if detector[4] == 1 or detector[3] == 1:
                        self.car.accelerator.stop()
                        self.car.steering.turn_right(130)
                        time.sleep(0.1)
                        self.car.accelerator.go_forward(50)
                        out == False
                        break

            # 좌회전을 위한 코드
            elif detector == [0, 1, 1, 0, 0]:
                self.car.steering.turn_left(75)
                out = False
            elif detector == [0, 1, 0, 0, 0]:
                self.car.steering.turn_left(70)
                out = False
            elif detector == [1, 1, 0, 0, 0]:
                self.car.steering.turn_left(60)
                out = True
            elif detector == [1, 0, 0, 0, 0]:
                self.car.steering.turn_left(55)
                out = True

            # 우회전을 위한 코드
            elif detector == [0, 0, 1, 1, 0]:
                self.car.steering.turn_right(105)
                out = False
            elif detector == [0, 0, 0, 1, 0]:
                self.car.steering.turn_right(110)
                out = False
            elif detector == [0, 0, 0, 1, 1]:
                self.car.steering.turn_right(120)
                out = True
            elif detector == [0, 0, 0, 0, 1]:
                self.car.steering.turn_right(125)
                out = True
            
            # 값이 튀면 현재 경로 유지
            else: continue

        pass


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()