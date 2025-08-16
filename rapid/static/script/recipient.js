// Application State
let currentStep = 1;
const totalSteps = 5;
let currentView = 'form';
let isLoading = false;

// Form Data
let formData = {
    reliefItems: {
        'Food assistance': { needed: false, amount: '', otherDetails: '' },
        'Temporary housing': { needed: false, amount: '', otherDetails: '' },
        'Medical assistance': { needed: false, amount: '', otherDetails: '' },
        'Clothing/Personal items': { needed: false, amount: '', otherDetails: '' },
        'Transportation': { needed: false, amount: '', otherDetails: '' },
        'Financial assistance': { needed: false, amount: '', otherDetails: '' },
        'Child care': { needed: false, amount: '', otherDetails: '' },
        'Mental health support': { needed: false, amount: '', otherDetails: '' },
        'Others': { needed: false, amount: '', otherDetails: '' }
    },
    supportingImages: [],
    gpsCoordinates: {
        latitude: '',
        longitude: ''
    }
};

// Mock Status Data
const mockRequests = [
    {
        id: 'REQ-001',
        firstName: 'Rashid',
        lastName: 'Ahmed',
        email: 'rashid.ahmed@email.com',
        phone: '+880 1712-345678',
        address: '23/A Dhanmondi Road',
        city: 'Dhaka',
        division: 'Dhaka',
        postalCode: '1205',
        gpsCoordinates: { latitude: 23.8103, longitude: 90.4125 },
        reliefItems: {
            'Food assistance': { needed: true, amount: '25 kg', otherDetails: 'Rice, lentils, oil' },
            'Financial assistance': { needed: true, amount: '৳15,000', otherDetails: 'House rent payment' }
        },
        priorityLevel: 'high',
        priorityMessage: 'Elderly person with diabetes, needs immediate food assistance after flood',
        supportingImages: ['medical-report.jpg', 'nid-card.jpg'],
        status: 'in-progress',
        assignedTeam: 'Relief Team Dhaka-1',
        teamContact: 'Fatima Khatun - +880 1987-654321',
        dateSubmitted: '2025-01-15'
    },
    {
        id: 'REQ-002',
        firstName: 'Nasir',
        lastName: 'Uddin',
        email: 'nasir.uddin@email.com',
        phone: '+880 1856-789012',
        address: '45 Agrabad Commercial Area',
        city: 'Chittagong',
        division: 'Chittagong',
        postalCode: '4100',
        gpsCoordinates: { latitude: 22.3569, longitude: 91.7832 },
        reliefItems: {
            'Temporary housing': { needed: true, amount: '2 weeks', otherDetails: 'Family of 5' },
            'Child care': { needed: true, amount: '3 children', otherDetails: 'Ages 4, 7, 10' }
        },
        priorityLevel: 'medium',
        priorityMessage: 'House damaged in cyclone, need temporary shelter for family',
        supportingImages: ['house-damage.jpg'],
        status: 'relief-sent',
        assignedTeam: 'Relief Team Chittagong-2',
        teamContact: 'Abdul Karim - +880 1765-432109',
        dateSubmitted: '2025-01-10'
    }
];

// DOM Elements
const elements = {
    // Navigation
    navForm: document.getElementById('nav-form'),
    navStatus: document.getElementById('nav-status'),
    navFeedback: document.getElementById('nav-feedback'),
    floatingFeedbackBtn: document.getElementById('floating-feedback-btn'),
    
    // Views
    formView: document.getElementById('form-view'),
    statusView: document.getElementById('status-view'),
    feedbackView: document.getElementById('feedback-view'),
    
    // Success Message
    successMessage: document.getElementById('success-message'),
    viewStatusBtn: document.getElementById('view-status-btn'),
    closeSuccessBtn: document.getElementById('close-success-btn'),
    
    // Progress
    stepIndicator: document.getElementById('step-indicator'),
    progressFill: document.getElementById('progress-fill'),
    loadingSpinner: document.getElementById('loading-spinner'),
    
    // Form
    reliefForm: document.getElementById('relief-form'),
    reliefItemsContainer: document.getElementById('relief-items-container'),
    fileInput: document.getElementById('file-input'),
    fileUploadBtn: document.getElementById('file-upload-btn'),
    fileUploadArea: document.getElementById('file-upload-area'),
    uploadedFiles: document.getElementById('uploaded-files'),
    reviewContent: document.getElementById('review-content'),
    
    // GPS Elements
    detectLocationBtn: document.getElementById('detect-location-btn'),
    latitudeInput: document.getElementById('latitude'),
    longitudeInput: document.getElementById('longitude'),
    locationStatus: document.getElementById('location-status'),
    
    // Navigation buttons
    prevBtn: document.getElementById('prev-btn'),
    nextBtn: document.getElementById('next-btn'),
    nextBtnText: document.getElementById('next-btn-text'),
    nextBtnIcon: document.getElementById('next-btn-icon'),
    nextBtnSpinner: document.getElementById('next-btn-spinner'),
    newRequestBtn: document.getElementById('new-request-btn'),
    backToFormBtn: document.getElementById('back-to-form-btn'),
    
    // Status
    statusContainer: document.getElementById('status-container')
};

