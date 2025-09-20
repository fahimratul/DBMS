// Application State
let currentStep = 1;
const totalSteps = 5;
let currentView = "form";
let isLoading = false;

// Form Data
let formData = {
  reliefItems: {
    "Food assistance": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Temporary housing": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Medical assistance": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Clothing/Personal items": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    Transportation: {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Financial assistance": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Child care": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Mental health support": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    Others: { needed: false, amount: "", otherDetails: "", selectedItemId: "" },
  },
  supportingImages: [],
  gpsCoordinates: {
    latitude: "",
    longitude: "",
  },
};

// Status data will be loaded from backend

// DOM Elements
const elements = {
  // Header/Logo
  logoSection: document.getElementById("logo-section"),

  // Navigation
  navForm: document.getElementById("nav-form"),
  navStatus: document.getElementById("nav-status"),
  navFeedback: document.getElementById("nav-feedback"),
  floatingFeedbackBtn: document.getElementById("floating-feedback-btn"),

  // Views
  formView: document.getElementById("form-view"),
  statusView: document.getElementById("status-view"),
  feedbackView: document.getElementById("feedback-view"),

  // Success Message
  successMessage: document.getElementById("success-message"),
  viewStatusBtn: document.getElementById("view-status-btn"),
  closeSuccessBtn: document.getElementById("close-success-btn"),

  // Progress
  stepIndicator: document.getElementById("step-indicator"),
  progressFill: document.getElementById("progress-fill"),
  loadingSpinner: document.getElementById("loading-spinner"),

  // Form
  reliefForm: document.getElementById("relief-form"),
  reliefItemsContainer: document.getElementById("relief-items-container"),
  fileInput: document.getElementById("file-input"),
  fileUploadBtn: document.getElementById("file-upload-btn"),
  fileUploadArea: document.getElementById("file-upload-area"),
  uploadedFiles: document.getElementById("uploaded-files"),
  reviewContent: document.getElementById("review-content"),

  // GPS Elements
  detectLocationBtn: document.getElementById("detect-location-btn"),
  latitudeInput: document.getElementById("latitude"),
  longitudeInput: document.getElementById("longitude"),
  locationStatus: document.getElementById("location-status"),

  // Navigation buttons
  prevBtn: document.getElementById("prev-btn"),
  nextBtn: document.getElementById("next-btn"),
  nextBtnText: document.getElementById("next-btn-text"),
  nextBtnIcon: document.getElementById("next-btn-icon"),
  nextBtnSpinner: document.getElementById("next-btn-spinner"),
  newRequestBtn: document.getElementById("new-request-btn"),
  backToFormBtn: document.getElementById("back-to-form-btn"),

  // Status
  statusContainer: document.getElementById("status-container"),
};

// Initialize Application
async function init() {
  setupEventListeners();
  await generateReliefItems();
  updateStep();
  await loadStatusData();
  setActiveView("form");
}

// Event Listeners
function setupEventListeners() {
  // Logo/Header navigation - return to main page
  elements.logoSection.addEventListener("click", () => {
    window.location.href = "/";
  });

  // Navigation
  elements.navForm.addEventListener("click", () => setActiveView("form"));
  elements.navStatus.addEventListener("click", () => setActiveView("status"));
  elements.navFeedback.addEventListener(
    "click",
    () => (window.location.href = "/recipient/feedback")
  );
  elements.floatingFeedbackBtn.addEventListener(
    "click",
    () => (window.location.href = "/recipient/feedback")
  );
  elements.newRequestBtn.addEventListener("click", () => setActiveView("form"));
  elements.backToFormBtn.addEventListener("click", () => setActiveView("form"));

  // Success message
  elements.viewStatusBtn.addEventListener("click", () => {
    hideSuccessMessage();
    setActiveView("status");
  });
  elements.closeSuccessBtn.addEventListener("click", hideSuccessMessage);

  // Form navigation
  elements.prevBtn.addEventListener("click", previousStep);
  elements.nextBtn.addEventListener("click", nextStep);

  // Form submission
  elements.reliefForm.addEventListener("submit", handleSubmit);

  // File upload
  elements.fileUploadBtn.addEventListener("click", () =>
    elements.fileInput.click()
  );
  elements.fileUploadArea.addEventListener("click", () =>
    elements.fileInput.click()
  );
  elements.fileInput.addEventListener("change", handleFileUpload);

  // GPS Detection
  elements.detectLocationBtn.addEventListener("click", detectLocation);
  elements.latitudeInput.addEventListener("input", (e) => {
    formData.gpsCoordinates.latitude = e.target.value;
  });
  elements.longitudeInput.addEventListener("input", (e) => {
    formData.gpsCoordinates.longitude = e.target.value;
  });

  // Form inputs
  document.addEventListener("change", handleFormChange);
  document.addEventListener("input", handleFormChange);
}

