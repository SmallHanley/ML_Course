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
        self.car_pos = ()
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        check = [0, 0, 0]
        self.car_pos = scene_info[self.player]
        if self.car_pos != ():
            if self.car_pos[0]  < 35:
                check[0] = 4
            if self.car_pos[0] > 595:
                check[2] = 4
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
            elif car['pos'] != () and self.car_pos != ():
                if(car['pos'][0] > self.car_pos[0] - 70 and car['pos'][0] < self.car_pos[0] + 70 and car['pos'][1] <= self.car_pos[1] and car['pos'][1] > self.car_pos[1] - 100):
                    check[1] = 3
                if(car['pos'][0] > self.car_pos[0] - 100 and car['pos'][0] < self.car_pos[0] - 20 and car['pos'][1] <= self.car_pos[1] + 10 and car['pos'][1] > self.car_pos[1] - 100):
                    check[0] = 3
                if(car['pos'][0] > self.car_pos[0] + 20 and car['pos'][0] < self.car_pos[0] + 100 and car['pos'][1] <= self.car_pos[1] + 10 and car['pos'][1] > self.car_pos[1] - 100):
                    check[2] = 3
                if(car['pos'][0] > self.car_pos[0] - 70 and car['pos'][0] < self.car_pos[0] + 70 and car['pos'][1] <= self.car_pos[1] - 100 and car['pos'][1] > self.car_pos[1] - 200):
                    check[1] = 2
                if(car['pos'][0] > self.car_pos[0] - 100 and car['pos'][0] < self.car_pos[0] - 20 and car['pos'][1] <= self.car_pos[1] - 100 and car['pos'][1] > self.car_pos[1] - 200):
                    check[0] = 2
                if(car['pos'][0] > self.car_pos[0] + 20 and car['pos'][0] < self.car_pos[0] + 100 and car['pos'][1] <= self.car_pos[1] - 100 and car['pos'][1] > self.car_pos[1] - 200):
                    check[2] = 2
                if(car['pos'][0] > self.car_pos[0] - 70 and car['pos'][0] < self.car_pos[0] + 70 and car['pos'][1] <= self.car_pos[1] - 200 and car['pos'][1] > self.car_pos[1] - 400):
                    check[1] = 1
                if(car['pos'][0] > self.car_pos[0] - 100 and car['pos'][0] < self.car_pos[0] - 20 and car['pos'][1] <= self.car_pos[1] - 200 and car['pos'][1] > self.car_pos[1] - 400):
                    check[0] = 1
                if(car['pos'][0] > self.car_pos[0] + 20 and car['pos'][0] < self.car_pos[0] + 100 and car['pos'][1] <= self.car_pos[1] - 200 and car['pos'][1] > self.car_pos[1] - 400):
                    check[2] = 1
        if scene_info["status"] != "ALIVE":
            return "RESET"
        
        
        if check[1] != 0 and check[0] == 0 and check[2] == 0:
            if self.car_pos[0] < 315:
                return ['SPEED', 'MOVE_RIGHT']
            else:
                return ['SPEED', 'MOVE_LEFT']
        elif check[1] != 0 and check[0] == 0 and check[2] != 0:
            return ['SPEED', 'MOVE_LEFT']
        elif check[1] != 0 and check[0] != 0 and check[2] == 0:
            return ['SPEED', 'MOVE_RIGHT']
        elif check[1] != 0 and check[0] != 0 and check[2] != 0:
            idx = check.index(min(check))
            if idx == 0 and check[idx] == 1:
                return ['SPEED', 'MOVE_LEFT']
            elif idx == 0 and check[idx] == 2:
                return ['MOVE_LEFT']
            elif idx == 0 and check[idx] == 3:
                return ['BRAKE', 'MOVE_LEFT']
            elif idx == 1 and check[idx] == 1:
                return ['SPEED']
            elif idx == 1 and check[idx] == 2:
                return []
            elif idx == 1 and check[idx] == 3:
                return ['BRAKE']
            elif idx == 1 and check[idx] == 1:
                return ['SPEED', 'MOVE_RIGHT']
            elif idx == 1 and check[idx] == 2:
                return ['MOVE_RIGHT']
            else:
                return ['BRAKE', 'MOVE_RIGHT']
        elif check[1] == 0:
            return ['SPEED']
        else:['BRAKE']


    def reset(self):
        """
        Reset the status
        """
        pass
