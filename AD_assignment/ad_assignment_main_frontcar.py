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
        overtake = False
        speed = 50
        determine_left = True

        # 최대조향각 40도로 설정
        self.car.steering.turning_max = 40

        # do-while의 구조를 취하기 위해 while True 사용
        while True:
            # 라인감지 시작
            detector = self.car.line_detector.read_digital()
            ultrasonic = self.car.distance_detector.get_distance()

            # Step-Turn 각 설정
            verylittle_turn = 10
            little_turn = 20
            medium_turn = 30
            heavy_turn = 40

            # 초음파센서가 앞차량을 감지하고 튀는 값을 필터링
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

            # 추월구간시작(0번, 4번 센서에 라인이 동시감지)이 감지되었을 때 감속
            elif detector[0] == 1 and detector[4] == 1 and overtake == False:
                speed -= 30
                overtake = True
                while detector[0] == 1 and detector[4] == 1:
                    detector = self.car.line_detector.read_digital()

            # 추월구간종료(0번, 4번 센서에 라인이 동시감지)가 감지되었을 때 가속
            elif detector[0] == 1 and detector[4] == 1 and overtake == True:
                speed += 30
                overtake = False
                while detector[0] == 1 and detector[4] == 1:
                    detector = self.car.line_detector.read_digital()

            # 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
            elif detector == [0, 0, 0, 0, 0]:
                self.car.accelerator.stop()
                if determine_left == True:
                    while True:
                        self.car.steering.turn_right(130)
                        time.sleep(0.1)
                        self.car.accelerator.go_backward(50)
                        detector = self.car.line_detector.read_digital()
                        if detector[0] == 1 or detector[1] == 1:
                            self.car.accelerator.stop()
                            self.car.steering.turn_left(50)
                            time.sleep(0.1)
                            self.car.accelerator.go_forward(speed)
                            break
                elif determine_left == False:
                    while True:
                        self.car.steering.turn_left(50)
                        time.sleep(0.1)
                        self.car.accelerator.go_backward(50)
                        detector = self.car.line_detector.read_digital()
                        if detector[4] == 1 or detector[3] == 1:
                            self.car.accelerator.stop()
                            self.car.steering.turn_right(130)
                            time.sleep(0.1)
                            self.car.accelerator.go_forward(speed)
                            break

            # 좌회전을 위한 코드
            elif detector[3] == 0 and detector[4] == 0:
                if detector[2] == 1 and detector[1] == 1:
                    angle = verylittle_turn
                elif detector[2] == 0:
                    if detector[1] == 1:
                        if detector[0] == 0:
                            angle = little_turn
                        elif detector[0] == 1:
                            angle = medium_turn
                    elif detector[1] == 0:
                        if detector[0] == 1:
                            angle = heavy_turn
                self.car.accelerator.go_forward(speed)
                determine_left = True
                self.car.steering.turn_left(90 - angle)

            # 우회전을 위한 코드
            elif detector[0] == 0 and detector[1] == 0:
                if detector[2] == 1 and detector[3] == 1:
                    angle = verylittle_turn
                elif detector[2] == 0:
                    if detector[3] == 1:
                        if detector[4] == 0:
                            angle = little_turn
                        elif detector[4] == 1:
                            angle = medium_turn
                    elif detector[3] == 0:
                        if detector[4] == 1:
                            angle = heavy_turn
                self.car.accelerator.go_forward(speed)
                determine_left = False
                self.car.steering.turn_right(90 + angle)
            
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