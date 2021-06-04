"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from machine_scheduling.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('error/<str:error_message>/', error_page),
    path('new_schedule/upload/', new_schedule_upload), 
    path('new_schedule/view&check/<str:document_date>/', new_schedule_viewcheck),
    path('new_schedule/schedule/<str:document_date>/', new_schedule_doschedule),
    path('history_schedule/', history_schedule_menu),
    path('history_schedule/delete/<int:year>/<int:month>/origin_num=<int:origin_num>/', history_schedule_menu_delete),
    path('history_schedule/select_range_delete/', history_schedule_select_range_delete),
    path('history_schedule/select_range_delete/<str:start_date>/<str:end_date>/', history_schedule_select_range_delete_check),
    path('history_schedule/<str:document_date>/', history_schedule_one),
    path('history_schedule/<str:document_date>/product_info_view/', history_schedule_one_view),
]
