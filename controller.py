import time
import pygame
import colorama
from colorama import Back
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
Binded to: {self.bind}
Running: {self.running}
Left Stick: ({self.leftX:.2f}, {self.leftY:.2f})
Right Stick: ({self.rightX:.2f}, {self.rightY:.2f})
Left Trigger: {self.leftTrigger:.2f}
Right Trigger: {self.rightTrigger:.2f}"""

    def start(self):
        try:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.running = True
            print(Back.GREEN + "[CONT] Connected")
            return True
        except pygame.error as e:
            pygame.quit()
            print(Back.RED + f"[CONT] Error: {e}")
            return False

    def stop(self):
        pygame.quit()
        self.running = False
        print(Back.GREEN + "[CONT] Disconnected")

    def update(self):
        if controller:
            pygame.event.pump()
            self.leftX = self.controller.get_axis(0)
            self.leftY = self.controller.get_axis(1)
            self.rightX = self.controller.get_axis(2)
            self.rightY = self.controller.get_axis(3)

            self.leftTrigger = self.controller.get_axis(4)
            self.rightTrigger = self.controller.get_axis(5)

    def bind(self, roboid):
        self.bind = roboid


pygame.init()
controller = ControllerClass()
controller.start()
if __name__ == "__main__":
    controller.start()
    while True:
        controller.update()
        print(controller)
        time.sleep(1)