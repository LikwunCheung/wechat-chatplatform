# -*- coding: utf-8 -*-

import ujson
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from wechat_chatplatform.platform_admin.models import AdminUser, AdminUserType
from wechat_chatplatform.common.choices import AdminUserStatus, Status
from wechat_chatplatform.common.utils.utils import init_http_bad_request, make_json_response, init_http_success, \
    check_api_key, make_dict
from wechat_chatplatform.common.config import DOMAIN, ADMIN_INDEX, LOGIN_REDIRECT


@require_http_methods(['POST'])
def admin_user_login(request):
    if request.method == 'POST':
        param = ujson.loads(request.body)
        username = param.get('user_name', None)
        password = param.get('password', None)

        try:
            admin_user = AdminUser.objects.get(status=AdminUserStatus.active.value, username=username,
                                               password=password)

            request.session['username'] = username
            request.session['type'] = admin_user.admin_user_type.tag
            request.session['is_admin'] = True
            request.session['is_anchor'] = False
            request.session['is_user'] = False
            request.session['is_login'] = True
            request.session.set_expiry(15 * 60)
        except Exception as e:
            resp = init_http_bad_request('Error Username Or Password')
            return make_json_response(HttpResponseBadRequest, resp)

        # redirect = param.get('redirect', None)
        return HttpResponse(ujson.dumps(dict(data=dict(token=''.join(uuid.uuid1().__str__().split('-'))))),
                            content_type='application/json')

    return HttpResponseBadRequest()


@require_http_methods(['POST'])
def admin_user_logout(request):
    if request.method == 'POST':
        if request.session.get('username', None):
            request.session.clear()
        else:
            HttpResponse(status=700)
    return HttpResponse()


@require_http_methods(['GET'])
@check_api_key
def get_user_info(request, *args, **kwargs):
    username = request.session.get('username', None)

    if not username:
        return HttpResponse(status=700)

    admin_user = AdminUser.objects.get(status=AdminUserStatus.active.value, username=username)

    resp = init_http_success()
    resp['data'] = dict(
        nickname=admin_user.nickname,
        type=admin_user.admin_user_type,
        avatar=''
    )

    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@check_api_key
def admin_user_router(request, *args, **kwargs):
    username = request.session.get('username', None)
    user_type = request.session.get('type', None)
    is_admin = request.session.get('is_admin', False)
    is_login = request.session.get('is_login', False)

    if not (username and user_type == 'super' and is_admin and is_login):
        return HttpResponse(status=700)

    request.session.set_expiry(15 * 60)

    if request.method == 'GET':
        return admin_user_get(request)
    elif request.method == 'POST':
        return admin_user_post(request)


def admin_user_get(request):
    admin_users = AdminUser.objects.filter(status=AdminUserStatus.active.value)

    results = [dict(
        id=admin_user.admin_user_id,
        nickname=admin_user.nickname,
        username=admin_user.username,
        password=admin_user.password,
        type=admin_user.admin_user_type,
        mobile=admin_user.mobile,
        dingtalk_robot=admin_user.dingtalk_robot,
        wechat_id=admin_user.wechat_id,
        join_date=admin_user.join_date,
    ) for admin_user in admin_users]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def admin_user_post(request):
    keys = ['username', 'password', 'nickname', 'dingtalk_robot', 'mobile', 'wechat_id', 'level']
    params = ujson.loads(request.body)
    params = make_dict(keys, params)

    try:
        params.update(dict(
            admin_user_type=AdminUserType.objects.get(admin_user_type_id=params.pop('level'), status=Status.active.value),
            dingtalk_mobile=params['mobile'] if 'mobile' in params else None
        ))

        admin_user = AdminUser(**params)
        admin_user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


@require_http_methods(['POST'])
@check_api_key
def admin_user_update(request):
    username = request.session.get('username', None)
    user_type = request.session.get('type', None)
    is_admin = request.session.get('is_admin', False)
    is_login = request.session.get('is_login', False)

    if not (username and user_type == 'super' and is_admin and is_login):
        return HttpResponse(status=700)

    keys = ['id', 'password', 'nickname', 'dingtalk_robot', 'mobile', 'wechat_id', 'level']
    params = ujson.loads(request.body)
    params = make_dict(keys, params)

    try:
        admin_user = AdminUser.objects.get(admin_user_id=params.pop('id'), status=Status.active.value)
        admin_user.update(**params)
        admin_user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


@require_http_methods(['POST'])
@check_api_key
def admin_user_remove(request, *args, **kwargs):
    username = request.session.get('username', None)
    user_type = request.session.get('type', None)
    is_admin = request.session.get('is_admin', False)
    is_login = request.session.get('is_login', False)

    if not (username and user_type == 'super' and is_admin and is_login):
        return HttpResponse(status=700)

    params = ujson.loads(request.body)

    try:
        admin_user = AdminUser.objects.get(admin_user_id=params.pop('id'), status=Status.active.value)
        admin_user.delete()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)
