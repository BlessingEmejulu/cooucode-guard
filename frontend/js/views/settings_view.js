/**
 * Editorial Settings & System Diagnostics View
 */
window.SettingsView = {
    async render() {
        const stats = await API.getSystemStats();
        const user = State.user || API.getUser() || {};

        return `
        <div style="max-width: 960px; margin: 0 auto;">
            <div style="margin-bottom: 24px; border-bottom: 2px solid var(--color-border); padding-bottom: 14px;">
                <span class="technical-coord">// MODULE: SYSTEM_DIAGNOSTICS &bull; LOCALHOST_ENGINE</span>
                <h2 style="font-family:var(--font-mono); font-size:1.5rem; font-weight:800; text-transform:uppercase; margin-top:4px;">
                    Diagnostics &amp; System Configuration
                </h2>
            </div>

            <!-- Lecturer Profile Card -->
            <div class="card" style="margin-bottom: 24px;">
                <div class="card-header">
                    <div>
                        <span class="technical-coord">// USER_IDENTITY</span>
                        <h3 class="card-title">Lecturer Profile Credentials</h3>
                    </div>
                    <span class="badge badge-low">ACTIVE_SESSION</span>
                </div>

                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 24px; font-family:var(--font-mono);">
                    <div>
                        <label class="form-label">Full Name</label>
                        <div style="font-weight:700; color:var(--color-text-main); font-size:1.05rem;">${user.full_name || 'Dr. Chukwuma Eze'}</div>
                    </div>
                    <div>
                        <label class="form-label">Email Identifier</label>
                        <div style="color:var(--color-text-muted);">${user.email || 'lecturer@coou.edu.ng'}</div>
                    </div>
                    <div>
                        <label class="form-label">Affiliation</label>
                        <div style="font-weight:700; color:var(--color-accent);">${stats.institution}</div>
                    </div>
                    <div>
                        <label class="form-label">Role Access Tier</label>
                        <div style="text-transform:uppercase; font-weight:700;">${user.role || 'Lecturer'}</div>
                    </div>
                </div>
            </div>

            <!-- Offline Storage & System Health Metrics -->
            <div class="card" style="margin-bottom: 24px;">
                <div class="card-header">
                    <div>
                        <span class="technical-coord">// STORAGE_METRICS</span>
                        <h3 class="card-title">Local Engine &amp; SQLite State</h3>
                    </div>
                    <span class="badge" style="background:var(--color-bg); font-weight:700;">100% OFFLINE</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px;">
                    <div style="padding:18px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--color-text-muted); font-weight:700; text-transform:uppercase;">Database Engine</div>
                        <div style="font-family:var(--font-mono); font-size:1.35rem; font-weight:800; color:var(--color-text-main); margin:4px 0;">${stats.database_engine}</div>
                        <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-subtle);">Size: ${stats.database_size_kb} KB</div>
                    </div>

                    <div style="padding:18px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--color-text-muted); font-weight:700; text-transform:uppercase;">Submissions Storage</div>
                        <div style="font-family:var(--font-mono); font-size:1.35rem; font-weight:800; color:var(--color-text-main); margin:4px 0;">${stats.counts.submissions} Files</div>
                        <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-subtle);">Size: ${stats.submissions_storage_kb} KB</div>
                    </div>

                    <div style="padding:18px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--color-text-muted); font-weight:700; text-transform:uppercase;">Plagiarism Audits</div>
                        <div style="font-family:var(--font-mono); font-size:1.35rem; font-weight:800; color:var(--color-text-main); margin:4px 0;">${stats.counts.scans} Scans</div>
                        <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-subtle);">Reports: ${stats.counts.reports}</div>
                    </div>
                </div>

                <div style="padding:14px 18px; background:var(--color-bg); border:1px solid var(--color-border); font-family:var(--font-mono); font-size:0.78rem; color:var(--color-text-muted);">
                    <strong>[DATA SOVEREIGNTY PROTOCOL]:</strong> All code tokens, AST representations, and audit dossiers are stored locally on SQLite and local NVMe/SSD drive. Zero network packets are dispatched externally.
                </div>
            </div>

            <!-- Maintenance & Demo Data -->
            <div class="card" style="border-color:var(--color-danger);">
                <div class="card-header">
                    <div>
                        <span class="technical-coord" style="color:var(--color-danger);">// MAINTENANCE</span>
                        <h3 class="card-title" style="color:var(--color-danger);">Reset &amp; Reload Demo Corpus</h3>
                    </div>
                </div>

                <p style="font-size:0.85rem; color:var(--color-text-muted); margin-bottom:18px;">
                    Restore the out-of-the-box demonstration dataset with sample Python, Java, and C++ submissions (featuring pre-scanned plagiarism and AI-generated cases).
                </p>

                <button class="btn btn-secondary" style="border-color:var(--color-danger); color:var(--color-danger);" onclick="SettingsView.resetDemoData()">
                    ${LucideIcons.render('refresh-cw', 14)} Reset &amp; Reload Demo Corpus
                </button>
            </div>
        </div>
        `;
    },

    async resetDemoData() {
        if (!confirm('Are you sure you want to reset and reload the sample demonstration dataset?')) return;
        try {
            App.showToast('Resetting database and seeding demo data...', 'info');
            await API.resetDemoData();
            App.showToast('Demo data successfully restored!', 'success');
            window.location.hash = '#dashboard';
        } catch (err) {
            App.showToast(`Reset failed: ${err.message}`, 'error');
        }
    }
};
