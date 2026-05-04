// ======================
// NAVBAR CONTROL
// ======================
function updateNavbar() {
    const token = localStorage.getItem("token");
    const user = getUserSafe();
    const nav = document.getElementById("nav-links");

    if (!nav) return;

    let html = `
        <a href="index.html"><i class="fas fa-home"></i></a>
        <a href="services.html"><i class="fas fa-tools"></i></a>
        <a href="contact.html"><i class="fas fa-envelope"></i></a>
    `;

    if (token) {
        html += `
            <a href="dashboard.html"><i class="fas fa-tachometer-alt"></i></a>
            <span class="nav-user">${user?.email || ""}</span>
            <a href="#" id="logout-btn"><i class="fas fa-sign-out-alt"></i></a>
        `;
    } else {
        html += `
            <a href="login.html"><i class="fas fa-user"></i></a>
        `;
    }

    nav.innerHTML = html;

    // Attach logout event safely
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault();
            logout();
        });
    }
}


// ======================
// SAFE USER PARSE
// ======================
function getUserSafe() {
    try {
        return JSON.parse(localStorage.getItem("user"));
    } catch {
        return null;
    }
}


// ======================
// LOGOUT
// ======================
function logout() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");

        window.location.href = "login.html";
    }
}


// ======================
// INIT (SAFE)
// ======================
document.addEventListener("DOMContentLoaded", () => {
    updateNavbar();
});