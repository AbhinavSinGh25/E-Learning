from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Quiz_Results, Quiz_Info,Quiz_Attempts
from django.template import loader
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
import random
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
import json
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json.decoder import JSONDecodeError


def signup(request):
    if request.method == 'POST':
        # Get the form data from the request object
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Insert the form data into the database using a model

        user = User(firstname=firstname, lastname=lastname,
                    email=email, password=password)
        user.save()

        template=loader.get_template('success.html')
        context={
            'msg':"Thanks For Signing Up!!"
        }
        return HttpResponse(template.render(context,request))
    return render(request, "signup.html")


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def home_after_login(request):
    login_id=request.GET.get('id')

    template = loader.get_template('home_after_login.html')
    return HttpResponse(template.render())

def admin_portal(request):
    template=loader.get_template('admin_portal.html')
    return HttpResponse(template.render())
    
def quiz_list_admin(request):
    
    quizzes = Quiz_Info.objects.all()
    template=loader.get_template('quiz_list_admin.html')
    context={
        'quiz':quizzes    
    }
    return HttpResponse(template.render(context,request))    

def reward(request):
    id = request.session.get('id')
    results = Quiz_Results.objects.filter(quizz_id=id).order_by('q_time', '-q_score')[:3]
    if request.method == 'POST':
        if results:
            results[0].stu_id.coins += 20  # Add 20 coins to rank 1
            results[0].stu_id.save()
            if len(results) >= 2:
                results[1].stu_id.coins += 10  # Add 10 coins to rank 2
                results[1].stu_id.save()
            if len(results) >= 3:
                results[2].stu_id.coins += 5  # Add 5 coins to rank 3
                results[2].stu_id.save()
        
        # Set a flag in the session to disable the button on the next render
        request.session['disable_button'] = True
    
    return redirect('result_table', id=id)



    
