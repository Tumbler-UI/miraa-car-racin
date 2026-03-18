from rest_framework.routers import DefaultRouter, path
from .views import *
from .views import signup, start_race, finish_race

router = DefaultRouter()
router.register('players', PlayerViewSet)
router.register('routes', RouteViewSet)
router.register('checkpoints', CheckpointViewSet)
router.register('sessions', GameSessionViewSet)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('start-race/', start_race),
    path('finish-race/', finish_race),
] + router.urls

