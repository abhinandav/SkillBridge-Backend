import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from User.models import *
from StudentApp.models import *
from TeacherApp.models import *
from User.api.serializers import *
from .serializers import *
from TeacherApp.serializers import *
# from StudentApp.serializers import *
from rest_framework.generics import ListCreateAPIView,ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import AuthenticationFailed,ParseError
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404


from rest_framework import status, permissions
from django.utils import timezone

from .permissions import *


from django.http import JsonResponse
from StudentApp.models import Orders
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth,TruncYear
from django.db.models import Sum
from datetime import datetime, timedelta
from StudentApp.serializers import UserProfileSerializer




#User management 
class AdminUserListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all().order_by('-date_joined')  
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username',  'email'] 

 

#accept user and block / unblock
class AcceptUserView(APIView):
    permission_classes = [IsAdmin]
    def patch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)

        if 'is_email_verified' in request.data:
            user.is_email_verified = True
            UserProfile.objects.get_or_create(user=user)

        elif 'is_active' in request.data:
            user.is_active = request.data['is_active']

        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# teacher management
class AdminTeacherListView(RetrieveAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer  

    def retrieve(self, request, *args, **kwargs):
        user_instance = self.get_object()
        print(user_instance)
        teacher_details_instance = TeacherDetails.objects.get(user=user_instance)
        teacher_documents_instance = TeacherDocument.objects.get(user=user_instance)
        teacher_profile_instance=UserProfile.objects.get(user=user_instance)
        
        user_serializer = self.get_serializer(user_instance)
        teacher_details_serializer = TeacherDetailsSerializer(teacher_details_instance)
        teacher_profile=UserProfileSerializer(teacher_profile_instance)
        teacher_documents_serializer = TeacherDocumentSerializer(teacher_documents_instance)

        data = {
            'user': user_serializer.data,
            'teacher_details': teacher_details_serializer.data,
            'teacher_documents': teacher_documents_serializer.data,
            'teacher_profile':teacher_profile.data
        }

        return Response(data, status=status.HTTP_200_OK)
    




# update documents of teacher
class UpdateTeacherDocuments(APIView):
    permission_classes = [IsAdmin]
    def put(self, request, id, format=None):
        print(id)
        try:
            teacher_document = TeacherDocument.objects.get(pk=id)
            print(teacher_document)
        except TeacherDocument.DoesNotExist:
            print('404...........')
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeacherDocumentSerializer(teacher_document, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDocumentStatusChangeView(APIView):
    permission_classes = [IsAdmin]
    def patch(self, request, id, *args, **kwargs):
        document = get_object_or_404(TeacherDocument, id=id)

        if 'id_verify' in request.data:
            document.id_verify = True
        if 'photo_verify' in request.data:
            document.photo_verify = True
        if 'tenth_verify' in request.data:
            document.tenth_verify = True
        if 'plustwo_verify' in request.data:
            document.plustwo_verify = True
        if 'graduation_verify' in request.data:
            document.graduation_verify = True
        if 'experience_verify' in request.data:
            document.experience_verify = True
       
        
        document.save()

        serializer = TeacherDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# Course Management  
class AdminCourseListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Course.objects.all().order_by('-date_added')  
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter]
    search_fields = ['course_name']


class CourseStatusChangeView(APIView):
    permission_classes = [IsAdmin]
    def patch(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, id=id)

        if 'is_accepted' in request.data:
            course.is_accepted = True
        if 'is_blocked' in request.data:
            course.is_blocked = request.data['is_blocked']



        if 'is_rejected' in request.data:
            print('true')
            course.is_rejected =  True
            course.reject_reason=request.data.get('reason')

        course.save()

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoStatusChangeView(APIView):
    permission_classes = [IsAdmin]
    def patch(self, request, id, *args, **kwargs):
        video = get_object_or_404(Videos, id=id)

        if 'is_accepted' in request.data:
            video.is_accepted = True

        if 'is_rejected' in request.data:
            video.is_rejected=True
            video.rejected_reason=request.data.get('reason') 

        video.save()

        serializer = VideosSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Order Manegement
class CustomPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdminOrderList(ListAPIView):
    permission_classes = [IsAdmin]
    queryset = Orders.objects.all().order_by('-date_purchased')  
    serializer_class = OrderListSerializer
    pagination_class = CustomPagination




# Dashboard
class AdminOrderList2(ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Orders.objects.all().order_by('-date_purchased')  
    serializer_class = OrderListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['course_name']

class AdminDashboardCount(APIView):
    permission_classes = [IsAdmin]
    def get(self,request):
        user_count=User.objects.filter(is_staff=False,is_superuser=False).count()
        teacher_count=User.objects.filter(is_staff=True,is_superuser=False).count()
        course_count=Course.objects.filter(is_accepted=True).count()
        orders=Orders.objects.all().count()
        bolcked_users=User.objects.filter(is_staff=False,is_superuser=False,is_active=False).count()
        blocked_teachers=User.objects.filter(is_staff=True,is_active=False).count()
        blocked_courses=Course.objects.filter(is_accepted=True,is_blocked=True).count()
        videos=Videos.objects.filter().count()
        data={
            'user':user_count,
            'teacher':teacher_count,
            'course':course_count,
            'orders':orders,
            'videos':videos,

            'buser':bolcked_users,
            'bteacher':blocked_teachers,
            'bcourse':blocked_courses
        }
        print(data)
        return Response(data,status=status.HTTP_200_OK)

class OrdersGraphView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        six_months_ago = now() - timedelta(days=30*6)
        orders = Orders.objects.filter(date_purchased__gte=six_months_ago)

        monthly_orders = orders.annotate(
            year_month=TruncMonth('date_purchased')
        ).values('year_month').annotate(
            total_orders=Count('id')
        ).order_by('year_month')

        # Convert queryset to dictionary
        orders_data = [
            {
                'year_month': order['year_month'].strftime('%Y-%m'),
                'total_orders': order['total_orders']
            }
            for order in monthly_orders
        ]
 

        return JsonResponse(orders_data, safe=False)
    
class OrderGraphYearView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        yearly_data = Orders.objects.annotate(
            year=TruncYear('date_purchased')
        ).values('year').annotate(
            total_orders=Count('id')
        ).order_by('year')

        formatted_yearly_data = [{'year_month': item['year'].strftime('%Y'), 'total_orders': item['total_orders']} for item in yearly_data]

        return JsonResponse(formatted_yearly_data, safe=False)
    
class OrdersByWeekView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=1, month=today.month+1) - timedelta(days=1)

        orders = Orders.objects.filter(date_purchased__range=[first_day_of_month, last_day_of_month])

        num_weeks = (last_day_of_month - first_day_of_month).days // 7 + 1

        orders_by_week = {}
        for week_number in range(num_weeks):
            start_of_week = first_day_of_month + timedelta(weeks=week_number)
            end_of_week = min(start_of_week + timedelta(days=6), last_day_of_month)
            week_name = f"Week {week_number + 1}"
            orders_in_week = orders.filter(date_purchased__range=[start_of_week, end_of_week])
            orders_by_week[week_name] = orders_in_week.count()

        return JsonResponse(orders_by_week)




# sales report
class TodaysSalesReportView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        today = timezone.now().date()
        orders_today = Orders.objects.filter(date_purchased=today)
        orders_today_count = Orders.objects.filter(date_purchased=today).count()
        order_list = Orders.objects.filter(date_purchased=today).order_by('-date_purchased') 
        serializer = OrderListSerializer(order_list, many=True)

        total_courses_ordered = orders_today.values('course').distinct().count()

        unique_user_ids = set(order.user.id for order in order_list)
        unique_users_count = len(unique_user_ids)

        total_earnings = sum(int(order.price) for order in orders_today if int(order.price))

        data = {
            'orders_today_count': orders_today_count,
            'users_count': unique_users_count,
            'course_count':total_courses_ordered,
            'order_list': serializer.data,
            'total_earnings': total_earnings,
        }
        return Response(data, status=status.HTTP_200_OK)


class MonthlySalesReportView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=1, month=today.month+1) - timedelta(days=1)

        orders_this_month = Orders.objects.filter(date_purchased__range=(first_day_of_month, last_day_of_month))


        orders_this_month_count = orders_this_month.count()
        total_courses_ordered = orders_this_month.values('course').distinct().count()

        unique_user_ids = set(order.user.id for order in orders_this_month)
        unique_users_count = len(unique_user_ids)

        total_earnings = sum(int(order.price) for order in orders_this_month if order.price.isdigit())

        serializer = OrderListSerializer(orders_this_month.order_by('-date_purchased'), many=True)

      
        data = {
            'orders_this_month_count': orders_this_month_count,
            'users_count': unique_users_count,
            'course_count': total_courses_ordered,
            'order_list': serializer.data,
            'total_earnings': total_earnings,
        }
        return Response(data, status=status.HTTP_200_OK)
    

