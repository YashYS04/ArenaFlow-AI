// ArenaFlow Interactive Client Controller
/* global I18N, drawStadiumEdges, clearRouteHighlights, highlightRouteSteps, setupMapInteraction */

// State Variables
let currentLanguage = "en";
let currentPersona = "fan";
let ttsEnabled = false;
let currentMetadata = null;
let activeIncidents = [];

// DOM Elements
const languageSelect = document.getElementById("language");
const personaToggle = document.getElementById("persona-toggle");
const ttsToggle = document.getElementById("tts-toggle");
const contrastToggle = document.getElementById("contrast-toggle");
const assistForm = document.getElementById("assist-form");
const currentLocationSelect = document.getElementById("current_location");
const destinationIntentSelect = document.getElementById("destination_intent");
const incidentLocationSelect = document.getElementById("incident_location");
const resultDiv = document.getElementById("result");
const speakBtn = document.getElementById("speak-btn");
const stadiumMetaP = document.getElementById("stadium-meta");

const staffCard = document.getElementById("staff-card");
const incidentForm = document.getElementById("incident-form");
const incidentsListDiv = document.getElementById("incidents-list");

// Init App
document.addEventListener("DOMContentLoaded", async () => {
  setupLanguageListener();
  setupSettingsListeners();
  setupFormListeners();

  setupMapInteraction((zoneId, zoneEl) => {
    if (currentPersona === "staff") {
      incidentLocationSelect.value = zoneId;
    } else {
      currentLocationSelect.value = zoneId;
    }
    clearRouteHighlights();
    zoneEl.classList.add("active-start");
  });

  await fetchStadiumMetadata();
  localizeUI(currentLanguage);
});

// Localization Engine
function setupLanguageListener() {
  languageSelect.addEventListener("change", (e) => {
    currentLanguage = e.target.value;
    document.documentElement.lang = currentLanguage;
    localizeUI(currentLanguage);
    if (currentMetadata) {
      submitAssistForm();
    }
  });
}

function localizeUI(lang) {
  const dict = I18N[lang] || I18N.en;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
        el.placeholder = dict[key];
      } else {
        el.textContent = dict[key];
      }
    }
  });

  personaToggle.textContent = currentPersona === "fan" ? dict.toggleStaff : dict.toggleFan;
  ttsToggle.textContent = ttsEnabled ? dict.toggleSpeechOn : dict.toggleSpeech;

  updateDropdownsLanguage(lang);
  renderIncidentsList();
}

function updateDropdownsLanguage(lang) {
  if (!currentMetadata) return;
  const dict = I18N[lang] || I18N.en;

  const currentLocVal = currentLocationSelect.value;
  const currentDestVal = destinationIntentSelect.value;
  const currentIncVal = incidentLocationSelect.value;

  currentLocationSelect.innerHTML = "";
  destinationIntentSelect.innerHTML = "";
  incidentLocationSelect.innerHTML = "";

  currentMetadata.zones.forEach((z) => {
    const locName = z.name[lang] || z.name.en || z.id;
    currentLocationSelect.add(new Option(locName, z.id));
    incidentLocationSelect.add(new Option(locName, z.id));
  });

  currentMetadata.intents.forEach((intent) => {
    const label = dict[intent] || intent.replace("_", " ");
    destinationIntentSelect.add(new Option(label, intent));
  });

  if (currentLocVal) currentLocationSelect.value = currentLocVal;
  if (currentDestVal) destinationIntentSelect.value = currentDestVal;
  if (currentIncVal) incidentLocationSelect.value = currentIncVal;
}

// Fetch Stadium Data & Draw Edges
async function fetchStadiumMetadata() {
  try {
    const res = await fetch("/api/stadium");
    if (!res.ok) throw new Error("Failed to load stadium metadata");
    currentMetadata = await res.json();

    const fifaName = (I18N[currentLanguage] && I18N[currentLanguage].metlifeFifaName) || "New York New Jersey Stadium";
    stadiumMetaP.innerHTML = `<strong>${currentMetadata.stadium.name}</strong> (${fifaName}) · Capacity: ${currentMetadata.stadium.capacity.toLocaleString()}`;

    updateDropdownsLanguage(currentLanguage);
    drawStadiumEdges();
  } catch (err) {
    console.error(err);
  }
}

