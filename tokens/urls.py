from django.urls import path


from tokens.views import  (
    DecoratedTokenObtainPairView,
    DecoratedTokenVerifyView,
    getroutes,
    DecoratedTokenRefreshView,
    DecoratedTokenBlacklistView)

urlpatterns = [
    path("",getroutes),
    path("token/",DecoratedTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path("token/refresh/",DecoratedTokenRefreshView.as_view(),name='token_refresh'),
    path("token/blacklist/",DecoratedTokenBlacklistView.as_view(),name="token_blacklist"),
    path("token/verify/",DecoratedTokenVerifyView.as_view(),name="token_verify")
]