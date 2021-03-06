# -*- coding: utf-8 -*-

from time import sleep
from random import shuffle

from wechat_chatplatform.handler.dingtalk_robot_handler.dingtalk_robot_handler import dingtalk_robot_handler
from wechat_chatplatform.common.choices import AdminUserStatus, Gender, Status, OrderRenew, AnchorStatus
from wechat_chatplatform.anchor.models import AnchorGroup, Anchor
from wechat_chatplatform.common.config import DOMAIN, ACCEPT_ORDER, GRAB_ORDER
from wechat_chatplatform.platform_admin.models import AdminUser


def send_new_applier_message(anchor_apply_record):
    admin_users = AdminUser.objects.values('nickname', 'dingtalk_robot').filter(status=AdminUserStatus.active.value)

    btns = list()
    btns.append(dict(
        title=u'查看详情',
        actionURL='http://www.suavechat.com/admin/#/manage/anchor'
    ))
    title = u'[有新店员申请待审核]'
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


def send_audit_pass_message(anchor, anchor_apply_record):
    admin_users = AdminUser.objects.values('nickname', 'dingtalk_robot').filter(status=AdminUserStatus.active.value)

    title = u'[申请审核通过]'
    text = u'**新店员已上架，详情:**\n\n- **昵称:** {}\n- **年龄:** {}\n- **星座:** {}\n- **性别:** {}\n- **城市:** {}\n' \
           u'- **等级:** {}\n- **审核人:** {}\n- **审核时间:** {}\n'
    text = text.format(anchor.nickname, anchor.age(), anchor.constellation(),
                       dict(Gender.GenderChoices.value)[anchor.gender], anchor.city, anchor.anchor_type.name,
                       anchor_apply_record.auditor.nickname,
                       anchor_apply_record.audit_date.strftime('%Y-%m-%d %H:%M:%S'))

    for admin_user in admin_users:
        if admin_user['dingtalk_robot']:
            _text = '**Hi, {}:**\n\n'.format(admin_user['nickname']) + text
            resp = dingtalk_robot_handler.send_markdown_card(token=admin_user['dingtalk_robot'], title=title,
                                                             text=_text)


def send_audit_reject_message(anchor_apply_record):
    admin_users = AdminUser.objects.values('nickname', 'dingtalk_robot').filter(status=AdminUserStatus.active.value)

    title = u'[申请审核拒绝]'
    text = u'**店员申请已被拒绝，详情:**\n\n- **申请编号:** {}\n- **昵称:** {}\n- **生日:** {}\n- **性别:** {}\n' \
           u'- **城市:** {}\n- **微信:** {}\n- **特长:** {}\n- **在线时间:** {}\n- **审核人:** {}\n- **审核时间:** {}\n'
    text = text.format(anchor_apply_record.anchor_apply_record_id, anchor_apply_record.nickname,
                       anchor_apply_record.birthday, dict(Gender.GenderChoices.value)[anchor_apply_record.gender],
                       anchor_apply_record.city, anchor_apply_record.wechat_id, anchor_apply_record.skill,
                       anchor_apply_record.online, anchor_apply_record.auditor.nickname,
                       anchor_apply_record.audit_date.strftime('%Y-%m-%d %H:%M:%S'))

    for admin_user in admin_users:
        if admin_user['dingtalk_robot']:
            _text = '**Hi, {}:**\n\n'.format(admin_user['nickname']) + text
            resp = dingtalk_robot_handler.send_markdown_card(token=admin_user['dingtalk_robot'], title=title,
                                                             text=_text)


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
    text = text.format(anchor.nickname, dict(OrderRenew.OrderRenewChoices.value)[order.renew],
                       order.product_anchor.product.product_type.name, order.product_anchor.product.name, order.number,
                       order.comment)
    resp = dingtalk_robot_handler.send_action_card(token=anchor.dingtalk_robot, title=title, text=text, btns=btns)


