(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "admin";
  const { getSession, getOrders, getInventory, saveInventory, findBook, updateOrder, addOrderEvent, escapeHtml, formatDate, formatCurrency, setMessage, renderSessionLabels, highlightActiveNav, BOOKS } = store;

  function renderAdminPage() {
    const adminOrders = document.getElementById("adminOrders");
    const stockTable = document.getElementById("stockTable");
    const adminMessage = document.getElementById("adminMessage");
    const session = getSession();

    function getShippingAction(order) {
      if (order.shippingStatus === "Delivered") {
        return null;
      }
      if (order.shippingMethod === "pickup") {
        if (order.shippingStatus === "Allocated for pickup") {
          return { label: "Mark ready for pickup", next: "Ready for pickup" };
        }
        if (order.shippingStatus === "Ready for pickup") {
          return { label: "Confirm picked up", next: "Picked up" };
        }
        if (order.shippingStatus === "Picked up") {
          return { label: "Close as delivered", next: "Delivered" };
        }
        return { label: "Mark ready for pickup", next: "Ready for pickup" };
      }
      if (order.shippingStatus === "Allocated to post") {
        return { label: "Allocate post", next: "Posted" };
      }
      if (order.shippingStatus === "Posted") {
        return { label: "Close as delivered", next: "Delivered" };
      }
      return { label: "Mark delivered", next: "Delivered" };
    }

    function renderOrders() {
      const orders = getOrders();
      if (session.kind !== "admin") {
        adminOrders.innerHTML = `<article class="empty-state"><h2>Admin access required</h2><p>Sign in with the admin account to manage shipping and stock.</p><a class="button-link" href="login.html">Go to login</a></article>`;
        if (adminMessage) {
          adminMessage.textContent = "Use admin@bookshelf.local / admin123 to access this page.";
        }
        return;
      }
      if (adminMessage) {
        adminMessage.textContent = "Admin session active. Manage shipping operations and update inventory below.";
      }
      if (orders.length === 0) {
        adminOrders.innerHTML = `<article class="empty-state"><h2>No purchases to process</h2><p>Orders will appear here after a checkout is completed.</p></article>`;
        return;
      }
      adminOrders.innerHTML = orders.map((order) => {
        const action = getShippingAction(order);
        return `
          <article class="order-card">
            <div class="order-head"><div><strong>${escapeHtml(order.id)}</strong><p>${escapeHtml(order.customerName)} · ${formatDate(order.createdAt)}</p></div><span>${escapeHtml(order.shippingStatus)}</span></div>
            <p>${order.items.length} item${order.items.length === 1 ? "" : "s"} · ${formatCurrency(order.total)}</p>
            <div class="action-stack inline">${action ? `<button class="button-link" type="button" data-order-id="${escapeHtml(order.id)}" data-next-status="${escapeHtml(action.next)}">${escapeHtml(action.label)}</button>` : ""}<a class="button-link secondary" href="tracking.html?order=${encodeURIComponent(order.id)}">Open tracking</a></div>
          </article>
        `;
      }).join("");
    }

    function renderStock() {
      if (session.kind !== "admin") {
        stockTable.innerHTML = "";
        return;
      }
      stockTable.innerHTML = `
        <div class="table-wrap">
          <table>
            <thead><tr><th>Book</th><th>Genre</th><th>Stock</th><th>Update</th></tr></thead>
            <tbody>
              ${BOOKS.map((book) => `<tr><td>${escapeHtml(book.title)}</td><td>${escapeHtml(book.genreLabel)}</td><td><input type="number" min="0" value="${getInventory()[book.id]}" data-stock-input="${book.id}" /></td><td><button type="button" class="details-btn" data-save-stock="${book.id}">Save</button></td></tr>`).join("")}
            </tbody>
          </table>
        </div>
      `;
    }

    adminOrders?.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-order-id]");
      if (!button || session.kind !== "admin") {
        return;
      }
      const orderId = button.dataset.orderId;
      const nextStatus = button.dataset.nextStatus || "Delivered";
      const updatedOrder = updateOrder(orderId, { shippingStatus: nextStatus, trackingStatus: nextStatus, status: nextStatus });
      if (updatedOrder) {
        addOrderEvent(updatedOrder, `Admin marked ${nextStatus.toLowerCase()}`);
        const orders = getOrders();
        const index = orders.findIndex((order) => order.id === updatedOrder.id);
        if (index !== -1) {
          orders[index] = updatedOrder;
          store.saveOrders(orders);
        }
        renderOrders();
        setMessage("adminMessage", `Updated ${orderId} to ${nextStatus}.`, "success");
      }
    });

    stockTable?.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-save-stock]");
      if (!button || session.kind !== "admin") {
        return;
      }
      const bookId = Number(button.dataset.saveStock);
      const input = stockTable.querySelector(`[data-stock-input="${bookId}"]`);
      const nextStock = Math.max(0, Number(input?.value || 0));
      const inventory = getInventory();
      inventory[bookId] = nextStock;
      saveInventory(inventory);
      renderStock();
      setMessage("adminMessage", `Stock updated for ${findBook(bookId)?.title || "book"}.`, "success");
    });

    renderOrders();
    renderStock();
  }

  if (PAGE === "admin") {
    renderSessionLabels();
    highlightActiveNav();
    renderAdminPage();
  }
})();
