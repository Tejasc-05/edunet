// Check if user is logged in
function checkLogin() {
    const userName = localStorage.getItem('userName');
    if (!userName) {
        window.location.href = 'login.html';
    } else {
        document.getElementById('userName').textContent = userName;
    }
}

// Handle logout
function logout() {
    localStorage.removeItem('userName');
    window.location.href = 'login.html';
}

// Initialize dashboard
function initDashboard() {
    checkLogin();
    
    // Set current date
    const date = new Date();
    document.getElementById('currentDate').textContent = date.toLocaleDateString('en-IN', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Add event listeners when document loads
document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
    
    // Attach logout event listener
    document.getElementById('logoutButton').addEventListener('click', logout);
});