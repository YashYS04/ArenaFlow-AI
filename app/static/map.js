// ArenaFlow Stadium Vector Map Module
/* global ZONE_COORDS, drawStadiumEdges, clearRouteHighlights, highlightRouteSteps, setupMapInteraction */

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

function drawStadiumEdges() {
  const edgesGroup = document.getElementById("svg-edges");
  if (!edgesGroup) return;
  edgesGroup.innerHTML = "";

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
}

function clearRouteHighlights() {
  document.querySelectorAll(".zone").forEach((el) => {
    el.classList.remove("active-start", "active-end", "active-path");
  });
  document.querySelectorAll("#svg-edges line").forEach((line) => {
    line.classList.remove("active-edge");
  });
}

function highlightRouteSteps(routeSteps, targetZone) {
  clearRouteHighlights();
  if (!routeSteps || routeSteps.length === 0) return;

  const startZone = routeSteps[0].from_zone;
  const startEl = document.getElementById(`svg-zone-${startZone}`);
  if (startEl) startEl.classList.add("active-start");

  const endEl = document.getElementById(`svg-zone-${targetZone}`);
  if (endEl) endEl.classList.add("active-end");

  routeSteps.forEach((step) => {
    const fromEl = document.getElementById(`svg-zone-${step.from_zone}`);
    if (fromEl && step.from_zone !== startZone && step.from_zone !== targetZone) {
      fromEl.classList.add("active-path");
    }

    const toEl = document.getElementById(`svg-zone-${step.to_zone}`);
    if (toEl && step.to_zone !== startZone && step.to_zone !== targetZone) {
      toEl.classList.add("active-path");
    }

    const edgeId1 = `edge-${step.from_zone}-${step.to_zone}`;
    const edgeId2 = `edge-${step.to_zone}-${step.from_zone}`;
    const edgeEl = document.getElementById(edgeId1) || document.getElementById(edgeId2);
    if (edgeEl) edgeEl.classList.add("active-edge");
  });
}

function setupMapInteraction(onZoneSelected) {
  document.querySelectorAll(".zone").forEach((zoneEl) => {
    zoneEl.addEventListener("click", () => {
      const zoneId = zoneEl.id.replace("svg-zone-", "");
      if (typeof onZoneSelected === "function") {
        onZoneSelected(zoneId, zoneEl);
      }
    });
  });
}
