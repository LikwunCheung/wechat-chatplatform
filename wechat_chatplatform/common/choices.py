# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class IdentityType(Enum):
    identity = 0
    passport = 1
    driver = 2


@unique
class EmployeeStatus(Enum):
    leave = 0
    active = 1
    unaudit = 2
    audit_fail = 3


@unique
class Gender(Enum):
    female = 0
    male = 1
    mix = 2


@unique
class Status(Enum):
    inactive = False
    active = True



if __name__ == '__main__':
    print(EmployeeStatus.leave.value)
