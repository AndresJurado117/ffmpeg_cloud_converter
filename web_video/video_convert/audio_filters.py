def eq_ten_band(ten_band: tuple) -> list:
    equalizer = []
    equalizer.append(("equalizer", {"f": 31.5, "t": "o", "w": "1", "g": ten_band[0]}))
    equalizer.append(("equalizer", {"f": 63, "t": "o", "w": "1", "g": ten_band[1]}))
    equalizer.append(("equalizer", {"f": 125, "t": "o", "w": "1", "g": ten_band[2]}))
    equalizer.append(("equalizer", {"f": 250, "t": "o", "w": "1", "g": ten_band[3]}))
    equalizer.append(("equalizer", {"f": 500, "t": "o", "w": "1", "g": ten_band[4]}))
    equalizer.append(("equalizer", {"f": 1000, "t": "o", "w": "1", "g": ten_band[5]}))
    equalizer.append(("equalizer", {"f": 2000, "t": "o", "w": "1", "g": ten_band[6]}))
    equalizer.append(("equalizer", {"f": 4000, "t": "o", "w": "1", "g": ten_band[7]}))
    equalizer.append(("equalizer", {"f": 8000, "t": "o", "w": "1", "g": ten_band[8]}))
    equalizer.append(("equalizer", {"f": 16000, "t": "o", "w": "1", "g": ten_band[9]}))
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
