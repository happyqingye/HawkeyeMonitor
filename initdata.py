#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/16 12:36
# @Auther : Wshu


import django, os

def initment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC import models
    menu_list = [
                {'title': '资产管理', 'icon': "&#xe653;"},
                {'title': '网络映射', 'icon': "&#xe674;"},
                {'title': '漏洞管理', 'icon': "&#xe663;"},
                {'title': '微信监控', 'icon': "&#xe677;"},
                {'title': '微博监控', 'icon': "&#xe675;"},
                {'title': '任务管理', 'icon': "&#xe628;"},
                {'title': '报表中心', 'icon': "&#xe629;"},
                {'title': '用户管理', 'icon': "&#xe770;"},
    ]

    for item in menu_list:
        models.Menu.objects.get_or_create(
            title=item['title'],
            icon=item['icon']
        )
    submain_list = [
        ## 资产管理
        {'title': '资产列表', 'icon': "&#xe60a;", 'parent_title': '资产管理'},
        {'title': '资产审批', 'icon': "&#xe60b;", 'parent_title': '资产管理'},
        {'title': '交接审批', 'icon': "&#xe607;", 'parent_title': '资产管理'},

        ## 网络映射
        {'title': '映射列表', 'icon': "&#xe60a;", 'parent_title': '网络映射'},

        ## 漏洞管理
        {'title': '漏洞列表', 'icon': "&#xe756;", 'parent_title': '漏洞管理'},
        {'title': '漏洞库', 'icon': "&#xe656;", 'parent_title': '漏洞管理'},

        ## 微信公众号
        {'title': '公众号列表', 'icon': '&#xe608;', 'parent_title': '微信监控'},
        {'title': '公众号审查', 'icon': '&#xe63c;', 'parent_title': '微信监控'},
        ## 新浪微博
        {'title': '微博列表', 'icon': '&#xe608;', 'parent_title': '微博监控'},
        {'title': '微博审查', 'icon': '&#xe63c;', 'parent_title': '微博监控'},

        ## 任务管理
        {'title': '任务列表', 'icon': "&#xe60a;", 'parent_title': '任务管理'},
        {'title': '任务审批', 'icon': "&#xe60b;", 'parent_title': '任务管理'},

        ## 报表管理
        {'title': '基础报表', 'icon': "&#xe654;", 'parent_title': '报表中心'},

        ## 用户管理
        {'title': '用户列表', 'icon': "&#xe60a;", 'parent_title': '用户管理'},
        {'title': '用户审批', 'icon': "&#xe60b;", 'parent_title': '用户管理'},
    ]

    for item in submain_list:
        models.Menu.objects.get_or_create(
            title=item['title'],
            icon=item['icon'],
            parent=models.Menu.objects.filter(title=item['parent_title']).first(),
        )


    permission_list = [
        {'title': '资产列表', 'url': '/asset/user/', 'is_menu': True, 'menu_title': '资产列表'},
        {'title': '资产审批', 'url': '/asset/request/', 'is_menu': True, 'menu_title': '资产审批'},
        {'title': '交接审批', 'url': '/asset/handover/', 'is_menu': True, 'menu_title': '交接审批'},
        {'title': '资产指定', 'url': '/asset/manage/', 'is_menu': False},

        {'title': '映射列表', 'url': '/mapped/', 'is_menu': True, 'menu_title': '映射列表'},

        {'title': '漏洞操作', 'url': '/vuln/manage/', 'is_menu': False},
        {'title': '漏洞列表', 'url': '/vuln/user/', 'is_menu': True, 'menu_title': '漏洞列表'},
        {'title': '漏洞库', 'url': '/vuln/cnvd/', 'is_menu': True, 'menu_title': '漏洞库'},

        {'title': '公众号列表', 'url': '/wxlist/', 'is_menu': True, 'menu_title': '公众号列表'},
        {'title': '公众号审查', 'url': '/wxcheck/', 'is_menu': False, 'menu_title': '公众号审查'},

        {'title': '微博列表', 'url': '/wblist/', 'is_menu': True, 'menu_title': '微博列表'},
        {'title': '微博审查', 'url': '/wbcheck/', 'is_menu': False, 'menu_title': '微博审查'},

        {'title': '任务列表', 'url': '/task/user/', 'is_menu': True, 'menu_title': '任务列表'},
        {'title': '任务审批', 'url': '/task/request/', 'is_menu': True, 'menu_title': '任务审批'},
        {'title': '扫描同步', 'url': '/task/manage/', 'is_menu': False},

        {'title': '基础报表', 'url': '/chart/', 'is_menu': True, 'menu_title': '基础报表'},

        {'title': '用户列表', 'url': '/manage/user/', 'is_menu': True, 'menu_title': '用户列表'},
        {'title': '用户审批', 'url': '/manage/userrequest/', 'is_menu': True, 'menu_title': '用户审批'},

    ]
    for item in permission_list:
        permission_tup = models.Permission.objects.get_or_create(
            title=item['title'],
            url=item['url']
        )
        permission = permission_tup[0]
        if item['is_menu']:
            permission.menu = models.Menu.objects.filter(title=item['menu_title']).first()
            permission.save()
    print('initrole ok')

