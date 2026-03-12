from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
    path('start/<int:applicant_id>/', views.start_conversation, name='start_conversation'),
    path('send/<int:conversation_id>/', views.send_message, name='send_message'),
    path('poll/<int:conversation_id>/', views.poll_messages, name='poll_messages'),
]