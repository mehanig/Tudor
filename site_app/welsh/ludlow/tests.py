from django.test import TestCase
import shutil, tempfile, os

from welsh.ludlow.models import *
from welsh.ludlow.const import *


class TestExample(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test_user@example.com', 'test_pass')
        self.profile = Profile(user=self.user)
        self.SERVER_PATH_ROOT = tempfile.mkdtemp()
        self.course_name = 'TestCourse'
        self.course_path = os.path.join(self.SERVER_PATH_ROOT, self.profile.user.username, self.course_name)
        os.makedirs(self.course_path)

        # Create 2 lessons, 1 empty, 1 with 2 steps ( 1 empty and one with 3 substeps
        # (1 empty, 1 with screen and one with camera ))
        self.lesson_list = ['test_lesson_empty', 'test_lesson_with_content']
        self.lesson_with_content = self.lesson_list[1]
        for i in [os.path.join(self.course_path, lesson) for lesson in self.lesson_list]:
            os.makedirs(i)
        self.step_list = ['test_step_empty', 'test_step_with_content']
        self.step_with_content = self.step_list[1]
        for i in [os.path.join(self.course_path, self.lesson_with_content, step) for step in self.step_list]:
            os.makedirs(i)
        self.substep_list = ['test_substep_empty', 'test_substep_screen', 'test_substep_camera']
        self.substep_screen = self.substep_list[1]
        self.substep_camera = self.substep_list[2]
        for i in [os.path.join(self.course_path, self.lesson_with_content, self.step_with_content, substep)
                          for substep in self.substep_list]:
            os.makedirs(i)
        open(os.path.join(self.course_path, self.lesson_with_content, self.step_with_content, self.substep_camera, SUBSTEP_CAMERA_NAME), 'a')
        open(os.path.join(self.course_path, self.lesson_with_content, self.step_with_content, self.substep_screen, SUBSTEP_SCREEN_NAME), 'w').close()

    def tearDown(self):
        shutil.rmtree(self.SERVER_PATH_ROOT)

    def test_course_is_ok(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            course = Course(author=self.profile, name=self.course_name)
            self.assertEqual(course.local_path, self.course_path)
            self.assertEqual(course.author, self.profile)
            self.assertEqual(course.name, self.course_name)

    def test_lessons_is_ok(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            course = Course(author=self.profile, name=self.course_name)
            self.assertEqual(len(course.lessons), 2)
            for l in course.lessons:
                self.assertTrue(l.local_path in [os.path.join(course.local_path, l_path) for l_path in self.lesson_list])

    def test_steps_and_substeps_is_ok(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            course = Course(author=self.profile, name=self.course_name)
            self.assertEqual(len(course.lessons), 2)
            non_empty_lesson = None
            for l in course.lessons:
                self.assertIn(len(l.steps), [0,2])
                if len(l.steps) == 2:
                    non_empty_lesson = l
            self.assertIsNotNone(non_empty_lesson)
            non_empty_step = None
            for s in non_empty_lesson.steps:
                self.assertIn(len(s.substeps), [0, 3])
                if len(s.substeps) == 3:
                    non_empty_step = s
            self.assertIsNotNone(non_empty_step)
            succ_but_mask = 0
            for ss in non_empty_step.substeps:
                if ss.has_substep_screen:
                    succ_but_mask += 1
                elif ss.has_substep_camera:
                    succ_but_mask += 3
                else:
                    succ_but_mask += 5
            self.assertEqual(succ_but_mask, 9)

    def test_rename_objects(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            course = Course(author=self.profile, name=self.course_name)
            lesson = course.lessons[0]
            items = len(lesson.steps)
            lesson._add_child('new_added_lesson')
            self.assertEqual(len(lesson.steps), items+1)
