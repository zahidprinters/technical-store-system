// Dashboard specific JavaScript for Technical Store System

class TSSDashboard {
    constructor() {
        this.tasks = {};
        this.progress = {};
        this.charts = {};
        this.init();
    }

    init() {
        this.loadTaskData();
        this.setupEventListeners();
        this.initializeCharts();
        this.updateAllProgress();
        this.animateCounters();
        this.setupRealTimeUpdates();
    }

    // Load task data from localStorage or initialize defaults
    loadTaskData() {
        const savedTasks = localStorage.getItem('tss-dashboard-tasks');
        if (savedTasks) {
            this.tasks = JSON.parse(savedTasks);
        } else {
            // Initialize default task structure
            this.tasks = {
                phase1: {
                    foundation: {
                        'Store Settings': false,
                        'Store UOM': false,
                        'Store Item Group': false,
                        'Store Technical Category': false,
                        'Store Location': false,
                        'Store Item': false,
                        'Store Item Serial Number': false,
                        'Store Item Batch Number': false
                    }
                },
                phase2: {
                    transactions: {
                        'Store Item Receipt': false,
                        'Store Item Issue': false,
                        'Store Item Requisition': false
                    },
                    workflows: {
                        'Approval Workflows': false,
                        'Quality Control': false,
                        'Reporting System': false
                    }
                },
                phase3: {
                    advanced: {
                        'Advanced Analytics': false,
                        'Mobile App': false,
                        'API Integration': false,
                        'Multi-tenant Support': false
                    }
                }
            };
        }
    }

