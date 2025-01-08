const host = window.location.hostname;
const socket = io(`http://${host}:8080`);

//---------------------------------------------------------------------------//

socket.on("connect", () => {
    socket.emit('update'); 
});

socket.on('change label', (data) => {
    let labelElement = document.getElementById("Alt-Text-View");
    labelElement.innerText = data;
});

socket.on('finished reroll', (data) => {
    toggle_reroll_button();
    document.getElementById("loader").style.visibility = "hidden";
    getImage();
});

//---------------------------------------------------------------------------//

function submitAlt() {
    let text = document.getElementById("Alt-Text-Input").value;
    socket.emit('set_alt_text', text); 
}

function reroll() {
    document.getElementById("image").src = "";
    document.getElementById("loader").style.visibility = "visible";
    document.getElementById("Alt-Text-View").innerText = "";
    socket.emit('reroll');
    toggle_reroll_button();
}

function toggle_reroll_button() {
    let button = document.getElementById("Reroll-Button");
    button.disabled = !button.disabled;
}

function getImage() {
    //Add the current timestamp as query parameter to avoid caching
    let image = document.getElementById("image");
    var d = new Date();
    image.src = "/image.png?" + d.getTime();
}

//---------------------------------------------------------------------------//

$('textarea').keyup(function() {
    var count = $(this).val().length,
        current = $('#current');
        current.text(count);
});

getImage();