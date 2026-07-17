// ArenaFlow Interactive Client Engine

// Localized UI Texts
const I18N = {
  en: {
    tagline: "Smart Operations & Wayfinding · FIFA World Cup 2026",
    skipLink: "Skip to main content",
    language: "Language",
    toggleStaff: "Switch to Staff Mode",
    toggleFan: "Switch to Fan Mode",
    toggleSpeech: "Voice Guidance Off",
    toggleSpeechOn: "Voice Guidance On",
    highVisibility: "High-visibility Mode",
    yourContext: "Your context",
    whereNow: "Where are you now?",
    whereGo: "Where do you want to go?",
    accessNeeds: "Accessibility needs",
    needWheelchair: "Wheelchair / step-free",
    needVisual: "Low vision / voice assistance",
    needHearing: "Deaf / hard of hearing",
    ticketSection: "Section (optional)",
    minutesToKickoff: "Minutes to kick-off",
    question: "Ask a question (optional)",
    questionHint: "Free text is treated strictly as data, never as commands.",
    getHelp: "Get help",
    assistance: "Assistance",
    placeholder: "Fill in your context and select “Get help”. Your AI assistant response will stream here.",
    stadiumMap: "Interactive Stadium Map",
    staffOperations: "Staff Operations Panel",
    incidentLocation: "Incident Zone",
    incidentType: "Issue Type",
    incidentDesc: "Details / Action required",
    reportIncident: "Log & Route Incident",
    activeIncidents: "Active Incidents",
    noIncidents: "No active incidents logged.",
    spill: "Spill (Block Zone)",
    congestion: "Congestion (High Delay)",
    maintenance: "Maintenance (Block Zone)",
    medical: "Medical emergency (Block Zone)",
    meansWalk: "Walk",
    meansRamp: "Ramp",
    meansElevator: "Elevator",
    meansStairs: "Stairs",
    crowdLabel: "Crowd: ",
    modeLabel: "Access Mode: ",
    routeHeading: "Route Directions:",
    metlifeFifaName: "New York New Jersey Stadium",
    grounding: "Answers are grounded in verified stadium layouts. The AI cannot hallucinate routes."
  },
  es: {
    tagline: "Operaciones Inteligentes y Orientación · Copa Mundial de la FIFA 2026",
    skipLink: "Saltar al contenido principal",
    language: "Idioma",
    toggleStaff: "Cambiar a Modo Personal",
    toggleFan: "Cambiar a Modo Aficionado",
    toggleSpeech: "Guía de Voz Desactivada",
    toggleSpeechOn: "Guía de Voz Activada",
    highVisibility: "Modo Alta Visibilidad",
    yourContext: "Su contexto",
    whereNow: "¿Dónde se encuentra ahora?",
    whereGo: "¿A dónde desea ir?",
    accessNeeds: "Necesidades de accesibilidad",
    needWheelchair: "Silla de ruedas / paso libre de escaleras",
    needVisual: "Baja visión / asistencia de voz",
    needHearing: "Sordo / dificultad auditiva",
    ticketSection: "Sección (opcional)",
    minutesToKickoff: "Minutos para el inicio",
    question: "Hacer una pregunta (opcional)",
    questionHint: "El texto libre se trata estrictamente como datos, nunca como comandos.",
    getHelp: "Obtener ayuda",
    assistance: "Asistencia",
    placeholder: "Complete su contexto y seleccione \"Obtener ayuda\". La respuesta de su asistente de IA se transmitirá aquí.",
    stadiumMap: "Mapa Interactivo del Estadio",
    staffOperations: "Panel de Operaciones de Personal",
    incidentLocation: "Zona del Incidente",
    incidentType: "Tipo de Problema",
    incidentDesc: "Detalles / Acción requerida",
    reportIncident: "Registrar y Enrutar Incidente",
    activeIncidents: "Incidentes Activos",
    noIncidents: "No hay incidentes activos registrados.",
    spill: "Derrame (Bloquear Zona)",
    congestion: "Congestión (Retraso Alto)",
    maintenance: "Mantenimiento (Bloquear Zona)",
    medical: "Emergencia médica (Bloquear Zona)",
    meansWalk: "Caminar",
    meansRamp: "Rampa",
    meansElevator: "Ascensor",
    meansStairs: "Escaleras",
    crowdLabel: "Afluencia: ",
    modeLabel: "Accesibilidad: ",
    routeHeading: "Indicaciones de Ruta:",
    metlifeFifaName: "Estadio de Nueva York Nueva Jersey",
    grounding: "Las respuestas se basan en distribuciones verificadas del estadio. La IA no puede inventar rutas."
  },
  fr: {
    tagline: "Opérations Intelligentes & Orientation · Coupe du Monde de la FIFA 2026",
    skipLink: "Passer au contenu principal",
    language: "Langue",
    toggleStaff: "Passer en Mode Personnel",
    toggleFan: "Passer en Mode Supporter",
    toggleSpeech: "Guidage Vocal Désactivé",
    toggleSpeechOn: "Guidage Vocal Activé",
    highVisibility: "Mode Haute Visibilité",
    yourContext: "Votre contexte",
    whereNow: "Où êtes-vous maintenant ?",
    whereGo: "Où voulez-vous aller ?",
    accessNeeds: "Besoins d'accessibilité",
    needWheelchair: "Fauteuil roulant / accès sans marche",
    needVisual: "Basse vision / guidage vocal",
    needHearing: "Sourd / malentendant",
    ticketSection: "Section (optionnel)",
    minutesToKickoff: "Minutes avant le coup d'envoi",
    question: "Poser une question (optionnel)",
    questionHint: "Le texte libre est traité strictement comme des données, pas des commandes.",
    getHelp: "Obtenir de l'aide",
    assistance: "Assistance",
    placeholder: "Remplissez votre contexte et sélectionnez \"Obtenir de l'aide\". La réponse de l'assistant IA s'affichera ici en temps réel.",
    stadiumMap: "Carte Interactive du Stade",
    staffOperations: "Panneau des Opérations du Personnel",
    incidentLocation: "Zone de l'Incident",
    incidentType: "Type de Problème",
    incidentDesc: "Détails / Action requise",
    reportIncident: "Signaler & Contourner l'Incident",
    activeIncidents: "Incidents Actifs",
    noIncidents: "Aucun incident actif signalé.",
    spill: "Déversement (Bloquer Zone)",
    congestion: "Congestion (Retard Élevé)",
    maintenance: "Maintenance (Bloquer Zone)",
    medical: "Urgence médicale (Bloquer Zone)",
    meansWalk: "Marcher",
    meansRamp: "Rampe",
    meansElevator: "Ascenseur",
    meansStairs: "Escaliers",
    crowdLabel: "Affluence : ",
    modeLabel: "Accessibilité : ",
    routeHeading: "Directions de l'itinéraire :",
    metlifeFifaName: "Stade de New York New Jersey",
    grounding: "Les réponses reposent sur des plans de stade vérifiés. L'IA ne peut pas inventer d'itinéraires."
  }
};

