const nextsection = document.querySelectorAll('.sign-section');
let currentDiv = 0;

nextsection.forEach((div, idx) => {
    div.style.display = idx === 0 ? 'flex' : 'none';
});

const nextButtons = document.querySelectorAll('.donate-submit:not(.prev)');
nextButtons.forEach((btn) => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentDiv < nextsection.length - 1) {
            nextsection[currentDiv].style.display = 'none';
            currentDiv++;
            nextsection[currentDiv].style.display = 'flex';
        }
    });
});

const prevButtons = document.querySelectorAll('.donate-submit.prev');
prevButtons.forEach((btn) => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentDiv > 0) {
            nextsection[currentDiv].style.display = 'none';
            currentDiv--;
            nextsection[currentDiv].style.display = 'flex';
        }
    });
});



