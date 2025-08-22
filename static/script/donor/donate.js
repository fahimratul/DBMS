        let selectedAmount = null;
        let donationType = 'money';

        function navigateTo(page) {
            window.location.href = page;
        }

        function logout() {
            if (confirm('Are you sure you want to log out?')) {
                alert('You have been logged out successfully!');
                window.location.href = 'login.html';
            }
        }

        function selectDonationType(type) {
            donationType = type;
            
            // Update button states
            document.getElementById('moneyBtn').classList.toggle('active', type === 'money');
            document.getElementById('itemsBtn').classList.toggle('active', type === 'items');
            
            // Update form
            document.getElementById('moneyFields').style.display = type === 'money' ? 'block' : 'none';
            document.getElementById('itemFields').style.display = type === 'items' ? 'block' : 'none';
            
            // Update form title and icon
            const title = type === 'money' ? 'Monetary Donation Form' : 'Item Donation Form';
            const icon = type === 'money' ? 'dollar-sign' : 'package';
            
            document.getElementById('formTitle').innerHTML = `<i data-lucide="${icon}" class="mr-3"></i>${title}`;
            
            lucide.createIcons();
        }

        // Amount button handling
        document.addEventListener('DOMContentLoaded', function() {
            const amountButtons = document.querySelectorAll('.amount-btn');
            const customAmount = document.getElementById('customAmount');
            
            amountButtons.forEach(btn => {
                btn.addEventListener('click', function() {
                    selectedAmount = parseInt(this.dataset.amount);
                    amountButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    customAmount.value = '';
                });
            });
            
            customAmount.addEventListener('input', function() {
                if (this.value) {
                    selectedAmount = parseInt(this.value);
                    amountButtons.forEach(b => b.classList.remove('active'));
                }
            });
            
            // Form submission
            document.getElementById('donationForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                if (donationType === 'money' && !selectedAmount) {
                    alert('Please select or enter a donation amount.');
                    return;
                }
                
                // Simulate submission
                alert('Thank you for your donation! Your contribution will make a real difference.');
                this.reset();
                selectedAmount = null;
                amountButtons.forEach(b => b.classList.remove('active'));
            });
            
            lucide.createIcons();
        });
    