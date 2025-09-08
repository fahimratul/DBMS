// Initialize Lucide icons
lucide.createIcons();

// DOM elements
const searchInput = document.getElementById('searchInput');
const downloadAllBtn = document.querySelector('.download-all-btn');
const loadMoreBtn = document.querySelector('.load-more-btn');
const donationsList = document.querySelector('.donations-list');
const donationModal = document.getElementById('donationModal');

// Event listeners
if (downloadAllBtn) {
    downloadAllBtn.addEventListener('click', downloadAllReceipts);
}

if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', loadMoreDonations);
}

// Search functionality - works with the existing HTML
if (searchInput) {
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const donationItems = document.querySelectorAll('.donation-item');
        
        donationItems.forEach(item => {
            const title = item.querySelector('h4').textContent.toLowerCase();
            const date = item.querySelector('.donation-date').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || date.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Handle action button clicks
document.addEventListener('click', function(e) {
    if (e.target.closest('.action-btn')) {
        handleActionClick(e);
    }
});

function handleActionClick(e) {
    const actionBtn = e.target.closest('.action-btn');
    const donationItem = actionBtn.closest('.donation-item');
    const donationId = donationItem.getAttribute('data-donation-id');
    
    const isViewBtn = actionBtn.querySelector('[data-lucide="eye"]');
    const isDownloadBtn = actionBtn.querySelector('[data-lucide="download"]');
    
    if (isViewBtn) {
        viewDonationDetails(donationId);
    } else if (isDownloadBtn) {
        downloadReceipt(donationId);
    }
}

function viewDonationDetails(donationId) {
    const donationElement = document.querySelector(`[data-donation-id="${donationId}"]`);
    if (!donationElement) return;
    
    const title = donationElement.querySelector('h4').textContent;
    const date = donationElement.querySelector('.donation-date').textContent;
    const amount = donationElement.querySelector('.amount').textContent;
    const itemsElement = donationElement.querySelector('.donation-items');
    const paymentMethodElement = donationElement.querySelector('.payment-method');
    
    let modalContent = `
        <div style="margin-bottom: 1rem;">
            <strong>Donation:</strong> ${title}
        </div>
        <div style="margin-bottom: 1rem;">
            <strong>Date:</strong> ${date.replace(/📅|calendar/gi, '').trim()}
        </div>
        <div style="margin-bottom: 1rem;">
            <strong>Amount:</strong> ${amount}
        </div>
    `;
    
    if (itemsElement) {
        const itemsText = itemsElement.textContent.replace(/📦|package|Items:/gi, '').trim();
        modalContent += `
            <div style="margin-bottom: 1rem;">
                <strong>Items:</strong> ${itemsText}
            </div>
        `;
    }
    
    if (paymentMethodElement) {
        const methodText = paymentMethodElement.textContent.replace(/💳|credit-card|Via:/gi, '').trim();
        modalContent += `
            <div style="margin-bottom: 1rem;">
                <strong>Payment Method:</strong> ${methodText}
            </div>
        `;
    }
    
    modalContent += `
        <div style="margin-bottom: 1rem;">
            <strong>Status:</strong> <span style="color: #10b981;">Completed</span>
        </div>
        <div style="margin-bottom: 1rem;">
            <strong>Donation ID:</strong> ${donationId}
        </div>
    `;
    
    document.getElementById('modalBody').innerHTML = modalContent;
    donationModal.classList.remove('hidden');
}

function closeDonationModal() {
    if (donationModal) {
        donationModal.classList.add('hidden');
    }
}

function downloadReceipt(donationId) {
    showNotification(`Downloading receipt for donation #${donationId}...`, 'info');
    
    // Redirect to the actual download route
    setTimeout(() => {
        window.location.href = `/donor/download_receipt/${donationId}`;
    }, 1000);
}

function downloadAllReceipts() {
    showNotification('Preparing all receipts for download...', 'info');
    
    // In a real implementation, you would make an AJAX call to your backend
    setTimeout(() => {
        showNotification('Feature coming soon! Individual receipts are available.', 'info');
    }, 2000);
}

function loadMoreDonations() {
    const currentUrl = new URL(window.location);
    const page = parseInt(currentUrl.searchParams.get('page') || '1');
    
    showNotification('Loading more donations...', 'info');
    
    // Add page parameter and reload
    currentUrl.searchParams.set('page', page + 1);
    
    // For now, just show a message since pagination isn't fully implemented
    setTimeout(() => {
        showNotification('Pagination feature coming soon!', 'info');
        if (loadMoreBtn) {
            loadMoreBtn.disabled = true;
            loadMoreBtn.textContent = 'No more donations';
            loadMoreBtn.style.opacity = '0.6';
        }
    }, 1000);
}

function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
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
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    `;
    
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function getNotificationColor(type) {
    switch (type) {
        case 'success': return '#10b981';
        case 'error': return '#ef4444';
        case 'warning': return '#f59e0b';
        default: return '#3b82f6';
    }
}

// Close modal when clicking outside or on close button
if (donationModal) {
    donationModal.addEventListener('click', function(e) {
        if (e.target === this) {
            closeDonationModal();
        }
    });
    
    const closeBtn = donationModal.querySelector('.modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeDonationModal);
    }
}

// Handle escape key to close modal
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && donationModal && !donationModal.classList.contains('hidden')) {
        closeDonationModal();
    }
});

// Handle logout functionality
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        window.location.href = '/auth/logout';
    }
}

// Add logout handler to logout links
document.addEventListener('click', function(e) {
    const logoutLink = e.target.closest('a[href*="logout"]');
    if (logoutLink) {
        e.preventDefault();
        handleLogout();
    }
});

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    console.log('History page loaded');
    
    // Add any initialization code here
    const donationItems = document.querySelectorAll('.donation-item');
    console.log(`Found ${donationItems.length} donation items`);
    
    // Check if there are no donations and hide load more button
    if (donationItems.length === 0) {
        if (loadMoreBtn) {
            loadMoreBtn.style.display = 'none';
        }
    }
    
    // If there are fewer than 10 donations, hide the load more button
    if (donationItems.length < 10 && loadMoreBtn) {
        loadMoreBtn.style.display = 'none';
    }
});