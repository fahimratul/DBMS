
const popupDivs = document.querySelectorAll('.popup-content-div.color');
let currentDiv = 0;

document.getElementById("requestdonation").addEventListener("click", function() {
    document.querySelector(".popup").style.display = "flex";
    document.body.style.overflow = "hidden";
    currentDiv = 0;
});
document.getElementById("popup-close-btn").addEventListener("click", function() {
    document.querySelector(".popup").style.display = "none";
});


// Hide all except the first
popupDivs.forEach((div, idx) => {
    div.style.display = idx === 0 ? 'flex' : 'none';
});

// Add next button functionality
const nextButtons = document.querySelectorAll('.popup-content-div.color .donate-submit:not(.prev)');
nextButtons.forEach((btn) => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        if (currentDiv < popupDivs.length - 1) {
            popupDivs[currentDiv].style.display = 'none';
            currentDiv++;
            popupDivs[currentDiv].style.display = 'flex';
        }
    });
});

// Add previous button functionality
const prevButtons = document.querySelectorAll('.popup-content-div.color .donate-submit.prev');
prevButtons.forEach((btn) => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        if (currentDiv > 0) {
            popupDivs[currentDiv].style.display = 'none';
            currentDiv--;
            popupDivs[currentDiv].style.display = 'flex';
        }
    });
});


// Add form submission functionality
document.getElementById("request-submit").addEventListener("click", function(e) {
    document.querySelector(".popup").style.display = "none";
    e.preventDefault();
    const doneDiv = document.querySelector(".subimitondone");
    doneDiv.style.display = "flex";
    doneDiv.style.opacity = "1";
    doneDiv.style.transition = "opacity 0.5s";

    setTimeout(() => {
        doneDiv.style.opacity = "0";
        setTimeout(() => {
            doneDiv.style.display = "none";
            doneDiv.style.opacity = "1";
        }, 700);
    }, 200);
}); 

document.getElementById("notification-close-btn").addEventListener("click", function() {
    document.querySelector(".subimitondone").style.display = "none";
});