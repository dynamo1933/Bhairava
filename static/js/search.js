// ===== DAIVA ANUGHARA - SEARCH FUNCTIONALITY =====
// Site-wide search implementation

document.addEventListener('DOMContentLoaded', function() {
    initSearch();
});

function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.getElementById('search-input');
    const searchModal = document.getElementById('search-modal');
    const closeModal = document.querySelector('.close-modal');
    
    if (!searchForm || !searchInput || !searchModal) return;
    
    // Handle search form submission
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const query = searchInput.value.trim();
        
        if (query.length < 2) {
            showSearchError('Please enter at least 2 characters to search.');
            return;
        }
        
        performSearch(query);
    });
    
    // Handle search input changes (debounced)
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        } else {
            hideSearchModal();
        }
    });
    
    // Close modal functionality
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            hideSearchModal();
        });
    }
    
    // Close modal when clicking outside
    searchModal.addEventListener('click', function(event) {
        if (event.target === searchModal) {
            hideSearchModal();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + K to open search
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            searchInput.focus();
        }
        
        // Escape to close search modal
        if (event.key === 'Escape') {
            hideSearchModal();
        }
    });
    
    // Focus search input when modal opens
    searchModal.addEventListener('shown', function() {
        searchInput.focus();
    });
}

function performSearch(query) {
    const searchModal = document.getElementById('search-modal');
    const searchResults = document.getElementById('search-results');
    
    if (!searchModal || !searchResults) return;
    
    // Show loading state
    showSearchLoading();
    showSearchModal();
    
    // Fetch search results from API
    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.results, query);
        })
        .catch(error => {
            console.error('Search error:', error);
            showSearchError('An error occurred while searching. Please try again.');
        });
}

function displaySearchResults(results, query) {
    const searchResults = document.getElementById('search-results');
    const searchModal = document.getElementById('search-modal');
    
    if (!searchResults || !searchModal) return;
    
    if (results.length === 0) {
        searchResults.innerHTML = `
            <div class="no-results">
                <p>No results found for "<strong>${escapeHtml(query)}</strong>"</p>
                <p>Try different keywords or check the spelling.</p>
            </div>
        `;
        return;
    }
    
    // Group results by page
    const groupedResults = groupResultsByPage(results);
    
    let html = `<div class="search-summary">Found ${results.length} result${results.length === 1 ? '' : 's'} for "<strong>${escapeHtml(query)}</strong>"</div>`;
    
    Object.keys(groupedResults).forEach(page => {
        const pageResults = groupedResults[page];
        const pageTitle = getPageTitle(page);
        
        html += `
            <div class="search-page-group">
                <h4 class="page-group-title">${pageTitle}</h4>
                <ul class="search-results-list">
        `;
        
        pageResults.forEach(result => {
            html += `
                <li class="search-result-item">
                    <a href="${result.url}" class="search-result-link">
                        <span class="result-title">${highlightQuery(result.title, query)}</span>
                        <span class="result-page">${pageTitle}</span>
                    </a>
                </li>
            `;
        });
        
        html += `
                </ul>
            </div>
        `;
    }
    
    searchResults.innerHTML = html;
    
    // Add click handlers to result links
    const resultLinks = searchResults.querySelectorAll('.search-result-link');
    resultLinks.forEach(link => {
        link.addEventListener('click', function() {
            hideSearchModal();
            // Clear search input
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.value = '';
            }
        });
    });
}

function groupResultsByPage(results) {
    const grouped = {};
    
    results.forEach(result => {
        if (!grouped[result.page]) {
            grouped[result.page] = [];
        }
        grouped[result.page].push(result);
    });
    
    return grouped;
}

function getPageTitle(page) {
    const pageTitles = {
        'home': 'Home',
        'documents': 'Documents & Updates',
        'ashtami': 'Ashtami',
        'devi': 'Devi',
        'about': 'About'
    };
    
    return pageTitles[page] || page.charAt(0).toUpperCase() + page.slice(1);
}