// GPS Location Detection
function detectLocation() {
  if (!navigator.geolocation) {
    showLocationStatus(
      "Geolocation is not supported by this browser.",
      "error"
    );
    return;
  }

  elements.detectLocationBtn.disabled = true;
  elements.detectLocationBtn.textContent = "Detecting...";
  showLocationStatus("Getting your location...", "loading");

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude.toFixed(6);
      const lng = position.coords.longitude.toFixed(6);

      elements.latitudeInput.value = lat;
      elements.longitudeInput.value = lng;
      formData.gpsCoordinates.latitude = lat;
      formData.gpsCoordinates.longitude = lng;

      showLocationStatus(
        `Location detected successfully! Accuracy: ${Math.round(
          position.coords.accuracy
        )}m`,
        "success"
      );
      elements.detectLocationBtn.disabled = false;
      elements.detectLocationBtn.textContent = "Location Detected ✓";

      setTimeout(() => {
        elements.detectLocationBtn.textContent = "Detect My Location";
      }, 3000);
    },
    (error) => {
      let errorMessage = "Unable to detect location. ";
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage +=
            "Location access was denied. Please enable location services and try again.";
          break;
        case error.POSITION_UNAVAILABLE:
          errorMessage += "Location information is unavailable.";
          break;
        case error.TIMEOUT:
          errorMessage += "Location request timed out. Please try again.";
          break;
        default:
          errorMessage += "An unknown error occurred.";
          break;
      }
      showLocationStatus(errorMessage, "error");
      elements.detectLocationBtn.disabled = false;
      elements.detectLocationBtn.textContent = "Detect My Location";
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 60000,
    }
  );
}

// Show location status
function showLocationStatus(message, type) {
  elements.locationStatus.textContent = message;
  elements.locationStatus.className = `location-status ${type}`;

  if (type === "success" || type === "error") {
    setTimeout(() => {
      elements.locationStatus.className = "location-status";
    }, 5000);
  }
}

// Success Message Functions
function showSuccessMessage() {
  elements.successMessage.classList.remove("hide");
  elements.successMessage.classList.add("show");
}

function hideSuccessMessage() {
  elements.successMessage.classList.add("hide");
  setTimeout(() => {
    elements.successMessage.classList.remove("show", "hide");
  }, 300);
}

// View Management
function setActiveView(view) {
  currentView = view;

  // Update navigation active states
  elements.navForm.classList.remove("active");
  elements.navStatus.classList.remove("active");
  elements.navFeedback.classList.remove("active");

  // Hide all views
  elements.formView.classList.add("view-hidden");
  elements.statusView.classList.add("view-hidden");
  elements.feedbackView.classList.add("view-hidden");

  // Show selected view and update navigation
  if (view === "form") {
    elements.formView.classList.remove("view-hidden");
    elements.navForm.classList.add("active");
  } else if (view === "status") {
    elements.statusView.classList.remove("view-hidden");
    elements.navStatus.classList.add("active");
  } else if (view === "feedback") {
    elements.feedbackView.classList.remove("view-hidden");
    elements.navFeedback.classList.add("active");
  }

  // Add fade in animation
  const activeView =
    view === "form"
      ? elements.formView
      : view === "status"
      ? elements.statusView
      : elements.feedbackView;
  activeView.classList.add("animate-fadeInUp");

  // Remove animation class after animation completes
  setTimeout(() => {
    activeView.classList.remove("animate-fadeInUp");
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
      step.classList.add("active");
    } else {
      step.classList.remove("active");
    }
  }

  // Update navigation buttons
  elements.prevBtn.disabled = currentStep === 1;

  if (currentStep === totalSteps) {
    elements.nextBtnText.textContent = "Submit Request";
    elements.nextBtnIcon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>';
  } else {
    elements.nextBtnText.textContent = "Next";
    elements.nextBtnIcon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>';
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
  await new Promise((resolve) => setTimeout(resolve, 800));

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
    elements.loadingSpinner.classList.add("active");
    elements.nextBtnSpinner.classList.add("active");
    elements.nextBtnIcon.style.display = "none";
  } else {
    elements.loadingSpinner.classList.remove("active");
    elements.nextBtnSpinner.classList.remove("active");
    elements.nextBtnIcon.style.display = "block";
  }
}

