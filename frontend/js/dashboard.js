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
    const service = document.getElementById("service").value.trim();
    const desc = document.getElementById("desc").value.trim();
    const location = document.getElementById("location").value.trim();

    if (!service || !desc || !location) {
        alert("All fields required");
        return;
    }

    const btn = event.target;
    btn.innerText = "Submitting...";
    btn.disabled = true;

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

        if (!res.ok) throw new Error();

        addNotification("✅ Request created");
        loadRequests();

    } catch {
        alert("Failed to create request");
    } finally {
        btn.innerText = "Submit Request";
        btn.disabled = false;
    }
}

// ======================
// LOAD REQUESTS
// ======================
async function loadRequests() {
    const res = await fetch(`${API}/requests`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await res.json();
    const list = document.getElementById("request-list");

    list.innerHTML = "";

    if (!data.length) {
        list.innerHTML = "<li style='color:#9ca3af;'>No requests yet</li>";
        return;
    }

    data.forEach(r => {
        const li = document.createElement("li");

        let payBtn = "";

        if (r.status !== "paid") {
            payBtn = `
                <button onclick="payWithPaystack('${r.user_email}', ${r.amount || 50}, ${r.id}, '${r.subaccount_code || ""}')">
                    💳 Pay
                </button>
            `;
        }

        li.innerHTML = `
            ${r.service_type} - ${r.location}
            <span class="status ${r.status}">${r.status}</span>
            ${payBtn}
        `;

        list.appendChild(li);
    });
}

// ======================
// PAYSTACK PAYMENT
// ======================
function payWithPaystack(email, amount, requestId, subaccountCode) {

    if (!email) {
        alert("Missing user email");
        return;
    }

    let handler = PaystackPop.setup({
        key: "pk_test_xxxxxxxxx", // 🔥 REPLACE WITH YOUR REAL KEY
        email: email,
        amount: amount * 100,
        currency: "GHS",

        subaccount: subaccountCode || undefined,
        bearer: "subaccount",

        callback: function(response) {
            verifyPayment(response.reference, requestId);
        },

        onClose: function() {
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
            body: JSON.stringify({ reference, request_id: requestId })
        });

        if (!res.ok) throw new Error();

        addNotification("💳 Payment successful");
        loadRequests();

    } catch {
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

        const data = await res.json();

        document.getElementById("earnings").innerText =
            `₵${data.total_earnings} (${data.jobs_completed} jobs)`;

    } catch {
        console.log("Earnings error");
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
// INIT
// ======================
window.onload = function () {
    loadRequests();
    loadEarnings();
};