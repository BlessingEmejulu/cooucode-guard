/**
 * Single Page Application Hash Router with Role-Based Student/Lecturer Navigation
 */
window.Router = {
    routes: {
        'landing': { view: 'LandingView', title: 'COOUCodeGuard &bull; Code Integrity System', authRequired: false },
        'login': { view: 'AuthView', title: 'Session Authentication', authRequired: false },
        'student-portal': { view: 'StudentPortalView', title: 'Student Submission Portal', authRequired: false },
        'dashboard': { view: 'DashboardView', title: 'Forensic Overview', authRequired: false },
        'submissions': { view: 'SubmissionsView', title: 'Stored Submissions', authRequired: false },
        'upload': { view: 'UploadView', title: 'Ingest Assignment', authRequired: false },
        'scan': { view: 'ScanView', title: 'Plagiarism Scanner', authRequired: false },
        'results': { view: 'ResultsView', title: 'Forensic Analysis & Code Diff', authRequired: false },
        'repository': { view: 'RepositoryView', title: 'Local Repository Corpus', authRequired: false },
        'reports': { view: 'ReportsView', title: 'Audit Dossiers', authRequired: false },
        'settings': { view: 'SettingsView', title: 'System Diagnostics', authRequired: false }
    },

    isInitialized: false,

    init() {
        if (this.isInitialized) return;
        this.isInitialized = true;
        
        window.addEventListener('hashchange', () => this.handleRoute());
        setTimeout(() => this.handleRoute(), 0);
    },

    getView(viewName) {
        if (window[viewName] && typeof window[viewName].render === 'function') {
            return window[viewName];
        }
        
        // Explicit global view fallbacks
        if (viewName === 'LandingView' && window.LandingView) return window.LandingView;
        if (viewName === 'AuthView' && window.AuthView) return window.AuthView;
        if (viewName === 'StudentPortalView' && window.StudentPortalView) return window.StudentPortalView;
        if (viewName === 'DashboardView' && window.DashboardView) return window.DashboardView;
        return null;
    },

    updateRoleNav(user) {
        const isStudent = user && user.role === 'student';
        const navContainer = document.querySelector('.sidebar-nav');
        if (!navContainer) return;

        if (isStudent) {
            navContainer.innerHTML = `
                <div class="nav-section-title">01 // STUDENT_PORTAL</div>
                <a href="#student-portal" class="nav-item">
                    ${LucideIcons.render('layout-dashboard', 16)}
                    <span>My Portal</span>
                </a>
                <a href="#upload" class="nav-item">
                    ${LucideIcons.render('upload-cloud', 16)}
                    <span>Submit Code</span>
                </a>
                <a href="#submissions" class="nav-item">
                    ${LucideIcons.render('files', 16)}
                    <span>My Submissions</span>
                </a>

                <div class="nav-section-title">02 // SYSTEM</div>
                <a href="#settings" class="nav-item">
                    ${LucideIcons.render('settings', 16)}
                    <span>Account Profile</span>
                </a>
                <a href="#landing" class="nav-item" style="color:var(--color-accent);">
                    ${LucideIcons.render('external-link', 16)}
                    <span>Showcase Landing</span>
                </a>
            `;
        } else {
            navContainer.innerHTML = `
                <div class="nav-section-title">01 // OVERVIEW</div>
                <a href="#dashboard" class="nav-item">
                    ${LucideIcons.render('layout-dashboard', 16)}
                    <span>Dashboard</span>
                </a>
                <a href="#submissions" class="nav-item">
                    ${LucideIcons.render('files', 16)}
                    <span>Submissions</span>
                </a>
                <a href="#upload" class="nav-item">
                    ${LucideIcons.render('upload-cloud', 16)}
                    <span>Ingest File</span>
                </a>

                <div class="nav-section-title">02 // AUDIT_ENGINE</div>
                <a href="#scan" class="nav-item">
                    ${LucideIcons.render('scan', 16)}
                    <span>Plagiarism Scan</span>
                </a>
                <a href="#results" class="nav-item">
                    ${LucideIcons.render('git-compare', 16)}
                    <span>Code Diff &amp; Results</span>
                </a>
                <a href="#repository" class="nav-item">
                    ${LucideIcons.render('database', 16)}
                    <span>Local Repository</span>
                </a>
                <a href="#reports" class="nav-item">
                    ${LucideIcons.render('file-text', 16)}
                    <span>Audit Dossiers</span>
                </a>

                <div class="nav-section-title">03 // SYSTEM_OPS</div>
                <a href="#settings" class="nav-item">
                    ${LucideIcons.render('settings', 16)}
                    <span>Diagnostics &amp; Data</span>
                </a>
                <a href="#landing" class="nav-item" style="color:var(--color-accent);">
                    ${LucideIcons.render('external-link', 16)}
                    <span>Showcase Landing</span>
                </a>
            `;
        }
    },

    async handleRoute() {
        const rawHash = (window.location.hash || '').replace(/^#/, '');
        const routeKey = rawHash.split('?')[0] || 'landing';
        const route = this.routes[routeKey] || this.routes['landing'];

        const user = (window.State && State.user) || API.getUser();
        this.updateRoleNav(user);

        const sidebar = document.getElementById('sidebar');
        const topbar = document.getElementById('topbar');
        const contentBody = document.getElementById('content-body');
        const pageTitle = document.getElementById('page-title');

        if (!contentBody) return;

        if (routeKey === 'landing' || routeKey === 'login') {
            if (sidebar) sidebar.style.display = 'none';
            if (topbar) topbar.style.display = 'none';
            contentBody.style.padding = '0';
        } else {
            if (sidebar) sidebar.style.display = 'flex';
            if (topbar) topbar.style.display = 'flex';
            contentBody.style.padding = '32px';
            if (pageTitle) pageTitle.innerHTML = route.title;

            // Update active menu link
            document.querySelectorAll('.nav-item').forEach(el => {
                const target = (el.getAttribute('href') || '').replace('#', '');
                if (target === routeKey) {
                    el.classList.add('active');
                } else {
                    el.classList.remove('active');
                }
            });
        }

        // Resolve view object
        const viewObj = this.getView(route.view);
        if (viewObj && typeof viewObj.render === 'function') {
            try {
                const html = await viewObj.render();
                contentBody.innerHTML = html;

                // Post-render hooks
                if (routeKey === 'dashboard' && window.DashboardView && DashboardView.initCharts) {
                    try {
                        const stats = await API.getDashboardStats();
                        DashboardView.initCharts(stats);
                    } catch (e) {
                        DashboardView.initCharts({
                            similarity_distribution: { '0-29% (Low)': 4, '30-59% (Moderate)': 2, '60-79% (High)': 2, '80-100% (Critical)': 2 },
                            language_distribution: { 'Python': 4, 'Java': 2, 'C++': 2 }
                        });
                    }
                }

                // Render all SVG icons
                if (window.LucideIcons && LucideIcons.init) {
                    LucideIcons.init();
                }
            } catch (err) {
                console.error(`Error rendering view [${routeKey}]:`, err);
                contentBody.innerHTML = `<div class="card" style="margin:40px; border-color:var(--color-danger); color:var(--color-danger); font-family:var(--font-mono);">&gt; DIAGNOSTIC WARNING: ${err.message}</div>`;
            }
        }
    }
};
