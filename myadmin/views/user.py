#员工消息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from myadmin.models import User
from django.core.paginator import Paginator

from django.db.models import Q #封装或的条件搜索
from datetime import datetime
def index(request,pIndex=1):
    '''浏览信息'''
    umod = User.objects
    ulist = umod.filter(status__lt = 9)#1正常/2禁用/9删除

    #搜索框
    mywhere = []#搜索条件维持
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(Q(username__contains = kw) | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)
    #执行分页操作
    pIndex = int(pIndex)
    page = Paginator(ulist,5)#以每页5条数据分页
    maxpages = page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range #获取页码列表信息 ，获取page数目范围，返回一个range_interator对象
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/user/index.html",context)

def add(request):
    '''加载信息添加表单'''
    return render(request,"myadmin/user/add.html")
def insert(request):
    '''执行信息添加'''
    try:
        ob = User()#实例化当前对象
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']

        #将当前员工信息的密码做md5处理
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000,999999)
        s = request.POST['password']+str(n)#从表单中获取密码并添加干扰值
        md5.update(s.encode('utf-8'))#将要生产md5的子串放进去
        ob.password_hash = md5.hexdigest()#获取md5值
        ob.password_salt = n

        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"添加成功！"}
    except Exception as err:
        print(err)
        context = {'info':"添加失败！"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid=0):
    '''执行信息删除'''
    try:
        ob =User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)
def edit(request,uid=0):
    '''加载信息编辑表单'''
    try:
        ob = User.objects.get(id=uid)
        context = {'user': ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息"}
    return render(request, "myadmin/info.html", context)
def update(request,uid=0):
    '''执行信息编辑'''
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
    return render(request, "myadmin/info.html", context)


