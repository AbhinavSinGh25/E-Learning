from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home', views.home,name='home'),
    path('home_afterlogin/<int:id>/', views.home_after_login,name='home_after_login'),
    path('signup/', views.signup,name='signup'),
    path('signup/login/signup/', views.signup,name='signup'),
    path('signup/login/', views.login,name='login'),
     path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    # path('quiz/', views.quizView, name='quiz'),
    path('dashboard/<int:id>/', views.dashboard, name='dashboard'),
    path('add_mcq_questions/', views.add_mcq_questions, name='add'),
        # path to show list of available quizzes
    path('quiz_list/<int:id>/', views.quiz_list, name='quiz_list'),
    path('quizView/', views.quizView, name='quizView'),
    
    # path to show a particular quiz
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('result_table/<int:id>/', views.result_table, name='result_table'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('quiz_list_admin/', views.quiz_list_admin, name='quiz_list_admin'),
    path('reward/', views.reward, name='reward'),
    path('voucher/', views.voucher, name='voucher'),
    path('update_coins/', views.update_coins, name='update_coins'),
    
   

    # Add more URLs for other views here
]
urlpatterns += staticfiles_urlpatterns()