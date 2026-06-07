(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "tracking";
  const { getOrders, getLatestOrderForSession, updateOrder, addOrderEvent, formatDate, formatCurrency, escapeHtml, renderSessionLabels, highlightActiveNav } = store;

  function renderTrackingPage() {
    const trackingCard = document.getElementById("trackingCard");
    const trackingMessage = document.getElementById("trackingMessage");
    const params = new URLSearchParams(window.location.search);
    const orderId = params.get("order");
    const order = orderId ? getOrders().find((entry) => entry.id === orderId) : getLatestOrderForSession();

    if (!order) {
      trackingCard.innerHTML = `<article class="empty-state"><h2>No order selected</h2><p>Complete a purchase first, then return here to watch the delivery update.</p><a class="button-link" href="purchases.html">See purchases</a></article>`;
      trackingMessage.textContent = "Open a purchase to start tracking.";
      return;
    }

    function refresh() {
      const current = getOrders().find((entry) => entry.id === order.id) || order;
      const events = Array.isArray(current.events) ? current.events : [];
      trackingCard.innerHTML = `
        <article class="tracking-card">
          <div class="order-head"><div><strong>${escapeHtml(current.id)}</strong><p>${formatDate(current.createdAt)}</p></div><span>${escapeHtml(current.shippingStatus)}</span></div>
          <p><strong>${escapeHtml(current.customerName)}</strong> · ${escapeHtml(current.shippingMethod === "pickup" ? "Pickup" : "Post")}</p>
          <div class="timeline">
            ${events.map((event) => `<div class="timeline-item"><span></span><div><strong>${escapeHtml(event.label)}</strong><p>${formatDate(event.at)}</p></div></div>`).join("")}
            <div class="timeline-item highlight"><span></span><div><strong>${escapeHtml(current.shippingStatus)}</strong><p>Auto delivery finishes in about 10 seconds on this page.</p></div></div>
          </div>
          <div class="order-footer"><strong>${formatCurrency(current.total)}</strong><a class="button-link secondary" href="purchases.html?order=${encodeURIComponent(current.id)}">Back to purchases</a></div>
        </article>
      `;
      trackingMessage.textContent = current.shippingStatus === "Delivered" ? "This order is already marked as delivered." : "The page will auto-mark the order as delivered after 10 seconds.";
    }

    refresh();

    const currentOrder = getOrders().find((entry) => entry.id === order.id) || order;
    if (currentOrder.shippingStatus !== "Delivered" && currentOrder.shippingStatus !== "Cancelled") {
      const elapsed = Date.now() - currentOrder.createdAt;
      const wait = Math.max(0, 10000 - elapsed);
      window.setTimeout(() => {
        const updated = updateOrder(currentOrder.id, { shippingStatus: "Delivered", trackingStatus: "Delivered", status: "Delivered" });
        if (updated) {
          addOrderEvent(updated, "Dummy delivery completed");
          const orders = getOrders();
          const index = orders.findIndex((entry) => entry.id === updated.id);
          if (index !== -1) {
            orders[index] = updated;
            store.saveOrders(orders);
          }
          refresh();
        }
      }, wait);
    }
  }

  if (PAGE === "tracking") {
    renderSessionLabels();
    highlightActiveNav();
    renderTrackingPage();
  }
})();
