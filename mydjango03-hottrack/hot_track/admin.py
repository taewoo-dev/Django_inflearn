from django.contrib import admin

from hot_track.models import Song
from hot_track.utils.melon import get_likes_dict


# Register your models here.
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
    list play 속성에 지정하는 이름들은
    1) Model Field
    2) Model CustomField
    3) Model Class의 인자 없는 함수
    4) ModelAdmin Class 인자 1개 받는 함수
    """

    list_display = [
        "cover_image_tag",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]

    """
    format_html API는 장고 내에서 HTML태그를 조합할 수 있는 가장 안전한 방법.
    직접 조합x, mark_safe도 사용하지마라
    인자로 넘겨서 조합하면 XSS 해킹 방어에 용이하다
    """
    # 4번 예시
    # @staticmethod
    # def cover_image_tag(self, song):
    #     return format_html('<img src="{}" style="width:50px;"/>', self.cover_url)

    """
    search_fields 속성에 대하여 or 조건으로 검색
    where 조건으로 쿼리가 수행되어 출력된다
    """

    search_fields = [
        "name",
        "artist_name",
        "album_name",
    ]

    """
    list_filter의 속성으로 DateTime필드가 지정되면 예외적으로 
    오늘, 지난7일, 이번달, 올해 선택지가 주어진다
    """

    list_filter = [
        "genre",
        "release_date",
    ]

    """
    admin 기본에는 delete action만 제공된다
    custom action을 만들어보자
    """

    actions = [
        "update_like_count",
    ]

    """
    actions에 등록된 함수는 인자를 2개 받는다
    1번 인자로 request, 2번 인자로 queryset
    action도 하나의 웹 요청이므로 request를 인자로 받는다.
    두번째 인자인 queryset은 선택된 record에 대한 쿼리셋이다.
    """

    def update_like_count(self, request, queryset):
        melon_uid_list = queryset.values_list("melon_uid", flat=True)
        likes_dict = get_likes_dict(melon_uid_list)
        print("likes dict :", likes_dict)

        changed_count = 0
        for song in queryset:
            if song.like_count != likes_dict.get(song.melon_uid):
                song.like_count = likes_dict.get(song.melon_uid)
                # song.save() 장고에서 models.save()는 모든 column에 대해서 업데이트를 진행한다
                # song.save(update_fields=["like_count"]) 업데이트 필드를 지정해주면 쿼리가 매우 줄어든다
                changed_count += 1

        Song.objects.bulk_update(
            queryset,
            fields=["like_count"],
        )

        self.message_user(
            request=request, message=f"{changed_count}곡 좋아요 갱신 완료"
        )
