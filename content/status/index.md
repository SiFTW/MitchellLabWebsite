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
  .modal-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  z-index: 999999;
  align-items: center;
  justify-content: center;
  padding: 16px;
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
(function() {
  const NODES = [
    {
      id: "simon",
      name: "simon-HP-Z6-G4-Workstation",
      ip: "139.184.170.218",
      specs: "72 Cores @ 2.3 GHz",
      columns: 12,
      url: "https://counting-dryer-depot-payments.trycloudflare.com",
      history: []
    },
    {
      id: "jlp",
      name: "Jean Luc Packard Bell (JLP)",
      ip: "139.184.169.98",
      specs: "104 Cores @ 2.1 GHz",
      columns: 13,
      url: "https://thereby-william-search-reader.trycloudflare.com",
      history: []
    },
    {
      id: "priti",
      name: "Priti TheDell",
      ip: "139.184.171.6",
      specs: "12 Cores @ 4.0 GHz",
      columns: 6,
      url: "https://info-critics-explanation-ski.trycloudflare.com",
      history: []
    }
  ];

  let activeModalNode = null;

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
    return `${d}d ${h}m`;
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
      card.setAttribute("data-node-id", node.id);
      card.innerHTML = `
        <span class="card-hint">Inspect ↗</span>
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

    // Delegated click listener on the entire container
    container.addEventListener("click", function(e) {
      const targetCard = e.target.closest(".node-card");
      if (!targetCard) return;
      const nodeId = targetCard.getAttribute("data-node-id");
      const matchedNode = NODES.find(n => n.id === nodeId);
      if (matchedNode) {
        openModal(matchedNode);
      }
    });
  }

  function openModal(node) {
    activeModalNode = node;
    const modal = document.getElementById("nodeModal");
    const nameEl = document.getElementById("modalNodeName");
    if (nameEl) nameEl.innerText = node.name;
    if (modal) modal.style.display = "flex";
    renderModalGraph(node);
    fetchModalTasks(node);
  }

  function closeModal() {
    activeModalNode = null;
    const modal = document.getElementById("nodeModal");
    if (modal) modal.style.display = "none";
  }

  // Bind close buttons safely
  const modalOverlay = document.getElementById("nodeModal");
  if (modalOverlay) {
    modalOverlay.addEventListener("click", function(e) {
      if (e.target === modalOverlay) closeModal();
    });
  }

  const closeBtn = document.querySelector(".modal-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }

  function renderModalGraph(node) {
    const history = node.history && node.history.length > 0 ? node.history : [0];
    const latest = history[history.length - 1];
    const latestValEl = document.getElementById("chartLatestVal");
    if (latestValEl) latestValEl.innerText = `${latest}% Current`;

    const width = 500;
    const height = 100;
    const step = width / (Math.max(history.length - 1, 1));

    let points = history.map((val, i) => {
      const x = i * step;
      const y = height - (val / 100) * (height - 10) - 5;
      return `${x},${y}`;
    });

    const polyPoints = `0,${height} ` + points.join(" ") + ` ${width},${height}`;
    const sparkline = document.getElementById("sparklinePoly");
    if (sparkline) sparkline.setAttribute("points", polyPoints);
  }

  async function fetchModalTasks(node) {
    const tbody = document.getElementById("taskTableBody");
    if (!tbody) return;
    try {
      const procList = await fetch(`${node.url}/api/3/processlist`).then(r => r.json());
      procList.sort((a, b) => (b.cpu_percent || 0) - (a.cpu_percent || 0));
      const top10 = procList.slice(0, 10);

      tbody.innerHTML = "";
      top10.forEach(p => {
        const row = document.createElement("tr");
        const cpu = (p.cpu_percent || 0).toFixed(1);
        const mem = (p.memory_percent || 0).toFixed(1);
        row.innerHTML = `
          <td style="color:#64748b;">${p.pid}</td>
          <td style="font-weight:600;">${p.name}</td>
          <td style="color:#475569;">${p.username || "root"}</td>
          <td style="color: ${cpu > 50 ? '#dc2626' : '#1e293b'}; font-weight: 600;">${cpu}%</td>
          <td>${mem}%</td>
        `;
        tbody.appendChild(row);
      });
    } catch (e) {
      tbody.innerHTML = `
        <tr><td colspan="5" style="text-align: center; color: #ef4444;">Unable to fetch active processes.</td></tr>
      `;
    }
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

      const cpuTotal = cpuRes.total ? Number(cpuRes.total.toFixed(1)) : 0;
      node.history.push(cpuTotal);
      if (node.history.length > 40) node.history.shift();

      const cpuVal = document.getElementById(`cpu-val-${node.id}`);
      const cpuBar = document.getElementById(`cpu-bar-${node.id}`);
      if (cpuVal) cpuVal.innerText = `${cpuTotal}%`;
      if (cpuBar) cpuBar.style.width = `${Math.min(cpuTotal, 100)}%`;

      const ramUsedGB = (memRes.used / (1024 ** 3)).toFixed(1);
      const ramTotalGB = (memRes.total / (1024 ** 3)).toFixed(0);
      const ramPct = ((memRes.used / memRes.total) * 100).toFixed(1);
      const ramVal = document.getElementById(`ram-val-${node.id}`);
      const ramBar = document.getElementById(`ram-bar-${node.id}`);
      if (ramVal) ramVal.innerText = `${ramUsedGB} / ${ramTotalGB} GB`;
      if (ramBar) ramBar.style.width = `${Math.min(ramPct, 100)}%`;

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

      if (activeModalNode && activeModalNode.id === node.id) {
        renderModalGraph(node);
        fetchModalTasks(node);
      }

    } catch (err) {
      const badge = document.getElementById(`badge-${node.id}`);
      if (badge) badge.className = "status-badge status-offline";
    }
  }

  function updateTelemetry() {
    NODES.forEach(fetchNodeTelemetry);
  }

  // Initialize immediately and on DOM load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      initCards();
      updateTelemetry();
      setInterval(updateTelemetry, 3000);
    });
  } else {
    initCards();
    updateTelemetry();
    setInterval(updateTelemetry, 3000);
  }
})();
</script>