// Form Validation
function validateStep(step) {
  const requiredFields = {
    1: ["first-name", "last-name", "email", "phone", "date-of-birth"],
    2: ["address", "city", "division", "postal-code"],
    3: [], // Relief items validation is custom
    4: ["priority-message"], // Priority level validation is custom
    5: [], // Review step
  };

  // Check required fields
  const fields = requiredFields[step] || [];
  for (const fieldId of fields) {
    const field = document.getElementById(fieldId);
    if (!field || !field.value.trim()) {
      if (field) {
        field.focus();
        field.style.borderColor = "#ef4444";
        setTimeout(() => (field.style.borderColor = ""), 3000);
      }
      showError(`Please fill in all required fields.`);
      return false;
    }
  }

  // Custom validations
  if (step === 3) {
    const hasSelectedRelief = Object.values(formData.reliefItems).some(
      (item) => item.needed
    );
    if (!hasSelectedRelief) {
      showError("Please select at least one type of relief assistance.");
      return false;
    }
  }

  if (step === 4) {
    const priorityLevel = document.querySelector(
      'input[name="priorityLevel"]:checked'
    );
    if (!priorityLevel) {
      showError("Please select a priority level.");
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

  if (target.matches(".relief-item-checkbox")) {
    const item = target.dataset.item;
    const checked = target.checked;

    formData.reliefItems[item].needed = checked;

    const details = target
      .closest(".relief-item")
      .querySelector(".relief-item-details");
    if (checked) {
      details.classList.add("active");
    } else {
      details.classList.remove("active");
      // Clear values when unchecked
      formData.reliefItems[item].amount = "";
      formData.reliefItems[item].otherDetails = "";
      formData.reliefItems[item].selectedItemId = "";
      const amountInput = details.querySelector(".amount-input");
      const detailsInput = details.querySelector(".details-input");
      const itemSelect = details.querySelector(".available-items-select");
      if (amountInput) amountInput.value = "";
      if (detailsInput) detailsInput.value = "";
      if (itemSelect) itemSelect.value = "";
    }
  }

  if (target.matches(".amount-input")) {
    const item = target.dataset.item;
    formData.reliefItems[item].amount = target.value;
  }

  if (target.matches(".details-input")) {
    const item = target.dataset.item;
    formData.reliefItems[item].otherDetails = target.value;
  }

  if (target.matches(".available-items-select")) {
    const item = target.dataset.item;
    formData.reliefItems[item].selectedItemId = target.value;
  }
}

// Relief Items Generation
async function generateReliefItems() {
  const container = elements.reliefItemsContainer;
  container.innerHTML = '<div class="loading">Loading available items...</div>';

  try {
    // Fetch available items from backend
    const response = await fetch("/recipient/get_items");
    const data = await response.json();

    if (data.success) {
      container.innerHTML = "";

      // Map backend item types to frontend relief categories
      const itemMapping = {
        Food: ["Food assistance"],
        Medicine: ["Medical assistance"],
        Clothing: ["Clothing/Personal items"],
        Shelter: ["Temporary housing"],
        Money: ["Financial assistance"],
        Water: ["Food assistance"], // Water can be part of food assistance
        Hygiene: ["Clothing/Personal items"],
        Tools: ["Others"],
        Fuel: ["Transportation"],
        Other: ["Others"],
      };

      // Create relief items based on our predefined categories
      const reliefCategories = [
        "Food assistance",
        "Temporary housing",
        "Medical assistance",
        "Clothing/Personal items",
        "Transportation",
        "Financial assistance",
        "Child care",
        "Mental health support",
        "Others",
      ];

      reliefCategories.forEach((category, index) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "relief-item";
        itemDiv.style.animationDelay = `${index * 0.1}s`;

        // Find available items for this category
        let availableItems = [];
        for (const [dbType, categories] of Object.entries(itemMapping)) {
          if (categories.includes(category) && data.items[dbType]) {
            availableItems = availableItems.concat(data.items[dbType]);
          }
        }

        itemDiv.innerHTML = `
                    <div class="relief-item-header">
                        <input type="checkbox" class="relief-item-checkbox" data-item="${category}" id="relief-${index}">
                        <label for="relief-${index}">${category}</label>
                    </div>
                    <div class="relief-item-details">
                        <div class="relief-details-row">
                            <div class="form-group">
                                <label>Amount/Quantity Needed</label>
                                <input type="text" class="amount-input" data-item="${category}" 
                                       placeholder="e.g., 25 kg, ৳15,000, 2 weeks, 3 people">
                            </div>
                            <div class="form-group">
                                <label>Additional Details</label>
                                <textarea class="details-input" data-item="${category}" 
                                          placeholder="Specific requirements or details" rows="3"></textarea>
                            </div>
                        </div>
                        ${
                          availableItems.length > 0
                            ? `
                            <div class="form-group">
                                <label>Available Items</label>
                                <select class="available-items-select" data-item="${category}">
                                    <option value="">Select specific item</option>
                                    ${availableItems
                                      .map(
                                        (item) =>
                                          `<option value="${item.id}">${item.name}</option>`
                                      )
                                      .join("")}
                                </select>
                            </div>
                        `
                            : ""
                        }
                    </div>
                `;

        container.appendChild(itemDiv);
      });
    } else {
      container.innerHTML =
        '<div class="error">Failed to load items. Please try again.</div>';
    }
  } catch (error) {
    console.error("Error loading items:", error);
    container.innerHTML =
      '<div class="error">Failed to load items. Please try again.</div>';
  }
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
    elements.uploadedFiles.classList.add("active");
  }
}

