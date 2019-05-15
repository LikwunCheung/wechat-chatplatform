# -*- coding: utf-8 -*-

import requests

from .config import DINGTALK_ROBOT_URL


class DingTalkRobotHandler(object):

    def send_action_card(self, token, title, text, btns):
        content = dict(
            actionCard=dict(
                title=title,
                text=text,
                hideAvatar=0,
                btnOrientation=0,
                btns=btns
            ),
            msgtype='actionCard'
        )
        url = DINGTALK_ROBOT_URL.format(token)
        resp = requests.post(url, json=content)


dingtalk_robot_handler = DingTalkRobotHandler()
