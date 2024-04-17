import ffmpeg
from .google_cloud_storage import upload_cs_file, get_cs_file_url
from .ffmpeg_exceptions import InvalidVideoFileType
from .audio_parameters import check_audio_value
from .video_filters import video_filters_list
from .audio_filters import audio_filters_list
from .local_video_management import local_video_save, local_video_delete
from .video_extensions import video_extensions
from .global_variables import ENCODER_MODE, AUDIO_CODEC, STORAGE_CONVERTED_VIDEOS


def check_video_resolution_widescreen(video_resolution: str) -> str:
    """
    Check video resolution
    """
    match video_resolution:
        case "-1":
            return video_resolution
        case "360":
            return video_resolution
        case "480":
            return video_resolution
        case "720":
            return video_resolution
        case "1080":
            return video_resolution
        case "2160":
            return video_resolution
        case _:
            raise NotImplementedError


def check_video_value(
    mode: str,
    video_qp: int,
    video_bitrate: int,
    qp_min: int,
    qp_max: int,
    bitrate_min: int,
    bitrate_max: int,
) -> list:
    match mode:
        case "qp":
            mode_name = "constqp"
            mode_value = "qp"
        case "vbr":
            mode_name = "vbr"
            mode_value = "b"
        case _:
            raise NotImplementedError

    if mode_name == "constqp" and qp_min <= video_qp <= qp_max:
        return [mode_name, mode_value, video_qp]
    elif mode_name == "vbr" and bitrate_min <= video_bitrate <= bitrate_max:
        return [mode_name, mode_value, video_bitrate * 1000]
    else:
        raise ValueError


def video_convert(
    input_name: str,
    video_file: bytes,
    video_resolution: int,
    video_value_list: list,
    video_preset: str,
    audio_value_list: list,
    video_filter_list: list,
    audio_filter_list: list,
) -> None:
    video_values = check_video_value(
        video_value_list[0],
        video_value_list[1],
        video_value_list[2],
        video_value_list[3],
        video_value_list[4],
        video_value_list[5],
        video_value_list[6],
    )
    audio_value = check_audio_value(
        audio_value_list[0], audio_value_list[1], audio_value_list[2]
    )
    video_filters = video_filters_list(
        video_filter_list[0],
        video_filter_list[1],
        video_filter_list[2],
        video_filter_list[3],
        video_filter_list[4],
        video_filter_list[5],
        video_filter_list[6],
        video_filter_list[7],
        video_filter_list[8],
        video_filter_list[9],
        video_filter_list[10],
    )
    audio_filters = audio_filters_list(
        audio_filter_list[0],
        audio_filter_list[1],
        audio_filter_list[2],
        audio_filter_list[3],
    )

    match ENCODER_MODE:
        case "GPU":
            enc_backend = "h264_nvenc"
            global_args = ["-hwaccel", "cuda", "-y"]
        case "CPU":
            enc_backend = "libx264"
            global_args = ["-y"]

    if input_name.endswith(video_extensions):
        local_video_save(f"{input_name}", video_file)
        input = ffmpeg.input(f"uploaded_videos/{input_name}")
    else:
        raise InvalidVideoFileType

    video_info = ffmpeg.probe(f"uploaded_videos/{input_name}")
    number_streams = len(video_info["streams"])
    streams = []

    for i in range(number_streams):
        streams.append(video_info["streams"][i]["codec_type"])

    if video_info["streams"][0]["codec_type"] == "video":
        if int(video_info["streams"][0]["width"]) > int(
            video_info["streams"][0]["height"]
        ):
            video = input.video.filter(
                "scale",
                width=-1,
                height=check_video_resolution_widescreen(video_resolution),
            )
        elif int(video_info["streams"][0]["width"]) < int(
            video_info["streams"][0]["height"]
        ):
            video = input.video.filter(
                "scale",
                width=check_video_resolution_widescreen(video_resolution),
                height=-1,
            )
        else:
            raise ValueError

    for filter_name, filter_params in video_filters:
        video = video.filter(filter_name, **filter_params)

    if "audio" in streams:
        audio = input.audio

        for filter_name, filter_params in audio_filters:
            audio = audio.filter(filter_name, **filter_params)

        ffmpeg.output(
            video,
            audio,
            f"converted_videos/{input_name}_converted.mp4",
            vcodec=enc_backend,
            pix_fmt="yuv420p",
            preset=video_preset,
            rc=video_values[0],
            **{video_values[1]: video_values[2]},
            acodec=AUDIO_CODEC,
            audio_bitrate=audio_value,
        ).global_args(*global_args).run() 
    else:
        ffmpeg.output(
            video,
            f"converted_videos/{input_name}_converted.mp4",
            vcodec=enc_backend,
            pix_fmt="yuv420p",
            preset=video_preset,
            rc=video_values[0],
            **{video_values[1]: video_values[2]},
        ).global_args(*global_args).run() 

    match STORAGE_CONVERTED_VIDEOS:
        case "LOCAL":
            # Converted video is already saved locally
            pass
        case "GPC":
            upload_cs_file(
                    "video_cloud_converter",
                    f"converted_videos/{input_name}_converted.mp4",
                    f"converted_videos/{input_name}_converted",
                )
            # Delete a file
            local_video_delete(f"uploaded_videos/{input_name}")
            return get_cs_file_url(
                "video_cloud_converter", f"converted_videos/{input_name}_converted"
            )
        case "AZURE":
            pass
        case "AWS":
            pass

def get_video_url(filename):
    match STORAGE_CONVERTED_VIDEOS:
        case "LOCAL":
            return None
        case "GCP":
            get_cs_file_url("video_cloud_converter",
                            f"converted_videos/{filename}_converted",)
        case "AZURE":
            pass
        case "AWS":
            pass