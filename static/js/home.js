var MAX_QUEUE_LENGTH = 5;

var songNames = [];
var songIds = [];
var songIsPlaying = false;

addEventListener("DOMContentLoaded", function() {
    var options = {target: document.getElementById("nanobar")};
    var nanobar = new Nanobar(options);
    nanobar.go(0);
    var playButtons = document.querySelectorAll(".play_button");
    for (var i=0, l=playButtons.length; i<l; i++) {
        var button = playButtons[i];
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (songNames.length < MAX_QUEUE_LENGTH) {
                var clickedButton = e.target;
                var songName = clickedButton.name;
                var songId = clickedButton.id;
                var request = new XMLHttpRequest();
                request.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        songNames.shift();
                        songIds.shift();
                        if (songNames.length == 0) {
                            songIsPlaying = false;
                        }
                        nanobar.go(0);
                        updateSongQueue();
                        if (songIds.length > 0) {
                            startNanobarProgress(songIds[0], nanobar);
                        }
                    }
                }
                request.open("GET", "/play/" + songId, true);
                request.send();
                songNames.push(songName);
                songIds.push(songId);
                nanobar.go(0);
                updateSongQueue();
                if (!songIsPlaying) {
                    startNanobarProgress(songId, nanobar);
                }
                songIsPlaying = true;
            }
        });
    }
}, true);



function updateSongQueue() {
    if (songNames.length > 0) {
        document.getElementById("current_song").innerHTML = "Currently playing: " + songNames[0];
    }
    else {
        document.getElementById("current_song").innerHTML = ""
    }

    if (songNames.length > 1) {
        document.getElementById("next_song").innerHTML = "Next: " + songNames[1];
    }
    else {
        document.getElementById("next_song").innerHTML = ""
    }

    if (songNames.length == 3) {
        document.getElementById("num_songs").innerHTML = "1 more song in the queue";
    }
    else if (songNames.length > 3) {
        document.getElementById("num_songs").innerHTML = (songNames.length-2).toString() + " more songs in the queue";
    }
    else {
        document.getElementById("num_songs").innerHTML = ""
    }
}

function startNanobarProgress(songId, nanobar) {
    var startTime = 0;
    var songTime = 0;
    if (songId == "LetItGo") {
        songTime = 2170;
    }
    else if (songId == "CarolOfTheBells") {
        songTime = 2030;
    }
    else if (songId == "MadRussianXmas") {
        songTime = 2790;
    }
    else if (songId == "LinusAndLucy") {
        songTime = 1830;
    }
    else if (songId == "SilentNight") {
        songTime = 1240;
    }
    else if (songId == "WizardsInWinter") {
        songTime = 1830;
    }
    var timeInterval = setInterval(function () {
        startTime += 1;
        nanobar.go((startTime/songTime) * 100);
        if (startTime >= songTime) {
            clearInterval(timeInterval);
            nanobar.go(0);
        }
    }, 100);
}

$(document).ready(function() {
    $('#musicTable').DataTable();
});
