---
title: "Cluster Telemetry"
summary: "Real-time workstation cluster and storage resource monitoring"
date: 2026-09-27
type: page
---

<style>
  /* HEADER BAR & ADVANCED VIEW BUTTON */
  .telemetry-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0 16px 0;
    gap: 12px;
    flex-wrap: wrap;
  }
  .telemetry-header-info {
    font-size: 0.88rem;
    color: #4b5563;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  .btn-advanced-view {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0f172a;
    color: #f8fafc !important;
    text-decoration: none !important;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.80rem;
    font-weight: 600;
    padding: 7px 14px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
    border: 1px solid #1e293b;
  }
  .btn-advanced-view:hover {
    background: #1e293b;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    color: #38bdf8 !important;
    border-color: #38bdf8;
  }
  .pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ec4899;
    box-shadow: 0 0 6px #ec4899;
    display: inline-block;
  }

  .telemetry-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1f2937;
    margin: 10px 0 20px 0;
    position: relative;
    z-index: 10;
  }
  .node-card {
    background: #f3f6f9;
    border: 1px solid #d1d9e0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    cursor: pointer !important;
    position: relative;
    user-select: none;
    pointer-events: auto !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  }
  .node-card * {
    pointer-events: none;
  }
  .node-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.12);
    border-color: #3b82f6;
  }
  .card-hint {
    position: absolute;
    top: 16px;
    right: 16px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #2563eb;
    background: #dbeafe;
    padding: 3px 8px;
    border-radius: 6px;
  }
  .node-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 10px 0;
    color: #111827;
    padding-right: 70px;
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

  #clusterModalOverlay {
    display: none;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(4px);
    z-index: 2147483647 !important;
    align-items: center;
    justify-content: center;
    padding: 16px;
    box-sizing: border-box;
  }
  .modal-window {
    background: #ffffff;
    border-radius: 16px;
    max-width: 740px;
    width: 100%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
    overflow: hidden;
    pointer-events: auto;
  }
  .modal-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f8fafc;
  }
  .modal-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
  }
  .modal-close-btn {
    background: #e2e8f0;
    border: none;
    font-size: 1.4rem;
    line-height: 1;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    color: #334155;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .modal-close-btn:hover {
    background: #cbd5e1;
    color: #000;
  }
  .modal-body {
    padding: 20px;
    overflow-y: auto;
  }
  .chart-box {
    margin-bottom: 20px;
  }
  .chart-heading {
    font-size: 0.88rem;
    font-weight: 700;
    color: #334155;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
  }
  .sparkline-svg {
    width: 100%;
    height: 90px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
  }
  .task-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }
  .task-table th {
    text-align: left;
    padding: 8px 12px;
    background: #f1f5f9;
    color: #475569;
    font-weight: 600;
    border-bottom: 1px solid #cbd5e1;
  }
  .task-table td {
    padding: 7px 12px;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }
  .task-table tr:hover td {
    background: #f8fafc;
  }
</style>

<div class="telemetry-header-bar">
  <div class="telemetry-header-info">
    Live cluster compute and storage nodes
  </div>
  <a href="/status/kiosk/" class="btn-advanced-view">
    <span class="pulse-dot"></span> Advanced View ↗
  </a>
</div>

<div class="telemetry-container" id="telemetryGrid"></div>

<div id="clusterModalOverlay">
  <div class="modal-window" id="modalWindow">
    <div class="modal-header">
      <h3 class="modal-title" id="modalNodeName">Workstation Details</h3>
      <button class="modal-close-btn" id="modalCloseBtn">&times;</button>
    </div>
    <div class="modal-body">
      <div class="chart-box">
        <div class="chart-heading">
          <span>Recent CPU Load Trend</span>
          <span id="chartLatestVal" style="color: #f59e0b;">--</span>
        </div>
        <svg class="sparkline-svg" viewBox="0 0 500 100" preserveAspectRatio="none">
          <polyline id="sparklinePoly" fill="rgba(245, 158, 11, 0.15)" stroke="#f59e0b" stroke-width="2" points="" />
        </svg>
      </div>
      <div id="taskTableWrapper"></div>
    </div>
  </div>
</div>

