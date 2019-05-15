# -*- coding: utf-8 -*-

from wechat_chatplatform.handler.dingtalk_robot_handler.dingtalk_robot_handler import dingtalk_robot_handler
from wechat_chatplatform.common.choices import AdminUserStatus, Gender
from wechat_chatplatform.platform_admin.models import AdminUser


def send_new_applier_message(anchor_apply_record):
    admin_users = AdminUser.objects.values('nickname', 'dingtalk_robot').filter(status=AdminUserStatus.active.value)

    btns = list()
    btns.append(dict(
        title=u'查看详情',
        actionURL='http://www.suavechat.com/admin/unaudit/'
    ))
    title = '[有新店员申请待审核]'
    text = '有新店员申请待你审核，申请人详情:\n- **昵称:** {}\n- **生日:** {}\n- **性别:** {}\n- **城市:** {}\n- **微信:** {}\n' \
           '- **特长:** {}\n- **在线时间:** {}\n\n请联系申请人微信，核实情况后点击 [查看详情] 前往审核'
    text = text.format(anchor_apply_record.nickname, anchor_apply_record.birthday,
                       Gender.GenderChoices.value[anchor_apply_record.gender][1], anchor_apply_record.city,
                       anchor_apply_record.wechat_id, anchor_apply_record.skill, anchor_apply_record.online)

    for admin_user in admin_users:
        if admin_user['dingtalk_robot']:
            _text = '**Hi, {}:**\n\n'.format(admin_user['nickname']) + text
            resp = dingtalk_robot_handler.send_action_card(token=admin_user['dingtalk_robot'], title=title, text=_text,
                                                           btns=btns)


def send_new_order_message(order):
    pass