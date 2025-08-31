// ===== DAIVA ANUGHARA - COUNTDOWN TIMER =====
// Ashtami Sadhana countdown functionality

let countdownInterval;
let ashtamiCountdownInterval;

document.addEventListener('DOMContentLoaded', function() {
    initCountdown();
});

// Countdown Timer for Home Page
function initCountdown() {
    // Fetch next Ashtami date first
    fetch('/api/next-ashtami')
        .then(response => response.json())
        .then(data => {
            if (data && data.date) {
                // Now get countdown for this date
                return fetch(`/api/countdown?next_ashtami=${data.date}`);
            } else {
                throw new Error('No Ashtami date available');
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.warn('Countdown API error:', data.error);
                // Set default countdown display
                updateCountdownDisplay();
            } else {
                startCountdownTimer(data);
            }
        })
        .catch(error => {
            console.warn('Error fetching countdown:', error);
            // Set default countdown display
            updateCountdownDisplay();
        });
}

// ===== HOME PAGE COUNTDOWN =====
function updateCountdownDisplay() {
    fetch('/api/countdown')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log('No upcoming Ashtami found');
                displayNoAshtamiMessage();
                return;
            }
            
            updateCountdownElements(data);
        })
        .catch(error => {
            console.error('Error fetching countdown:', error);
            displayCountdownError();
        });
}

function updateCountdownElements(data) {
    const daysElement = document.getElementById('countdown-days');
    const hoursElement = document.getElementById('countdown-hours');
    const minutesElement = document.getElementById('countdown-minutes');
    
    if (daysElement) daysElement.textContent = data.days || '--';
    if (hoursElement) hoursElement.textContent = data.hours || '--';
    if (minutesElement) minutesElement.textContent = data.minutes || '--';
    
    // Add visual feedback for different time ranges
    addCountdownVisualFeedback(data);
}

function startCountdownTimer() {
    // Update countdown every minute
    countdownInterval = setInterval(() => {
        updateCountdownDisplay();
    }, 60000); // 60 seconds
}

// ===== ASHTAMI PAGE COUNTDOWN =====
function updateAshtamiCountdown() {
    fetch('/api/countdown')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log('No upcoming Ashtami found');
                displayAshtamiNoUpcoming();
                return;
            }
            
            updateAshtamiCountdownElements(data);
        })
        .catch(error => {
            console.error('Error fetching Ashtami countdown:', error);
            displayAshtamiCountdownError();
        });
}

function updateAshtamiCountdownElements(data) {
    const daysElement = document.getElementById('ashtami-days');
    const hoursElement = document.getElementById('ashtami-hours');
    const minutesElement = document.getElementById('ashtami-minutes');
    
    if (daysElement) daysElement.textContent = data.days || '--';
    if (hoursElement) hoursElement.textContent = data.hours || '--';
    if (minutesElement) minutesElement.textContent = data.minutes || '--';
    
    // Add special visual effects for Ashtami countdown
    addAshtamiCountdownEffects(data);
}

function startAshtamiCountdownTimer() {
    // Update Ashtami countdown every 30 seconds for more precision
    ashtamiCountdownInterval = setInterval(() => {
        updateAshtamiCountdown();
    }, 30000); // 30 seconds
}

// ===== VISUAL EFFECTS & FEEDBACK =====
function addCountdownVisualFeedback(data) {
    const countdownContainer = document.querySelector('.countdown-container');
    if (!countdownContainer) return;
    
    // Remove existing classes
    countdownContainer.classList.remove('urgent', 'approaching', 'distant');
    
    const totalHours = (data.days * 24) + data.hours;
    
    if (totalHours <= 24) {
        // Within 24 hours - urgent
        countdownContainer.classList.add('urgent');
        addUrgentAnimation();
    } else if (totalHours <= 72) {
        // Within 3 days - approaching
        countdownContainer.classList.add('approaching');
        addApproachingAnimation();
    } else {
        // More than 3 days - distant
        countdownContainer.classList.add('distant');
    }
}

function addAshtamiCountdownEffects(data) {
    const countdownContainer = document.querySelector('.countdown-timer-large');
    if (!countdownContainer) return;
    
    // Remove existing classes
    countdownContainer.classList.remove('urgent', 'approaching', 'distant');
    
    const totalHours = (data.days * 24) + data.hours;
    
    if (totalHours <= 24) {
        // Within 24 hours - urgent
        countdownContainer.classList.add('urgent');
        addAshtamiUrgentEffects();
    } else if (totalHours <= 72) {
        // Within 3 days - approaching
        countdownContainer.classList.add('approaching');
        addAshtamiApproachingEffects();
    } else {
        // More than 3 days - distant
        countdownContainer.classList.add('distant');
    }
}

function addUrgentAnimation() {
    const countdownItems = document.querySelectorAll('.countdown-item');
    countdownItems.forEach(item => {
        item.style.animation = 'pulse 1s infinite';
    });
}

function addApproachingAnimation() {
    const countdownItems = document.querySelectorAll('.countdown-item');
    countdownItems.forEach(item => {
        item.style.animation = 'glow 2s ease-in-out infinite alternate';
    });
}

