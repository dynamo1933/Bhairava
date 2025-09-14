// ===== DAIVA ANUGHARA - MAIN JAVASCRIPT =====
// Sacred Spiritual Practice Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initMobileMenu();
    initDropdowns();
    initSmoothScrolling();
    initAccessibility();
    initPWA();
    initFlashMessages();
    
    // Update announcement banner with next Ashtami date
    updateAnnouncementBanner();
});

// ===== PWA FUNCTIONALITY =====
function initPWA() {
    // Register service worker
    if ('serviceWorker' in navigator) {
        registerServiceWorker();
    }
    
    // Initialize PWA features
    initInstallPrompt();
    initOfflineDetection();
    initAppLikeBehavior();
    initTouchGestures();
}

function registerServiceWorker() {
    navigator.serviceWorker.register('/static/sw.js')
        .then((registration) => {
            console.log('Service Worker registered successfully:', registration);
            
            // Handle updates
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        showUpdateNotification();
                    }
                });
            });
        })
        .catch((error) => {
            console.log('Service Worker registration failed:', error);
        });
}

function initInstallPrompt() {
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        // Show install button
        showInstallButton();
    });
    
    // Handle install button click
    document.addEventListener('click', (e) => {
        if (e.target.matches('.install-app-btn')) {
            e.preventDefault();
            deferredPrompt.prompt();
            
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                } else {
                    console.log('User dismissed the install prompt');
                }
                deferredPrompt = null;
                hideInstallButton();
            });
        }
    });
}

function showInstallButton() {
    // Create install button if it doesn't exist
    if (!document.querySelector('.install-app-btn')) {
        const installBtn = document.createElement('button');
        installBtn.className = 'install-app-btn';
        installBtn.innerHTML = '<i class="fas fa-download"></i> Install App';
        installBtn.setAttribute('aria-label', 'Install Daiva Anughara as app');
        
        // Add to header
        const header = document.querySelector('.header-container');
        if (header) {
            header.appendChild(installBtn);
        }
    }
}

function hideInstallButton() {
    const installBtn = document.querySelector('.install-app-btn');
    if (installBtn) {
        installBtn.remove();
    }
}

function initOfflineDetection() {
    // Update UI based on online/offline status
    function updateOnlineStatus() {
        const isOnline = navigator.onLine;
        document.body.classList.toggle('offline', !isOnline);
        
        if (!isOnline) {
            showOfflineNotification();
        } else {
            hideOfflineNotification();
        }
    }
    
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    updateOnlineStatus(); // Initial check
}