    // Setup event listeners
    setupEventListeners() {
        // Task checkboxes
        document.querySelectorAll('.task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.updateTaskStatus(e.target);
                this.saveTaskData();
                this.updateAllProgress();
            });
        });

        // Collapsible sections
        document.querySelectorAll('.task-header').forEach(header => {
            header.addEventListener('click', function() {
                const section = this.closest('.task-section');
                section.classList.toggle('active');
            });
        });

        // Progress ring hover effects
        document.querySelectorAll('.progress-ring').forEach(ring => {
            ring.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
            });
            ring.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }

    // Update task status
    updateTaskStatus(checkbox) {
        const taskId = checkbox.id;
        const isChecked = checkbox.checked;

        // Update task status in data structure
        const [phase, category, task] = taskId.split('-');
        if (this.tasks[phase] && this.tasks[phase][category]) {
            this.tasks[phase][category][task] = isChecked;
        }

        // Update visual feedback
        const taskItem = checkbox.closest('.task-item');
        if (taskItem) {
            taskItem.classList.toggle('completed', isChecked);
        }
    }

    // Save task data to localStorage
    saveTaskData() {
        localStorage.setItem('tss-dashboard-tasks', JSON.stringify(this.tasks));
    }

    // Update all progress calculations
    updateAllProgress() {
        Object.keys(this.tasks).forEach(phase => {
            this.updatePhaseProgress(phase);
        });
        this.updateOverallProgress();
    }

    // Update phase progress
    updatePhaseProgress(phase) {
        const phaseData = this.tasks[phase];
        let totalTasks = 0;
        let completedTasks = 0;

        Object.values(phaseData).forEach(category => {
            Object.values(category).forEach(isCompleted => {
                totalTasks++;
                if (isCompleted) completedTasks++;
            });
        });

        const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
        this.progress[phase] = progress;

        this.updateProgressRing(phase, progress);
        this.updateProgressText(phase, progress, completedTasks, totalTasks);
    }

    // Update progress ring
    updateProgressRing(phase, progress) {
        const ring = document.querySelector(`#${phase}-ring .progress-ring-fill`);
        const text = document.querySelector(`#${phase}-ring .progress-ring-text`);

        if (ring && text) {
            const circumference = 283; // 2 * π * 45
            const offset = circumference - (progress / 100) * circumference;

            ring.style.strokeDashoffset = offset;
            text.textContent = Math.round(progress) + '%';

            // Update color based on progress
            const ringElement = ring.closest('.progress-ring');
            ringElement.className = `progress-ring progress-${this.getProgressClass(progress)}`;
        }
    }

    // Update progress text
    updateProgressText(phase, progress, completed, total) {
        const textElement = document.querySelector(`#${phase}-progress-text`);
        if (textElement) {
            textElement.innerHTML = `
                <strong>${Math.round(progress)}% Complete</strong><br>
                <small>${completed}/${total} tasks</small>
            `;
        }
    }

    // Get progress class for styling
    getProgressClass(progress) {
        if (progress === 100) return 'complete';
        if (progress >= 75) return 'high';
        if (progress >= 50) return 'medium';
        if (progress >= 25) return 'low';
        return 'none';
    }

    // Update overall progress
    updateOverallProgress() {
        const totalProgress = Object.values(this.progress);
        const averageProgress = totalProgress.reduce((a, b) => a + b, 0) / totalProgress.length;

        const overallElement = document.querySelector('#overall-progress');
        if (overallElement) {
            overallElement.textContent = Math.round(averageProgress) + '%';
        }

        // Update overall progress bar
        const progressBar = document.querySelector('#overall-progress-bar .progress-fill');
        if (progressBar) {
            progressBar.style.width = averageProgress + '%';
        }
    }

    // Initialize charts
    initializeCharts() {
        this.createProgressChart();
        this.createTimelineChart();
        this.createTaskDistributionChart();
    }

    // Create progress chart
    createProgressChart() {
        const ctx = document.getElementById('progress-chart');
        if (!ctx) return;

        const data = {
            labels: ['Phase 1', 'Phase 2', 'Phase 3'],
            datasets: [{
                label: 'Completion %',
                data: [this.progress.phase1 || 0, this.progress.phase2 || 0, this.progress.phase3 || 0],
                backgroundColor: [
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 152, 0, 0.8)',
                    'rgba(33, 150, 243, 0.8)'
                ],
                borderColor: [
                    '#4CAF50',
                    '#FF9800',
                    '#2196F3'
                ],
                borderWidth: 2
            }]
        };

        this.charts.progress = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Create timeline chart
    createTimelineChart() {
        const ctx = document.getElementById('timeline-chart');
        if (!ctx) return;

        const data = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Planned Progress',
                data: [10, 25, 45, 60, 75, 85, 90, 95, 98, 100, 100, 100],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Actual Progress',
                data: [10, 20, 35, 50, 65, 75, 80, 85, 88, 90, 92, 94],
                borderColor: '#764ba2',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                fill: true,
                tension: 0.4
            }]
        };

        this.charts.timeline = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // Create task distribution chart
    createTaskDistributionChart() {
        const ctx = document.getElementById('distribution-chart');
        if (!ctx) return;

        const data = {
            labels: ['Completed', 'In Progress', 'Planned'],
            datasets: [{
                data: [45, 12, 43],
                backgroundColor: [
                    '#4CAF50',
                    '#FF9800',
                    '#2196F3'
                ],
                borderWidth: 0
            }]
        };

        this.charts.distribution = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Animate counters
    animateCounters() {
        const counters = document.querySelectorAll('.stat-number, .summary-number');

        counters.forEach(counter => {
            const target = parseInt(counter.textContent.replace(/[^\d]/g, ''));
            if (target && target > 0) {
                this.animateCounter(counter, 0, target, 2000);
            }
        });
    }

    // Animate counter function
    animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        const startValue = start;
        const endValue = end;

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const current = Math.floor(startValue + (endValue - startValue) * this.easeOutCubic(progress));

            if (element.classList.contains('summary-number')) {
                element.textContent = current.toLocaleString();
            } else {
                element.textContent = current;
            }

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    // Easing function
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    // Setup real-time updates
    setupRealTimeUpdates() {
        // Update progress every 30 seconds
        setInterval(() => {
            this.updateAllProgress();
        }, 30000);

        // Listen for storage changes (for multi-tab synchronization)
        window.addEventListener('storage', (e) => {
            if (e.key === 'tss-dashboard-tasks') {
                this.loadTaskData();
                this.updateAllProgress();
            }
        });
    }

    // Export progress data
    exportProgress() {
        const data = {
            tasks: this.tasks,
            progress: this.progress,
            exportDate: new Date().toISOString(),
            version: '1.0'
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `tss-progress-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // Import progress data
    importProgress(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                if (data.tasks && data.progress) {
                    this.tasks = data.tasks;
                    this.progress = data.progress;
                    this.saveTaskData();
                    this.updateAllProgress();
                    this.showNotification('Progress data imported successfully!', 'success');
                } else {
                    throw new Error('Invalid file format');
                }
            } catch (error) {
                this.showNotification('Error importing progress data: ' + error.message, 'error');
            }
        };
        reader.readAsText(file);
    }

    // Show notification (fallback if main utils not available)
    showNotification(message, type = 'info') {
        if (window.TSS && window.TSS.utils && window.TSS.utils.showNotification) {
            window.TSS.utils.showNotification(message, type);
        } else {
            alert(message);
        }
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.dashboard-header')) {
        window.tssDashboard = new TSSDashboard();
    }
});

// Export for global access
window.TSSDashboard = TSSDashboard;