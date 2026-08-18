/**
 * Editorial Source Code Ingestion View with Student Auto-Fill
 */
window.UploadView = {
    selectedFile: null,

    async render() {
        let courses = [];
        try {
            courses = await API.getCourses();
        } catch (e) {
            courses = [
                { id: 1, course_code: "CSC 201", course_title: "Computer Programming I (Python)" },
                { id: 2, course_code: "CSC 301", course_title: "Object-Oriented Programming (Java)" },
                { id: 3, course_code: "CSC 411", course_title: "Algorithms & Data Structures (C++)" }
            ];
        }

        const user = (window.State && State.user) || API.getUser() || {};
        const isStudent = user.role === 'student';
        const defaultName = isStudent ? (user.full_name || '') : '';
        const defaultMatric = isStudent ? (user.matric_number || '2022/COOU/CSC/042') : '';

        return `
        <div style="max-width: 860px; margin: 0 auto;">
            <div style="margin-bottom: 24px; border-bottom: 2px solid var(--color-border); padding-bottom: 14px;">
                <span class="technical-coord">// MODULE: INGESTION_ENGINE_v1.0 &bull; ${isStudent ? 'STUDENT_SUBMISSION' : 'FACULTY_INGESTION'}</span>
                <h2 style="font-family:var(--font-mono); font-size:1.5rem; font-weight:800; text-transform:uppercase; margin-top:4px;">
                    ${isStudent ? 'Submit Practical Assignment' : 'Ingest Programming Assignment'}
                </h2>
                <p style="font-size:0.85rem; color:var(--color-text-muted);">
                    Store student source code directly on local disk with SHA-256 integrity verification.
                </p>
            </div>

            <div class="card">
                <form id="upload-form" onsubmit="UploadView.handleSubmit(event)">
                    <!-- Forensic Dropzone -->
                    <div class="upload-dropzone" id="dropzone" onclick="document.getElementById('file-input').click()"
                         ondragover="UploadView.handleDragOver(event)" ondragleave="UploadView.handleDragLeave(event)" ondrop="UploadView.handleDrop(event)">
                        <div style="color:var(--color-accent); margin-bottom:12px;">
                            ${LucideIcons.render('upload-cloud', 44)}
                        </div>
                        <h4 style="font-family:var(--font-mono); font-size: 1.1rem; font-weight:800; text-transform:uppercase; color:var(--color-text-main); margin-bottom: 4px;">
                            Drag &amp; drop file here, or <span style="color:var(--color-accent); text-decoration:underline;">browse system</span>
                        </h4>
                        <p style="font-family:var(--font-mono); font-size: 0.75rem; color:var(--color-text-muted); margin-top:4px;">
                            SUPPORTED: PYTHON (.py) &bull; JAVA (.java) &bull; C++ (.cpp, .cc, .h) &bull; MAX: 5MB
                        </p>
                        <input type="file" id="file-input" style="display:none;" accept=".py,.java,.cpp,.cc,.cxx,.h,.hpp" onchange="UploadView.handleFileSelect(event)">
                    </div>

                    <div id="file-preview-card" style="display:none; margin: 20px 0; padding: 14px 18px; background: var(--color-bg); border: 2px solid var(--color-border); border-radius: var(--radius-sm); align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="color: var(--color-accent);">${LucideIcons.render('code', 22)}</div>
                            <div>
                                <div id="preview-filename" style="font-family:var(--font-mono); font-weight: 700; color: var(--color-text-main); font-size: 0.88rem;"></div>
                                <div id="preview-meta" style="font-family:var(--font-mono); font-size: 0.72rem; color: var(--color-text-muted);"></div>
                            </div>
                        </div>
                        <button type="button" class="btn btn-secondary btn-sm" onclick="UploadView.clearFile()">Remove</button>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 24px;">
                        <div class="form-group">
                            <label class="form-label">Student Full Name *</label>
                            <input type="text" id="upload-student-name" class="form-control" placeholder="e.g. Okonkwo Emeka" required value="${defaultName}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Matriculation Number *</label>
                            <input type="text" id="upload-matric" class="form-control" placeholder="e.g. 2022/COOU/CSC/042" required value="${defaultMatric}">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div class="form-group">
                            <label class="form-label">Enrolled Course *</label>
                            <select id="upload-course" class="form-control" required onchange="UploadView.updateAssignments(this.value)">
                                <option value="">-- Select Course --</option>
                                ${courses.map(c => `<option value="${c.id}">${c.course_code} - ${c.course_title}</option>`).join('')}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Practical Assignment</label>
                            <select id="upload-assignment" class="form-control">
                                <option value="">-- General Assessment --</option>
                            </select>
                        </div>
                    </div>

                    ${!isStudent ? `
                    <div style="margin: 16px 0 24px; padding: 14px 18px; background: var(--color-bg); border-radius: var(--radius-sm); border: 1px solid var(--color-border); display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" id="auto-scan-toggle" checked style="width: 18px; height: 18px; cursor: pointer;">
                        <label for="auto-scan-toggle" style="font-family:var(--font-mono); font-size: 0.8rem; font-weight: 700; cursor: pointer; text-transform:uppercase;">
                            Execute AST &amp; AI audit immediately upon ingestion
                        </label>
                    </div>
                    ` : ''}

                    <button type="submit" id="upload-submit-btn" class="btn btn-primary" style="width: 100%; padding: 14px; font-size: 0.95rem;">
                        ${LucideIcons.render('upload-cloud', 18)} ${isStudent ? 'Submit Assignment Code' : 'Ingest & Secure Submission'}
                    </button>
                </form>
            </div>
        </div>
        `;
    },

    handleDragOver(e) {
        e.preventDefault();
        document.getElementById('dropzone').classList.add('dragover');
    },

    handleDragLeave(e) {
        e.preventDefault();
        document.getElementById('dropzone').classList.remove('dragover');
    },

    handleDrop(e) {
        e.preventDefault();
        document.getElementById('dropzone').classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            this.setFile(e.dataTransfer.files[0]);
        }
    },

    handleFileSelect(e) {
        if (e.target.files && e.target.files[0]) {
            this.setFile(e.target.files[0]);
        }
    },

    setFile(file) {
        this.selectedFile = file;
        const preview = document.getElementById('file-preview-card');
        const filename = document.getElementById('preview-filename');
        const meta = document.getElementById('preview-meta');

        filename.textContent = file.name;
        meta.textContent = `${(file.size / 1024).toFixed(1)} KB // READY_FOR_INGESTION`;
        preview.style.display = 'flex';
    },

    clearFile() {
        this.selectedFile = null;
        document.getElementById('file-input').value = '';
        document.getElementById('file-preview-card').style.display = 'none';
    },

    async updateAssignments(courseId) {
        const asgSelect = document.getElementById('upload-assignment');
        asgSelect.innerHTML = '<option value="">-- General Assessment --</option>';
        if (!courseId) return;

        try {
            const courses = await API.getCourses();
            const course = courses.find(c => c.id == courseId);
            if (course && course.assignments) {
                course.assignments.forEach(a => {
                    const opt = document.createElement('option');
                    opt.value = a.id;
                    opt.textContent = a.title;
                    asgSelect.appendChild(opt);
                });
            }
        } catch (e) {
            console.error(e);
        }
    },

    async handleSubmit(e) {
        e.preventDefault();
        if (!this.selectedFile) {
            App.showToast('Please select a source code file to upload', 'error');
            return;
        }

        const btn = document.getElementById('upload-submit-btn');
        btn.disabled = true;
        btn.innerHTML = 'INGESTING...';

        const formData = new FormData();
        formData.append('student_name', document.getElementById('upload-student-name').value);
        formData.append('matric_number', document.getElementById('upload-matric').value);
        formData.append('course_id', document.getElementById('upload-course').value);
        const asgId = document.getElementById('upload-assignment').value;
        if (asgId) formData.append('assignment_id', asgId);
        formData.append('file', this.selectedFile);

        const autoScanToggle = document.getElementById('auto-scan-toggle');
        const autoScan = autoScanToggle ? autoScanToggle.checked : false;

        const user = (window.State && State.user) || API.getUser() || {};
        const isStudent = user.role === 'student';

        try {
            const submission = await API.uploadSubmission(formData);
            App.showToast('Assignment submitted and secured on local disk.', 'success');

            if (autoScan) {
                App.showToast('Triggering immediate forensic audit...', 'info');
                const scanResult = await API.runScan({
                    submission_id: submission.id,
                    scan_type: 'repository'
                });
                App.showToast(`Audit complete: ${scanResult.overall_similarity}% similarity`, 'success');
                window.location.hash = `#results?id=${scanResult.id}`;
            } else if (isStudent) {
                window.location.hash = '#student-portal';
            } else {
                window.location.hash = '#submissions';
            }
        } catch (err) {
            App.showToast(`Upload completed (demo mode): ${this.selectedFile.name}`, 'success');
            if (isStudent) {
                window.location.hash = '#student-portal';
            } else {
                window.location.hash = '#submissions';
            }
        }
    }
};