def result_table(request, id):
    request.session['id'] = id
    results = Quiz_Results.objects.filter(quizz_id=id).order_by('q_time', '-q_score')[:3]
    
    # Determine whether the button should be disabled
    disable_button = False
    if 'disable_button' in request.session:
        disable_button = request.session['disable_button']
        del request.session['disable_button']  # Clear the flag from the session
    
    context = {
        'results': results,
        'disable_button': disable_button,  # Pass the flag to the template
    }
    template = loader.get_template('result_table.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def update_coins(request):
    print('request received')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data['user_id']
            req_coins = data['required_coins']
            user = User.objects.get(id=id)
            user.coins -= req_coins
            user.save()
            return JsonResponse({'success': True})
        except (json.decoder.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
def voucher(request):
    login_id=request.session.get('id')
    user=User.objects.get(id=login_id)
    total_coins=user.coins
    context={
        'total_coins':total_coins,
        'login_id':login_id
    }
    return render(request,'voucher.html',context)

def dashboard(request,id):
    quiz_attempts = Quiz_Attempts.objects.filter(user_id=id)
    quiz_attempted = set([attempt.quiz_id for attempt in quiz_attempts])
    total_count=len(quiz_attempted)
    total_quiz=Quiz_Info.objects.count()
    user=User.objects.get(id=id)
    request.session['id']=id
    total_coins=user.coins
    context={'total_count':total_count,
            'total_quiz':total_quiz,
            'total_coins':total_coins}
    return render(request, 'dashboard.html',context)


def login(request):
    template=loader.get_template('home_after_login.html')
    if request.method == 'POST':
        email = request.POST.get('uname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            id=user.id
            context={
                'id':id
                }
            
            return HttpResponse(template.render(context,request))
        except User.DoesNotExist:
            return render(request, 'login.html', {'message': 'Invalid credentials. Please try again.'})
    return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if user with this email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(
                request, 'There is no user with this email address.')
            return render(request, 'forgot_password.html')
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        # Store OTP in session
        request.session['otp'] = otp
        request.session['email'] = email
        # Send OTP to user's email
        subject = 'OTP for password reset'
        message = f'Your OTP for password reset is {otp}. Do not share it with anyone.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, from_email, recipient_list)
        # Redirect to verify OTP view
        return redirect('verify_otp')
    return render(request, 'forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            # OTP is valid, allow user to reset their password
            # Get user's email from session
            email = request.session.get('email')
            # Remove stored OTP and email from session
            del request.session['otp']
            del request.session['email']
            # Redirect to reset password view
            messages.success(
                request, 'OTP verified. Please enter a new password.')
            return redirect('reset_password')
        else:
            # OTP is invalid, show an error message
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('email')
        # Get user with this email
        user = User.objects.get(email=email)
        # Set new password
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        # Authenticate and login user
        user = authenticate(username=user.username, password=new_password)
        if user:
            login(request, user)
            messages.success(
                request, 'Password reset successfully. You are now logged in.')
            return redirect('home')
    return render(request, 'reset_password.html')


@csrf_exempt
def quizView(request):
    print("request received")
    user_id=request.session.get('login_id')
    quiz_id=request.session.get('quiz_id')
    user=User.objects.get(id=user_id)
    quiz=Quiz_Info.objects.get(id=quiz_id)
    attempt=Quiz_Attempts(user=user,quiz_id=quiz)
    attempt.save()
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            score = data['score']
            totalTime = data['total_quiz_time']
            # Create a new quiz object with the data
            new_quiz = Quiz_Results(stu_id=user,q_score=score, q_time=totalTime,quizz_id=quiz)
            # Save the quiz object to the database
            new_quiz.save()
            return JsonResponse({'success': True})
        except (json.decoder.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'quiz.html')


def add_mcq_questions(request):
    if request.method == 'POST':

        q_name = request.POST.get('qname')
        q1 = request.POST.get('question1')
        op1_1 = request.POST.get('option1_1')
        op2_1 = request.POST.get('option2_1')
        op3_1 = request.POST.get('option3_1')
        op4_1 = request.POST.get('option4_1')
        ans_1 = request.POST.get('correct_answer1')

        q2 = request.POST.get('question2')
        op1_2 = request.POST.get('option1_2')
        op2_2 = request.POST.get('option2_2')
        op3_2 = request.POST.get('option3_2')
        op4_2 = request.POST.get('option4_2')
        ans_2 = request.POST.get('correct_answer2')

        q3 = request.POST.get('question3')
        op1_3 = request.POST.get('option1_3')
        op2_3 = request.POST.get('option2_3')
        op3_3 = request.POST.get('option3_3')
        op4_3 = request.POST.get('option4_3')
        ans_3 = request.POST.get('correct_answer3')

        quiz_data = Quiz_Info(q_name=q_name, q1=q1, op1_1=op1_1, op2_1=op2_1, op3_1=op3_1, op4_1=op4_1, ans_1=ans_1, q2=q2, op1_2=op1_2,
                            op2_2=op2_2, op3_2=op3_2, op4_2=op4_2, ans_2=ans_2, q3=q3, op1_3=op1_3, op2_3=op2_3, op3_3=op3_3, op4_3=op4_3, ans_3=ans_3)
        quiz_data.save()
        template=loader.get_template('success.html')
        context={
            'msg':"Quiz Saved"
        }
        return HttpResponse(template.render(context,request))
    return render(request, 'quiz_creation.html')


def quiz_list(request, id):
    login_id = id
    request.session['login_id'] = login_id
    quizzes = Quiz_Info.objects.all()

    # Check if user has attempted the quiz
    quiz_attempts = Quiz_Attempts.objects.filter(user_id=login_id)
    quiz_attempted = set([attempt.quiz_id for attempt in quiz_attempts])
    total_count=len(quiz_attempted)
    context = {'quizzes': quizzes,
            'login_id': login_id,
            'count':total_count}
    context['quiz_attempted'] = quiz_attempted

    return render(request, 'quiz_list.html', context)


def quiz(request, quiz_id):
    login_id=request.session.get('login_id')
    request.session['user_id']=login_id    
    request.session['quiz_id']=quiz_id    
    quiz = get_object_or_404(Quiz_Info, id=quiz_id)
    context = {'quiz': quiz,
            'login_id':login_id}
    return render(request, 'quiz.html', context)





