// Initialize Lucide icons
lucide.createIcons();

// Sample donations data
const donationsData = [
    {
        id: "1",
        date: "2024-01-15",
        amount: 250,
        cause: "Hurricane Relief Fund",
        status: "completed",
        receiptId: "RC-2024-001"
    },
    {
        id: "2",
        date: "2024-01-01",
        amount: 100,
        cause: "Food Bank Support",
        status: "completed",
        receiptId: "RC-2024-002"
    },
    {
        id: "3",
        date: "2023-12-25",
        amount: 500,
        cause: "Holiday Toy Drive",
        status: "completed",
        receiptId: "RC-2023-125"
    },
    {
        id: "4",
        date: "2023-12-15",
        amount: 75,
        cause: "Winter Clothing Drive",
        status: "completed",
        receiptId: "RC-2023-115"
    },
    {
        id: "5",
        date: "2023-11-30",
        amount: 200,
        cause: "Education Support Fund",
        status: "completed",
        receiptId: "RC-2023-098"
    }
];

// Handle logout functionality
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        console.log("User logged out");
        alert("You have been logged out successfully!");
    }
}

// DOM elements
const downloadAllBtn = document.querySelector('.download-all-btn');
const loadMoreBtn = document.querySelector('.load-more-btn');
const donationsList = document.querySelector('.donations-list');

// Event listeners
downloadAllBtn.addEventListener('click', downloadAllReceipts);
loadMoreBtn.addEventListener('click', loadMoreDonations);

// Add event listeners to all action buttons
document.addEventListener('click', function(e) {
    if (e.target.closest('.action-btn')) {
        handleActionClick(e);
    }
});

function handleActionClick(e) {
    const actionBtn = e.target.closest('.action-btn');
    const donationItem = actionBtn.closest('.donation-item');
    const donationId = getDonationIdFromItem(donationItem);
    
    const isViewBtn = actionBtn.querySelector('[data-lucide="eye"]');
    const isDownloadBtn = actionBtn.querySelector('[data-lucide="download"]');
    
    if (isViewBtn) {
        viewDonationDetails(donationId);
    } else if (isDownloadBtn) {
        downloadReceipt(donationId);
    }
}

function getDonationIdFromItem(donationItem) {
    const items = Array.from(donationsList.querySelectorAll('.donation-item'));
    const index = items.indexOf(donationItem);
    return donationsData[index]?.id || '1';
}

function viewDonationDetails(donationId) {
    const donation = donationsData.find(d => d.id === donationId);
    if (donation) {
        showModal('Donation Details', `
            <div class="modal-content">
                <h3>${donation.cause}</h3>
                <p><strong>Amount:</strong> ${donation.amount}</p>
                <p><strong>Date:</strong> ${formatDate(donation.date)}</p>
                <p><strong>Receipt ID:</strong> ${donation.receiptId}</p>
                <p><strong>Status:</strong> ${donation.status}</p>
            </div>
        `);
    }
}

function downloadReceipt(donationId) {
    const donation = donationsData.find(d => d.id === donationId);
    if (donation) {
        showNotification(`Downloading receipt for ${donation.cause}...`, 'info');
        
        setTimeout(() => {
            showNotification(`Receipt ${donation.receiptId} downloaded successfully!`, 'success');
        }, 1500);
    }
}

function downloadAllReceipts() {
    showNotification('Preparing all receipts for download...', 'info');
    
    setTimeout(() => {
        showNotification('All receipts downloaded successfully!', 'success');
    }, 2000);
}

function loadMoreDonations() {
    showNotification('Loading more donations...', 'info');
    
    setTimeout(() => {
        showNotification('No more donations to load.', 'info');
        loadMoreBtn.disabled = true;
        loadMoreBtn.textContent = 'All donations loaded';
        loadMoreBtn.style.opacity = '0.6';
    }, 1000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
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

function showModal(title, content) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.2s ease-out;
    `;
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.cssText = `
        background: white;
        border-radius: 1rem;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        max-height: 80%;
        overflow-y: auto;
        animation: scaleIn 0.2s ease-out;
    `;
    
    modal.innerHTML = `
        <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h2 style="font-size: 1.5rem; font-weight: 600;">${title}</h2>
            <button class="modal-close" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #6b7280;">×</button>
        </div>
        <div class="modal-body">
            ${content}
        </div>
    `;
    
    if (!document.querySelector('#modal-styles')) {
        const style = document.createElement('style');
        style.id = 'modal-styles';
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes scaleIn {
                from { transform: scale(0.9); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            .modal-content h3 {
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 1rem;
                color: #111827;
            }
            .modal-content p {
                margin-bottom: 0.5rem;
                font-size: 1rem;
                color: #374151;
            }
        `;
        document.head.appendChild(style);
    }
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            closeModal();
        }
    });
    
    function closeModal() {
        overlay.style.animation = 'fadeIn 0.2s ease-in reverse';
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        }, 200);
    }
    
    document.addEventListener('keydown', function handleEscape(e) {
        if (e.key === 'Escape') {
            closeModal();
            document.removeEventListener('keydown', handleEscape);
        }
    });
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    console.log('History page loaded');
    
    // Calculate and update summary stats
    const totalAmount = donationsData.reduce((sum, donation) => sum + donation.amount, 0);
    const summaryCards = document.querySelectorAll('.summary-card h3');
    if (summaryCards[0]) {
        summaryCards[0].textContent = `${totalAmount.toLocaleString()}`;
    }
});