# 初始化区域
def initarea():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC.models import Area
    area_list =[
        {'name': '华北'},
        {'name': '华南'},
        {'name': '华东'},
        {'name': '华中'},
        ]
    for item in area_list:
        Area.objects.get_or_create(name=item['name'])
    print('initrole ok')


def initrole():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC.models import Role, Permission
    permissions_list = [
        {'title': '安全管理员', 'permissions': '资产列表'},
        {'title': '安全管理员', 'permissions': '资产审批'},
        {'title': '安全管理员', 'permissions': '交接审批'},
        {'title': '安全管理员', 'permissions': '资产指定'},
        {'title': '安全管理员', 'permissions': '映射列表'},
        {'title': '安全管理员', 'permissions': '漏洞操作'},
        {'title': '安全管理员', 'permissions': '漏洞列表'},
        {'title': '安全管理员', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '公众号列表'},
        {'title': '安全管理员', 'permissions': '公众号审查'},
        {'title': '安全管理员', 'permissions': '微博列表'},
        {'title': '安全管理员', 'permissions': '微博审查'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '安全管理员', 'permissions': '任务审批'},
        {'title': '安全管理员', 'permissions': '扫描同步'},
        {'title': '安全管理员', 'permissions': '基础报表'},
        {'title': '安全管理员', 'permissions': '用户列表'},
        {'title': '安全管理员', 'permissions': '用户审批'},

        {'title': '运维管理员', 'permissions': '资产列表'},
        {'title': '运维管理员', 'permissions': '漏洞列表'},
        {'title': '运维管理员', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '运维管理员', 'permissions': '基础报表'},

        {'title': '网络管理员', 'permissions': '资产列表'},
        {'title': '网络管理员', 'permissions': '漏洞列表'},
        {'title': '网络管理员', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '网络管理员', 'permissions': '基础报表'},

        {'title': '业务负责人', 'permissions': '资产列表'},
        {'title': '业务负责人', 'permissions': '漏洞列表'},
        {'title': '业务负责人', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '业务负责人', 'permissions': '基础报表'},
    ]
    for item in permissions_list:
        role_list = Role.objects.get_or_create(title=item['title'])
        role_list[0].permissions.add(Permission.objects.filter(title=item['permissions']).first())
        role_list[0].save()

    print('initrole ok')


def initsuperuser():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC.models import Role
    from django.contrib.auth.models import User
    user_manage_list = User.objects.filter(is_superuser=True)
    role = Role.objects.filter(title='安全管理员').first()
    for user in user_manage_list:
        user.profile.roles.add(role)
        user.save()
    print('initsuperuser ok')


if __name__ == '__main__':
    initment()
    # initarea()
    initrole()
    # initsuperuser()