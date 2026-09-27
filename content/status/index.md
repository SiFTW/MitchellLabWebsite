---
title: "Cluster Telemetry"
summary: "Real-time workstation cluster resource monitoring"
date: 2026-09-27
type: page
---

<style>
  .telemetry-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1f2937;
    margin: 20px 0;
  }
  .node-card {
    background: #f3f6f9;
    border: 1px solid #d1d9e0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  }
  .node-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 10px 0;
    color: #111827;
  }
  .node-meta {
    font-size: 0.85rem;
    line-height: 1.45;
    color: #4b5563;
    margin-bottom: 15px;
  }
  .metric-label {
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
  }
  .progress-bg {
    width: 100%;
    height: 9px;
    background: #e5e7eb;
    border-radius: 9999px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.4s ease;
  }
  .fill-load    { background: #f59e0b; }
  .fill-ram     { background: #16a34a; }
  .fill-storage { background: #3b82f6; }

  .heatmap-section-title {
    font-size: 0.85rem;
    font-weight: 600;
    margin: 16px 0 8px 0;
    color: #374151;
  }
  .heatmap-grid {
    display: grid;
    gap: 3px;
    background: #ffffff;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
  }
  .core-box {
    aspect-ratio: 1 / 1;
    border-radius: 2px;
    background: #e5e7eb;
    transition: background-color 0.3s ease;
  }
  .status-badge {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    background: #9ca3af;
  }
  .status-online { background: #10b981; }
  .status-offline { background: #ef4444; }
</style>

<div class="telemetry-container" id="telemetryGrid"></div>

<script>
const NODES = [
  {
    id: "simon",
    name: "simon-HP-Z6-G4-Workstation",
    ip: "139.184.170.218",
    specs: "72 Cores @ 2.3 GHz",
    columns: 12,
    url: "https://counting-dryer-depot-payments.trycloudflare.com"
  },
  {
    id: "jlp",
    name: "Jean Luc Packard Bell (JLP)",
    ip: "139.184.169.98",
    specs: "104 Cores @ 2.1 GHz",
    columns: 13,
    url: "https://thereby-william-search-reader.trycloudflare.com"
  },
  {
    id: "priti",
    name: "Priti TheDell",
    ip: "139.184.171.6",
    specs: "12 Cores @ 4.0 GHz",
    columns: 6,
    url: "https://info-critics-explanation-ski.trycloudflare.com"
  }
];

function formatUptime(uptimeData) {
  if (!uptimeData) return "Unknown";
  if (typeof uptimeData === "string") {
    return uptimeData.replace("days", "d").replace("day", "d").replace("hours", "h").replace("mins", "m");
  }
  const s = parseInt(uptimeData, 10);
  if (isNaN(s)) return String(uptimeData);
  const d = Math.floor(s / (3600 * 24));
  const h = Math.floor((s % (3600 * 24)) / 3600);
  const m = Math.floor((s % 3600) / 60);
  return `${d}d ${h}h ${m}m`;
}

function getCoreColor(usage) {
  if (usage < 15) return "#e5e7eb";
  if (usage < 40) return "#fcd34d";
  if (usage < 75) return "#f59e0b";
  return "#ef4444";
}

function initCards() {
  const container = document.getElementById("telemetryGrid");
  if (!container) return;
  container.innerHTML = "";

  NODES.forEach(node => {
    const card = document.createElement("div");
    card.className = "node-card";
    card.id = `card-${node.id}`;
    card.innerHTML = `
      <div class="node-title">
        <span class="status-badge" id="badge-${node.id}"></span>${node.name}
      </div>
      <div class="node-meta">
        IP: ${node.ip}<br>
        ${node.specs}<br>
        Uptime: <span id="uptime-${node.id}">--</span>
      </div>

      <div class="metric-label">
        <span>CPU Load: <span id="cpu-val-${node.id}">--%</span></span>
      </div>
      <div class="progress-bg">
        <div class="progress-fill fill-load" id="cpu-bar-${node.id}" style="width: 0%;"></div>
      </div>

      <div class="metric-label">
        <span>RAM: <span id="ram-val-${node.id}">-- / -- GB</span></span>
      </div>
      <div class="progress-bg">
        <div class="progress-fill fill-ram" id="ram-bar-${node.id}" style="width: 0%;"></div>
      </div>

      <div class="metric-label">
        <span>Storage: <span id="disk-val-${node.id}">-- / -- GB</span></span>
      </div>
      <div class="progress-bg">
        <div class="progress-fill fill-storage" id="disk-bar-${node.id}" style="width: 0%;"></div>
      </div>

      <div class="heatmap-section-title">Core Heatmap:</div>
      <div class="heatmap-grid" id="grid-${node.id}" style="grid-template-columns: repeat(${node.columns}, 1fr);">
        <div style="font-size:0.75rem; color:#9ca3af; grid-column: 1/-1;">Connecting telemetry...</div>
      </div>
    `;
    container.appendChild(card);
  });
}

async function fetchNodeTelemetry(node) {
  try {
    const [cpuRes, perCpuRes, memRes, fsRes, uptimeRes] = await Promise.all([
      fetch(`${node.url}/api/3/cpu`).then(r => r.json()),
      fetch(`${node.url}/api/3/percpu`).then(r => r.json()),
      fetch(`${node.url}/api/3/mem`).then(r => r.json()),
      fetch(`${node.url}/api/3/fs`).then(r => r.json()),
      fetch(`${node.url}/api/3/uptime`).then(r => r.json())
    ]);

    const badge = document.getElementById(`badge-${node.id}`);
    if (badge) badge.className = "status-badge status-online";

    const uptimeEl = document.getElementById(`uptime-${node.id}`);
    if (uptimeEl) uptimeEl.innerText = formatUptime(uptimeRes);

    // CPU Progress
    const cpuTotal = cpuRes.total ? cpuRes.total.toFixed(1) : 0;
    const cpuVal = document.getElementById(`cpu-val-${node.id}`);
    const cpuBar = document.getElementById(`cpu-bar-${node.id}`);
    if (cpuVal) cpuVal.innerText = `${cpuTotal}%`;
    if (cpuBar) cpuBar.style.width = `${Math.min(cpuTotal, 100)}%`;

    // RAM Progress
    const ramUsedGB = (memRes.used / (1024 ** 3)).toFixed(1);
    const ramTotalGB = (memRes.total / (1024 ** 3)).toFixed(0);
    const ramPct = ((memRes.used / memRes.total) * 100).toFixed(1);
    const ramVal = document.getElementById(`ram-val-${node.id}`);
    const ramBar = document.getElementById(`ram-bar-${node.id}`);
    if (ramVal) ramVal.innerText = `${ramUsedGB} / ${ramTotalGB} GB`;
    if (ramBar) ramBar.style.width = `${Math.min(ramPct, 100)}%`;

    // Storage Progress (Targets root mount '/')
    if (Array.isArray(fsRes) && fsRes.length > 0) {
      const rootFs = fsRes.find(d => d.mnt_point === "/") || fsRes[0];
      const diskUsedGB = (rootFs.used / (1024 ** 3)).toFixed(0);
      const diskTotalGB = (rootFs.size / (1024 ** 3)).toFixed(0);
      const diskPct = rootFs.percent !== undefined ? rootFs.percent.toFixed(0) : ((rootFs.used / rootFs.size) * 100).toFixed(0);

      const diskVal = document.getElementById(`disk-val-${node.id}`);
      const diskBar = document.getElementById(`disk-bar-${node.id}`);
      if (diskVal) diskVal.innerText = `${diskUsedGB} / ${diskTotalGB} GB (${diskPct}%)`;
      if (diskBar) diskBar.style.width = `${Math.min(diskPct, 100)}%`;
    }

    // Heatmap Grid
    const grid = document.getElementById(`grid-${node.id}`);
    if (grid) {
      grid.innerHTML = "";
      perCpuRes.forEach((core, idx) => {
        const box = document.createElement("div");
        box.className = "core-box";
        const usage = core.total || 0;
        box.style.backgroundColor = getCoreColor(usage);
        box.title = `Core ${idx}: ${usage.toFixed(1)}%`;
        grid.appendChild(box);
      });
    }
  } catch (err) {
    const badge = document.getElementById(`badge-${node.id}`);
    if (badge) badge.className = "status-badge status-offline";
  }
}

function updateTelemetry() {
  NODES.forEach(fetchNodeTelemetry);
}

document.addEventListener("DOMContentLoaded", () => {
  initCards();
  updateTelemetry();
  setInterval(updateTelemetry, 3000);
});
</script>
