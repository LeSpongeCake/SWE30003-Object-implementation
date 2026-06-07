(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "login";
  const { getUsers, saveUsers, createGuestSession, getSession, getCurrentUser, loginSession, setMessage, renderSessionLabels, highlightActiveNav } = store;

  function renderLoginPage() {
    const loginForm = document.getElementById("loginForm");
    const createForm = document.getElementById("createForm");
    const guestButton = document.getElementById("guestButton");
    const signOutButton = document.getElementById("signOutButton");
    const currentSession = getSession();
    const currentUser = getCurrentUser(currentSession);

    signOutButton?.addEventListener("click", () => {
      createGuestSession();
      setMessage("authMessage", "Switched to a guest session.", "success");
      renderSessionLabels();
    });

    loginForm?.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      const email = String(formData.get("email") || "").trim().toLowerCase();
      const password = String(formData.get("password") || "").trim();
      
      try {
        const res = await fetch("/account/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: email, password: password })
        });
        const data = await res.json();
        
        if (!res.ok || data.error) {
          setMessage("authMessage", data.error || "Invalid email or password.", "error");
          return;
        }
        
        const user = {
          id: data.account_id,
          name: data.name,
          email: data.username,
          role: data.role === "customer" ? "user" : data.role
        };
        loginSession(user);
        setMessage("authMessage", `Signed in as ${user.name}.`, "success");
        window.location.href = user.role === "admin" ? "admin.html" : "account.html";
      } catch (err) {
        setMessage("authMessage", "Network error. Please try again.", "error");
      }
    });

    createForm?.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(createForm);
      const name = String(formData.get("name") || "").trim();
      const email = String(formData.get("createEmail") || "").trim().toLowerCase();
      const password = String(formData.get("createPassword") || "").trim();
      if (!name || !email || !password) {
        setMessage("authMessage", "Fill in every field to create an account.", "error");
        return;
      }
      
      try {
        const res = await fetch("/account/create", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: name, username: email, password: password })
        });
        
        if (!res.ok) {
          setMessage("authMessage", "Failed to create an account. Email might be in use.", "error");
          return;
        }
        
        // Auto-login after creation
        const loginRes = await fetch("/account/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: email, password: password })
        });
        const loginData = await loginRes.json();
        
        if (!loginRes.ok || loginData.error) {
           setMessage("authMessage", "Account created, but auto-login failed.", "error");
           return;
        }
        
        const user = {
          id: loginData.account_id,
          name: loginData.name,
          email: loginData.username,
          role: loginData.role === "customer" ? "user" : loginData.role
        };
        loginSession(user);
        setMessage("authMessage", `Account created for ${name}.`, "success");
        window.location.href = "account.html";
      } catch (err) {
        setMessage("authMessage", "Network error. Please try again.", "error");
      }
    });

    guestButton?.addEventListener("click", () => {
      createGuestSession();
      setMessage("authMessage", "You are browsing as a guest.", "success");
      window.location.href = "guest.html";
    });

    setMessage("authMessage", currentSession.kind === "guest" ? "Guest session ready." : `Signed in as ${currentUser?.name || currentSession.name}.`, "info");
  }

  if (PAGE === "login") {
    renderSessionLabels();
    highlightActiveNav();
    renderLoginPage();
  }
})();
