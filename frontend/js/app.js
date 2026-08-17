/**
 * Main Application Orchestrator
 */
window.App = {
    async init() {
        console.log('[COOUCodeGuard] Initializing offline system...');

        // Restore active user if token is present
        if (State.isAuthenticated()) {
            try {
                const user = await API.getMe();
                State.setUser(user);
                this.updateUserUI(user);
            } catch {
                State.setUser(null);
            }
        }

        // Initialize Router
        Router.init();
    },

    updateUserUI(user) {
        if (!user) return;
        const nameEl = document.getElementById('user-full-name');
        const roleEl = document.getElementById('user-role-label');
        const avatarEl = document.getElementById('user-avatar-initials');

        if (nameEl) nameEl.textContent = user.full_name;
        if (roleEl) roleEl.textContent = user.role.toUpperCase();
        if (avatarEl) {
            const initials = user.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            avatarEl.textContent = initials || 'LE';
        }
    },

    logout() {
        API.clearToken();
        State.setUser(null);
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

        toast.innerHTML = `
            ${LucideIcons.render(iconName, 18)}
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

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
