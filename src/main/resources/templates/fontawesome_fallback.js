"use strict";

const pWatched = document.createElement("p");
pWatched.classList.add("watched");
pWatched.innerHTML = "Watched";
pWatched.title = "Watched";

const pNotWatched = document.createElement("p");
pNotWatched.classList.add("not_watched");
pNotWatched.innerHTML = "Not watched";
pNotWatched.title = "Not watched";

function noConnectionExists() {
    let watched = document.getElementsByClassName("watched");
    let notWatched = document.getElementsByClassName("not_watched");

    for (let i = 0; i < watched.length; i++) {
        let parent = watched[i].parentNode;
        parent.removeChild(parent.childNodes[0]);
        parent.appendChild(pWatched.cloneNode(true));
    }

    for (let i = 0; i < notWatched.length; i++) {
        let parent = notWatched[i].parentNode;
        parent.removeChild(parent.childNodes[0]);
        parent.appendChild(pNotWatched.cloneNode(true));
    }
}

function checkForConnection() {
    const request = new XMLHttpRequest();
    const file = "https://use.fontawesome.com/releases/v5.3.1/css/all.css";
    const randomNum = Math.round(Math.random() * 10000);

    request.open("HEAD", file + "?rand=" + randomNum, true);
    request.send();

    request.onload = () => {
        if (request.readyState === 4) {
            if (request.status !== 200) {
                noConnectionExists();
            }
        }
    };

    request.onerror = () => {
        noConnectionExists();
    };
}

window.addEventListener("load", () => {
    checkForConnection();
});