// Settings Controls
function setupSettingsListeners() {
  personaToggle.addEventListener("click", () => {
    currentPersona = currentPersona === "fan" ? "staff" : "fan";
    if (currentPersona === "staff") {
      staffCard.classList.remove("hidden");
      personaToggle.setAttribute("aria-pressed", "true");
      fetchIncidents();
    } else {
      staffCard.classList.add("hidden");
      personaToggle.setAttribute("aria-pressed", "false");
    }
    localizeUI(currentLanguage);
  });

  ttsToggle.addEventListener("click", () => {
    ttsEnabled = !ttsEnabled;
    ttsToggle.setAttribute("aria-pressed", String(ttsEnabled));
    if (!ttsEnabled && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    localizeUI(currentLanguage);
  });

  contrastToggle.addEventListener("click", () => {
    const isHiVis = document.body.classList.toggle("hi-vis");
    contrastToggle.setAttribute("aria-pressed", String(isHiVis));
  });

  speakBtn.addEventListener("click", () => {
    speakDirections();
  });
}

function setupFormListeners() {
  assistForm.addEventListener("submit", (e) => {
    e.preventDefault();
    submitAssistForm();
  });

  incidentForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    await submitIncidentForm();
  });
}

async function submitAssistForm() {
  const checkedNeeds = Array.from(document.querySelectorAll('input[name="need"]:checked')).map((cb) => cb.value);
  const payload = {
    persona: currentPersona,
    language: currentLanguage,
    current_location: currentLocationSelect.value,
    destination_intent: destinationIntentSelect.value,
    accessibility_needs: checkedNeeds,
    ticket_section: document.getElementById("ticket_section").value || null,
    minutes_to_kickoff: parseInt(document.getElementById("minutes_to_kickoff").value, 10),
    question: document.getElementById("question").value || null
  };

  resultDiv.setAttribute("aria-busy", "true");
  speakBtn.classList.add("hidden");
  if (window.speechSynthesis) window.speechSynthesis.cancel();

  resultDiv.innerHTML = `
    <div class="meta-badges">
      <span class="badge">Computing Route...</span>
    </div>
    <div class="answer-text"></div>
  `;

  try {
    const res = await fetch("/api/assist/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.status === 429) {
      const retryAfter = res.headers.get("Retry-After") || 5;
      showError(`Too many requests. Please wait ${retryAfter}s.`);
      return;
    }
    if (!res.ok) {
      const errData = await res.json();
      showError(errData.detail || "Route computation failed");
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let textContainer = resultDiv.querySelector(".answer-text");
    let fullText = "";
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const blocks = buffer.split("\n\n");
      buffer = blocks.pop() || "";

      for (const block of blocks) {
        if (!block.trim()) continue;
        let eventType = "message";
        let dataPayload = "";

        const lines = block.split("\n");
        for (const line of lines) {
          if (line.startsWith("event:")) {
            eventType = line.slice(6).trim();
          } else if (line.startsWith("data:")) {
            const part = line.slice(5).trim();
            dataPayload = dataPayload ? `${dataPayload}\n${part}` : part;
          }
        }

        if (!dataPayload) continue;

        if (eventType === "metadata") {
          const metadata = JSON.parse(dataPayload);
          renderRouteMetadata(metadata);
          textContainer = resultDiv.querySelector(".answer-text");
          highlightRouteSteps(metadata.route_steps, metadata.facility.zone);
        } else if (eventType === "token") {
          const token = dataPayload.replace(/\\n/g, "\n");
          fullText += token;
          if (textContainer) textContainer.textContent = fullText;
        } else if (eventType === "result") {
          const finalResult = JSON.parse(dataPayload);
          if (textContainer) {
            textContainer.textContent = finalResult.answer;
            textContainer.classList.add("done");
          }
          resultDiv.setAttribute("aria-busy", "false");
          speakBtn.classList.remove("hidden");
          if (ttsEnabled) speakDirections();
        }
      }
    }
  } catch (err) {
    showError(err.message);
  }
}

