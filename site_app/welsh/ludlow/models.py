import os
from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from .const import *


class ServerFileSystemFolder:
    def __init__(self, local_path, SubFoldersItemsClassName=None, attr_name=None, parent=None):
        self.local_path = local_path
        self._className = SubFoldersItemsClassName
        self._attr_name = attr_name
        self.name = os.path.basename(os.path.normpath(local_path))
        self.parent_name = parent.name
        if SubFoldersItemsClassName is not None:
            setattr(self, attr_name, [SubFoldersItemsClassName(local_path, parent=self) for local_path in filter(os.path.isdir,
                             [os.path.join(self.local_path, item_path) for item_path in os.listdir(self.local_path)])])

    def rename(self, new_name):
        os.rename(src=self.local_path, dst=os.path.join(os.path.dirname(self.local_path), new_name))

    @classmethod
    def rename_in_course(cls, course, old_path, new_path):
        if old_path.startswith(course.local_path) and new_path.startswith(course.local_path):
            if not os.path.exists(new_path) and os.path.exists(old_path):
                os.rename(src=old_path, dst=new_path)
                return True
            else:
                print("Problem with path existence")
                return False
        else:
            print("Paths are inconsistent or not related to Course")
            return False

    def _add_child(self, name):
        if not os.path.exists(os.path.join(self.local_path, name)):
            os.makedirs(os.path.join(self.local_path, name))
            self._update_childs()

    def _update_childs(self):
        if self._className is not None and self._attr_name is not None:
            setattr(self, self._attr_name, [self._className(local_path, parent=self) for local_path in filter(os.path.isdir,
                [os.path.join(self.local_path, item_path) for item_path in os.listdir(self.local_path)])])

    def add(self, name):
        return self._add_child(name)

    def __repr__(self):
        return self.__class__.__name__ + ' : at' + str(self.local_path)

    def __str__(self):
        return self.__repr__()


class Lesson(ServerFileSystemFolder):
    def __init__(self, local_path, parent=None):
        super().__init__(local_path, Step, 'steps', parent=parent)


class Step(ServerFileSystemFolder):
    def __init__(self, local_path, parent=None):
        super().__init__(local_path, SubStep, 'substeps', parent=parent)


class SubStep(ServerFileSystemFolder):
    def __init__(self, local_path, parent=None):
        super().__init__(local_path, None, parent=parent)
        self.has_substep_screen = os.path.exists(os.path.join(self.local_path, SUBSTEP_SCREEN_NAME))
        self.has_substep_camera = os.path.exists(os.path.join(self.local_path, SUBSTEP_CAMERA_NAME))

    def __repr__(self):
        return 'SubStep : ' + ' at ' + str(self.local_path)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return 'Profile: ' + str(self.user)


class Course(models.Model):
    author = models.ForeignKey(Profile, null=False, blank=False)
    name = models.CharField(max_length=256, db_index=True)

    # Dont touch, it will be OK by default
    # TODO: TEST IT!
    rel_path = models.CharField(max_length=512, blank=True)

    @property
    def local_path(self):
        return os.path.join(settings.SERVER_PATH_ROOT, str(self.author.user.username), self.rel_path, self.name)

    @property
    def lessons(self):
        return [Lesson(full_item_path, parent=self) for full_item_path in
                filter(os.path.isdir, [os.path.join(self.local_path, item_path) for item_path in os.listdir(self.local_path)])]

    def __repr__(self):
        return 'Course : ' + str(self.name) + ' at ' + str(self.local_path)

    def __str__(self):
        return self.__repr__()

    def save(self, *args, **kwargs):
        if Course.objects.filter(author=self.author).filter(name=self.name).count() == 0:
            super(Course, self).save(*args, **kwargs)
        else:
            raise ValidationError('Course already exist')
