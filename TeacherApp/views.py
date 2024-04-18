import os
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course
from .serializers import *
from rest_framework.permissions import IsAuthenticated 
from rest_framework import generics
from Adminapp.serializers import *
import cv2 
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.generic import View
from StudentApp.models import Orders
from django.db.models import Count, Sum, FloatField, Value
from django.utils.timezone import now
from django.db.models.functions import TruncMonth, TruncYear, Cast




class AddCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data['added_by'] = request.user.id
        
        serializer = CourseSerializer(data=mutable_data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddVideoView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Save the uploaded video to a temporary file
            video_file = request.data['video']
            with open('temp_video.mp4', 'wb') as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)

            # Read the video file and extract duration
            video_capture = cv2.VideoCapture('temp_video.mp4')
            frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            duration_seconds = round(frames / fps)
            video_duration = timedelta(seconds=duration_seconds)  # Use timedelta from datetime module
            print(video_duration)
            video_capture.release()

            # Delete the temporary video file
            os.remove('temp_video.mp4')

            # Create serializer instance with duration information
            serializer = VideosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(duration=video_duration)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 

# class AddVideoView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             # Save the uploaded video to a temporary file
#             video_file = request.data['video']
#             with open('temp_video.mp4', 'wb') as temp_file:
#                 for chunk in video_file.chunks():
#                     temp_file.write(chunk)

#             # Read the video file and extract duration
#             video_capture = cv2.VideoCapture('temp_video.mp4')
#             frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
#             fps = video_capture.get(cv2.CAP_PROP_FPS)
#             duration_seconds = round(frames / fps)
#             video_duration = datetime.timedelta(seconds=duration_seconds)
#             print(video_duration)
#             video_capture.release()

#             # Delete the temporary video file
#             os.remove('temp_video.mp4')

#             # Create serializer instance with duration information
#             serializer = VideosSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(duration=video_duration)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print(e)
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyCoursesListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            c=Course.objects.filter(added_by_id=user.id)
            print(c)
            return Course.objects.filter(added_by_id=user.id)
        else:
            print('s')
            return Course.objects.none() 


class EditCourseView(APIView):
    def post(self, request, id):
        course = Course.objects.get(pk=id)
        mutable_data = request.data.copy()
        mutable_data['added_by'] = request.user.id
        serializer = CourseSerializer(course, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VideoDetailView(APIView):
    print('working')
    def get(self, request, id):
        try:
            video = Videos.objects.get(id=id)
            serializer = VideosSerializer(video)
            return Response(serializer.data)
        except Videos.DoesNotExist:
            return Response({"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            video = Videos.objects.get(id=id)
        except Videos.DoesNotExist:
            return Response({"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideosSerializer(video, data=request.data)
       
        
        if serializer.is_valid():
            serializer.save()
            course = video.course
            course.is_accepted = False
            course.save()


            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CourseStatusChangeView(APIView):
    def patch(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, id=id)

        if 'is_blocked' in request.data:
            course.is_blocked = request.data['is_blocked']

        course.save()

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class TeacherDashboardData(APIView):
    def get(self,request):
        teacher=request.user.id
        orders=Orders.objects.filter(course__added_by=teacher)
        total_orders=orders.count()

        total_students=orders.values('user').distinct().count()

        total_course=Course.objects.filter(added_by=teacher).count()

        total_amount = orders.annotate(price_float=Cast('price', FloatField())).aggregate(
            total_price=Sum('price_float')
        )['total_price']

        serializer=OrderListSerializer(orders,many=True)

        data={
            'total_course':total_course,
            'total_order':total_orders,
            'total_students':total_students,
            'total_amount':total_amount,
            'orders':serializer.data
        }

        # print(data)
        return Response(data,status=status.HTTP_200_OK)
    





class TeacherOrdersGraphView(APIView):
    def get(self, request):
        six_months_ago = now() - timedelta(days=30*6)
        print('user',request.user)
        
       
        user_courses = Course.objects.filter(added_by=request.user.id)
        print('user_courses',user_courses)
        orders = Orders.objects.filter(course__in=user_courses, date_purchased__gte=six_months_ago)

        print('orders',orders)

        monthly_orders = orders.annotate(
            year_month=TruncMonth('date_purchased')
        ).values('year_month').annotate(
            total_orders=Count('id')
        ).order_by('year_month')
        orders_data = [
            {
                'year_month': order['year_month'].strftime('%Y-%m'),
                'total_orders': order['total_orders']
            }
            for order in monthly_orders
        ]

        print(orders_data)

        return JsonResponse(orders_data, safe=False)