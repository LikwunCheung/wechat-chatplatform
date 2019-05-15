# -*- coding: utf-8 -*-

import requests

from .config import DINGTALK_ROBOT_URL


class DingTalkRobotError(BaseException):

    def __init__(self, ErrorInfo=None):
        super().__init__(self)
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info


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
        if resp.status_code != 200:
            raise DingTalkRobotError('Response Error: %s' % resp.content)
        return resp


dingtalk_robot_handler = DingTalkRobotHandler()