// Initialize Application
function init() {
    setupEventListeners();
    generateReliefItems();
    updateStep();
    loadStatusData();
    setActiveView('form');
}

// Event Listeners
function setupEventListeners() {
    // Navigation
    elements.navForm.addEventListener('click', () => setActiveView('form'));
    elements.navStatus.addEventListener('click', () => setActiveView('status'));
    elements.navFeedback.addEventListener('click', () => setActiveView('feedback'));
    elements.floatingFeedbackBtn.addEventListener('click', () => setActiveView('feedback'));
    elements.newRequestBtn.addEventListener('click', () => setActiveView('form'));
    elements.backToFormBtn.addEventListener('click', () => setActiveView('form'));
    
    // Success message
    elements.viewStatusBtn.addEventListener('click', () => {
        hideSuccessMessage();
        setActiveView('status');
    });
    elements.closeSuccessBtn.addEventListener('click', hideSuccessMessage);
    
    // Form navigation
    elements.prevBtn.addEventListener('click', previousStep);
    elements.nextBtn.addEventListener('click', nextStep);
    
    // Form submission
    elements.reliefForm.addEventListener('submit', handleSubmit);
    
    // File upload
    elements.fileUploadBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileUploadArea.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileUpload);
    
    // GPS Detection
    elements.detectLocationBtn.addEventListener('click', detectLocation);
    elements.latitudeInput.addEventListener('input', (e) => {
        formData.gpsCoordinates.latitude = e.target.value;
    });
    elements.longitudeInput.addEventListener('input', (e) => {
        formData.gpsCoordinates.longitude = e.target.value;
    });
    
    // Form inputs
    document.addEventListener('change', handleFormChange);
    document.addEventListener('input', handleFormChange);
}

// GPS Location Detection
function detectLocation() {
    if (!navigator.geolocation) {
        showLocationStatus('Geolocation is not supported by this browser.', 'error');
        return;
    }

    elements.detectLocationBtn.disabled = true;
    elements.detectLocationBtn.textContent = 'Detecting...';
    showLocationStatus('Getting your location...', 'loading');

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude.toFixed(6);
            const lng = position.coords.longitude.toFixed(6);
            
            elements.latitudeInput.value = lat;
            elements.longitudeInput.value = lng;
            formData.gpsCoordinates.latitude = lat;
            formData.gpsCoordinates.longitude = lng;
            
            showLocationStatus(`Location detected successfully! Accuracy: ${Math.round(position.coords.accuracy)}m`, 'success');
            elements.detectLocationBtn.disabled = false;
            elements.detectLocationBtn.textContent = 'Location Detected ✓';
            
            setTimeout(() => {
                elements.detectLocationBtn.textContent = 'Detect My Location';
            }, 3000);
        },
        (error) => {
            let errorMessage = 'Unable to detect location. ';
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage += 'Location access was denied. Please enable location services and try again.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage += 'Location information is unavailable.';
                    break;
                case error.TIMEOUT:
                    errorMessage += 'Location request timed out. Please try again.';
                    break;
                default:
                    errorMessage += 'An unknown error occurred.';
                    break;
            }
            showLocationStatus(errorMessage, 'error');
            elements.detectLocationBtn.disabled = false;
            elements.detectLocationBtn.textContent = 'Detect My Location';
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 60000
        }
    );
}

