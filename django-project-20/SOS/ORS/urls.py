from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index),
    path('<page>/', views.action),
    path('<page>/<operation>/<int:id>', views.action),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),

]