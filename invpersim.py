from math import *
import time
import random
import pygame
import pygame.display
import pygame.draw


class InvPerSim:
    def __init__(self):
        self.tilt = 0.0
        self.ang_vel = 0.0
        self.pos = 0.0
        self.vel = 0.0
        self._show_init = False

    def reset(self):
        self.tilt = 0.0
        self.ang_vel = 0.0
        self.pos = 0.0
        self.vel = 0.0

    def randomize(self):
        random.seed()
        self.tilt = random.uniform(-pi/4, pi/4)
        self.ang_vel = random.uniform(-pi/6, pi/6)
        self.pos = random.uniform(-1.5, 1.5)
        self.vel = random.uniform(-0.5, 0.5)
        return self

    def copy(self):
        ips = InvPerSim()
        ips.tilt = self.tilt
        ips.ang_vel = self.ang_vel
        ips.pos = self.pos
        ips.vel = self.vel
        return ips

    def start_show(self, size):
        self._show_init = True
        pygame.init()
        if pygame.display.get_init():
            pygame.display.quit()
        pygame.display.init()
        self._display = pygame.display.set_mode([size, 240])
        self._size = size

    def stop_show(self):
        self._show_init = False
        self._display = None
        if pygame.display.get_init():
            pygame.display.quit()

    def show(self):
        if not self._show_init:
            return
        self._display.fill((255, 255, 255))
        pygame.draw.line(self._display, (0, 255, 0),
                         (int(self._size/2 + self.pos*100 - 10), 120),
                         (int(self._size/2 + self.pos*100 + 10), 120),
                         5)
        pygame.draw.line(self._display, (0, 0, 255),
                         (int(self._size/2 + self.pos*100), 120),
                         (int(self._size/2 + self.pos*100 +
                              100*sin(self.tilt)),
                         int(120 - cos(self.tilt)*100)), 2)
        pygame.draw.circle(self._display, (255, 0, 0),
                           (int(self._size/2 + self.pos*100 +
                                100*sin(self.tilt)),
                           int(120 - cos(self.tilt)*100)),
                           10, 0)
        pygame.display.flip()

    def sim(self, time_ctrl, test_func):
        err = 0.0
        time_ctrl.start()
        while not time_ctrl.get_stop():
            dt = time_ctrl.dtime()
            acc = test_func(self.tilt, self.ang_vel,
                            self.pos, self.vel)
            self.vel += acc * dt
            self.pos += self.vel * dt
            ang_acc = 10.0 * sin(self.tilt) - acc * cos(self.tilt)
            self.ang_vel += ang_acc * dt
            self.tilt += self.ang_vel * dt
            nerr = 0.0
            nerr += 3.0 * cos(self.tilt)
            nerr += 1.0 * (1 / (1 + self.ang_vel ** 2))
            nerr += 1.0 * (1 / (1 + self.pos ** 2))
            nerr += 0.5 * (1 / (1 + self.vel ** 2))
            err += nerr * dt
            if abs(self.tilt) > pi/2 or abs(self.pos) > 5:
                return err
            self.show()
        return err

    class ConstantTimeCtrl:
        def __init__(self, time_step=0.01, step_count=2000):
            self.time_step = time_step
            self.step_count = step_count
            
        def start(self):
            self._cnt = 0
            
        def get_stop(self):
            return self._cnt >= self.step_count
            
        def dtime(self):
            self._cnt += 1
            return self.time_step
            
    class RealTimeCtrl:
        def __init__(self, sim_length=20.0):
            self.sim_length = sim_length
        
        def start(self):
            self._t = 0.0
            self._lt = time.perf_counter()
            
        def get_stop(self):
            return self._t > self.sim_length
            
        def dtime(self):
            nt = time.perf_counter()
            dt = nt - self._lt
            self._t += dt
            self._lt = nt
            return dt

    def ct_sim(self, test_func, time_step=0.01, step_count=2000):
        return self.sim(self.ConstantTimeCtrl(time_step, step_count),
                        test_func)

    def rt_sim(self, test_func, sim_legth=20.0):
        return self.sim(self.RealTimeCtrl(sim_legth),
                        test_func)
