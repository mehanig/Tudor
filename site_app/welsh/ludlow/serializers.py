from rest_framework import serializers

from django.contrib.auth.models import User

from welsh.ludlow.models import Course, Lesson


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class CourseSerializer(serializers.ModelSerializer):

    lessons = serializers.SerializerMethodField('get_course_lessons')
    key = serializers.SerializerMethodField('get_id_as_key')

    def get_course_lessons(self, obj):
        return [{'name': o.name,
                 'local_path': o.local_path,
                 'parent_name': o.parent_name,
                 'steps': [{'name': s.name,
                            'local_path': s.local_path,
                            'parent_name': s.parent_name,
                            'substeps': [{'name': ss.name,
                                          'local_path': ss.local_path,
                                          'parent_name': ss.parent_name,
                                          'substep_screen': ss.has_substep_screen,
                                          'substep_camera': ss.has_substep_camera
                            } for ss in s.substeps],
                           } for s in o.steps]} for o in obj.lessons]

    def get_id_as_key(self, obj):
        return obj.id

    class Meta:
        model = Course
        fields = ('id', 'key', 'author', 'name', 'lessons')


class LessonSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField('get_lesson_steps')

    def get_lesson_steps(self, obj):
        return "OK"

    class Meta:
        model = Lesson
        fields = ('steps',)
