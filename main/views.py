
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings
from .models import *
from .serializers import *
from .tools import alert_request,mobile_to_abc,abc_to_mobile,get_ip


# 视图集基类
class BaseViewSet(viewsets.ViewSet):
    """
    示例 viewset 演示了将由路由器类处理的标准动作。
    如果你使用格式后缀，请务必为每个动作包含一个`format=None` 的关键字参数。
    """
    def list(self, request):
        raise serializers.ValidationError('不允许的操作')

    def create(self, request):
        raise serializers.ValidationError('不允许的操作')

    def retrieve(self, request, pk=None):
        raise serializers.ValidationError('不允许的操作')

    def update(self, request, pk=None):
        raise serializers.ValidationError('不允许的操作')

    def partial_update(self, request, pk=None):
        raise serializers.ValidationError('不允许的操作')

    def destroy(self, request, pk=None):
        raise serializers.ValidationError('不允许的操作')


# 用于测试的地方
class TestViewSet(ModelViewSet):
    serializer_class =TestSerializer
    queryset =CodesTable.objects.get_queryset().order_by('id')
    def list(self,request,*args,**kwargs):
        return Response('')
        # self.test_1(request)
        # a=ActorTable.objects.filter(mobile=17686988582).delete()  #清空用户  涛哥手机号18621508176
        code_objs=CodesTable.objects.filter(created_at__gt=datetime.datetime.now()-datetime.timedelta(minutes=5))
        code_objs=code_objs.order_by('-created_at')
        code_serializer=TestSerializer(code_objs,many=True)
        c=request.GET.get('c',None)
        if c=='user':
            StartTable.objects.all().delete()
            actor_objs=ActorTable.objects.all()
            aaa=[]
            for actor_obj in actor_objs:
                info='已经删除{}'.format(actor_obj.mobile)
                actor_obj.delete()
                aaa.append(info)
            return Response(aaa)
        elif c=='ip':
            PlayFinishTable.objects.all().delete()
            return Response('成功清除所有ip标志')
        elif c=='test_2':
            self.test_2()
        return Response(code_serializer.data)

    def test_1(self,request):
        ActorTable.objects.create(mobile='17686988583',supporter_count=100,)

    def test_2(self):
        path='aaa.png'
        img_handler=ImageHandler(path=path)
        img=img_handler.img_to_jpeg()
        img=img_handler.img_to_range()
        img.save('xxx.png')




# 参赛者添加图片
class ActorImgViewSet(BaseViewSet):
    serializer_class=ActorImgSerializer
    queryset=ActorTable.objects.get_queryset().order_by('id')

    def validate_code(self,request):
        # return request
        try:
            request.data._mutable=True
            code=request.data.get('code',None)
            mobile=request.data.get('mobile',None)
            request.data._mutable=False
        except:
            print('mutable错误')
            code=request.data.get('code',None)
            mobile=request.data.get('mobile',None)
        if not code or not mobile:raise serializers.ValidationError('验证码是必填的')
        now=datetime.datetime.now()
        if not CodesTable.objects.filter(mobile=mobile,code=code,created_at__gt=now-datetime.timedelta(minutes=5)):
            raise serializers.ValidationError('验证码无效或者已过期')
        return request

    def validate_mobile(self,request):
        mobile=request.data.get('mobile',None)
        if not mobile:raise serializers.ValidationError('手机号是必填的')
        instance=ActorTable.objects.filter(mobile=mobile).first()
        return instance

    def create_mobile(self,request):
        serializer=ActorImgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.custom_view=self
            instance=serializer.save()
            return self.return_response(instance)
        else:
            raise serializers.ValidationError(self.error_handler(serializer.errors))

    def update_mobile(self,request,instance):
        serializer = ActorImgSerializer(instance,request.data)
        if serializer.is_valid():
            serializer.custom_view = self
            instance = serializer.save()
            return self.return_response(instance)
        else:
            raise serializers.ValidationError(self.error_handler(serializer.errors))

    def error_handler(self,error):
        if error.get('img',None):
            error['img'] = '请上传正确的图片格式'
        return error

    def return_response(self,instance):
        root_ip = settings.ROOR_IP
        mobile = instance.mobile
        mobile = mobile_to_abc(mobile)
        qr_code_url = '{}/{}/{}/'.format(root_ip, 'assistance', mobile)
        img_url = instance.img
        return Response({'qr_code_url': qr_code_url, 'img_url': str(img_url)})

    def create(self,request,*args,**kwargs):
        print(request.data)
        request=self.validate_code(request)
        instance=self.validate_mobile(request)
        if not instance:
            return self.create_mobile(request)
        else:
            return self.update_mobile(request,instance)


