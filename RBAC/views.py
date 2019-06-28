#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 14:59
# @Auther : Wshu

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from SysconfManage.views import strtopsd
from SysconfManage.SmallFun.checkpsd import checkpsd
from SysconfManage.SmallFun import mails
from . import forms, models
import django.utils.timezone as timezone
from django.contrib import auth
import datetime, hashlib

### 仪表盘
@login_required
def dashboard(request):
    return render(request, 'Dashboard.html')


### 首页
@login_required
def index(request):
    return render(request, 'RBAC/index.html')


### 登录
def login(request):
    error = ''
    if request.method == "POST":
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_get = User.objects.filter(username=username).first()
            if user_get:
                if user_get.profile.lock_time > timezone.now():
                    error = u'账号已锁定,' + str(user_get.profile.lock_time.strftime("%Y-%m-%d %H:%M")) + '后可尝试'
                else:
                    user = auth.authenticate(username=username, password=password)
                    if user:
                        user.profile.error_count = 0
                        user.save()
                        auth.login(request, user)
                        # 初始化权限
                        return HttpResponseRedirect('/user/')
                    else:
                        user_get.profile.error_cout += 1
                        if user_get.profile.error_cout >= 5:
                            user_get.profile.error_cout = 0
                            user_get.profile.lock_time = timezone.now() + datetime.timedelta(minutes=10)
                        user_get.save()
                        error = '登陆失败,已错误登录'+str(user_get.profile.error_count) +'次,5次后账号锁定',
            else:
                error = '请检查用户信息'
        else:
            error = u'请检查输入'
        return render(request,'RBAC/login.html',{'form':form,'error':error})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/user/')
        else:
            form = forms.SigninForm()
    return render(request, 'RBAC/login.html', {'form': form})


### 用户注册
@csrf_protect
def regist(request, argu):
    error = ''
    if argu == 'regist':
        if request.method == "POST":
            form = forms.RegistForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user_get = User.objects.filter(username=email)
                if user_get:
                    error = "用户名已存在"
                else:
                    userregist_get = models.UserRequest.objects.filter(email=email)
                    if userregist_get.count() > 2:
                        error = '用户已多次添加'
                    else:
                        area = form.cleaned_data['area']
                        request_type = form.cleaned_data['request_type']
                        urlarg = strtopsd(email)
                        models.UserRequest.objects.get_or_create(
                            email=email,
                            urlarg=urlarg,
                            area=area,
                            request_type=request_type
                        )
                        # res = mails.sendregistmail(email, urlarg)
                        error = '申请成功，审批通过后会向您发送邮件'
            else:
                error = '请检查输入'
        else:
            form = forms.RegistForm()
        return render(request, 'RBAC/registrequest.html', {'form': form, 'error': error})
    else:
        resetpsd = get_object_or_404(models.UserResetpsd, urlarg=argu)
        if resetpsd:
            email_get = resetpsd.email
            if request.method == 'POST':
                form = forms.ResetpsdForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    repassword = form.cleaned_data['repassword']
                    if checkpsd(password):
                        if password == repassword:
                            if email_get == email:
                                user = get_object_or_404(User, email=email)
                                if user:
                                    user.set_password(password)
                                    user.save()
                                    resetpsd.delete()
                                    return HttpResponseRedirect('/welcome/')
                                else:
                                    error = '用户信息有误'
                            else:
                                error = '用户邮箱不匹配'
                        else:
                            error = '两次密码不一致'
                    else:
                        error = '密码必须6位以上且包含字母、数字'
                else:
                    error = '请检查输入'
            else:
                form = forms.ResetpsdForm()
            return render(request, 'RBAC/')

### zhuce
@csrf_protect
def resetpasswd(request, argu='resetpsd'):
    error = ''
    if argu == 'resetpsd':
        if request.method == 'POST':
            form = forms.ResetpsdRequestForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = get_object_or_404(User, email=email)
                if user:
                    hash_res = hashlib.md5()
                    hash_res.update(make_password(email).encode('utf-8'))
                    urlarg = hash_res.hexdigest()
                    models.UserResetpsd.objects.get_or_create(
                        email=email,
                        urlarg=urlarg
                    )
                    res = mails.sendregistmail(email, urlarg)
                    if res:
                        error = '申请已发送，请检查邮件通知，请注意检查邮箱'
                    else:
                        error = '重置邮件发送失败，请重试'
                else:
                    error = '重置邮件发送失败，请重试'
            else:
                error = '请检查输入信息'
        else:
            form = forms.ResetpsdRequestForm()
        return render(request, 'RBAC/registrequest.html', {'form': form, 'error': error})
    else:
        resetpsd = get_object_or_404(models.UserResetpsd, urlarg=argu)
        if resetpsd:
            email_get = resetpsd.email
            if request.method == 'POST':
                form = forms.ResetpsdForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    repassword = form.cleaned_data['repassword']
                    if checkpsd(password):
                        if password == repassword:
                            if email_get == email:
                                user = get_object_or_404(User, email=email)
                                if user:
                                    user.set_password(password)
                                    user.save()
                                    resetpsd.delete()
                                    return HttpResponseRedirect('/view/')

                                else:
                                    error = '用户信息有误'
                            else:
                                error = '用户邮箱不匹配'
                        else:
                            error = '两次密码不一致'
                    else:
                        error = '密码必须6位以上且包含字母、数字'
                else:
                    error = '请检查输入'
            else:
                form = forms.ResetpsdForm()
            return render(request, 'RBAC/resetpsd.html', {'form': form, 'error': error, 'title': '重置'})



