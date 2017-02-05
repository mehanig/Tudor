import os
import signal
import unittest
import uuid
import time
import psutil

from host.ffmpeg_runner import FFmpegRunner, FfmpegActions

FFmpegRunner.run_command_tmplt = ' '.join(
    ['ffmpeg', '-f', 'lavfi', '-i', 'nullsrc=s=1920x1080:d=250', '-vf', '"geq=random(1)*255:128:128"',
     '{file_path}', '-y'])


def random_mp4_name():
    return str(uuid.uuid4()).upper()[0:6] + '.mp4'


class TestFFmpegRunner(unittest.TestCase):

    def setUp(self):
        self.PATH = os.path.sep.join(['.', random_mp4_name()])
        self.PATH_OTHER = os.path.sep.join(['.', random_mp4_name()])

    def tearDown(self):
        FFmpegRunner.kill_all()
        for _PATH in [self.PATH, self.PATH_OTHER]:
            if _PATH.endswith('.mp4'):
                try:
                    os.remove(_PATH)
                except OSError as e:
                    pass

    def test_ffmpeg_is_correct_fails(self):
        self.assertFalse(FFmpegRunner.is_correct(None))
        self.assertFalse(FFmpegRunner.is_correct({}))
        self.assertFalse(FFmpegRunner.is_correct({'ACTION': None}))
        self.assertFalse(FFmpegRunner.is_correct({'PATH': None}))
        self.assertFalse(FFmpegRunner.is_correct({'ACTION': None, 'PATH': 'LOL'}))
        self.assertFalse(FFmpegRunner.is_correct({'ACTION': [None], 'PATH': 'LOL'}))

    def test_ffmpeg_is_correct_correct(self):
        self.assertTrue(FFmpegRunner.is_correct({'ACTION': ['START'], 'PATH': ['/']}))

    def test_ffmpeg_will_start_and_stop(self):
        proc = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        running_process = proc.act()
        self.assertEqual(psutil.Process(running_process.pid).status(), 'running')
        os.kill(running_process.pid, signal.SIGKILL)
        time.sleep(1)
        self.assertEqual(psutil.Process(running_process.pid).status(), 'zombie')

    def test_ffmpeg_creates_file(self):
        proc = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        proc.act()
        time.sleep(0.5)
        file_exist = os.path.exists(self.PATH)
        self.assertTrue(file_exist)

    def test_ffmpeg_can_start_multiple_processes(self):
        proc1 = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        proc2 = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH_OTHER]})
        proc1.act()
        proc2.act()
        time.sleep(1)
        file_exist1, file_exist2 = os.path.exists(self.PATH), os.path.exists(self.PATH_OTHER)
        self.assertTrue(file_exist1)
        self.assertTrue(file_exist2)

    def test_ffmpeg_processes_no_garbage_left_when_stop(self):
        proc1 = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        proc2 = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH_OTHER]})
        proc1.act()
        proc2.act()
        time.sleep(0.5)
        FFmpegRunner({"ACTION": [FfmpegActions.STOP], "PATH": [self.PATH]}).act()
        FFmpegRunner({"ACTION": [FfmpegActions.STOP], "PATH": [self.PATH_OTHER]}).act()
        proc_list1 = len(proc1.proc_list)
        proc_list2 = len(proc2.proc_list)
        proc_maper1 = len(proc1.proc_maper.keys())
        proc_maper2 = len(proc1.proc_maper.keys())
        self.assertTrue(proc_list1 == proc_list2 == proc_maper1 == proc_maper2 == 0)

    def test_ffmpeg_can_start_and_stop(self):
        proc = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        running_process = proc.act()
        proc.stop()
        time.sleep(0.5)
        self.assertTrue(len(list(proc.proc_list)) == len(proc.proc_maper.keys()) == 0)
        self.assertEqual(psutil.Process(running_process.pid).status(), 'zombie')

    def test_ffmpeg_can_kill_all(self):
        proc = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        proc.act()
        FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH_OTHER]}).act()
        FFmpegRunner.kill_all()
        time.sleep(0.5)
        self.assertTrue(len(list(proc.proc_list)) == len(proc.proc_maper.keys()) == 0)

    def test_ffmpeg_can_kill_all_with_action(self):
        proc = FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH]})
        proc.act()
        FFmpegRunner({"ACTION": [FfmpegActions.START], "PATH": [self.PATH_OTHER]}).act()
        FFmpegRunner({"ACTION": [FfmpegActions.KILL_ALL], "PATH": ['./']}).act()
        time.sleep(0.5)
        self.assertTrue(len(list(proc.proc_list)) == len(proc.proc_maper.keys()) == 0)

class TestProcessServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_process_can_start(self):
        pass