class YearlySalesReportView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        today = timezone.now().date()
        first_day_of_year = today.replace(month=1, day=1)
        last_day_of_year = today.replace(month=12, day=31)


        orders_this_year = Orders.objects.filter(date_purchased__range=(first_day_of_year, last_day_of_year))

        orders_this_year_count = orders_this_year.count()
        total_courses_ordered = orders_this_year.values('course').distinct().count()

        unique_user_ids = set(order.user.id for order in orders_this_year)
        unique_users_count = len(unique_user_ids)

        total_earnings = sum(int(order.price) for order in orders_this_year if order.price.isdigit())


        serializer = OrderListSerializer(orders_this_year.order_by('-date_purchased'), many=True)

        data = {
            'orders_this_year_count': orders_this_year_count,
            'users_count': unique_users_count,
            'course_count': total_courses_ordered,
            'order_list': serializer.data,
            'total_earnings': total_earnings,
        }
        return Response(data, status=status.HTTP_200_OK)
    

class WeeklySalesReportView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        orders_this_week = Orders.objects.filter(date_purchased__range=(start_of_week, end_of_week))

        orders_this_week_count = orders_this_week.count()
        total_courses_ordered = orders_this_week.values('course').distinct().count()

        unique_user_ids = set(order.user.id for order in orders_this_week)
        unique_users_count = len(unique_user_ids)

        total_earnings = sum(int(order.price) for order in orders_this_week if order.price.isdigit())

        serializer = OrderListSerializer(orders_this_week.order_by('-date_purchased'), many=True)

        data = {
            'orders_this_week_count': orders_this_week_count,
            'users_count': unique_users_count,
            'course_count': total_courses_ordered,
            'order_list': serializer.data,
            'total_earnings': total_earnings,
        }
        return Response(data, status=status.HTTP_200_OK)
    

class CustomGenerateReport(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, *args, **kwargs):
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Query orders based on date range
        orders = Orders.objects.filter(date_purchased__range=(start_date, end_date))
        
        # Calculate statistics
        num_orders = orders.count()
        unique_users = orders.values('user').distinct().count()
        unique_courses = orders.values('course').distinct().count()
        total_price = sum(int(order.price) for order in orders if order.price.isdigit())
  

        # Serialize order data
        order_data = [
            {
                'id': order.id,
                'user': order.user.username,
                'course': order.course.course_name,
                'author':order.course.added_by.username,
                'price': order.price,
                'date_purchased': order.date_purchased,
            }
            for order in orders
        ]

        report_data = {
            'start_date': start_date_str,
            'end_date': end_date_str,
            'num_orders': num_orders,
            'unique_users': unique_users,
            'unique_courses': unique_courses,
            'total_price': total_price,
            'order_data': order_data,
        }
        
        return Response(report_data)