
from django.urls import path
from .views import *


urlpatterns = [
 path('ordercourse_teachers/',OrderWithUserView.as_view()),
 path('created_teacher/<int:oid>/', TeacherRecieverView.as_view()),
 path('chat-messages/<int:oid>/', OrderChatMessagesAPIView.as_view()),
 path('users_messaged_teacher/', UsersMessagedTeacher.as_view(), name='users_messaged_teacher'),
 path('buyed_user/<int:oid>/', UserRecieverView.as_view()),
] 