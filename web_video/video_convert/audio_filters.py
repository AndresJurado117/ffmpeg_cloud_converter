def eq_ten_band(ten_band: tuple) -> list:
    waves = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    equalizer = []
    for i in range(10):
        equalizer.append(
            ("equalizer", {"f": waves[i], "t": "o", "w": "1", "g": ten_band[i]})
        )
    return equalizer


def audio_filters(
    audio_volume: float, volume_min: float, volume_max: float, ten_band: list
) -> list:
    audio_filters = []
    if volume_min <= audio_volume <= volume_max:
        audio_filters.append(("volume", {"volume": audio_volume}))
    else:
        raise ValueError
    audio_filters.extend(eq_ten_band(ten_band))
    return audio_filters
