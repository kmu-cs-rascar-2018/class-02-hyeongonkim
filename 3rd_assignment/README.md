## 3rd_assignment_main

## 1. 상황을 정확히 판단하기 위해 판단에 사용할 변수들을 사전에 생성하였습니다.
    lap_cnt = 0
    obstacle_detect = False
    self.car.steering.turning_max = 40
    stopback_time = 0
    lastultrasonic_time = 0
    start_time = time.time()
    determine_left = True

    1) lap_cnt = 랩수 카운터
    2) obstacle_detect = 장애물을 감지했는지
        - 장애물을 감지하면 True로 변경하고 회피기동 실행
        - 회피 후 다시 메인스트리트 진입시 False로 변경
    3) 최대조향각을 40도로 설정
        - 급격한 코너를 돌아나가기 위해
    4) stopback_time = 차량이 라인을 벗어나 후진하고 정지하는 시간을 기록
        - 수정 조향 과정에서 코너를 출발선으로 감지하지 않도록 필터링하기 위함
    5) lastultrasonic_time = 초음파센서를 특정시간동안 비활성화 하기위해 사용
        - 초음파센서로 인해 라인감지에 딜레이가 생기고 판단 신뢰도가 떨어지는 일을 방지하기 위함
    6) start_time = 총 주행시간을 측정하기 위해 사용
    7) determine_left = 라인을 벗어났을 때 직전 조향이 좌측 조향인지 판단
        - 직전 조향의 반대방향으로 조향 후 후진하기 위함

## 2. do-while의 구조를 취하기 위해 while True의 무한 루프를 사용하였습니다.
    while True:
        # 라인감지 시작
        detector = self.car.line_detector.read_digital()

## 3. 초음파센서를 특정시간동안 비활성화하도록 코드를 작성하였습니다.
    # 초음파센서를 메인스트리트 복귀후 6초간은 비활성화(라인감지 속도 향상을 위해)
    nowtime = time.time()
    ultrasonic_ontime = nowtime - lastultrasonic_time
    ultrasonic = 0
    if ultrasonic_ontime > 6:
        ultrasonic = self.car.distance_detector.get_distance()
    
    1) 후술할 장애물 감지 코드 내부에서 측정한 lastultrasonic_time 시간과 현재시간의 차를 구합니다.
    2) 그 차이가 6초 초과일 경우(회피기동이 끝나고 6초가 경과하면) 초음파센서를 활성화합니다. 6초 이하일 경우 초음파센서를 사용하지 않습니다.

## 4. 상황별 조향을 위해 Step-Turn각을 4단계로 설정하였습니다.
    # Step-Turn 각 설정
    verylittle_turn = 10
    little_turn = 25
    medium_turn = 30
    heavy_turn = 40

    1) 30회 반복 트랙주행을 통해 최적의 각을 산출하였습니다.

## 5. 초음파센서가 10초과 30미만 값을 감지하면 회피조향합니다.
    # 초음파센서가 장애물을 감지하고 튀는 값을 필터링
    if 10 < ultrasonic < 30 and obstacle_detect == False:
        n_ultrasonic = self.car.distance_detector.get_distance()
        while n_ultrasonic == -1 or n_ultrasonic > 30:
            n_ultrasonic = self.car.distance_detector.get_distance()
        distance = (ultrasonic + n_ultrasonic) / 2
        # 장애물을 감지했다고 최종 판단하면 좌측으로 회피 조향
        if distance < 30:
            print("obstacle detected")
            obstacle_detect == True
            self.car.accelerator.go_forward(70)
            self.car.steering.turn_left(50)
            time.sleep(0.6)
            self.car.steering.center_alignment()
            while True:
                self.car.accelerator.go_forward(70)
                detector = self.car.line_detector.read_digital()
                # 가이드라인을 감지하면 우측 조향하여 바로 메인스트리트 복귀
                if detector != [0, 0, 0, 0, 0]:
                    print("guideline detected")
                    self.car.accelerator.go_forward(70)
                    self.car.steering.turn_right(130)
                    time.sleep(0.9)
                    self.car.steering.center_alignment()
                    break
            while True:
                detector = self.car.line_detector.read_digital()
                # 메인스트리트 감지하면 좌측 조향하여 코너 진입 준비
                if detector[1] == 1:
                    print("on main street")
                    lastultrasonic_time = time.time()
                    obstacle_detect = False
                    self.car.steering.turn_left(50)
                    time.sleep(0.4)
                    break

    1) 값이 10초과 30미만으로 감지되면 신뢰도 검증을 위해 2차 측정을 시행합니다.
    2) 두 값의 평균치로 거리를 읽어들이고, 이 값이 30미만이면 장애물 감지로 판단합니다.
    3) 회피를 위해 70의 속도로 주행하며 좌측으로 40도 조향후 0.6초 후 직진조향합니다.
    4) 가이드라인을 감지하면 시간단축을 위해 바로 우측 조향하여 메인스트리트로 복귀합니다.
        - 우측으로 40도 조향하고 0.9초 후 직진조향합니다.
    5) 메인스트리트를 감지하면 좌측 조향하여 일직선 정렬합니다.
        - 좌측으로 40도 조향하고 0.4초 후 while루프를 빠져나옵니다.
        - 메인스트리트에 진입한 순간의 시간을 lastultrasonic_time에 저장하여 초음파센서 비활성화에 사용합니다.

