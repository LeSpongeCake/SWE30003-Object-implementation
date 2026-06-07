(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "purchases";
  const { getOrdersForSession, escapeHtml, formatDate, formatCurrency, renderSessionLabels, highlightActiveNav } = store;

  function renderPurchasesPage() {
    const purchaseList = document.getElementById("purchaseList");
    const orders = getOrdersForSession();
    if (orders.length === 0) {
      purchaseList.innerHTML = `<article class="empty-state"><h2>No purchases yet</h2><p>Your completed checkout will appear here.</p><a class="button-link" href="index.html">Browse books</a></article>`;
      return;
    }
    purchaseList.innerHTML = orders.map((order) => `
      <article class="order-card">
        <div class="order-head"><div><strong>${escapeHtml(order.id)}</strong><p>${formatDate(order.createdAt)}</p></div><span>${escapeHtml(order.status)}</span></div>
        <div class="order-items">${order.items.map((item) => `<div class="order-item"><span>${escapeHtml(item.title)}</span><span>x${item.quantity}</span></div>`).join("")}</div>
        <div class="order-footer"><strong>${formatCurrency(order.total)}</strong><span>${escapeHtml(order.shippingStatus)}</span><a class="button-link secondary" href="tracking.html?order=${encodeURIComponent(order.id)}">Track delivery</a></div>
      </article>
    `).join("");
  }

  if (PAGE === "purchases") {
    renderSessionLabels();
    highlightActiveNav();
    renderPurchasesPage();
  }
})();
