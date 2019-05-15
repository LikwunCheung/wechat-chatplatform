# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.employee.models import Employee, EmployeeType, EmployeeGroup, EmployeeCity, EmployeeTag
from wechat_chatplatform.common.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.handler.employee_handler import EmployeeHandler


employee_handler = EmployeeHandler()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def anchor_apply_router(requset, *args, **kwargs):
    if requset.method == 'POST':
        return anchor_apply_post(requset)
    return HttpResponseNotAllowed()


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_apply_unaudit_router(requset, *args, **kwargs):
    if requset.method == 'GET':
        return anchor_apply_unaudit_get(requset)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def anchor_apply_action_router(requset, *args, **kwargs):
    action = None
    for arg in args:
        if isinstance(args, dict):
            action = args.get('action', None)

    if requset.method == 'POST':
        return anchor_apply_action_post(requset, action)
    return HttpResponseNotAllowed()


def anchor_apply_post(request):
    keys = ['name', 'nickname', 'city_id', 'identity_type', 'identity', 'birthday', 'gender', 'mobile', 'wechat_id',
            'audio', 'avatar', 'image', 'slogan', 'tags']

    param = ujson.loads(request.body)
    print(param)

    try:
        for i in range(len(param['image'])):
            param.update({'img{}'.format(i + 1): param['image'][i]})
        param.pop('image')
        param['tags'] = ','.join([str(tag) for tag in param['tags']])
        param['city_id'] = EmployeeCity.objects.get(city_id=param['city_id'])
        param['identity_type'] = IdentityType.identity.value
    except Exception as e:
        print(e)
        resp = init_http_bad_request('AttributeError')
        return make_json_response(HttpResponseBadRequest, resp)

    param.update(dict(
        status=EmployeeStatus.unaudit.value
    ))

    employee = employee_handler.apply_employee(param)

    resp = init_http_success()
    resp['data'].update(dict(id=employee.employee_id))
    return make_json_response(HttpResponse, resp)


def anchor_apply_unaudit_get(request):

    employees = Employee.objects.filter(status=EmployeeStatus.unaudit.value)
    results = []

    for employee in employees:
        img = []
        tags = []
        img.append(employee.img1) if employee.img1 else None
        img.append(employee.img2) if employee.img2 else None
        img.append(employee.img3) if employee.img3 else None
        if employee.tags:
            _tags = employee.tags.split(',')
            for tag in _tags:
                try:
                    tag_name = EmployeeTag.objects.values('name').get(tag_id=int(tag))
                    tags.append(tag_name['name'])
                except Exception as e:
                    continue

        results.append(dict(
                id=employee.employee_id,
                name=employee.name,
                nickname=employee.nickname,
                city=employee.city_id.name,
                identity=employee.identity,
                birthday=employee.birthday.strftime('%Y-%m-%d'),
                gender=Gender.GenderChoices.value[employee.gender][1],
                mobile=employee.mobile,
                wechat_id=employee.wechat_id,
                audio=employee.audio,
                img=img,
                slogan=employee.slogan,
                tags=tags
            )
        )

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_apply_action_post(request, action):
    employee_id = request.POST.get('id', None)
    if not employee_id:
        resp = init_http_bad_request('No Employee ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Exception as e:
        resp = init_http_bad_request('No Match Employee')
        return make_json_response(HttpResponseBadRequest, resp)

    if employee.status != EmployeeStatus.unaudit:
        resp = init_http_bad_request('Employee Audited')
        return make_json_response(HttpResponseBadRequest, resp)

    if action == 'pass':
        level = request.POST.get('level', 1)
        employee.type_id = EmployeeType.objects.get(type_id=level)
        employee.status = EmployeeStatus.active.value
        employee.join_date = now()
        employee.audit_date = now()
        employee.auditor = None
        employee.save()
    elif action == 'reject':
        employee.status = EmployeeStatus.audit_fail.value
        employee.audit_date = now()
        employee.auditor = None
        employee.save()

    results = dict(
        id=employee.employee_id,
        name=employee.name,
        status=dict(EmployeeStatus.EmployeeStatusChoice.value)[employee.status]
    )
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
