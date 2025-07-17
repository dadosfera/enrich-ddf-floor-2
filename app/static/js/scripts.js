// Custom JavaScript for Enrich DDF Floor 2

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form handlers
    initializeFormHandlers();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize API status checker
    initializeApiStatusChecker();
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

function initializeFormHandlers() {
    // Handle search form submission
    const searchForm = document.getElementById('quick-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = document.getElementById('quickSearch');
            if (searchInput && searchInput.value.trim().length < 3) {
                e.preventDefault();
                showAlert('Please enter at least 3 characters to search.', 'warning');
            }
        });
    }
    
    // Handle API endpoint copy functionality
    const apiEndpoints = document.querySelectorAll('.api-endpoint');
    apiEndpoints.forEach(function(endpoint) {
        endpoint.addEventListener('click', function() {
            const code = this.querySelector('code');
            if (code) {
                navigator.clipboard.writeText(code.textContent).then(function() {
                    showAlert('API endpoint copied to clipboard!', 'success');
                }).catch(function() {
                    showAlert('Failed to copy to clipboard.', 'danger');
                });
            }
        });
    });
}

function initializeSearch() {
    // Add search suggestions if needed
    const searchInput = document.getElementById('quickSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Could add search suggestions here
            const query = this.value.trim();
            if (query.length >= 3) {
                // Show loading indicator
                showLoadingIndicator();
            }
        });
    }
}

function initializeApiStatusChecker() {
    // Check API status periodically
    checkApiStatus();
    setInterval(checkApiStatus, 30000); // Check every 30 seconds
}

function checkApiStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            updateApiStatusDisplay(data);
        })
        .catch(error => {
            console.error('Failed to check API status:', error);
            updateApiStatusDisplay({ status: 'error' });
        });
}

function updateApiStatusDisplay(data) {
    const statusElement = document.getElementById('api-status');
    if (statusElement) {
        if (data.status === 'running') {
            statusElement.innerHTML = '<span class="badge bg-success">Online</span>';
        } else {
            statusElement.innerHTML = '<span class="badge bg-danger">Offline</span>';
        }
    }
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function showLoadingIndicator() {
    // Show loading spinner
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'loading-spinner';
    loadingSpinner.id = 'search-loading';
    
    const searchButton = document.querySelector('#quick-search-form button[type="submit"]');
    if (searchButton) {
        searchButton.appendChild(loadingSpinner);
    }
}

function hideLoadingIndicator() {
    const loadingSpinner = document.getElementById('search-loading');
    if (loadingSpinner) {
        loadingSpinner.remove();
    }
}

// Utility functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

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

// Export functions for global use
window.EnrichDDF = {
    showAlert,
    showLoadingIndicator,
    hideLoadingIndicator,
    formatNumber,
    checkApiStatus
}; 