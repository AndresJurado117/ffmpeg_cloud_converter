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
    nvidia_presets = (
        ("slow", "Slow (NVENC)"),
        ("medium", "Medium (NVENC)"),
        ("fast", "Fast (NVENC)"),
    )
    nvidia_rate_control = ("qp", "QP"), ("vbr", "VBR"), ("cbr", "CBR")

    input_file = forms.FileField()
    video_mode = forms.ChoiceField(choices=nvidia_rate_control)
    video_qp = forms.IntegerField(
        min_value=VIDEO_QP_MIN, max_value=VIDEO_QP_MAX, initial=VIDEO_QP_INITIAL
    )
    video_bitrate = forms.IntegerField(
        min_value=VIDEO_BITRATE_MIN,
        max_value=VIDEO_BITRATE_MAX,
        initial=VIDEO_BITRATE_INITIAL,
    )
    video_preset = forms.ChoiceField(choices=nvidia_presets, initial="medium")
    audio_bitrate = forms.IntegerField(
        min_value=AUDIO_BITRATE_INITIAL,
        max_value=AUDIO_BITRATE_MAX,
        initial=AUDIO_BITRATE_INITIAL,
    )


def azure_upload():
    ...


def azure_get_link():
    ...


def local_video_save(filename, content):
    with open(f"uploaded_videos/{filename}", "wb") as file:
        for chunk in content.chunks():
            file.write(chunk)


def get_video_mode(mode):
    match mode:
        case "qp":
            return "qp"
        case "vbr":
            return "vbr"
        case "cbr":
            return "cbr"
        case _:
            raise NotImplementedError


async def index(request):
    return render(request, "index.html", {"form": ConvertVideo()})


# Add check until video is encoded
async def conversion(request):
    if request.method == "POST":
        form = ConvertVideo(request.POST, request.FILES)
        if form.is_valid():
            input_name = form.cleaned_data["input_file"]
            video_mode = get_video_mode(form.cleaned_data["video_mode"])
            if (
                video_mode == "qp"
                and VIDEO_QP_MIN <= form.cleaned_data["video_qp"] <= VIDEO_QP_MAX
            ):
                compression = form.cleaned_data["video_qp"]
            elif (
                video_mode == "vbr"
                or "cbr"
                and VIDEO_BITRATE_MIN
                <= form.cleaned_data["video_bitrate"]
                <= VIDEO_BITRATE_MAX
            ):
                compression = form.cleaned_data["video_bitrate"]

            local_video_save(f"{input_name}", request.FILES["input_file"])
            ffmpeg.input(f"uploaded_videos/{input_name}").output(
                f"converted_videos/{input_name}_converted.mp4",
                **{"c:v": "h264_nvenc"},
                preset=form.cleaned_data["video_preset"],
                **{video_mode: compression},
                # qp=form.cleaned_data["video_cqp"],
                **{"c:a": "aac"},
                audio_bitrate=form.cleaned_data["audio_bitrate"] * 1000,
            ).global_args("-hwaccel", "cuda", "-y").run()
        return render(request, "test.html")
