# -*- coding: utf-8 -*-

from wechat_chatplatform.common.utils.utils import make_dict
from wechat_chatplatform.anchor.models import Anchor, AnchorCity, AnchorGroup, AnchorTag, AnchorType
from wechat_chatplatform.common.choices import AnchorStatus


class AnchorHandler(object):

    def __init__(self):
        pass

    def apply_anchor(self, anchor_info):
        keys = ['name', 'nickname', 'type_id', 'status', 'city_id', 'identity_type', 'identity', 'birthday', 'gender',
                'mobile', 'wechat_id', 'audio', 'avatar', 'image', 'join_date', 'leave_date', 'slogan', 'tags']
        anchor_info = make_dict(keys, anchor_info)
        if not anchor_info:
            raise ValueError()

        anchor = Anchor(name=anchor_info['name'], nickname=anchor_info['nickname'], city_id=anchor_info['city_id'],
                        identity_type=anchor_info['identity_type'], identity=anchor_info['identity'],
                        birthday=anchor_info['birthday'], gender=anchor_info['gender'], mobile=anchor_info['mobile'],
                        wechat_id=anchor_info['wechat_id'], audio=anchor_info['audio'], avatar=anchor_info['avatar'],
                        image=anchor_info['image'], slogan=anchor_info['slogan'], tags=anchor_info['tags'],
                        status=anchor_info['status'])
        try:
            anchor.save()
            return anchor
        except Exception as e:
            print(e)
            return None


anchor_handler = AnchorHandler()
