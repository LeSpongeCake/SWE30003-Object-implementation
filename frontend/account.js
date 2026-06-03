(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "account";
  const { getSession, getCurrentUser, getSessionIdentifier, getCartCount, getOrdersForSession, createGuestSession, formatDate, formatCurrency, escapeHtml, renderSessionLabels, highlightActiveNav } = store;

  function renderAccountLikePage(mode = "account") {
    const profileCard = document.getElementById("accountProfile");
    const activityCard = document.getElementById("accountActivity");
    const orderList = document.getElementById("accountOrders");
    const signOutButton = document.getElementById("accountSignOut");
    const session = getSession();
    const user = getCurrentUser(session);
    const orders = getOrdersForSession();

    profileCard.innerHTML = `
      <div class="panel-block">
        <p class="eyebrow">${session.kind === "guest" ? "Guest account" : "User account"}</p>
        <h2>${escapeHtml(user?.name || session.name || "Guest")}</h2>
        <p>${session.kind === "guest" ? "Browsing without a login." : `${escapeHtml(user?.email || "No email saved")}`}</p>
      </div>
      <dl class="summary-grid compact">
        <div><dt>Session</dt><dd>${escapeHtml(getSessionIdentifier().slice(-8))}</dd></div>
        <div><dt>Role</dt><dd>${escapeHtml(session.kind)}</dd></div>
        <div><dt>Cart items</dt><dd>${getCartCount()}</dd></div>
        <div><dt>Purchases</dt><dd>${orders.length}</dd></div>
      </dl>
    `;

    activityCard.innerHTML = `
      <div class="panel-block">
        <p class="eyebrow">Quick actions</p>
        <div class="action-stack">
          <a class="button-link" href="cart.html">Open cart</a>
          <a class="button-link secondary" href="checkout.html">Go to payment</a>
          <a class="button-link secondary" href="purchases.html">View purchases</a>
          ${session.kind === "admin" ? '<a class="button-link secondary" href="admin.html">Admin console</a>' : ""}
        </div>
      </div>
      <p class="muted">Guest sessions are stored in this browser and linked to the cart and purchase history.</p>
    `;

    if (orderList) {
      if (orders.length === 0) {
        orderList.innerHTML = `<article class="empty-state"><h2>No purchases yet</h2><p>Complete a checkout and your orders will appear here.</p></article>`;
      } else {
        orderList.innerHTML = orders.map((order) => `
          <article class="order-card">
            <div class="order-head"><div><strong>${escapeHtml(order.id)}</strong><p>${formatDate(order.createdAt)}</p></div><span>${escapeHtml(order.status)}</span></div>
            <p>${order.items.length} item${order.items.length === 1 ? "" : "s"} · ${formatCurrency(order.total)}</p>
            <p>Shipping: ${escapeHtml(order.shippingStatus)}</p>
            <a class="button-link secondary" href="tracking.html?order=${encodeURIComponent(order.id)}">Track delivery</a>
          </article>
        `).join("");
      }
    }

    signOutButton?.addEventListener("click", () => {
      createGuestSession();
      window.location.href = mode === "guest" ? "guest.html" : "login.html";
    });
  }

  if (PAGE === "account" || PAGE === "guest") {
    renderSessionLabels();
    highlightActiveNav();
    renderAccountLikePage(PAGE);
  }
})();
