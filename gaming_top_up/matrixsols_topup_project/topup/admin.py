from django.contrib import admin
from .models import Game, TopUpProduct, TopUpOrder

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_id', 'is_active')
    search_fields = ('name', 'game_id')


@admin.register(TopUpProduct)
class TopUpProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_game_currency', 'game')
    search_fields = ('name', 'game__name')
    list_filter = ('game',)


@admin.register(TopUpOrder)
class TopUpOrderAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user_email',)
