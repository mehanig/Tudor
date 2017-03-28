from django.conf.urls import url, include
from django.contrib import admin
from django.views import generic
from django.conf.urls.static import static

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    url(r'^courses$', generic.TemplateView.as_view(template_name='main_page.html')),
    url(r'^settings$', generic.TemplateView.as_view(template_name='main_page.html')),
]
