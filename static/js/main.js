// ===== DAIVA ANUGHARA - MAIN JAVASCRIPT =====
// Sacred Spiritual Practice Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initMobileMenu();
    initDropdowns();
    initSmoothScrolling();
    initAccessibility();
    
    // Update announcement banner with next Ashtami date
    updateAnnouncementBanner();
});

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
        } else {
            mobileNav.removeAttribute('hidden');
            this.setAttribute('aria-expanded', 'true');
        }
        
        // Animate hamburger lines
        animateHamburger(this, !isExpanded);
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!mobileToggle.contains(event.target) && !mobileNav.contains(event.target)) {
            mobileNav.setAttribute('hidden', '');
            mobileToggle.setAttribute('aria-expanded', 'false');
            animateHamburger(mobileToggle, false);
        }
    });
}

function animateHamburger(toggle, isOpen) {
    const lines = toggle.querySelectorAll('.hamburger-line');
    
    if (isOpen) {
        // Transform to X
        lines[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        lines[1].style.opacity = '0';
        lines[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
    } else {
        // Reset to hamburger
        lines[0].style.transform = 'none';
        lines[1].style.opacity = '1';
        lines[2].style.transform = 'none';
    }
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
    
    // Fetch next Ashtami date from API
    fetch('/api/next-ashtami')
        .then(response => response.json())
        .then(data => {
            if (data && data.date) {
                const date = new Date(data.date);
                const formattedDate = date.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                
                announcementDate.textContent = `${formattedDate}, ${data.start_time} - ${data.end_time} ${data.timezone}`;
            } else {
                announcementDate.textContent = 'Date to be announced';
            }
        })
        .catch(error => {
            console.error('Error fetching Ashtami date:', error);
            announcementDate.textContent = 'Date to be announced';
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

// ===== ERROR HANDLING =====
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    // You can add error reporting here
});

// ===== SERVICE WORKER REGISTRATION (if needed) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment if you want to add a service worker
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// ===== EXPORT FUNCTIONS FOR OTHER MODULES =====
window.DaivaAnughara = window.DaivaAnughara || {};
window.DaivaAnughara.main = {
    updateAnnouncementBanner,
    initMobileMenu,
    initDropdowns,
    initSmoothScrolling,
    initAccessibility
};
