from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='main'),
    path('accounts/verify/', email_verify, name='verify'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', log_out, name='out'),
    path('accounts/signup/', user_signup, name='new_acc'),
    path('create/', AddPost.as_view(), name='add'),
    path('post/<int:pk>/', PostDetail.as_view(), name='detail'),
    path('post/<int:pk>/add_reply/', add_reply, name='reply'),
    path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('replies/', PostReplyView.as_view(), name='prof'),
    path('replies/<int:pk>/submit/', rep_submit, name='submit'),
    path('replies/<int:pk>/delete/', rep_delete, name='rep_delete'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('my_subs/', subscriptions, name='my_subs'),
]

