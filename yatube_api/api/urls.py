from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import CommentViewSet, GroupViewSet, PostViewSet


app_name = 'api'

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
