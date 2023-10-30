from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import ffmpeg, requests, os
from dotenv import load_dotenv
from .video_parameters import (
    local_video_save,
    check_video_resolution_widescreen,
    check_video_value,
    video_convert,
)
from .video_filters import video_filters
from .audio_parameters import check_audio_value
from .audio_filters import eq_ten_band, audio_filters

load_dotenv()
print(os.getenv("GOOGLE_CLOUD_STORAGE_API"))

# Nvidia RTX 30/40 Series supports 5 simultaneous encoding sessions, apparently RTX A2000, A4000 can take around 26 sessions
SIMULTANEOUS_TRANSCODING_SESSIONS = 5

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

# Audio filter values
AUDIO_VOLUME_MIN = 0.0
AUDIO_VOLUME_MAX = 4.0
AUDIO_VOLUME_INITIAL = 1.0


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
        disabled=True,
        widget=forms.NumberInput(attrs={"type": "range", "step": 100}),
    )

    video_preset = forms.ChoiceField(choices=nvidia_presets, initial="medium")

    audio_bitrate = forms.IntegerField(
        min_value=AUDIO_BITRATE_MIN,
        max_value=AUDIO_BITRATE_MAX,
        initial=AUDIO_BITRATE_INITIAL,
        widget=forms.NumberInput(attrs={"type": "range", "step": 32}),
    )

    video_flip = forms.BooleanField(required=False)

    green_outlines = forms.BooleanField(required=False)

    frame_interpolation = forms.BooleanField(required=False)

    gaussian_blur = forms.BooleanField(required=False)

    video_brightness_boolean = forms.BooleanField(required=False)

    video_brightness_value = forms.FloatField(
        min_value=-1.0,
        max_value=1.0,
        initial=0.0,
        disabled=True,
        widget=forms.NumberInput(attrs={"type": "range", "step": 0.01}),
    )

    video_contrast_boolean = forms.BooleanField(required=False)

    video_contrast_value = forms.FloatField(
        min_value=0.0,
        max_value=2.0,
        initial=1.0,
        disabled=True,
        widget=forms.NumberInput(attrs={"type": "range", "step": 0.01}),
    )

    video_saturation_boolean = forms.BooleanField(required=False)

    video_saturation_value = forms.FloatField(
        min_value=0.0,
        max_value=3.0,
        initial=1,
        disabled=True,
        widget=forms.NumberInput(attrs={"type": "range", "step": 0.01}),
    )

    lut_list = (
        ("none", "None"),
        ("Rec709_Fujifilm_3510_D65.cube", "Fujifilm 3510 (Juan Melara)"),
        ("Rec709_Kodak_2383_D65.cube", "Kodak 2383 (Juan Melara)"),
        ("Rec709_Kodak_2393_D65.cube", "Kodak 2393 (Juan Melara)"),
        ("LBK-K-Tone_33.cube", "The new K-Tone (Frank Glencairn)"),
        ("LBK-K-Tone-Intense_33.cube", "New K-Tone intense (Frank Glencairn)"),
        (
            "LBK-K-Tone-Intense_BlackLift_33.cube",
            "New K-Tone intense - raised blacks (Frank Glencairn)",
        ),
    )

    video_lut = forms.ChoiceField(choices=lut_list)

    audio_volume = forms.FloatField(
        min_value=AUDIO_VOLUME_MIN,
        max_value=AUDIO_VOLUME_MAX,
        initial=AUDIO_VOLUME_INITIAL,
        widget=forms.NumberInput(attrs={"type": "range", "step": 0.01}),
    )

    # Equalizer presets form
    equalizer_presets = (
        ("custom", "Custom"),
        ("eq_hi_end", "Dialog - Clean add hi end"),
        ("eq_dialog_female_lav", "Dialog - Female lav mic fixer"),
        ("eq_dialog_male_lav", "Dialog - Male lav finisher"),
        ("eq_dialog_male", "Dialog - Male"),
        ("eq_telephone", "General - Telephone"),
        ("eq_music_top_end_boost", "Music Master - Top end Boost"),
    )

    equalizer_preset = forms.ChoiceField(choices=equalizer_presets, initial="custom")

    # Equalizer form
    eq_ten_band_1 = (
        eq_ten_band_2
    ) = (
        eq_ten_band_3
    ) = (
        eq_ten_band_4
    ) = (
        eq_ten_band_5
    ) = (
        eq_ten_band_6
    ) = (
        eq_ten_band_7
    ) = eq_ten_band_8 = eq_ten_band_9 = eq_ten_band_10 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )


def video_render_queue():
    ...


def google_cloud_storage_upload():
    ...


def azure_get_link():
    ...


async def index(request):
    return render(request, "index.html", {"form": ConvertVideo()})


# Add check until video is encoded, for a queue.
async def conversion(request):
    if request.method == "POST":
        form = ConvertVideo(request.POST, request.FILES)
        if form.is_valid():
            try:
                video_convert(
                    form.cleaned_data["input_file"],
                    request.FILES["input_file"],
                    form.cleaned_data["video_resolution"],
                    check_video_value(
                        form.cleaned_data["video_mode"],
                        form.cleaned_data["video_qp"],
                        form.cleaned_data["video_bitrate"],
                        VIDEO_QP_MIN,
                        VIDEO_QP_MAX,
                        VIDEO_BITRATE_MIN,
                        VIDEO_BITRATE_MAX,
                    ),
                    form.cleaned_data["video_preset"],
                    check_audio_value(
                        form.cleaned_data["audio_bitrate"],
                        AUDIO_BITRATE_MIN,
                        AUDIO_BITRATE_MAX,
                    ),
                    video_filters(
                        form.cleaned_data["video_flip"],
                        form.cleaned_data["green_outlines"],
                        form.cleaned_data["frame_interpolation"],
                        form.cleaned_data["gaussian_blur"],
                        form.cleaned_data["video_brightness_boolean"],
                        form.cleaned_data["video_brightness_value"],
                        form.cleaned_data["video_contrast_boolean"],
                        form.cleaned_data["video_contrast_value"],
                        form.cleaned_data["video_saturation_boolean"],
                        form.cleaned_data["video_saturation_value"],
                    ),
                    audio_filters(
                        form.cleaned_data["audio_volume"],
                        AUDIO_VOLUME_MIN,
                        AUDIO_VOLUME_MAX,
                        (
                            form.cleaned_data["eq_ten_band_1"],
                            form.cleaned_data["eq_ten_band_2"],
                            form.cleaned_data["eq_ten_band_3"],
                            form.cleaned_data["eq_ten_band_4"],
                            form.cleaned_data["eq_ten_band_5"],
                            form.cleaned_data["eq_ten_band_6"],
                            form.cleaned_data["eq_ten_band_7"],
                            form.cleaned_data["eq_ten_band_8"],
                            form.cleaned_data["eq_ten_band_9"],
                            form.cleaned_data["eq_ten_band_10"],
                        ),
                    ),
                )
            except (NotImplementedError, ValueError):
                return render(request, "error.html")
        return render(request, "test.html")
