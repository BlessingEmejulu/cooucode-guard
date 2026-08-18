/**
 * Editorial Technical Auth View with Lecturer & Student Portals
 */
window.AuthView = {
    currentPortal: 'lecturer', // 'lecturer' | 'student'

    render() {
        return `
        <div style="min-height: 100vh; width: 100vw; display: flex; align-items: center; justify-content: center; background: var(--color-bg); padding: 20px;">
            <div style="width: 100%; max-width: 500px; background: var(--color-surface); border: 2px solid var(--color-border); border-radius: var(--radius-sm); padding: 36px 32px; box-shadow: var(--shadow-lg);">
                
                <!-- Brand & Header -->
                <div style="margin-bottom: 20px; border-bottom: 2px solid var(--color-border); padding-bottom: 16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span class="brand-badge">CG</span>
                        <span class="technical-coord">// SEC_AUTH_v2.0</span>
                    </div>
                    <h2 style="font-family:var(--font-mono); font-size:1.45rem; font-weight:800; text-transform:uppercase; letter-spacing:-0.03em;">
                        COOUCodeGuard
                    </h2>
                    <p style="font-size:0.8rem; color:var(--color-text-muted); margin-top:2px;">
                        Chukwuemeka Odumegwu Ojukwu University &bull; Uli Campus<br>
                        <strong>Source Code Integrity &amp; Forensic System</strong>
                    </p>
                </div>

                <!-- Role / Portal Selector Tabs -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:20px; background:var(--color-bg); padding:4px; border:2px solid var(--color-border); border-radius:var(--radius-sm);">
                    <button type="button" id="tab-lecturer" class="btn btn-sm ${this.currentPortal === 'lecturer' ? 'btn-primary' : 'btn-secondary'}" style="box-shadow:none;" onclick="AuthView.switchPortal('lecturer')">
                        Lecturer Portal
                    </button>
                    <button type="button" id="tab-student" class="btn btn-sm ${this.currentPortal === 'student' ? 'btn-primary' : 'btn-secondary'}" style="box-shadow:none;" onclick="AuthView.switchPortal('student')">
                        Student Portal
                    </button>
                </div>

                <div id="auth-error" style="display:none; background:var(--color-danger-bg); color:var(--color-danger); padding:10px 14px; border:1px solid var(--color-danger); font-family:var(--font-mono); font-size:0.8rem; margin-bottom:18px;"></div>
                <div id="auth-success" style="display:none; background:var(--color-success-bg); color:var(--color-success); padding:10px 14px; border:1px solid var(--color-success); font-family:var(--font-mono); font-size:0.8rem; margin-bottom:18px;"></div>

                <!-- 01. LOGIN FORM -->
                <div id="login-form-container">
                    <form id="login-form" onsubmit="AuthView.handleLogin(event)">
                        <div class="form-group">
                            <label class="form-label" id="login-email-label">
                                ${this.currentPortal === 'student' ? 'Student Institutional Email' : 'Lecturer Institutional Email'}
                            </label>
                            <input type="email" id="login-email" class="form-control" placeholder="user@coou.edu.ng" required value="${this.currentPortal === 'student' ? 'student@coou.edu.ng' : 'lecturer@coou.edu.ng'}">
                        </div>
                        <div class="form-group">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <label class="form-label" style="margin-bottom:0;">Password</label>
                                <a href="javascript:void(0)" onclick="AuthView.setMode('forgot')" style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-accent); text-decoration:none; font-weight:600;">
                                    Forgot Password?
                                </a>
                            </div>
                            <input type="password" id="login-password" class="form-control" placeholder="Password" required value="${this.currentPortal === 'student' ? 'cooustudent2026' : 'coouguard2026'}">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 13px; font-size: 0.9rem;">
                            Authenticate ${this.currentPortal === 'student' ? 'Student' : 'Lecturer'} Session &rarr;
                        </button>
                    </form>

                    <!-- Fast Auto-Fill Verification Box -->
                    <div style="margin-top: 20px; padding: 12px 14px; background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size: 0.7rem; font-weight: 700; color: var(--color-text-muted); text-transform: uppercase; margin-bottom: 6px;">
                            Quick Demo Verification
                        </div>
                        <div style="display:flex; gap:8px;">
                            <button type="button" class="btn btn-secondary btn-sm" style="flex:1; font-size:0.72rem; padding:5px 8px;" onclick="AuthView.fillLecturerDemo()">
                                Fill Lecturer
                            </button>
                            <button type="button" class="btn btn-secondary btn-sm" style="flex:1; font-size:0.72rem; padding:5px 8px;" onclick="AuthView.fillStudentDemo()">
                                Fill Student
                            </button>
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 18px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--color-text-muted);">
                        Need an account? <a href="javascript:void(0)" onclick="AuthView.setMode('register')" style="color: var(--color-accent); font-weight: 700; text-decoration: none;">Register here</a>
                    </div>
                </div>

                <!-- 02. REGISTER FORM -->
                <div id="register-form-container" style="display: none;">
                    <form id="register-form" onsubmit="AuthView.handleRegister(event)">
                        <div class="form-group">
                            <label class="form-label">Full Name &amp; Title</label>
                            <input type="text" id="reg-name" class="form-control" placeholder="e.g. Okonkwo Emeka" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Account Role</label>
                            <select id="reg-role" class="form-control" onchange="AuthView.handleRoleChange(this.value)">
                                <option value="lecturer">Lecturer / Faculty</option>
                                <option value="student">Undergraduate Student</option>
                                <option value="admin">Department Administrator</option>
                            </select>
                        </div>
                        <div class="form-group" id="reg-matric-group" style="display:none;">
                            <label class="form-label">Matriculation Number *</label>
                            <input type="text" id="reg-matric" class="form-control" placeholder="e.g. 2022/COOU/CSC/042">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Institutional Email</label>
                            <input type="email" id="reg-email" class="form-control" placeholder="e.g. e.okonkwo@coou.edu.ng" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Password (min. 6 characters)</label>
                            <input type="password" id="reg-password" class="form-control" minlength="6" placeholder="Choose a password" required>
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 13px; font-size: 0.9rem;">
                            Create Account &rarr;
                        </button>
                    </form>
                    <div style="text-align: center; margin-top: 18px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--color-text-muted);">
                        Already registered? <a href="javascript:void(0)" onclick="AuthView.setMode('login')" style="color: var(--color-accent); font-weight: 700; text-decoration: none;">Sign in</a>
                    </div>
                </div>

                <!-- 03. FORGOT / RESET PASSWORD FORM -->
                <div id="forgot-form-container" style="display: none;">
                    <div id="forgot-step-1">
                        <div style="margin-bottom:16px;">
                            <span class="technical-coord">// CREDENTIAL_RECOVERY_STEP_01</span>
                            <h3 style="font-family:var(--font-mono); font-size:1.05rem; font-weight:700; text-transform:uppercase; margin-top:2px;">
                                Recover Account Password
                            </h3>
                            <p style="font-size:0.8rem; color:var(--color-text-muted); margin-top:4px;">
                                Enter your institutional email to generate an offline security recovery token.
                            </p>
                        </div>

                        <form onsubmit="AuthView.handleRequestReset(event)">
                            <div class="form-group">
                                <label class="form-label">Institutional Email</label>
                                <input type="email" id="forgot-email" class="form-control" placeholder="user@coou.edu.ng" required value="lecturer@coou.edu.ng">
                            </div>
                            <button type="submit" id="forgot-req-btn" class="btn btn-primary" style="width: 100%; padding: 12px; font-size: 0.88rem;">
                                Generate Security Recovery Token &rarr;
                            </button>
                        </form>
                    </div>

                    <div id="forgot-step-2" style="display:none;">
                        <div style="margin-bottom:16px;">
                            <span class="technical-coord">// CREDENTIAL_RECOVERY_STEP_02</span>
                            <h3 style="font-family:var(--font-mono); font-size:1.05rem; font-weight:700; text-transform:uppercase; margin-top:2px;">
                                Set New Password
                            </h3>
                            <div id="recovery-user-info" style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-accent); margin-top:4px; font-weight:600;"></div>
                        </div>

                        <form onsubmit="AuthView.handleCompleteReset(event)">
                            <div class="form-group">
                                <label class="form-label">Offline Recovery Token</label>
                                <input type="text" id="reset-code-input" class="form-control" placeholder="COOU-XXXXXX" required style="font-weight:700; letter-spacing:0.05em;">
                            </div>
                            <div class="form-group">
                                <label class="form-label">New Password (min. 6 characters)</label>
                                <input type="password" id="reset-new-password" class="form-control" placeholder="Enter new password" minlength="6" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Confirm New Password</label>
                                <input type="password" id="reset-confirm-password" class="form-control" placeholder="Confirm new password" minlength="6" required>
                            </div>
                            <button type="submit" id="reset-submit-btn" class="btn btn-primary" style="width: 100%; padding: 12px; font-size: 0.88rem;">
                                Update Password &amp; Authenticate &rarr;
                            </button>
                        </form>
                    </div>

                    <div style="text-align: center; margin-top: 20px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--color-text-muted);">
                        <a href="javascript:void(0)" onclick="AuthView.setMode('login')" style="color: var(--color-text-main); font-weight: 600; text-decoration: none;">&larr; Back to Login</a>
                    </div>
                </div>
            </div>
        </div>
        `;
    },

    switchPortal(portal) {
        this.currentPortal = portal;
        const isStudent = portal === 'student';
        
        document.getElementById('tab-lecturer').className = `btn btn-sm ${!isStudent ? 'btn-primary' : 'btn-secondary'}`;
        document.getElementById('tab-student').className = `btn btn-sm ${isStudent ? 'btn-primary' : 'btn-secondary'}`;

        document.getElementById('login-email-label').textContent = isStudent ? 'Student Institutional Email' : 'Lecturer Institutional Email';
        document.getElementById('login-email').value = isStudent ? 'student@coou.edu.ng' : 'lecturer@coou.edu.ng';
        document.getElementById('login-password').value = isStudent ? 'cooustudent2026' : 'coouguard2026';
    },

    handleRoleChange(role) {
        const matricGroup = document.getElementById('reg-matric-group');
        if (matricGroup) {
            matricGroup.style.display = (role === 'student') ? 'block' : 'none';
        }
    },

    setMode(mode) {
        document.getElementById('login-form-container').style.display = (mode === 'login') ? 'block' : 'none';
        document.getElementById('register-form-container').style.display = (mode === 'register') ? 'block' : 'none';
        document.getElementById('forgot-form-container').style.display = (mode === 'forgot') ? 'block' : 'none';

        if (mode === 'forgot') {
            document.getElementById('forgot-step-1').style.display = 'block';
            document.getElementById('forgot-step-2').style.display = 'none';
        }

        const errDiv = document.getElementById('auth-error');
        const succDiv = document.getElementById('auth-success');
        if (errDiv) errDiv.style.display = 'none';
        if (succDiv) succDiv.style.display = 'none';
    },

    fillLecturerDemo() {
        this.switchPortal('lecturer');
    },

    fillStudentDemo() {
        this.switchPortal('student');
    },

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const errDiv = document.getElementById('auth-error');

        try {
            errDiv.style.display = 'none';
            const data = await API.login(email, password);
            API.setToken(data.access_token);
            State.setUser(data.user);
            
            App.showToast(`Welcome back, ${data.user.full_name}`, 'success');
            
            if (data.user.role === 'student') {
                window.location.hash = '#student-portal';
            } else {
                window.location.hash = '#dashboard';
            }
        } catch (error) {
            errDiv.textContent = `> AUTH_FAILED: ${error.message || 'Login failed'}`;
            errDiv.style.display = 'block';
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const fullName = document.getElementById('reg-name').value;
        const role = document.getElementById('reg-role').value;
        const matric = document.getElementById('reg-matric')?.value || null;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const errDiv = document.getElementById('auth-error');

        try {
            errDiv.style.display = 'none';
            const data = await API.request('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify({
                    full_name: fullName,
                    role: role,
                    matric_number: matric,
                    email: email,
                    password: password
                })
            });
            API.setToken(data.access_token);
            State.setUser(data.user);
            App.showToast('Account registered successfully.', 'success');

            if (role === 'student') {
                window.location.hash = '#student-portal';
            } else {
                window.location.hash = '#dashboard';
            }
        } catch (error) {
            errDiv.textContent = `> REGISTRATION_FAILED: ${error.message || 'Failed'}`;
            errDiv.style.display = 'block';
        }
    },

    async handleRequestReset(e) {
        e.preventDefault();
        const email = document.getElementById('forgot-email').value;
        const errDiv = document.getElementById('auth-error');
        const succDiv = document.getElementById('auth-success');
        const btn = document.getElementById('forgot-req-btn');

        btn.disabled = true;
        btn.innerHTML = 'VERIFYING...';
        errDiv.style.display = 'none';
        succDiv.style.display = 'none';

        try {
            const res = await API.forgotPassword(email);
            document.getElementById('forgot-step-1').style.display = 'none';
            document.getElementById('forgot-step-2').style.display = 'block';

            document.getElementById('recovery-user-info').textContent = `Account: ${res.user_name} (${res.email})`;
            document.getElementById('reset-code-input').value = res.reset_code;

            succDiv.textContent = `> VERIFIED: Security token generated [${res.reset_code}]. Set your new password.`;
            succDiv.style.display = 'block';
        } catch (err) {
            errDiv.textContent = `> RECOVERY_ERROR: ${err.message}`;
            errDiv.style.display = 'block';
            btn.disabled = false;
            btn.innerHTML = 'Generate Security Recovery Token &rarr;';
        }
    },

    async handleCompleteReset(e) {
        e.preventDefault();
        const email = document.getElementById('forgot-email').value;
        const resetCode = document.getElementById('reset-code-input').value;
        const newPass = document.getElementById('reset-new-password').value;
        const confirmPass = document.getElementById('reset-confirm-password').value;

        const errDiv = document.getElementById('auth-error');
        const succDiv = document.getElementById('auth-success');
        const btn = document.getElementById('reset-submit-btn');

        if (newPass !== confirmPass) {
            errDiv.textContent = '> ERROR: Passwords do not match.';
            errDiv.style.display = 'block';
            return;
        }

        btn.disabled = true;
        btn.innerHTML = 'UPDATING...';
        errDiv.style.display = 'none';

        try {
            await API.resetPassword(email, resetCode, newPass);
            succDiv.textContent = '> SUCCESS: Password updated successfully. Redirecting to login...';
            succDiv.style.display = 'block';

            App.showToast('Password updated successfully. Please log in.', 'success');

            setTimeout(() => {
                AuthView.setMode('login');
                document.getElementById('login-email').value = email;
                document.getElementById('login-password').value = newPass;
            }, 1200);
        } catch (err) {
            errDiv.textContent = `> RESET_FAILED: ${err.message}`;
            errDiv.style.display = 'block';
            btn.disabled = false;
            btn.innerHTML = 'Update Password &amp; Authenticate &rarr;';
        }
    }
};
