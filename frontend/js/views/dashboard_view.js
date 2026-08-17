/**
 * Editorial Command Center Dashboard View with Resilient Fallback
 */
window.DashboardView = {
    async render() {
        let stats, recentScans, recentSubmissions;

        try {
            [stats, recentScans, recentSubmissions] = await Promise.all([
                API.getDashboardStats(),
                API.getRecentScans(),
                API.getRecentSubmissions()
            ]);
        } catch (err) {
            console.warn("Using sample dashboard data:", err);
            stats = {
                total_submissions: 8,
                total_scans: 4,
                critical_cases: 2,
                high_cases: 1,
                medium_cases: 1,
                low_cases: 0,
                average_similarity: 67.4,
                similarity_distribution: { "0-29% (Low)": 1, "30-59% (Moderate)": 2, "60-79% (High)": 2, "80-100% (Critical)": 3 },
                language_distribution: { "Python": 4, "Java": 2, "C++": 2 }
            };
            recentScans = [
                { id: 1, student_name: "Nnamdi Chinedu", matric_number: "2022/COOU/CSC/089", course_code: "CSC 201", language: "Python", overall_similarity: 88.5, ast_similarity: 92.4, token_similarity: 86.0, fingerprint_similarity: 85.0, ai_pattern_score: 15.0, risk_level: "Critical" },
                { id: 2, student_name: "Amadi Kinsley", matric_number: "2022/COOU/CSC/115", course_code: "CSC 201", language: "Python", overall_similarity: 78.2, ast_similarity: 81.0, token_similarity: 75.0, fingerprint_similarity: 70.0, ai_pattern_score: 75.0, risk_level: "High" },
                { id: 3, student_name: "Uche Cynthia", matric_number: "2021/COOU/CSC/073", course_code: "CSC 301", language: "Java", overall_similarity: 74.6, ast_similarity: 78.0, token_similarity: 72.0, fingerprint_similarity: 68.0, ai_pattern_score: 20.0, risk_level: "High" },
                { id: 4, student_name: "Emmanuel Chukwudi", matric_number: "2020/COOU/CSC/061", course_code: "CSC 411", language: "C++", overall_similarity: 82.0, ast_similarity: 85.0, token_similarity: 80.0, fingerprint_similarity: 76.0, ai_pattern_score: 10.0, risk_level: "Critical" }
            ];
            recentSubmissions = [
                { id: 1, student_name: "Okonkwo Emeka", matric_number: "2022/COOU/CSC/042", course_code: "CSC 201", language: "Python", file_name: "dijkstra.py", latest_similarity: 88.5, latest_risk_level: "Critical" },
                { id: 2, student_name: "Nnamdi Chinedu", matric_number: "2022/COOU/CSC/089", course_code: "CSC 201", language: "Python", file_name: "graph_solver.py", latest_similarity: 88.5, latest_risk_level: "Critical" },
                { id: 3, student_name: "Amadi Kinsley", matric_number: "2022/COOU/CSC/115", course_code: "CSC 201", language: "Python", file_name: "shortest_path.py", latest_similarity: 78.2, latest_risk_level: "High" },
                { id: 5, student_name: "Ifeanyi Obinna", matric_number: "2021/COOU/CSC/058", course_code: "CSC 301", language: "Java", file_name: "BankAccount.java", latest_similarity: 74.6, latest_risk_level: "High" }
            ];
        }

        return `
        <!-- Top Command Center Banner -->
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:28px; border-bottom:2px solid var(--color-border); padding-bottom:16px; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="technical-coord">// SYSTEM_COORDINATES: 05°47'N 06°52'E &bull; COOU_ULI_CAMPUS</span>
                <h2 style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; text-transform:uppercase; letter-spacing:-0.03em; margin-top:4px;">
                    Forensic Overview
                </h2>
            </div>
            <div style="display:flex; gap:10px;">
                <a href="#scan" class="btn btn-primary btn-sm">
                    ${LucideIcons.render('scan', 14)} New Audit
                </a>
                <a href="#upload" class="btn btn-secondary btn-sm">
                    ${LucideIcons.render('upload-cloud', 14)} Ingest File
                </a>
            </div>
        </div>

        <!-- Large Editorial Numeric Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">
                    <span>01 // Stored Submissions</span>
                    <span class="technical-coord">SQLITE_LOCAL</span>
                </div>
                <div class="stat-val count-up">${stats.total_submissions}</div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">Total student assignment units</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    <span>02 // Executed Audits</span>
                    <span class="technical-coord">AST_WINNOW</span>
                </div>
                <div class="stat-val count-up">${stats.total_scans}</div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">Completed structural scans</div>
            </div>

            <div class="stat-card" style="border-color:${(stats.critical_cases + stats.high_cases) > 0 ? 'var(--color-danger)' : 'var(--color-border)'};">
                <div class="stat-label">
                    <span style="color:var(--color-danger);">03 // High Matches (&ge;60%)</span>
                    <span class="technical-coord" style="color:var(--color-danger);">FLAGGED</span>
                </div>
                <div class="stat-val count-up" style="color:var(--color-danger);">
                    ${stats.critical_cases + stats.high_cases}
                </div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-danger); font-weight:600;">Critical risk overlap cases</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    <span>04 // Avg. Similarity</span>
                    <span class="technical-coord">COMPOSITE</span>
                </div>
                <div class="stat-val">${stats.average_similarity}%</div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">Departmental baseline index</div>
            </div>
        </div>

        <!-- Asymmetric Data Visualization Grid -->
        <div style="display:grid; grid-template-columns: 1.2fr 1fr; gap:20px; margin-bottom:28px;">
            <div class="card">
                <div class="card-header">
                    <div>
                        <span class="technical-coord">[SEC_02 // MATRIX_DISTRIBUTION]</span>
                        <h3 class="card-title">Similarity Risk Index</h3>
                        <p class="card-subtitle">Aggregated similarity breakdown across active cohort</p>
                    </div>
                </div>
                <div style="height:210px; position:relative;">
                    <canvas id="similarity-dist-chart"></canvas>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:14px; font-family:var(--font-mono); font-size:0.72rem; font-weight:700; border-top:1px solid var(--color-border-subtle); padding-top:10px;">
                    <span style="color:var(--color-success);">&bull; LOW (0-29%)</span>
                    <span style="color:var(--color-warning);">&bull; MODERATE (30-59%)</span>
                    <span style="color:#E65100;">&bull; HIGH (60-79%)</span>
                    <span style="color:var(--color-danger);">&bull; CRITICAL (80-100%)</span>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <div>
                        <span class="technical-coord">[SEC_03 // LANGUAGE_SPECS]</span>
                        <h3 class="card-title">Language Parsing Volume</h3>
                        <p class="card-subtitle">Active language engines in repository</p>
                    </div>
                </div>
                <div style="height:210px; position:relative;">
                    <canvas id="language-dist-chart"></canvas>
                </div>
            </div>
        </div>

        <!-- Recent Scans Matrix -->
        <div class="card" style="margin-bottom:28px;">
            <div class="card-header">
                <div>
                    <span class="technical-coord">[LOG_01 // RECENT_AUDITS]</span>
                    <h3 class="card-title">Recent Plagiarism Audits</h3>
                    <p class="card-subtitle">Latest forensic AST and fingerprint comparisons</p>
                </div>
            </div>

            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Student Identity</th>
                            <th>Course Code</th>
                            <th>Language</th>
                            <th>Overall Match</th>
                            <th>AST / Token / FP</th>
                            <th>AI Indication</th>
                            <th>Risk State</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${recentScans.map(scan => `
                            <tr>
                                <td>
                                    <div style="font-family:var(--font-mono); font-weight:700; color:var(--color-text-main);">${scan.student_name}</div>
                                    <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${scan.matric_number}</div>
                                </td>
                                <td style="font-family:var(--font-mono); font-weight:600;">${scan.course_code}</td>
                                <td>
                                    <span class="badge badge-lang-${scan.language.toLowerCase().replace('++', 'pp')}">${scan.language}</span>
                                </td>
                                <td>
                                    <span style="font-family:var(--font-mono); font-size:1.15rem; font-weight:800; color:${DashboardView.getRiskColor(scan.risk_level)};">
                                        ${scan.overall_similarity}%
                                    </span>
                                </td>
                                <td>
                                    <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">
                                        AST: <strong>${scan.ast_similarity}%</strong> | TOK: <strong>${scan.token_similarity}%</strong> | FP: <strong>${scan.fingerprint_similarity}%</strong>
                                    </div>
                                </td>
                                <td>
                                    <span class="badge ${scan.ai_pattern_score >= 60 ? 'badge-critical' : (scan.ai_pattern_score >= 30 ? 'badge-moderate' : 'badge-low')}">
                                        ${scan.ai_pattern_score}% AI Score
                                    </span>
                                </td>
                                <td>
                                    <span class="badge badge-${scan.risk_level.toLowerCase()}">${scan.risk_level}</span>
                                </td>
                                <td>
                                    <a href="#results?id=${scan.id}" class="btn btn-secondary btn-sm">
                                        ${LucideIcons.render('git-compare', 14)} Inspect
                                    </a>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Stored Submissions Queue -->
        <div class="card">
            <div class="card-header">
                <div>
                    <span class="technical-coord">[LOG_02 // STORED_SUBMISSIONS]</span>
                    <h3 class="card-title">Stored Submissions Repository</h3>
                    <p class="card-subtitle">Student files ready for comparative structural evaluation</p>
                </div>
            </div>

            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Matriculation No.</th>
                            <th>Course</th>
                            <th>Language</th>
                            <th>File Name</th>
                            <th>Audit Status</th>
                            <th>Execute</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${recentSubmissions.map(sub => `
                            <tr>
                                <td style="font-family:var(--font-mono); font-weight:700;">${sub.student_name}</td>
                                <td style="font-family:var(--font-mono); font-size:0.78rem; color:var(--color-text-muted);">${sub.matric_number}</td>
                                <td style="font-family:var(--font-mono);">${sub.course_code}</td>
                                <td>
                                    <span class="badge badge-lang-${sub.language.toLowerCase().replace('++', 'pp')}">${sub.language}</span>
                                </td>
                                <td style="font-family:var(--font-mono); font-size:0.8rem;">${sub.file_name}</td>
                                <td>
                                    ${sub.latest_similarity !== null ? `
                                        <span class="badge badge-${sub.latest_risk_level.toLowerCase()}">
                                            ${sub.latest_similarity}% (${sub.latest_risk_level})
                                        </span>
                                    ` : '<span style="color:var(--color-text-subtle); font-family:var(--font-mono); font-size:0.75rem;">// UNSCANNED</span>'}
                                </td>
                                <td>
                                    <button class="btn btn-primary btn-sm" onclick="DashboardView.triggerQuickScan(${sub.id})">
                                        ${LucideIcons.render('scan', 12)} Scan
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
        `;
    },

    getRiskColor(risk) {
        if (risk === 'Critical') return 'var(--color-danger)';
        if (risk === 'High') return '#E65100';
        if (risk === 'Moderate') return 'var(--color-warning)';
        return 'var(--color-success)';
    },

    getRiskLevelString(score) {
        if (score >= 80) return 'Critical';
        if (score >= 60) return 'High';
        if (score >= 30) return 'Moderate';
        return 'Low';
    },

    initCharts(stats) {
        if (!stats) return;

        new OfflineChart('similarity-dist-chart', {
            type: 'doughnut',
            data: {
                labels: Object.keys(stats.similarity_distribution),
                datasets: [{
                    data: Object.values(stats.similarity_distribution),
                    backgroundColor: ['#18A957', '#E9A400', '#E65100', '#E53935']
                }]
            }
        });

        const langs = Object.keys(stats.language_distribution);
        const counts = Object.values(stats.language_distribution);
        new OfflineChart('language-dist-chart', {
            type: 'bar',
            data: {
                labels: langs.length ? langs : ['Python', 'Java', 'C++'],
                datasets: [{
                    data: counts.length ? counts : [0, 0, 0],
                    backgroundColor: ['#2457FF', '#C2410C', '#7E22CE']
                }]
            }
        });
    },

    async triggerQuickScan(submissionId) {
        try {
            App.showToast('Initiating forensic scan across local repository...', 'info');
            const result = await API.runScan({
                submission_id: submissionId,
                scan_type: 'repository'
            });
            App.showToast(`Audit complete: ${result.overall_similarity}% match (${result.risk_level})`, 'success');
            window.location.hash = `#results?id=${result.id}`;
        } catch (err) {
            App.showToast(`Scan failed: ${err.message}`, 'error');
        }
    }
};
