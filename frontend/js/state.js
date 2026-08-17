/**
 * COOUCodeGuard Global Application State Store
 */
window.State = {
    user: null,
    courses: [],
    submissions: [],
    recentScans: [],
    activeScan: null,
    activeComparison: null,
    stats: null,

    setUser(user) {
        this.user = user;
        if (user) {
            API.setUser(user);
        } else {
            API.clearToken();
        }
    },

    isAuthenticated() {
        return !!API.getToken();
    }
};
