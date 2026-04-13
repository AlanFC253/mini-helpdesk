const API_BASE_URL = "http://127.0.0.1:8000";

const state = {
  currentPage: 1,
  currentPages: 1,
  isLoading: false,
};

const elements = {
  loginForm: document.getElementById("loginForm"),
  loginMessage: document.getElementById("loginMessage"),
  authStatus: document.getElementById("authStatus"),
  logoutBtn: document.getElementById("logoutBtn"),

  filtersForm: document.getElementById("filtersForm"),
  clearFiltersBtn: document.getElementById("clearFiltersBtn"),

  createTicketForm: document.getElementById("createTicketForm"),
  createMessage: document.getElementById("createMessage"),

  editTicketForm: document.getElementById("editTicketForm"),
  cancelEditBtn: document.getElementById("cancelEditBtn"),
  editMessage: document.getElementById("editMessage"),

  ticketsMeta: document.getElementById("ticketsMeta"),
  ticketsContainer: document.getElementById("ticketsContainer"),

  prevPageBtn: document.getElementById("prevPageBtn"),
  nextPageBtn: document.getElementById("nextPageBtn"),

  editId: document.getElementById("edit_id"),
  editTitle: document.getElementById("edit_title"),
  editDescription: document.getElementById("edit_description"),
  editPriority: document.getElementById("edit_priority"),
  editStatus: document.getElementById("edit_status"),

  sort: document.getElementById("sort"),
  order: document.getElementById("order"),
  pageSize: document.getElementById("page_size"),
  ticketPriority: document.getElementById("ticket_priority"),
};

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

function setMessage(element, text) {
  element.textContent = text;
}

function clearMessages() {
  setMessage(elements.loginMessage, "");
  setMessage(elements.createMessage, "");
  setMessage(elements.editMessage, "");
}

function updateAuthUI() {
  const isAuthenticated = Boolean(getToken());

  elements.authStatus.textContent = isAuthenticated
    ? "Autenticado"
    : "Não autenticado";

  elements.logoutBtn.classList.toggle("hidden", !isAuthenticated);
}

function updatePaginationButtons() {
  elements.prevPageBtn.disabled = state.currentPage <= 1 || state.isLoading;
  elements.nextPageBtn.disabled =
    state.currentPage >= state.currentPages || state.isLoading;
}

function setLoading(isLoading) {
  state.isLoading = isLoading;
  updatePaginationButtons();
}

function buildQueryParams() {
  const formData = new FormData(elements.filtersForm);
  const params = new URLSearchParams();

  params.set("page", String(state.currentPage));

  for (const [key, value] of formData.entries()) {
    if (!value) continue;

    if (key === "created_from" || key === "created_to") {
      params.set(key, new Date(value).toISOString());
      continue;
    }

    params.set(key, value);
  }

  return params.toString();
}

async function apiRequest(path, options = {}) {
  const token = getToken();
  const headers = new Headers(options.headers || {});

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  return fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });
}

async function login(username, password) {
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Falha no login");
  }

  return data;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeJs(value) {
  return String(value)
    .replaceAll("\\", "\\\\")
    .replaceAll("'", "\\'")
    .replaceAll("\n", "\\n")
    .replaceAll("\r", "");
}

function renderTicketsMeta(data) {
  elements.ticketsMeta.innerHTML = `
    <p>
      <strong>Total:</strong> ${data.total}
      | <strong>Página:</strong> ${data.page} de ${data.pages}
      | <strong>Por página:</strong> ${data.page_size}
    </p>
  `;
}

function renderTickets(tickets) {
  if (!Array.isArray(tickets)) {
    elements.ticketsContainer.innerHTML =
      "<p>Formato de resposta inválido.</p>";
    return;
  }

  if (tickets.length === 0) {
    elements.ticketsContainer.innerHTML = "<p>Nenhum ticket encontrado.</p>";
    return;
  }

  const isAuthenticated = Boolean(getToken());

  elements.ticketsContainer.innerHTML = tickets
    .map(
      (ticket) => `
        <div class="ticket">
          <h3>${escapeHtml(ticket.title)}</h3>
          <p><strong>ID:</strong> ${ticket.id}</p>
          <p><strong>Status:</strong> ${ticket.status}</p>
          <p><strong>Prioridade:</strong> ${ticket.priority}</p>
          <p><strong>Descrição:</strong> ${escapeHtml(ticket.description ?? "Sem descrição")}</p>

          ${
            isAuthenticated
              ? `
              <div class="ticket-actions">
                <button
                  onclick="startEditTicket(${ticket.id}, '${escapeJs(ticket.title)}', '${escapeJs(ticket.description ?? "")}', '${ticket.priority}', '${ticket.status}')"
                >
                  Editar
                </button>
                <button class="danger" onclick="deleteTicket(${ticket.id})">
                  Deletar
                </button>
              </div>
            `
              : ""
          }
        </div>
      `
    )
    .join("");
}

