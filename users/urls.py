from django.urls import path
from . import views
urlpatterns = [
    path("register/", views.register, name="register"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("profile/", views.profile, name="profile"),
    path("sign_out/", views.sign_out, name="sign_out")
]