// SVG coordinates for MetLife Stadium zones to draw edge lines
const ZONE_COORDS = {
  "gate_a": { x: 70, y: 330 },
  "gate_b": { x: 330, y: 330 },
  "gate_c": { x: 330, y: 70 },
  "gate_d": { x: 70, y: 70 },
  "concourse_lower_sw": { x: 145, y: 255 },
  "concourse_lower_se": { x: 255, y: 255 },
  "concourse_lower_ne": { x: 255, y: 145 },
  "concourse_lower_nw": { x: 145, y: 145 },
  "concourse_upper_w": { x: 120, y: 200 },
  "concourse_upper_e": { x: 280, y: 200 },
  "seating_lower": { x: 200, y: 200 },
  "seating_upper": { x: 200, y: 100 }
};

// State Variables
let currentLanguage = "en";
let currentPersona = "fan";
let ttsEnabled = false;
let currentMetadata = null;
let activeIncidents = [];
let speechUtterance = null;

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
const placeholderText = document.getElementById("placeholder");
const stadiumMetaP = document.getElementById("stadium-meta");

const staffCard = document.getElementById("staff-card");
const fanCard = document.getElementById("fan-card");
const incidentForm = document.getElementById("incident-form");
const incidentsListDiv = document.getElementById("incidents-list");

// Init App
document.addEventListener("DOMContentLoaded", async () => {
  setupLanguageListener();
  setupSettingsListeners();
  setupFormListeners();
  setupMapInteraction();
  
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
      // Re-trigger generation to refresh translations on result cards
      submitAssistForm();
    }
  });
}

function localizeUI(lang) {
  const dict = I18N[lang];
  // Localize standard text elements
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

  // Localize dynamic buttons
  personaToggle.textContent = currentPersona === "fan" ? dict.toggleStaff : dict.toggleFan;
  ttsToggle.textContent = ttsEnabled ? dict.toggleSpeechOn : dict.toggleSpeech;

  // Localize dropdown intents/needs if populated
  updateDropdownsLanguage(lang);
  renderIncidentsList();
}

