from django.contrib.auth.models import User

from rest_framework import viewsets, response, permissions
from rest_framework.response import Response

from welsh.ludlow.models import Course
from welsh.ludlow.serializers import CourseSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return Response(UserSerializer(request.user, context={'request': request}).data)
        return super().retrieve(request, pk)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data)
