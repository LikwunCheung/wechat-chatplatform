# -*- coding: utf-8 -*-

from wechat_chatplatform.common.utils import make_dict
from wechat_chatplatform.employee.models import Employee, EmployeeCity, EmployeeGroup, EmployeeTag, EmployeeType
from wechat_chatplatform.common.choices import EmployeeStatus


class EmployeeHandler(object):

    def __init__(self):
        pass

    def apply_employee(self, employee_info):
        keys = ['name', 'nickname', 'type_id', 'status', 'city_id', 'identity_type', 'identity', 'birthday', 'gender',
                'mobile', 'wechat_id', 'audio', 'avatar', 'img1', 'img2', 'img3', 'img4', 'join_date',
                'leave_date', 'slogan', 'tags']
        employee_info = make_dict(keys, employee_info)
        if not employee_info:
            raise ValueError()

        employee = Employee(name=employee_info['name'], nickname=employee_info['nickname'],
                            city_id=employee_info['city_id'], identity_type=employee_info['identity_type'],
                            identity=employee_info['identity'], birthday=employee_info['birthday'],
                            gender=employee_info['gender'], mobile=employee_info['mobile'],
                            wechat_id=employee_info['wechat_id'], audio=employee_info['audio'],
                            avatar=employee_info['avatar'], img1=employee_info['img1'], img2=employee_info['img2'],
                            img3=employee_info['img3'], slogan=employee_info['slogan'], tags=employee_info['tags'],
                            status=employee_info['status'])
        try:
            employee.save()
            return employee
        except Exception as e:
            print(e)
            return None


employee_handler = EmployeeHandler()
