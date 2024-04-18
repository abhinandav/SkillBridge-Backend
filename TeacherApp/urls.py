from .views import *
from django.urls import path


urlpatterns = [
   path('add_course/', AddCourseView.as_view(), name='add_course'),
   path('add_video/', AddVideoView.as_view(), name='add_video'),
   path('my_courses/', MyCoursesListView.as_view(), name='my_courses'),
   path('edit_course/<int:id>/', EditCourseView.as_view(), name='my_courses'),
   path('edit_video/<int:id>/', VideoDetailView.as_view(), name='edit_video'),
   path('course_status/<int:id>/', CourseStatusChangeView.as_view(), name='course_status'),

   path('tprofile_orderdata/',TeacherDashboardData.as_view()),

   # graph
   path('teacher_graph_month/',TeacherOrdersGraphView.as_view()),


]