## 6. 기본적인 라인트레이싱은 2차 주행과제를 베이스로 수정하였습니다.
    # 라인이 정중앙에 있을 때 직진
    if detector == [0, 0, 1, 0, 0]:
        self.car.steering.center_alignment()
        self.car.accelerator.go_forward(70)

    # 좌회전을 위한 코드
    elif detector[3] == 0 and detector[4] == 0:
        if detector[2] == 1 and detector[1] == 1:
            angle = verylittle_turn
            speed = 60
        elif detector[2] == 0:
            if detector[1] == 1:
                if detector[0] == 0:
                    angle = little_turn
                    speed = 50
                elif detector[0] == 1:
                    angle = medium_turn
                    speed = 45
            elif detector[1] == 0:
                if detector[0] == 1:
                    angle = heavy_turn
                    speed = 40
        self.car.accelerator.go_forward(speed)
        self.car.steering.turn_left(90 - angle)
        determine_left = True

    # 우회전을 위한 코드
    elif detector[0] == 0 and detector[1] == 0:
        if detector[2] == 1 and detector[3] == 1:
            angle = verylittle_turn
            speed = 60
        elif detector[2] == 0:
            if detector[3] == 1:
                if detector[4] == 0:
                    angle = little_turn
                    speed = 50
                elif detector[4] == 1:
                    angle = medium_turn
                    speed = 45
            elif detector[3] == 0:
                if detector[4] == 1:
                    angle = heavy_turn
                    speed = 40
        self.car.accelerator.go_forward(speed)
        self.car.steering.turn_right(90 + angle)
        determine_left = False
    
    # 값이 튀면 현재 경로 유지
    else: continue

    1) 직진 상황에서 70의 속도로 주행합니다.
    2) verylittle_turn 상황에서 60의 속도로 주행합니다.
    3) little_turn 상황에서 50의 속도로 주행합니다.
    4) medium_turn 상황에서 45의 속도로 주행합니다.
    5) heavy_turn 상황에서 40의 속도로 주행합니다.
    6) 값이 튀면 현재 주행을 유지합니다.
    7) 원활하게 코너를 돌아나갈 수 있도록 단계별 감속을 실행합니다.
    8) 라인이 3개이상 감지되어도 적정 값을 찾아서 주행할 수 있습니다.

## 7. 정상적으로 라인트레이싱 중 코스를 이탈하면 후진합니다.
    # 장애물을 감지하지 않은 상황에서 라인이 사라졌을 때 정지 후 반대방향으로 조향 후 후진
    elif detector == [0, 0, 0, 0, 0] and obstacle_detect == False:
        self.car.accelerator.stop()
        time.sleep(0.1)
        while determine_left == True:
            self.car.steering.turn_right(130)
            self.car.accelerator.go_backward(50)
            detector = self.car.line_detector.read_digital()
            if detector[2] == 1:
                stopback_time = time.time()
                time.sleep(0.1)
                break
        while determine_left == False:
            self.car.steering.turn_left(50)
            self.car.accelerator.go_backward(50)
            detector = self.car.line_detector.read_digital()
            if detector[2] == 1:
                stopback_time = time.time()
                time.sleep(0.1)
                break
    
    1) 직전 조향의 반대방향으로 40도 조향하고 50의 속도로 후진합니다.
    2) 중앙 트레이싱센서에 라인이 감지될 때 까지 후진합니다.
        - 라인이 감지되면 후진이 끝난 현재시간을 stopback_time에 저장하여 출발선 판단조건으로 사용합니다.

## 8. 출발선이 감지되면 1랩씩 증가시켜 2랩을 완주 후 정지합니다.
    # 정지조건(0번, 3번 센서에 라인이 동시감지)이 감지되었을 때 lap_cnt를 증가시키고, 2랩 완주 후 정지
        elif detector[0] == 1 and detector[3] == 1:
            lapcnt_time = time.time()
            if 2.2 > lapcnt_time - stopback_time > 0.5:
                lap_cnt += 1
                print("+1 lap")
            if lap_cnt == 2:
                end_time = time.time()
                self.car.drive_parking()
                print("완주시간 : ", end_time - start_time)
                break
            while detector[0] == 1 and detector[3] == 1:
                detector = self.car.line_detector.read_digital()
    
    1) 출발선의 형태 불안정성을 감안하여 0번, 3번센서에 라인이 동시감지되는 상황을 정지조건으로 판단합니다.
    2) 정지조건이 감지된 시간을 lapcnt_time에 저장하고 stopback_time과 차를 구해 0.3초과, 2미만 일 때만 출발선을 감지한 것으로 판단합니다.
        - 수정조향과정에서 정지조건이 걸리면 0.5을 넘는 값이 나올 수 없음을 반복주행을 통해 확인하였습니다.
        - 장애물을 피하고 메인스트리트로 복귀하는 과정에서 의도치않게 정지조건이 감지되면 2.2초가 넘는 값이 나옴을 확인했습니다.
        - 따라서 마지막 코너를 돌아 출발선을 감지하기까지 0.3초 초과, 2초 미만의 시간이 걸림을 측정하고 값을 결정하였습니다.
    3) 완주시간을 계산하여 터미널에 출력합니다.