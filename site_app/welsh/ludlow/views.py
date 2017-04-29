from django.contrib.auth.models import User
from rest_framework import status, permissions, authentication

from rest_framework import viewsets, response, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from welsh.ludlow.models import Course, Profile
from welsh.ludlow.operations import UserAction
from welsh.ludlow.permissions import IsOwnerOnly
from welsh.ludlow.serializers import CourseSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return Response(UserSerializer(request.user, context={'request': request}).data)
        return super().retrieve(request, pk)

    def list(self, request, *args, **kwargs):
        queryset = User.objects.get(id=request.user.id)
        serializer = UserSerializer(queryset, many=False, context={'request': request})
        return Response(data=serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsOwnerOnly, permissions.IsAuthenticated)

    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all().filter(author_id=request.user.id)
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        course = Course.objects.get(id=pk)
        if course:
            serializer = CourseSerializer(course)
            f = serializer.data
            return Response(f)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, pk=None, *args, **kwargs):
        try:
            if pk is None:
                user_profile = Profile.objects.get(user=request.user)
                data = request.data
                course = Course(author=user_profile, name=data['name'])
                course.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            if pk is not None:
                course = Course.objects.get(id=pk)
                data = request.data
                success = UserAction(course, request).result
                if not success:
                    raise Exception("Can't perform operation")
            else:
                pass
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


@api_view()
def start_recording(request):
    return Response({"message": "Start Recording!"})


@api_view()
def stop_recording(request):
    return Response({"message": "Stop Recording!"})


@api_view()
def status_recording(request):
    return Response({"message": "Status Recording!"})
