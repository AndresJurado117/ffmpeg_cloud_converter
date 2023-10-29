document.addEventListener("DOMContentLoaded", (event) => {
    /*  Declare Video Mode and Sliders */
    const videoMode = document.getElementById("id_video_mode");
    const qpSlider = document.getElementById("id_video_qp");
    const bitrateSlider = document.getElementById("id_video_bitrate");

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

    const qpValue = document.getElementById("qp_value");

    qpValue.innerHTML = qpSlider.value;

    qpSlider.oninput = function () {
        qpValue.innerHTML = this.value;
    }

    /* Video Bitrate Slider */

    const bitrateValue = document.getElementById("bitrate_value");

    bitrateValue.innerHTML = bitrateSlider.value;

    bitrateSlider.oninput = function () {
        bitrateValue.innerHTML = this.value;
    }

    /* Audio Bitrate Slider */

    const audioSlider = document.getElementById("id_audio_bitrate");
    const audioValue = document.getElementById("audio_value");

    audioValue.innerHTML = audioSlider.value;

    audioSlider.oninput = function () {
        audioValue.innerHTML = this.value;
    }

    /* Brightness Slider */

    const brightnessBoolean = document.getElementById("id_video_brightness_boolean");
    const brightnessSlider = document.getElementById("id_video_brightness_value");
    const brightnessValue = document.getElementById("brightness_value");

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

    const contrastBoolean = document.getElementById("id_video_contrast_boolean")
    const contrastSlider = document.getElementById("id_video_contrast_value");
    const contrastValue = document.getElementById("contrast_value");

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

    const saturationBoolean = document.getElementById("id_video_saturation_boolean")
    const saturationSlider = document.getElementById("id_video_saturation_value");
    const saturationValue = document.getElementById("saturation_value");

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

    const volumeSlider = document.getElementById("id_audio_volume");
    const volumeValue = document.getElementById("volume_value");

    volumeValue.innerHTML = Math.round(volumeSlider.value * 100);

    volumeSlider.oninput = function () {
        volumeValue.innerHTML = Math.round(this.value * 100);
    }

    /* EQ Presets and Sliders */

    const eqPresets = document.getElementById("id_equalizer_preset");
    
    const barSliderFunction = (sliderBar, sliderValue) => {
        let slider = document.getElementById(sliderBar);
        let sliderVal = document.getElementById(sliderValue);

        sliderVal.innerHTML = slider.value;

        slider.oninput = function () {
            sliderVal.innerHTML = this.value;
            eqPresets.value = "custom";
        }
    }

    barSliderFunction("id_eq_ten_band_1", "eq_bar_1");
    barSliderFunction("id_eq_ten_band_2", "eq_bar_2");
    barSliderFunction("id_eq_ten_band_3", "eq_bar_3");
    barSliderFunction("id_eq_ten_band_4", "eq_bar_4");
    barSliderFunction("id_eq_ten_band_5", "eq_bar_5");
    barSliderFunction("id_eq_ten_band_6", "eq_bar_6");
    barSliderFunction("id_eq_ten_band_7", "eq_bar_7");
    barSliderFunction("id_eq_ten_band_8", "eq_bar_8");
    barSliderFunction("id_eq_ten_band_9", "eq_bar_9");
    barSliderFunction("id_eq_ten_band_10", "eq_bar_10");

    const equalizerValues = (bandOne, bandTwo, bandThree, bandFour, bandFive, bandSix, bandSeven, bandEight, bandNine, bandTen) => {
        document.getElementById("id_eq_ten_band_1").value = document.getElementById("eq_bar_1").value = document.getElementById("eq_bar_1").innerHTML = bandOne;
        document.getElementById("id_eq_ten_band_2").value = document.getElementById("eq_bar_2").value = document.getElementById("eq_bar_2").innerHTML = bandTwo;
        document.getElementById("id_eq_ten_band_3").value = document.getElementById("eq_bar_3").value = document.getElementById("eq_bar_3").innerHTML = bandThree;
        document.getElementById("id_eq_ten_band_4").value = document.getElementById("eq_bar_4").value = document.getElementById("eq_bar_4").innerHTML = bandFour;
        document.getElementById("id_eq_ten_band_5").value = document.getElementById("eq_bar_5").value = document.getElementById("eq_bar_5").innerHTML = bandFive;
        document.getElementById("id_eq_ten_band_6").value = document.getElementById("eq_bar_6").value = document.getElementById("eq_bar_6").innerHTML = bandSix;
        document.getElementById("id_eq_ten_band_7").value = document.getElementById("eq_bar_7").value = document.getElementById("eq_bar_7").innerHTML = bandSeven;
        document.getElementById("id_eq_ten_band_8").value = document.getElementById("eq_bar_8").value = document.getElementById("eq_bar_8").innerHTML = bandEight;
        document.getElementById("id_eq_ten_band_9").value = document.getElementById("eq_bar_9").value = document.getElementById("eq_bar_9").innerHTML = bandNine;
        document.getElementById("id_eq_ten_band_10").value = document.getElementById("eq_bar_10").value = document.getElementById("eq_bar_10").innerHTML = bandTen;
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