// Show location status
function showLocationStatus(message, type) {
    elements.locationStatus.textContent = message;
    elements.locationStatus.className = `location-status ${type}`;
    
    if (type === 'success' || type === 'error') {
        setTimeout(() => {
            elements.locationStatus.className = 'location-status';
        }, 5000);
    }
}

// Success Message Functions
function showSuccessMessage() {
    elements.successMessage.classList.remove('hide');
    elements.successMessage.classList.add('show');
}

function hideSuccessMessage() {
    elements.successMessage.classList.add('hide');
    setTimeout(() => {
        elements.successMessage.classList.remove('show', 'hide');
    }, 300);
}

// View Management
function setActiveView(view) {
    currentView = view;
    
    // Update navigation active states
    elements.navForm.classList.remove('active');
    elements.navStatus.classList.remove('active');
    elements.navFeedback.classList.remove('active');
    
    // Hide all views
    elements.formView.classList.add('view-hidden');
    elements.statusView.classList.add('view-hidden');
    elements.feedbackView.classList.add('view-hidden');
    
    // Show selected view and update navigation
    if (view === 'form') {
        elements.formView.classList.remove('view-hidden');
        elements.navForm.classList.add('active');
    } else if (view === 'status') {
        elements.statusView.classList.remove('view-hidden');
        elements.navStatus.classList.add('active');
    } else if (view === 'feedback') {
        elements.feedbackView.classList.remove('view-hidden');
        elements.navFeedback.classList.add('active');
    }
    
    // Add fade in animation
    const activeView = view === 'form' ? elements.formView : 
                      view === 'status' ? elements.statusView : elements.feedbackView;
    activeView.classList.add('animate-fadeInUp');
    
    // Remove animation class after animation completes
    setTimeout(() => {
        activeView.classList.remove('animate-fadeInUp');
    }, 600);
}

