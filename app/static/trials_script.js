var timeout;

function $(id) {
    return document.getElementById(id);
};

var bins = document.getElementsByClassName("bin");
dragArr = [$("staging")]
for (i = 0; i < bins.length; i++) {
    dragArr[i + 1] = $(bins[i].id);
}
var drake = dragula(dragArr, {
    invalid: function(el, handle) {
        if (el.classList.contains('prev-card')) {
            return (true);
        } else {
            return (false);
        };
    },
}).on("drop", function(el) {
    var chosen_bin = document.getElementById("current-chosen-bin");
    chosen_bin.textContent = el.parentElement.id;
    console.log("Moved to " + el.parentElement.id);
});

function showFeedback() {
    var submit_choice_btn = document.getElementById("submit_choice_btn");
    var chosen_bin = document.getElementById("current-chosen-bin").textContent;
    var correct_bin = document.getElementById("correct_bin").textContent;
    var bin0_correct = correct_bin.substring(correct_bin.lastIndexOf("[") + 1, correct_bin.lastIndexOf(",")) == 'True';
    var bin1_correct = correct_bin.substring(correct_bin.lastIndexOf(",") + 2, correct_bin.lastIndexOf("]")) == 'True';

    // var video_obj = document.getElementById("robot-video");
    console.log("Chose " + chosen_bin);
    if (chosen_bin == "staging" || chosen_bin == "") {
        alert("Please choose one of the two bins!")
    } else {
        submit_choice_btn.classList.add("invisible");
        drake.destroy();
        var chosen_bin_obj = document.getElementById("chosen_bin");
        chosen_bin_obj.value = document.getElementById('current-chosen-bin').textContent;

        if (chosen_bin == 'bin0') {
            if (bin0_correct) {
                alert("Correct!")
            } else {
                alert("Incorrect!")
            }
        }
        if (chosen_bin == 'bin1') {
            if (bin1_correct) {
                alert("Correct!")
            } else {
                alert("Incorrect!")
            }
        }

        var submit_trial_btn = document.getElementById("submit_trial");
        submit_trial_btn.click();
        // var video_name = '../static/robot/' + 'happy' + '.mp4'; //Replace this when we have all the videos
        // video_obj.innerHTML = '<source id="robot-video-source" src="' + video_name + '" type="video/mp4">';
        // video_obj.addEventListener('ended', videoEnded, false);
        // video_obj.loop = false
        // video_obj.load();
        // video_obj.play();
    }
}

// function videoEnded(e) {
//     // What you want to do after the event
//     var chosen_bin_obj = document.getElementById("chosen_bin");
//     chosen_bin_obj.value = document.getElementById('current-chosen-bin').textContent;
//     var submit_trial_btn = document.getElementById("submit_trial");
//     submit_trial_btn.click();
// }