function highlightQuery(text, query) {
    if (!query) return escapeHtml(text);
    
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return escapeHtml(text).replace(regex, '<mark>$1</mark>');
}

function showSearchModal() {
    const searchModal = document.getElementById('search-modal');
    if (searchModal) {
        searchModal.removeAttribute('hidden');
        // Trigger shown event
        searchModal.dispatchEvent(new CustomEvent('shown'));
    }
}

function hideSearchModal() {
    const searchModal = document.getElementById('search-modal');
    if (searchModal) {
        searchModal.setAttribute('hidden', '');
    }
}

function showSearchLoading() {
    const searchResults = document.getElementById('search-results');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="search-loading">
                <div class="loading-spinner"></div>
                <p>Searching...</p>
            </div>
        `;
    }
}

function showSearchError(message) {
    const searchResults = document.getElementById('search-results');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="search-error">
                <p>${escapeHtml(message)}</p>
            </div>
        `;
    }
    
    // Show modal to display error
    showSearchModal();
}

// ===== UTILITY FUNCTIONS =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeRegex(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// ===== SEARCH SUGGESTIONS =====
function getSearchSuggestions(query) {
    // Common spiritual terms and concepts
    const suggestions = [
        'Bhairava Sadhana',
        'Sādhanā Paddhati',
        'Ashtami',
        'Devi',
        'spiritual practice',
        'meditation',
        'guidelines',
        'sacred documents',
        'pranayama',
        'mantra',
        'dhyana',
        'yoga',
        'spiritual awakening',
        'divine grace',
        'surrender',
        'devotion'
    ];
    
    if (!query || query.length < 2) return [];
    
    const filtered = suggestions.filter(suggestion => 
        suggestion.toLowerCase().includes(query.toLowerCase())
    );
    
    return filtered.slice(0, 5); // Return top 5 suggestions
}

// ===== SEARCH HISTORY =====
function saveSearchQuery(query) {
    if (!query || query.length < 2) return;
    
    let searchHistory = JSON.parse(localStorage.getItem('daivaSearchHistory') || '[]');
    
    // Remove if already exists
    searchHistory = searchHistory.filter(item => item !== query);
    
    // Add to beginning
    searchHistory.unshift(query);
    
    // Keep only last 10 searches
    searchHistory = searchHistory.slice(0, 10);
    
    localStorage.setItem('daivaSearchHistory', JSON.stringify(searchHistory));
}

function getSearchHistory() {
    return JSON.parse(localStorage.getItem('daivaSearchHistory') || '[]');
}

function clearSearchHistory() {
    localStorage.removeItem('daivaSearchHistory');
}

// ===== ADVANCED SEARCH FEATURES =====
function initAdvancedSearch() {
    // Add filters for different types of content
    const searchFilters = document.createElement('div');
    searchFilters.className = 'search-filters';
    searchFilters.innerHTML = `
        <div class="filter-group">
            <label>Content Type:</label>
            <select id="content-type-filter">
                <option value="">All Content</option>
                <option value="documents">Documents</option>
                <option value="practices">Spiritual Practices</option>
                <option value="guidelines">Guidelines</option>
                <option value="information">General Information</option>
            </select>
        </div>
        <div class="filter-group">
            <label>Difficulty Level:</label>
            <select id="difficulty-filter">
                <option value="">All Levels</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
            </select>
        </div>
    `;
    
    // Insert filters after search input
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.appendChild(searchFilters);
    }
}

// ===== SEARCH ANALYTICS =====
function trackSearch(query, resultsCount) {
    // Track search usage for analytics
    if (typeof gtag !== 'undefined') {
        gtag('event', 'search', {
            search_term: query,
            results_count: resultsCount
        });
    }
    
    // Save search query for history
    saveSearchQuery(query);
}

// ===== EXPORT FUNCTIONS =====
window.DaivaAnughara = window.DaivaAnughara || {};
window.DaivaAnughara.search = {
    performSearch,
    getSearchSuggestions,
    getSearchHistory,
    clearSearchHistory,
    initAdvancedSearch
};
