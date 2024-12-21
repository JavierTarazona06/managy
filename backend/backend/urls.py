from django.contrib import admin
from django.urls import path, include
#from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users import views as userView


urlpatterns = [
    path("admin/", admin.site.urls),
    #path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("users/view/", userView.UserListView.as_view(), name="user-view"),
    path("users/delete/<int:pk>/", userView.UserDeleteView.as_view(), name="user-delete"),
    #path("users/register/worker/", userView.CreateUserWorkerView.as_view(), name="register-worker"),
    #path("users/register/member/", userView.CreateUserMemberView.as_view(), name="register-member"),
    path("users/register/admin/", userView.CreateUserAdminView.as_view(), name="register-member"),
    path("users/admin/createuser/", userView.UserFromAdminView.as_view(), name="users-from-admin"),
    path("users/admin/deleteuser/<int:pk>/", userView.DelUserFromAdminView.as_view(), name="delusers-from-admin"),

#-----------------------------------------------------------------------
#---------------- JAVIER - elr490 --------------------------------------
#-----------------------------------------------------------------------

    path("user/admin/createuserbatch/", userView.UserFromAdminBatchView.as_view(), name="create-users-batch"),

    path("user/resetpassword/", userView.RequestPasswordReset.as_view(), name="reset-password-token"),
    path("user/changepassword/<slug:token>/", userView.ResetPassword.as_view(), name="reset-password"),
    path("user/getinfo/", userView.UserGetView.as_view(), name="get-user-info"),

    path("users/admin/deleteuserBatch/", userView.DelUserAdminBatch.as_view(), name="delusers-from-admin-batch")
]