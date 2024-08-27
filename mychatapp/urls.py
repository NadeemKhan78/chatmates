from django.urls import path
from . import views

app_name = 'mychat'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.log_out, name='logout'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('remove_friend/<str:pk>', views.remove_friend, name='remove_friend'),
    path('send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('friend_request_notification', views.friend_request_notification, name='friend_request_notification'),
    path('accept_friend_request', views.accept_friend_request, name='accept_friend_request'),
    path('friend/<str:pk>', views.chatroom, name='chatroom'),
    path('sent_msg/<str:pk>', views.sentMessages, name='sent_msg'),
    path('rec_msg/<str:pk>', views.receivedMessages, name='rec_msg'),
    path('notification', views.chatNotification, name='notification'),
    path('request_notification', views.requestNotification, name='request_notification'),

    # Responsive paths
    path('my_profile', views.my_profile, name = 'my_profile')
]
