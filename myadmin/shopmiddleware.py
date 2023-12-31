# 自定义中间件类(执行是否登录判断)
from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("ShopMiddleware")

    def __call__(self, request):
        path = request.path
        print("url:",path)

        #拦截，只有登录才可进入后台管理系统
        #判断管理后台是否登录
        #定义后台不登录也可直接访问的url列表,要不然会死循环
        urllist = ['/myadmin/login','/myadmin/logout','/myadmin/dologin','/myadmin/verify']
        #判断当前url地址是否是以/myadmin开头,并且不在urllist中，才做是否登录判断
        if re.match(r"^/myadmin",path) and (path not in urllist):
            #判断是否登录
            if "adminuser" not in request.session:
                #重定向到登录页
                return redirect(reverse('myadmin_login'))


        #大堂点餐请求判断，判断是否登录（session中是否有webuser）
        if re.match(r"^/web",path):
            #判断是否登录
            if "webuser" not in request.session:
                #重定向到登录页
                return redirect(reverse('web_login'))

        #判断移动端是否登录
        #定义移动端不登录也可直接访问的url列表,要不然会死循环
        urllist = ['/mobile/register','/mobile/doregister']
        #判断当前url地址是否是以/mobile开头,并且不在urllist中，才做是否登录判断
        if re.match(r"^/mobile",path) and (path not in urllist):
            #判断是否登录(在于session中没有mobileuser)
            if "mobileuser" not in request.session:
                #重定向到登录页
                return redirect(reverse('mobile_register'))



        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response