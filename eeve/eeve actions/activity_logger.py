from datetime import datetime, timedelta
import math
from time import sleep
from travel_backpack import Singleton, thread_encapsulation, time_now_to_string
import win32gui, win32process, psutil

timer_runing = False
timer_initialized = False


class Timer(metaclass=Singleton):
    def __init__(self, t=5 * 60, p='activity.log'):
        global timer_initialized
        print('starting timer')
        self.last_move = datetime.now()
        self.active = False
        self.t = t
        self.log_path = p
        self.countdown()
        timer_initialized = True
        self.last_active_window = ''
        self.last_active_window_time = self.last_move

    @thread_encapsulation
    def countdown(self):
        while True:
            #print(self.active, self.t - (datetime.now() - self.last_move).total_seconds())
            if self.active and (datetime.now() - self.last_move).total_seconds() >= self.t:
                self.active = False
                print('System deactivated')
                with open(self.log_path, 'a') as f:
                    f.write(f'[{time_now_to_string()}] System Idle\n')

            if self.active:
                self.update_window()

            sleep(1)

    def update(self, print_proc_name=False):
        if not self.active:
            self.active = True
            print('System activated')
            with open(self.log_path, 'a') as f:
                time = round_up_time_delta(datetime.now() - self.last_move)
                f.write(f'\n\n\n[{time_now_to_string()}] System resume from {time} idle time\n')

        self.last_move = datetime.now()
        if print_proc_name:
            sleep(0.1)
            self.update_window()

    def update_window(self):
        active_window = self.get_active_window()
        if active_window != self.last_active_window:
            with open(self.log_path, 'a') as f:
                time = round_up_time_delta(datetime.now() - self.last_active_window_time)
                f.write(f'[{time_now_to_string()}] spent {time} on {self.last_active_window}\n' +
                        f'[{time_now_to_string()}] ---------------> {active_window}\n')

            self.last_active_window = active_window
            self.last_active_window_time = self.last_move

    def get_active_window(self):
        fgw = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(fgw)  #This produces a list of PIDs active window relates to
        return f'{psutil.Process(pid[-1]).name()}: {win32gui.GetWindowText(fgw)}'


def round_up_time_delta(td: timedelta) -> timedelta:
    return timedelta(seconds=math.ceil(td.total_seconds()))


def log_activity():
    if timer_initialized:
        t = Timer()
        t.update()


def log_activity_and_current_window():
    if timer_initialized:
        t = Timer()
        t.update(True)


def initialize_logger(time, log_path):
    global timer_runing
    if not timer_runing:
        timer_runing = True
        t = Timer(t=time * 60, p=log_path)


actions = {
    'log activity': {
        'run': log_activity
    },
    'log activity and current window': {
        'run': log_activity_and_current_window
    },
    'start activity logger': {
        'run': initialize_logger
    }
}
