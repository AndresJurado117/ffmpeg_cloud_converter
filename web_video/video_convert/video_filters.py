def video_luts_list(lut_name) -> str:
    match lut_name:
        case "R709F3510D65":
            lut = "Rec709_Fujifilm_3510_D65.cube"
        case "R709K2383D65":
            lut = "Rec709_Kodak_2383_D65.cube"
        case "R709K2393D65":
            lut = "Rec709_Kodak_2393_D65.cube"
        case "LBKKT33":
            lut = "LBK-K-Tone_33.cube"
        case "LBKKTI33":
            lut = "LBK-K-Tone-Intense_33.cube"
        case "LBKKTIB33":
            lut = "LBK-K-Tone-Intense_BlackLift_33.cube"
        case _:
            raise NotImplementedError

    return f"LUT/{lut}"


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
    video_lut: str,
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
    if video_lut != "none":
        filters.append(("lut3d", {"file": video_luts_list(video_lut)}))
    return filters
