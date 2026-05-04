const API = (() => {
    const host = window.location.hostname;

    if (host === "localhost" || host === "127.0.0.1") {
        return "http://127.0.0.1:8000";
    }

    return "https://fixit-app-x4ew.onrender.com";
})();