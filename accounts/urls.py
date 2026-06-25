from django.urls import path

from accounts import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.SignInView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("edit-profile/", views.ProfileEditView.as_view(), name="edit_profile"),
    path(
        "change-password/",
        views.PasswordChangeView.as_view(),
        name="change_password",
    ),
    path("list/", views.UserListView.as_view(), name="list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="profile"),
]
