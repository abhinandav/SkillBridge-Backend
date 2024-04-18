from . import views
from django.urls import path


urlpatterns = [
    path('users/', views.AdminUserListCreateView.as_view(), name='users'),
    path('users/status/<int:pk>/', views.AcceptUserView.as_view(), name='accept_teachers_view'),

    path('teachers/', views.AdminUserListCreateView.as_view(), name='teachers'),
    path('teachers/accept/<int:pk>/', views.AcceptUserView.as_view(), name='accept_teachers_view'),
    path('teacher_detail/<int:pk>/', views.AdminTeacherListView.as_view(), name='teacher_detail'),
    path('document_status/<int:id>/', views.TeacherDocumentStatusChangeView.as_view(), name='update_documents'),


    path('courses/', views.AdminCourseListCreateView.as_view(), name='courses'),
    path('course_status/<int:id>/', views.CourseStatusChangeView.as_view(), name='course_status'),
    path('video_status/<int:id>/', views.VideoStatusChangeView.as_view(), name='video_status'),

    path('orders2/', views.AdminOrderList2.as_view(), name='orders2'),
    path('orders/', views.AdminOrderList.as_view(), name='orders'),


    # graph
    path('admin_home/', views.AdminDashboardCount.as_view()),
    path('order_graph/', views.OrdersGraphView.as_view()),
    path('order_graph_year/', views.OrderGraphYearView.as_view()),
    path('order_graph_week/', views.OrdersByWeekView.as_view()),

    #sales report
    path('todays_report/',views.TodaysSalesReportView.as_view()),
    path('monthly_report/',views.MonthlySalesReportView.as_view()),
    path('monthly_report/',views.MonthlySalesReportView.as_view()),
    path('weekly_report/',views.WeeklySalesReportView.as_view()),
    path('yearly_report/',views.YearlySalesReportView.as_view()),
    path('custom_report/',views.CustomGenerateReport.as_view()),
]

