# Naver Login + client_id, secret_id
NAVER_CALLBACK_URL = "http://127.0.0.1:8000/accounts/naver/callback/"
NAVER_STATE = "naver_login"
NAVER_SCOPE = ""
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize"
NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
NAVER_PROFILE_URL = "https://openapi.naver.com/v1/nid/me"

# Kakao Login + client_id, secret_id
KAKAO_CALLBACK_URL = "http://127.0.0.1:8000/accounts/kakao/callback/"
KAKAO_STATE = "kakao_login"
KAKAO_SCOPE = "openid,account_email"
KAKAO_LOGIN_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_URL = "https://kapi.kakao.com/v2/user/me"

# Google Login + client_id, secret_id
