const nextsection = document.querySelectorAll(".sign-section");
let currentDiv = 0;

// Initialize section visibility
nextsection.forEach((div, idx) => {
  div.style.display = idx === 0 ? "flex" : "none";
});

// Navigation button handlers will be set up later with validation

const prevButtons = document.querySelectorAll(".donate-submit.prev");
prevButtons.forEach((btn) => {
  btn.addEventListener("click", function (e) {
    e.preventDefault();
    console.log("Previous button clicked, currentDiv:", currentDiv);
    if (currentDiv > 0) {
      nextsection[currentDiv].style.display = "none";
      currentDiv--;
      nextsection[currentDiv].style.display = "flex";
    }
  });
});

// Form validation functions
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateUsername(username) {
  const usernameRegex = /^[a-zA-Z0-9_]+$/;
  return usernameRegex.test(username) && username.length <= 20;
}

function validatePassword(password) {
  const hasUpper = /[A-Z]/.test(password);
  const hasLower = /[a-z]/.test(password);
  const hasDigit = /[0-9]/.test(password);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  const hasMinLength = password.length >= 8;

  return hasUpper && hasLower && hasDigit && hasSpecial && hasMinLength;
}

function validatePhone(phone) {
  // Allow various phone formats
  const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,20}$/;
  return phoneRegex.test(phone);
}

function showError(message, field = null) {
  alert(message); // Simple alert for now
  if (field) {
    field.style.borderColor = "#ff0000";
    field.focus();
    setTimeout(() => {
      field.style.borderColor = "";
    }, 3000);
  }
}

function validateCurrentSection(sectionIndex) {
  const currentSection = nextsection[sectionIndex];
  const inputs = currentSection.querySelectorAll(
    "input[required], textarea[required]"
  );

  for (let input of inputs) {
    if (!input.value.trim()) {
      showError(`Please fill in the ${input.name || input.id} field.`, input);
      return false;
    }

    // Specific validation based on field type
    if (input.type === "email" && !validateEmail(input.value)) {
      showError("Please enter a valid email address.", input);
      return false;
    }

    if (input.name === "phone" && !validatePhone(input.value)) {
      showError("Please enter a valid phone number.", input);
      return false;
    }

    if (input.name === "username" && !validateUsername(input.value)) {
      showError(
        "Username must be 20 characters or less and contain only letters, numbers, and underscores.",
        input
      );
      return false;
    }

    if (input.name === "password" && !validatePassword(input.value)) {
      showError(
        "Password must be at least 8 characters with uppercase, lowercase, digit, and special character.",
        input
      );
      return false;
    }

    if (input.name === "confirm_password") {
      const password = document.querySelector('input[name="password"]').value;
      if (input.value !== password) {
        showError("Passwords do not match.", input);
        return false;
      }
    }

    if (
      input.name === "account_id" &&
      (isNaN(input.value) || input.value <= 0)
    ) {
      showError("Please enter a valid account number (digits only).", input);
      return false;
    }
  }

  return true;
}

// Update next button handlers to include validation
const nextButtons = document.querySelectorAll(
  'button.donate-submit:not(.prev):not(.donate-submit-final):not([type="submit"])'
);
nextButtons.forEach((btn) => {
  btn.addEventListener("click", function (e) {
    e.preventDefault();
    console.log("Next button clicked, currentDiv:", currentDiv);

    // Validate current section before proceeding
    if (!validateCurrentSection(currentDiv)) {
      return; // Stop if validation fails
    }

    if (currentDiv < nextsection.length - 1) {
      nextsection[currentDiv].style.display = "none";
      currentDiv++;
      nextsection[currentDiv].style.display = "flex";
    }
  });
});

// Handle submit button with validation
const submitButton = document.querySelector(
  '.donate-submit-final[type="submit"]'
);
if (submitButton) {
  console.log("Submit button found and ready");
  submitButton.addEventListener("click", function (e) {
    e.preventDefault(); // Prevent default form submission
    console.log("Submit button clicked - validating form");

    // Validate current (final) section
    if (!validateCurrentSection(currentDiv)) {
      return;
    }

    // Additional final validation
    const form = submitButton.closest("form");
    if (!form) {
      console.error("No form found for submit button!");
      return;
    }

    // All validation passed, submit the form
    console.log("All validation passed, submitting form...");

    // Show loading state
    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    // Submit the form
    form.submit();
  });
} else {
  console.error("Submit button not found!");
}
