# -*- coding: utf-8 -*-

from wechat_chatplatform.handler.dingtalk_robot_handler.dingtalk_robot_handler import dingtalk_robot_handler
from wechat_chatplatform.common.choices import AdminUserStatus, Gender, Status, OrderRenew
from wechat_chatplatform.anchor.models import AnchorGroup
from wechat_chatplatform.common.config import DOMAIN, ACCEPT_ORDER, GRAB_ORDER
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
    anchor = order.anchor
    if not anchor.dingtalk_robot:
        return

    btns = list()
    btns.append(dict(
        title=u'确认接单',
        actionURL=DOMAIN + ACCEPT_ORDER.format(order.order_id)
    ))

    title = '[你有一个新订单]'
    text = '**Hi, {}:**\n\n你有一个新订单待接单，订单详情:\n- **订单类型:** {}\n- **类型:** {}\n- **时长:** {}\n' \
           '- **数量:** {}\n- **备注:** {}\n\n接单后提供客户微信'
    text = text.format(anchor.nickname, dict(OrderRenew.OrderRenewChoices.value)[order.renew_order],
                       order.product_anchor.product.product_type.name, order.product_anchor.product.name, order.number,
                       order.comment)
    resp = dingtalk_robot_handler.send_action_card(token=anchor.dingtalk_robot, title=title, text=text, btns=btns)


def send_accept_order_message(order):
    anchor = order.anchor
    if not anchor.dingtalk_robot:
        return

    title = '[接单成功]'
    text = '**Hi, {}:**\n\n接单成功:\n- **订单类型:** {}\n- **服务类型:** {}\n- **时长:** {}\n- **数量:** {}\n' \
           '- **客户微信:** {}\n- **备注:** {}\n'
    text = text.format(anchor.nickname, dict(OrderRenew.OrderRenewChoices.value)[order.renew_order],
                       order.product_anchor.product.product_type.name, order.product_anchor.product.name, order.number,
                       order.wechat_id, order.comment)
    resp = dingtalk_robot_handler.sned_markdown_card(token=anchor.dingtalk_robot, title=title, text=text)


def send_random_order_message(order, tags=None):
    anchor_groups = AnchorGroup.objects.filter(status=Status.active.value)

    btns = list()
    btns.append(dict(
        title=u'前往抢单',
        actionURL=DOMAIN + GRAB_ORDER.format(order.order_id)
    ))

    title = '[新随机订单]'
    text = '**[新随机订单]**\n\n订单详情:\n- **店员等级:** {}\n- **店员性别:** {}\n- **服务类型:** {}\n- **时长:** {}\n' \
           '- **数量:** {}\n- **标签:** {}\n- **备注:** {}\n\n抢单后提供客户微信'
    text = text.format(order.anchor_type_id.name, dict(Gender.GenderChoices.value)[order.gender],
                       order.product_id.product_id.product_type_id.name, order.product_id.product_id.name, order.number,
                       tags, order.comment)
    for anchor_group in anchor_groups:
        resp = dingtalk_robot_handler.send_action_card(token=anchor_group.dingtalk_robot, title=title, text=text,
                                                       btns=btns)