function refreshUploadedFiles() {
  const container = elements.uploadedFiles;
  container.innerHTML = "";

  formData.supportingImages.forEach((imageUrl, index) => {
    const fileDiv = document.createElement("div");
    fileDiv.className = "uploaded-file";

    fileDiv.innerHTML = `
            <img src="${imageUrl}" alt="Supporting document ${index + 1}">
            <button type="button" class="file-remove-btn" onclick="removeImage(${index})">×</button>
        `;

    container.appendChild(fileDiv);
  });

  if (formData.supportingImages.length === 0) {
    container.classList.remove("active");
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
    firstName: formDataObj.get("firstName"),
    lastName: formDataObj.get("lastName"),
    email: formDataObj.get("email"),
    phone: formDataObj.get("phone"),
  };

  const locationInfo = {
    address: formDataObj.get("address"),
    city: formDataObj.get("city"),
    division: formDataObj.get("division"),
    postalCode: formDataObj.get("postalCode"),
    latitude: formData.gpsCoordinates.latitude,
    longitude: formData.gpsCoordinates.longitude,
  };

  const priorityLevel = formDataObj.get("priorityLevel");
  const priorityMessage = formDataObj.get("priorityMessage");

  const selectedRelief = Object.entries(formData.reliefItems).filter(
    ([_, details]) => details.needed
  );

  container.innerHTML = `
        <div class="review-row">
            <div class="review-item review-section">
                <h4>Personal Information</h4>
                <div class="review-content-box">
                    <div>${personalInfo.firstName} ${
    personalInfo.lastName
  }</div>
                    <div>${personalInfo.email}</div>
                    <div>${personalInfo.phone}</div>
                </div>
            </div>
            <div class="review-item review-section">
                <h4>Location</h4>
                <div class="review-content-box">
                    <div>${locationInfo.address}</div>
                    <div>${locationInfo.city}, ${locationInfo.division} ${
    locationInfo.postalCode
  }</div>
                    ${
                      locationInfo.latitude && locationInfo.longitude
                        ? `
                        <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #059669;">
                            📍 GPS: ${locationInfo.latitude}, ${locationInfo.longitude}
                        </div>
                    `
                        : ""
                    }
                </div>
            </div>
        </div>
        
        <div class="review-section">
            <h4>Requested Relief Items</h4>
            <div class="review-content-box">
                <div class="relief-items-list">
                    ${selectedRelief
                      .map(
                        ([item, details], index) => `
                        <div class="relief-item-review" style="animation-delay: ${
                          0.3 + index * 0.1
                        }s">
                            <span>${item}</span>
                            <span>
                                ${details.amount} ${
                          details.otherDetails
                            ? `(${details.otherDetails})`
                            : ""
                        }
                            </span>
                        </div>
                    `
                      )
                      .join("")}
                </div>
            </div>
        </div>
        
        <div class="review-section">
            <h4>Priority Level</h4>
            <div class="priority-display ${getPriorityClass(priorityLevel)}">
                ${priorityLevel?.toUpperCase()}
            </div>
            ${
              priorityMessage
                ? `
                <div class="status-priority-message" style="margin-top: 0.5rem;">
                    ${priorityMessage}
                </div>
            `
                : ""
            }
        </div>
        
        ${
          formData.supportingImages.length > 0
            ? `
            <div class="review-section">
                <h4>Supporting Documents</h4>
                <div class="review-content-box">
                    ${formData.supportingImages.length} file(s) uploaded
                </div>
            </div>
        `
            : ""
        }
    `;
}

