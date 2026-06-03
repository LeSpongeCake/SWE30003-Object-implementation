(function () {
  const STORAGE_KEYS = {
    session: "book_catalog_session_v2",
    users: "book_catalog_users_v2",
    orders: "book_catalog_orders_v2",
    inventory: "book_catalog_inventory_v2",
  };

  const BOOKS = [
    { id: 1, title: "The Left Hand of Darkness", author: "Ursula K. Le Guin", year: 1969, genreKey: "sci-fi", genreLabel: "Sci-Fi", tag: "Classic", price: 18.5, stock: 6, summary: "A diplomat travels to a world where gender is fluid and every alliance must be renegotiated." },
    { id: 2, title: "The Name of the Wind", author: "Patrick Rothfuss", year: 2007, genreKey: "fiction", genreLabel: "Fiction", tag: "Epic", price: 21, stock: 5, summary: "A gifted student recounts the rise of his legend, the mistakes behind it, and the cost of memory." },
    { id: 3, title: "The Dawn of Everything", author: "David Graeber & David Wengrow", year: 2021, genreKey: "history", genreLabel: "History", tag: "Ideas", price: 24, stock: 4, summary: "A challenge to simple origin stories that asks how societies formed and why alternatives matter." },
    { id: 4, title: "The Design of Everyday Things", author: "Don Norman", year: 2013, genreKey: "design", genreLabel: "Design", tag: "UX", price: 19, stock: 7, summary: "A practical look at why some products feel intuitive while others create friction and confusion." },
    { id: 5, title: "The Hobbit", author: "J. R. R. Tolkien", year: 1937, genreKey: "adventure", genreLabel: "Adventure", tag: "Quest", price: 16.5, stock: 8, summary: "A reluctant traveler joins a company of dwarves on a journey shaped by treasure, riddles, and courage." },
    { id: 6, title: "Project Hail Mary", author: "Andy Weir", year: 2021, genreKey: "sci-fi", genreLabel: "Sci-Fi", tag: "Modern", price: 22, stock: 5, summary: "A stranded scientist wakes alone in space and must solve a survival puzzle with an unlikely ally." },
  ];

  const DEFAULT_USERS = [
    { id: "admin", name: "Admin User", email: "admin@bookshelf.local", password: "admin123", role: "admin" },
    { id: "demo-user", name: "Ava Reader", email: "ava@bookshelf.local", password: "user123", role: "user" },
  ];

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  }

  function writeJSON(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  function getUsers() {
    const users = readJSON(STORAGE_KEYS.users, null);
    if (Array.isArray(users) && users.length > 0) {
      return users;
    }
    writeJSON(STORAGE_KEYS.users, DEFAULT_USERS);
    return [...DEFAULT_USERS];
  }

  function saveUsers(users) {
    writeJSON(STORAGE_KEYS.users, users);
  }

  function getInventory() {
    const inventory = readJSON(STORAGE_KEYS.inventory, null);
    if (inventory && typeof inventory === "object" && !Array.isArray(inventory)) {
      return inventory;
    }
    const seed = {};
    BOOKS.forEach((book) => {
      seed[book.id] = book.stock;
    });
    writeJSON(STORAGE_KEYS.inventory, seed);
    return seed;
  }

  function saveInventory(inventory) {
    writeJSON(STORAGE_KEYS.inventory, inventory);
  }

  function getOrders() {
    const orders = readJSON(STORAGE_KEYS.orders, []);
    return Array.isArray(orders) ? orders : [];
  }

  function saveOrders(orders) {
    writeJSON(STORAGE_KEYS.orders, orders);
  }

  function createGuestSession() {
    const session = { kind: "guest", id: `guest-${Date.now().toString(36)}`, name: "Guest" };
    writeJSON(STORAGE_KEYS.session, session);
    return session;
  }

  function getSession() {
    const session = readJSON(STORAGE_KEYS.session, null);
    if (session && session.id && session.kind) {
      return session;
    }
    return createGuestSession();
  }

  function saveSession(session) {
    writeJSON(STORAGE_KEYS.session, session);
  }

  function getCurrentUser(session = getSession()) {
    if (session.kind === "guest") {
      return null;
    }
    return getUsers().find((user) => user.id === session.userId) || null;
  }

  function getSessionIdentifier(session = getSession()) {
    return session.kind === "guest" ? session.id : session.userId;
  }

  function getCartKey(sessionId = getSessionIdentifier()) {
    return `book_catalog_cart_v2:${sessionId}`;
  }

  function getCart(sessionId = getSessionIdentifier()) {
    const cart = readJSON(getCartKey(sessionId), []);
    return Array.isArray(cart) ? cart : [];
  }

  function saveCart(cart, sessionId = getSessionIdentifier()) {
    writeJSON(getCartKey(sessionId), cart);
  }

  function clearCart(sessionId = getSessionIdentifier()) {
    saveCart([], sessionId);
  }

  function findBook(bookId) {
    return BOOKS.find((book) => book.id === Number(bookId));
  }

  function getBookStock(bookId) {
    const inventory = getInventory();
    const book = findBook(bookId);
    return Number(inventory[bookId] ?? book?.stock ?? 0);
  }

  function getCartItems(sessionId = getSessionIdentifier()) {
    return getCart(sessionId)
      .map((item) => {
        const book = findBook(item.bookId);
        if (!book) {
          return null;
        }
        return {
          ...book,
          quantity: item.quantity,
          lineTotal: book.price * item.quantity,
          stock: getBookStock(book.id),
        };
      })
      .filter(Boolean);
  }

  function getCartCount(sessionId = getSessionIdentifier()) {
    return getCart(sessionId).reduce((count, item) => count + item.quantity, 0);
  }

  function getCartSubtotal(sessionId = getSessionIdentifier()) {
    return getCartItems(sessionId).reduce((total, item) => total + item.lineTotal, 0);
  }

  function formatCurrency(amount) {
    return `$${Number(amount).toFixed(2)}`;
  }

  function formatDate(value) {
    return new Date(value).toLocaleString([], { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[character]);
  }

  function renderSessionLabels() {
    const session = getSession();
    const user = getCurrentUser(session);
    const label = session.kind === "guest"
      ? `Guest session · ${session.id.slice(-6)}`
      : `${session.kind === "admin" ? "Admin" : "User"} · ${user?.name || session.name}`;

    document.querySelectorAll("[data-session-label]").forEach((element) => {
      element.textContent = label;
    });

    document.querySelectorAll("[data-cart-count]").forEach((element) => {
      element.textContent = String(getCartCount());
    });
  }

  function highlightActiveNav() {
    const page = document.body.dataset.page || "catalog";
    document.querySelectorAll("[data-page-link]").forEach((link) => {
      link.classList.toggle("active", link.dataset.pageLink === page);
    });
  }

  function setMessage(targetId, message, tone = "info") {
    const target = document.getElementById(targetId);
    if (!target) {
      return;
    }
    target.textContent = message;
    target.classList.remove("message-info", "message-success", "message-error");
    target.classList.add(`message-${tone}`);
  }

  function addToCart(bookId, quantity = 1) {
    const book = findBook(bookId);
    if (!book) {
      return { ok: false, message: "Book not found." };
    }
    const sessionId = getSessionIdentifier();
    const cart = getCart(sessionId);
    const entry = cart.find((item) => item.bookId === book.id);
    const nextQuantity = (entry?.quantity || 0) + quantity;
    if (nextQuantity > getBookStock(book.id)) {
      return { ok: false, message: `Only ${getBookStock(book.id)} left in stock.` };
    }
    if (entry) {
      entry.quantity = nextQuantity;
    } else {
      cart.push({ bookId: book.id, quantity });
    }
    saveCart(cart, sessionId);
    return { ok: true, message: `${book.title} added to cart.` };
  }

  function updateCartItem(bookId, quantity) {
    const sessionId = getSessionIdentifier();
    const cart = getCart(sessionId);
    const entry = cart.find((item) => item.bookId === Number(bookId));
    if (!entry) {
      return;
    }
    if (quantity <= 0) {
      saveCart(cart.filter((item) => item.bookId !== Number(bookId)), sessionId);
      return;
    }
    if (quantity > getBookStock(bookId)) {
      return;
    }
    entry.quantity = quantity;
    saveCart(cart, sessionId);
  }

  function removeCartItem(bookId) {
    const sessionId = getSessionIdentifier();
    saveCart(getCart(sessionId).filter((item) => item.bookId !== Number(bookId)), sessionId);
  }

  function addOrderEvent(order, label) {
    order.events = Array.isArray(order.events) ? order.events : [];
    order.events.unshift({ label, at: Date.now() });
  }

  function updateOrder(orderId, updates) {
    const orders = getOrders();
    const index = orders.findIndex((order) => order.id === orderId);
    if (index === -1) {
      return null;
    }
    const updated = { ...orders[index], ...updates };
    orders[index] = updated;
    saveOrders(orders);
    return updated;
  }

  function placeOrder(paymentData) {
    const session = getSession();
    const sessionId = getSessionIdentifier(session);
    const cartItems = getCartItems(sessionId);
    if (cartItems.length === 0) {
      return { ok: false, message: "Your cart is empty." };
    }

    const inventory = getInventory();
    for (const item of cartItems) {
      if (item.quantity > Number(inventory[item.id] ?? 0)) {
        return { ok: false, message: `Not enough stock for ${item.title}.` };
      }
    }

    cartItems.forEach((item) => {
      inventory[item.id] = Number(inventory[item.id] ?? 0) - item.quantity;
    });
    saveInventory(inventory);

    const order = {
      id: `ORD-${Date.now().toString(36).toUpperCase()}`,
      sessionId,
      userId: session.kind === "guest" ? null : session.userId,
      sessionKind: session.kind,
      customerName: paymentData.fullName || session.name || "Guest",
      customerEmail: paymentData.email || "",
      address: paymentData.address || "",
      shippingMethod: paymentData.shippingMethod,
      paymentMethod: paymentData.paymentMethod,
      status: "Payment confirmed",
      shippingStatus: paymentData.shippingMethod === "pickup" ? "Allocated for pickup" : "Allocated to post",
      trackingStatus: "Processing",
      total: cartItems.reduce((sum, item) => sum + item.lineTotal, 0),
      items: cartItems.map((item) => ({ bookId: item.id, title: item.title, quantity: item.quantity, price: item.price, lineTotal: item.lineTotal })),
      createdAt: Date.now(),
      events: [],
    };

    addOrderEvent(order, "Payment confirmed");
    addOrderEvent(order, order.shippingMethod === "pickup" ? "Pickup allocation created" : "Post allocation created");

    const orders = getOrders();
    orders.unshift(order);
    saveOrders(orders);
    clearCart(sessionId);
    return { ok: true, order };
  }

  function getOrdersForSession(sessionId = getSessionIdentifier()) {
    return getOrders().filter((order) => order.sessionId === sessionId);
  }

  function getLatestOrderForSession(sessionId = getSessionIdentifier()) {
    return getOrdersForSession(sessionId).sort((left, right) => right.createdAt - left.createdAt)[0] || null;
  }

  function loginSession(user) {
    saveSession({ kind: user.role, userId: user.id, id: `${user.role}-${user.id}`, name: user.name });
  }

  window.BookStore = {
    STORAGE_KEYS,
    BOOKS,
    getUsers,
    saveUsers,
    getInventory,
    saveInventory,
    getOrders,
    saveOrders,
    createGuestSession,
    getSession,
    saveSession,
    getCurrentUser,
    getSessionIdentifier,
    getCart,
    saveCart,
    clearCart,
    findBook,
    getBookStock,
    getCartItems,
    getCartCount,
    getCartSubtotal,
    formatCurrency,
    formatDate,
    escapeHtml,
    renderSessionLabels,
    highlightActiveNav,
    setMessage,
    addToCart,
    updateCartItem,
    removeCartItem,
    addOrderEvent,
    updateOrder,
    placeOrder,
    getOrdersForSession,
    getLatestOrderForSession,
    loginSession,
  };
})();