function showOfflineNotification() {
    if (!document.querySelector('.offline-notification')) {
        const notification = document.createElement('div');
        notification.className = 'offline-notification';
        notification.innerHTML = `
            <i class="fas fa-wifi-slash"></i>
            <span>You're offline. Some features may be limited.</span>
        `;
        document.body.appendChild(notification);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
}

function hideOfflineNotification() {
    const notification = document.querySelector('.offline-notification');
    if (notification) {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }
}

function initAppLikeBehavior() {
    // Prevent zoom on double tap
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (event) => {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
    
    // Add pull-to-refresh functionality
    initPullToRefresh();
    
    // Add swipe navigation
    initSwipeNavigation();
    
    // Add haptic feedback
    initHapticFeedback();
}

function initPullToRefresh() {
    let startY = 0;
    let currentY = 0;
    let pullDistance = 0;
    let isPulling = false;
    
    document.addEventListener('touchstart', (e) => {
        if (window.scrollY === 0) {
            startY = e.touches[0].clientY;
            isPulling = true;
        }
    });
    
    document.addEventListener('touchmove', (e) => {
        if (!isPulling) return;
        
        currentY = e.touches[0].clientY;
        pullDistance = currentY - startY;
        
        if (pullDistance > 0 && pullDistance < 100) {
            showPullToRefreshIndicator(pullDistance);
        }
    });
    
    document.addEventListener('touchend', () => {
        if (isPulling && pullDistance > 80) {
            // Trigger refresh
            location.reload();
        }
        hidePullToRefreshIndicator();
        isPulling = false;
        pullDistance = 0;
    });
}

function showPullToRefreshIndicator(distance) {
    let indicator = document.querySelector('.pull-refresh-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'pull-refresh-indicator';
        indicator.innerHTML = '<i class="fas fa-arrow-down"></i> Pull to refresh';
        document.body.appendChild(indicator);
    }
    
    indicator.style.transform = `translateY(${Math.min(distance, 100)}px)`;
    indicator.style.opacity = Math.min(distance / 100, 1);
}

function hidePullToRefreshIndicator() {
    const indicator = document.querySelector('.pull-refresh-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function initSwipeNavigation() {
    let startX = 0;
    let startY = 0;
    let endX = 0;
    let endY = 0;
    
    document.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        endY = e.changedTouches[0].clientY;
        
        const diffX = startX - endX;
        const diffY = startY - endY;
        
        // Minimum swipe distance
        if (Math.abs(diffX) > 50 && Math.abs(diffY) < 100) {
            if (diffX > 0) {
                // Swipe left - go forward
                handleSwipeLeft();
            } else {
                // Swipe right - go back
                handleSwipeRight();
            }
        }
    });
}

function handleSwipeLeft() {
    // Navigate to next page or section
    const nextLink = document.querySelector('[data-next-page]');
    if (nextLink) {
        window.location.href = nextLink.href;
    }
}

function handleSwipeRight() {
    // Navigate to previous page or go back
    if (document.referrer && document.referrer.includes(window.location.origin)) {
        history.back();
    }
}

function initHapticFeedback() {
    if ('vibrate' in navigator) {
        // Add haptic feedback to interactive elements
        const interactiveElements = document.querySelectorAll('button, .btn, .nav-link, .mobile-nav-link');
        
        interactiveElements.forEach(element => {
            element.addEventListener('touchstart', () => {
                navigator.vibrate(10);
            });
        });
    }
}

function showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'update-notification';
    notification.innerHTML = `
        <div class="update-content">
            <i class="fas fa-sync-alt"></i>
            <span>New version available</span>
            <button class="update-btn" onclick="location.reload()">Update</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 10000);
}

// ===== MOBILE MENU FUNCTIONALITY =====
function initMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.nav-mobile');
    
    if (!mobileToggle || !mobileNav) return;
    
    mobileToggle.addEventListener('click', function() {
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        
        // Toggle mobile navigation
        if (isExpanded) {
            mobileNav.setAttribute('hidden', '');
            this.setAttribute('aria-expanded', 'false');
            this.classList.remove('is-active'); // Remove active class
        } else {
            mobileNav.removeAttribute('hidden');
            this.setAttribute('aria-expanded', 'true');
            this.classList.add('is-active'); // Add active class
        }
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!mobileToggle.contains(event.target) && !mobileNav.contains(event.target)) {
            mobileNav.setAttribute('hidden', '');
            mobileToggle.setAttribute('aria-expanded', 'false');
            mobileToggle.classList.remove('is-active'); // Remove active class
        }
    });
    
    // Initialize mobile navigation sections
    initMobileNavSections();
}

function initMobileNavSections() {
    const sections = document.querySelectorAll('.mobile-nav-section');
    
    sections.forEach(section => {
        const title = section.querySelector('.mobile-nav-section-title');
        const submenu = section.querySelector('.mobile-nav-submenu');
        
        if (title && submenu) {
            // Add click handler to section title
            title.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const isExpanded = submenu.style.display !== 'none';
                
                if (isExpanded) {
                    submenu.style.display = 'none';
                    title.setAttribute('aria-expanded', 'false');
                    title.classList.remove('expanded');
                } else {
                    submenu.style.display = 'block';
                    title.setAttribute('aria-expanded', 'true');
                    title.classList.add('expanded');
                }
            });
            
            // Initialize submenu state
            submenu.style.display = 'none';
            title.setAttribute('aria-expanded', 'false');
            title.setAttribute('role', 'button');
            title.setAttribute('tabindex', '0');
            
            // Add keyboard support
            title.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    title.click();
                }
            });
        }
    });
}



// ===== DROPDOWN MENU FUNCTIONALITY =====
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('.nav-link');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (!link || !menu) return;
        
        // Show dropdown on hover (desktop)
        dropdown.addEventListener('mouseenter', function() {
            if (window.innerWidth > 768) {
                showDropdown(menu);
            }
        });
        
        dropdown.addEventListener('mouseleave', function() {
            if (window.innerWidth > 768) {
                hideDropdown(menu);
            }
        });
        
        // Show dropdown on click (mobile)
        link.addEventListener('click', function(event) {
            if (window.innerWidth <= 768) {
                event.preventDefault();
                toggleDropdown(menu);
            }
        });
    });
}

function showDropdown(menu) {
    menu.style.opacity = '1';
    menu.style.visibility = 'visible';
    menu.style.transform = 'translateY(0)';
}

function hideDropdown(menu) {
    menu.style.opacity = '0';
    menu.style.visibility = 'hidden';
    menu.style.transform = 'translateY(-10px)';
}

function toggleDropdown(menu) {
    const isVisible = menu.style.visibility === 'visible';
    
    if (isVisible) {
        hideDropdown(menu);
    } else {
        showDropdown(menu);
    }
}

// ===== SMOOTH SCROLLING =====
function initSmoothScrolling() {
    // Smooth scroll for internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const href = this.getAttribute('href');
            
            if (href === '#') return;
            
            const targetElement = document.querySelector(href);
            if (targetElement) {
                event.preventDefault();
                
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== ACCESSIBILITY FEATURES =====
function initAccessibility() {
    // Skip link functionality
    const skipLinks = document.querySelectorAll('.skip-link');
    
    skipLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                event.preventDefault();
                targetElement.focus();
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Keyboard navigation for dropdowns
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            // Close mobile menu and dropdowns
            const mobileNav = document.querySelector('.nav-mobile');
            const mobileToggle = document.querySelector('.mobile-menu-toggle');
            
            if (mobileNav && !mobileNav.hasAttribute('hidden')) {
                mobileNav.setAttribute('hidden', '');
                mobileToggle.setAttribute('aria-expanded', 'false');
                animateHamburger(mobileToggle, false);
            }
            
            // Close search modal if open
            const searchModal = document.getElementById('search-modal');
            if (searchModal && !searchModal.hasAttribute('hidden')) {
                searchModal.setAttribute('hidden', '');
            }
        }
    });
    
    // Focus management for mobile menu
    const mobileNav = document.querySelector('.nav-mobile');
    if (mobileNav) {
        const mobileLinks = mobileNav.querySelectorAll('.mobile-nav-link');
        
        mobileLinks.forEach((link, index) => {
            link.addEventListener('keydown', function(event) {
                if (event.key === 'ArrowDown') {
                    event.preventDefault();
                    const nextLink = mobileLinks[index + 1] || mobileLinks[0];
                    nextLink.focus();
                } else if (event.key === 'ArrowUp') {
                    event.preventDefault();
                    const prevLink = mobileLinks[index - 1] || mobileLinks[mobileLinks.length - 1];
                    prevLink.focus();
                }
            });
        });
    }
}

// ===== ANNOUNCEMENT BANNER =====
function updateAnnouncementBanner() {
    const announcementDate = document.getElementById('next-ashtami-date');
    if (!announcementDate) return;
    
    // Set default text first
    announcementDate.textContent = 'Date to be announced';
    
    // Fetch next Ashtami date from API
    fetch('/api/next-ashtami')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && data.date) {
                const date = new Date(data.date);
                const formattedDate = date.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                
                announcementDate.textContent = `${formattedDate}, ${data.start_time} - ${data.end_time} ${data.timezone}`;
            }
        })
        .catch(error => {
            console.error('Error fetching Ashtami date:', error);
            // Don't show global error for API failures
        });
}

// ===== UTILITY FUNCTIONS =====
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== WINDOW RESIZE HANDLING =====
window.addEventListener('resize', debounce(function() {
    // Handle responsive behavior
    const mobileNav = document.querySelector('.nav-mobile');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    
    if (window.innerWidth > 768) {
        // Desktop view - ensure mobile menu is hidden
        if (mobileNav) {
            mobileNav.setAttribute('hidden', '');
        }
        if (mobileToggle) {
            mobileToggle.setAttribute('aria-expanded', 'false');
            animateHamburger(mobileToggle, false);
        }
    }
}, 250));

// ===== SCROLL EFFECTS =====
window.addEventListener('scroll', throttle(function() {
    // Add scroll effects if needed
    const header = document.querySelector('.header');
    if (header) {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
}, 100));

// ===== PERFORMANCE OPTIMIZATION =====
// Intersection Observer for lazy loading (if needed)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            }
        });
    });
    
    // Observe images with data-src attribute
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== ENHANCED ERROR HANDLING =====
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    
    // Only show error if:
    // 1. showGlobalError function is available
    // 2. DOM is ready
    // 3. It's a JavaScript runtime error (not resource loading)
    // 4. It's not a script loading error
    // 5. It's not a network error
    // 6. It's not a resource loading error
    // 7. It's not a fetch error
    // 8. It's not a CORS error
    // 9. It's not a service worker error
    // 10. It's not a promise rejection
    // 11. It's not a module loading error
    // 12. It's not a security error
    // 13. It's not a timeout error
    // 14. It's not a resource error
    // 15. It's not a DOM error
    // 16. It's not a media error
    // 17. It's not a validation error
    // 18. It's not a constraint error
    // 19. It's not a quota error
    // 20. It's not a data error
    // 21. It's not a transaction error
    // 22. It's not a version error
    if (typeof showGlobalError === 'function' && 
        document.readyState === 'complete' && 
        event.target === window &&
        event.error &&
        event.error.name !== 'ChunkLoadError' &&
        event.error.name !== 'TypeError' &&
        event.error.name !== 'NetworkError' &&
        event.error.name !== 'SyntaxError' &&
        event.error.name !== 'ReferenceError' &&
        event.error.name !== 'ServiceWorkerError' &&
        event.error.name !== 'PromiseRejectionError' &&
        event.error.name !== 'ModuleLoadError' &&
        event.error.name !== 'SecurityError' &&
        event.error.name !== 'TimeoutError' &&
        event.error.name !== 'ResourceError' &&
        event.error.name !== 'DOMError' &&
        event.error.name !== 'MediaError' &&
        event.error.name !== 'ValidationError' &&
        event.error.name !== 'ConstraintError' &&
        event.error.name !== 'QuotaExceededError' &&
        event.error.name !== 'DataError' &&
        event.error.name !== 'TransactionError' &&
        event.error.name !== 'VersionError' &&
        !event.filename.includes('sw.js') &&
        !event.message.includes('Loading chunk') &&
        !event.message.includes('Loading CSS chunk') &&
        !event.message.includes('Failed to load') &&
        !event.message.includes('net::ERR_') &&
        !event.message.includes('fetch') &&
        !event.message.includes('CORS') &&
        !event.message.includes('Cross-Origin') &&
        !event.message.includes('Service Worker') &&
        !event.message.includes('Promise') &&
        !event.message.includes('Module') &&
        !event.message.includes('Security') &&
        !event.message.includes('timeout') &&
        !event.message.includes('Resource') &&
        !event.message.includes('DOM') &&
        !event.message.includes('Media') &&
        !event.message.includes('Validation') &&
        !event.message.includes('Constraint') &&
        !event.message.includes('Quota') &&
        !event.message.includes('Data') &&
        !event.message.includes('Transaction') &&
        !event.message.includes('Version')) {
        showGlobalError('An unexpected error occurred. Please refresh the page and try again.');
    }
});

// Global error handler for fetch requests
function handleFetchError(error, context = 'operation') {
    console.error(`Error during ${context}:`, error);
    
    let message = 'An error occurred. Please try again.';
    
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
        message = 'Network error. Please check your connection and try again.';
    } else if (error.name === 'SyntaxError') {
        message = 'Invalid response from server. Please try again.';
    }
    
    showGlobalError(message);
}

// Global error display function
function showGlobalError(message, type = 'error') {
    // Only show errors if DOM is ready and we're not already showing an error
    if (document.readyState === 'loading' || document.querySelector('.global-error-message')) {
        return;
    }
    
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.global-error-message');
    existingErrors.forEach(error => error.remove());
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'global-error-message';
    errorDiv.innerHTML = `
        <div class="error-content">
            <div class="error-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="error-text">
                <strong>Error:</strong> ${message}
            </div>
            <button class="error-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Insert at the top of the page
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(errorDiv, mainContent.firstChild);
    } else if (document.body) {
        document.body.insertBefore(errorDiv, document.body.firstChild);
    }
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 10000);
}

