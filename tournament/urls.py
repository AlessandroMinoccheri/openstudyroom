from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<tournament_id>[0-9]+)/$',
        views.about,
        name='view'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/rules/$',
        views.rules,
        name='rules'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/about/$',
        views.about,
        name='about'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/groups/$',
        views.groups_view,
        name='groups'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/calendar/$',
        views.calendar,
        name='calendar'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/calendar-feed/$',
        views.calendar_feed,
        name='calendar_feed'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/calendar/new-event/$',
        views.create_calendar_event,
        name='create_calendar_event'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/about/edit/$',
        views.edit_about,
        name='edit_about'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/games/$',
        views.games_view,
        name='games'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/games/(?P<sgf_id>[0-9]+)$',
        views.games_view,
        name='games'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/brackets/$',
        views.brackets_view,
        name='brackets'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/players/$',
        views.players_view,
        name='players'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/profile/(?P<user_id>[0-9]+)/update/$',
        views.edit_player_profile,
        name='edit_player_profile'
    ),
    url(
        r'^create/$',
        views.TournamentCreate.as_view(success_url='/tournament/list/'),
        name='create'
    ),
    url(
        r'^list/$',
        views.tournament_list,
        name='list'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/calendar/manage/$',
        views.manage_calendar,
        name='manage_calendar'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/settings/$',
        views.manage_settings,
        name='manage_settings'
    ),

    url(
        r'^(?P<tournament_id>[0-9]+)/admin/groups/$',
        views.manage_groups,
        name='manage_groups'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/brackets/$',
        views.manage_brackets,
        name='manage_brackets'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/games/$',
        views.manage_games,
        name='manage_games'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/upload_sgf/$',
        views.upload_sgf,
        name='upload_sgf'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/create-sgf/$',
        views.create_sgf,
        name='create_sgf'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/set-stage/$',
        views.set_stage,
        name='set_stage'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/invite/$',
        views.invite_user,
        name='invite_user'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/admin/quit/$',
        views.remove_players,
        name='remove_players'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/save_players_order/$',
        views.save_players_order,
        name='save_players_order'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/create-group/$',
        views.create_group,
        name='create_group'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/create-bracket/$',
        views.create_bracket,
        name='create_bracket'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/save-groups/$',
        views.save_groups,
        name='save_groups'
    ),
    url(
        r'^create-match/(?P<round_id>[0-9]+)/$',
        views.create_match,
        name='create_match'
    ),
    url(
        r'^delete_match/(?P<round_id>[0-9]+)/$',
        views.delete_match,
        name='delete_match'
    ),
    url(
        r'^create-round/(?P<bracket_id>[0-9]+)/$',
        views.create_round,
        name='create_round'
    ),
    url(
        r'^rename-round/(?P<round_id>[0-9]+)/$',
        views.rename_round,
        name='rename_round'
    ),
    url(
        r'^delete-round/(?P<round_id>[0-9]+)/$',
        views.delete_round,
        name='delete_round'
    ),
    url(
        r'^(?P<tournament_id>[0-9]+)/save-brackets/$',
        views.save_brackets,
        name='save_brackets'
    ),
    url(
        r'^rename-bracket/(?P<bracket_id>[0-9]+)/$',
        views.rename_bracket,
        name='rename_bracket'
    ),
    url(
        r'^delete-bracket/(?P<bracket_id>[0-9]+)/$',
        views.delete_bracket,
        name='delete_bracket'
    ),
    url(
        r'^update-event/(?P<pk>[0-9]+)/$',
        views.TournamentEventUpdate.as_view(),
        name='update_event'
    ),

]
