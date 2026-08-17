/**
 * Editorial Submissions Directory View
 */
window.SubmissionsView = {
    async render() {
        const [submissions, courses] = await Promise.all([
            API.getSubmissions(),
            API.getCourses()
        ]);

        return `
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:24px; border-bottom:2px solid var(--color-border); padding-bottom:14px; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="technical-coord">// MODULE: SUBMISSION_INDEX_v1.0 &bull; TOTAL_COUNT: ${submissions.length}</span>
                <h2 style="font-family:var(--font-mono); font-size:1.5rem; font-weight:800; text-transform:uppercase; margin-top:4px;">
                    Stored Submissions
                </h2>
            </div>
            <a href="#upload" class="btn btn-primary btn-sm">
                ${LucideIcons.render('upload-cloud', 14)} Ingest File
            </a>
        </div>

        <div class="card" style="margin-bottom: 24px; padding:20px;">
            <div style="display: flex; gap: 14px; flex-wrap: wrap; align-items: center;">
                <div style="flex: 1; min-width: 260px;">
                    <input type="text" id="sub-search-input" class="form-control" placeholder="Search student name or matric..." oninput="SubmissionsView.handleFilter()">
                </div>
                <select id="sub-course-filter" class="form-control" style="width: 220px;" onchange="SubmissionsView.handleFilter()">
                    <option value="">All Courses</option>
                    ${courses.map(c => `<option value="${c.id}">${c.course_code} - ${c.course_title}</option>`).join('')}
                </select>
                <select id="sub-lang-filter" class="form-control" style="width: 170px;" onchange="SubmissionsView.handleFilter()">
                    <option value="">All Languages</option>
                    <option value="Python">Python</option>
                    <option value="Java">Java</option>
                    <option value="C++">C++</option>
                </select>
            </div>
        </div>

        <div class="card" style="padding:0; overflow:hidden;">
            <div class="table-container" style="border:none;">
                <table class="data-table" id="submissions-table">
                    <thead>
                        <tr>
                            <th>Student Identity</th>
                            <th>Course</th>
                            <th>Language</th>
                            <th>File Name</th>
                            <th>Ingested At</th>
                            <th>Plagiarism State</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="submissions-table-body">
                        ${SubmissionsView.renderTableRows(submissions)}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Forensic Code Viewer Modal -->
        <div class="modal-overlay" id="code-modal">
            <div class="modal-dialog" style="max-width: 900px;">
                <div class="modal-header">
                    <div>
                        <span class="technical-coord">// SOURCE_PREVIEW</span>
                        <h3 class="card-title" id="modal-title">Source Code Preview</h3>
                        <p class="card-subtitle" id="modal-subtitle">File Details</p>
                    </div>
                    <button class="btn btn-secondary btn-icon" onclick="SubmissionsView.closeModal()">
                        &times;
                    </button>
                </div>
                <div class="modal-body" style="background:var(--color-terminal-bg); padding:0; max-height:550px; overflow-y:auto;">
                    <pre style="margin:0; padding:24px; font-family:var(--font-mono); font-size:0.84rem; color:#E6E6E6; line-height:1.65;"><code id="modal-code-content"></code></pre>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary btn-sm" onclick="SubmissionsView.closeModal()">Close Window</button>
                </div>
            </div>
        </div>
        `;
    },

    renderTableRows(submissions) {
        if (!submissions || !submissions.length) {
            return `<tr><td colspan="7" style="text-align:center; color:var(--color-text-muted); padding:30px; font-family:var(--font-mono);">&gt; NO STORED SUBMISSIONS FOUND.</td></tr>`;
        }

        return submissions.map(sub => `
            <tr>
                <td>
                    <div style="font-family:var(--font-mono); font-weight:700; color:var(--color-text-main);">${sub.student_name}</div>
                    <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${sub.matric_number}</div>
                </td>
                <td>
                    <div style="font-family:var(--font-mono); font-weight:600;">${sub.course_code || 'N/A'}</div>
                    <div style="font-size:0.72rem; color:var(--color-text-muted);">${sub.assignment_title || ''}</div>
                </td>
                <td>
                    <span class="badge badge-lang-${sub.language.toLowerCase().replace('++', 'pp')}">${sub.language}</span>
                </td>
                <td style="font-family:var(--font-mono); font-size:0.8rem;">${sub.file_name}</td>
                <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${new Date(sub.submitted_at).toLocaleDateString()}</td>
                <td>
                    ${sub.latest_scan_similarity !== null ? `
                        <a href="#results?id=${sub.latest_scan_id}" style="text-decoration:none;">
                            <span class="badge badge-${DashboardView.getRiskLevelString(sub.latest_scan_similarity).toLowerCase()}">
                                ${sub.latest_scan_similarity}% Match
                            </span>
                        </a>
                    ` : '<span style="color:var(--color-text-subtle); font-family:var(--font-mono); font-size:0.75rem;">// UNSCANNED</span>'}
                </td>
                <td>
                    <div style="display:flex; gap:6px;">
                        <button class="btn btn-primary btn-sm" onclick="SubmissionsView.runScan(${sub.id})" title="Run Scan">
                            ${LucideIcons.render('scan', 12)} Scan
                        </button>
                        <button class="btn btn-secondary btn-sm btn-icon" onclick="SubmissionsView.viewSource(${sub.id})" title="View Code">
                            ${LucideIcons.render('code', 12)}
                        </button>
                        <button class="btn btn-secondary btn-sm btn-icon" style="color:var(--color-danger);" onclick="SubmissionsView.deleteSubmission(${sub.id})" title="Delete">
                            ${LucideIcons.render('trash', 12)}
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    },

    async handleFilter() {
        const search = document.getElementById('sub-search-input').value;
        const courseId = document.getElementById('sub-course-filter').value;
        const language = document.getElementById('sub-lang-filter').value;

        const params = {};
        if (search) params.search = search;
        if (courseId) params.course_id = courseId;
        if (language) params.language = language;

        try {
            const data = await API.getSubmissions(params);
            document.getElementById('submissions-table-body').innerHTML = this.renderTableRows(data);
        } catch (err) {
            console.error(err);
        }
    },

    async viewSource(id) {
        try {
            const data = await API.getSubmission(id);
            document.getElementById('modal-title').textContent = `${data.student_name} (${data.matric_number})`;
            document.getElementById('modal-subtitle').textContent = `FILE: ${data.file_name} // LANG: ${data.language} // COURSE: ${data.course_code}`;
            document.getElementById('modal-code-content').textContent = data.source_code;
            document.getElementById('code-modal').classList.add('active');
        } catch (err) {
            App.showToast('Could not load source code', 'error');
        }
    },

    closeModal() {
        document.getElementById('code-modal').classList.remove('active');
    },

    async runScan(id) {
        try {
            App.showToast('Scanning submission against repository...', 'info');
            const result = await API.runScan({ submission_id: id, scan_type: 'repository' });
            App.showToast(`Scan complete: ${result.overall_similarity}% similarity`, 'success');
            window.location.hash = `#results?id=${result.id}`;
        } catch (err) {
            App.showToast(`Scan failed: ${err.message}`, 'error');
        }
    },

    async deleteSubmission(id) {
        if (!confirm('Permanently delete this submission from local database and filesystem?')) return;
        try {
            await API.deleteSubmission(id);
            App.showToast('Submission deleted successfully', 'success');
            this.handleFilter();
        } catch (err) {
            App.showToast(`Delete failed: ${err.message}`, 'error');
        }
    }
};
