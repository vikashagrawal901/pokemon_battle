from django.contrib import admin
from .models import Battle
# Register your models here.

class CustomBattleAdmin(admin.ModelAdmin):
    model=Battle
    list_display=['battle_id', 'pokemon_a', 'pokemon_b', 'status', 'result']

admin.site.register(Battle, CustomBattleAdmin)
