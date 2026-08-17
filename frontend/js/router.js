/**
 * Single Page Application Hash Router with Landing Page & Editorial Views
 */
window.Router = {
    routes: {
        'landing': { view: 'LandingView', title: 'COOUCodeGuard &bull; Code Integrity System', authRequired: false },
        'login': { view: 'AuthView', title: 'Lecturer Authentication', authRequired: false },
        'dashboard': { view: 'DashboardView', title: 'Forensic Overview', authRequired: false }, // Allow preview with demo data
        'submissions': { view: 'SubmissionsView', title: 'Stored Submissions', authRequired: false },
        'upload': { view: 'UploadView', title: 'Ingest Assignment', authRequired: false },
        'scan': { view: 'ScanView', title: 'Plagiarism Scanner', authRequired: false },
        'results': { view: 'ResultsView', title: 'Forensic Analysis & Code Diff', authRequired: false },
        'repository': { view: 'RepositoryView', title: 'Local Repository Corpus', authRequired: false },
        'reports': { view: 'ReportsView', title: 'Audit Dossiers', authRequired: false },
        'settings': { view: 'SettingsView', title: 'System Diagnostics', authRequired: false }
    },

    init() {
        window.addEventListener('hashchange', () => this.handleRoute());
        this.handleRoute();
    },

    async handleRoute() {
        const rawHash = window.location.hash.slice(1) || 'landing';
        const routeKey = rawHash.split('?')[0] || 'landing';
        const route = this.routes[routeKey] || this.routes['landing'];

        // Adjust UI shell visibility based on route
        const sidebar = document.getElementById('sidebar');
        const topbar = document.getElementById('topbar');
        const contentBody = document.getElementById('content-body');
        const pageTitle = document.getElementById('page-title');

        if (routeKey === 'landing' || routeKey === 'login') {
            if (sidebar) sidebar.style.display = 'none';
            if (topbar) topbar.style.display = 'none';
            if (contentBody) contentBody.style.padding = '0';
        } else {
            if (sidebar) sidebar.style.display = 'flex';
            if (topbar) topbar.style.display = 'flex';
            if (contentBody) contentBody.style.padding = '32px';
            if (pageTitle) pageTitle.textContent = route.title;

            // Update active menu link
            document.querySelectorAll('.nav-item').forEach(el => {
                const target = el.getAttribute('href')?.replace('#', '');
                if (target === routeKey) {
                    el.classList.add('active');
                } else {
                    el.classList.remove('active');
                }
            });
        }

        // Render target view safely
        const viewObj = window[route.view];
        if (viewObj && typeof viewObj.render === 'function') {
            contentBody.innerHTML = '<div style="text-align:center; padding:40px; font-family:var(--font-mono); color:var(--color-text-muted);">&gt; LOADING FORENSIC MODULE...</div>';
            try {
                const html = await viewObj.render();
                contentBody.innerHTML = html;

                // Post-render lifecycle hooks
                if (routeKey === 'dashboard') {
                    try {
                        const stats = await API.getDashboardStats();
                        DashboardView.initCharts(stats);
                    } catch (e) {
                        // Fallback mock stats for offline preview
                        DashboardView.initCharts({
                            similarity_distribution: { '0-29% (Low)': 4, '30-59% (Moderate)': 2, '60-79% (High)': 2, '80-100% (Critical)': 2 },
                            language_distribution: { 'Python': 4, 'Java': 2, 'C++': 2 }
                        });
                    }
                }

                // Render all SVG icons
                if (window.LucideIcons) {
                    LucideIcons.init();
                }
            } catch (err) {
                console.error("View rendering error:", err);
                contentBody.innerHTML = `<div class="card" style="border-color:var(--color-danger); color:var(--color-danger); font-family:var(--font-mono);">&gt; MODULE ERROR: ${err.message}</div>`;
            }
        }
    }
};
