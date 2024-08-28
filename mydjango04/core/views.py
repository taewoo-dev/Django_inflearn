from django.shortcuts import render
from django.contrib import messages

# Create your views here.


def index(request):
    # info level 이상의 message만 기본적으로 출력된다
    # 쿠키, 세션에 등록하기에 request가 인자로 필요하다
    messages.debug(request, "디버그 메세지")
    messages.info(request, "정보 메세지")
    messages.success(request, "성공 메세지")
    messages.warning(request, "경고 메세지")
    messages.error(request, "오류 메세지")

    return render(request, template_name="core/index.html")
