const nextsection = document.querySelectorAll('.sign-section');
let currentDiv = 0;

nextsection.forEach((div, idx) => {
    div.style.display = idx === 0 ? 'flex' : 'none';
});

// Only handle navigation buttons (exclude submit button)
const nextButtons = document.querySelectorAll('button.donate-submit:not(.prev):not(.donate-submit-final)');
nextButtons.forEach((btn) => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        console.log('Next button clicked');
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
        console.log('Previous button clicked');
        if (currentDiv > 0) {
            nextsection[currentDiv].style.display = 'none';
            currentDiv--;
            nextsection[currentDiv].style.display = 'flex';
        }
    });
});

// Explicitly handle submit button - let it submit normally
const submitButton = document.querySelector('.donate-submit-final[type="submit"]');
if (submitButton) {
    console.log('Submit button found and ready');
    submitButton.addEventListener('click', function(e) {
        console.log('Submit button clicked - form will submit');
        // Don't call e.preventDefault() - let the form submit normally
    });
} else {
    console.log('Submit button not found!');
}



