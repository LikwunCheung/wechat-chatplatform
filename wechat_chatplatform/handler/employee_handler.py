# -*- coding: utf-8 -*-

from wechat_chatplatform.common.utils import make_dict
from wechat_chatplatform.employee.models import Employee, EmployeeCity, EmployeeGroup, EmployeeTag, EmployeeType
from wechat_chatplatform.common.choices import EmployeeStatus


class EmployeeHandler(object):

    def __init__(self):
        pass

    def create_new_employee(self, **kwargs):
        keys = ['name', 'nickname', 'type_id', 'status', 'city_id', 'identity_type', 'identity', 'birthday', 'gender',
                'mobile', 'dingtalk_id', 'wechat_id', 'audio', 'avatar', 'img1', 'img2', 'img3', 'img4', 'join_date',
                'leave_date', 'slogan', 'tags']
        employee_info = make_dict(keys=keys, kwargs=kwargs)
        employee = Employee.objects.create(employee_info)
        employee.status = Employee.STATUS_CHOICES[EmployeeStatus.unaudit.value]


employee_handler = EmployeeHandler()
