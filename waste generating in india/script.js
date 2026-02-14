function validateForm(formType) {
    let isValid = true;
    const form = document.querySelector(formType === 'login' ? '#loginForm' : '#signupForm');
    const inputs = form.querySelectorAll('input');
    
    inputs.forEach(input => {
        const error = input.nextElementSibling;
        error.style.display = 'none';
        
        if (!input.value.trim()) {
            error.style.display = 'block';
            error.textContent = `${input.getAttribute('placeholder')} is required`;
            isValid = false;
        } else if (input.type === 'email' && !validateEmail(input.value)) {
            error.style.display = 'block';
            error.textContent = 'Please enter a valid email address';
            isValid = false;
        } else if (input.type === 'password' && input.value.length < 6) {
            error.style.display = 'block';
            error.textContent = 'Password must be at least 6 characters long';
            isValid = false;
        }
    });
    
    if (isValid) {
        if (formType === 'login') {
            // Store user email as name for demo purposes
            const userEmail = document.querySelector('#email').value;
            const userName = userEmail.split('@')[0]; // Use part before @ as name
            localStorage.setItem('userName', userName);
            window.location.href = 'dashboard.html';
        } else {
            // For signup, store the actual name
            const userName = document.querySelector('#name').value;
            localStorage.setItem('userName', userName);
            window.location.href = 'dashboard.html';
        }
    }
    
    return false; // Prevent form submission for this demo
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}