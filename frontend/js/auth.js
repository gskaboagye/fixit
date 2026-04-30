// ======================
// LOGIN
// ======================
async function login(event) {
    event.preventDefault(); // prevents form reload

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Please fill all fields");
        return;
    }

    const btn = event.target;
    btn.innerText = "Logging in...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Invalid email or password");
            return;
        }

        // ✅ SAVE TOKEN
        localStorage.setItem("token", data.access_token);

        // ✅ OPTIONAL: SAVE USER INFO (future use)
        if (data.user) {
            localStorage.setItem("user", JSON.stringify(data.user));
        }

        // ✅ SUCCESS FEEDBACK
        alert("✅ Login successful");

        // REDIRECT
        window.location.href = "dashboard.html";

    } catch (err) {
        console.error(err);
        alert("Network error. Please try again.");
    } finally {
        btn.innerText = "Login";
        btn.disabled = false;
    }
}