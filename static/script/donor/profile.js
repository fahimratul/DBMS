
        // Initialize Lucide icons
        lucide.createIcons();

        let isEditing = false;
        let originalData = {};

        function navigateTo(page) {
            window.location.href = page;
        }

        function logout() {
            if (confirm('Are you sure you want to log out?')) {
                alert('You have been logged out successfully!');
                window.location.href = 'login.html';
            }
        }

        function toggleEdit() {
            isEditing = true;
            
            // Store original data
            originalData = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                accountName: document.getElementById('accountName').value,
                address: document.getElementById('address').value
            };

            // Enable form fields
            document.getElementById('name').disabled = false;
            document.getElementById('phone').disabled = false;
            document.getElementById('email').disabled = false;
            document.getElementById('accountName').disabled = false;
            document.getElementById('address').disabled = false;

            // Toggle buttons
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('saveBtn').classList.remove('hidden');
            document.getElementById('cancelBtn').classList.remove('hidden');

            // Re-initialize icons
            lucide.createIcons();
        }

        function saveProfile() {
            // Validate form data
            const name = document.getElementById('name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const email = document.getElementById('email').value.trim();
            const accountName = document.getElementById('accountName').value.trim();
            const address = document.getElementById('address').value.trim();

            if (!name || !phone || !email || !accountName || !address) {
                alert('Please fill in all required fields.');
                return;
            }

            if (!isValidEmail(email)) {
                alert('Please enter a valid email address.');
                return;
            }

            // Simulate saving data
            setTimeout(() => {
                alert('Profile updated successfully!');
                
                // Update display name
                document.getElementById('displayName').textContent = name;
                
                // Disable form fields
                disableFormFields();
                
                // Toggle buttons
                toggleButtons();
                
                isEditing = false;
            }, 500);
        }

        function cancelEdit() {
            // Restore original data
            document.getElementById('name').value = originalData.name;
            document.getElementById('phone').value = originalData.phone;
            document.getElementById('email').value = originalData.email;
            document.getElementById('accountName').value = originalData.accountName;
            document.getElementById('address').value = originalData.address;

            // Disable form fields
            disableFormFields();
            
            // Toggle buttons
            toggleButtons();
            
            isEditing = false;
        }

        function disableFormFields() {
            document.getElementById('name').disabled = true;
            document.getElementById('phone').disabled = true;
            document.getElementById('email').disabled = true;
            document.getElementById('accountName').disabled = true;
            document.getElementById('address').disabled = true;
        }

        function toggleButtons() {
            document.getElementById('editBtn').classList.remove('hidden');
            document.getElementById('saveBtn').classList.add('hidden');
            document.getElementById('cancelBtn').classList.add('hidden');
            
            // Re-initialize icons
            lucide.createIcons();
        }

        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        // Prevent navigation away if editing
        window.addEventListener('beforeunload', function(e) {
            if (isEditing) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
    