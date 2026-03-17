from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('players', PlayerViewSet)
router.register('routes', RouteViewSet)
router.register('checkpoints', CheckpointViewSet)
router.register('sessions', GameSessionViewSet)

urlpatterns = router.urls