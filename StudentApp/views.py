import json
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from User.models import *
from .serializers import *
from .models import *
from TeacherApp . models import *
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404




from django.db.models import Subquery,OuterRef,Q

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        
        try:
            user_profile = UserProfile.objects.get(user=user)
            user_profile_serializer = UserProfileSerializer(user_profile)
            data = {
                "user": user_serializer.data,
                "user_profile": user_profile_serializer.data
            }
            return Response(data)
        except UserProfile.DoesNotExist:
            data = {
                "user": user_serializer.data,
                "user_profile": None
            }
            return Response(data)


class UserDetailsUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):

        print('post')
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        print(user_profile)
        serializer = UserProfileUpdateSerializer(user_profile, data=request.data, partial=True)
        print(serializer)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(course_name__icontains=search_query)
            print(queryset)
        return queryset



class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        queryset = Course.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        course_instance = self.get_object()
        video_instances = Videos.objects.filter(course=course_instance)

        course_serializer = self.get_serializer(course_instance)
        video_serializer = VideoSerializer(video_instances, many=True)

       

        data = {
            'course': course_serializer.data,
            'videos': video_serializer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id, video_id):
        try:
            video = Videos.objects.get(course_id=course_id, id=video_id)
            serializer = VideoSerializer(video)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Videos.DoesNotExist:
            return Response({"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.id
        print(request.user.id)
        
        serializer = OrderSerializer(data=mutable_data)
        
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CheckCoursePurchaseAPIView(APIView):
    def get(self, request, course_id, format=None):
        print(request.user)
        if not request.user:
            return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        order = Orders.objects.filter(user=request.user, course_id=course_id).first()  
        serializers=OrderSerializer(order)  
        
        if order:
            return Response({"purchased": True, 'order_id': order.id ,'order':serializers.data}, status=status.HTTP_200_OK)
        else:
            return Response({"purchased": False}, status=status.HTTP_200_OK)
        

class PurchasedCoursesListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderMycourseSerializer

    def get_queryset(self):
        user = self.request.user
        order=Orders.objects.filter(user=user)
        return order
    


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VideoCommentsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    def get_queryset(self):
        video_id = self.kwargs['video_id']
        comments=Comment.objects.filter(video=video_id).order_by('-id')
        # print(comments)
        return comments 
    


class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=pk)

            comment_text = request.data.get('comment_text')
            print(comment_text)
            if comment_text is not None:
                comment.comment = comment_text
                comment.save()

                return Response({"message": "Comment updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Comment text not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AddReplyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    print('working')
    def post(self, request, comment_id):
        # print(request.data)
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRepliesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        replies = Reply.objects.filter(comment=comment)
        serializer = ReplySerializer(replies, many=True)
        # print(serializer.data)
        return Response(serializer.data)





class ReplyUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        reply = Reply.objects.get(pk=pk)
        try:
            reply = Reply.objects.get(pk=pk)

            reply_text = request.data.get('reply_text')
            print(reply_text)
            if reply_text is not None:
                reply.reply_text = reply_text
                reply.save()

                return Response({"message": "reply updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "reply text not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({"error": "reply not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import OrderSerializer

env = environ.Env()

environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    price = request.data['amount']
    course_id = request.data['course']
    user_id= request.data['user_id']

    course = Course.objects.get(pk=course_id)
    user = User.objects.get(pk=user_id)

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    payment = client.order.create({"amount": int(price) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    order = Orders.objects.create(user=user,course=course, 
                                 price=price
                               )

    serializer = OrderSerializer(order)


    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


