function renderRouteMetadata(metadata) {
  const dict = I18N[currentLanguage] || I18N.en;
  const crowdClass = `crowd-${metadata.crowd_level}`;

  let noticeHtml = "";
  if (metadata.urgency) {
    noticeHtml = `<div class="notice urgent">${metadata.urgency}</div>`;
  } else if (metadata.alternatives_note) {
    noticeHtml = `<div class="notice">${metadata.alternatives_note}</div>`;
  }

  let stepsHtml = "";
  if (metadata.route_steps && metadata.route_steps.length > 0) {
    stepsHtml = `
      <h3>${dict.routeHeading}</h3>
      <ol class="route-steps">
        ${metadata.route_steps.map((s) => `<li>${s.instruction} <span class="step-means">${s.means}</span></li>`).join("")}
      </ol>
    `;
  }

  resultDiv.innerHTML = `
    <div class="meta-badges">
      <span class="badge ${crowdClass}">${dict.crowdLabel} ${metadata.crowd_level}</span>
      <span class="badge">${dict.modeLabel} ${metadata.accessibility_mode}</span>
    </div>
    ${noticeHtml}
    ${stepsHtml}
    <div class="answer-text"></div>
  `;
}

function showError(msg) {
  resultDiv.setAttribute("aria-busy", "false");
  resultDiv.innerHTML = `<div class="error-msg">${msg}</div>`;
}

function speakDirections() {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const text = resultDiv.innerText || resultDiv.textContent;
  if (!text) return;

  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = currentLanguage === "fr" ? "fr-FR" : currentLanguage === "es" ? "es-ES" : "en-US";
  window.speechSynthesis.speak(utter);
}

// Staff Incident Management
async function fetchIncidents() {
  try {
    const res = await fetch("/api/incidents");
    if (!res.ok) return;
    activeIncidents = await res.json();
    renderIncidentsList();
  } catch (e) {
    console.error(e);
  }
}

function renderIncidentsList() {
  if (!incidentsListDiv) return;
  const dict = I18N[currentLanguage] || I18N.en;
  const unresolved = activeIncidents.filter((inc) => !inc.resolved);

  if (unresolved.length === 0) {
    incidentsListDiv.innerHTML = `<p class="muted">${dict.noIncidents}</p>`;
    return;
  }

  incidentsListDiv.innerHTML = unresolved.map((inc) => `
    <div class="incident-item">
      <div>
        <strong>${inc.issue_type.toUpperCase()}</strong> · Zone: <em>${inc.zone_id}</em>
        <p>${inc.description}</p>
      </div>
      <button type="button" class="resolve-btn" onclick="resolveIncident('${inc.id}')">Resolve</button>
    </div>
  `).join("");
}

async function submitIncidentForm() {
  const payload = {
    persona: "staff",
    language: currentLanguage,
    current_location: incidentLocationSelect.value,
    destination_intent: "first_aid",
    accessibility_needs: [],
    minutes_to_kickoff: 30,
    incident_report: document.getElementById("incident_desc").value,
    reported_issue_type: document.getElementById("incident_type").value
  };

  try {
    const res = await fetch("/api/assist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      document.getElementById("incident_desc").value = "";
      await fetchIncidents();
    }
  } catch (err) {
    console.error(err);
  }
}

window.resolveIncident = async function(id) {
  try {
    const res = await fetch(`/api/incidents/${id}/resolve`, { method: "POST" });
    if (res.ok) {
      await fetchIncidents();
    }
  } catch (err) {
    console.error(err);
  }
};
