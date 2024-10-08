from django.urls import path
from baseball.views import BaseballStatsView, PlayerDescriptionView, UpdateStatsView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('players/', BaseballStatsView.as_view(), name="players_list"),
    path('players/<int:id>/', PlayerDescriptionView.as_view(), name="player_description"),
    path('players/<int:id>/update-stats', UpdateStatsView.as_view(), name="update_player_stats"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
