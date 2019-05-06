from rest_framework import serializers
from django.conf import settings
from .tools import SendSMS,mobile_to_abc,ImageHandler
import random,datetime
from .models import *


#参赛者信息
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model=ActorTable
        fields=('mobile','supporter_count','is_first',)
        read_only_fileds=('is_first',)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=CodesTable
        fields=('id','mobile','created_at','code',)


#参赛者添加图片
class ActorImgSerializer(serializers.ModelSerializer):
    code=serializers.CharField(write_only=True)
    class Meta:
        model=ActorTable
        fields=('img','mobile','code',)

    def create(self, validated_data):
        validated_data.pop('code')
        if not validated_data.get('img',None):raise serializers.ValidationError('首次注册必须上传图片')
        mobile=validated_data.get('mobile')
        view=self.custom_view
        img=view.request.data.get('img')
        path='image_dir/{}.png'.format(mobile_to_abc(mobile))
        with open(path,'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        self.alert_img(path)
        validated_data.update({'img':path})
        instance = ActorTable.objects.create(**validated_data)
        return instance

    def alert_img(self,path):
        img_handler=ImageHandler(path=path)
        # img_handler.img_to_jpeg()
        img=img_handler.img_to_range()
        img.save(path)

    def update(self, instance, validated_data):
        img=validated_data.get('img')
        if not img:
            validated_data.pop('img')
            return super().update(instance, validated_data)
        else:
            mobile = validated_data.get('mobile')
            view = self.custom_view
            img = view.request.data.get('img')
            path = 'image_dir/{}.png'.format(mobile_to_abc(mobile))
            with open(path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            instance.img=path
            instance.save()
            return instance


#验证码
class CodesSerializer(serializers.ModelSerializer):

    class Meta:
        model=CodesTable
        fields=('id','mobile','created_at')

    def get_code(self):
        return ''.join([str(random.randint(0,9)) for i in range(4)])

    def validate(self,data):
        mobile=data.get('mobile')
        #是否没超过1分钟
        now=datetime.datetime.now()
        code_objs = CodesTable.objects.filter(mobile=mobile)
        if code_objs.filter(created_at__gt=now - settings.CODE_TIME):
            raise serializers.ValidationError('这个手机号距离上次请求的时间还没有超过1分钟[开发期暂为5秒],请稍后再试')
        return data


    def create(self, validated_data):
        mobile=validated_data.get('mobile')
        code=self.get_code()
        validated_data['code']=code
        sms=SendSMS(mobile=mobile,data=code,log='瓦力工厂验证码')
        status=sms.send()
        if status:
            code_obj=CodesTable.objects.create(**validated_data)
        else:
            raise serializers.ValidationError('短信发送失败')
        return code_obj


#计数返回值
class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model=ActorTable
        fields=('img','supporter_count','mobile')


#排行
class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ActorTable
        fields=('mobile','img','supporter_count',)


#返回获奖者
class LuckSerializer(serializers.Serializer):
    luck=serializers.CharField(write_only=True)
    request_mobile=serializers.CharField(write_only=True)

    def validate_request_mobile(self, request_mobile):
        actor_obj=ActorTable.objects.filter(mobile=request_mobile).first()
        if actor_obj:
            return actor_obj
        else:
            raise serializers.ValidationError('参赛者不存在')

    def create(self, validated_data):
        actor_obj=validated_data.get('request_mobile')
        #手机，照片，中奖标志
        mobile=actor_obj.mobile
        is_first=actor_obj.is_first
        # img=actor_obj.img
        luck = validated_data.get('luck')
        self.luck_info={'mobile':mobile,'luck':luck,'is_first':is_first}
        # actor_obj.is_first=False
        # actor_obj.save()
        return {'mobile':mobile,'luck':luck,'is_first':is_first}


#启动抽奖的序列化器
class StartSerializer(serializers.Serializer):
    password=serializers.CharField(help_text='在这里输入管理员给你的密码，启动抽奖环节',write_only=True)
    status=serializers.ChoiceField(help_text='选择开启或者关闭抽奖功能',choices=((1,'开启抽奖'),(0,'关闭抽奖'),(4,'清除中奖者,谨慎操作')))

    def validate_password(self, attrs):
        if attrs==settings.STARTPASSWORD:
            return attrs
        else:
            raise serializers.ValidationError('不正确的密码')

    def create(self,validated_data):
        status=validated_data.get('status')
        if status==1:
            StartTable.objects.create(start=True)
            return {'status':'启动了抽奖'}
        elif status==0:
            StartTable.objects.all().delete()
            return {'status':'关闭了抽奖'}
        elif status==4:
            LuckTable.objects.all().delete()
            return {'status':'清空了中奖者'}


#手机号字段
class MobileWriteSerializer(serializers.Serializer):
    mobile=serializers.CharField(write_only=True)


#密码字段
class PasswordWriteSerializer(serializers.Serializer):
    password=serializers.CharField(write_only=True)


#验证码字段
class CodeWirteSerializer(serializers.Serializer):
    code=serializers.CharField()

#手机号游戏分数字段
class MobileGameScoreSerializer(serializers.Serializer):
    mobile=serializers.CharField()
    game_score=serializers.CharField()










