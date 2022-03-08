from pybricks.parameters import Button
from pybricks.tools import wait
from threading import Thread
from time import time
from pybricks.parameters import Stop
from math import pi
class FLL:
    def __init__(self, robot):
        self.robot = robot
        # Δείχνει τον αριθμό του τρέχοντος run
        self.current_run = 0
        # Το συνολικό πλήθος των runs μέχρι τώρα
        self.total_runs = 4
        self.last_run_time = 0
        self.total_runs_time = 0
        

    def display_menu(self):
        screen = self.robot.ev3.screen
        screen.clear()
        screen.print()
        screen.print("                 RUN " + str(self.current_run))
        screen.print()
        screen.print("Previous                       Next")
        screen.print("       Press Center to Start")
        screen.print("last run time: " + str(self.last_run_time))
        screen.print("total run time: " + str(self.total_runs_time))
        

    def run(self):
        if self.current_run == 1:
            self.run_1()
        elif self.current_run == 2:
            self.run_2()
        elif self.current_run == 3:
            self.run_3()
        elif self.current_run == 4:
            self.run_4()
        # Αύξηση του μετρητή, για να τρέξει την επόμενη φορά το επόμενο run
        self.current_run += 1
        # Αν ξεπεράσουμε το τελευταίο run, επιστρέφουμε στο 1ο
        if self.current_run > self.total_runs: 
            self.current_run = 1

    def main(self):
        # Ξεκινάμε από το 1ο run
        self.current_run = 1
        start_time = time()
        # Έναρξη αποστολών
        while True:
            # Εμφάνιση του κεντρικού μενού
            self.display_menu()
            #wait(500)
            # Αναμονή για την επιλογή του χρήστη

            while not self.robot.ev3.buttons.pressed():
                pass
            if Button.CENTER in self.robot.ev3.buttons.pressed():
                # Με το μεσαίο κουμπί τρέχουμε το run που φαίνεται στην οθόνη
                start_run = time()
                self.run()
                self.last_run_time = time() - start_run
                self.total_runs_time += self.last_run_time
            elif Button.LEFT in self.robot.ev3.buttons.pressed():
                # Με το αριστερό κουμπί, αλλάζουμε τον μετρητή στο προηγούμενο run
                if self.current_run > 1:
                    self.current_run -= 1
                else:
                    # ... εκτός και αν είναι το πρώτο οπότε  πάμε στο τελευταίο
                    self.current_run = self.total_runs
                wait(300)
            elif Button.RIGHT in self.robot.ev3.buttons.pressed():
                # Με το δεξί κουμπί, αλλάζουμε τον μετρητή στο επόμενο run
                self.current_run += 1
                # ... εκτός και αν είναι το τελευταίο, επιστρέφουμε πάμε στο 1ο
                if self.current_run > self.total_runs: 
                    self.current_run = 1
                wait(300)
            elif Button.DOWN in self.robot.ev3.buttons.pressed():
                # Με το κάτω πλήκτρο σταματάμε το ρομπότ προσωρινά και ...
                self.robot.stop("BRAKE")
                self.robot.ev3.screen.clear()
                self.robot.ev3.screen.print("Are you sure you")
                self.robot.ev3.screen.print("want to exit?")
                self.robot.ev3.screen.print()
                self.robot.ev3.screen.print("(CENTER to exit)")
                self.robot.ev3.screen.print("(UP to continue)")
                wait(500)
                # ... περιμένουμε τον χρήστη να επιβεβαιώσει το κλείσιμο του προγράμματος ...
                while not self.robot.ev3.buttons.pressed():
                    pass
                if Button.CENTER in self.robot.ev3.buttons.pressed():
                    break
                elif Button.UP in self.robot.ev3.buttons.pressed():
                    # ... ή να ακυρώσει την προηγούμενη επιλογή του και να ξαναεπιστρέψει στο πρόγραμμα
                    continue
                
    
    def run_1(self):
        
        self.robot.ev3.screen.clear()
        self.robot.ev3.screen.print("RUN 1")
        self.robot.ev3.screen.print()
        self.robot.ev3.screen.print("LEFT: Yellow on 1")
        self.robot.ev3.screen.print("RIGHT: Yellow on 3")
        
        self.robot.move_back_arm(speed=-30, mode="time", value=0.2, wait=False)
        self.robot.move_front_arm(speed=50, mode="time", value=0.2, wait=False)
        while Button.LEFT not in self.robot.ev3.buttons.pressed() and Button.RIGHT not in self.robot.ev3.buttons.pressed():
            pass
        yellow = 1
        if Button.RIGHT in self.robot.ev3.buttons.pressed():
            yellow = 3
        ################ RUN 1 - START ##################
        #  M14        
        self.robot.move_front_arm(speed=-100, mode="angle", value=163)
        wait(200)
        self.robot.drive_base.stop()
        self.robot.left_motor.reset_angle(0)
        t14 = Thread(target=self.thr_run1_m14, args=())
        t14.start()
        self.robot.straight(distance=85, speed=100, brake=True)
        self.robot.move_front_arm(speed=50, mode="angle", value=123, wait=False)
        self.robot.straight(distance=33, speed=100, brake=True)

        # M11
        self.robot.turn(angle=90, brake=True)
        self.robot.drive(speed=80, turn_rate=0, mode="time", value=0.8, brake=True)
        self.robot.straight(distance=-6, speed=80, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.straight(distance=-9, speed=100, brake=True)
        for i in range(3):
            self.robot.move_back_arm(speed=100, mode="time", value=0.25)
            wait(50)
            self.robot.move_back_arm(speed=-100, mode="time", value=0.25)
            wait(50)
        self.robot.straight(distance=8.5, speed=80, brake=True)

        # M10
        self.robot.turn(angle=-90, brake=True)
        self.robot.drive(speed=80, turn_rate=0, mode="time", value=0.3, brake=True)
        self.robot.straight(distance=-42.5, speed=90, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.straight(distance=6, speed=90, brake=False)
        self.robot.straight(distance=-20, speed=90, brake=False)
        self.robot.backward_align()
        if yellow == 3:
            self.robot.straight(distance=-6, speed=90, brake=True)
            self.robot.turn(angle=90, brake=True)
            self.robot.straight(distance=9, speed=40, brake=True)
            self.robot.move_back_arm(speed=100, mode="time", value=0.4, then=Stop.COAST)
            #wait_button()
            self.robot.straight(distance=-9, speed=10, brake=True)
            self.robot.move_back_arm(speed=-80, mode="time", value=3, wait=False)
            wait(300)
            self.robot.straight(distance=4, speed=15, brake=True)
            self.robot.turn(angle=90, brake=True)
            self.robot.straight(distance=8, speed=100, brake=True)
        else:
            self.robot.straight(distance=-16, speed=90, brake=True)
            self.robot.turn(angle=90, brake=True)
            self.robot.straight(distance=9, speed=40, brake=True)
            self.robot.move_back_arm(speed=100, mode="time", value=0.4, then=Stop.COAST)
            #wait_button()
            self.robot.straight(distance=-9, speed=10, brake=True)
            self.robot.move_back_arm(speed=-80, mode="time", value=3, wait=False)
            wait(300)
            self.robot.straight(distance=3, speed=15, brake=True)
            self.robot.turn(angle=90, brake=True)
            #self.robot.straight(distance=8, speed=100, brake=True)
        # M09
        
        self.robot.forward_align()
        self.robot.straight(distance=2.5, speed=80, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.straight(distance=9, speed=100, brake=True)
        self.robot.turn(angle=-10, brake=True)
        self.robot.move_front_arm(speed=-100, mode="time", value=0.6)
        self.robot.move_front_arm(speed=70, mode="angle", value=170)
        self.robot.turn(angle=10, brake=True)

        # M17
        self.robot.straight(distance=-43, speed=100, brake=True)
        self.robot.stop("Brake")
        self.robot.move_front_arm(speed=-80, mode="time", value=0.6)
        self.robot.move_front_arm(speed=80, mode="angle", value=30)
        self.robot.lf_cross(port=1, speed=60, min_distance=40, accelerate=False, then="Brake", outer=True)
        self.robot.stop("Brake")
        #self.robot.straight(distance=1, speed=80, brake=True)
        self.robot.move_front_arm(speed=100, mode="angle", value=150)

        #M08
        self.robot.turn(angle=-15, brake=True)
        self.robot.straight(distance=-53, speed=100, brake=True)
        self.robot.forward_align()
        self.robot.straight(distance=2, speed=40, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.straight(distance=-12, speed=40, brake=True)
        
        # M04a
        self.robot.lf_distance(port=1, speed=40, distance=3, accelerate=False, then="Nothing", outer=True, pid_ks=(0.4, 0.1, 0.005))
        self.robot.lf_distance(port=1, speed=70, distance=40, accelerate=False, then="Nothing", outer=True, pid_ks=(0.5, 0.1, 0.002))
        self.robot.lf_cross(port=1, speed=40, min_distance=25, accelerate=False, then="Nothing", outer=True, pid_ks=(0.5, 0.1, 0.005))
        self.robot.lf_distance(port=1, speed=60, distance=2, accelerate=False, then="Nothing", outer=True, pid_ks=(0.3, 0.05, 0.001))
        self.robot.lf_distance(port=1, speed=60, distance=24, accelerate=False, then="Brake", outer=True, pid_ks=(0.5, 0.1, 0.006))
        self.robot.move_front_arm(speed=80, mode="time", value=0.6)
        self.robot.lf_distance(port=1, speed=30, distance=17, accelerate=False, then="Brake", outer=True, pid_ks=(0.6, 0.2, 0.02))
        self.robot.move_front_arm(speed=-80, mode="angle", value=200)

        # # M04b
        self.robot.lf_distance(port=1, speed=25, distance=4, accelerate=False, then="Brake", outer=True, pid_ks=(0.6, 0.1, 0.02))
        self.robot.lf_distance(port=1, speed=50, distance=20, accelerate=False, then="Brake", outer=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.backward_align()
        self.robot.straight(distance=21, speed=80, brake=True)
        self.robot.move_front_arm(speed=50, mode="time", value=0.8)
        self.robot.straight(distance=35, speed=90, brake=True)
        # self.robot.turn(angle=-45, brake=True)
        self.robot.move_front_arm(speed=-80, mode="angle", value=120, wait=False)
        wait(50)
        self.robot.turn(angle=60, brake=True)
        self.robot.move_back_arm(speed=100, mode="time", value=0.3, wait=False)
        self.robot.straight(distance=-35, speed=100, brake=True)

        ################ RUN 1 - END ##################

    def thr_run1_m14(self):
        while abs(self.robot.left_motor.angle()) < 840:
            pass
        self.robot.move_front_arm(speed=-100, mode="angle", value=105, wait=True)
        # self.robot.move_front_arm(speed=100, mode="angle", value=90, wait=False)

    def run_2(self):
        self.robot.ev3.screen.clear()
        self.robot.ev3.screen.print("RUN 2: Press UP to GO!")
        self.robot.move_front_arm(speed=100, mode="time", value=0.5)
        while Button.UP not in self.robot.ev3.buttons.pressed():
            pass
        ################ RUN 2 - START ##################
        # M03
        self.robot.straight(distance=14, speed=100, brake=True)
        self.robot.lf_cross(port=2, speed=50, min_distance=50, accelerate=False, then="Brake", outer=False)
        self.robot.straight(distance=8, speed=100, brake=True)
        self.robot.move_back_arm(speed=100, mode="time", value=1)
        self.robot.move_back_arm(speed=-100, mode="angle", value=200)

        # M05
        self.robot.straight(distance=6, speed=100, brake=True)
        self.robot.move_front_arm(speed=-30, mode="time", value=0.8)
        self.robot.straight(distance=-30, speed=100, brake=True)
        self.robot.move_front_arm(speed=100, mode="time", value=0.3)
        self.robot.straight(distance=-50, speed=100, brake=True)

        ################ RUN 2 - END ##################

    def run_3(self):
        self.robot.ev3.screen.clear()
        self.robot.ev3.screen.print("RUN 3: Press UP to GO!")
        while Button.UP not in self.robot.ev3.buttons.pressed():
            pass
        ################ RUN 3 - START ##################
        # get truck
        self.robot.straight(distance=5, speed=100, brake=False)
        self.robot.lf_distance(port=2, speed=60, distance=25, accelerate=False, then="Nothing", outer=False)
        self.robot.lf_distance(port=2, speed=50, distance=10, accelerate=False, then="Nothing", outer=False)
        self.robot.lf_distance(port=2, speed=60, distance=30, accelerate=False, then="Brake", outer=False)
        self.robot.move_back_arm(speed=-100, mode="time", value=0.5)
        self.robot.straight(distance=-100, speed=100, brake=False)
        ################ RUN 3 - END ##################

    def run_4(self):
        self.robot.ev3.screen.clear()
        self.robot.ev3.screen.print("RUN 4: Press UP to GO!")
        self.robot.move_front_arm(speed=-100, mode="time", value=0.4, wait=False)
        self.robot.move_back_arm(speed=20, mode="time", value=0.4, wait=False)
        # while Button.UP not in self.robot.ev3.buttons.pressed():
        #     pass
        ################ RUN 4 - START ##################
        # M13
        self.robot.move_front_arm(speed=-100, mode="time", value=0.2, wait=False)
        self.robot.move_back_arm(speed=20, mode="time", value=0.2, wait=False)
        self.robot.straight(distance=10, speed=100, brake=False)
        self.robot.lf_cross(port=2, speed=60, min_distance=20, accelerate=False, then="Nothing", outer=False)
        self.robot.lf_distance(port=2, speed=50, distance=12, accelerate=False, then="Brake", outer=False)
        self.robot.lf_distance(port=2, speed=60, distance=40, accelerate=False, then="Brake", outer=False)
        self.robot.straight(distance=-3, speed=80, brake=True)

        # M01 - M16/CargoConnect
        self.robot.lf_cross(port=2, speed=60, min_distance=27, accelerate=False, then="Brake", outer=False)
        self.robot.straight(distance=8, speed=100, brake=True)
        self.robot.pivot(speed=80, degrees=250)

        # M16/Blue
        self.robot.straight(distance=-6, speed=80, brake=True)
        self.robot.turn(angle=-100, brake=True)
        self.robot.lf_distance(port=2, speed=25, distance=3, accelerate=False, then="Nothing", outer=False, pid_ks=(0.6, 0.1, 0.02))
        self.robot.lf_cross(port=2, speed=60, min_distance=46, accelerate=False, then="Brake", outer=False)
        self.robot.straight(distance=-5, speed=80, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.move_back_arm(speed=-20, mode="time", value=0.8)
        self.robot.straight(distance=3, speed=80, brake=True)
        self.robot.move_back_arm(speed=30, mode="time", value=0.5)

        # M16/center gray
        self.robot.straight(distance=-4, speed=80, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.lf_distance(port=1, speed=50, distance=13, accelerate=False, then="Brake", outer=False)
        self.robot.turn(angle=90, brake=True)
        self.robot.move_back_arm(speed=-40, mode="time", value=0.5)
        self.robot.straight(distance=7, speed=80, brake=True)
        self.robot.move_back_arm(speed=100, mode="time", value=0.5, wait=False)

        # M07
        self.robot.straight(distance=-7, speed=80, brake=True)
        self.robot.turn(angle=-87, brake=True)
        self.robot.lf_distance(port=1, speed=60, distance=25, accelerate=False, then="Brake", outer=False)
        self.robot.turn(angle=38, brake=True)
        self.robot.straight(distance=29, speed=100, brake=True)
        self.robot.forward_align()
        self.robot.straight(distance=14, speed=100, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.straight(distance=22, speed=80, brake=True)
        self.robot.turn(angle=90, brake=True)
        self.robot.move_front_arm(speed=100, mode="time", value=1, wait=False)
        self.robot.straight(distance=26, speed=100, brake=True)

        # M06
        self.robot.straight(distance=-14, speed=100, brake=True)
        self.robot.turn(angle=30, brake=True)
        self.robot.straight(distance=-17, speed=100, brake=True)
        self.robot.turn(angle=-30, brake=True)
        self.robot.forward_align()
        t06 = Thread(target=self.thr_run4_m06, args=())
        t06.start()
        self.robot.straight(distance=-9.5, speed=50, brake=True)
        
        ################ RUN 4 - END ##################


    def thr_run4_m06(self):
        self.robot.move_back_arm(speed=80, mode="time", value=0.2, wait=True)
        self.robot.move_back_arm(speed=-50, mode="angle", value=48, wait=True)