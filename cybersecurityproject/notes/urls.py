from django.urls import path

from .views import index, addView, homePageView

urlpatterns = [
    path("", homePageView, name="home"),
    path('add/',addView,name='add')
]