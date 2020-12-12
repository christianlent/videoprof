from pymediainfo import MediaInfo
from typing import Dict, Sequence, Union

MediaAttribute = Union[str, bool, int, float]
MediaTrack = Dict[str, MediaAttribute]
MediaInfoList = Sequence[MediaTrack]


def get_media_info_list(filename: str) -> MediaInfoList:
    return [x.to_data() for x in MediaInfo.parse(filename).tracks]
