from django.db import models


#参赛者
class ActorTable(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    mobile=models.CharField(max_length=15,unique=True)
    img=models.ImageField(null=True)
    supporter_count=models.IntegerField(default=0)
    is_first=models.BooleanField(default=True)


#手机验证码
class CodesTable(models.Model):
    code=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now=True)
    mobile=models.CharField(max_length=15)


#ip记录
class IpTable(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    ip=models.CharField(max_length=20)


#获奖等级
class LuckTable(models.Model):
    luck_name=models.CharField(max_length=20)
    actor_obj=models.OneToOneField(to='ActorTable',on_delete=models.CASCADE)


#是否开始抽奖
class StartTable(models.Model):
    start=models.BooleanField()


#记录游玩者ip
class PlayFinishTable(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    ip=models.CharField(max_length=100)
















