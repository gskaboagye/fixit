// ======================
// API CONFIG (PRODUCTION READY)
// ======================

const isLocal =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";

// 🔥 SET YOUR PRODUCTION URL HERE
const PROD_API = "https://fixit-app-x4ew.onrender.com";

// 🔥 OPTIONAL: override manually if needed
const CUSTOM_API = localStorage.getItem("API_URL");

// FINAL API
const API = CUSTOM_API || (isLocal ? "http://127.0.0.1:8000" : PROD_API);

// ======================
// DEBUG (optional)
// ======================
console.log("🌐 API URL:", API);