### 退出用户
@login_required
def logout(request):
    auth.logout(request)
    request.session.clear()
    return HttpResponseRedirect('/welcome/')



### 更改密码
@login_required
@csrf_protect
def changepwd(request):
    error = ''
    if request.method == 'POST':
        form = forms.ChangPasswdForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            re_new_password = form.cleaned_data['re_new_password']
            username = request.user.username
            if checkpsd(new_password):
                if new_password and new_password == re_new_password:
                    if old_password:
                        user = auth.authenticate(username=username, password=old_password)
                        if user:
                            user.set_password(new_password)
                            user.save()
                            auth.logout(request)
                            error = '修改成功'
                        else:
                            error = '账号信息错误'
                    else:
                        error = '请检查原始密码'
                else:
                    error = '两次密码不一致'
            else:
                error = '密码必须6位以上且包含字母、数字'
        else:
            error = '请检查输入'
        return render(request, 'formedit.html', {'form': form, 'post_url': changepwd, 'error':error})
    else:
        form = forms.ChangPasswdForm()
    return render(request, 'formedit.html', {'form': form, 'post_url': changepwd})

### 用户列表
@login_required
@csrf_protect
def userlist(request):
    user = request.user
    error = ''
    if user.is_superuser:
        area = models.Area.objects.filter(parent__isnull=True)
        city = models.Area.objects.filter(parent__isnull=False)
        return render(request, 'RBAC/userlist.html', {'area': area, 'city': city})
    else:
        error = '权限错误'
    return render(request, 'error.html', {'error':error})

### 用户提交注册处理
@login_required
@csrf_protect
def userregistaction(request):
    user = request.user
    error = ''
    if user.is_superuser():
        regist_id = request.POST.get('request_id')
        action = request.POST.get('action')
        userregist = get_object_or_404(models.UserRequest, id=regist_id)
        if userregist.is_check:
            error = '请勿重复审批'
        else:
            if action == 'access':
                userregist.is_check = True
                userregist.status = '1'
                res = mails.sendregistmail(userregist.email, userregist.urlarg)
                if res:
                    error = '添加成功，已向该员工发送邮件'
                else:
                    error = '添加成功，邮件发送失败，请重试'
                userregist.save()
            else:
                if action == 'deny':
                    userregist.is_check = True
                    userregist.status = '2'
                    userregist.is_use = True
                    userregist.save()
                    error = '已审批'
                else:
                    error = '未指定操作'
    else:
        error = '权限错误'
    return JsonResponse({'error': error})

### 注册用户列表
@login_required
def userregistlist(request):
    user = request.user
    error = ''
    if user.is_superuser:
        area = models.Area.objects.filter(parent__isnull=True)
        return render(request, 'RBAC/userregistlist.html', {'area': area})
    else:
        error = '权限错误'
    return render(request, 'error.html', {'error': error})


### 添加用户
@login_required
@csrf_protect
def user_add(request):
    user = request.user
    error = ''
    if user.is_superuser:
        if request.method == 'POST':
            form = forms.RegistForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user_get = User.objects.filter(username=email)
                if user_get:
                    error = '用户已存在'
                else:
                    userregist_get = models.UserRequest.objects.filter(email=email)
                    if userregist_get.count() > 2:
                        error = '用户已多次添加'
                    else:
                        area = form.cleaned_data['area']
                        request_type = form.cleaned_data['request_type']
                        urlarg = strtopsd(email)
                        models.UserRequest.objects.get_or_create(
                            email=email,
                            urlarg=urlarg,
                            area=area,
                            request_type=request_type,
                            is_check=True,
                            status='1',
                            action_user=user
                        )
                        res = mails.sendregistmail(email, urlarg)
                        if res:
                            error = '添加成功，已向该员工发送邮件'
                        else:
                            error = '添加成功，邮件发送失败，请重试'
            else:
                error = '请检查输入'
        else:
            form = forms.RegistForm()
    else:
        error = '请检查权限是否正确'
    return render(request, 'formedit.html', {'form': form, 'error': error})