// Enhanced fetch wrapper with error handling
function safeFetch(url, options = {}) {
    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response;
        })
        .catch(error => {
            handleFetchError(error, 'network request');
            throw error;
        });
}

// ===== SERVICE WORKER REGISTRATION (if needed) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment if you want to add a service worker
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// ===== FLASH MESSAGE FUNCTIONALITY =====
function closeFlashMessage(button) {
    const message = button.closest('.flash-message');
    if (message) {
        message.classList.add('removing');
        setTimeout(() => {
            message.remove();
            
            // Remove flash messages container if empty
            const container = document.getElementById('flashMessages');
            if (container && container.children.length === 0) {
                container.remove();
            }
        }, 300);
    }
}

// Auto-hide flash messages after 5 seconds
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        const category = message.dataset.category;
        let timeout = 5000; // Default 5 seconds
        
        // Different timeouts for different message types
        if (category === 'error') {
            timeout = 8000; // Errors stay longer
        } else if (category === 'success') {
            timeout = 4000; // Success messages shorter
        }
        
        setTimeout(() => {
            if (message.parentElement) {
                closeFlashMessage(message.querySelector('.message-close'));
            }
        }, timeout);
    });
}

// ===== EXPORT FUNCTIONS FOR OTHER MODULES =====
window.DaivaAnughara = window.DaivaAnughara || {};
window.DaivaAnughara.main = {
    updateAnnouncementBanner,
    initMobileMenu,
    initDropdowns,
    initSmoothScrolling,
    initAccessibility,
    closeFlashMessage
};

// Make closeFlashMessage globally available
window.closeFlashMessage = closeFlashMessage;

// Mobile menu close function
function closeMobileMenu() {
    const mobileNav = document.querySelector('.nav-mobile');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    
    if (mobileNav && mobileToggle) {
        mobileNav.setAttribute('hidden', '');
        mobileToggle.setAttribute('aria-expanded', 'false');
        mobileToggle.classList.remove('is-active');
    }
}

// Make closeMobileMenu globally available
window.closeMobileMenu = closeMobileMenu;

// Function to clear all error messages
function clearAllErrors() {
    const errorMessages = document.querySelectorAll('.global-error-message');
    errorMessages.forEach(error => error.remove());
}

// Make clearAllErrors globally available
window.clearAllErrors = clearAllErrors;
