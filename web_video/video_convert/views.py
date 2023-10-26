from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import ffmpeg, requests

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

# Video filter values

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

    # Equalizer presets
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

    # Equalizer
    eq_ten_band_1 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_2 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_3 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_4 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_5 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_6 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_7 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_8 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_9 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )

    eq_ten_band_10 = forms.FloatField(
        min_value=-20,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(
            attrs={"type": "range", "orient": "vertical", "step": 0.1}
        ),
    )


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


def video_filters(
    mirror,
    green_outlines,
    frame_interpolation,
    gaussian_blur,
    video_brightness_boolean,
    video_brightness_value,
    video_contrast_boolean,
    video_contrast_value,
    video_saturation_boolean,
    video_saturation_value,
):
    filters = []
    if mirror == True:
        filters.append(("hflip", {}))
    if green_outlines == True:
        filters.append(("sobel", {}))
        filters.append(("eq", {"saturation": 0.2}))
    if frame_interpolation == True:
        filters.append(("tmix", {"frames": 15}))
    if gaussian_blur == True:
        filters.append(
            ("gblur", {"sigma": 1}),
        )
    if video_brightness_boolean == True and -1.0 <= video_brightness_value <= 1.0:
        filters.append(("eq", {"brightness": video_brightness_value}))
    if video_contrast_boolean == True and -1.0 <= video_contrast_value <= 2.0:
        filters.append(("eq", {"contrast": video_contrast_value}))
    if video_saturation_boolean == True and 0.0 <= video_saturation_value <= 3.0:
        filters.append(("eq", {"saturation": video_saturation_value}))
    return filters


def eq_ten_band(
    band_1, band_2, band_3, band_4, band_5, band_6, band_7, band_8, band_9, band_10
):
    equalizer = []
    equalizer.append(("equalizer", {"f": 31.5, "t": "o", "w": "1", "g": band_1}))
    equalizer.append(("equalizer", {"f": 63, "t": "o", "w": "1", "g": band_2}))
    equalizer.append(("equalizer", {"f": 125, "t": "o", "w": "1", "g": band_3}))
    equalizer.append(("equalizer", {"f": 250, "t": "o", "w": "1", "g": band_4}))
    equalizer.append(("equalizer", {"f": 500, "t": "o", "w": "1", "g": band_5}))
    equalizer.append(("equalizer", {"f": 1000, "t": "o", "w": "1", "g": band_6}))
    equalizer.append(("equalizer", {"f": 2000, "t": "o", "w": "1", "g": band_7}))
    equalizer.append(("equalizer", {"f": 4000, "t": "o", "w": "1", "g": band_8}))
    equalizer.append(("equalizer", {"f": 8000, "t": "o", "w": "1", "g": band_9}))
    equalizer.append(("equalizer", {"f": 16000, "t": "o", "w": "1", "g": band_10}))
    return equalizer


def audio_filters(
    audio_volume,
    band_1,
    band_2,
    band_3,
    band_4,
    band_5,
    band_6,
    band_7,
    band_8,
    band_9,
    band_10,
):
    audio_filters = []
    if AUDIO_VOLUME_MIN <= audio_volume <= AUDIO_VOLUME_MAX:
        audio_filters.append(("volume", {"volume": audio_volume}))
    else:
        raise ValueError
    audio_filters.extend(
        eq_ten_band(
            band_1,
            band_2,
            band_3,
            band_4,
            band_5,
            band_6,
            band_7,
            band_8,
            band_9,
            band_10,
        )
    )
    return audio_filters


# Need to check if an audio track exists
def video_convert(
    input_name,
    video_file,
    video_resolution,
    video_value,
    video_preset,
    audio_value,
    video_filters,
    audio_filters,
):
    local_video_save(f"{input_name}", video_file)
    input = ffmpeg.input(f"uploaded_videos/{input_name}")
    video = input.video.filter(
        "scale",
        width=-1,
        height=check_video_resolution_widescreen(video_resolution),
    )

    for filter_name, filter_params in video_filters:
        video = video.filter(filter_name, **filter_params)

    audio = input.audio

    for filter_name, filter_params in audio_filters:
        audio = audio.filter(filter_name, **filter_params)

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
            try:
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
                )
            except (NotImplementedError, ValueError):
                return render(request, "error.html")
        return render(request, "test.html")