# 短信验证码
class CodesViewSet(BaseViewSet):
    '''
    在此处申请验证码
    '''
    serializer_class=CodesSerializer
    queryset = CodesTable.objects.get_queryset().order_by('id')

    def create(self,request):
        serializer=CodesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise serializers.ValidationError(serializer.errors)


# 访问参赛者信息，(修改后不再为参赛者添加计数分数)
class CountViewSet(BaseViewSet):

    def list(self,request,*args,**kwargs):
        print(1)
        mobile=kwargs.get('mobile')
        print(2)
        mobile=abc_to_mobile(mobile)
        print(3)
        actor_obj=ActorTable.objects.filter(mobile=mobile).first()
        print(4)
        if not actor_obj:raise serializers.ValidationError('不存在的参赛者')
        print(5)
        if self.validate_ip(get_ip(request)):raise serializers.ValidationError('当前ip访问过于频繁,请稍后再为您支持的选手加油！')
        print(6)
        # actor_obj.supporter_count+=1
        # actor_obj.save()
        print(7)
        serializer=CountSerializer(actor_obj)
        print(8)
        return Response(serializer.data)

    def validate_ip(self,ip):
        print(9)
        ip_objs=IpTable.objects.filter(ip=ip)
        print(10)
        #没有这个ip,直接允许
        if not ip_objs:
            print(11)
            IpTable.objects.create(ip=ip)
            print(12)
            return False
        else:
            print(13)
            TriesLimit = settings.TRIESLIMIT  #限制次数
            print(14)
            LimitedTime=settings.LIMITEDTIME  #限制时间
            print(15)
            now=datetime.datetime.now()
            print(16)
            #限制时间以内这个ip的访问次数
            ip_count=ip_objs.filter(created_at__gt=now-LimitedTime).count()
            print(17)
            #如果访问次数大于ip限制次数,返回错误信息
            if ip_count>TriesLimit:
                print(18)
                return True
            else:
                print(19)
                IpTable.objects.create(ip=ip)
                print(20)
                IpTable.objects.filter(ip=ip,created_at__lt=now-datetime.timedelta(days=1)).delete()
                print(21)
                return False


# 竞赛者排名
class RankingViewSet(BaseViewSet):
    serializer_class=RankingSerializer
    queryset = ActorTable.objects.get_queryset().order_by('-supporter_count')

    def list(self,request):
        queryset =ActorTable.objects.get_queryset().order_by('-supporter_count')
        serializer=RankingSerializer(queryset,many=True)
        if len(serializer.data)<9:
            return Response(serializer.data)
        else:
            return Response(serializer.data[:8])


