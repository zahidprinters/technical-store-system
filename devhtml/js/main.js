// Main JavaScript for Technical Store System Documentation
// Global variables and utilities

const TSS = {
    // Configuration
    config: {
        theme: localStorage.getItem('tss-theme') || 'light',
        animations: true,
        autoSave: true
    },

    // DOM elements cache
    elements: {},

    // Utility functions
    utils: {
        // Debounce function for performance
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Throttle function for performance
        throttle: function(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            }
        },

        // Copy to clipboard
        copyToClipboard: async function(text) {
            try {
                await navigator.clipboard.writeText(text);
                this.showNotification('Copied to clipboard!', 'success');
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                this.showNotification('Copied to clipboard!', 'success');
            }
        },

        // Show notification
        showNotification: function(message, type = 'info', duration = 3000) {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.innerHTML = `
                <i class="fas ${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            `;

            document.body.appendChild(notification);

            // Animate in
            setTimeout(() => notification.classList.add('show'), 10);

            // Auto remove
            if (duration > 0) {
                setTimeout(() => {
                    notification.classList.remove('show');
                    setTimeout(() => notification.remove(), 300);
                }, duration);
            }
        },

        // Get notification icon based on type
        getNotificationIcon: function(type) {
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-exclamation-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };
            return icons[type] || icons.info;
        },

        // Format date
        formatDate: function(date) {
            return new Date(date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        },

        // Check if element is in viewport
        isInViewport: function(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        },

        // Smooth scroll to element
        scrollToElement: function(element, offset = 0) {
            const elementPosition = element.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - offset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    },

    // Theme management
    theme: {
        // Initialize theme
        init: function() {
            this.applyTheme(TSS.config.theme);
            this.createThemeToggle();
        },

        // Apply theme
        applyTheme: function(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('tss-theme', theme);
            TSS.config.theme = theme;
        },

        // Toggle theme
        toggle: function() {
            const newTheme = TSS.config.theme === 'light' ? 'dark' : 'light';
            this.applyTheme(newTheme);
        },

        // Create theme toggle button
        createThemeToggle: function() {
            const toggle = document.createElement('button');
            toggle.className = 'theme-toggle';
            toggle.innerHTML = '<i class="fas fa-moon"></i>';
            toggle.title = 'Toggle theme';
            toggle.onclick = () => this.toggle();

            document.body.appendChild(toggle);
        }
    },

    // Navigation management
    navigation: {
        // Initialize navigation
        init: function() {
            this.setupMobileNav();
            this.setupScrollSpy();
            this.setupSmoothScrolling();
        },

        // Setup mobile navigation
        setupMobileNav: function() {
            const navToggle = document.querySelector('.nav-toggle');
            const navLinks = document.querySelector('.nav-links');

            if (navToggle && navLinks) {
                navToggle.addEventListener('click', () => {
                    navLinks.classList.toggle('open');
                });

                // Close mobile nav when clicking outside
                document.addEventListener('click', (e) => {
                    if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                        navLinks.classList.remove('open');
                    }
                });
            }
        },

        // Setup scroll spy for navigation highlighting
        setupScrollSpy: function() {
            const sections = document.querySelectorAll('section[id]');
            const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

            window.addEventListener('scroll', TSS.utils.throttle(() => {
                let current = '';

                sections.forEach(section => {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.clientHeight;

                    if (window.pageYOffset >= sectionTop - sectionHeight / 3) {
                        current = section.getAttribute('id');
                    }
                });

                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href').substring(1) === current) {
                        link.classList.add('active');
                    }
                });
            }, 100));
        },

        // Setup smooth scrolling for anchor links
        setupSmoothScrolling: function() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));

                    if (target) {
                        TSS.utils.scrollToElement(target, 80);
                    }
                });
            });
        }
    },

    // Component management
    components: {
        // Initialize components
        init: function() {
            this.setupTabs();
            this.setupAccordions();
            this.setupCodeBlocks();
            this.setupTooltips();
        },

        // Setup tabs
        setupTabs: function() {
            document.querySelectorAll('.tabs').forEach(tabContainer => {
                const tabs = tabContainer.querySelectorAll('.tab');
                const contents = tabContainer.parentElement.querySelectorAll('.tab-content');

                tabs.forEach((tab, index) => {
                    tab.addEventListener('click', () => {
                        // Remove active class from all tabs and contents
                        tabs.forEach(t => t.classList.remove('active'));
                        contents.forEach(c => c.classList.remove('active'));

                        // Add active class to clicked tab and corresponding content
                        tab.classList.add('active');
                        contents[index].classList.add('active');
                    });
                });
            });
        },

        // Setup accordions
        setupAccordions: function() {
            document.querySelectorAll('.accordion').forEach(accordion => {
                const header = accordion.querySelector('.accordion-header');

                header.addEventListener('click', () => {
                    accordion.classList.toggle('active');
                });
            });
        },

        // Setup code blocks with copy functionality
        setupCodeBlocks: function() {
            document.querySelectorAll('.code-block').forEach(block => {
                // Add copy button if not already present
                if (!block.querySelector('.code-copy-btn')) {
                    const copyBtn = document.createElement('button');
                    copyBtn.className = 'code-copy-btn';
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                    copyBtn.onclick = () => {
                        const code = block.querySelector('pre, code')?.textContent || block.textContent;
                        TSS.utils.copyToClipboard(code.trim());
                        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        copyBtn.classList.add('copied');
                        setTimeout(() => {
                            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                            copyBtn.classList.remove('copied');
                        }, 2000);
                    };
                    block.appendChild(copyBtn);
                }
            });
        },

        // Setup tooltips
        setupTooltips: function() {
            // Tooltips are handled via CSS hover, but we can add JS enhancements here
            document.querySelectorAll('.tooltip').forEach(tooltip => {
                tooltip.addEventListener('mouseenter', function() {
                    // Add any JS tooltip enhancements here
                });
            });
        }
    },

    // Dashboard specific functionality
    dashboard: {
        // Initialize dashboard
        init: function() {
            this.setupProgressTracking();
            this.setupTaskManagement();
            this.animateStats();
        },

        // Setup progress tracking
        setupProgressTracking: function() {
            this.updateProgress();

            // Update progress when checkboxes change
            document.querySelectorAll('.task-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', () => this.updateProgress());
            });
        },

        // Update progress calculations
        updateProgress: function() {
            const phases = ['phase1', 'phase2', 'phase3'];

            phases.forEach(phase => {
                const phaseElement = document.getElementById(phase);
                if (!phaseElement) return;

                const checkboxes = phaseElement.querySelectorAll('.task-checkbox');
                const checked = phaseElement.querySelectorAll('.task-checkbox:checked');

                const progress = checkboxes.length > 0 ? (checked.length / checkboxes.length) * 100 : 0;
                this.updateProgressRing(phase, progress);
                this.updateProgressText(phase, progress);
            });
        },

        // Update progress ring
        updateProgressRing: function(phase, progress) {
            const ring = document.querySelector(`#${phase}-ring .progress-ring-fill`);
            const text = document.querySelector(`#${phase}-ring .progress-ring-text`);

            if (ring && text) {
                const circumference = 283; // 2 * π * 45 (radius)
                const offset = circumference - (progress / 100) * circumference;

                ring.style.strokeDashoffset = offset;
                text.textContent = Math.round(progress) + '%';
            }
        },

        // Update progress text
        updateProgressText: function(phase, progress) {
            const textElement = document.querySelector(`#${phase}-progress-text`);
            if (textElement) {
                textElement.textContent = Math.round(progress) + '% Complete';
            }
        },

        // Setup task management
        setupTaskManagement: function() {
            document.querySelectorAll('.task-header').forEach(header => {
                header.addEventListener('click', function() {
                    const taskSection = this.closest('.task-section');
                    taskSection.classList.toggle('active');
                });
            });

            // Load saved checkbox states
            this.loadTaskStates();

            // Save checkbox states on change
            document.querySelectorAll('.task-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', () => this.saveTaskStates());
            });
        },

        // Load task states from localStorage
        loadTaskStates: function() {
            const savedStates = localStorage.getItem('tss-task-states');
            if (savedStates) {
                const states = JSON.parse(savedStates);
                Object.keys(states).forEach(taskId => {
                    const checkbox = document.getElementById(taskId);
                    if (checkbox) {
                        checkbox.checked = states[taskId];
                    }
                });
            }
        },

        // Save task states to localStorage
        saveTaskStates: function() {
            const states = {};
            document.querySelectorAll('.task-checkbox').forEach(checkbox => {
                states[checkbox.id] = checkbox.checked;
            });
            localStorage.setItem('tss-task-states', JSON.stringify(states));
        },

        // Animate statistics counters
        animateStats: function() {
            const statNumbers = document.querySelectorAll('.stat-number');

            statNumbers.forEach(stat => {
                const target = parseInt(stat.textContent.replace(/[^\d]/g, ''));
                if (target) {
                    this.animateCounter(stat, 0, target, 2000);
                }
            });
        },

        // Animate counter
        animateCounter: function(element, start, end, duration) {
            const startTime = performance.now();

            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                const current = Math.floor(start + (end - start) * this.easeOutCubic(progress));
                element.textContent = current.toLocaleString();

                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            };

            requestAnimationFrame(animate);
        },

        // Easing function
        easeOutCubic: function(t) {
            return 1 - Math.pow(1 - t, 3);
        }
    },

    // Search functionality
    search: {
        // Initialize search
        init: function() {
            this.createSearchInterface();
            this.setupSearchFunctionality();
        },

        // Create search interface
        createSearchInterface: function() {
            const searchContainer = document.createElement('div');
            searchContainer.className = 'search-container';
            searchContainer.innerHTML = `
                <div class="search-input-container">
                    <i class="fas fa-search search-icon"></i>
                    <input type="text" class="search-input" placeholder="Search documentation...">
                    <button class="search-clear" style="display: none;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="search-results" style="display: none;"></div>
            `;

            // Insert after navigation
            const nav = document.querySelector('.nav');
            if (nav) {
                nav.parentNode.insertBefore(searchContainer, nav.nextSibling);
            }

            this.searchInput = searchContainer.querySelector('.search-input');
            this.searchResults = searchContainer.querySelector('.search-results');
            this.searchClear = searchContainer.querySelector('.search-clear');
        },

        // Setup search functionality
        setupSearchFunctionality: function() {
            if (!this.searchInput) return;

            // Search input handler
            this.searchInput.addEventListener('input', TSS.utils.debounce(() => {
                const query = this.searchInput.value.trim();
                if (query.length > 2) {
                    this.performSearch(query);
                    this.searchClear.style.display = 'block';
                } else {
                    this.hideResults();
                    this.searchClear.style.display = 'none';
                }
            }, 300));

            // Clear search
            this.searchClear.addEventListener('click', () => {
                this.searchInput.value = '';
                this.hideResults();
                this.searchClear.style.display = 'none';
                this.searchInput.focus();
            });

            // Hide results when clicking outside
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.search-container')) {
                    this.hideResults();
                }
            });
        },

        // Perform search
        performSearch: function(query) {
            const results = this.searchContent(query);
            this.displayResults(results, query);
        },

        // Search content
        searchContent: function(query) {
            const results = [];
            const elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li, .code-block');

            elements.forEach(element => {
                const text = element.textContent.toLowerCase();
                const queryLower = query.toLowerCase();

                if (text.includes(queryLower)) {
                    results.push({
                        element: element,
                        text: element.textContent,
                        type: element.tagName.toLowerCase(),
                        relevance: this.calculateRelevance(text, queryLower)
                    });
                }
            });

            return results.sort((a, b) => b.relevance - a.relevance).slice(0, 10);
        },

        // Calculate relevance score
        calculateRelevance: function(text, query) {
            let score = 0;

            // Exact matches get higher score
            if (text === query) score += 100;

            // Starts with query
            if (text.startsWith(query)) score += 50;

            // Contains query
            if (text.includes(query)) score += 20;

            // Word boundaries
            const words = query.split(' ');
            words.forEach(word => {
                const regex = new RegExp(`\\b${word}\\b`, 'gi');
                if (regex.test(text)) score += 10;
            });

            return score;
        },

        // Display search results
        displayResults: function(results, query) {
            if (results.length === 0) {
                this.searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
            } else {
                const html = results.map(result => `
                    <div class="search-result-item" onclick="TSS.search.navigateToResult('${result.element.id || ''}', '${result.element.offsetTop}')">
                        <div class="search-result-type">${result.type}</div>
                        <div class="search-result-text">${this.highlightText(result.text, query)}</div>
                    </div>
                `).join('');

                this.searchResults.innerHTML = html;
            }

            this.searchResults.style.display = 'block';
        },

        // Highlight search text
        highlightText: function(text, query) {
            const regex = new RegExp(`(${query})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        },

        // Navigate to search result
        navigateToResult: function(id, position) {
            if (id) {
                const element = document.getElementById(id);
                if (element) {
                    TSS.utils.scrollToElement(element, 80);
                }
            } else {
                window.scrollTo({ top: position - 80, behavior: 'smooth' });
            }
            this.hideResults();
        },

        // Hide search results
        hideResults: function() {
            if (this.searchResults) {
                this.searchResults.style.display = 'none';
            }
        }
    },

    // Initialize everything
    init: function() {
        // Initialize all modules
        this.theme.init();
        this.navigation.init();
        this.components.init();

        // Initialize page-specific functionality
        if (document.querySelector('.dashboard-header')) {
            this.dashboard.init();
        }

        // Initialize search if enabled
        if (document.body.dataset.search !== 'false') {
            this.search.init();
        }

        // Add loading class removal
        document.body.classList.add('loaded');

        console.log('Technical Store System Documentation initialized');
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    TSS.init();
});

// Global error handler
window.addEventListener('error', (e) => {
    console.error('TSS Error:', e.error);
    TSS.utils.showNotification('An error occurred. Please refresh the page.', 'error');
});

// Service worker registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}