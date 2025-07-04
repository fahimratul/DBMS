
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
const nextButtons = document.querySelectorAll('.popup-content-div.color .donate-submit');
nextButtons.forEach((btn, idx) => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        if (idx < popupDivs.length - 1) {
            popupDivs[idx].style.display = 'none';
            popupDivs[idx + 1].style.display = 'flex';
        }
    });
});

// Add previous button functionality
const prevButtons = document.querySelectorAll('.popup-content-div.color .donate-submit.prev');
prevButtons.forEach((btn, idx) => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        if (idx > 0) {
            popupDivs[idx].style.display = 'none';
            popupDivs[idx - 1].style.display = 'flex';
        }
    });
});