from django.urls import path
from .views import (
    NewsList,
    Sport360,
    NewsDeleteAll,
    NewsDetailView,
    WordPress,beinSports,youm7sport,dawriSaudi,
    GoalNewsAdd,
)

urlpatterns = [
    path("news/", NewsList.as_view()),
    path("news/goal", GoalNewsAdd.as_view()),
    path("news/dawriSaudi",dawriSaudi.as_view()),
    path("news/youm7", youm7sport.as_view()),
    path("news/beinsport", beinSports.as_view()),
    path("news/360", Sport360.as_view()),
    path("news/delete-all/", NewsDeleteAll.as_view(), name="news-delete-all"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news-detail"),
    path("wordpress/", WordPress.as_view(), name="wordpress-list"),
]
