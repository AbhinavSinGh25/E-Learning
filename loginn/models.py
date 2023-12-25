from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=100,default="null")
    lastname = models.CharField(max_length=100,default="null")
    email = models.EmailField(max_length=254,default="null")
    password = models.CharField(max_length=100,default="null")
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.firstname
    
    
class Quiz_Info(models.Model):
    q_name=models.CharField(max_length=255,default="NULL")
    q1=models.CharField(max_length=255,default="Null")
    op1_1=models.CharField(max_length=255,default="Null")
    op2_1=models.CharField(max_length=255,default="Null")
    op3_1=models.CharField(max_length=255,default="Null")
    op4_1=models.CharField(max_length=255,default="Null")
    ans_1=models.CharField(max_length=255,default="Null")
    
    q2=models.CharField(max_length=255,default="Null")
    op1_2=models.CharField(max_length=255,default="Null")
    op2_2=models.CharField(max_length=255,default="Null")
    op3_2=models.CharField(max_length=255,default="Null")
    op4_2=models.CharField(max_length=255,default="Null")
    ans_2=models.CharField(max_length=255,default="Null")


    q3=models.CharField(max_length=255,default="Null")
    op1_3=models.CharField(max_length=255,default="Null")
    op2_3=models.CharField(max_length=255,default="Null")
    op3_3=models.CharField(max_length=255,default="Null")
    op4_3=models.CharField(max_length=255,default="Null")
    ans_3=models.CharField(max_length=255,default="Null")

class Quiz_Results(models.Model):
    stu_id=models.ForeignKey(User,on_delete=models.CASCADE)
    q_score = models.IntegerField(default=0)
    q_time = models.IntegerField(default=0)
    quizz_id=models.ForeignKey(Quiz_Info,on_delete=models.CASCADE)
    
class Quiz_Attempts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz_id=models.ForeignKey(Quiz_Info,on_delete=models.CASCADE)

    
    