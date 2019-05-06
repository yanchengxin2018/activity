from django.conf.urls import url,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from main import views
from django.views.static import serve

router=DefaultRouter()


#测试
router.register('test',views.TestViewSet,base_name='test')
#手机验证码
router.register('code',views.CodesViewSet)
#提交手机号,已废弃
# router.register('mobile',views.ActorMobileViewSet)
#提交手机号及图片
router.register('img',views.ActorImgViewSet,base_name='img')
#选手排名
router.register('rank',views.RankingViewSet)

#启动或者关闭抽奖
router.register('start',views.StartLuckViewSet,base_name='start')
#后台通过密码查看中奖者
router.register('look',views.LookLuckViewSet,base_name='look')
#这个用户是否抽过
router.register('luck',views.AManOfGoodLuckViewSet,base_name='luck')

#GO抽奖
router.register('luck_finish',views.AlertLuckStatusViewSet,base_name='luckbutno')

#点击机器人
router.register('play',views.PlayViewSet,base_name='play')



urlpatterns = [
    url(r'^api/',include(router.urls)),
    url(r'^assistance/(?P<mobile>[a-k]+)/',views.CountViewSet.as_view({'get':'list'})),

    url(r'^image_dir/(?P<path>.+)$',serve,{"document_root":settings.STATIC_ROOT}),

]















