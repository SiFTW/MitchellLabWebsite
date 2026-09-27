---
title: "Lab Compute Cluster"
summary: "Live monitoring of lab compute workstations."
date: 2026-09-27
type: page
share: false
commentable: false
editable: false
show_breadcrumb: true
---

<div style="display: flex; gap: 8px; margin-bottom: 1rem;">
  <button onclick="setServer('simon')" class="btn btn-primary" id="btn-simon">Simon (72 cores)</button>
  <button onclick="setServer('jlp')" class="btn btn-outline-primary" id="btn-jlp">JLP (104 cores)</button>
  <button onclick="setServer('priti')" class="btn btn-outline-primary" id="btn-priti">Priti (12 cores)</button>
</div>

<iframe id="cluster-frame" src="https://counting-dryer-depot-payments.trycloudflare.com/" style="width: 100%; height: 85vh; border: 1px solid #444; border-radius: 8px;"></iframe>

<script>
const urls = {
  simon: "https://counting-dryer-depot-payments.trycloudflare.com/",
  jlp: "https://jlp-tunnel-url.trycloudflare.com/",
  priti: "https://priti-tunnel-url.trycloudflare.com/"
};

function setServer(name) {
  document.getElementById('cluster-frame').src = urls[name];
  ['simon', 'jlp', 'priti'].forEach(k => {
    const el = document.getElementById('btn-' + k);
    if (k === name) {
      el.className = 'btn btn-primary';
    } else {
      el.className = 'btn btn-outline-primary';
    }
  });
}
</script>
