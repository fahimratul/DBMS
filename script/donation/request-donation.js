
const popupDivs = document.querySelectorAll('.popup-content-div.color');
let currentDiv = 0;

document.getElementById("requestdonation").addEventListener("click", function () {
    currentDiv = 0;
    document.querySelector(".popup").style.display = "flex";
    document.body.style.overflow = "hidden";
    popupDivs.forEach((div, idx) => {
        div.style.display = idx === 0 ? 'flex' : 'none';
    });
    const formElements = document.querySelectorAll('.popup-content-div.color input, .popup-content-div.color textarea, .popup-content-div.color select');
    formElements.forEach(element => {
        if (element.type === 'checkbox' || element.type === 'radio') {
            element.checked = false;
        } else {
            element.value = '';
        }
    });

});
document.getElementById("popup-close-btn").addEventListener("click", function () {
    document.body.style.overflow = "auto";
    document.querySelector(".popup").style.display = "none";
    currentDiv = 0;
    popupDivs.forEach((div, idx) => {
        div.style.display = idx === 0 ? 'flex' : 'none';
    });
    const formElements = document.querySelectorAll('.popup-content-div.color input, .popup-content-div.color textarea, .popup-content-div.color select');
    formElements.forEach(element => {
        if (element.type === 'checkbox' || element.type === 'radio') {
            element.checked = false;
        } else {
            element.value = '';
        }
    });
    document.body.style.overflow = "auto";
});


// Hide all except the first
popupDivs.forEach((div, idx) => {
    div.style.display = idx === 0 ? 'flex' : 'none';
});

// Add next button functionality
const nextButtons = document.querySelectorAll('.popup-content-div.color .donate-submit:not(.prev)');
nextButtons.forEach((btn) => {
    btn.addEventListener('click', function (e) {
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
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentDiv > 0) {
            popupDivs[currentDiv].style.display = 'none';
            currentDiv--;
            popupDivs[currentDiv].style.display = 'flex';
        }
    });
});


// Add form submission functionality
document.getElementById("request-submit").addEventListener("click", function (e) {
    document.querySelector(".popup").style.display = "none";
    document.body.style.overflow = "auto";
    // Simulate form submission
    e.preventDefault();
    const doneDiv = document.querySelector(".subimitondone");
    doneDiv.style.display = "flex";
    doneDiv.style.opacity = "1";
    doneDiv.style.transition = "opacity 0.7s ease-in-out";

    setTimeout(() => {
        doneDiv.style.opacity = "0";
        setTimeout(() => {
            doneDiv.style.display = "none";
            doneDiv.style.opacity = "1";
            currentDiv = 0;
            popupDivs.forEach((div, idx) => {
                div.style.display = idx === 0 ? 'flex' : 'none';
            });
            const formElements = document.querySelectorAll('.popup-content-div.color input, .popup-content-div.color textarea, .popup-content-div.color select');
            formElements.forEach(element => {
                if (element.type === 'checkbox' || element.type === 'radio') {
                    element.checked = false;
                } else {
                    element.value = '';
                }
            });
        }, 700);
    }, 4000);
});

document.getElementById("notification-close-btn").addEventListener("click", function () {
    document.querySelector(".subimitondone").style.display = "none";
});