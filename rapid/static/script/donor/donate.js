        // Handles donation form logic for donor/donate.html
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            let currentDonationType = 'money';

            // Donation Type Toggle
            window.selectDonationType = function(type) {
                const moneyFields = document.getElementById('moneyFields');
                const itemFields = document.getElementById('itemFields');
                const moneyBtn = document.getElementById('moneyBtn');
                const itemsBtn = document.getElementById('itemsBtn');
                const formTitle = document.getElementById('formTitle');
                const donationTypeField = document.getElementById('donationType');

                currentDonationType = type;
                donationTypeField.value = type;

                if(type === 'money') {
                    moneyFields.style.display = 'block';
                    itemFields.style.display = 'none';
                    moneyBtn.classList.add('active');
                    itemsBtn.classList.remove('active');
                    formTitle.innerHTML = '<i data-lucide="coins" id="formIcon" class="mr-3"></i> Monetary Donation Form';
                    document.querySelector('input[name="amount"]').setAttribute('required', 'required');
                    document.querySelector('select[name="payment_method"]').setAttribute('required', 'required');
                    document.querySelectorAll('select[name="items"]').forEach(select => {
                        select.removeAttribute('required');
                    });
                    document.querySelectorAll('input[name="quantity"]').forEach(input => {
                        input.removeAttribute('required');
                    });
                } else {
                    moneyFields.style.display = 'none';
                    itemFields.style.display = 'block';
                    moneyBtn.classList.remove('active');
                    itemsBtn.classList.add('active');
                    formTitle.innerHTML = '<i data-lucide="package" id="formIcon" class="mr-3"></i> Item Donation Form';
                    document.querySelector('input[name="amount"]').removeAttribute('required');
                    document.querySelector('select[name="payment_method"]').removeAttribute('required');
                }
                lucide.createIcons();
            };

            // Add item row functionality
            function addItemRow() {
                const itemRows = document.getElementById('itemRows');
                const firstRow = itemRows.querySelector('.item-row');
                const newRow = firstRow.cloneNode(true);
                newRow.querySelector('.item-name').selectedIndex = 0;
                newRow.querySelector('.item-qty').value = 1;
                newRow.querySelector('.remove-item-btn').style.display = 'inline-block';
                newRow.querySelector('.remove-item-btn').addEventListener('click', function() {
                    newRow.remove();
                    updateAvailableItems();
                });
                newRow.querySelector('.item-name').addEventListener('change', updateAvailableItems);
                itemRows.appendChild(newRow);
                updateAvailableItems();
            }

            // Update available items in dropdowns based on selections
            function updateAvailableItems() {
                const itemSelects = document.querySelectorAll('select[name="items"]');
                const selectedValues = [];
                itemSelects.forEach(select => {
                    if (select.value && select.value !== '') {
                        selectedValues.push(select.value);
                    }
                });
                itemSelects.forEach(select => {
                    const currentValue = select.value;
                    const options = select.querySelectorAll('option');
                    options.forEach(option => {
                        if (option.value === '' || option.value === currentValue) {
                            option.style.display = 'block';
                            option.disabled = false;
                        } else if (selectedValues.includes(option.value)) {
                            option.style.display = 'none';
                            option.disabled = true;
                        } else {
                            option.style.display = 'block';
                            option.disabled = false;
                        }
                    });
                });
            }

            // Form validation and submission
            function validateForm() {
                document.querySelectorAll('.error-message').forEach(error => {
                    error.style.display = 'none';
                });
                if (currentDonationType === 'money') {
                    const amount = document.getElementById('customAmount').value;
                    const paymentMethod = document.querySelector('select[name="payment_method"]').value;
                    if (!amount || parseFloat(amount) <= 0) {
                        document.getElementById('amountError').style.display = 'block';
                        document.getElementById('customAmount').focus();
                        return false;
                    }
                    if (!paymentMethod) {
                        document.getElementById('paymentError').style.display = 'block';
                        document.querySelector('select[name="payment_method"]').focus();
                        return false;
                    }
                } else if (currentDonationType === 'items') {
                    const itemSelects = document.querySelectorAll('select[name="items"]');
                    let hasValidItems = false;
                    itemSelects.forEach(select => {
                        if (select.value && select.value.trim() !== '') {
                            hasValidItems = true;
                        }
                    });
                    if (!hasValidItems) {
                        document.getElementById('itemError').style.display = 'block';
                        document.querySelector('select[name="items"]').focus();
                        return false;
                    }
                    document.getElementById('customAmount').value = '';
                }
                return true;
            }

            // Amount buttons
            document.querySelectorAll('.amount-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    document.getElementById('customAmount').value = btn.dataset.amount;
                    document.getElementById('amountError').style.display = 'none';
                });
            });

            // Custom amount input
            document.getElementById('customAmount').addEventListener('input', (e) => {
                document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
                document.getElementById('amountError').style.display = 'none';
            });

            // Payment method change
            document.getElementById('paymentMethod').addEventListener('change', () => {
                document.getElementById('paymentError').style.display = 'none';
            });

            // Item select change - Add listener to first row
            document.querySelector('.item-name').addEventListener('change', () => {
                updateAvailableItems();
                document.getElementById('itemError').style.display = 'none';
            });

            // Initial remove button for first row (hidden by default)
            document.querySelector('.remove-item-btn').style.display = 'none';

            // Add item button
            document.getElementById('addItemBtn').addEventListener('click', addItemRow);

            // Form submission
            document.getElementById('donationForm').addEventListener('submit', (e) => {
                document.querySelectorAll('.error-message').forEach(error => {
                    error.style.display = 'none';
                });
                if (!validateForm()) {
                    e.preventDefault();
                    return false;
                }
                return true;
            });
        });
    