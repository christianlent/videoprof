from pymediainfo import MediaInfo
from typing import cast, Any, Dict, List


MediaTrack = Dict[str, Any]
MediaInfoList = List[MediaTrack]


def get_media_info_list(filename: str) -> MediaInfoList:
    media_info = MediaInfo.parse(filename)
    return cast(MediaInfoList, [x.to_data() for x in media_info.tracks])
