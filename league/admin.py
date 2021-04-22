from django.contrib import admin
from django.db.models.functions import Lower

from .models import Deck, Week, Player, Table

# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ('discord_id', 'name')
    list_display = ('name', 'signup')
    search_fields = ('name', )
    ordering = (Lower('name'), )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    date_hierarchy = 'week__start'
    ordering = ('-week__start', )
    list_select_related = True
    list_display = ('__str__', 'player1_corp_deck', 'player2_runner_deck', 'player2_corp_deck', 'player1_runner_deck')
    search_fields = ('player1__name', 'player2__name')
    fieldsets = (
            (None, {
                'fields': ('week', 'player1', 'player2')
                }),
            ('Game 1', {
                'fields': ('player1_corp_deck', 'player2_runner_deck'),
                }),
            ('Game 2', {
                'fields': ('player2_corp_deck', 'player1_runner_deck'),
                }),
            )


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'week':
            kwargs['queryset'] = Week.objects.order_by('-start')
        if db_field.name.endswith('corp_deck'):
            kwargs['queryset'] = Deck.objects.filter(side='corp')
        if db_field.name.endswith('runner_deck'):
            kwargs['queryset'] = Deck.objects.filter(side='runner')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'side', 'faction')
    list_filter = ('side', 'faction')
    ordering = ('name', )

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    pass
