from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spaces.views import PublicSpaceViewSet , PrivateSpaceViewSet , RequestAPIView , RequestStateAPIView , AcceptOrRejectRequestAPIView , SpaceUsersListAPI



router = DefaultRouter()
router.register(r'public' , PublicSpaceViewSet , basename="public")
router.register(r'private' , PrivateSpaceViewSet , basename="private")


urlpatterns = [
    path('', include(router.urls)),
    path('request/' , RequestAPIView.as_view()),
    path('request/<int:pk>/' , RequestStateAPIView.as_view()),
    path('requested/<int:pk>/' , AcceptOrRejectRequestAPIView.as_view()),
    path('users/<str:name>/' , SpaceUsersListAPI.as_view())
]

