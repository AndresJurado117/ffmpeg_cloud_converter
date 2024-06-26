document.addEventListener("DOMContentLoaded", () => {
    
    //  Declare Video Mode and Sliders
    const videoResolution = document.getElementById("id_video_resolution");
    const videoMode = document.getElementById("id_video_mode");
    const qpSlider = document.getElementById("id_video_qp");
    const bitrateSlider = document.getElementById("id_video_bitrate");

    videoMode.onchange = function() {
        if (this.value == "qp") {
            qpSlider.disabled = false;
            bitrateSlider.disabled = true;
        }
        else if (this.value == "vbr") {
            qpSlider.disabled = true;
            bitrateSlider.disabled = false;
        };
    };

    // QP Slider

    const qpValue = document.getElementById("qp_value");

    qpValue.innerHTML = qpSlider.value;

    qpSlider.oninput = function() {
        qpValue.innerHTML = this.value;
    };

    // Video Bitrate Slider

    const bitrateValue = document.getElementById("bitrate_value");

    bitrateValue.innerHTML = bitrateSlider.value;

    bitrateSlider.oninput = function() {
        bitrateValue.innerHTML = this.value;
    };

    // Audio Bitrate Slider

    const audioSlider = document.getElementById("id_audio_bitrate");
    const audioValue = document.getElementById("audio_value");

    audioValue.innerHTML = audioSlider.value;

    audioSlider.oninput = function() { 
        audioValue.innerHTML = this.value;
    };

    // Video Preset Select

    const videoPresetSelect = document.getElementById("id_video_preset");

    // Video Filters

    const vFMirrorBoolean = document.getElementById("id_video_flip");
    const vfGreenOutlinesBoolean = document.getElementById("id_green_outlines");
    const vfFrameInterpolationBoolean = document.getElementById("id_frame_interpolation");
    const vfGaussianBlurBoolean = document.getElementById("id_gaussian_blur");
    

    // Brightness Slider

    const brightnessBoolean = document.getElementById("id_video_brightness_boolean");
    const brightnessSlider = document.getElementById("id_video_brightness_value");
    const brightnessValue = document.getElementById("brightness_value");

    brightnessBoolean.onclick = function() {
        if (brightnessSlider.disabled == true) {
            brightnessSlider.disabled = false;
        }
        else {
            brightnessSlider.disabled = true;
        };
    };

    brightnessValue.innerHTML = parseFloat(brightnessSlider.value).toFixed(2);

    brightnessSlider.oninput = function() {
        brightnessValue.innerHTML = parseFloat(this.value).toFixed(2);
    }

    // Contrast Slider

    const contrastBoolean = document.getElementById("id_video_contrast_boolean");
    const contrastSlider = document.getElementById("id_video_contrast_value");
    const contrastValue = document.getElementById("contrast_value");

    contrastBoolean.onclick = function() {
        if (contrastSlider.disabled == true) {
            contrastSlider.disabled = false;
        }
        else {
            contrastSlider.disabled = true;
        };
    };

    contrastValue.innerHTML = parseFloat(contrastSlider.value).toFixed(2);

    contrastSlider.oninput = function() {
        contrastValue.innerHTML = parseFloat(this.value).toFixed(2);
    };

    // Saturation Slider

    const saturationBoolean = document.getElementById("id_video_saturation_boolean");
    const saturationSlider = document.getElementById("id_video_saturation_value");
    const saturationValue = document.getElementById("saturation_value");

    saturationBoolean.onclick = function() {
        if (saturationSlider.disabled == true) {
            saturationSlider.disabled = false;
        }
        else {
            saturationSlider.disabled = true;
        };
    };

    saturationValue.innerHTML = parseFloat(saturationSlider.value).toFixed(2);

    saturationSlider.oninput = function() {
        saturationValue.innerHTML = parseFloat(this.value).toFixed(2);
    }

    // LUT

    const lutSelect = document.getElementById("id_video_lut");

    // Volume Slider

    const volumeSlider = document.getElementById("id_audio_volume");
    const volumeValue = document.getElementById("volume_value");

    volumeValue.innerHTML = Math.round(volumeSlider.value * 100);

    volumeSlider.oninput = function() {
        volumeValue.innerHTML = Math.round(this.value * 100);
    };

    // EQ Presets and Sliders

    const eqPresetsSelect = document.getElementById("id_equalizer_preset");
    
    const barSliderFunction = (sliderBar, sliderValue) => {
        let slider = document.getElementById(sliderBar);
        let sliderVal = document.getElementById(sliderValue);

        sliderVal.innerHTML = slider.value;

        slider.oninput = function() {
            sliderVal.innerHTML = this.value;
            eqPresetsSelect.value = "custom";
        };
    };

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

    const tenBand1 = document.getElementById("id_eq_ten_band_1");
    const tenBand2 = document.getElementById("id_eq_ten_band_2");
    const tenBand3 = document.getElementById("id_eq_ten_band_3");
    const tenBand4 = document.getElementById("id_eq_ten_band_4");
    const tenBand5 = document.getElementById("id_eq_ten_band_5");
    const tenBand6 = document.getElementById("id_eq_ten_band_6");
    const tenBand7 = document.getElementById("id_eq_ten_band_7");
    const tenBand8 = document.getElementById("id_eq_ten_band_8");
    const tenBand9 = document.getElementById("id_eq_ten_band_9");
    const tenBand10 = document.getElementById("id_eq_ten_band_10");

    const equalizerValues = (bandOne, bandTwo, bandThree, bandFour, bandFive, bandSix, bandSeven, bandEight, bandNine, bandTen) => {
        tenBand1.value = document.getElementById("eq_bar_1").value = document.getElementById("eq_bar_1").innerHTML = bandOne;
        tenBand2.value = document.getElementById("eq_bar_2").value = document.getElementById("eq_bar_2").innerHTML = bandTwo;
        tenBand3.value = document.getElementById("eq_bar_3").value = document.getElementById("eq_bar_3").innerHTML = bandThree;
        tenBand4.value = document.getElementById("eq_bar_4").value = document.getElementById("eq_bar_4").innerHTML = bandFour;
        tenBand5.value = document.getElementById("eq_bar_5").value = document.getElementById("eq_bar_5").innerHTML = bandFive;
        tenBand6.value = document.getElementById("eq_bar_6").value = document.getElementById("eq_bar_6").innerHTML = bandSix;
        tenBand7.value = document.getElementById("eq_bar_7").value = document.getElementById("eq_bar_7").innerHTML = bandSeven;
        tenBand8.value = document.getElementById("eq_bar_8").value = document.getElementById("eq_bar_8").innerHTML = bandEight;
        tenBand9.value = document.getElementById("eq_bar_9").value = document.getElementById("eq_bar_9").innerHTML = bandNine;
        tenBand10.value = document.getElementById("eq_bar_10").value = document.getElementById("eq_bar_10").innerHTML = bandTen;
    };

    eqPresetsSelect.onchange = function() {
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
        };
    };

    // Loading Bar
    const convertBtn = document.getElementById("convert_btn");
    const progressBar = document.getElementById("progress_bar");
    const loadingDots = document.getElementById("loading_dots");

    form = document.getElementById("form-video-convert");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const attachedFile = document.getElementById("id_input_file");

        if (attachedFile.files.length == 1) {
            progressBar.style.display = "block";
            convertBtn.style.display = "none";
            
            const id = setInterval(frame, 500);
            function frame() {
                if (loadingDots.innerHTML.length >= 3) {
                    loadingDots.innerHTML = "";
                }
                else {
                    loadingDots.innerHTML += ".";
                }
            };
        }
        else {
            console.log("File does not exist");
        }

        const formData = new FormData(form);
        fetch("/conversion/", {
            method: "POST",
            body: formData
        })
        .then(videoResolution.disabled=true, videoMode.disabled=true, qpSlider.disabled=true, bitrateSlider.disabled=true, audioSlider.disabled=true, videoPresetSelect.disabled=true, brightnessBoolean.disabled=true, vFMirrorBoolean.disabled=true, vfGreenOutlinesBoolean.disabled=true, vfFrameInterpolationBoolean.disabled=true, vfGaussianBlurBoolean.disabled=true, brightnessSlider.disabled=true, contrastSlider.disabled=true, saturationSlider.disabled=true, lutSelect.disabled=true, volumeSlider.disabled=true, eqPresetsSelect.disabled=true, tenBand1.disabled=true, tenBand2.disabled=true, tenBand3.disabled=true, tenBand4.disabled=true, tenBand5.disabled=true, tenBand6.disabled=true, tenBand7.disabled=true, tenBand8.disabled=true, tenBand9.disabled=true, tenBand10.disabled=true)
        .then(response => response.json())
        .then(function() {
            window.location = "/conversion/", {
                method: "GET",
                data: {
                    videoName: document.getElementById("id_input_file").value.replace("C:\\fakepath\\","")
                }
            }
        })

        window.addEventListener("pageshow", () => {
            videoResolution.disabled = false;
            videoMode.disabled = false;
            qpSlider.disabled = false;
            bitrateSlider.disabled = false;
            audioSlider.disabled = false;
            videoPresetSelect.disabled=false;
            brightnessBoolean.disabled=false;
            vFMirrorBoolean.disabled=false;
            vfGreenOutlinesBoolean.disabled=false;
            vfFrameInterpolationBoolean.disabled=false;
            vfGaussianBlurBoolean.disabled=false;
            brightnessSlider.disabled=false;
            contrastSlider.disabled=false;
            saturationSlider.disabled=false;
            lutSelect.disabled=false;
            volumeSlider.disabled=false;
            eqPresetsSelect.disabled=false;
            tenBand1.disabled=false;
            tenBand2.disabled=false;
            tenBand3.disabled=false;
            tenBand4.disabled=false;
            tenBand5.disabled=false;
            tenBand6.disabled=false;
            tenBand7.disabled=false;
            tenBand8.disabled=false;
            tenBand9.disabled=false;
            tenBand10.disabled=false;
            progressBar.style.display = "none";
            convertBtn.style.display = "block";
        });
    })
});