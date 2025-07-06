
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
    // Collect all form data from all steps
    const formData = new FormData();
    
    // Get data from step 1
    const name = document.getElementById('name').value;
    const phone = document.getElementById('number').value;
    const emergencyPhone = document.getElementById('emergency-number').value;
    const district = document.getElementById('district_autocomplete').value;
    const postalCode = document.getElementById('postal-code').value;
    
    // Get data from step 2
    const address = document.getElementById('address').value;
    const message = document.getElementById('message').value;
    
    // Get data from step 3 & 4 (item quantities)
    const waterBottle = document.getElementById('water-bottle').value || 0;
    const rice = document.getElementById('rice').value || 0;
    const daal = document.getElementById('daal').value || 0;
    const orsaline = document.getElementById('orsaline').value || 0;
    const muriChira = document.getElementById('muri-chira').value || 0;
    const biscuit = document.getElementById('biscuit').value || 0;
    const khejur = document.getElementById('khejur').value || 0;
    const sugar = document.getElementById('sugar').value || 0;
    const toothpowder = document.getElementById('toothpowder').value || 0;
    const blanketMat = document.getElementById('blanket-mat').value || 0;
    const torch = document.getElementById('torch').value || 0;
    const soap = document.getElementById('soap').value || 0;
    
    // Get additional requirements from step 5
    const additionalReqs = document.getElementById('additional-requirements').value;
    
    // Validate required fields
    if (!name || !phone || !district || !postalCode || !address) {
        console.log('Validation failed:', { name, phone, district, postalCode, address });
        alert('Please fill in all required fields: Name, Phone, District, Postal Code, and Address');
        return;
    }
    
    // Create items list
    const items = [];
    if (waterBottle > 0) items.push(`Water bottle (500mL): ${waterBottle}`);
    if (rice > 0) items.push(`Rice (2 kg): ${rice}`);
    if (daal > 0) items.push(`Daal (2 kg): ${daal}`);
    if (orsaline > 0) items.push(`ORSaline (25 pack box): ${orsaline}`);
    if (muriChira > 0) items.push(`Muri and Chira (2 kg): ${muriChira}`);
    if (biscuit > 0) items.push(`Biscuit (1 kg): ${biscuit}`);
    if (khejur > 0) items.push(`Khejur (20 pcs): ${khejur}`);
    if (sugar > 0) items.push(`Sugar (250 gm): ${sugar}`);
    if (toothpowder > 0) items.push(`Toothpowder (1 box): ${toothpowder}`);
    if (blanketMat > 0) items.push(`Blanket and Mat (1 pc each): ${blanketMat}`);
    if (torch > 0) items.push(`Torch with batteries (1 set): ${torch}`);
    if (soap > 0) items.push(`Soap (1 pc): ${soap}`);
    
    // Combine messages
    let finalMessage = message;
    if (items.length > 0) {
        finalMessage += '\n\nRequested Items:\n' + items.join('\n');
    }
    if (additionalReqs) {
        finalMessage += '\n\nAdditional Requirements:\n' + additionalReqs;
    }
    
    // Debug: Log the data being submitted
    console.log('Submitting data:', {
        name, phone, emergencyPhone, district, postalCode, address, finalMessage
    });
    
    // Create a hidden form and submit it
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = 'php/requestdonation.php';
    form.style.display = 'none';
    
    // Add all fields as hidden inputs
    const fields = {
        'name': name,
        'phone': phone,
        'emergencynumber': emergencyPhone,
        'district': district,
        'postalcode': postalCode,
        'address': address,
        'message': finalMessage,
        'requestdonation': '1'
    };
    
    Object.entries(fields).forEach(([key, value]) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value || ''; // Ensure no null values
        form.appendChild(input);
    });
    
    // Add form to body and submit
    document.body.appendChild(form);
    
    // Close the popup before submitting
    document.querySelector(".popup").style.display = "none";
    document.body.style.overflow = "auto";
    
    // Submit the form
    setTimeout(() => {
        form.submit();
    }, 100); // Small delay to ensure DOM is ready
});

document.getElementById("notification-close-btn").addEventListener("click", function () {
    document.querySelector(".subimitondone").style.display = "none";
});