## 2nd_assignment_main

## 1. 센서 인식 상황별로 Step-Turn을 수행하였습니다.
    verylittle_turn = 5
    little_turn = 10
    midium_turn = 20
    heavy_turn = 35

    1) 30회 반복 주행을 통해 상황에 적합한 조향각을 새로 산출하였습니다.
    2) Step-Turn각도를 midium_turn 조건에서 코스의 곡률에 적합한 20도로 변경하였습니다.

## 2. while문을 통해 반복해서 라인을 감지하며 전진하고, 정지조건에서 break문을 통해 빠져나옵니다.
    while True:
        # speed의 속도로 전진하며 라인감지 시작
        speed = 100
        self.car.accelerator.go_forward(speed)
        detector = self.car.line_detector.read_digital()

        # 라인이 정중앙에 있을 때 직진
        if detector == [0, 0, 1, 0, 0]:
            self.car.steering.center_alignment()

        # 라인이 사라졌을 때 정지
        elif detector == [0, 0, 0, 0, 0] or detector == [1, 1, 1, 1, 1]:
            self.car.steering.center_alignment()
            self.car.accelerator.stop()
            break
    
    1) 라인이 정중앙 센서에만 감지되면 직진합니다.
    2) 라인이 모두 사라지거나 모든 센서에서 라인을 감지하면 종료조건으로 판정하고 정지합니다.

## 3. 판단횟수과 조향명령 횟수를 줄이기 위해 좌/우회전 판단을 중앙센서로부터 하나씩 읽어가며 판단했습니다.
    # 좌회전을 위한 코드
        elif detector[3] == 0 and detector[4] == 0:
            if detector[2] == 1 and detector[1] == 1: angle = verylittle_turn
            elif detector[2] == 0:
                if detector[1] == 1:
                    if detector[0] == 0: angle = little_turn
                    elif detector[0] == 1: angle = midium_turn
                elif detector[1] == 0:
                    if detector[0] == 1: angle = heavy_turn
            self.car.steering.turn_left(90 - angle)

    # 우회전을 위한 코드
        elif detector[0] == 0 and detector[1] == 0:
            if detector[2] == 1 and detector[3] == 1: angle = verylittle_turn
            elif detector[2] == 0:
                if detector[3] == 1:
                    if detector[4] == 0: angle = little_turn
                    elif detector[4] == 1: angle = midium_turn
                elif detector[3] == 0:
                    if detector[4] == 1: angle = heavy_turn
            self.car.steering.turn_right(90 + angle)

    1) 우측 또는 좌측 센서 두개에 라인이 감지되지 않는다면 반대쪽으로 훑어가며 라인이 감지되는 상황을 판단하여 Step-Turn합니다.

## 4. 값이 튀거나 동시에 3개 이상의 센서에서 감지될 경우 현재 주행경로를 유지합니다.
    else: continue
    
    1) 판단가능한 상황이 될 때까지 현재 조향각과 속도로 주행합니다.
