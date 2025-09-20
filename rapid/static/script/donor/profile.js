// Initialize Lucide icons
lucide.createIcons();

// Store original values for cancel functionality
let originalValues = {};

// DOM elements
const editBtn = document.getElementById('editBtn');
const saveBtn = document.getElementById('saveBtn');
const cancelBtn = document.getElementById('cancelBtn');
const profileForm = document.getElementById('profileForm');

// Event listeners
if (editBtn) editBtn.addEventListener('click', toggleEdit);
if (saveBtn) saveBtn.addEventListener('click', saveProfile);
if (cancelBtn) cancelBtn.addEventListener('click', cancelEdit);

function toggleEdit() {
    editBtn.classList.add('hidden');
    saveBtn.classList.remove('hidden');
    cancelBtn.classList.remove('hidden');

    const editableInputs = document.querySelectorAll('#profileForm input[name], #accountName, #accountId, #address');

    editableInputs.forEach(input => {
        originalValues[input.id || input.name] = input.value;
        enableInput(input); // Enable all editable inputs for editing mode
    });

    addEditingStyles();
    showNotification('Profile editing enabled. Make your changes and click Save.', 'info');
}

function enableInput(input) {
    input.disabled = false;
    input.style.backgroundColor = '#ffffff';
    input.style.borderColor = '#d1d5db';
    input.classList.add('editing');
}

function disableInput(input) {
    input.disabled = true;
    input.style.backgroundColor = '#f9fafb';
    input.style.borderColor = '#e5e7eb';
    input.classList.remove('editing');
}

function addEditingStyles() {
    if (!document.getElementById('editing-styles')) {
        const style = document.createElement('style');
        style.id = 'editing-styles';
        style.textContent = `
            .editing {
                transition: all 0.2s ease;
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
            }
            .editing:focus {
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            .editing:hover {
                border-color: #9ca3af;
            }
        `;
        document.head.appendChild(style);
    }
}

function cancelEdit() {
    Object.keys(originalValues).forEach(key => {
        const input = document.getElementById(key) || document.querySelector(`[name="${key}"]`);
        if (input) input.value = originalValues[key];
    });
    resetEditingMode();
    showNotification('Changes cancelled. Profile restored to original values.', 'info');
}

function saveProfile() {
    const nameInput = document.querySelector('input[name="name"]');
    const emailInput = document.querySelector('input[name="email"]');
    const phoneInput = document.querySelector('input[name="phone"]');
    const accountNameInput = document.getElementById('accountName');
    const accountIdInput = document.getElementById('accountId');
    const addressInput = document.getElementById('address');

    if (!validateForm(nameInput, emailInput, phoneInput)) return;

    setLoadingState(true);

    const formData = new FormData();
    formData.append('name', nameInput.value.trim());
    formData.append('email', emailInput.value.trim());
    formData.append('phone', phoneInput.value.trim());
    if (accountNameInput && accountNameInput.value.trim()) formData.append('account_name', accountNameInput.value.trim());
    if (accountIdInput && accountIdInput.value.trim()) formData.append('account_id', accountIdInput.value.trim());
    if (addressInput && addressInput.value.trim()) formData.append('address', addressInput.value.trim());

    fetch(profileForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.ok ? response.json().catch(() => location.reload()) : Promise.reject('Server error'))
    .then(data => {
        if (data && data.success) {
            showNotification('Profile updated successfully!', 'success');

            // Disable all inputs including account ID after save
            [nameInput, emailInput, phoneInput, accountNameInput, accountIdInput, addressInput].forEach(input => disableInput(input));

            // Reset buttons
            editBtn.classList.remove('hidden');
            saveBtn.classList.add('hidden');
            cancelBtn.classList.add('hidden');

            updateDisplayValues(formData);
        } else throw new Error(data.message || 'Update failed');
    })
    .catch(error => {
        console.error('Error saving profile:', error);
        showNotification(error.message || 'Failed to save changes. Please try again.', 'error');
    })
    .finally(() => setLoadingState(false));
}

function validateForm(nameInput, emailInput, phoneInput) {
    if (!nameInput.value.trim()) { showNotification('Name is required.', 'error'); nameInput.focus(); return false; }
    if (!emailInput.value.trim()) { showNotification('Email is required.', 'error'); emailInput.focus(); return false; }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput.value)) { showNotification('Please enter a valid email.', 'error'); emailInput.focus(); return false; }
    if (!phoneInput.value.trim()) { showNotification('Phone number is required.', 'error'); phoneInput.focus(); return false; }
    const phoneRegex = /^[\+]?[0-9][\d]{0,15}$/;
    if (!phoneRegex.test(phoneInput.value.replace(/[\s\-\(\)]/g, ''))) { showNotification('Please enter a valid phone number.', 'error'); phoneInput.focus(); return false; }
    return true;
}

function setLoadingState(loading) {
    if (loading) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i data-lucide="loader-2" style="width: 16px; height: 16px; animation: spin 1s linear infinite;"></i> Saving...';
        if (!document.getElementById('spinner-styles')) {
            const style = document.createElement('style');
            style.id = 'spinner-styles';
            style.textContent = `@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`;
            document.head.appendChild(style);
        }
    } else {
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i data-lucide="save" style="width: 16px; height: 16px;"></i> Save';
    }
    lucide.createIcons();
}

function updateDisplayValues(formData) {
    const displayName = document.getElementById('displayName');
    if (displayName && formData.get('name')) displayName.textContent = formData.get('name');

    const navbarUserName = document.querySelector('.menu-list span');
    if (navbarUserName && formData.get('name')) navbarUserName.textContent = formData.get('name');
}

function resetEditingMode() {
    editBtn.classList.remove('hidden');
    saveBtn.classList.add('hidden');
    cancelBtn.classList.add('hidden');

    const editableSelectors = [
        'input[name="name"]',
        'input[name="email"]',
        'input[name="phone"]',
        '#accountName',
        '#accountId',
        '#address'
    ];

    editableSelectors.forEach(selector => {
        const input = document.querySelector(selector);
        if (input) disableInput(input);
    });

    originalValues = {};
    setLoadingState(false);
}

function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) existingNotification.remove();

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background-color: ${getNotificationColor(type)};
        color: white;
        border-radius: 0.5rem;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
    `;
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
            @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
        `;
        document.head.appendChild(style);
    }
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => { if (notification.parentNode) notification.parentNode.removeChild(notification); }, 300);
    }, 4000);
}

function getNotificationColor(type) {
    switch(type) {
        case 'success': return '#10b981';
        case 'error': return '#ef4444';
        case 'warning': return '#f59e0b';
        default: return '#3b82f6';
    }
}

// Profile picture upload
function handleProfilePictureChange(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const avatarImg = document.getElementById('avatarImg');
            if (avatarImg) avatarImg.src = e.target.result;
        };
        reader.readAsDataURL(file);
        showNotification('Profile picture updated. Click Save to confirm changes.', 'success');
    } else showNotification('Please select a valid image file.', 'error');
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Profile page loaded');

    const flashMessages = document.querySelectorAll('[style*="background: #10b981"]');
    flashMessages.forEach(message => {
        showNotification(message.textContent, 'success');
        message.style.display = 'none';
    });

    // Prevent Enter submission in edit mode
    profileForm.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !saveBtn.classList.contains('hidden')) {
            e.preventDefault();
            saveProfile();
        }
    });
});

// Expose globally
window.toggleEdit = toggleEdit;
window.saveProfile = saveProfile;
window.cancelEdit = cancelEdit;
window.handleProfilePictureChange = handleProfilePictureChange;