# 抽奖接口
class AManOfGoodLuckViewSet(BaseViewSet):
    serializer_class=MobileWriteSerializer

    def create(self,request,*args,**kwargs):
        #检测这个手机号是否达到抽奖标准
        if self.actor_standard(request):return Response(self.actor_standard(request))
        #查询有没有产生第一名
        #有就返回用户获奖状态
        #没有就新建第一名同时返回获奖状态
        luck_obj=LuckTable.objects.all()
        #如果没有第一名，那就产生第一名
        if not luck_obj:
            self.get_lucker()

        #现在有第一名了，取出这个第一名，与提交者的手机号对比
        luck_obj = LuckTable.objects.all()
        luck_obj=luck_obj.first().actor_obj
        #中将者手机号
        actor_mobile=luck_obj.mobile
        #提交的手机号
        request_mobile=request.data.get('mobile',None)
        if not request_mobile:raise serializers.ValidationError('手机号是必填的')
        #对比提交的手机号和中间者手机号
        if actor_mobile==request_mobile:
            # 提交的手机号和中将者手机号相同，luck标记为1
            luck=1
            help='中奖'
        else:
            #提交的手机号与中将者手机号不同时，luck标记为0
            luck=0
            help='未中奖'
        #通过这些数据构造提示信息
        data={'request_mobile':request_mobile,'luck':luck,'help':help}
        serializer=LuckSerializer(data=data)
        #如果数据不合法，直接抛出异常
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #返回生成的数据
        return Response(serializer.luck_info)

    #得到中将者
    def get_lucker(self):
        #如果已经存在中奖者直接返回
        if LuckTable.objects.all():return

        #筛选出符合抽奖标准的参赛者
        supporter_count=settings.SUPPORTERCOUNT
        actor_objs=ActorTable.objects.filter(supporter_count__gt=supporter_count).distinct()
        #如果有人符合条件,肯定是有的,否则self.actor_standard()会抛出异常
        if actor_objs:
            luck_num=random.randint(0,len(actor_objs)-1)
            actor_obj=actor_objs[luck_num]
            LuckTable.objects.create(actor_obj=actor_obj,luck_name='一等奖')
        else:
            raise serializers.ValidationError('没有中奖')


    #检测这个手机号是否存在或达到抽奖标准
    def actor_standard(self,request):
        #40代表抽奖还没有开始
        if not StartTable.objects.all():return {'luck':40,'help':'抽奖还没有开始'}
        mobile=request.data.get('mobile',None)
        if not mobile:raise serializers.ValidationError('手机号是必填的')
        #通过手机号找到参赛者
        actor_obj=ActorTable.objects.filter(mobile=mobile).first()
        if not actor_obj:raise serializers.ValidationError('提交者的手机号不在参赛者名录')
        #与抽奖标准线对比，没有达标的参赛者luck状态为4
        supporter_count=settings.SUPPORTERCOUNT
        if actor_obj.supporter_count<supporter_count:
            #41代表没有达到抽奖标准
            return {'luck':41,'help':'没有达到抽奖标准'}


