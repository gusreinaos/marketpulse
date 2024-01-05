# Author: everyone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class Prediction(models.Model):
    prediction_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    prediction_value = models.FloatField(validators=[MaxValueValidator(2),MinValueValidator(0)])
    created_at = models.DateTimeField()
    company_code = models.CharField(max_length=10) 
    avg_sentiment = models.FloatField(default=0)
    tweet_rate = models.FloatField(default=0)
    stock_val = models.FloatField(default=0)
    #other values can be added, depending on what we decide is important

class TrainSentimentData(models.Model):
    ts_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    unclean = models.CharField(max_length=2000, default='NaN', unique=True)
    clean = models.CharField(max_length=2000, default='NaN')
    sentiment = models.IntegerField(validators=[MaxValueValidator(2),MinValueValidator(0)])
    created_at = models.DateTimeField()


class ValidSentimentData(models.Model):
    vs_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    unclean = models.CharField(max_length=2000, default='NaN', unique=True)
    clean = models.CharField(max_length=2000, default='NaN')
    sentiment = models.IntegerField(validators=[MaxValueValidator(2),MinValueValidator(0)])
    created_at = models.DateTimeField()

class TrainTrendData(models.Model):
    tt_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    ticker_symbol = models.CharField(max_length=10, default='NaN')
    post_date = models.IntegerField(default=0)
    sentiment = models.IntegerField(validators=[MaxValueValidator(2),MinValueValidator(0)])
    
class Company(models.Model):
    company_code = models.CharField(primary_key=True,max_length=10, unique=True,default='')
    company_name = models.CharField(max_length=20, unique=True)
    trainable  = models.BooleanField(default = False)
    company_info = models.CharField(max_length=300, unique=False, default='NaN')
    company_logo = models.CharField(max_length=300, unique=False, default='NaN')

class CustomUser(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=False)

class UserFavoritesCompany(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','company'],name='favorite company uniqueness')
        ]
