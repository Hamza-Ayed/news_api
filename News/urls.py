from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, PostViewSet, CommentViewSet
from .views import (
    NewsList,
    Sport360,
    NewsDeleteAll,
    NewsDetailView,
    WordPress, beinSports, youm7sport, dawriSaudi,
    GoalNewsAdd, UserViewSet,CommentUserView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # path('posts/', views.PostList.as_view(), name='post-list'),
    # path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    # path('comments/', views.CommentList.as_view(), name='comment-list'),
    # path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('wcomments/users', CommentUserView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
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
