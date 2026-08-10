import time
import pygame
import colorama
from colorama import Back, Fore
colorama.init(autoreset=True)

class ControllerClass:
    def __init__(self):
        self.bind = None
        self.controller = None
        self.running = False
        self.leftX = 0
        self.leftY = 0
        self.rightX = 0
        self.rightY = 0

        self.leftTrigger = 0
        self.rightTrigger = 0

    def __repr__(self):
        return f""" Controller
Binded to: ROBOT {self.bind}
Running: {self.running}
Left Stick: ({self.leftX:.2f}, {self.leftY:.2f})
Right Stick: ({self.rightX:.2f}, {self.rightY:.2f})
Left Trigger: {self.leftTrigger:.2f}
Right Trigger: {self.rightTrigger:.2f}"""

    def start(self):
        if self.running:
            print(Fore.RED + "[CONT] Controller already running")

        try:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.running = True
            self.controller.rumble(1, 500,1)
            print(Back.GREEN + f"[CONT] Connected {self.controller.get_name()}")
            time.sleep(1)
            self.controller.stop_rumble()
            return True
        except pygame.error as e:
            pygame.quit()
            print(Fore.RED + f"[CONT] Error: {e}")
            return False

    def stop(self):
        pygame.quit()
        self.running = False
        print("[CONT] Disconnected")

    def update(self):
        if self.controller is not None:
            pygame.event.pump()
            self.leftX = self.controller.get_axis(0)
            self.leftY = self.controller.get_axis(1)
            self.rightX = self.controller.get_axis(2)
            self.rightY = self.controller.get_axis(3)

            self.leftTrigger = self.controller.get_axis(4)
            self.rightTrigger = self.controller.get_axis(5)

    def control(self, roboid):
        self.bind = roboid


pygame.init()
controller = ControllerClass()
if __name__ == "__main__":
    controller.start()
    while True:
       # controller.update()
        print(controller)
        time.sleep(1)