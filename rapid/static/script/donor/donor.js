// Initialize Lucide icons
lucide.createIcons();

// Handle logout functionality
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        console.log("User logged out");
        alert("You have been logged out successfully!");
        window.location.href = '/auth/logout'; // ✅ redirect to backend logout route
    }
}

// Notification system
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
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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

// Stats animation
function animateStats() {
    const statCards = document.querySelectorAll('.total-amount-card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.transform = 'translateY(0)';
            card.style.opacity = '1';
        }, index * 100);
    });
}

// Sidebar toggle
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (window.innerWidth <= 768) {
        sidebar.style.transform = sidebar.style.transform === 'translateX(0px)' ? 'translateX(-100%)' : 'translateX(0px)';
    }
}

// Combine DOM logic
document.addEventListener('DOMContentLoaded', function() {

    // Donate Now button handler (robust navigation)
    document.querySelectorAll('.donate-now-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/donor/donor_donate';
        });
    });
    animateStats();

    // Search
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

        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Stat card click
    const statCards = document.querySelectorAll('.total-amount-card');
    statCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            const cardTypes = ['donations', 'count', 'organizations', 'membership'];
            showNotification(`Viewing ${cardTypes[index]} details`, 'info');
        });
    });

    // Sidebar nav links
    const navLinks = document.querySelectorAll('.sidebar-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                return;
            }
            e.preventDefault();
            const linkText = this.querySelector('.sidebar-label').textContent;
            if (linkText !== 'Dashboard') {
                showNotification(`Navigating to ${linkText}`, 'info');
            }
        });
    });

    // Bell notification
    const bellButton = document.querySelector('button > [data-lucide="bell"]');
    if (bellButton && bellButton.parentElement) {
        bellButton.parentElement.addEventListener('click', function() {
            showNotification('You have 3 new notifications', 'info');
        });
    }


});

// Responsive behavior
window.addEventListener('resize', function() {
    const sidebar = document.querySelector('.sidebar');
    const mainContainer = document.querySelector('.main-container');
    if (window.innerWidth > 768) {
        sidebar.style.transform = 'translateX(0)';
        mainContainer.style.marginLeft = '15.625rem';
    } else {
        sidebar.style.transform = 'translateX(-100%)';
        mainContainer.style.marginLeft = '0';
    }
});

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

console.log('Donor Dashboard loaded successfully');
