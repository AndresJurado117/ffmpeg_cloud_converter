def check_audio_value(audio_bitrate: int, bitrate_min: int, bitrate_max: int) -> int:
    if bitrate_min <= audio_bitrate <= bitrate_max:
        return audio_bitrate * 1000
    else:
        raise ValueError