function updateDropdownsLanguage(lang) {
  if (!currentMetadata) return;

  const dict = I18N[lang];
  
  // Save current selections
  const currentLocVal = currentLocationSelect.value;
  const currentDestVal = destinationIntentSelect.value;
  const currentIncVal = incidentLocationSelect.value;

  // Clear options
  currentLocationSelect.innerHTML = "";
  destinationIntentSelect.innerHTML = "";
  incidentLocationSelect.innerHTML = "";

  // Populate Location Dropdowns
  currentMetadata.zones.forEach((z) => {
    const locName = z.name[lang] || z.name.en || z.id;
    const opt1 = new Option(locName, z.id);
    const opt2 = new Option(locName, z.id);
    currentLocationSelect.add(opt1);
    incidentLocationSelect.add(opt2);
  });

  // Populate Intents
  currentMetadata.intents.forEach((intent) => {
    const labelKey = `intent_${intent}`;
    // If not direct i18n key exists, map to translation tables
    const label = dict[intent] || intent.replace("_", " ");
    destinationIntentSelect.add(new Option(label, intent));
  });

  // Restore values
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

    // Set FIFA name in footer
    stadiumMetaP.innerHTML = `<strong>${currentMetadata.stadium.name}</strong> (${I18N[currentLanguage].metlifeFifaName}) · Capacity: ${currentMetadata.stadium.capacity.toLocaleString()}`;
    
    // Initial dropdown setup
    updateDropdownsLanguage(currentLanguage);

    // Draw Map Edges
    const edgesGroup = document.getElementById("svg-edges");
    edgesGroup.innerHTML = "";
    
    // We map edges from static JSON mapping (deduplicating undirected paths)
    const drawnEdges = new Set();
    currentMetadata.zones.forEach(z => {
      // Find connections by checking edges array
      const matches = currentMetadata.facilities.filter(f => f.zone === z.id && f.type === "gate");
    });

    // Draw lines manually based on Dijkstra connections in JSON
    const edgesList = [
      ["gate_a", "concourse_lower_sw"],
      ["gate_b", "concourse_lower_se"],
      ["gate_c", "concourse_lower_ne"],
      ["gate_d", "concourse_lower_nw"],
      ["concourse_lower_sw", "concourse_lower_se"],
      ["concourse_lower_se", "concourse_lower_ne"],
      ["concourse_lower_ne", "concourse_lower_nw"],
      ["concourse_lower_nw", "concourse_lower_sw"],
      ["concourse_lower_sw", "seating_lower"],
      ["concourse_lower_sw", "concourse_upper_w"],
      ["concourse_lower_ne", "concourse_upper_e"],
      ["concourse_upper_w", "concourse_upper_e"],
      ["concourse_upper_w", "seating_upper"],
      ["concourse_upper_e", "seating_upper"]
    ];

    edgesList.forEach(([from, to]) => {
      const p1 = ZONE_COORDS[from];
      const p2 = ZONE_COORDS[to];
      if (p1 && p2) {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", p1.x);
        line.setAttribute("y1", p1.y);
        line.setAttribute("x2", p2.x);
        line.setAttribute("y2", p2.y);
        line.setAttribute("id", `edge-${from}-${to}`);
        edgesGroup.appendChild(line);
      }
    });

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
    ttsToggle.setAttribute("aria-pressed", ttsEnabled);
    if (!ttsEnabled && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    localizeUI(currentLanguage);
  });

  contrastToggle.addEventListener("click", () => {
    const isHiVis = document.body.classList.toggle("hi-vis");
    contrastToggle.setAttribute("aria-pressed", isHiVis);
  });

  speakBtn.addEventListener("click", () => {
    speakDirections();
  });
}

// Map interactions
function setupMapInteraction() {
  document.querySelectorAll(".zone").forEach((zoneEl) => {
    zoneEl.addEventListener("click", () => {
      const zoneId = zoneEl.id.replace("svg-zone-", "");
      if (currentPersona === "staff") {
        incidentLocationSelect.value = zoneId;
      } else {
        currentLocationSelect.value = zoneId;
      }
      
      // Visual feedback click
      document.querySelectorAll(".zone").forEach(el => el.classList.remove("active-start"));
      zoneEl.classList.add("active-start");
    });
  });
}

