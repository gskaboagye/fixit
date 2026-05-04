// ======================
// AUTH PROTECTION
// ======================
const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}


// ======================
// CREATE REQUEST
// ======================
async function createRequest(event) {
    if (event) event.preventDefault();

    console.log("🚀 Creating request...");

    const service = document.getElementById("service")?.value.trim();
    const desc = document.getElementById("desc")?.value.trim();
    const location = document.getElementById("location")?.value.trim();

    if (!service || !desc || !location) {
        alert("All fields required");
        return;
    }

    const btn = event?.target?.closest("button");
    if (btn) {
        btn.innerText = "Submitting...";
        btn.disabled = true;
    }

    try {
        const res = await fetch(`${API}/requests`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                service_type: service,
                description: desc,
                location
            })
        });

        const data = await res.json();

        if (!res.ok) {
            console.error(data);
            alert(data.detail || "Failed to create request");
            return;
        }

        addNotification("✅ Request created");
        loadRequests();

    } catch (err) {
        console.error("❌ Create request error:", err);
        alert("Server error while creating request");
    } finally {
        if (btn) {
            btn.innerText = "Submit Request";
            btn.disabled = false;
        }
    }
}


// ======================
// LOAD REQUESTS
// ======================
async function loadRequests() {
    console.log("📦 Loading requests...");

    try {
        const res = await fetch(`${API}/requests`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await res.json();
        const list = document.getElementById("request-list");

        if (!list) return;

        list.innerHTML = "";

        if (!Array.isArray(data) || data.length === 0) {
            list.innerHTML = "<li class='muted'>No requests yet</li>";
            return;
        }

        data.forEach(r => {
            const li = document.createElement("li");

            const email = JSON.parse(localStorage.getItem("user"))?.email || "";

            let payBtn = "";

            if (r.status !== "paid") {
                payBtn = `
                    <button onclick="payWithPaystack('${email}', ${r.amount || 50}, ${r.id}, '${r.subaccount_code || ""}')">
                        💳 Pay
                    </button>
                `;
            }

            li.innerHTML = `
                <strong>${r.service_type}</strong> - ${r.location}
                <span class="status ${r.status}">${r.status}</span>
                ${payBtn}
            `;

            list.appendChild(li);
        });

    } catch (err) {
        console.error("❌ Load requests error:", err);
    }
}


// ======================
// PAYSTACK PAYMENT
// ======================
function payWithPaystack(email, amount, requestId, subaccountCode) {

    if (!email) {
        alert("Missing user email");
        return;
    }

    if (!window.PaystackPop) {
        alert("Payment system not loaded");
        return;
    }

    const handler = PaystackPop.setup({
        key: "pk_test_xxxxxxxxx", // 🔥 PUT YOUR REAL KEY
        email: email,
        amount: amount * 100,
        currency: "GHS",

        subaccount: subaccountCode || undefined,
        bearer: subaccountCode ? "subaccount" : "account",

        callback: function (response) {
            console.log("💳 Payment success:", response.reference);
            verifyPayment(response.reference, requestId);
        },

        onClose: function () {
            console.log("Payment closed");
        }
    });

    handler.openIframe();
}


// ======================
// VERIFY PAYMENT
// ======================
async function verifyPayment(reference, requestId) {
    try {
        const res = await fetch(`${API}/verify-payment`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                reference,
                request_id: requestId
            })
        });

        const data = await res.json();

        if (!res.ok) {
            console.error(data);
            alert(data.detail || "Verification failed");
            return;
        }

        addNotification("💳 Payment successful");
        loadRequests();

    } catch (err) {
        console.error("❌ Verify payment error:", err);
        alert("Payment verification failed");
    }
}


// ======================
// EARNINGS
// ======================
async function loadEarnings() {
    try {
        const res = await fetch(`${API}/technician/earnings`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!res.ok) return;

        const data = await res.json();

        const el = document.getElementById("earnings");
        if (!el) return;

        el.innerText = `₵${data.total_earnings || 0} (${data.jobs_completed || 0} jobs)`;

    } catch (err) {
        console.log("Earnings error:", err);
    }
}


// ======================
// NOTIFICATIONS
// ======================
function addNotification(message) {
    const list = document.getElementById("notifications");
    if (!list) return;

    const li = document.createElement("li");
    li.innerText = message;

    list.prepend(li);
}


// ======================
// INIT (SAFE)
// ======================
document.addEventListener("DOMContentLoaded", () => {
    console.log("🔥 Dashboard loaded");

    loadRequests();
    loadEarnings();
});