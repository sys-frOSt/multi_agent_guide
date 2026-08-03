const form = document.getElementById("planner-form");
const input = document.getElementById("user-query");
const submitButton = document.getElementById("submit-btn");
const resultPanel = document.getElementById("result-panel");

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  submitButton.textContent = isLoading ? "Planning..." : "Generate itinerary";
}

function renderResult(data) {
  const response = data.response || "No plan was produced yet.";
  const messages = data.messages || [];

  resultPanel.innerHTML = `
    <div class="result-card">
      <span class="status-pill">Plan ready</span>
      <h2>Your travel outline</h2>
      <p>${response.replace(/\n/g, "<br />")}</p>
      ${messages.length ? `<ul>${messages.map((msg) => `<li>${msg.replace(/\n/g, "<br />")}</li>`).join("")}</ul>` : ""}
      <p><strong>LLM calls:</strong> ${data.llm_calls ?? 0}</p>
    </div>
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userQuery = input.value.trim();

  if (!userQuery) {
    resultPanel.innerHTML = `
      <div class="result-placeholder">
        <h2>Tell us where you want to go</h2>
        <p>Share a short destination, timing, and budget to start planning.</p>
      </div>
    `;
    return;
  }

  setLoading(true);
  resultPanel.innerHTML = `
    <div class="result-placeholder">
      <h2>Crafting your plan</h2>
      <p>One moment while the agents gather the best options.</p>
    </div>
  `;

  try {
    const response = await fetch("/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_query: userQuery }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "The planner could not create a trip plan.");
    }

    renderResult(payload);
  } catch (error) {
    resultPanel.innerHTML = `
      <div class="result-placeholder">
        <h2>Planning paused</h2>
        <p>${error.message}</p>
      </div>
    `;
  } finally {
    setLoading(false);
  }
});
