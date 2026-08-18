/**
 * Main Application Orchestrator
 */
window.App = {
    init() {
        console.log('[COOUCodeGuard] Initializing offline system...');

        // 1. Initialize Router IMMEDIATELY (never block on network/API)
        if (window.Router) {
            Router.init();
        }

        // 2. Restore active user asynchronously in background
        if (window.State && State.isAuthenticated && State.isAuthenticated()) {
            API.getMe()
                .then(user => {
                    State.setUser(user);
                    this.updateUserUI(user);
                })
                .catch(() => {
                    // Fail silently, use cached user
                    const cachedUser = API.getUser();
                    if (cachedUser) {
                        this.updateUserUI(cachedUser);
                    }
                });
        }
    },

    updateUserUI(user) {
        if (!user) return;
        const nameEl = document.getElementById('user-full-name');
        const roleEl = document.getElementById('user-role-label');
        const avatarEl = document.getElementById('user-avatar-initials');

        if (nameEl) nameEl.textContent = user.full_name || 'Dr. Chukwuma Eze';
        if (roleEl) roleEl.textContent = (user.role || 'Lecturer').toUpperCase();
        if (avatarEl && user.full_name) {
            const initials = user.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            avatarEl.textContent = initials || 'CE';
        }
    },

    logout() {
        API.clearToken();
        if (window.State) State.setUser(null);
        this.showToast('Logged out successfully', 'info');
        window.location.hash = '#login';
    },

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let iconName = 'check-circle';
        if (type === 'error') iconName = 'alert-triangle';
        else if (type === 'info') iconName = 'shield-check';

        const iconHtml = (window.LucideIcons && LucideIcons.render) ? LucideIcons.render(iconName, 18) : '';

        toast.innerHTML = `
            ${iconHtml}
            <span>${message}</span>
        `;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }
};

// Immediate or DOMContentLoaded execution
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}
