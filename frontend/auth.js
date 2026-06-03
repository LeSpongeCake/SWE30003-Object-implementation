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

    loginForm?.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      const email = String(formData.get("email") || "").trim().toLowerCase();
      const password = String(formData.get("password") || "").trim();
      const user = getUsers().find((entry) => entry.email.toLowerCase() === email && entry.password === password);
      if (!user) {
        setMessage("authMessage", "Invalid email or password.", "error");
        return;
      }
      loginSession(user);
      setMessage("authMessage", `Signed in as ${user.name}.`, "success");
      window.location.href = user.role === "admin" ? "admin.html" : "account.html";
    });

    createForm?.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData(createForm);
      const name = String(formData.get("name") || "").trim();
      const email = String(formData.get("createEmail") || "").trim().toLowerCase();
      const password = String(formData.get("createPassword") || "").trim();
      if (!name || !email || !password) {
        setMessage("authMessage", "Fill in every field to create an account.", "error");
        return;
      }
      const users = getUsers();
      if (users.some((user) => user.email.toLowerCase() === email)) {
        setMessage("authMessage", "That email already has an account.", "error");
        return;
      }
      const user = { id: `user-${Date.now().toString(36)}`, name, email, password, role: "user" };
      users.push(user);
      saveUsers(users);
      loginSession(user);
      setMessage("authMessage", `Account created for ${name}.`, "success");
      window.location.href = "account.html";
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
