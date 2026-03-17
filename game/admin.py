from django.contrib import admin
from .models import Player, Route, Checkpoint, GameSession

admin.site.register(Player)
admin.site.register(Route)
admin.site.register(Checkpoint)
admin.site.register(GameSession)
