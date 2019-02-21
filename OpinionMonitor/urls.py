from django.conf.urls import url
import OMDjango.settings as settings
from django.views.static import serve

from . import views

app_name = 'OpinionMonitor'
urlpatterns = [
    # 首页
    url(r'^$', views.index, name='index'),
    # 热点图
    url(r'^hot/$', views.hot, name='hot'),
    # 相似文本
    url(r'^sim_txt/', views.sim_txt, name='sim'),
    url(r'^sim_txt_result/', views.sim_txt_result, name='sim_result'),
    # 搜索页面
    url(r'^search/$', views.search, name='search'),
    url(r'^search/kwl/', views.get_keyword_list, name='kwl'),
    url(r'^search/fpl/', views.get_focus_passge_list, name='fpl')
]
