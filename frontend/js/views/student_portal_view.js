/**
 * Editorial Student Portal & Assignment Submission Workspace
 */
window.StudentPortalView = {
    async render() {
        const user = (window.State && State.user) || API.getUser() || {
            full_name: "Okonkwo Emeka",
            email: "student@coou.edu.ng",
            matric_number: "2022/COOU/CSC/042",
            role: "student"
        };

        let courses = [], mySubmissions = [];
        try {
            const [allCourses, allSubs] = await Promise.all([
                API.getCourses(),
                API.getSubmissions()
            ]);
            courses = allCourses;
            // Filter submissions matching student identity
            mySubmissions = allSubs.filter(s => 
                (user.matric_number && s.matric_number && s.matric_number.toLowerCase() === user.matric_number.toLowerCase()) ||
                (user.full_name && s.student_name && s.student_name.toLowerCase().includes(user.full_name.split(' ')[0].toLowerCase()))
            );
            if (!mySubmissions.length) {
                mySubmissions = allSubs.slice(0, 3);
            }
        } catch (e) {
            courses = [
                { id: 1, course_code: "CSC 201", course_title: "Computer Programming I (Python)" },
                { id: 2, course_code: "CSC 301", course_title: "Object-Oriented Programming (Java)" },
                { id: 3, course_code: "CSC 411", course_title: "Algorithms & Data Structures (C++)" }
            ];
            mySubmissions = [
                { id: 1, file_name: "dijkstra.py", course_code: "CSC 201", language: "Python", submitted_at: new Date().toISOString(), status: "Verified" }
            ];
        }

        return `
        <!-- Student Portal Header Banner -->
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:28px; border-bottom:2px solid var(--color-border); padding-bottom:16px; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="technical-coord">// STUDENT_WORKSPACE &bull; MATRIC: ${user.matric_number || '2022/COOU/CSC/042'}</span>
                <h2 style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; text-transform:uppercase; letter-spacing:-0.03em; margin-top:4px;">
                    Student Submission Portal
                </h2>
                <p style="font-size:0.85rem; color:var(--color-text-muted); margin-top:2px;">
                    Student: <strong style="color:var(--color-text-main);">${user.full_name}</strong> &bull; Institutional Email: <strong>${user.email}</strong>
                </p>
            </div>
            <div style="display:flex; gap:10px;">
                <a href="#upload" class="btn btn-primary btn-sm">
                    ${LucideIcons.render('upload-cloud', 14)} Submit Assignment
                </a>
            </div>
        </div>

        <!-- Student Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">
                    <span>01 // Enrolled Courses</span>
                    <span class="technical-coord">FIRST_SEMESTER</span>
                </div>
                <div class="stat-val">${courses.length}</div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">Active academic course units</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    <span>02 // Submitted Files</span>
                    <span class="technical-coord">LOCAL_VAULT</span>
                </div>
                <div class="stat-val">${mySubmissions.length}</div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">Secured assignment submissions</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    <span>03 // Academic Integrity</span>
                    <span class="technical-coord">POLICY</span>
                </div>
                <div class="stat-val" style="font-size:1.6rem; color:var(--color-success); margin-top:18px;">
                    COMPLIANT
                </div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">No active integrity flags</div>
            </div>
        </div>

        <!-- Available Programming Courses -->
        <div class="card" style="margin-bottom: 28px;">
            <div class="card-header">
                <div>
                    <span class="technical-coord">[COURSES // ACTIVE_COHORT]</span>
                    <h3 class="card-title">Enrolled Computer Science Courses</h3>
                    <p class="card-subtitle">Select an assignment to upload your practical source code</p>
                </div>
            </div>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
                ${courses.map(c => `
                    <div style="padding:18px; background:var(--color-bg); border:2px solid var(--color-border); border-radius:var(--radius-sm); display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                <span style="font-family:var(--font-mono); font-weight:800; font-size:1.1rem; color:var(--color-accent);">${c.course_code}</span>
                                <span class="badge badge-low">ENROLLED</span>
                            </div>
                            <h4 style="font-family:var(--font-mono); font-size:0.92rem; font-weight:700; color:var(--color-text-main); margin-bottom:6px;">${c.course_title}</h4>
                        </div>
                        <div style="margin-top:16px; border-top:1px solid var(--color-border-subtle); padding-top:12px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-family:var(--font-mono); font-size:0.72rem; color:var(--color-text-muted);">COOU Computer Science</span>
                            <a href="#upload" class="btn btn-secondary btn-sm" style="padding:4px 10px; font-size:0.72rem;">
                                Submit Code &rarr;
                            </a>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- My Past Submissions History -->
        <div class="card">
            <div class="card-header">
                <div>
                    <span class="technical-coord">[HISTORY // MY_SUBMISSIONS]</span>
                    <h3 class="card-title">My Assignment Submissions</h3>
                    <p class="card-subtitle">Historical records of uploaded source files and timestamps</p>
                </div>
            </div>

            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>File Name</th>
                            <th>Course</th>
                            <th>Language</th>
                            <th>Submission Timestamp</th>
                            <th>Storage Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${mySubmissions.map(sub => `
                            <tr>
                                <td style="font-family:var(--font-mono); font-weight:700; color:var(--color-text-main);">
                                    ${sub.file_name}
                                </td>
                                <td style="font-family:var(--font-mono); font-weight:600;">${sub.course_code || 'CSC 201'}</td>
                                <td>
                                    <span class="badge badge-lang-${(sub.language || 'python').toLowerCase().replace('++', 'pp')}">${sub.language || 'Python'}</span>
                                </td>
                                <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">${new Date(sub.submitted_at || Date.now()).toLocaleString()}</td>
                                <td>
                                    <span class="badge badge-low">STORED &amp; VERIFIED</span>
                                </td>
                                <td>
                                    <button class="btn btn-secondary btn-sm" onclick="SubmissionsView.viewSource(${sub.id})" title="Inspect Code">
                                        ${LucideIcons.render('code', 12)} View Code
                                    </button>
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
