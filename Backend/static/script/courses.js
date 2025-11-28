const token = localStorage.getItem('token');
if (!token) window.location.href = "/login";

async function fetchCourses() {
    try {
        const res = await fetch('/api/courses/');
        const data = await res.json();
        
        const list = document.getElementById('courseList');
        const dropdown = document.getElementById('courseDropdown');

        list.innerHTML = ''; 
        dropdown.innerHTML = '<option value="" disabled selected>-- Select a Course --</option>'; // Reset dropdown

        if(data.data.length === 0) {
            list.innerHTML = '<p>No courses available yet.</p>';
            return;
        }

        data.data.forEach(course => {
            // 1. Add to Dropdown
            const option = document.createElement('option');
            option.value = course._id; // The Course ID
            option.textContent = `${course.title} - ${course.instructor}`;
            dropdown.appendChild(option);

            // 2. Add to Card List (Visual)
            const card = document.createElement('div');
            card.className = 'course-card';
            card.innerHTML = `
                <h3>${course.title}</h3>
                <p>${course.description}</p>
                <span class="instructor">Instructor: ${course.instructor}</span>
                <button class="enroll-btn" onclick="enroll('${course._id}')">Enroll via Card</button>
            `;
            list.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        document.getElementById('courseList').innerText = "Failed to load courses.";
    }
}

// Function for the Button next to the Dropdown
async function enrollFromDropdown() {
    const dropdown = document.getElementById('courseDropdown');
    const selectedCourseId = dropdown.value;

    if (!selectedCourseId) {
        alert("Please select a course from the list first!");
        return;
    }
    await enroll(selectedCourseId);
}

// Main Enroll Function (Used by both Dropdown and Cards)
async function enroll(courseId) {
    try {
        const res = await fetch('/api/enrollments/enroll', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({ course_id: courseId })
        });

        const data = await res.json();

        if (res.ok) {
            alert("Successfully enrolled!");
        } else if (res.status === 409) {
            alert("You are already enrolled in this course.");
        } else {
            alert(data.error || "Enrollment failed.");
        }
    } catch (err) {
        console.error(err);
        alert("Error connecting to server.");
    }
}

// Run on page load
fetchCourses();