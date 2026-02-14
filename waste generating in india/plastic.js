// Show welcome message when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in (basic check)
    const userName = localStorage.getItem('userName');
    if (!userName) {
        window.location.href = 'login.html';
        return;
    }

    // Show welcome message
    setTimeout(() => {
        alert('Welcome to Plastic Waste Management Dashboard!');
    }, 500); // Slight delay to ensure page is loaded
});

// Handle logout
document.getElementById('logoutButton').addEventListener('click', () => {
    localStorage.removeItem('userName'); // Clear user data
    window.location.href = 'login.html'; // Redirect to login page
});