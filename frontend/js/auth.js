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

    const btn = event.target.closest("button"); // ✅ FIX BUTTON TARGET
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

        // ✅ HANDLE NON-JSON ERRORS SAFELY
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

        // ✅ SAVE TOKEN
        localStorage.setItem("token", data.access_token);

        // ✅ SAVE USER (if returned)
        if (data.user) {
            localStorage.setItem("user", JSON.stringify(data.user));
        }

        alert("✅ Login successful");

        // ✅ REDIRECT
        window.location.href = "dashboard.html";

    } catch (err) {
        console.error("Login error:", err);
        alert("❌ Network or server error. Check console.");
    } finally {
        if (btn) {
            btn.innerText = "Login";
            btn.disabled = false;
        }
    }
}