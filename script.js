let currentUser = null;

// ---------------- AUTH ----------------

function signup() {
    const data = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    };

    fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(res => {
            alert(res.message || res.error);
        });
}

function login() {
    const data = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    };

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(res => {
            if (res.token) {
                currentUser = res.token;
                alert("Logged in as: " + currentUser);
            } else {
                alert(res.error);
            }
        });
}

// ---------------- RUN CODE ----------------

function runCode() {
    const payload = {
        language: document.getElementById("language").value,
        code: document.getElementById("code").value
    };

    fetch("http://127.0.0.1:5000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(res => res.json())
        .then(res => {
            document.getElementById("output").textContent = res.output;
        });
}

// ---------------- SAVE CODE ----------------

function saveCode() {
    if (!currentUser) {
        alert("Please login before saving code!");
        return;
    }

    const payload = {
        username: currentUser,
        language: document.getElementById("language").value,
        code: document.getElementById("code").value
    };

    fetch("http://127.0.0.1:5000/save_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(res => res.json())
        .then(res => {
            alert(res.message || res.error);
        });
}
