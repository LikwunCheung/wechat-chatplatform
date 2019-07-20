# -*- coding: utf-8 -*-


APP_ID = 'wx67e680017dca0b2b'
APP_SECRET = '3771aed06e46c0c8048ce4df2dc7bfba'
# APP_ID = 'wx1c5f306604b0728c'
# APP_SECRET = '9ac35f05b4aba5dc4b35b401a16291f5'

ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
ACCESS_TOKEN_GRANT_TYPE = 'client_credential'

USER_CODE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
USER_CODE_REDIRECT_URL = 'http://www.suavechat.top/api/v1/wxoauth/recall/'
USER_CODE_RESPONSE_TYPE = 'code'
USER_CODE_SCOPE = 'snsapi_userinfo'
USER_CODE_WECHAT = '#wechat_redirect'

USER_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
USER_TOKEN_GRANT_TYPE = 'authorization_code'

USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo'
USER_INFO_LANG = 'zh_CN'