# 下达抽奖指令
class StartLuckViewSet(BaseViewSet):
    serializer_class=StartSerializer

    def list(self,request,*args,**kwargs):
        if StartTable.objects.all():
            return Response({'help':'抽奖已经开启,现在允许参赛者进行抽奖','status':'1'})
        else:
            return Response({'help':'抽奖已经关闭,现在不允许参赛者进行抽奖','status':'0'})


    def create(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# 后台查看获奖者
class LookLuckViewSet(BaseViewSet):
    serializer_class=PasswordWriteSerializer
    def create(self,request,*args,**kwargs):
        if settings.STARTPASSWORD!=request.data.get('password'):raise serializers.ValidationError('不正确的密码')
        self.get_lucker()

        lock_obj=LuckTable.objects.all()
        mobile=lock_obj.first().actor_obj.mobile
        return Response({'mobile':mobile,'help':'已经通过计算机随机算法产生中奖者。中奖者手机号为{}'.format(mobile)})

    #得到中将者
    def get_lucker(self):
        #如果已经存在中奖者直接返回
        if LuckTable.objects.all():return
        #筛选出符合抽奖标准的参赛者
        supporter_count=settings.SUPPORTERCOUNT
        actor_objs=ActorTable.objects.filter(supporter_count__gt=supporter_count).distinct()
        if actor_objs:
            luck_num=random.randint(0,len(actor_objs)-1)
            actor_obj=actor_objs[luck_num]
            LuckTable.objects.create(actor_obj=actor_obj,luck_name='一等奖')
        else:
            raise serializers.ValidationError('所有人都不符合抽奖标准')


# 后台查看获奖者,但不更新状态
class LookLuckNoAlertViewSet(BaseViewSet):
    serializer_class=RankingSerializer
    queryset = ActorTable.objects.get_queryset().order_by('-supporter_count')
    def create(self,request):
        mobile=request.data.get('mobile',None)
        if not mobile:raise serializers.ValidationError('mobile是必填的')
        actor_obj=ActorTable.objects.filter(mobile=mobile).first()
        if not actor_obj:raise serializers.ValidationError('不存在这个用户')
        return Response({'is_first':actor_obj.is_first})


# 改变抽奖状态
class AlertLuckStatusViewSet(BaseViewSet):
    def create(self,request):
        mobile=request.data.get('mobile',None)
        if not mobile:raise serializers.ValidationError('mobile是必填的')
        actor_obj=ActorTable.objects.filter(mobile=mobile).first()
        if not actor_obj:raise serializers.ValidationError('不存在这个用户')
        actor_obj.is_first=False
        actor_obj.save()
        return Response({'is_first':False})


# 参与游戏
class PlayViewSet(BaseViewSet):
    serializer_class=MobileGameScoreSerializer
    #这个接口用于判断支持者是不是已经玩过了
    def list(self,request,*args,**kwargs):
        if self.play_finisher(request):
            ip_error=hasattr(self,'ip_error')
            if ip_error:
                help_info=self.ip_error
            else:
                help_info = '已经玩过了,不能再愉快的玩耍了'
            return Response({'paly_finisher':True,'help':help_info})
        else:
            return Response({'paly_finisher':False,'help':'没有玩过,嗯,可以来一局'})

    #这个接口用于提交把支持者的分数累加到参赛者
    def create(self,request,*args,**kwargs):
        if self.play_finisher(request):
            raise serializers.ValidationError('失败,提交者之前已经玩过游戏')
        actor_obj,game_score=self.get_mobile_obj_game_score(request)
        actor_obj.supporter_count+=game_score
        actor_obj.save()
        serializer=ActorSerializer(actor_obj)
        response=Response(serializer.data)
        response=self.make_play_log(request,response)
        return response

    #判断这个游玩者是不是已经玩过了
    def play_finisher(self,request):
        #有这个字段证明已经玩过
        if request.COOKIES.get('is_play_finisher',None):
            return True
        #有这个ip证明已经玩过
        ip=get_ip(request)
        minutes=60*24
        count=1
        the_time=datetime.datetime.now()-datetime.timedelta(minutes=minutes)
        if PlayFinishTable.objects.filter(ip=ip,created_at__gt=the_time).count()>=count:
            self.ip_error='ip限制[在过去的{}分钟内已经进行了{}次游戏]'.format(minutes,count)
            return True
            # raise serializers.ValidationError('ip异常[在过去的{}分钟内进行了{}次游戏]'.format(minutes,count))
        #如果没有cookie和ip那就是没玩过
        return False

    #提取参赛者信息和支持者得到的游戏分数
    def get_mobile_obj_game_score(self,request):
        mobile=request.data.get('mobile',None)
        if not mobile :raise serializers.ValidationError('mobile是必须的参数')
        actor_obj=ActorTable.objects.filter(mobile=mobile).first()
        if not actor_obj:raise serializers.ValidationError('不存在的参赛者')
        game_score=request.data.get('game_score',None)
        if not game_score:raise serializers.ValidationError('game_score是必填的')
        try:
            game_score=int(game_score)
        except:
            raise serializers.ValidationError('game_score必须是一个数字')
        return actor_obj,game_score

    #为支持者的ip和cookie添加标记作为记号
    def make_play_log(self,request,response):
        #设置这个游戏者的那啥,cookie
        response.set_cookie('is_play_finisher', 'true')
        #添加这个游戏者的ip
        ip=get_ip(request)
        PlayFinishTable.objects.create(ip=ip)
        return response