def send_accept_order_message(order):
    anchor = order.anchor
    if not anchor.dingtalk_robot:
        return

    title = '[接单成功]'
    text = '**Hi, {}:**\n\n**接单成功，订单详情:**\n- **订单类型:** {}\n- **服务类型:** {}\n- **时长:** {}\n- **数量:** {}\n' \
           '- **客户微信:** {}\n- **备注:** {}\n\n请尽快联系客户微信！'
    text = text.format(anchor.nickname, dict(OrderRenew.OrderRenewChoices.value)[order.renew],
                       order.product_anchor.product.product_type.name, order.product_anchor.product.name, order.number,
                       order.wechat_id, order.comment)
    resp = dingtalk_robot_handler.send_markdown_card(token=anchor.dingtalk_robot, title=title, text=text)


def send_random_order_message(order, tags=None):
    gender = order.gender
    if gender == Gender.mix.value:
        anchor_groups = AnchorGroup.objects.filter(status=Status.active.value)
        anchors = Anchor.objects.filter(dingtalk_robot__isnull=False, status=AnchorStatus.active.value,
                                        anchor_type__anchor_type_id__lte=order.anchor_type.anchor_type_id)
    elif gender == Gender.male.value:
        anchor_groups = AnchorGroup.objects.filter(status=Status.active.value, gender=Gender.male.value)
        anchors = Anchor.objects.filter(dingtalk_robot__isnull=False, status=AnchorStatus.active.value,
                                        anchor_type__anchor_type_id__lte=order.anchor_type.anchor_type_id,
                                        gender=Gender.male.value)
    else:
        anchor_groups = AnchorGroup.objects.filter(status=Status.active.value, gender=Gender.female.value)
        anchors = Anchor.objects.filter(dingtalk_robot__isnull=False, status=AnchorStatus.active.value,
                                        anchor_type__anchor_type_id__lte=order.anchor_type.anchor_type_id,
                                        gender=Gender.female.value)

    title = '[新随机订单]'
    text = '**[新随机订单]**\n\n**10秒后开始抢单，请及时查看工作通知抢单**\n\n**订单详情:**\n- **要求等级:** {}\n- **要求性别:** {}' \
           '\n- **服务类型:** {}\n- **时长:** {}\n- **数量:** {}\n- **要求标签:** {}\n- **备注:** {}\n\n高级店员可抢低级单\n\n' \
           '要求标签非硬性\n\n抢单成功后提供客户微信'
    text = text.format(order.anchor_type.name, dict(Gender.GenderChoices.value)[order.gender],
                       order.product_anchor.product.product_type.name, order.product_anchor.product.name, order.number,
                       tags, order.comment)
    for anchor_group in anchor_groups:
        resp = dingtalk_robot_handler.send_markdown_card(token=anchor_group.dingtalk_robot, title=title, text=text)

    sleep(10)
    text = '已开始抢单, 订单详情:\n- **要求等级:** {}\n- **要求性别:** {}\n- **服务类型:** {}\n- **时长:** {}\n' \
           '- **数量:** {}\n- **要求标签:** {}\n- **备注:** {}\n\n高级店员可抢低级单\n\n要求标签非硬性\n\n抢单成功后提供客户微信'
    text = text.format(order.anchor_type.name, dict(Gender.GenderChoices.value)[order.gender],
                       order.product_anchor.product.product_type.name, order.product_anchor.product.name, order.number,
                       tags, order.comment)
    shuffle(list(anchors))

    for anchor in anchors:
        btns = list()
        btns.append(dict(
            title=u'一键抢单',
            actionURL=DOMAIN + GRAB_ORDER.format(order.order_id, anchor.anchor_id)
        ))
        _text = '**Hi, {}:**\n\n'.format(anchor.nickname) + text
        resp = dingtalk_robot_handler.send_action_card(token=anchor.dingtalk_robot, title=title, text=_text, btns=btns)


def send_ungrab_order_message(anchor_id):
    anchor = Anchor.objects.get(anchor_id=anchor_id)

    title = '[抢单失败]'
    text = '**Hi, {}:**\n\n本次手速慢了，下次努力～'.format(anchor.nickname)

    resp = dingtalk_robot_handler.send_markdown_card(token=anchor.dingtalk_robot, title=title, text=text)
