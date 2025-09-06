// ===== DAIVA ANUGHARA - COUNTDOWN TIMER =====
// Ashtami Sadhana countdown functionality

document.addEventListener('DOMContentLoaded', function() {
    initCountdown('countdown-timer-home');
    initCountdown('countdown-timer-ashtami');
});

function initCountdown(elementId) {
    const countdownElement = document.getElementById(elementId);
    if (!countdownElement) {
        return;
    }

    fetch('/api/next-ashtami')
        .then(response => response.json())
        .then(data => {
            if (data && data.date) {
                const nextAshtamiDate = new Date(data.date);
                simplyCountdown(countdownElement, {
                    year: nextAshtamiDate.getFullYear(),
                    month: nextAshtamiDate.getMonth() + 1,
                    day: nextAshtamiDate.getDate(),
                    hours: nextAshtamiDate.getHours(),
                    minutes: nextAshtamiDate.getMinutes(),
                    seconds: nextAshtamiDate.getSeconds(),
                    words: {
                        days: { singular: 'day', plural: 'days' },
                        hours: { singular: 'hour', plural: 'hours' },
                        minutes: { singular: 'minute', plural: 'minutes' },
                        seconds: { singular: 'second', plural: 'seconds' }
                    },
                    plural: true,
                    inline: false,
                    enableUtc: false,
                    onEnd: function() {
                        countdownElement.innerHTML = '<p>The sacred time has arrived.</p>';
                    },
                    refresh: 1000,
                    sectionClass: 'simply-section',
                    amountClass: 'simply-amount',
                    wordClass: 'simply-word',
                    zeroPad: false,
                });
            } else {
                countdownElement.innerHTML = '<p>No upcoming Ashtami date available.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching countdown:', error);
            countdownElement.innerHTML = '<p>Could not load countdown.</p>';
        });
}