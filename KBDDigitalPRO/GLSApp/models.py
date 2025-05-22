from django.db import models
from homeapp.models import User  

class Target_Data_IST(models.Model): 
    user = models.OneToOneField(User, to_field='Folio_Number', on_delete=models.CASCADE)
    IST_Base = models.CharField(max_length=20)
    Target_Income = models.FloatField()
    Target_Sales = models.FloatField()
    Target_Team = models.FloatField()


    def __str__(self):
        return f"{self.user.Folio_Number} - {self.IST_Base} Target"



class Target_Card_Data(models.Model):
    user = models.OneToOneField(User, to_field='Folio_Number', on_delete=models.CASCADE)
    Target_Income = models.FloatField(null=True, blank=True)
    Target_Sales = models.FloatField(null=True, blank=True)
    Target_Team = models.FloatField(null=True, blank=True)
    Target_Team1 = models.FloatField(null=True, blank=True)

    agriculture_percent = models.FloatField(null=True, blank=True)
    swastham_percent = models.FloatField(null=True, blank=True)
    ayurman_percent = models.FloatField(null=True, blank=True)
    paridhan_percent = models.FloatField(null=True, blank=True)

    Target_AGR = models.FloatField(null=True, blank=True)
    Target_SWA = models.FloatField(null=True, blank=True)
    Target_AYU = models.FloatField(null=True, blank=True)
    Target_PAR = models.FloatField(null=True, blank=True)


    Target_RPM = models.FloatField(null=True, blank=True)
    Target_DTR = models.FloatField(null=True, blank=True)
    Target_NID = models.FloatField(null=True, blank=True)
    Target_NGL = models.FloatField(null=True, blank=True)
    Target_VV = models.FloatField(null=True, blank=True)
    Target_KV = models.FloatField(null=True, blank=True)
    Target_OBS = models.FloatField(null=True, blank=True)
    Target_AD = models.FloatField(null=True, blank=True)

    TEL_Target = models.FloatField(null=True, blank=True)
    UP_Target = models.FloatField(null=True, blank=True)
    RJ_Target = models.FloatField(null=True, blank=True)
    PB_Target = models.FloatField(null=True, blank=True)
    HR_Target = models.FloatField(null=True, blank=True)
    HP_Target = models.FloatField(null=True, blank=True)
    TURPHH_Target = models.FloatField(null=True, blank=True)

    Target_BO = models.FloatField(null=True, blank=True)

    TEL_BO_Target = models.IntegerField(null=True, blank=True)
    UP_BO_Target = models.IntegerField(null=True, blank=True)
    RJ_BO_Target = models.IntegerField(null=True, blank=True)
    PB_BO_Target = models.IntegerField(null=True, blank=True)
    HR_BO_Target = models.IntegerField(null=True, blank=True)
    HP_BO_Target = models.IntegerField(null=True, blank=True)
    TURPHH_BO_Target = models.IntegerField(null=True, blank=True)

    Star_NGL_Target = models.IntegerField(null=True, blank=True)
    CMR_Target = models.IntegerField(null=True, blank=True)

    TAL_Target = models.IntegerField(null=True, blank=True)
    Mahavir_Award_Target = models.IntegerField(null=True, blank=True)
    CMR_Centre_Target = models.IntegerField(null=True, blank=True)

    SGA = models.IntegerField(null=True, blank=True)
    IK = models.IntegerField(null=True, blank=True)
    PP = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Target Card for {self.user.Folio_Number}"
