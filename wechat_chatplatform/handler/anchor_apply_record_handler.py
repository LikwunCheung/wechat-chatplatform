# -*- coding: utf-8 -*-

from django.utils.timezone import now

from wechat_chatplatform.common.utils.utils import make_dict
from wechat_chatplatform.anchor.models import AnchorApplyRecord
from wechat_chatplatform.common.choices import AnchorAuditStatus


class AnchorApplyRecordHandler(object):

    def __init__(self):
        pass

    def apply_anchor(self, anchor_info):
        keys = ['nickname', 'city', 'birthday', 'gender', 'wechat_id', 'audio', 'avatar', 'image', 'slogan', 'tags',
                'skill', 'experience', 'occupation', 'online']
        anchor_info = make_dict(keys, anchor_info)
        if not anchor_info:
            raise ValueError()

        anchor_apply_record = AnchorApplyRecord(nickname=anchor_info['nickname'], city=anchor_info['city'],
                                                birthday=anchor_info['birthday'], gender=anchor_info['gender'],
                                                wechat_id=anchor_info['wechat_id'], audio=anchor_info['audio'],
                                                avatar=anchor_info['avatar'], image=anchor_info['image'],
                                                slogan=anchor_info['slogan'], tags=anchor_info['tags'],
                                                skill=anchor_info['skill'], experience=anchor_info['experience'],
                                                occupation=anchor_info['occupation'], online=anchor_info['online'],
                                                status=AnchorAuditStatus.unaudit.value, apply_date=now())
        try:
            anchor_apply_record.save()
            return anchor_apply_record
        except Exception as e:
            print(e)
            return None


anchor_apply_record_handler = AnchorApplyRecordHandler()
