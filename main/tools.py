import requests,json
from django.conf import settings
import PIL.Image as I


def get_ip(request):
    ip=request.META.get('HTTP_X_FORWARDED_FOR',None)
    return ip if ip else request.META.get('REMOTE_ADDR')


def alert_request(request,data):
    request.data._mutable=True
    request.data.update(data)
    request.data._mutable=False
    return request


def mobile_to_abc(mobile):
    a=ord('a')
    s=''
    for char in mobile:
        num=int(char)
        s=s+chr(num+a)
    return s


def abc_to_mobile(abc):
    a = ord('a')
    s = ''
    for char in abc:
        num = ord(char)
        s = s + str(num - a)
    return s



#发送短信验证码
class SendSMS:
    '''
    get参数:
    account=用户账号
    ts=yyyyMMddHHmmss
    pswd=用户密码
    mobile=1234545,1323434
    msg=【签名】正式内容
    needstatus=是否需要状态报告，取值true或false
    product=订购的产品id
    resptype='json'
    https://120.27.244.164/msg/HttpBatchSendSM?account=QT-yybb&
    pswd=Net263yy&mobile=17686988582&
    msg=%E3%80%90%E7%93%A6%E5%8A%9B%E5%B7%A5%E5%8E%82%E3%80%911234&
    needstatus=True&resptype=json
    '''

    def __init__(self,mobile,data,log=False):
        self.test=settings.CODE_TEST
        # account='QT-yybb'  #此家短信服务商提供的账号
        # pswd='Net263yy'    #此家短信服务商提供的密码
        account=settings.CODE_USER
        pswd=settings.CODE_PASSWORD
        self.url='http://120.27.244.164/msg/HttpBatchSendSM'
        log='瓦力工厂' if not log else log
        self.text='【{}】{}'.format(log,data)
        self.args={'account':account,'pswd':pswd,'mobile':mobile,
                   'msg':self.text,'needstatus':'True','resptype':'json'}
        self.get_url()

    def get_url(self):
        args_all=''
        for key in self.args:
            args='{}={}&'.format(key,self.args[key])
            args_all=args_all+args
        self.url=self.url+'?'+args_all[:-1]

    def send(self):
        if self.test:
            return self.test_send()
        response = requests.get(self.url)
        data=json.loads(response.text)
        status=data.get('result',400)

        #status为空时返回True
        if not status:
            return True
        #status不为空时代表有错误发生.生成错误信息并返回False告诉调用者发送失败了
        else:
            error={103:'提交过快（同时时间请求验证码的用户过多）',104:'短信平台暂时不能响应请求',
                   107:'包含错误的手机号码',109:'无发送额度（请联系管理员）',110:'不在发送时间内',
                   111:'短信数量超出当月发送额度限制，请联系管理员',400:'运营商没有返回正确的参数'}
            error_info=error.get(status)
            if error_info:
                self.error_info=error_info
            else:
                self.error_info='未知错误'
            return False

    def test_send(self):
        print('短信模块暂时不可用,程序即将启动模拟发送')
        info='模拟发送：向[{}]的手机号发送了[{}]'.format(self.args.get('mobile'),self.text)
        print(info)
        return True


#处理图片
class ImageHandler:

    def __init__(self,path):
        try:
            self.img=I.open(path)
            self._img=self.img.copy()
            self.img_validated=True
        except:
            self.img_validated=False

    def img_to_jpeg(self):
        if not self.img_validated:return None
        self.img=self.img.convert('RGB')
        return self.img

    def img_to_range(self,range_l=1000,range_h=1000):
        if not self.img_validated: return None
        L,H=self.img.size
        if L<=1000 and H<=1000:
            return self.img
        handler=self.img_to_range_of_L if L>H else self.img_to_range_of_H
        img=handler(self.img,range_l,range_h)
        return img

    def img_to_range_of_L(self, img,range_l,range_h):
        L, H = img.size
        ratio=range_l/L
        l=range_l
        h=int(H*ratio)
        img = img.resize((l,h), I.ANTIALIAS)
        return img

    def img_to_range_of_H(self, img,range_l,range_h):
        L, H = img.size
        ratio=range_h/H
        l=int(L*ratio)
        h=range_h
        img = img.resize((l,h), I.ANTIALIAS)
        return img































