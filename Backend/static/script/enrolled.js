const token = localStorage.getItem('token');
if (!token) window.location.href = "/login";

async function loadEnrolled() {
    try {
        const res = await fetch('/api/enrollments/my-courses', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        
        const container = document.getElementById('enrolledCourses');
        container.innerHTML = '';

        if (!data.data || data.data.length === 0) {
            container.innerHTML = '<p style="text-align:center;">You have not enrolled in any courses yet.</p>';
            return;
        }

        // Relational Data: The backend sends course_title, instructor, etc.
        data.data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'enrolled-card';
            card.innerHTML = `
                <h3>${item.course_title}</h3>
                <p>Instructor: ${item.instructor}</p>
                <p>${item.course_desc}</p>
                <span class="status-badge">Active</span>
                <p style="font-size:0.8rem; color:#888; margin-top:10px;">Enrolled on: ${new Date(item.enrolled_at).toLocaleDateString()}</p>
            `;
            container.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        document.getElementById('enrolledCourses').innerText = "Error loading your courses.";
    }
}

loadEnrolled();