// Priority Class Helper
function getPriorityClass(priority) {
  switch (priority) {
    case "emergency":
      return "priority-emergency";
    case "high":
      return "priority-high";
    case "medium":
      return "priority-medium";
    default:
      return "priority-low";
  }
}

// Form Submission
async function handleSubmit(event) {
  if (event) event.preventDefault();

  setLoading(true);

  try {
    // Collect all form data
    const form = elements.reliefForm;
    const formDataObj = new FormData(form);

    // Prepare data for submission
    const submissionData = {
      // Personal Information
      firstName: formDataObj.get("firstName"),
      lastName: formDataObj.get("lastName"),
      email: formDataObj.get("email"),
      phone: formDataObj.get("phone"),
      dateOfBirth: formDataObj.get("dateOfBirth"),

      // Location Information
      address: formDataObj.get("address"),
      city: formDataObj.get("city"),
      division: formDataObj.get("division"),
      postalCode: formDataObj.get("postalCode"),
      latitude: formData.gpsCoordinates.latitude,
      longitude: formData.gpsCoordinates.longitude,

      // Relief Items
      reliefItems: formData.reliefItems,

      // Priority Information
      priorityLevel: formDataObj.get("priorityLevel"),
      priorityMessage: formDataObj.get("priorityMessage"),
    };

    // Submit to backend
    const response = await fetch("/recipient/submit_request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(submissionData),
    });

    const result = await response.json();

    if (result.success) {
      console.log("Relief request submitted successfully:", result);

      // Show success message
      showSuccessMessage();

      // Reset form
      resetForm();

      // Load updated status data
      await loadStatusData();
    } else {
      throw new Error(result.error || "Failed to submit request");
    }
  } catch (error) {
    console.error("Error submitting request:", error);
    showError("Failed to submit request: " + error.message);
  }

  setLoading(false);
}

// Form Reset
function resetForm() {
  currentStep = 1;
  elements.reliefForm.reset();
  formData.reliefItems = {
    "Food assistance": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Temporary housing": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Medical assistance": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Clothing/Personal items": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    Transportation: {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Financial assistance": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Child care": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    "Mental health support": {
      needed: false,
      amount: "",
      otherDetails: "",
      selectedItemId: "",
    },
    Others: { needed: false, amount: "", otherDetails: "", selectedItemId: "" },
  };
  formData.supportingImages = [];
  formData.gpsCoordinates = { latitude: "", longitude: "" };

  // Reset GPS fields
  elements.latitudeInput.value = "";
  elements.longitudeInput.value = "";
  elements.detectLocationBtn.textContent = "Detect My Location";
  elements.detectLocationBtn.disabled = false;
  elements.locationStatus.className = "location-status";

  updateStep();
  generateReliefItems();
  refreshUploadedFiles();
}

// Status Management
async function loadStatusData() {
  const container = elements.statusContainer;
  container.innerHTML = '<div class="loading">Loading your requests...</div>';

  try {
    // Fetch user requests from backend
    const response = await fetch("/recipient/get_status");
    const data = await response.json();

    if (data.success) {
      container.innerHTML = "";

      if (data.requests.length === 0) {
        container.innerHTML = `
                    <div class="no-requests">
                        <div class="no-requests-icon">📋</div>
                        <h3>No Requests Found</h3>
                        <p>You haven't submitted any relief requests yet.</p>
                        <button type="button" onclick="setActiveView('form')" class="btn-primary">Submit Your First Request</button>
                    </div>
                `;
        return;
      }

      data.requests.forEach((request, index) => {
        const requestDiv = document.createElement("div");
        requestDiv.className = "status-card";
        requestDiv.style.animationDelay = `${index * 0.1}s`;

        requestDiv.innerHTML = createStatusCard(request);
        container.appendChild(requestDiv);
      });
    } else {
      container.innerHTML =
        '<div class="error">Failed to load requests. Please try again.</div>';
    }
  } catch (error) {
    console.error("Error loading requests:", error);
    container.innerHTML =
      '<div class="error">Failed to load requests. Please try again.</div>';
  }
}

