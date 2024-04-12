# These keys should be ENV variables.
# Values for ENCODER_MODE are "GPU", "CPU"
ENCODER_MODE = "GPU"
VIDEO_CODEC = None
AUDIO_CODEC = "aac"
# Values for STORAGE_CONVERTED_VIDEOS are "LOCAL", "GCP", "AZURE", "AWS", LOCAL will keep the converted files in the converted folder but won't return a download link on the web GUI, it will return None.
STORAGE_CONVERTED_VIDEOS = "LOCAL"

# Nvidia RTX 30/40 Series supports 5 simultaneous encoding sessions as of driver version 551.23, it now supports 8 encoding sessions, apparently RTX A2000, A4000 can take around 26 sessions
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