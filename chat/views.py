from User.models import *
from TeacherApp.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Orders
from .serializers import *
from rest_framework import status


from TeacherApp.serializers import CourseSerializer
from .serializers import OrderSerializer

from rest_framework.response import Response
from rest_framework.views import APIView




# user sidebar teacher list


# class OrderWithUserView(APIView):
#     def get(self, request):
#         print('user:',request.user)
#         orders = Orders.objects.filter(user=request.user)
#         print('orders',orders.values())

#         unique_user_ids = set(order.course.added_by_id for order in orders)
#         print('unique_user_ids',unique_user_ids)

#         user_profiles = UserProfile.objects.filter(user_id__in=unique_user_ids)
#         user_profiles_dict = {profile.user_id: profile for profile in user_profiles}

#         unique_orders = []
#         for order in orders:
#             user_profile = user_profiles_dict.get(order.course.added_by_id)
#             if user_profile:
#                 serializer = OrderWithUserSerializer(order)
#                 serialized_order = serializer.data
#                 serialized_order['user_profile'] = {
#                     'profile_pic': str(user_profile.profile_pic),
#                 }
#                 unique_orders.append(serialized_order)
#                 print('unique_orders',unique_orders)


#         return Response(unique_orders)

class OrderWithUserView(APIView):
    def get(self, request):
        orders = Orders.objects.filter(user=request.user)
        unique_orders = {}
        
        for order in orders:
            course_id = order.course.added_by_id
            if course_id not in unique_orders:
                unique_orders[course_id] = order
                
        unique_order_list = []
        for order in unique_orders.values():
            user_profile = UserProfile.objects.get(user_id=order.course.added_by_id)
            serializer = OrderWithUserSerializer(order)
            serialized_order = serializer.data
            serialized_order['user_profile'] = {
                'profile_pic': str(user_profile.profile_pic),
            }
            unique_order_list.append(serialized_order)

        return Response(unique_order_list)


# class OrderWithUserView(APIView):
#     def get(self, request):
#         orders = Orders.objects.filter(user=request.user)
#         unique_usernames = set()
#         unique_orders = []
        
#         for order in orders:
#             username = order.course.added_by.username
#             if username not in unique_usernames:
#                 unique_usernames.add(username)
#                 unique_orders.append(order)

#         # Serialize the unique orders
#         serializer = OrderWithUserSerializer(unique_orders, many=True)
#         print(serializer.data)
#         return Response(serializer.data)
    



class TeacherRecieverView(APIView):
    def get(self, request,oid):
        orders = Orders.objects.filter(pk=oid)  
        course_id = orders.values_list('course_id', flat=True).distinct()
        courses = Course.objects.filter(id__in=course_id)
        added_user = set(course.added_by for course in courses)
        # print('added_user', added_user)

        serializer = UserSerializer(added_user, many=True)
        serialized_data = serializer.data

        return Response(serialized_data)


class UserRecieverView(APIView):
    def get(self, request,oid):
        order = Orders.objects.get(pk=oid)  
        user =order.user_id
        # serializer = UserSerializer(user, many=True)
        # serialized_data = serializer.data
        print('user....',user)
        return Response(user)
    





class OrderChatMessagesAPIView(APIView):
    def get(self, request, oid, *args, **kwargs):
        try:
            order = Orders.objects.get(pk=oid)
        except Orders.DoesNotExist:
            return Response({'error': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

        chat_messages = order.chat_messages.all()

        if not chat_messages:
            return Response({'message': 'No chat messages for this order'}, status=status.HTTP_200_OK)

        sender = chat_messages.first().sender
        receiver = chat_messages.first().receiver
        
        sender_profile = UserProfile.objects.get(user=sender)
        print(sender_profile)
        receiver_profile = UserProfile.objects.get(user=receiver)
        print(receiver_profile)
        
        # Serialize chat messages along with sender and receiver profile pictures
        serialized_data = []
        for message in chat_messages:
            serializer = ChatMessageSerializer(message)
            sender_profile_pic = sender_profile.profile_pic.url if sender_profile.profile_pic else None
            receiver_profile_pic = receiver_profile.profile_pic.url if receiver_profile.profile_pic else None
            serialized_data.append({
                **serializer.data,
                'sender_profile_pic': sender_profile_pic,
                'receiver_profile_pic': receiver_profile_pic
            })

        return Response(serialized_data, status=status.HTTP_200_OK)







# class OrderChatMessagesAPIView(APIView):
#     def get(self, request, oid, *args, **kwargs):
#         try:
#             order = Orders.objects.get(pk=oid)
#         except Orders.DoesNotExist:
#             return Response({'error': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

#         chat_messages = order.chat_messages.all()

#         if not chat_messages:
#             return Response({'message': 'No chat messages for this order'}, status=status.HTTP_200_OK)

#         sender = chat_messages.first().sender
#         receiver = chat_messages.first().receiver
        
#         # Fetch user profiles for sender and receiver
#         sender_profile = UserProfile.objects.get(user=sender)
#         print(sender_profile)
#         receiver_profile = UserProfile.objects.get(user=receiver)
#         print(receiver_profile)
        
#         # Serialize chat messages along with sender and receiver profile pictures
#         serialized_data = []
#         for message in chat_messages:
#             serializer = ChatMessageSerializer(message)
#             sender_profile_pic = sender_profile.profile_pic.url if sender_profile.profile_pic else None
#             receiver_profile_pic = receiver_profile.profile_pic.url if receiver_profile.profile_pic else None
#             serialized_data.append({
#                 **serializer.data,
#                 'sender_profile_pic': sender_profile_pic,
#                 'receiver_profile_pic': receiver_profile_pic
#             })

#         return Response(serialized_data, status=status.HTTP_200_OK)




class UsersMessagedTeacher(APIView):
    def get(self, request):
        current_user = request.user
        chat = ChatMessage.objects.filter(receiver=current_user)
        orders = set(ord.order for ord in chat)

        user_ids = {order.user_id for order in orders}
        user_profiles = UserProfile.objects.filter(user_id__in=user_ids)
        user_profiles_dict = {profile.user_id: profile for profile in user_profiles}


        serialized_data = []
        for order in orders:
            user_profile = user_profiles_dict.get(order.user_id)
            if user_profile:
                serializer = OrderSerializer(order)
                serialized_order = serializer.data
                serialized_order['profile_pic'] = str(user_profile.profile_pic)
                serialized_data.append(serialized_order)

        return Response(serialized_data, status=status.HTTP_200_OK)
















# class OrderWithUserView(APIView):
#     def get(self, request):
#         orders = Orders.objects.filter(user=request.user)
#         unique_usernames = set()
#         unique_orders = []
        
#         for order in orders:
#             username = order.course.added_by.username
#             if username not in unique_usernames:
#                 unique_usernames.add(username)
#                 unique_orders.append(order)

#         # Serialize the unique orders
#         serializer = OrderWithUserSerializer(unique_orders, many=True)
#         return Response(serializer.data)
    