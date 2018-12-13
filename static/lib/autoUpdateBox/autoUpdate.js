function change() {
    document.querySelector("#level1").className = "loader";
    document.querySelector("#level2").className = "face";
    document.querySelector("#level3").className = "circle1";
    document.querySelector("#level4circle").className = "updatingCiecle";
    document.querySelector("#level4line").className = "updatingline";
    document.querySelector("#saving").className = "text saving";
    document.querySelector("#ok").className = "text ok";
    document.querySelector("#saving").innerHTML = "saving";
    document.querySelector("#ok").innerHTML = "ok";
}
function ret() {
    //document.querySelector("#level2").className="faceChange"
    document.querySelector("#saving").className = "text saving1";
    document.querySelector("#ok").className = "text ok1";
    setTimeout(optimal, 1000)
}
function optimal() {
    document.querySelector("#level1").className = "toggle-button-wrapper";
    document.querySelector("#level2").className = "toggle-button";
    document.querySelector("#level3").className = "button-label";
    document.querySelector("#level4circle").className = "circle";
    document.querySelector("#level4line").className = "line";
    document.querySelector("#saving").className = "";
    document.querySelector("#ok").className = "";
    document.querySelector("#saving").innerHTML = "";
    document.querySelector("#ok").innerHTML = "";
}