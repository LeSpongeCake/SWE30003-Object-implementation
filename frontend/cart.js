(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "cart";
  const { formatCurrency, escapeHtml, getCartItems, getCartCount, getCartSubtotal, getSession, getSessionIdentifier, updateCartItem, removeCartItem, renderSessionLabels, highlightActiveNav } = store;

  function renderCartPage() {
    const cartList = document.getElementById("cartList");
    const cartSummary = document.getElementById("cartSummary");
    const cartMessage = document.getElementById("cartMessage");
    const checkoutLink = document.getElementById("checkoutLink");

    function render() {
      const items = getCartItems();
      cartList.innerHTML = "";
      if (items.length === 0) {
        cartList.innerHTML = `<article class="empty-state"><h2>Your cart is empty</h2><p>Go back to the catalog and add a few books to start a purchase.</p><a class="button-link" href="index.html">Browse catalog</a></article>`;
        cartSummary.innerHTML = "<p>No items selected yet.</p>";
        checkoutLink?.classList.add("disabled");
        checkoutLink?.setAttribute("aria-disabled", "true");
        cartMessage.textContent = `Cart linked to ${getSession().kind} session ${getSessionIdentifier().slice(-6)}.`;
        return;
      }

      checkoutLink?.classList.remove("disabled");
      checkoutLink?.removeAttribute("aria-disabled");

      items.forEach((item) => {
        const row = document.createElement("article");
        row.className = "list-item";
        row.innerHTML = `
          <div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.author)} · ${formatCurrency(item.price)} each</p></div>
          <div class="quantity-controls"><button type="button" data-action="decrease" data-book-id="${item.id}">−</button><strong>${item.quantity}</strong><button type="button" data-action="increase" data-book-id="${item.id}">+</button></div>
          <div class="list-meta"><strong>${formatCurrency(item.lineTotal)}</strong><span>${item.stock} available</span><button type="button" class="details-btn" data-action="remove" data-book-id="${item.id}">Remove</button></div>
        `;
        cartList.appendChild(row);
      });

      const subtotal = getCartSubtotal();
      cartSummary.innerHTML = `
        <dl class="summary-grid">
          <div><dt>Items</dt><dd>${items.reduce((sum, item) => sum + item.quantity, 0)}</dd></div>
          <div><dt>Subtotal</dt><dd>${formatCurrency(subtotal)}</dd></div>
          <div><dt>Shipping</dt><dd>Calculated at payment</dd></div>
          <div><dt>Total</dt><dd>${formatCurrency(subtotal)}</dd></div>
        </dl>
      `;
      cartMessage.textContent = `Cart linked to ${getSession().kind} session ${getSessionIdentifier().slice(-6)}.`;
    }

    cartList?.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) {
        return;
      }
      const bookId = Number(button.dataset.bookId);
      const current = getCartItems().find((item) => item.id === bookId);
      if (!current) {
        return;
      }
      if (button.dataset.action === "increase") {
        updateCartItem(bookId, current.quantity + 1);
      }
      if (button.dataset.action === "decrease") {
        updateCartItem(bookId, current.quantity - 1);
      }
      if (button.dataset.action === "remove") {
        removeCartItem(bookId);
      }
      renderSessionLabels();
      render();
    });

    render();
  }

  if (PAGE === "cart") {
    renderSessionLabels();
    highlightActiveNav();
    renderCartPage();
  }
})();
