// ======================
// NAVBAR CONTROL
// ======================
function updateNavbar() {
    const token = localStorage.getItem("token");
    const nav = document.getElementById("nav-links");

    if (!nav) return;

    // Clear first (prevents duplication)
    nav.innerHTML = "";

    // Always visible links
    nav.innerHTML += `
        <a href="index.html"><i class="fas fa-home"></i></a>
        <a href="services.html"><i class="fas fa-tools"></i></a>
        <a href="contact.html"><i class="fas fa-envelope"></i></a>
    `;

    // Logged-in user
    if (token) {
        nav.innerHTML += `
            <a href="dashboard.html"><i class="fas fa-tachometer-alt"></i></a>
            <a href="#" onclick="logout()"><i class="fas fa-sign-out-alt"></i></a>
        `;
    } else {
        nav.innerHTML += `
            <a href="login.html"><i class="fas fa-user"></i></a>
        `;
    }
}

// ======================
// LOGOUT CONFIRMATION
// ======================
function logout() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "login.html";
    }
}

// ======================
// INIT
// ======================
window.onload = updateNavbar;