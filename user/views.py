from django.shortcuts import render, redirect, HttpResponse
from user.models import User


def login_required(view_func):
    """登录判断装饰器"""

    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('islogin'):
            # 用户已登录，调用对应视图
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录，跳转到登录页
            return redirect('/login/')

    return wrapper


def login(request):

    return render(request, 'user/login.html')


def loginCheck(request):
    """登录校验"""
    # 获取用户名和密码

    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        message = ''

        # 进行效验，返回json数据
        try:
            user = User.objects.get(account=account)
            # userAccount = user.account

        except:
            message = 'Your account is wrong !'
            return render(request, 'user/login.html', locals())

        else:
            if user.password == password:
                # 记住用户登录状态，只有session中有islogin，就认为用户已登录
                response = redirect('/home')
                request.session['islogin'] = True
                request.session['account'] = user.account

                if user.authority == 1:
                    return redirect('/polyclinicDepartment/')

                else:
                    return redirect('/login/')

            else:

                message = 'Your password is wrong !'
                return render(request, 'user/login.html', locals())


def logout(request):

    request.session.clear()

    return redirect('/login/')


@login_required
def profileAdmin(request):
    """用户资料"""

    if 'account' in request.session:
        userAccount = request.session['account']
        user = User.objects.get(account=userAccount)

    return render(request, 'user/adminProfile.html', locals())


@login_required
def editAdminProfile(request, user_id):
    """编辑账户信息"""

    user = User.objects.get(account=request.session['account'])

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # 更新数据库
        user.name = name
        user.password = password
        user.save()

        if user.authority == 1:
            return redirect('/profileAdmin/', locals())

        elif user.authority == 2:
            return redirect('/profileUser/', locals())