async function loadTickets() {
  setLoading(true);
  elements.ticketsMeta.innerHTML = "<p>Carregando informações...</p>";
  elements.ticketsContainer.innerHTML = "<p>Carregando tickets...</p>";

  try {
    const query = buildQueryParams();
    const response = await apiRequest(`/tickets/?${query}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `Erro HTTP: ${response.status}`);
    }

    state.currentPage = data.page;
    state.currentPages = data.pages;

    renderTicketsMeta(data);
    renderTickets(data.items);
  } catch (error) {
    elements.ticketsMeta.innerHTML = "<p>Não foi possível carregar os dados.</p>";
    elements.ticketsContainer.innerHTML = `<p>Erro ao carregar tickets: ${error.message}</p>`;
  } finally {
    setLoading(false);
  }
}

function hideEditForm() {
  elements.editTicketForm.classList.add("hidden");
  elements.editTicketForm.reset();
  setMessage(elements.editMessage, "");
}

function showEditForm() {
  elements.editTicketForm.classList.remove("hidden");
}

window.startEditTicket = function (id, title, description, priority, status) {
  if (!getToken()) {
    alert("Você precisa estar logado para editar.");
    return;
  }

  elements.editId.value = id;
  elements.editTitle.value = title;
  elements.editDescription.value = description;
  elements.editPriority.value = priority;
  elements.editStatus.value = status;

  showEditForm();
  setMessage(elements.editMessage, "");
  window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
};

window.deleteTicket = async function (id) {
  if (!getToken()) {
    alert("Você precisa estar logado para deletar.");
    return;
  }

  const confirmed = confirm(`Deseja deletar o ticket ${id}?`);
  if (!confirmed) return;

  try {
    const response = await apiRequest(`/tickets/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      let errorMessage = `Erro HTTP: ${response.status}`;

      try {
        const data = await response.json();
        errorMessage = data.detail || errorMessage;
      } catch {
      }

      throw new Error(errorMessage);
    }

    alert("Ticket deletado com sucesso.");
    await loadTickets();
  } catch (error) {
    alert(error.message);
  }
};

elements.loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();

  const formData = new FormData(elements.loginForm);
  const username = formData.get("username");
  const password = formData.get("password");

  try {
    const data = await login(username, password);
    setToken(data.access_token);
    updateAuthUI();
    setMessage(elements.loginMessage, "Login realizado com sucesso.");
    await loadTickets();
  } catch (error) {
    setMessage(elements.loginMessage, error.message);
  }
});

elements.logoutBtn.addEventListener("click", async () => {
  clearToken();
  updateAuthUI();
  hideEditForm();
  setMessage(elements.loginMessage, "Logout realizado.");
  await loadTickets();
});

elements.filtersForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  state.currentPage = 1;
  await loadTickets();
});

elements.clearFiltersBtn.addEventListener("click", async () => {
  elements.filtersForm.reset();
  elements.sort.value = "created_at";
  elements.order.value = "desc";
  elements.pageSize.value = "10";
  state.currentPage = 1;
  await loadTickets();
});

elements.createTicketForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();

  const payload = {
    title: elements.createTicketForm.title.value,
    description: elements.createTicketForm.description.value,
    priority: elements.createTicketForm.priority.value,
  };

  try {
    const response = await apiRequest("/tickets/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao criar ticket");
    }

    setMessage(elements.createMessage, "Ticket criado com sucesso.");
    elements.createTicketForm.reset();
    elements.ticketPriority.value = "medium";
    state.currentPage = 1;
    await loadTickets();
  } catch (error) {
    setMessage(elements.createMessage, error.message);
  }
});

elements.editTicketForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setMessage(elements.editMessage, "");

  const id = elements.editId.value;

  const payload = {
    title: elements.editTitle.value,
    description: elements.editDescription.value,
    priority: elements.editPriority.value,
    status: elements.editStatus.value,
  };

  try {
    const response = await apiRequest(`/tickets/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao editar ticket");
    }

    setMessage(elements.editMessage, "Ticket atualizado com sucesso.");
    hideEditForm();
    await loadTickets();
  } catch (error) {
    setMessage(elements.editMessage, error.message);
  }
});

elements.cancelEditBtn.addEventListener("click", () => {
  hideEditForm();
});

elements.prevPageBtn.addEventListener("click", async () => {
  if (state.currentPage > 1) {
    state.currentPage -= 1;
    await loadTickets();
  }
});

elements.nextPageBtn.addEventListener("click", async () => {
  if (state.currentPage < state.currentPages) {
    state.currentPage += 1;
    await loadTickets();
  }
});

updateAuthUI();
updatePaginationButtons();
loadTickets();