function createStatusCard(request) {
  return `
        <div class="status-card-header">
            <div class="status-card-title">
                <h3>Request ID: ${request.id}</h3>
                <div class="status-badge ${getStatusClass(request.status)}">
                    ${getStatusIcon(request.status)} ${request.status
    .replace("-", " ")
    .toUpperCase()}
                </div>
            </div>
            <div class="status-date">
                Submitted: ${new Date(request.date).toLocaleDateString()}
            </div>
            <p class="status-card-description">
                ${request.name}${request.address ? " - " + request.address : ""}
            </p>
        </div>
        
        <div class="status-card-content">
            <div class="status-info-grid">
                <div class="status-info-section">
                    <h4>Contact Information</h4>
                    <div class="status-info-content">
                        <div>${request.email || "No email provided"}</div>
                        <div>${request.phone || "No phone provided"}</div>
                        <div>${request.address || "No address provided"}</div>
                        ${
                          request.latitude && request.longitude
                            ? `
                            <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #059669;">
                                📍 GPS: ${request.latitude}, ${request.longitude}
                            </div>
                        `
                            : ""
                        }
                    </div>
                </div>
                <div class="status-info-section">
                    <h4>Relief Items Requested</h4>
                    <div class="status-info-content">
                        <div class="status-relief-items">
                            ${
                              request.relief_items.length > 0
                                ? request.relief_items
                                    .map(
                                      (item) => `
                                <div class="status-relief-item">
                                    <span>${item.name}:</span>
                                    <span>${item.quantity} units</span>
                                </div>
                              `
                                    )
                                    .join("")
                                : "<div>No items specified</div>"
                            }
                        </div>
                        ${
                          request.additional_details
                            ? `
                            <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #e5e7eb;">
                                <strong>Additional Details:</strong> ${request.additional_details}
                            </div>
                        `
                            : ""
                        }
                    </div>
                </div>
            </div>
            
            ${
              request.priority_message
                ? `
                <div>
                    <h4>Priority Message</h4>
                    <div class="status-priority-message">${request.priority_message}</div>
                </div>
            `
                : ""
            }
            
            <div class="status-progress">
                <div class="status-progress-header">
                    <span>Progress</span>
                    <span>${getProgressPercent(request.status)}%</span>
                </div>
                <div class="status-progress-bar">
                    <div class="status-progress-fill" style="width: ${getProgressPercent(
                      request.status
                    )}%"></div>
                </div>
            </div>
        </div>
    `;
}

// Status Helper Functions
function getStatusClass(status) {
  switch (status) {
    case "submitted":
      return "status-submitted";
    case "pending":
      return "status-pending";
    case "approved":
      return "status-approved";
    case "completed":
      return "status-completed";
    // Legacy status values for backward compatibility
    case "in-progress":
      return "status-in-progress";
    case "relief-sent":
      return "status-relief-sent";
    default:
      return "status-submitted";
  }
}

function getStatusIcon(status) {
  switch (status) {
    case "submitted":
      return "📄";
    case "pending":
      return "⏳";
    case "approved":
      return "✅";
    case "completed":
      return "⭐";
    // Legacy status values for backward compatibility
    case "in-progress":
      return "⏰";
    case "relief-sent":
      return "✅";
    default:
      return "📄";
  }
}

function getProgressPercent(status) {
  switch (status) {
    case "submitted":
      return 25;
    case "pending":
      return 50;
    case "approved":
      return 75;
    case "completed":
      return 100;
    // Legacy status values for backward compatibility
    case "in-progress":
      return 50;
    case "relief-sent":
      return 75;
    default:
      return 25; // Default to submitted status
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
document.addEventListener("DOMContentLoaded", init);

// Handle browser back/forward buttons
window.addEventListener("popstate", function (event) {
  if (event.state && event.state.view) {
    setActiveView(event.state.view);
  }
});

// Add window.removeImage to global scope for onclick handlers
window.removeImage = removeImage;

// Add error handling for unhandled promise rejections
window.addEventListener("unhandledrejection", function (event) {
  console.error("Unhandled promise rejection:", event.reason);
  event.preventDefault();
});

// Add error handling for general errors
window.addEventListener("error", function (event) {
  console.error("Script error:", event.error);
});
