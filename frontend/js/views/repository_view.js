/**
 * Editorial Local Repository Browser View with Fallback
 */
window.RepositoryView = {
    async render() {
        let submissions = [];
        try {
            submissions = await API.getSubmissions();
        } catch (e) {
            submissions = [
                { id: 1, student_name: "Okonkwo Emeka", matric_number: "2022/COOU/CSC/042", course_code: "CSC 201", language: "Python", file_name: "dijkstra.py", source_hash: "a4f89d1b092ce8182b81093847291a8291837492019284728918237498127394", submitted_at: new Date().toISOString() },
                { id: 2, student_name: "Nnamdi Chinedu", matric_number: "2022/COOU/CSC/089", course_code: "CSC 201", language: "Python", file_name: "graph_solver.py", source_hash: "b7c29e847192a837482910394857291837492019284728918237498127394827", submitted_at: new Date().toISOString() },
                { id: 3, student_name: "Amadi Kinsley", matric_number: "2022/COOU/CSC/115", course_code: "CSC 201", language: "Python", file_name: "shortest_path.py", source_hash: "c9d3847291837492019284728918237498127394827182938472819283746591", submitted_at: new Date().toISOString() }
            ];
        }

        return `
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:24px; border-bottom:2px solid var(--color-border); padding-bottom:14px; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="technical-coord">// MODULE: LOCAL_REPOSITORY_BROWSER &bull; TOTAL_UNITS: ${submissions.length}</span>
                <h2 style="font-family:var(--font-mono); font-size:1.5rem; font-weight:800; text-transform:uppercase; margin-top:4px;">
                    Local Repository Corpus
                </h2>
            </div>
            <a href="#upload" class="btn btn-primary btn-sm">
                ${LucideIcons.render('upload-cloud', 14)} Add Submission
            </a>
        </div>

        <div class="card" style="padding:0; overflow:hidden;">
            <div class="table-container" style="border:none;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Matriculation No.</th>
                            <th>Course</th>
                            <th>Language</th>
                            <th>File Name</th>
                            <th>SHA-256 Checksum</th>
                            <th>Timestamp</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${submissions.map(sub => `
                            <tr>
                                <td style="font-family:var(--font-mono); font-weight:700;">${sub.student_name}</td>
                                <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${sub.matric_number}</td>
                                <td style="font-family:var(--font-mono); font-weight:600;">${sub.course_code || 'N/A'}</td>
                                <td>
                                    <span class="badge badge-lang-${sub.language.toLowerCase().replace('++', 'pp')}">${sub.language}</span>
                                </td>
                                <td style="font-family:var(--font-mono); font-size:0.8rem;">${sub.file_name}</td>
                                <td style="font-family:var(--font-mono); font-size:0.72rem; color:var(--color-text-subtle);" title="${sub.source_hash}">
                                    ${(sub.source_hash || 'hash').substring(0, 12)}...
                                </td>
                                <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${new Date(sub.submitted_at).toLocaleDateString()}</td>
                                <td>
                                    <div style="display:flex; gap:6px;">
                                        <button class="btn btn-secondary btn-sm" onclick="SubmissionsView.viewSource(${sub.id})" title="View Code">
                                            ${LucideIcons.render('code', 12)} View
                                        </button>
                                        <button class="btn btn-primary btn-sm" onclick="SubmissionsView.runScan(${sub.id})" title="Plagiarism Scan">
                                            ${LucideIcons.render('scan', 12)} Scan
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
        `;
    }
};