// Step Management
function updateStep() {
    // Update step indicator
    elements.stepIndicator.textContent = `Step ${currentStep} of ${totalSteps}`;
    
    // Update progress bar
    const progressPercent = (currentStep / totalSteps) * 100;
    elements.progressFill.style.width = `${progressPercent}%`;
    
    // Show/hide steps
    for (let i = 1; i <= totalSteps; i++) {
        const step = document.getElementById(`step-${i}`);
        if (i === currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    }
    
    // Update navigation buttons
    elements.prevBtn.disabled = currentStep === 1;
    
    if (currentStep === totalSteps) {
        elements.nextBtnText.textContent = 'Submit Request';
        elements.nextBtnIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>';
    } else {
        elements.nextBtnText.textContent = 'Next';
        elements.nextBtnIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>';
    }
}

// Step Navigation
async function nextStep() {
    if (isLoading) return;
    
    if (currentStep === totalSteps) {
        await handleSubmit();
        return;
    }
    
    // Validate current step
    if (!validateStep(currentStep)) {
        return;
    }
    
    setLoading(true);
    
    // Simulate loading
    await new Promise(resolve => setTimeout(resolve, 800));
    
    currentStep++;
    updateStep();
    
    if (currentStep === 5) {
        generateReviewContent();
    }
    
    setLoading(false);
}

function previousStep() {
    if (currentStep > 1) {
        currentStep--;
        updateStep();
    }
}

// Loading State
function setLoading(loading) {
    isLoading = loading;
    elements.nextBtn.disabled = loading;
    
    if (loading) {
        elements.loadingSpinner.classList.add('active');
        elements.nextBtnSpinner.classList.add('active');
        elements.nextBtnIcon.style.display = 'none';
    } else {
        elements.loadingSpinner.classList.remove('active');
        elements.nextBtnSpinner.classList.remove('active');
        elements.nextBtnIcon.style.display = 'block';
    }
}

// Form Validation
function validateStep(step) {
    const requiredFields = {
        1: ['first-name', 'last-name', 'email', 'phone', 'date-of-birth'],
        2: ['address', 'city', 'division', 'postal-code'],
        3: [], // Relief items validation is custom
        4: ['priority-message'], // Priority level validation is custom
        5: [] // Review step
    };
    
    // Check required fields
    const fields = requiredFields[step] || [];
    for (const fieldId of fields) {
        const field = document.getElementById(fieldId);
        if (!field || !field.value.trim()) {
            if (field) {
                field.focus();
                field.style.borderColor = '#ef4444';
                setTimeout(() => field.style.borderColor = '', 3000);
            }
            showError(`Please fill in all required fields.`);
            return false;
        }
    }
    
    // Custom validations
    if (step === 3) {
        const hasSelectedRelief = Object.values(formData.reliefItems).some(item => item.needed);
        if (!hasSelectedRelief) {
            showError('Please select at least one type of relief assistance.');
            return false;
        }
    }
    
    if (step === 4) {
        const priorityLevel = document.querySelector('input[name="priorityLevel"]:checked');
        if (!priorityLevel) {
            showError('Please select a priority level.');
            return false;
        }
    }
    
    return true;
}

// Error Display
function showError(message) {
    alert(message); // Simple alert for now, could be enhanced with toast notifications
}

// Form Change Handler
function handleFormChange(event) {
    const { target } = event;
    
    if (target.matches('.relief-item-checkbox')) {
        const item = target.dataset.item;
        const checked = target.checked;
        
        formData.reliefItems[item].needed = checked;
        
        const details = target.closest('.relief-item').querySelector('.relief-item-details');
        if (checked) {
            details.classList.add('active');
        } else {
            details.classList.remove('active');
            // Clear values when unchecked
            formData.reliefItems[item].amount = '';
            formData.reliefItems[item].otherDetails = '';
            const amountInput = details.querySelector('.amount-input');
            const detailsInput = details.querySelector('.details-input');
            if (amountInput) amountInput.value = '';
            if (detailsInput) detailsInput.value = '';
        }
    }
    
    if (target.matches('.amount-input')) {
        const item = target.dataset.item;
        formData.reliefItems[item].amount = target.value;
    }
    
    if (target.matches('.details-input')) {
        const item = target.dataset.item;
        formData.reliefItems[item].otherDetails = target.value;
    }
}

// Relief Items Generation
function generateReliefItems() {
    const container = elements.reliefItemsContainer;
    container.innerHTML = '';
    
    Object.keys(formData.reliefItems).forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'relief-item';
        itemDiv.style.animationDelay = `${index * 0.1}s`;
        
        itemDiv.innerHTML = `
            <div class="relief-item-header">
                <input type="checkbox" class="relief-item-checkbox" data-item="${item}" id="relief-${index}">
                <label for="relief-${index}">${item}</label>
            </div>
            <div class="relief-item-details">
                <div class="relief-details-row">
                    <div class="form-group">
                        <label>Amount/Quantity Needed</label>
                        <input type="text" class="amount-input" data-item="${item}" 
                               placeholder="e.g., 25 kg, ৳15,000, 2 weeks, 3 people">
                    </div>
                    <div class="form-group">
                        <label>Additional Details</label>
                        <input type="text" class="details-input" data-item="${item}" 
                               placeholder="Specific requirements or details">
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(itemDiv);
    });
}

// File Upload
function handleFileUpload(event) {
    const files = Array.from(event.target.files);
    
    files.forEach((file, index) => {
        const fileUrl = URL.createObjectURL(file);
        formData.supportingImages.push(fileUrl);
        
        setTimeout(() => {
            refreshUploadedFiles();
        }, index * 100);
    });
    
    if (formData.supportingImages.length > 0) {
        elements.uploadedFiles.classList.add('active');
    }
}

function refreshUploadedFiles() {
    const container = elements.uploadedFiles;
    container.innerHTML = '';
    
    formData.supportingImages.forEach((imageUrl, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'uploaded-file';
        
        fileDiv.innerHTML = `
            <img src="${imageUrl}" alt="Supporting document ${index + 1}">
            <button type="button" class="file-remove-btn" onclick="removeImage(${index})">×</button>
        `;
        
        container.appendChild(fileDiv);
    });
    
    if (formData.supportingImages.length === 0) {
        container.classList.remove('active');
    }
}

function removeImage(index) {
    formData.supportingImages.splice(index, 1);
    refreshUploadedFiles();
}

// Review Content Generation
function generateReviewContent() {
    const container = elements.reviewContent;
    const form = elements.reliefForm;
    const formDataObj = new FormData(form);
    
    const personalInfo = {
        firstName: formDataObj.get('firstName'),
        lastName: formDataObj.get('lastName'),
        email: formDataObj.get('email'),
        phone: formDataObj.get('phone')
    };
    
    const locationInfo = {
        address: formDataObj.get('address'),
        city: formDataObj.get('city'),
        division: formDataObj.get('division'),
        postalCode: formDataObj.get('postalCode'),
        latitude: formData.gpsCoordinates.latitude,
        longitude: formData.gpsCoordinates.longitude
    };
    
    const priorityLevel = formDataObj.get('priorityLevel');
    const priorityMessage = formDataObj.get('priorityMessage');
    
    const selectedRelief = Object.entries(formData.reliefItems)
        .filter(([_, details]) => details.needed);
    
    container.innerHTML = `
        <div class="review-row">
            <div class="review-item review-section">
                <h4>Personal Information</h4>
                <div class="review-content-box">
                    <div>${personalInfo.firstName} ${personalInfo.lastName}</div>
                    <div>${personalInfo.email}</div>
                    <div>${personalInfo.phone}</div>
                </div>
            </div>
            <div class="review-item review-section">
                <h4>Location</h4>
                <div class="review-content-box">
                    <div>${locationInfo.address}</div>
                    <div>${locationInfo.city}, ${locationInfo.division} ${locationInfo.postalCode}</div>
                    ${locationInfo.latitude && locationInfo.longitude ? `
                        <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #059669;">
                            📍 GPS: ${locationInfo.latitude}, ${locationInfo.longitude}
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
        
        <div class="review-section">
            <h4>Requested Relief Items</h4>
            <div class="review-content-box">
                <div class="relief-items-list">
                    ${selectedRelief.map(([item, details], index) => `
                        <div class="relief-item-review" style="animation-delay: ${0.3 + index * 0.1}s">
                            <span>${item}</span>
                            <span>
                                ${details.amount} ${details.otherDetails ? `(${details.otherDetails})` : ''}
                            </span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
        
        <div class="review-section">
            <h4>Priority Level</h4>
            <div class="priority-display ${getPriorityClass(priorityLevel)}">
                ${priorityLevel?.toUpperCase()}
            </div>
            ${priorityMessage ? `
                <div class="status-priority-message" style="margin-top: 0.5rem;">
                    ${priorityMessage}
                </div>
            ` : ''}
        </div>
        
        ${formData.supportingImages.length > 0 ? `
            <div class="review-section">
                <h4>Supporting Documents</h4>
                <div class="review-content-box">
                    ${formData.supportingImages.length} file(s) uploaded
                </div>
            </div>
        ` : ''}
    `;
}

// Priority Class Helper
function getPriorityClass(priority) {
    switch (priority) {
        case 'emergency': return 'priority-emergency';
        case 'high': return 'priority-high';
        case 'medium': return 'priority-medium';
        default: return 'priority-low';
    }
}

// Form Submission
async function handleSubmit(event) {
    if (event) event.preventDefault();
    
    setLoading(true);
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    console.log('Relief request submitted:', formData);
    
    // Show success message instead of alert
    showSuccessMessage();
    
    // Reset form
    resetForm();
    setLoading(false);
}

// Form Reset
function resetForm() {
    currentStep = 1;
    elements.reliefForm.reset();
    formData.reliefItems = {
        'Food assistance': { needed: false, amount: '', otherDetails: '' },
        'Temporary housing': { needed: false, amount: '', otherDetails: '' },
        'Medical assistance': { needed: false, amount: '', otherDetails: '' },
        'Clothing/Personal items': { needed: false, amount: '', otherDetails: '' },
        'Transportation': { needed: false, amount: '', otherDetails: '' },
        'Financial assistance': { needed: false, amount: '', otherDetails: '' },
        'Child care': { needed: false, amount: '', otherDetails: '' },
        'Mental health support': { needed: false, amount: '', otherDetails: '' },
        'Others': { needed: false, amount: '', otherDetails: '' }
    };
    formData.supportingImages = [];
    formData.gpsCoordinates = { latitude: '', longitude: '' };
    
    // Reset GPS fields
    elements.latitudeInput.value = '';
    elements.longitudeInput.value = '';
    elements.detectLocationBtn.textContent = 'Detect My Location';
    elements.detectLocationBtn.disabled = false;
    elements.locationStatus.className = 'location-status';
    
    updateStep();
    generateReliefItems();
    refreshUploadedFiles();
}

// Status Management
function loadStatusData() {
    const container = elements.statusContainer;
    container.innerHTML = '';
    
    mockRequests.forEach((request, index) => {
        const requestDiv = document.createElement('div');
        requestDiv.className = 'status-card';
        requestDiv.style.animationDelay = `${index * 0.1}s`;
        
        requestDiv.innerHTML = createStatusCard(request);
        container.appendChild(requestDiv);
    });
}

function createStatusCard(request) {
    return `
        <div class="status-card-header">
            <div class="status-card-title">
                <h3>Request ID: ${request.id}</h3>
                <div class="status-badge ${getStatusClass(request.status)}">
                    ${getStatusIcon(request.status)} ${request.status.replace('-', ' ').toUpperCase()}
                </div>
            </div>
            <div class="status-date">
                Submitted: ${new Date(request.dateSubmitted).toLocaleDateString()}
            </div>
            <p class="status-card-description">
                ${request.firstName} ${request.lastName} - ${request.city}, ${request.division}
            </p>
        </div>
        
        <div class="status-card-content">
            <div class="status-info-grid">
                <div class="status-info-section">
                    <h4>Contact Information</h4>
                    <div class="status-info-content">
                        <div>${request.email}</div>
                        <div>${request.phone}</div>
                        <div>${request.address}, ${request.city}, ${request.division} ${request.postalCode}</div>
                        ${request.gpsCoordinates && request.gpsCoordinates.latitude ? `
                            <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #059669;">
                                📍 GPS: ${request.gpsCoordinates.latitude}, ${request.gpsCoordinates.longitude}
                            </div>
                        ` : ''}
                    </div>
                </div>
                <div class="status-info-section">
                    <h4>Relief Items Requested</h4>
                    <div class="status-info-content">
                        <div class="status-relief-items">
                            ${Object.entries(request.reliefItems).map(([item, details]) => `
                                <div class="status-relief-item">
                                    <span>${item}:</span>
                                    <span>${details.amount}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
            
            ${request.priorityMessage ? `
                <div>
                    <h4>Priority Message</h4>
                    <div class="status-priority-message">${request.priorityMessage}</div>
                </div>
            ` : ''}
            
            ${(request.status === 'in-progress' || request.status === 'relief-sent') && request.assignedTeam ? `
                <div class="status-team-info">
                    <h4>Assigned Team Information</h4>
                    <div class="status-team-content">
                        <div><strong>Team:</strong> ${request.assignedTeam}</div>
                        <div><strong>Contact:</strong> ${request.teamContact}</div>
                        <div class="status-team-note">
                            Your assigned team will contact you within 24 hours with updates.
                        </div>
                    </div>
                </div>
            ` : ''}
            
            ${request.status === 'relief-sent' ? `
                <div class="status-relief-update">
                    <h4>Relief Status Update</h4>
                    <div>
                        Your relief has been dispatched and should arrive within 1-2 business days. 
                        You will receive a call from the delivery team to confirm the delivery time.
                    </div>
                </div>
            ` : ''}
            
            <div class="status-progress">
                <div class="status-progress-header">
                    <span>Progress</span>
                    <span>${getProgressPercent(request.status)}%</span>
                </div>
                <div class="status-progress-bar">
                    <div class="status-progress-fill" style="width: ${getProgressPercent(request.status)}%"></div>
                </div>
            </div>
        </div>
    `;
}

// Status Helper Functions
function getStatusClass(status) {
    switch (status) {
        case 'submitted': return 'status-submitted';
        case 'in-progress': return 'status-in-progress';
        case 'relief-sent': return 'status-relief-sent';
        case 'completed': return 'status-completed';
        default: return 'status-submitted';
    }
}

function getStatusIcon(status) {
    switch (status) {
        case 'submitted': return '📄';
        case 'in-progress': return '⏰';
        case 'relief-sent': return '✅';
        case 'completed': return '⭐';
        default: return '📄';
    }
}

function getProgressPercent(status) {
    switch (status) {
        case 'submitted': return 25;
        case 'in-progress': return 50;
        case 'relief-sent': return 75;
        case 'completed': return 100;
        default: return 0;
    }
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);

// Handle browser back/forward buttons
window.addEventListener('popstate', function(event) {
    if (event.state && event.state.view) {
        setActiveView(event.state.view);
    }
});

// Add window.removeImage to global scope for onclick handlers
window.removeImage = removeImage;

// Add error handling for unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    event.preventDefault();
});

// Add error handling for general errors
window.addEventListener('error', function(event) {
    console.error('Script error:', event.error);
});