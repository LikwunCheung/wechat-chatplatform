# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class IdentityType(Enum):
    identity = 0
    passport = 1
    driver = 2

    IdentityTypeChoice = (
        (identity, u'身份证'),
        (passport, u'护照'),
        (driver, u'驾驶证'),
    )


@unique
class EmployeeStatus(Enum):
    leave = 0
    active = 1
    unaudit = 2
    audit_fail = 3

    EmployeeStatusChoice = (
        (leave, u'离职'),
        (active, u'在职'),
        (unaudit, u'待审核'),
        (audit_fail, u'审核失败'),
    )


@unique
class AdminUserStatus(Enum):
    leave = 0
    active = 1

    AdminUserStatusChoice = (
        (leave, u'离职'),
        (active, u'在职'),
    )


@unique
class Gender(Enum):
    female = 0
    male = 1
    mix = 2

    GenderChoices = (
        (female, u'女'),
        (male, u'男'),
        (mix, u'混合'),
    )


@unique
class Status(Enum):
    inactive = False
    active = True

    StatusChoice = (
        (inactive, u'失效'),
        (active, u'激活')
    )


@unique
class OrderStatus(Enum):
    delete = 0
    unpaid = 1
    unacknowledge = 2
    ungrab = 3
    salary = 4
    close = 5
    change = 6
    overtime = 7

    OrderStatusChoices = (
        (delete, u'已删除'),
        (unpaid, u'待付款'),
        (unacknowledge, u'待接单'),
        (ungrab, u'待抢单'),
        (salary, u'待发放工资'),
        (close, u'正常关闭'),
        (change, u'已换人'),
        (overtime, u'付款超时失败'),
    )


@unique
class ExtendStatus(Enum):
    first = False
    extend = True

    ExtendStatusChoice = (
        (first, u'首单'),
        (extend, u'续单'),
    )


if __name__ == '__main__':
    print(EmployeeStatus.leave.value)
