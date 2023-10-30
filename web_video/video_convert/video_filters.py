def video_filters(
    mirror: bool,
    green_outlines: bool,
    frame_interpolation: bool,
    gaussian_blur: bool,
    video_brightness_boolean: bool,
    video_brightness_value: float,
    video_contrast_boolean: bool,
    video_contrast_value: float,
    video_saturation_boolean: bool,
    video_saturation_value: float,
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
