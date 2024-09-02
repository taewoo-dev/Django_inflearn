from urllib.request import Request

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict


class JsonResponseMixin:
    def finalize_response(
        self, request: Request, response: Response, *args, **kwargs
    ) -> Response:
        is_ok = 200 <= response.status_code < 400

        # finalize 매서드 호출 시 지정된다. api 처리중 예외가 발생하면 이 속성이 지정되지 않는다.
        accepted_renderer = getattr(request, "accepted_renderer", None)

        if accepted_renderer is None or response.exception is True:
            response.data = {
                "ok": False,
                "result": response.data,
            }

        elif isinstance(
            request.accepted_renderer, (JSONRenderer, BrowsableAPIRenderer)
        ):
            # 원본 데이터는 ReturnDict Type
            response.data = ReturnDict(
                {
                    "ok": is_ok,
                    "result": response.data,  # ReturnDict Type
                },
                serializer=response.data.serializer,  # 원본 데이터의 serializer를 참조해서 지정
            )
        return super().finalize_response(request, response, *args, **kwargs)
