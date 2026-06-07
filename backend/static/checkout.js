(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "checkout";
  const { getSession, getCurrentUser, getCartItems, getCartSubtotal, placeOrder, escapeHtml, formatCurrency, setMessage, renderSessionLabels, highlightActiveNav } = store;

  function renderCheckoutPage() {
    const checkoutSummary = document.getElementById("checkoutSummary");
    const paymentForm = document.getElementById("paymentForm");
    const session = getSession();
    const currentUser = getCurrentUser(session);
    const items = getCartItems();

    function renderSummary() {
      if (items.length === 0) {
        checkoutSummary.innerHTML = `<article class="empty-state small"><h2>No cart items</h2><p>Add books from the catalog before checking out.</p><a class="button-link" href="index.html">Browse catalog</a></article>`;
        return;
      }
      checkoutSummary.innerHTML = `
        <div class="summary-list">${items.map((item) => `<div class="summary-row"><span>${escapeHtml(item.title)} x${item.quantity}</span><strong>${formatCurrency(item.lineTotal)}</strong></div>`).join("")}</div>
        <dl class="summary-grid compact"><div><dt>Subtotal</dt><dd>${formatCurrency(getCartSubtotal())}</dd></div><div><dt>Stock checked</dt><dd>Yes</dd></div></dl>
      `;
    }

    renderSummary();

    if (paymentForm) {
      const nameField = paymentForm.querySelector('[name="fullName"]');
      const emailField = paymentForm.querySelector('[name="email"]');
      if (nameField && !nameField.value) {
        nameField.value = currentUser?.name || session.name || "Guest";
      }
      if (emailField && !emailField.value && currentUser?.email) {
        emailField.value = currentUser.email;
      }
    }

    if (paymentForm && !paymentForm.dataset.listenerAttached) {
      paymentForm.dataset.listenerAttached = 'true';
      paymentForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const latestItems = getCartItems();
        if (latestItems.length === 0) {
          setMessage("checkoutMessage", "Your cart is empty.", "error");
          return;
        }
        const formData = new FormData(paymentForm);
        const result = placeOrder({
          fullName: String(formData.get("fullName") || "").trim(),
          email: String(formData.get("email") || "").trim(),
          address: String(formData.get("address") || "").trim(),
          shippingMethod: String(formData.get("shippingMethod") || "post"),
          paymentMethod: String(formData.get("paymentMethod") || "card"),
        });
        if (!result.ok) {
          setMessage("checkoutMessage", result.message, "error");
          return;
        }
        setMessage("checkoutMessage", `Payment confirmed for ${result.order.id}.`, "success");
        window.location.href = `purchases.html?order=${encodeURIComponent(result.order.id)}&paid=1`;
      });
    }
  }

  if (PAGE === "checkout") {
    renderSessionLabels();
    highlightActiveNav();
    renderCheckoutPage();
    document.addEventListener('books:loaded', () => {
      renderSessionLabels();
      highlightActiveNav();
      renderCheckoutPage();
    });
  }
})();
