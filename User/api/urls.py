# urls.py
from django.urls import path
from .views import *
from User.api.serializers import MyTokenObtainPairSerializer 


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     path('token/', TokenObtainPairView.as_view(serializer_class=MyTokenObtainPairSerializer), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("",getAccountsRoutes.as_view(), name="accounts-routes"),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='login'),
    path('userotp/', OTPVerificationView.as_view(),name='userotp'),
    path('resendotp/', ResendOTPView.as_view(),name='resendotp'),
    path('deleteotp/', DeleteOTPView.as_view(),name='deleteotp'),
    path("user/details/", UserDetails.as_view(), name="user-details"),
    path('forgotpassword/', ForgotPassword.as_view(), name='forgotpassword'),
    path('change_password/<int:id>/', ChangePasswordAPIView.as_view(), name='forgotpassword'),
    # path('decode_hash/', DecodeHash.as_view(), name='decode_hash'),





    path('teacher/teacher_signup/', TeacherRegisterView.as_view(), name='teacher_signup'),
    path('teacher/teacher_login/', TeacherLoginView.as_view(), name='teacher_login'),
    path('teacher/teacher_details/', TeacherDetailsView.as_view(), name='teacher_details'),
    path('teacher/teacher_documents/', TeacherDocumentView.as_view(), name='teacher_documents'),



    path('admin/admin_login/', AdminLoginView.as_view(), name='admin_login'),
]

