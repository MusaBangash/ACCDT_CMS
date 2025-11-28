/**
 * Common JavaScript utilities for School Management System
 */

// Confirm delete action
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Format date to readable string
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Format currency
function formatCurrency(amount) {
    return 'Rs. ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = alertHtml;
    document.body.appendChild(tempDiv.firstElementChild);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert[role="alert"]');
        alerts.forEach(alert => {
            if (alert.textContent.includes(message)) {
                alert.remove();
            }
        });
    }, 5000);
}

// API Helper - GET request with error handling
async function apiGet(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API GET error:', error);
        showToast('Failed to fetch data. Please try again.', 'error');
        throw error;
    }
}

// API Helper - POST request with CSRF token
async function apiPost(url, data = {}) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API POST error:', error);
        showToast('Failed to process request. Please try again.', 'error');
        throw error;
    }
}

// Get CSRF token from meta tag or cookie
function getCSRFToken() {
    // Try to get from meta tag first
    const token = document.querySelector('meta[name="csrf-token"]');
    if (token) {
        return token.getAttribute('content');
    }

    // Fall back to cookie if available
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrf_token') {
            return decodeURIComponent(value);
        }
    }

    return '';
}

// Enable/disable form elements
function setFormDisabled(formId, disabled = true) {
    const form = document.getElementById(formId);
    if (!form) return;

    const elements = form.querySelectorAll('input, select, textarea, button');
    elements.forEach(element => {
        element.disabled = disabled;
    });
}

// Clear form
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate phone number (basic)
function isValidPhone(phone) {
    const re = /^[\d\-\+\(\)\s]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

// Debounce function
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

// Truncate text
function truncateText(text, maxLength = 50) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'error');
    });
}

// Ready helper for when DOM is loaded
function ready(callback) {
    if (document.readyState !== 'loading') {
        callback();
    } else {
        document.addEventListener('DOMContentLoaded', callback);
    }
}

// Log for debugging
function debugLog(message, data = null) {
    if (data) {
        console.log(`[DEBUG] ${message}:`, data);
    } else {
        console.log(`[DEBUG] ${message}`);
    }
}
