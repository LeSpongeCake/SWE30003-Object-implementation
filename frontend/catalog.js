(() => {
  const store = window.BookStore;
  const PAGE = document.body.dataset.page || "catalog";
  const { BOOKS, findBook, formatCurrency, escapeHtml, getCart, getCartCount, getBookStock, addToCart, removeCartItem, renderSessionLabels, highlightActiveNav } = store;

  function renderCatalogPage() {
    const bookGrid = document.getElementById("bookGrid");
    const searchInput = document.getElementById("searchInput");
    const sortSelect = document.getElementById("sortSelect");
    const chips = document.querySelectorAll("[data-genre]");
    const resultSummary = document.getElementById("resultSummary");
    const totalBooks = document.getElementById("totalBooks");
    const cartCount = document.getElementById("catalogCartCount");
    const modal = document.getElementById("detailsModal");
    const modalGenre = document.getElementById("modalGenre");
    const modalTitle = document.getElementById("modalTitle");
    const modalMeta = document.getElementById("modalMeta");
    const modalSummary = document.getElementById("modalSummary");
    const modalSaveBtn = document.getElementById("modalSaveBtn");
    const state = { query: "", genre: "all", sort: "featured", selectedBookId: null };

    function getFilteredBooks() {
      const query = state.query.trim().toLowerCase();
      let filtered = BOOKS.filter((book) => {
        const haystack = [book.title, book.author, book.genreLabel, book.tag, book.summary].join(" ").toLowerCase();
        return (!query || haystack.includes(query)) && (state.genre === "all" || book.genreKey === state.genre);
      });
      if (state.sort === "title") {
        filtered = filtered.slice().sort((left, right) => left.title.localeCompare(right.title));
      } else if (state.sort === "year-desc") {
        filtered = filtered.slice().sort((left, right) => right.year - left.year);
      }
      return filtered;
    }

    function syncModalAction(bookId) {
      const saved = getCart().some((item) => item.bookId === bookId);
      modalSaveBtn.textContent = saved ? "Remove from cart" : "Add to cart";
      modalSaveBtn.classList.toggle("saved", saved);
    }

    function openDetails(bookId) {
      const book = findBook(bookId);
      if (!book || !modal) {
        return;
      }
      state.selectedBookId = bookId;
      modalGenre.textContent = book.genreLabel;
      modalTitle.textContent = book.title;
      modalMeta.textContent = `${book.author} · ${book.year} · ${formatCurrency(book.price)}`;
      modalSummary.textContent = `${book.summary} Stock: ${getBookStock(book.id)}.`;
      syncModalAction(book.id);
      modal.hidden = false;
    }

    function closeDetails() {
      if (modal) {
        modal.hidden = true;
      }
      state.selectedBookId = null;
    }

    function renderBooks() {
      const filtered = getFilteredBooks();
      bookGrid.innerHTML = "";
      if (filtered.length === 0) {
        bookGrid.innerHTML = `<article class="book-card"><h3>No books found</h3><p class="summary">Try a different search term or switch back to all genres.</p></article>`;
      } else {
        filtered.forEach((book) => {
          const card = document.createElement("article");
          card.className = "book-card";
          const inCart = getCart().some((item) => item.bookId === book.id);
          card.innerHTML = `
            <div class="book-badge">${escapeHtml(book.tag)}</div>
            <h3>${escapeHtml(book.title)}</h3>
            <p class="meta">${escapeHtml(book.author)} · ${book.year}</p>
            <p class="summary">${escapeHtml(book.summary)}</p>
            <div class="book-meta-row"><span>${escapeHtml(book.genreLabel)}</span><span>${formatCurrency(book.price)}</span><span>${getBookStock(book.id)} in stock</span></div>
            <div class="card-actions"><button class="details-btn" type="button" data-action="details">View details</button><button class="save-btn ${inCart ? "saved" : ""}" type="button" data-action="cart">${inCart ? "In cart" : "Add to cart"}</button></div>
          `;
          card.querySelector('[data-action="details"]').addEventListener("click", () => openDetails(book.id));
          card.querySelector('[data-action="cart"]').addEventListener("click", () => {
            const result = inCart ? { ok: true, message: "Already in cart." } : addToCart(book.id, 1);
            if (result.ok) {
              renderSessionLabels();
              renderBooks();
            }
          });
          bookGrid.appendChild(card);
        });
      }
      resultSummary.textContent = `${filtered.length} book${filtered.length === 1 ? "" : "s"} shown`;
      totalBooks.textContent = String(BOOKS.length);
      cartCount.textContent = String(getCartCount());
    }

    searchInput?.addEventListener("input", (event) => {
      state.query = event.target.value;
      renderBooks();
    });
    sortSelect?.addEventListener("change", (event) => {
      state.sort = event.target.value;
      renderBooks();
    });
    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        state.genre = chip.dataset.genre || "all";
        chips.forEach((button) => button.classList.toggle("active", button === chip));
        renderBooks();
      });
    });
    modal?.querySelectorAll("[data-close]").forEach((button) => button.addEventListener("click", closeDetails));
    modalSaveBtn?.addEventListener("click", () => {
      if (state.selectedBookId === null) {
        return;
      }
      if (getCart().some((item) => item.bookId === state.selectedBookId)) {
        removeCartItem(state.selectedBookId);
      } else {
        addToCart(state.selectedBookId, 1);
      }
      syncModalAction(state.selectedBookId);
      renderBooks();
    });
    modal?.addEventListener("click", (event) => {
      if (event.target.matches("[data-close]")) {
        closeDetails();
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && modal && !modal.hidden) {
        closeDetails();
      }
    });
    renderBooks();
  }

  if (PAGE === "catalog") {
    store.renderSessionLabels();
    store.highlightActiveNav();
    renderCatalogPage();
  }
})();
