const nextsection = document.querySelectorAll('.sign-section');
let currentDiv = 0;

// Initialize section visibility
nextsection.forEach((div, idx) => {
    div.style.display = idx === 0 ? 'flex' : 'none';
});

// Handle navigation buttons (exclude submit button)
const nextButtons = document.querySelectorAll('button.donate-submit:not(.prev):not(.donate-submit-final):not([type="submit"])');
nextButtons.forEach((btn) => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        console.log('Next button clicked, currentDiv:', currentDiv);
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
        console.log('Previous button clicked, currentDiv:', currentDiv);
        if (currentDiv > 0) {
            nextsection[currentDiv].style.display = 'none';
            currentDiv--;
            nextsection[currentDiv].style.display = 'flex';
        }
    });
});

// Handle submit button
const submitButton = document.querySelector('.donate-submit-final[type="submit"]');
if (submitButton) {
    console.log('Submit button found and ready');
    submitButton.addEventListener('click', function (e) {
        console.log('Submit button clicked - attempting form submission');
        const form = submitButton.closest('form');
        if (form) {
            console.log('Form found, submitting...');
            form.submit(); // Programmatically submit the form
        } else {
            console.error('No form found for submit button!');
        }
    });
} else {
    console.error('Submit button not found!');
}