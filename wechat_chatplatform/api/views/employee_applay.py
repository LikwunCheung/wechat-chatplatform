# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods

from wechat_chatplatform.employee.models import Employee, EmployeeType, EmployeeGroup, EmployeeCity
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
def anchor_apply_pass_router(requset, *args, **kwargs):
    if requset.method == 'POST':
        return anchor_apply_pass_post(requset)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def anchor_apply_reject_router(requset, *args, **kwargs):
    if requset.method == 'POST':
        return anchor_apply_reject_post(requset)
    return HttpResponseNotAllowed()


def anchor_apply_post(request):
    keys = ['name', 'nickname', 'city_id', 'identity_type', 'identity', 'birthday', 'gender', 'mobile', 'wechat_id',
            'audio', 'avatar', 'image', 'slogan', 'tags']

    param = ujson.loads(request.body)

    try:
        for i in range(len(param['image'])):
            param.update({'img{}'.format(i + 1): param['image'][i]})
        param.pop('image')
        param['tags'] = ','.join([str(tag) for tag in param['tags']])
        employee_city = EmployeeCity.objects.get(city_id=param['city_id'])
        param['city_id'] = employee_city
    except Exception as e:
        print(e)
        resp = init_http_bad_request('AttributeError')
        return make_json_response(HttpResponseBadRequest, resp)

    param.update(dict(
        status=EmployeeStatus.unaudit.value
    ))

    print(param)
    employee = employee_handler.create_new_employee(param)

    temp_id = employee.employee_id
    employee = Employee.objects.get(employee_id=temp_id)
    print(employee.nickname)
    resp = init_http_success()
    resp['data'].update(dict(id=temp_id))
    return make_json_response(HttpResponse, resp)


def anchor_apply_unaudit_get(request):
    employees = Employee.objects.filter(status=EmployeeStatus.unaudit.value)
    print(employees)
    results = dict()
    for employee in employees:
        img = []
        img.append(employee.img1) if employee.img1 else None
        img.append(employee.img2) if employee.img2 else None
        img.append(employee.img3) if employee.img3 else None
        results.update({
            employee.employee_id: dict(
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
                tags=employee.tags
            )
        })
    print(results)
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_apply_pass_post(request):
    pass


def anchor_apply_reject_post(request):
    pass