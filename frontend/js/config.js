const API = (() => {
    const host = window.location.hostname;

    // 🔧 Local development
    if (host === "localhost" || host === "127.0.0.1") {
        return "http://127.0.0.1:8000";
    }

    // 🚀 Production (Render)
    return "https://fixit-app-x4ew.onrender.com";
})();