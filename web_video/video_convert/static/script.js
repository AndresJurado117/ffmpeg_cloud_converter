document.addEventListener("DOMContentLoaded", (event) => {
    var videoMode = document.getElementById("id_video_mode");

    var qpSlider = document.getElementById("id_video_qp");
    var qpValue = document.getElementById("qp_value");

    qpValue.innerHTML = qpSlider.value;

    qpSlider.oninput = function () {
        qpValue.innerHTML = this.value;
    }

    var bitrateSlider = document.getElementById("id_video_bitrate");
    var bitrateValue = document.getElementById("bitrate_value");

    bitrateValue.innerHTML = bitrateSlider.value;

    bitrateSlider.oninput = function () {
        bitrateValue.innerHTML = this.value;
    }

    var audioSlider = document.getElementById("id_audio_bitrate");
    var audioValue = document.getElementById("audio_value");

    audioValue.innerHTML = audioSlider.value;

    audioSlider.oninput = function () {
        audioValue.innerHTML = this.value;
    }
});