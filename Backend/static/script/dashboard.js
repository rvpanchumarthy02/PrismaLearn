// 1. Security Check
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = "/login"; // Kick user out if no token
}

// 2. Load User Info
const userName = localStorage.getItem('userName') || "Student";
document.getElementById('profileInfo').innerHTML = `<p>Logged in as: <strong>${userName}</strong></p>`;

// 3. Logout Logic
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userName');
    window.location.href = "/login";
});