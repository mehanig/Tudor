import os
import signal
from enum import Enum
from functools import partial

import subprocess
import asyncio


class FfmpegActions(Enum):
    START = 'START'
    STOP = 'STOP'
    KILL_ALL = 'KILL_ALL'


class FFmpegRunner():

    proc_list = set()
    proc_maper = {}

    run_command_tmplt = ' '.join(
    ['ffmpeg', '-f', 'lavfi', '-i', 'nullsrc=s=1920x1080:d=250', '-vf', '"geq=random(1)*255:128:128"',
     '{file_path}', '-y'])

    def __init__(self, params):
        if not FFmpegRunner.is_correct(params):
            return
        self.action = FfmpegActions(params['ACTION'][0])
        self.path = params['PATH'][0]
        if self.action == FfmpegActions.START:
            self.run_command = self.run_command_tmplt.format(file_path=self.path)
            self.actor = self.run
        if self.action == FfmpegActions.STOP:
            for pid in list(FFmpegRunner.proc_maper):
                if FFmpegRunner.proc_maper[pid] == self.path:
                    self.actor = partial(self.proc_killer_deferred, [pid])
        if self.action == FfmpegActions.KILL_ALL:
            self.actor = FFmpegRunner.kill_all
        super().__init__()

    @staticmethod
    def is_correct(params):
        if params and 'ACTION' in params and 'PATH' in params:
            if params['ACTION'] and params['PATH'] and len(params['ACTION']) == 1 and len(params['PATH']) == 1:
                return True
        return False

    @staticmethod
    def kill(pid):
        del FFmpegRunner.proc_maper[pid]
        FFmpegRunner.proc_list.remove(pid)
        os.kill(pid, signal.SIGKILL)

    # TODO: Make it author safe: Can Kill only processes spawned by Python
    @staticmethod
    def kill_all():
        for p in list(FFmpegRunner.proc_list):
            try:
                FFmpegRunner.kill(p)
            except ProcessLookupError as e:
                pass # Make shure we don't fail due to race conditions

    def sigkill(self, pid=None):
        if pid is not None:
            self.proc_id = pid
        FFmpegRunner.kill(self.proc_id)

    def add_process_to_pool(self, _id):
        self.proc_id = _id
        FFmpegRunner.proc_list.add(self.proc_id)

    def run(self):
        proc = subprocess.Popen(self.run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.add_process_to_pool(proc.pid)
        FFmpegRunner.proc_maper[self.proc_id] = self.path
        return proc

    def act(self):
        return self.actor()

    def proc_killer_deferred(self, pid_list):
        for l in pid_list:
            self.sigkill(l)

    def stop(self):
        self.sigkill()
