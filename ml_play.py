class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = (0, 0)
        self.car_lane = -1
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        command = []
        speed = 0
        nlanes = 0
        road = [0 for i in range(9)]
        money = [0 for i in range(9)]
        self.car_pos = scene_info[self.player]
        if self.car_pos != () and self.car_lane != self.car_pos[0] // 70:
            self.car_lane = self.car_pos[0] // 70
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
            elif car['pos'] != () and self.car_pos != ():
                for i in range(9):
                    if(car['pos'][0] >= i * 70 and car['pos'][0] < (i + 1) * 70 and car['pos'][1] <= self.car_pos[1] - 400 and car['pos'][1] > self.car_pos[1] - 600 and road[i] < 1):
                        road[i] = 0.5
                    elif(car['pos'][0] >= i * 70 and car['pos'][0] < (i + 1) * 70 and car['pos'][1] <= self.car_pos[1] - 200 and car['pos'][1] > self.car_pos[1] - 400 and road[i] < 1):
                        road[i] = 1
                    elif(car['pos'][0] >= i * 70 and car['pos'][0] < (i + 1) * 70 and car['pos'][1] <= self.car_pos[1] - 100 and car['pos'][1] > self.car_pos[1] - 200 and road[i] < 2):
                        road[i] = 2
                    elif(car['pos'][0] >= i * 70 and car['pos'][0] < (i + 1) * 70 and car['pos'][1] <= self.car_pos[1] + 85 and car['pos'][1] > self.car_pos[1] - 100 and road[i] < 3):
                        road[i] = 4
                                
        if scene_info["status"] != "ALIVE":
            return "RESET"
        for coin in scene_info["coins"]:
            for i in range(9):
                if coin != () and self.car_pos != ():
                    if coin[0] // 70 == i and coin[1] < self.car_pos[1]:
                        money[i] = 1
        for i in range(9):
            road[i] += (abs(i - self.car_lane) // 2)
            road[i] -= money[i]
        road[0] += 0.5
        road[8] += 0.5
        for car in scene_info["cars_info"]:
            if car["id"] != self.player_no and car['pos'] != () and self.car_pos != ():
                if abs(car['pos'][0] - self.car_pos[0]) < 45 and car['pos'][1] < self.car_pos[1] and self.car_pos[1] - car['pos'][1] <= 150 and self.car_vel > car['velocity']:
                    return ['BRAKE']
        for car in scene_info["cars_info"]:
            if car["id"] != self.player_no and car['pos'] != () and self.car_pos != ():
                if car['pos'][0] <= self.car_pos[0] and self.car_pos[0] - car['pos'][0] <= 46 and car['pos'][1] <= self.car_pos[1] + 85 and car['pos'][1] >= self.car_pos[1] - 85:
                    return ['MOVE_RIGHT']
                if car['pos'][0] >= self.car_pos[0] and car['pos'][0] - self.car_pos[0] <= 46 and car['pos'][1] <= self.car_pos[1] + 85 and car['pos'][1] >= self.car_pos[1] - 85:
                    return ['MOVE_LEFT']
        nlanes = road.index(min(road))
        if road[self.car_lane] == min(road) and self.car_lane >= 0:
            nlanes = self.car_lane
        if self.car_pos != ():
            if self.car_pos[0] < self.lanes[nlanes] - 4:
                command.append('MOVE_RIGHT')
            elif self.car_pos[0] > self.lanes[nlanes] + 4:
                command.append('MOVE_LEFT')
        '''if self.player_no == 0:
            print(road)
            print(self.car_lane)
            print(nlanes)'''
        if min(road) >= 3:
            speed = 0
        elif min(road) == 2:
            speed = 1
        elif min(road) <= 1:
            speed = 2
        if speed == 2:
            command.append('SPEED')
        elif speed == 0:
            command.append('BRAKE')
        return command


    def reset(self):
        """
        Reset the status
        """
        pass