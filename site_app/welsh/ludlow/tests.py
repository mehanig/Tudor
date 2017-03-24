from django.test import TestCase
import shutil, tempfile, os

from rest_framework.authtoken.models import Token

from welsh.ludlow.models import *
from welsh.ludlow.const import *
from welsh.ludlow.views import CourseViewSet, UserViewSet

from rest_framework.test import APIClient
from rest_framework import status


# TODO: Make it ClassMethod for BaseClass
def _gen_course_structure(testClass):
    testClass.lesson_list = ['test_lesson_empty', 'test_lesson_with_content']
    testClass.lesson_with_content = testClass.lesson_list[1]
    for i in [os.path.join(testClass.course_path, lesson) for lesson in testClass.lesson_list]:
        os.makedirs(i)
    testClass.step_list = ['test_step_empty', 'test_step_with_content']
    testClass.step_with_content = testClass.step_list[1]
    for i in [os.path.join(testClass.course_path, testClass.lesson_with_content, step) for step in testClass.step_list]:
        os.makedirs(i)
    testClass.substep_list = ['test_substep_empty', 'test_substep_screen', 'test_substep_camera']
    testClass.substep_screen = testClass.substep_list[1]
    testClass.substep_camera = testClass.substep_list[2]
    for i in [os.path.join(testClass.course_path, testClass.lesson_with_content, testClass.step_with_content, substep) for substep in
              testClass.substep_list]:
        os.makedirs(i)
    open(os.path.join(testClass.course_path, testClass.lesson_with_content, testClass.step_with_content, testClass.substep_camera,
                      SUBSTEP_CAMERA_NAME), 'a')
    open(os.path.join(testClass.course_path, testClass.lesson_with_content, testClass.step_with_content, testClass.substep_screen,
                      SUBSTEP_SCREEN_NAME), 'w').close()



