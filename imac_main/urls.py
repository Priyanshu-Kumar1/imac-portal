from django.contrib import admin
from django.urls import path, reverse
from imac_main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signupPost', views.signupPost, name='signupPost'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('adminportal', views.adminportal, name='adminportal'),
    path('approve-user', views.approve_user, name='approve_user'),
    path('approve-booking', views.approve_booking, name='approve_booking'),
    path('portal', views.portal, name='portal'),
    path('portal_pending', views.portal_pending, name='portal_pending'),
    path('submitreq', views.submitreq, name='submitreq'),
    path('loadlab', views.loadlab, name='loadlab')
]
