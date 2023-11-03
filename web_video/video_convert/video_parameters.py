import ffmpeg, os
from .google_cloud_storage import upload_cs_file, get_cs_file_url


def local_video_save(filename: str, content) -> None:
    with open(f"uploaded_videos/{filename}", "wb") as file:
        for chunk in content.chunks():
            file.write(chunk)


def local_video_delete(filename: str) -> None:
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")


def check_video_resolution_widescreen(video_resolution: str) -> str:
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
    video_file,
    video_resolution,
    video_value,
    video_preset,
    audio_value,
    video_filters,
    audio_filters,
) -> None:
    local_video_save(f"{input_name}", video_file)
    input = ffmpeg.input(f"uploaded_videos/{input_name}")
    video_info = ffmpeg.probe(f"uploaded_videos/{input_name}")
    number_streams = len(video_info["streams"])
    streams = []

    for i in range(number_streams):
        streams.append(video_info["streams"][i]["codec_type"])
    video = input.video.filter(
        "scale",
        width=-1,
        height=check_video_resolution_widescreen(video_resolution),
    )

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
            vcodec="h264_nvenc",
            pix_fmt="yuv420p",
            preset=video_preset,
            rc=video_value[0],
            **{video_value[1]: video_value[2]},
            acodec="aac",
            audio_bitrate=audio_value,
        ).global_args("-hwaccel", "cuda", "-y").run()
        upload_cs_file(
            "video_cloud_converter",
            f"converted_videos/{input_name}_converted.mp4",
            f"converted_videos/{input_name}_converted",
        )
    else:
        ffmpeg.output(
            video,
            f"converted_videos/{input_name}_converted.mp4",
            vcodec="h264_nvenc",
            pix_fmt="yuv420p",
            preset=video_preset,
            rc=video_value[0],
            **{video_value[1]: video_value[2]},
        ).global_args("-hwaccel", "cuda", "-y").run()
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