function addAshtamiUrgentEffects() {
    const countdownItems = document.querySelectorAll('.countdown-item-large');
    countdownItems.forEach(item => {
        item.style.animation = 'urgentPulse 0.8s infinite';
        item.style.border = '2px solid #e74c3c';
    });
    
    // Add sound notification (if user has interacted with page)
    if (document.visibilityState === 'visible') {
        showUrgentNotification();
    }
}

function addAshtamiApproachingEffects() {
    const countdownItems = document.querySelectorAll('.countdown-item-large');
    countdownItems.forEach(item => {
        item.style.animation = 'approachingGlow 3s ease-in-out infinite alternate';
        item.style.border = '2px solid #f39c12';
    });
}

// ===== NOTIFICATIONS =====
function showUrgentNotification() {
    // Check if browser supports notifications
    if (!('Notification' in window)) return;
    
    // Check if user has granted permission
    if (Notification.permission === 'granted') {
        new Notification('🕉️ Ashtami Sadhana Approaching', {
            body: 'The sacred time for Ashtami Sadhana is within 24 hours. Please prepare your mind and space.',
            icon: '/static/images/favicon.ico',
            tag: 'ashtami-urgent'
        });
    } else if (Notification.permission !== 'denied') {
        // Request permission
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                showUrgentNotification();
            }
        });
    }
}

// ===== ERROR HANDLING =====
function displayNoAshtamiMessage() {
    const countdownContainer = document.querySelector('.countdown-container');
    if (!countdownContainer) return;
    
    countdownContainer.innerHTML = `
        <h3>No Upcoming Ashtami</h3>
        <p>Please check back later for the next Ashtami Sadhana schedule.</p>
        <p class="countdown-note">🕉️ Sacred timing will be announced when available 🕉️</p>
    `;
}

function displayCountdownError() {
    const countdownContainer = document.querySelector('.countdown-container');
    if (!countdownContainer) return;
    
    countdownContainer.innerHTML = `
        <h3>Countdown Unavailable</h3>
        <p>Unable to load countdown information at this time.</p>
        <p class="countdown-note">🕉️ Please refresh the page or try again later 🕉️</p>
    `;
}

function displayAshtamiNoUpcoming() {
    const countdownContainer = document.querySelector('.countdown-timer-large');
    if (!countdownContainer) return;
    
    countdownContainer.innerHTML = `
        <div class="no-upcoming-message">
            <h4>No Upcoming Ashtami</h4>
            <p>Please check back later for the next Ashtami Sadhana schedule.</p>
        </div>
    `;
}

function displayAshtamiCountdownError() {
    const countdownContainer = document.querySelector('.countdown-timer-large');
    if (!countdownContainer) return;
    
    countdownContainer.innerHTML = `
        <div class="countdown-error-message">
            <h4>Countdown Unavailable</h4>
            <p>Unable to load countdown information at this time.</p>
            <button onclick="updateAshtamiCountdown()" class="btn btn-secondary">Retry</button>
        </div>
    `;
}

// ===== UTILITY FUNCTIONS =====
function formatTime(seconds) {
    const days = Math.floor(seconds / (24 * 60 * 60));
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
    const minutes = Math.floor((seconds % (60 * 60)) / 60);
    
    return { days, hours, minutes };
}

function isAshtamiActive() {
    // Check if current time falls within Ashtami period
    // This would need to be implemented based on your specific Ashtami timing logic
    return false;
}

// ===== CLEANUP =====
function cleanupCountdown() {
    if (countdownInterval) {
        clearInterval(countdownInterval);
    }
    if (ashtamiCountdownInterval) {
        clearInterval(ashtamiCountdownInterval);
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', cleanupCountdown);

// ===== PAGE VISIBILITY HANDLING =====
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Page became visible, update countdown
        updateCountdownDisplay();
        updateAshtamiCountdown();
    }
});

// ===== EXPORT FUNCTIONS =====
window.DaivaAnughara = window.DaivaAnughara || {};
window.DaivaAnughara.countdown = {
    updateCountdownDisplay,
    updateAshtamiCountdown,
    startCountdownTimer,
    startAshtamiCountdownTimer,
    cleanupCountdown
};

// ===== CSS ANIMATIONS (if not defined in CSS) =====
function addCountdownCSSAnimations() {
    if (!document.getElementById('countdown-animations')) {
        const style = document.createElement('style');
        style.id = 'countdown-animations';
        style.textContent = `
            @keyframes urgentPulse {
                0%, 100% { 
                    transform: scale(1);
                    box-shadow: 0 0 20px rgba(231, 76, 60, 0.5);
                }
                50% { 
                    transform: scale(1.05);
                    box-shadow: 0 0 30px rgba(231, 76, 60, 0.8);
                }
            }
            
            @keyframes approachingGlow {
                0% { 
                    box-shadow: 0 0 15px rgba(243, 156, 18, 0.3);
                }
                100% { 
                    box-shadow: 0 0 25px rgba(243, 156, 18, 0.6);
                }
            }
            
            .urgent .countdown-item,
            .urgent .countdown-item-large {
                background: rgba(231, 76, 60, 0.2) !important;
            }
            
            .approaching .countdown-item,
            .approaching .countdown-item-large {
                background: rgba(243, 156, 18, 0.2) !important;
            }
        `;
        document.head.appendChild(style);
    }
}

// Add CSS animations when countdown is initialized
document.addEventListener('DOMContentLoaded', addCountdownCSSAnimations);
