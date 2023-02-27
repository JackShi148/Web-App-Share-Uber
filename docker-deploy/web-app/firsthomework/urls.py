"""firsthomework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from user import views as user_views
from ride import views as ride_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.homePage, name='home'),
    path('home/', user_views.homePage, name='home'),
    path('login/', user_views.loginPage, name='login'),
    path('logout/', user_views.logoutPage, name='logout'),
    path('register/', user_views.registerPage, name='register'),
    path('user/profile/', user_views.profilePage, name='user_profile'),
    path('user/edit_profile/', user_views.user_edit_page, name='user_edit'),
    path('user/request_ride/', ride_views.request_ride_page, name='request_ride'),
    path('user/owner_view_ride/', ride_views.view_ride_page, name='view_ride'),
    path('user/history_rides/', ride_views.view_history_rides_page, name='view_history_rides'),
    path('user/<int:nid>/owner_edit_ride/', ride_views.owner_edit_ride_page, name='edit_ride'),
    path('user/<int:nid>/owner_delete_ride/', ride_views.owner_delete_ride_page, name='delete_ride'),
    path('user/sharer_join_ride/', ride_views.sharer_join_ride_page, name='join_ride'),
    path('user/<int:nid>/join_specific_ride/', ride_views.join_specific_ride_page, name='join_specific_ride'),
    path('user/<int:nid>/sharer_edit_ride/', ride_views.sharer_edit_ride_page, name='sharer_edit_ride'),
    path('user/<int:nid>/sharer_delete_ride/', ride_views.sharer_delete_ride_page, name='sharer_delete_ride'),
    path('user/view_as_driver/', ride_views.view_as_driver, name='view_as_driver'),
    path('user/register_driver/', user_views.register_driver, name='register_driver'),
    path('user/edit_profile_driver_info/', user_views.edit_profile_driver_info, name='edit_profile_driver_info'),
    path('user/unregister_driver/', user_views.unregister_driver, name='unregister_driver'),
    path('user/driver_search&confirm_ride/', ride_views.driver_search_confirm_ride, name='driver_search&confirm_ride'),
    path('user/<int:nid>/confirm_specific_ride_as_driver/', ride_views.confirm_specific_ride_as_driver, name='confirm_specific_ride_as_driver'),
    path('user/<int:nid>/driver_complete_ride/', ride_views.driver_complete_ride, name='driver_complete_ride'),
]
