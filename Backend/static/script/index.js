const musicBtn = document.getElementById("musicBtn");
const bgMusic = document.getElementById("bgMusic");

let isPlaying = false;

musicBtn.addEventListener("click", () => {

    if (!isPlaying) {
        bgMusic.volume = 0.5; 
        bgMusic.play();
        musicBtn.textContent = "🔊";
        isPlaying = true;

    } else {
        bgMusic.pause();
        musicBtn.textContent = "🔇";
        isPlaying = false;
    }

});

let glowbtn = document.querySelector(".glow-btn")
// glowbtn.textContent.style = "black"
glowbtn.addEventListener("click", function () {
    // window.location.href = "login.html"
    //location.href = "login.html"

    //redirect to Flask route
    location.href = "/login"
})

