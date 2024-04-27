from .views import *
from django.urls import path

urlpatterns=[
    path("user_details/", UserDetails.as_view(), name="user_details"),
    path('profile_update/', UserDetailsUpdate.as_view(), name='profile_update'),
    path('courses/',CourseListCreateAPIView.as_view(),name='courses'),
    path('course_view/<int:id>/', CourseDetailView.as_view(), name='course-detail'),

    path('order/',OrderCreateAPIView.as_view(),name='order'),
    path('purchased/<int:course_id>/',CheckCoursePurchaseAPIView.as_view(),name='purchased'),
    path('enrolled_courses/',PurchasedCoursesListAPIView.as_view(),name='enrolled_courses'),

    path('courses/<int:course_id>/videos/<int:video_id>/', VideoDetailView.as_view(), name='video-detail'),

    path('add_comment/',CommentCreateView.as_view(),name='add_comment'),
    path('video_comments/<int:video_id>/', VideoCommentsView.as_view(), name='video_comments'),

    path('comments/<int:comment_id>/add_reply/',AddReplyAPIView.as_view(),name='add_reply'),
    path('comments/<int:comment_id>/replies/',GetRepliesAPIView.as_view(),name='get_reply'),
    path('edit_comment/<int:pk>/',CommentUpdateView.as_view()),
    path('edit_reply/<int:pk>/',ReplyUpdateView.as_view()),



    path('view_status/<int:id>/', MarkVideoAsWatched.as_view(), name='view_status'),
    path('check_all_videos_watched/<int:course_id>/', CheckAllVideosWatched.as_view(), name='check_all_videos_watched'),
    path('certificate/',CertificateView.as_view()),
    path('viewed_videos/',ViewedVideos.as_view()),


    path('pay/', start_payment, name="payment"),


]











#     path('my-messages/<user_id>/',MyInbox.as_view(),name='my-messages'),
#     path('get-messages/<sender_id>/<reciever_id>/',GetMessages.as_view(),name='get-messages'),
#     path('send-message/',SendMessage.as_view(),name='send-message'),


# # get/filter data
#     path('profile/<int:pk>/',ProfileDetail.as_view()),
#     path('search/<username>/',SearchUser.as_view()),