// Form Handlers & SSE streaming
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
  // Capture payload
  const checkedNeeds = Array.from(document.querySelectorAll('input[name="need"]:checked')).map(cb => cb.value);
  const payload = {
    persona: currentPersona,
    language: currentLanguage,
    current_location: currentLocationSelect.value,
    destination_intent: destinationIntentSelect.value,
    accessibility_needs: checkedNeeds,
    ticket_section: document.getElementById("ticket_section").value || null,
    minutes_to_kickoff: parseInt(document.getElementById("minutes_to_kickoff").value),
    question: document.getElementById("question").value || null
  };

  // Reset display
  resultDiv.setAttribute("aria-busy", "true");
  speakBtn.classList.add("hidden");
  if (window.speechSynthesis) window.speechSynthesis.cancel();

  resultDiv.innerHTML = `
    <div class="meta-badges">
      <span class="badge" data-i18n="loading">Computing Route...</span>
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
      showError(errData.detail || "Verification failed");
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let currentEvent = null;
    let textContainer = resultDiv.querySelector(".answer-text");
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n\n");

      for (let line of lines) {
        if (!line.trim()) continue;

        if (line.startsWith("event: ")) {
          currentEvent = line.replace("event: ", "").trim();
        } else if (line.startsWith("data: ")) {
          const dataStr = line.replace("data: ", "").trim();

          if (currentEvent === "metadata") {
            const metadata = JSON.parse(dataStr);
            renderRouteMetadata(metadata);
            textContainer = resultDiv.querySelector(".answer-text");
          } else if (currentEvent === "token") {
            const token = dataStr.replace(/\\n/g, "\n");
            fullText += token;
            textContainer.textContent = fullText;
          } else if (currentEvent === "result") {
            const finalResult = JSON.parse(dataStr);
            textContainer.textContent = finalResult.answer;
            textContainer.classList.add("done");
            resultDiv.setAttribute("aria-busy", "false");
            
            // Enable TTS Button
            speakBtn.classList.remove("hidden");

            if (ttsEnabled) {
              speakDirections();
            }
          }
        }
      }
    }

  } catch (err) {
    showError(err.message);
  }
}

function renderRouteMetadata(metadata) {
  const dict = I18N[currentLanguage];
  const crowdClass = `crowd-${metadata.crowd_level}`;
  const crowdLabel = dict[`crowd-${metadata.crowd_level}`] || metadata.crowd_level;
  
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
        ${metadata.route_steps.map(s => {
          const meansLabel = dict[`means${s.means.charAt(0).toUpperCase() + s.means.slice(1)}`] || s.means;
          return `<li>${s.instruction} <span class="step-means">${meansLabel}</span></li>`;
        }).join("")}
      </ol>
    `;
  }

  resultDiv.innerHTML = `
    <div class="meta-badges">
      <span class="badge ${crowdClass}">${dict.crowdLabel} ${crowdLabel}</span>
      <span class="badge">${dict.modeLabel} ${metadata.accessibility_mode}</span>
    </div>
    ${noticeHtml}
    <div class="answer-text"></div>
    ${stepsHtml}
  `;

  // Draw Path Highlights on SVG Map
  highlightMapPath(metadata.route_steps, metadata.facility);
}

function highlightMapPath(steps, targetFacility) {
  // Clear previous path highlights
  document.querySelectorAll(".zone").forEach((el) => {
    el.classList.remove("active-start", "active-end", "on-path");
  });
  document.querySelectorAll(".map-edges line").forEach((el) => {
    el.classList.remove("highlighted");
  });

  if (!steps || steps.length === 0) {
    // If already there, just highlight target
    const targetZoneEl = document.getElementById(`svg-zone-${targetFacility.zone}`);
    if (targetZoneEl) targetZoneEl.classList.add("active-end");
    return;
  }

  // Highlight Start & End Zones
  const startZone = steps[0].from_zone;
  const endZone = steps[steps.length - 1].to_zone;

  const startEl = document.getElementById(`svg-zone-${startZone}`);
  const endEl = document.getElementById(`svg-zone-${endZone}`);
  
  if (startEl) startEl.classList.add("active-start");
  if (endEl) endEl.classList.add("active-end");

  // Highlight Intermediate Nodes & Connections
  steps.forEach((step) => {
    // Node highlights
    if (step.to_zone !== endZone) {
      const midEl = document.getElementById(`svg-zone-${step.to_zone}`);
      if (midEl) midEl.classList.add("on-path");
    }

    // Edge highlights (try both directional names)
    const edgeId1 = `edge-${step.from_zone}-${step.to_zone}`;
    const edgeId2 = `edge-${step.to_zone}-${step.from_zone}`;
    const lineEl = document.getElementById(edgeId1) || document.getElementById(edgeId2);
    if (lineEl) {
      lineEl.classList.add("highlighted");
    }
  });
}

