from django.db import models

class User(models.Model):
    Name = models.CharField(max_length=100)
    Code = models.CharField(max_length=20)
    Rank = models.CharField(max_length=50)
    Folio_Number = models.CharField(max_length=20, unique=True)
    Password = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=15)
    GLS_4_Participation = models.BooleanField(default=False)
    TC_Filled = models.BooleanField(null=True,default=False)
    

    def __str__(self):
        return f"{self.Name} ({self.Folio_Number})"

class UserData(models.Model):
    user = models.OneToOneField(User, to_field='Folio_Number', on_delete=models.CASCADE)
    Income_24_25 = models.FloatField()
    Sales_24_25 = models.FloatField()
    Team_24_25 = models.FloatField()
    Team_23_24 = models.FloatField()
    RPM_24_25 = models.FloatField()
    TEL_T_24_25  = models.FloatField()
    UP_T_24_25  = models.FloatField()
    RJ_T_24_25  = models.FloatField()
    PB_T_24_25  = models.FloatField()
    HR_T_24_25  = models.FloatField()
    HP_T_24_25  = models.FloatField()
  


class GLS_Data(models.Model):
    user = models.OneToOneField(User, to_field='Folio_Number', on_delete=models.CASCADE)
    Batch = models.CharField(max_length=20)
    Seat_Number = models.CharField(max_length=10)
    Checked_In = models.BooleanField(default=False)
    Checkin_Time = models.DateTimeField(null=True, blank=True)
    Logged_In = models.BooleanField(default=False)
    Feedback_Form_Filled = models.BooleanField(default=False)
    Expected_Arrival = models.DateTimeField(null=True, blank=True)
    First_Time_Attendee = models.BooleanField(default=False)    
    Mode_of_Transport = models.CharField(max_length=100, blank=True)  
    Emergency_Contact = models.CharField(max_length=50, blank=True)
    Admit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.Name} - {self.Batch} - Seat {self.Seat_Number}"