<script>
(function() {
  const GIST_RAW_URL = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw/endpoints.json";
  const GIST_BASE = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw";

  function renderCloudSyncBadge(sync) {
    const statusEl = document.getElementById("nas-sync-status");
    const pillEl = document.getElementById("nas-sync-pill");
    const timeEl = document.getElementById("nas-sync-time");
    const fileEl = document.getElementById("nas-sync-file");

    if (!statusEl || !pillEl || !timeEl || !sync) return;

    if (sync.state === "success") {
      statusEl.innerText = "Synced";
      statusEl.style.color = "#16a34a";
      pillEl.style.background = "#10b981";
      pillEl.style.boxShadow = "0 0 6px rgba(16, 185, 129, 0.4)";
      timeEl.innerText = `Last synced: ${sync.last_synced}`;
      if (fileEl && sync.last_file) {
        fileEl.innerText = sync.last_file;
        fileEl.title = `Last synced file: ${sync.last_file}`;
      }
    } else {
      statusEl.innerText = sync.status || "Failed";
      statusEl.style.color = "#dc2626";
      pillEl.style.background = "#ef4444";
      pillEl.style.boxShadow = "0 0 6px rgba(239, 68, 68, 0.4)";
      timeEl.innerText = `Alert: ${sync.recent_errors || 1} error(s)`;
      if (fileEl && sync.last_file) {
        fileEl.innerText = sync.last_file;
        fileEl.title = `File error: ${sync.last_file}`;
      }
    }
  }

  async function updateCloudSync() {
    try {
      const res = await fetch(`${GIST_BASE}/cloudsync.json?t=${Date.now()}`);
      if (res.ok) {
        const sync = await res.json();
        renderCloudSyncBadge(sync);
      }
    } catch (err) {
      console.warn("Could not fetch cloudsync status", err);
    }
  }

  const NODES = [
    {
      id: "simon",
      name: "simon-HP-Z6-G4-Workstation",
      specs: "72 Cores @ 2.3 GHz",
      columns: 12,
      url: "",
      history: []
    },
    {
      id: "jlp",
      name: "Jean Luc Packard Bell (JLP)",
      specs: "104 Cores @ 2.1 GHz",
      columns: 13,
      url: "",
      history: []
    },
    {
      id: "priti",
      name: "Priti TheDell",
      specs: "12 Cores @ 4.0 GHz",
      columns: 6,
      url: "",
      history: []
    },
    {
      id: "nas",
      name: "Synology DiskStation",
      specs: "4 Cores • 23 TB Btrfs RAID Pool",
      columns: 4,
      url: "",
      history: []
    }
  ];

  let activeModalNode = null;

  function moveModalToBody() {
    const modal = document.getElementById("clusterModalOverlay");
    if (modal && modal.parentElement !== document.body) {
      document.body.appendChild(modal);
    }
  }

  function formatBytes(bytes) {
    if (!bytes || isNaN(bytes)) return "--";
    const gb = bytes / (1024 ** 3);
    if (gb >= 1000) {
      return (bytes / (1024 ** 4)).toFixed(1) + " TB";
    }
    return gb.toFixed(0) + " GB";
  }

  function formatUptime(uptimeData) {
    if (!uptimeData) return "--";
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

  function openNodeModal(node) {
    activeModalNode = node;
    const modal = document.getElementById("clusterModalOverlay");
    const nameEl = document.getElementById("modalNodeName");
    if (nameEl) nameEl.innerText = node.name;
    if (modal) modal.style.display = "flex";
    renderModalGraph(node);
    fetchModalTasks(node);
  }

  function closeNodeModal() {
    activeModalNode = null;
    const modal = document.getElementById("clusterModalOverlay");
    if (modal) modal.style.display = "none";
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
    const wrapper = document.getElementById("taskTableWrapper");

    if (!wrapper || !node.url) return;

    try {
      const cleanUrl = node.url.replace(/\/+$/, "");
      const apiVer = node.id === "nas" ? "4" : "3";
      const res = await fetch(`${cleanUrl}/api/${apiVer}/processlist`);
      if (!res.ok) throw new Error("Status " + res.status);
      const procList = await res.json();
      procList.sort((a, b) => (b.cpu_percent || 0) - (a.cpu_percent || 0));
      const top10 = procList.slice(0, 10);

      let rowsHtml = "";
      top10.forEach(p => {
        const cpu = (p.cpu_percent || 0).toFixed(1);
        const mem = (p.memory_percent || 0).toFixed(1);
        rowsHtml += `
          <tr>
            <td style="color:#64748b;">${p.pid}</td>
            <td style="font-weight:600;">${p.name}</td>
            <td style="color:#475569;">${p.username || "root"}</td>
            <td style="color: ${cpu > 50 ? '#dc2626' : '#1e293b'}; font-weight: 600;">${cpu}%</td>
            <td>${mem}%</td>
          </tr>
        `;
      });

      wrapper.innerHTML = `
        <div class="chart-heading">Top Active Processes (by CPU / RAM)</div>
        <table class="task-table">
          <thead>
            <tr>
              <th>PID</th>
              <th>Process</th>
              <th>User</th>
              <th>CPU %</th>
              <th>MEM %</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      `;
    } catch (e) {
      wrapper.innerHTML = `
        <div class="chart-heading">Top Active Processes (by CPU / RAM)</div>
        <div style="text-align: center; color: #ef4444; padding: 12px; font-size: 0.85rem;">
          Unable to fetch active processes.
        </div>
      `;
    }
  }

  function initDashboard() {
    moveModalToBody();

    const container = document.getElementById("telemetryGrid");
    if (!container) return;
    container.innerHTML = "";

    NODES.forEach(node => {
      const card = document.createElement("div");
      card.className = "node-card";
      card.id = `card-${node.id}`;

      const isNas = node.id === "nas";
      const syncSectionHtml = isNas ? `
        <div style="margin-top: 14px; border-top: 1px solid rgba(229, 231, 235, 0.6); padding-top: 10px;">
          <div class="metric-label" style="margin-bottom: 4px;">
            <span>Cloud Sync:</span>
            <span id="nas-sync-status" style="font-weight: 700; color: #64748b;">Checking...</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.78rem; color: #475569;">
            <div style="display: flex; align-items: center; gap: 6px;">
              <span id="nas-sync-pill" style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #9ca3af; transition: background 0.3s ease;"></span>
              <span id="nas-sync-time">Last synced: --</span>
            </div>
            <span id="nas-sync-file" style="color: #6b7280; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.72rem; overflow: hidden; text-overflow: ellipsis; max-width: 140px; white-space: nowrap;"></span>
          </div>
        </div>
      ` : "";

      card.innerHTML = `
        <span class="card-hint">Inspect ↗</span>
        <div class="node-title">
          <span class="status-badge" id="badge-${node.id}"></span>${node.name}
        </div>
        <div class="node-meta">
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
          <span>Storage: <span id="disk-val-${node.id}">-- / --</span></span>
        </div>
        <div class="progress-bg">
          <div class="progress-fill fill-storage" id="disk-bar-${node.id}" style="width: 0%;"></div>
        </div>

        ${syncSectionHtml}

        <div class="heatmap-section-title">Core Heatmap:</div>
        <div class="heatmap-grid" id="grid-${node.id}" style="grid-template-columns: repeat(${node.columns}, 1fr);">
          <div style="font-size:0.75rem; color:#9ca3af; grid-column: 1/-1;">Connecting telemetry...</div>
        </div>
      `;

      card.addEventListener("click", () => {
        openNodeModal(node);
      });

      container.appendChild(card);
    });

    const modal = document.getElementById("clusterModalOverlay");
    const closeBtn = document.getElementById("modalCloseBtn");
    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) closeNodeModal();
      });
    }
    if (closeBtn) {
      closeBtn.addEventListener("click", closeNodeModal);
    }
  }

  async function fetchNodeTelemetry(node) {
    if (!node.url || !node.url.startsWith("http")) {
      const badge = document.getElementById(`badge-${node.id}`);
      if (badge) badge.className = "status-badge status-offline";
      return;
    }

    const cleanUrl = node.url.replace(/\/+$/, "");
    const apiVer = node.id === "nas" ? "4" : "3";

    try {
      const [cpuRes, memRes] = await Promise.all([
        fetch(`${cleanUrl}/api/${apiVer}/cpu`).then(r => {
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          return r.json();
        }),
        fetch(`${cleanUrl}/api/${apiVer}/mem`).then(r => {
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          return r.json();
        })
      ]);

      const badge = document.getElementById(`badge-${node.id}`);
      if (badge) badge.className = "status-badge status-online";

      const cpuTotal = cpuRes && cpuRes.total !== undefined ? Number(cpuRes.total.toFixed(1)) : 0;
      node.history.push(cpuTotal);
      if (node.history.length > 40) node.history.shift();

      const cpuVal = document.getElementById(`cpu-val-${node.id}`);
      const cpuBar = document.getElementById(`cpu-bar-${node.id}`);
      if (cpuVal) cpuVal.innerText = `${cpuTotal}%`;
      if (cpuBar) cpuBar.style.width = `${Math.min(cpuTotal, 100)}%`;

      if (memRes && memRes.total) {
        const ramUsedGB = (memRes.used / (1024 ** 3)).toFixed(1);
        const ramTotalGB = (memRes.total / (1024 ** 3)).toFixed(0);
        const ramPct = memRes.percent !== undefined ? memRes.percent : ((memRes.used / memRes.total) * 100);
        const ramVal = document.getElementById(`ram-val-${node.id}`);
        const ramBar = document.getElementById(`ram-bar-${node.id}`);
        if (ramVal) ramVal.innerText = `${ramUsedGB} / ${ramTotalGB} GB`;
        if (ramBar) ramBar.style.width = `${Math.min(ramPct, 100)}%`;
      }

      fetch(`${cleanUrl}/api/${apiVer}/fs`)
        .then(r => r.ok ? r.json() : null)
        .then(fsRes => {
          if (Array.isArray(fsRes) && fsRes.length > 0) {
            const targetFs = fsRes.find(d => d.mnt_point === "/volume1") ||
                             fsRes.find(d => d.mnt_point === "/") ||
                             fsRes[0];

            const diskUsedStr = formatBytes(targetFs.used);
            const diskTotalStr = formatBytes(targetFs.size);
            const diskPct = targetFs.percent !== undefined 
              ? Number(targetFs.percent).toFixed(0) 
              : ((targetFs.used / targetFs.size) * 100).toFixed(0);

            const diskVal = document.getElementById(`disk-val-${node.id}`);
            const diskBar = document.getElementById(`disk-bar-${node.id}`);
            if (diskVal) diskVal.innerText = `${diskUsedStr} / ${diskTotalStr} (${diskPct}%)`;
            if (diskBar) diskBar.style.width = `${Math.min(diskPct, 100)}%`;
          }
        })
        .catch(() => {});

      fetch(`${cleanUrl}/api/${apiVer}/percpu`)
        .then(r => r.ok ? r.json() : null)
        .then(perCpuRes => {
          const grid = document.getElementById(`grid-${node.id}`);
          if (grid && Array.isArray(perCpuRes)) {
            grid.innerHTML = "";
            perCpuRes.forEach((core, idx) => {
              const box = document.createElement("div");
              box.className = "core-box";
              const usage = core.total !== undefined ? core.total : (core.percent || 0);
              box.style.backgroundColor = getCoreColor(usage);
              box.title = `Core ${idx}: ${Number(usage).toFixed(1)}%`;
              grid.appendChild(box);
            });
          }
        })
        .catch(() => {});

      fetch(`${cleanUrl}/api/${apiVer}/uptime`)
        .then(r => r.ok ? r.json() : null)
        .then(uptimeRes => {
          const uptimeEl = document.getElementById(`uptime-${node.id}`);
          if (uptimeEl) uptimeEl.innerText = formatUptime(uptimeRes);
        })
        .catch(() => {});

      if (activeModalNode && activeModalNode.id === node.id) {
        renderModalGraph(node);
      }

    } catch (err) {
      const badge = document.getElementById(`badge-${node.id}`);
      if (badge) badge.className = "status-badge status-offline";
    }
  }

  function updateAll() {
    NODES.forEach(fetchNodeTelemetry);
  }

  async function startClusterMonitoring() {
    try {
      const res = await fetch(`${GIST_BASE}/endpoints.json?t=${Date.now()}`);
      if (res.ok) {
        const endpoints = await res.json();
        NODES.forEach(n => {
          const targetUrl = endpoints[n.id] || (n.id === "nas" ? endpoints["nas"] : null);
          if (targetUrl && typeof targetUrl === "string" && targetUrl.startsWith("http")) {
            n.url = targetUrl.replace(/\/+$/, "");
          }
        });
      }
    } catch (err) {
      console.warn("Could not load dynamic endpoints", err);
    }

    initDashboard();
    updateCloudSync();
    updateAll();

    setInterval(updateAll, 3000);
    setInterval(updateCloudSync, 30000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startClusterMonitoring);
  } else {
    startClusterMonitoring();
  }
})();
</script>
