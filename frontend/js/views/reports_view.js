/**
 * Editorial Audit Reports Archive View
 */
window.ReportsView = {
    async render() {
        const reports = await API.getReports();

        return `
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:24px; border-bottom:2px solid var(--color-border); padding-bottom:14px; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="technical-coord">// MODULE: REPORT_DOSSIER_ARCHIVE &bull; TOTAL_GENERATED: ${reports.length}</span>
                <h2 style="font-family:var(--font-mono); font-size:1.5rem; font-weight:800; text-transform:uppercase; margin-top:4px;">
                    Plagiarism Audit Reports
                </h2>
            </div>
        </div>

        <div class="card" style="padding:0; overflow:hidden;">
            <div class="table-container" style="border:none;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Dossier ID</th>
                            <th>Audit Title</th>
                            <th>Overall Match</th>
                            <th>Risk Tier</th>
                            <th>Generated Timestamp</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${reports.length ? reports.map(rep => {
                            const sim = rep.summary_data?.overall_similarity || 0;
                            const risk = rep.summary_data?.risk_level || 'Low';
                            return `
                            <tr>
                                <td style="font-family:var(--font-mono); font-weight:700; color:var(--color-accent);">#REP_${rep.id}</td>
                                <td style="font-family:var(--font-mono); font-weight:700; color:var(--color-text-main);">${rep.title}</td>
                                <td>
                                    <span style="font-family:var(--font-mono); font-size:1.1rem; font-weight:800; color:${DashboardView.getRiskColor(risk)};">
                                        ${sim}%
                                    </span>
                                </td>
                                <td>
                                    <span class="badge badge-${risk.toLowerCase()}">${risk}</span>
                                </td>
                                <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${new Date(rep.created_at).toLocaleString()}</td>
                                <td>
                                    <div style="display:flex; gap:8px;">
                                        <button class="btn btn-secondary btn-sm" onclick="ReportsView.openHtmlReport(${rep.id})">
                                            ${LucideIcons.render('printer', 12)} Dossier
                                        </button>
                                        <a href="#results?id=${rep.scan_id}" class="btn btn-primary btn-sm">
                                            ${LucideIcons.render('git-compare', 12)} Diff
                                        </a>
                                    </div>
                                </td>
                            </tr>
                            `;
                        }).join('') : `
                            <tr><td colspan="6" style="text-align:center; color:var(--color-text-muted); padding:30px; font-family:var(--font-mono);">&gt; NO ARCHIVED REPORTS FOUND.</td></tr>
                        `}
                    </tbody>
                </table>
            </div>
        </div>
        `;
    },

    openHtmlReport(reportId) {
        window.open(API.getReportHtmlUrl(reportId), '_blank');
    }
};