class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test_user@example.com', 'test_pass')
        self.profile = Profile(user=self.user)
        self.SERVER_PATH_ROOT = tempfile.mkdtemp()
        self.course_name = 'TestCourse'
        self.course_path = os.path.join(self.SERVER_PATH_ROOT, self.profile.user.username, self.course_name)
        os.makedirs(self.course_path)

        _gen_course_structure(self)

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

    def test_rename_objects_and_parenting(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            course = Course(author=self.profile, name=self.course_name)
            lesson = course.lessons[0]
            items = len(lesson.steps)
            lesson._add_child('new_added_step')
            self.assertEqual(len(lesson.steps), items+1)
            self.assertEqual(lesson.steps[-1].name, 'new_added_step')

            step = lesson.steps[0]
            self.assertEqual(len(step.substeps), 0)
            step._add_child('new_added_substep')
            self.assertEqual(len(step.substeps), 1)
            self.assertEqual(step.substeps[-1].name, 'new_added_substep')

            self.assertEqual(step.substeps[-1].parent_name, 'new_added_step')
            self.assertEqual(step.parent_name, lesson.name)


# TODO! REWRITE URLS TO reverse

class TestAPIPermissions(TestCase):
    def setUp(self):
        password = 'mypassword'
        self.test_user = User.objects.create(username='myuser', email='myuser@test.com', password=password)
        token = Token.objects.get(user__username=self.test_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.SERVER_PATH_ROOT = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.SERVER_PATH_ROOT)

    def test_not_allowed_for_not_logged(self):
        unauthorized_client = APIClient()
        for r in ['/api/courses/', '/api/courses/1/', '/api/users/', '/api/users/1/', '/api/users/i/']:
            res = unauthorized_client.get(r)
            self.assertEqual(res.status_code,  status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_is_correct(self):
        token = Token.objects.get(user__username=self.test_user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.get('/api/users/i/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.test_user.username)

    def test_authorized_user_can_see_only_self(self):
        res = self.client.get('/api/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.test_user.username)
        res = self.client.get('/api/users/{user}/'.format(user=self.test_user.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.test_user.username)

    def test_can_create_course_correct(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            token = Token.objects.get(user__username=self.test_user)
            client = APIClient()
            data = {'name': 'test_course'}
            res = self.client.post('/api/courses/', data, format='json')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            res = self.client.get('/api/courses/')
            self.assertEqual(res.data[0]['name'], 'test_course')


class TestCourseActions(TestCase):
    def setUp(self):
        password = 'mypassword'
        self.test_user = User.objects.create(username='myuser', email='myuser@test.com', password=password)
        self.test_user.save()
        self.profile = Profile.objects.get(user=self.test_user)
        token = Token.objects.get(user__username=self.test_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.SERVER_PATH_ROOT = tempfile.mkdtemp()

        self.course_name = 'TestCourse'
        self.course_path = os.path.join(self.SERVER_PATH_ROOT, self.test_user.username, self.course_name)
        os.makedirs(self.course_path)

        _gen_course_structure(self)

        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            self.course = Course(author=self.profile, name=self.course_name)
            self.course.save()

    def tearDown(self):
        shutil.rmtree(self.SERVER_PATH_ROOT)
        self.test_user.delete()
        self.course.delete()

    def test_rename_lesson(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            old_path = self.course.lessons[0].local_path
            data = {"action": "rename",
                    "old_path": old_path,
                    "new_path": old_path + "_new"}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(self.course.lessons[0].local_path, old_path + '_new')

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.course.lessons[0].local_path, old_path + '_new')

    def test_rename_step(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            old_path = self.course.lessons[1].steps[1].local_path
            data = {"action": "rename",
                    "old_path": old_path,
                    "new_path": old_path + "_new"}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(self.course.lessons[1].steps[1].local_path, old_path + '_new')

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.course.lessons[1].steps[1].local_path, old_path + '_new')

    def test_rename_substep(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            old_path = self.course.lessons[1].steps[1].substeps[1].local_path
            data = {"action": "rename",
                    "old_path": old_path,
                    "new_path": old_path + "_new"}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(self.course.lessons[1].steps[1].substeps[1].local_path, old_path + '_new')

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.course.lessons[1].steps[1].substeps[1].local_path, old_path + '_new')

    def test_add_lesson(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            course_path = self.course.local_path
            new_lesson_name = "new_created_lesson"
            data = {"action": "add",
                    "new_path":  os.path.join(course_path, new_lesson_name)}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)

            self.assertIn(new_lesson_name, [l.name for l in self.course.lessons])

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(new_lesson_name, [l.name for l in self.course.lessons])

    def test_add_step(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            lesson_path = self.course.lessons[0].local_path
            new_step_name = "new_created_step"
            data = {"action": "add",
                    "new_path":  os.path.join(lesson_path, new_step_name)}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)

            self.assertIn(new_step_name, [s.name for s in self.course.lessons[0].steps])

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(new_step_name, [s.name for s in self.course.lessons[0].steps])

    def test_add_substep(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            step_path = self.course.lessons[1].steps[0].local_path
            new_substep_name = "new_created_substep"
            data = {"action": "add",
                    "new_path":  os.path.join(step_path, new_substep_name)}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)

            self.assertIn(new_substep_name, [s.name for s in self.course.lessons[1].steps[0].substeps])

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(new_substep_name, [s.name for s in self.course.lessons[1].steps[0].substeps])

    def test_delete_lesson(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            lesson_path = self.course.lessons[0].local_path
            lesson_name = self.course.lessons[0].name
            lesson_prefix_in_trash_bin = self.course.name + "_" + lesson_name
            data = {"action": "delete",
                    "path":  lesson_path}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertNotIn(lesson_path, [l.local_path for l in self.course.lessons])

            trash_bin_path = os.path.join(self.course.author.local_path, TRASH_BIN)
            trash_bin_files = os.listdir(trash_bin_path)
            self.assertTrue(any([l.startswith(lesson_prefix_in_trash_bin) for l in trash_bin_files]))

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn(lesson_path, [l.local_path for l in self.course.lessons])

    def test_delete_step(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            step_path = self.course.lessons[1].steps[0].local_path
            step_name = self.course.lessons[1].steps[0].name
            step_prefix_in_trash_bin = self.course.name + "_" + step_name
            data = {"action": "delete",
                    "path":  step_path}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertNotIn(step_path, [l.local_path for l in self.course.lessons[1].steps])

            trash_bin_path = os.path.join(self.course.author.local_path, TRASH_BIN)
            trash_bin_files = os.listdir(trash_bin_path)
            self.assertTrue(any([s.startswith(step_prefix_in_trash_bin) for s in trash_bin_files]))

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn(step_path, [s.local_path for s in self.course.lessons[1].steps])

    def test_delete_substep(self):
        with self.settings(SERVER_PATH_ROOT=self.SERVER_PATH_ROOT):
            substep_path = self.course.lessons[1].steps[1].substeps[0].local_path
            substep_name = self.course.lessons[1].steps[1].substeps[0].name
            substep_prefix_in_trash_bin = self.course.name + "_" + substep_name
            data = {"action": "delete",
                    "path":  substep_path}
            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertNotIn(substep_path, [l.local_path for l in self.course.lessons[1].steps[1].substeps])

            trash_bin_path = os.path.join(self.course.author.local_path, TRASH_BIN)
            trash_bin_files = os.listdir(trash_bin_path)
            self.assertTrue(any([l.startswith(substep_prefix_in_trash_bin) for l in trash_bin_files]))

            res = self.client.put('/api/courses/{course_id}/'.format(course_id=self.course.id), data, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn(substep_path, [l.local_path for l in self.course.lessons[1].steps[1].substeps])

