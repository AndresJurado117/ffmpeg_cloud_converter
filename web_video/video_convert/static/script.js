document.addEventListener("DOMContentLoaded", (event) => {
    /*  Declare Video Mode and Sliders */
    var videoMode = document.getElementById("id_video_mode");
    var qpSlider = document.getElementById("id_video_qp");
    var bitrateSlider = document.getElementById("id_video_bitrate");

    videoMode.onchange = function () {
        if (this.value == "qp") {
            qpSlider.disabled = false;
            bitrateSlider.disabled = true;
        }
        else if (this.value == "vbr") {
            qpSlider.disabled = true;
            bitrateSlider.disabled = false;
        }
    }

    /* QP Slider */

    var qpValue = document.getElementById("qp_value");

    qpValue.innerHTML = qpSlider.value;

    qpSlider.oninput = function () {
        qpValue.innerHTML = this.value;
    }

    /* Video Bitrate Slider */

    var bitrateValue = document.getElementById("bitrate_value");

    bitrateValue.innerHTML = bitrateSlider.value;

    bitrateSlider.oninput = function () {
        bitrateValue.innerHTML = this.value;
    }

    /* Audio Bitrate Slider */

    var audioSlider = document.getElementById("id_audio_bitrate");
    var audioValue = document.getElementById("audio_value");

    audioValue.innerHTML = audioSlider.value;

    audioSlider.oninput = function () {
        audioValue.innerHTML = this.value;
    }

    /* Brightness Slider */

    var brightnessBoolean = document.getElementById("id_video_brightness_boolean");
    var brightnessSlider = document.getElementById("id_video_brightness_value");
    var brightnessValue = document.getElementById("brightness_value");

    brightnessBoolean.onclick = function () {
        if (brightnessSlider.disabled == true) {
            brightnessSlider.disabled = false;
        }
        else {
            brightnessSlider.disabled = true;
        }
    }

    brightnessValue.innerHTML = parseFloat(brightnessSlider.value).toFixed(2);

    brightnessSlider.oninput = function () {
        brightnessValue.innerHTML = parseFloat(this.value).toFixed(2);
    }

    /* Contrast Slider */

    var contrastBoolean = document.getElementById("id_video_contrast_boolean")
    var contrastSlider = document.getElementById("id_video_contrast_value");
    var contrastValue = document.getElementById("contrast_value");

    contrastBoolean.onclick = function () {
        if (contrastSlider.disabled == true) {
            contrastSlider.disabled = false;
        }
        else {
            contrastSlider.disabled = true;
        }
    }

    contrastValue.innerHTML = parseFloat(contrastSlider.value).toFixed(2);

    contrastSlider.oninput = function () {
        contrastValue.innerHTML = parseFloat(this.value).toFixed(2);
    }

    /* Saturation Slider */

    var saturationBoolean = document.getElementById("id_video_saturation_boolean")
    var saturationSlider = document.getElementById("id_video_saturation_value");
    var saturationValue = document.getElementById("saturation_value");

    saturationBoolean.onclick = function () {
        if (saturationSlider.disabled == true) {
            saturationSlider.disabled = false;
        }
        else {
            saturationSlider.disabled = true;
        }
    }

    saturationValue.innerHTML = parseFloat(saturationSlider.value).toFixed(2);

    saturationSlider.oninput = function () {
        saturationValue.innerHTML = parseFloat(this.value).toFixed(2);
    }

    /* Volumen Slider */

    var volumeSlider = document.getElementById("id_audio_volume");
    var volumeValue = document.getElementById("volume_value");

    volumeValue.innerHTML = Math.round(volumeSlider.value * 100);

    volumeSlider.oninput = function () {
        volumeValue.innerHTML = Math.round(this.value * 100);
    }

    /* EQ Presets and Sliders */

    var eqPresets = document.getElementById("id_equalizer_preset");

    var eqBarOneSlider = document.getElementById("id_eq_ten_band_1");
    var eqBarOneValue = document.getElementById("eq_bar_1");

    eqBarOneValue.innerHTML = eqBarOneSlider.value;

    eqBarOneSlider.oninput = function () {
        eqBarOneValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarTwoSlider = document.getElementById("id_eq_ten_band_2");
    var eqBarTwoValue = document.getElementById("eq_bar_2");

    eqBarTwoValue.innerHTML = eqBarTwoSlider.value;

    eqBarTwoSlider.oninput = function () {
        eqBarTwoValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarThreeSlider = document.getElementById("id_eq_ten_band_3");
    var eqBarThreeValue = document.getElementById("eq_bar_3");

    eqBarThreeValue.innerHTML = eqBarThreeSlider.value;

    eqBarThreeSlider.oninput = function () {
        eqBarThreeValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarFourSlider = document.getElementById("id_eq_ten_band_4");
    var eqBarFourValue = document.getElementById("eq_bar_4");

    eqBarFourValue.innerHTML = eqBarFourSlider.value;

    eqBarFourSlider.oninput = function () {
        eqBarFourValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarFiveSlider = document.getElementById("id_eq_ten_band_5");
    var eqBarFiveValue = document.getElementById("eq_bar_5");

    eqBarFiveValue.innerHTML = eqBarFiveSlider.value;

    eqBarFiveSlider.oninput = function () {
        eqBarFiveValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarSixSlider = document.getElementById("id_eq_ten_band_6");
    var eqBarSixValue = document.getElementById("eq_bar_6");

    eqBarSixValue.innerHTML = eqBarSixSlider.value;

    eqBarSixSlider.oninput = function () {
        eqBarSixValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarSevenSlider = document.getElementById("id_eq_ten_band_7");
    var eqBarSevenValue = document.getElementById("eq_bar_7");

    eqBarSevenValue.innerHTML = eqBarSevenSlider.value;

    eqBarSevenSlider.oninput = function () {
        eqBarSevenValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarEightSlider = document.getElementById("id_eq_ten_band_8");
    var eqBarEightValue = document.getElementById("eq_bar_8");

    eqBarEightValue.innerHTML = eqBarEightSlider.value;

    eqBarEightSlider.oninput = function () {
        eqBarEightValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarNineSlider = document.getElementById("id_eq_ten_band_9");
    var eqBarNineValue = document.getElementById("eq_bar_9");

    eqBarNineValue.innerHTML = eqBarNineSlider.value;

    eqBarNineSlider.oninput = function () {
        eqBarNineValue.innerHTML = this.value;
        eqPresets.value = "custom"
    }

    var eqBarTenSlider = document.getElementById("id_eq_ten_band_10");
    var eqBarTenValue = document.getElementById("eq_bar_10");

    eqBarTenValue.innerHTML = eqBarTenSlider.value;

    eqBarTenSlider.oninput = function () {
        eqBarTenValue.innerHTML = this.value;
        eqPresets.value = "custom";
    }

    const equalizerValues = (bandOne, bandTwo, bandThree, bandFour, bandFive, bandSix, bandSeven, bandEight, bandNine, bandTen) => {
        eqBarOneSlider.value = eqBarOneValue.value = eqBarOneValue.innerHTML = bandOne;
        eqBarTwoSlider.value = eqBarTwoValue.value = eqBarTwoValue.innerHTML = bandTwo;
        eqBarThreeSlider.value = eqBarThreeValue.value = eqBarThreeValue.innerHTML = bandThree;
        eqBarFourSlider.value = eqBarFourValue.value = eqBarFourValue.innerHTML = bandFour;
        eqBarFiveSlider.value = eqBarFiveValue.value = eqBarFiveValue.innerHTML = bandFive;
        eqBarSixSlider.value = eqBarSixValue.value = eqBarSixValue.innerHTML = bandSix;
        eqBarSevenSlider.value = eqBarSevenValue.value = eqBarSevenValue.innerHTML = bandSeven;
        eqBarEightSlider.value = eqBarEightValue.value = eqBarEightValue.innerHTML = -bandEight;
        eqBarNineSlider.value = eqBarNineValue.value = eqBarNineValue.innerHTML = bandNine;
        eqBarTenSlider.value = eqBarTenValue.value = eqBarTenValue.innerHTML = bandTen;
    }

    eqPresets.onchange = function () {
        /*
        switch (this.value) {
            case "eq_hi_end":
                equalizerValues(-15, -5, -1, -1, 0, 0.5, 2, 1.5, 3, 4.2)
            case "eq_dialog_female_lav":
                equalizerValues(-10, -0.5, 2.7, 2.5, 1, 0, 1, 3, 4.5, 4.5)
            case "eq_dialog_male_lav":
                equalizerValues(-10, 0, 3.8, -20, 5.1, 2, 0.5, 0.5, 2.5, 4)
            case "eq_dialog_male":
                equalizerValues(-20, -12, -1, 0.5, -5, 2, 4, 1.5, -2, 2)
            case "eq_telephone":
                equalizerValues(-20, -20, -20, -20, 0, 10, 0, -20, -20, -20)
            case "eq_music_top_end_boost":
                equalizerValues(0, 0, 0, 0, 0, 0, 0, 2, 4, 4)
        }
        */
        if (this.value == "eq_hi_end") {
            equalizerValues(-15, -5, -1, -1, 0, 0.5, 2, 1.5, 3, 4.2)
        }
        else if (this.value == "eq_dialog_female_lav") {
            equalizerValues(-10, -0.5, 2.7, 2.5, 1, 0, 1, 3, 4.5, 4.5)
        }
        else if (this.value == "eq_dialog_male_lav") {
            equalizerValues(-10, 0, 3.8, -20, 5.1, 2, 0.5, 0.5, 2.5, 4)
        }
        else if (this.value == "eq_dialog_male") {
            equalizerValues(-20, -12, -1, 0.5, -5, 2, 4, 1.5, -2, 2)
        }
        else if (this.value == "eq_telephone") {
            equalizerValues(-20, -20, -20, -20, 0, 10, 0, -20, -20, -20)
        }
        else if (this.value == "eq_music_top_end_boost") {
            equalizerValues(0, 0, 0, 0, 0, 0, 0, 2, 4, 4)
        }
    }
});