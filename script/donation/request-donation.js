document.getElementById("requestdonation").addEventListener("click", function() {
    document.querySelector(".popup").style.display = "flex";
    document.body.style.overflow = "hidden";
});
document.getElementById("popup-close-btn").addEventListener("click", function() {
    document.querySelector(".popup").style.display = "none";
});