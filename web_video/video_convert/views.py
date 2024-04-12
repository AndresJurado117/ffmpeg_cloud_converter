from django.shortcuts import render
from .encoding_parameters import video_convert, get_video_url
from .ffmpeg_exceptions import InvalidVideoFileType
from .video_forms import ConvertVideo
from .global_variables import VIDEO_QP_MIN, VIDEO_QP_MAX, VIDEO_QP_INITIAL, VIDEO_BITRATE_MIN, VIDEO_BITRATE_MAX, AUDIO_BITRATE_MIN, AUDIO_BITRATE_MAX, AUDIO_VOLUME_MIN, AUDIO_VOLUME_MAX, AUDIO_VOLUME_INITIAL, ENCODER_MODE, STORAGE_CONVERTED_VIDEOS


def index(request):
    return render(request, "index.html", {"form": ConvertVideo(), "encoderMode": ENCODER_MODE, "storageConvertedVideos": STORAGE_CONVERTED_VIDEOS})


# Add check until video is encoded, for a queue.
def conversion(request):
    if request.method == "POST":
        form = ConvertVideo(request.POST, request.FILES)
        if form.is_valid():
            try:
                video_convert(
                    form.cleaned_data["input_file"].name,
                    request.FILES["input_file"],
                    form.cleaned_data["video_resolution"],
                    [
                        form.cleaned_data["video_mode"],
                        form.cleaned_data["video_qp"],
                        form.cleaned_data["video_bitrate"],
                        VIDEO_QP_MIN,
                        VIDEO_QP_MAX,
                        VIDEO_BITRATE_MIN,
                        VIDEO_BITRATE_MAX,
                    ],
                    form.cleaned_data["video_preset"],
                    [
                        form.cleaned_data["audio_bitrate"],
                        AUDIO_BITRATE_MIN,
                        AUDIO_BITRATE_MAX,
                    ],
                    [
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
                        form.cleaned_data["video_lut"],
                    ],
                    [
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
                    ],
                )
            except (NotImplementedError, ValueError):
                return render(
                    request,
                    "error.html",
                    {"error": "We encountered an unexpected error."},
                )

            except InvalidVideoFileType:
                return render(
                    request,
                    "error.html",
                    {"error": "File is not a supported video file."},
                )
        return render(
            request,
            "test.html",
            {
                "download_link": get_video_url(form.cleaned_data['input_file'])
            },
        )
