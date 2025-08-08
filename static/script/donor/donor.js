// Initialize Lucide icons
lucide.createIcons();

// Handle logout functionality
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        console.log("User logged out");
        alert("You have been logged out successfully!");
        // In a real application, you would redirect to login page
        // window.location.href = '/login.html';
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Add styles
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
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;

    // Add animation styles if not already present
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

    // Add to DOM
    document.body.appendChild(notification);

    // Remove after 3 seconds
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

// Stats animation on page load
function animateStats() {
    const statCards = document.querySelectorAll('.total-amount-card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.transform = 'translateY(0)';
            card.style.opacity = '1';
        }, index * 100);
    });
}

// Mobile sidebar toggle
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContainer = document.querySelector('.main-container');
    if (window.innerWidth <= 768) {
        sidebar.style.transform = sidebar.style.transform === 'translateX(0px)' ? 'translateX(-100%)' : 'translateX(0px)';
    }
}

// Combine all DOMContentLoaded logic into one
document.addEventListener('DOMContentLoaded', function() {
    // Animate stats cards on load
    animateStats();

    // Search functionality
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const searchTerm = this.value.trim();
                if (searchTerm) {
                    console.log('Searching for:', searchTerm);
                    showNotification(`Searching for: ${searchTerm}`, 'info');
                }
            }
        });

        // Focus search input on Ctrl+K or Cmd+K
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Add click handlers for stat cards
    const statCards = document.querySelectorAll('.total-amount-card');
    statCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            const cardTypes = ['donations', 'count', 'organizations', 'membership'];
            showNotification(`Viewing ${cardTypes[index]} details`, 'info');
        });
    });

    // Add click handlers for navigation items
    const navLinks = document.querySelectorAll('.sidebar-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                // Let the normal navigation happen
                return;
            }
            e.preventDefault();
            const linkText = this.querySelector('.sidebar-label').textContent;
            if (linkText !== 'Dashboard') {
                showNotification(`Navigating to ${linkText}`, 'info');
            }
        });
    });

    // Add bell notification click handler
    const bellButton = document.querySelector('button > [data-lucide="bell"]');
    if (bellButton && bellButton.parentElement) {
        bellButton.parentElement.addEventListener('click', function() {
            showNotification('You have 3 new notifications', 'info');
        });
    }
});

// Handle responsive behavior
window.addEventListener('resize', function() {
    const sidebar = document.querySelector('.sidebar');
    const mainContainer = document.querySelector('.main-container');
    if (window.innerWidth > 768) {
        sidebar.style.transform = 'translateX(0)';
        mainContainer.style.marginLeft = '15.625rem';
    } else {
        sidebar.style.transform = 'translateX(-100%)'; // Ensure sidebar is hidden on mobile
        mainContainer.style.marginLeft = '0';
    }
});

// Initialize responsive behavior on load
window.addEventListener('load', function() {
    const sidebar = document.querySelector('.sidebar');
    const mainContainer = document.querySelector('.main-container');
    if (window.innerWidth <= 768) {
        sidebar.style.transform = 'translateX(-100%)';
        mainContainer.style.marginLeft = '0';
    } else {
        sidebar.style.transform = 'translateX(0)';
        mainContainer.style.marginLeft = '15.625rem';
    }
});

console.log('Dashboard loaded successfully');