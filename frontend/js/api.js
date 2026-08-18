/**
 * COOUCodeGuard REST API Client
 */
const API = {
    // Dynamic backend URL resolution for Live Server (port 5500) and native FastAPI
    BASE_URL: (window.location.port === '5500' || window.location.port === '5501' || window.location.port === '3000' || window.location.protocol === 'file:')
        ? 'http://127.0.0.1:8001'
        : '',

    getToken() {
        return localStorage.getItem('coou_guard_token');
    },

    setToken(token) {
        localStorage.setItem('coou_guard_token', token);
    },

    clearToken() {
        localStorage.removeItem('coou_guard_token');
        localStorage.removeItem('coou_guard_user');
    },

    getUser() {
        try {
            return JSON.parse(localStorage.getItem('coou_guard_user'));
        } catch {
            return null;
        }
    },

    setUser(user) {
        localStorage.setItem('coou_guard_user', JSON.stringify(user));
    },

    async request(endpoint, options = {}) {
        let url = `${this.BASE_URL}${endpoint}`;
        const headers = options.headers || {};
        const token = this.getToken();

        if (token && !headers['Authorization']) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        if (!(options.body instanceof FormData) && !headers['Content-Type']) {
            headers['Content-Type'] = 'application/json';
        }

        const config = {
            ...options,
            headers
        };

        try {
            let response;
            try {
                response = await fetch(url, config);
            } catch (networkErr) {
                // If port 8001 failed from Live Server, try fallback to 8000
                if (this.BASE_URL === 'http://127.0.0.1:8001') {
                    this.BASE_URL = 'http://127.0.0.1:8000';
                    url = `${this.BASE_URL}${endpoint}`;
                    response = await fetch(url, config);
                } else {
                    throw networkErr;
                }
            }

            if (response.status === 401) {
                this.clearToken();
                window.location.hash = '#login';
                throw new Error('Session expired. Please log in again.');
            }

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || `Request failed with status ${response.status}`);
            }

            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            return await response.text();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    },

    // Auth
    login(email, password) {
        return this.request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },

    register(fullName, email, password, role = 'lecturer') {
        return this.request('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify({ full_name: fullName, email, password, role })
        });
    },

    forgotPassword(email) {
        return this.request('/api/auth/forgot-password', {
            method: 'POST',
            body: JSON.stringify({ email })
        });
    },

    resetPassword(email, resetCode, newPassword) {
        return this.request('/api/auth/reset-password', {
            method: 'POST',
            body: JSON.stringify({ email, reset_code: resetCode, new_password: newPassword })
        });
    },

    getMe() {
        return this.request('/api/auth/me');
    },

    // Dashboard
    getDashboardStats() {
        return this.request('/api/dashboard/statistics');
    },

    getRecentSubmissions() {
        return this.request('/api/dashboard/recent-submissions');
    },

    getRecentScans() {
        return this.request('/api/dashboard/recent-scans');
    },

    // Courses & Assignments
    getCourses() {
        return this.request('/api/courses');
    },

    createCourse(courseData) {
        return this.request('/api/courses', {
            method: 'POST',
            body: JSON.stringify(courseData)
        });
    },

    createAssignment(assignmentData) {
        return this.request('/api/courses/assignments', {
            method: 'POST',
            body: JSON.stringify(assignmentData)
        });
    },

    // Submissions
    getSubmissions(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/api/submissions${query ? '?' + query : ''}`);
    },

    getSubmission(id) {
        return this.request(`/api/submissions/${id}`);
    },

    uploadSubmission(formData) {
        return this.request('/api/submissions/upload', {
            method: 'POST',
            body: formData
        });
    },

    deleteSubmission(id) {
        return this.request(`/api/submissions/${id}`, {
            method: 'DELETE'
        });
    },

    // Scans & Comparisons
    runScan(scanData) {
        return this.request('/api/scans', {
            method: 'POST',
            body: JSON.stringify(scanData)
        });
    },

    getScans(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/api/scans${query ? '?' + query : ''}`);
    },

    getScan(id) {
        return this.request(`/api/scans/${id}`);
    },

    deleteScan(id) {
        return this.request(`/api/scans/${id}`, {
            method: 'DELETE'
        });
    },

    getComparison(id) {
        return this.request(`/api/comparisons/${id}`);
    },

    // Reports
    getReports() {
        return this.request('/api/reports');
    },

    generateReport(scanId) {
        return this.request(`/api/reports/generate/${scanId}`, {
            method: 'POST'
        });
    },

    getReportHtmlUrl(id) {
        const base = this.BASE_URL || window.location.origin;
        return `${base}/api/reports/${id}/html`;
    },

    // System
    getSystemStats() {
        return this.request('/api/system/statistics');
    },

    resetDemoData() {
        return this.request('/api/system/reset-demo-data', {
            method: 'POST'
        });
    }
};

window.API = API;
