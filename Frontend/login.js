function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("error-msg");

    fetch("http://localhost:5001/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem("loggedIn", "true");
            window.location.href = "index.html";
        } else {
            errorMsg.textContent = data.message || "Invalid credentials";
        }
    })
    .catch(() => {
        errorMsg.textContent = "Cannot connect to server";
    });
}

document.addEventListener("keydown", function(e) {
    if (e.key === "Enter") login();
});
