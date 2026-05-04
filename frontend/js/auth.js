const API = "https://fixit-app-x4ew.onrender.com";

// ======================
// LOGIN
// ======================
async function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Please fill all fields");
        return;
    }

    const btn = event.target.closest("button");
    if (btn) {
        btn.innerText = "Logging in...";
        btn.disabled = true;
    }

    try {
        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        let data;
        try {
            data = await res.json();
        } catch {
            throw new Error("Invalid server response");
        }

        if (!res.ok) {
            alert(data.detail || "Invalid email or password");
            return;
        }

        // 🔐 SAVE AUTH DATA
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));

        alert("✅ Login successful");
        window.location.href = "dashboard.html";

    } catch (err) {
        console.error("Login error:", err);
        alert("❌ Network or server error.");
    } finally {
        if (btn) {
            btn.innerText = "Login";
            btn.disabled = false;
        }
    }
}


// ======================
// SIGNUP
// ======================
async function signup(event) {
    event.preventDefault();

    const full_name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!full_name || !email || !phone || !password) {
        alert("Please fill all fields");
        return;
    }

    try {
        const res = await fetch(`${API}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                full_name,
                email,
                phone,
                password
            })
        });

        let data;
        try {
            data = await res.json();
        } catch {
            throw new Error("Invalid server response");
        }

        if (!res.ok) {
            alert(data.detail || "Signup failed");
            return;
        }

        alert("✅ Account created successfully!");
        window.location.href = "login.html";

    } catch (err) {
        console.error("Signup error:", err);
        alert("❌ Failed to create account.");
    }
}


// ======================
// LOGOUT
// ======================
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    alert("Logged out successfully");
    window.location.href = "login.html";
}


// ======================
// AUTH HELPERS
// ======================
function getToken() {
    return localStorage.getItem("token");
}

function getUser() {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
}

function isLoggedIn() {
    return !!getToken();
}


// ======================
// PROTECT PAGES
// ======================
function protectPage() {
    if (!isLoggedIn()) {
        alert("Please login first");
        window.location.href = "login.html";
    }
}