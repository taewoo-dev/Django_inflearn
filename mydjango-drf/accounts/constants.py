# 회원가입 인증 url
VERIFY_EMAIL_URL = "http://127.0.0.1:8000/accounts/verify/?token="

# Naver Login + client_id, secret_id
NAVER_STATE = "naver_login"
NAVER_SCOPE = ""
NAVER_CALLBACK_URL = "http://127.0.0.1:8000/accounts/naver/callback/"
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize"
NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
NAVER_PROFILE_URL = "https://openapi.naver.com/v1/nid/me"

# Kakao Login + client_id, secret_id
KAKAO_STATE = "kakao_login"
KAKAO_SCOPE = "openid,account_email"
KAKAO_CALLBACK_URL = "http://127.0.0.1:8000/accounts/kakao/callback/"
KAKAO_LOGIN_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_URL = "https://kapi.kakao.com/v2/user/me"

# Google Login + client_id, secret_id
GOOGLE_STATE = "google_login"
GOOGLE_SCOPE = "openid profile email"
GOOGLE_CALLBACK_URL = "http://127.0.0.1:8000/accounts/google/callback/"
GOOGLE_LOGIN_URL = "https://accounts.google.com/o/oauth2/v2/auth"

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_PROFILE_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
