const API_BASE = "/api/auth";

// Handle Registration
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const res = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });
            const data = await res.json();

            if (res.ok) {
                alert("Registration successful! Please login.");
                window.location.href = "/login"; // Redirect to login page
            } else {
                alert(data.error || "Registration failed");
            }
        } catch (err) {
            console.error(err);
            alert("An error occurred.");
        }
    });
}

// Handle Login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();

            if (res.ok) {
                // Save Token and User Name to LocalStorage
                localStorage.setItem('token', data.data.token);
                localStorage.setItem('userName', data.data.name);
                
                alert("Login Successful!");
                window.location.href = "/dashboard"; // Redirect to dashboard
            } else {
                alert(data.error || "Invalid Credentials");
            }
        } catch (err) {
            console.error(err);
            alert("Server error. Check console.");
        }
    });
}