function showError(msg) {
  resultDiv.setAttribute("aria-busy", "false");
  resultDiv.innerHTML = `<p class="error">${msg}</p>`;
}

// Text to Speech
function speakDirections() {
  if (!window.speechSynthesis) return;

  window.speechSynthesis.cancel(); // stop previous speak

  const textToRead = resultDiv.innerText;
  speechUtterance = new SpeechSynthesisUtterance(textToRead);
  
  // Set language voice
  if (currentLanguage === "es") {
    speechUtterance.lang = "es-ES";
  } else if (currentLanguage === "fr") {
    speechUtterance.lang = "fr-FR";
  } else {
    speechUtterance.lang = "en-US";
  }

  window.speechSynthesis.speak(speechUtterance);
}

// Staff Incidents Operations
async function submitIncidentForm() {
  const payload = {
    persona: "staff",
    language: currentLanguage,
    current_location: incidentLocationSelect.value,
    destination_intent: "first_aid", // Dummy intent required by schemas
    ticket_section: null,
    minutes_to_kickoff: parseInt(document.getElementById("minutes_to_kickoff").value),
    question: null,
    incident_report: document.getElementById("incident_description").value,
    reported_issue_type: document.getElementById("incident_type").value
  };

  resultDiv.setAttribute("aria-busy", "true");
  
  try {
    const res = await fetch("/api/assist/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      showError(err.detail || "Logging failed");
      return;
    }

    // Read stream to get logged incident ID
    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let currentEvent = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n\n");
      for (let line of lines) {
        if (line.startsWith("event: ")) {
          currentEvent = line.replace("event: ", "").trim();
        } else if (line.startsWith("data: ") && currentEvent === "result") {
          const finalResult = JSON.parse(line.replace("data: ", ""));
          
          resultDiv.innerHTML = `
            <div class="meta-badges">
              <span class="badge crowd-high">INCIDENT LOGGED</span>
            </div>
            <div class="answer-text done">${finalResult.answer}</div>
          `;
          resultDiv.setAttribute("aria-busy", "false");
          
          // Clear text description form
          document.getElementById("incident_description").value = "";

          // Reload incident lists
          await fetchIncidents();
        }
      }
    }

  } catch (err) {
    showError(err.message);
  }
}

async function fetchIncidents() {
  try {
    const res = await fetch("/api/incidents");
    if (!res.ok) throw new Error("Failed to load incidents");
    activeIncidents = await res.json();
    renderIncidentsList();
    highlightIncidentZones();
  } catch (err) {
    console.error(err);
  }
}

function renderIncidentsList() {
  const dict = I18N[currentLanguage];
  incidentsListDiv.innerHTML = "";

  const active = activeIncidents.filter(inc => !inc.resolved);

  if (active.length === 0) {
    incidentsListDiv.innerHTML = `<p class="muted">${dict.noIncidents}</p>`;
    return;
  }

  active.forEach((inc) => {
    const typeLabel = dict[inc.issue_type] || inc.issue_type;
    const item = document.createElement("div");
    item.className = "incident-item";
    item.innerHTML = `
      <div class="incident-details">
        <span class="meta-tag spill">${typeLabel}</span>
        <strong>Zone: ${inc.zone_id.replace("_", " ").toUpperCase()}</strong>
        <span>${inc.description}</span>
      </div>
      <button class="resolve-btn" data-id="${inc.id}">Resolve</button>
    `;

    // Hook Resolve listener
    item.querySelector(".resolve-btn").addEventListener("click", async () => {
      await resolveIncident(inc.id);
    });

    incidentsListDiv.appendChild(item);
  });
}

async function resolveIncident(id) {
  try {
    const res = await fetch(`/api/incidents/${id}/resolve`, { method: "POST" });
    if (!res.ok) throw new Error("Failed to resolve incident");
    await fetchIncidents();
    // Re-verify assistant routing if any form is submitted
  } catch (err) {
    console.error(err);
  }
}

function highlightIncidentZones() {
  // Clear previous blocked styles
  document.querySelectorAll(".zone").forEach(el => el.classList.remove("blocked"));

  // Apply blocked class to active incident zones
  activeIncidents.forEach((inc) => {
    if (!inc.resolved && (inc.issue_type === "spill" || inc.issue_type === "maintenance" || inc.issue_type === "medical")) {
      const zoneEl = document.getElementById(`svg-zone-${inc.zone_id}`);
      if (zoneEl) {
        zoneEl.classList.add("blocked");
      }
    }
  });
}
