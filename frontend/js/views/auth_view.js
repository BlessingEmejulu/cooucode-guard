/**
 * Editorial Technical Auth View
 */
window.AuthView = {
    render() {
        return `
        <div style="min-height: 100vh; width: 100vw; display: flex; align-items: center; justify-content: center; background: var(--color-bg); padding: 20px;">
            <div style="width: 100%; max-width: 460px; background: var(--color-surface); border: 2px solid var(--color-border); border-radius: var(--radius-sm); padding: 40px 36px; box-shadow: var(--shadow-lg);">
                <div style="margin-bottom: 28px; border-bottom: 2px solid var(--color-border); padding-bottom: 18px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span class="brand-badge">CG</span>
                        <span class="technical-coord">// SEC_AUTH_v1.0</span>
                    </div>
                    <h2 style="font-family:var(--font-mono); font-size:1.45rem; font-weight:800; text-transform:uppercase; letter-spacing:-0.03em;">
                        COOUCodeGuard
                    </h2>
                    <p style="font-size:0.8rem; color:var(--color-text-muted); margin-top:2px;">
                        Chukwuemeka Odumegwu Ojukwu University &bull; Uli Campus<br>
                        <strong>Source Code Integrity &amp; Forensic System</strong>
                    </p>
                </div>

                <div id="auth-error" style="display:none; background:var(--color-danger-bg); color:var(--color-danger); padding:10px 14px; border:1px solid var(--color-danger); font-family:var(--font-mono); font-size:0.8rem; margin-bottom:18px;"></div>

                <div id="login-form-container">
                    <form id="login-form" onsubmit="AuthView.handleLogin(event)">
                        <div class="form-group">
                            <label class="form-label">Lecturer Institutional Email</label>
                            <input type="email" id="login-email" class="form-control" placeholder="lecturer@coou.edu.ng" required value="lecturer@coou.edu.ng">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Security Credential / Password</label>
                            <input type="password" id="login-password" class="form-control" placeholder="Password" required value="coouguard2026">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 13px; font-size: 0.9rem;">
                            Authenticate Session &rarr;
                        </button>
                    </form>

                    <div style="margin-top: 24px; padding: 14px; background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size: 0.72rem; font-weight: 700; color: var(--color-text-muted); text-transform: uppercase; margin-bottom: 8px;">
                            Quick Demo Verification
                        </div>
                        <button type="button" class="btn btn-secondary btn-sm" style="width:100%;" onclick="AuthView.fillDemo()">
                            Auto-Fill Dr. Chukwuma Eze (COOU CS)
                        </button>
                    </div>

                    <div style="text-align: center; margin-top: 20px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--color-text-muted);">
                        Need an account? <a href="javascript:void(0)" onclick="AuthView.toggleMode(true)" style="color: var(--color-accent); font-weight: 700; text-decoration: none;">Register here</a>
                    </div>
                </div>

                <div id="register-form-container" style="display: none;">
                    <form id="register-form" onsubmit="AuthView.handleRegister(event)">
                        <div class="form-group">
                            <label class="form-label">Full Name &amp; Academic Title</label>
                            <input type="text" id="reg-name" class="form-control" placeholder="e.g. Dr. Ngozi Okafor" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Institutional Email</label>
                            <input type="email" id="reg-email" class="form-control" placeholder="e.g. n.okafor@coou.edu.ng" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Password (min. 6 characters)</label>
                            <input type="password" id="reg-password" class="form-control" minlength="6" placeholder="Choose a password" required>
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 13px; font-size: 0.9rem;">
                            Create Lecturer Account &rarr;
                        </button>
                    </form>
                    <div style="text-align: center; margin-top: 20px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--color-text-muted);">
                        Already registered? <a href="javascript:void(0)" onclick="AuthView.toggleMode(false)" style="color: var(--color-accent); font-weight: 700; text-decoration: none;">Sign in</a>
                    </div>
                </div>
            </div>
        </div>
        `;
    },

    toggleMode(showRegister) {
        document.getElementById('login-form-container').style.display = showRegister ? 'none' : 'block';
        document.getElementById('register-form-container').style.display = showRegister ? 'block' : 'none';
        document.getElementById('auth-error').style.display = 'none';
    },

    fillDemo() {
        document.getElementById('login-email').value = 'lecturer@coou.edu.ng';
        document.getElementById('login-password').value = 'coouguard2026';
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
            App.showToast('Session authenticated. Welcome to COOUCodeGuard.', 'success');
            window.location.hash = '#dashboard';
        } catch (error) {
            errDiv.textContent = `> AUTH_FAILED: ${error.message || 'Login failed'}`;
            errDiv.style.display = 'block';
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const fullName = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const errDiv = document.getElementById('auth-error');

        try {
            errDiv.style.display = 'none';
            const data = await API.register(fullName, email, password);
            API.setToken(data.access_token);
            State.setUser(data.user);
            App.showToast('Account registered successfully.', 'success');
            window.location.hash = '#dashboard';
        } catch (error) {
            errDiv.textContent = `> REGISTRATION_FAILED: ${error.message || 'Failed'}`;
            errDiv.style.display = 'block';
        }
    }
};
