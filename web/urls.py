#前台大堂端子路由
from django.urls import path,include
from web.views import index,cart,orders
urlpatterns = [
    path('', index.index,name="index"),

    #前台登陆提出的操作
    path('login',index.login,name = "web_login"),#加载登陆表单
    path('dologin',index.dologin,name = "web_dologin"),#执行登陆
    path('logout',index.logout,name = "web_logout"),#退出
    path('verify',index.verify,name = "web_verify"),#输出验证码

    #为路由添加请求前缀web/ ,凡是带此web前缀的url地址必须登陆后才可访问
    path("web/",include([
        path('',index.webindex,name="web_index"),#前台大堂点餐首页
        #购物车管理
        path('cart/add/<str:pid>',cart.add,name="web_cart_add"),#购物车添加
        path('cart/delete/<str:pid>',cart.delete,name="web_cart_delete"),#购物车添加
        path('cart/clear',cart.clear,name="web_cart_clear"),#购物车清空
        path('cart/change',cart.change,name="web_cart_change"),#购物车添加

        #订单处理路由
        path('orders/<int:pIndex>',orders.index,name='web_orders_index'),#订单浏览
        path('orders/insert',orders.insert,name='web_orders_insert'),#执行订单插入操作
        path('orders/detail',orders.detail,name='web_orders_detail'),#执行订单插入操作
        path('orders/status',orders.status,name='web_orders_status'),#执行订单插入操作

    ]))

]