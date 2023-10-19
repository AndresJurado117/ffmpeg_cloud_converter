from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import ffmpeg, requests

# Set global values for audio and video encoding
VIDEO_QP_MIN = 20
VIDEO_QP_MAX = 32
VIDEO_QP_INITIAL = 32
VIDEO_BITRATE_MIN = 500
VIDEO_BITRATE_MAX = 5000
VIDEO_BITRATE_INITIAL = 2500
AUDIO_BITRATE_MIN = 32
AUDIO_BITRATE_MAX = 256
AUDIO_BITRATE_INITIAL = 128


class ConvertVideo(forms.Form):
    widescreen_resolutions = (
        ("-1", "Original"),
        ("360", "360p"),
        ("480", "480p"),
        ("720", "720p"),
        ("1080", "1080p"),
        ("2160", "4K"),
    )
    nvidia_presets = (
        ("slow", "Slow (NVENC)"),
        ("medium", "Medium (NVENC)"),
        ("fast", "Fast (NVENC)"),
    )
    nvidia_rate_control = ("qp", "QP"), ("vbr", "VBR")

    input_file = forms.FileField()
    video_resolution = forms.ChoiceField(choices=widescreen_resolutions)
    video_mode = forms.ChoiceField(choices=nvidia_rate_control)
    video_qp = forms.IntegerField(
        min_value=VIDEO_QP_MIN,
        max_value=VIDEO_QP_MAX,
        initial=VIDEO_QP_INITIAL,
        widget=forms.NumberInput(attrs={"type": "range"}),
    )
    video_bitrate = forms.IntegerField(
        min_value=VIDEO_BITRATE_MIN,
        max_value=VIDEO_BITRATE_MAX,
        initial=VIDEO_BITRATE_INITIAL,
        widget=forms.NumberInput(attrs={"type": "range"}),
    )
    video_preset = forms.ChoiceField(choices=nvidia_presets, initial="medium")
    audio_bitrate = forms.IntegerField(
        min_value=AUDIO_BITRATE_MIN,
        max_value=AUDIO_BITRATE_MAX,
        initial=AUDIO_BITRATE_INITIAL,
        widget=forms.NumberInput(attrs={"type": "range"}),
    )
    video_flip = forms.BooleanField(required=False)
    green_outlines = forms.BooleanField(required=False)
    gaussian_blur = forms.BooleanField(required=False)


def video_render_queue():
    ...


def azure_upload():
    ...


def azure_get_link():
    ...


def local_video_save(filename, content):
    with open(f"uploaded_videos/{filename}", "wb") as file:
        for chunk in content.chunks():
            file.write(chunk)


def check_video_resolution_widescreen(video_resolution):
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


def check_video_value(mode, video_qp, video_bitrate):
    match mode:
        case "qp":
            mode_name = "constqp"
            mode_value = "qp"
        case "vbr":
            mode_name = "vbr"
            mode_value = "b"
        case _:
            raise NotImplementedError

    if mode_name == "constqp" and VIDEO_QP_MIN <= video_qp <= VIDEO_QP_MAX:
        return [mode_name, mode_value, video_qp]
    elif mode_name == "vbr" and VIDEO_BITRATE_MIN <= video_bitrate <= VIDEO_BITRATE_MAX:
        return [mode_name, mode_value, video_bitrate * 1000]
    else:
        raise ValueError


def check_audio_value(audio_bitrate):
    if AUDIO_BITRATE_MIN <= audio_bitrate <= AUDIO_BITRATE_MAX:
        return audio_bitrate * 1000
    else:
        raise ValueError


def video_filters(mirror, green_outlines, gaussian_blur):
    filters = []
    if mirror == True:
        filters.append(("hflip", {}))
    if green_outlines == True:
        filters.append(("sobel", {}))
        filters.append(("eq", {"saturation": 0.2}))
        filters.append(("tmix", {"frames": 15}))
    if gaussian_blur == True:
        filters.append(
            ("gblur", {"sigma": 1}),
        )
    return filters


# Nvidia RTX 30/40 Series supports 5 simultaneous encoding sessions
def video_convert(
    input_name,
    video_file,
    video_resolution,
    video_value,
    video_preset,
    audio_value,
    custom_filters,
):
    local_video_save(f"{input_name}", video_file)
    input = ffmpeg.input(f"uploaded_videos/{input_name}")
    video = input.video.filter(
        "scale",
        width=-1,
        height=check_video_resolution_widescreen(video_resolution),
    )

    for filter_name, filter_params in custom_filters:
        print(len(custom_filters))
        print(filter_name, filter_params)
        print(len(filter_params))
        video = video.filter(filter_name, **filter_params)

        # .filter("sobel")
        # .filter("eq", saturation=0.2)
        # .filter("tmix", frames=15)
        # .filter("hflip")
    audio = input.audio
    ffmpeg.output(
        video,
        audio,
        f"converted_videos/{input_name}_converted.mp4",
        vcodec="h264_nvenc",
        preset=video_preset,
        rc=video_value[0],
        **{video_value[1]: video_value[2]},
        acodec="aac",
        audio_bitrate=audio_value,
    ).global_args("-hwaccel", "cuda", "-y").run()


async def index(request):
    return render(request, "index.html", {"form": ConvertVideo()})


# Add check until video is encoded, for a queue.
async def conversion(request):
    if request.method == "POST":
        form = ConvertVideo(request.POST, request.FILES)
        if form.is_valid():
            video_convert(
                form.cleaned_data["input_file"],
                request.FILES["input_file"],
                form.cleaned_data["video_resolution"],
                check_video_value(
                    form.cleaned_data["video_mode"],
                    form.cleaned_data["video_qp"],
                    form.cleaned_data["video_bitrate"],
                ),
                form.cleaned_data["video_preset"],
                check_audio_value(form.cleaned_data["audio_bitrate"]),
                video_filters(
                    form.cleaned_data["video_flip"],
                    form.cleaned_data["green_outlines"],
                    form.cleaned_data["gaussian_blur"],
                ),
            )
        return render(request, "test.html")
