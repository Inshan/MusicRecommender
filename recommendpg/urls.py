from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='reco-home'),
    # path('recopage/', views.recommend,name='recopage'),
]
