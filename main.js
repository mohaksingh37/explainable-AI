/* ═══════════════════════════════════════════════════
   XAI Legal Predictor — main.js
   Handles: navigation, form, predictions, charts
   ═══════════════════════════════════════════════════ */

"use strict";

// ─── Chart registry ──────────────────────────────────
const charts = {};

function destroyChart(id) {
  if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

// ─── Navigation ──────────────────────────────────────
function showSection(id) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('section-' + id).classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const map = { home: 0, predictor: 1, about: 2 };
  document.querySelectorAll('.nav-btn')[map[id]]?.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Tab switching ────────────────────────────────────
function showTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

// ─── Range display ────────────────────────────────────
function updateRangeDisplay(key, val) {
  const el = document.getElementById('val-' + key);
  if (el) el.textContent = parseFloat(val).toFixed(
    FEATURE_DESCRIPTIONS[key]?.step < 1 ? 1 : 0
  );
}

function updateToggleDisplay(key) { /* handled by CSS */ }

// Initialize range displays
window.addEventListener('DOMContentLoaded', () => {
  for (const key in FEATURE_DESCRIPTIONS) {
    const fd = FEATURE_DESCRIPTIONS[key];
    if (fd.type === 'range') {
      const init = ((fd.min + fd.max) / 2).toFixed(fd.step < 1 ? 1 : 0);
      const el = document.getElementById('val-' + key);
      if (el) el.textContent = init;
    }
  }
});

// ─── Collect form values ──────────────────────────────
function collectFeatures() {
  const features = {};
  for (const key in FEATURE_DESCRIPTIONS) {
    const fd = FEATURE_DESCRIPTIONS[key];
    const el = document.getElementById('feat-' + key);
    if (!el) continue;

    if (fd.type === 'toggle') {
      features[key] = el.checked ? 1 : 0;
    } else {
      features[key] = parseFloat(el.value);
    }
  }
  return features;
}

// ─── Load sample case into form ───────────────────────
function loadCase(id) {
  const c = SAMPLE_CASES.find(x => x.id === id);
  if (!c) return;

  document.getElementById('case-name').value = c.title;

  for (const key in c.features) {
    const el = document.getElementById('feat-' + key);
    const fd = FEATURE_DESCRIPTIONS[key];
    if (!el || !fd) continue;

    if (fd.type === 'toggle') {
      el.checked = c.features[key] === 1;
    } else {
      el.value = c.features[key];
      const valEl = document.getElementById('val-' + key);
      if (valEl) valEl.textContent = parseFloat(c.features[key]).toFixed(fd.step < 1 ? 1 : 0);
    }
  }

  showSection('predictor');
  setTimeout(predict, 300); // auto-predict
}

// ─── Reset form ───────────────────────────────────────
function resetForm() {
  document.getElementById('case-name').value = 'Custom Case';
  for (const key in FEATURE_DESCRIPTIONS) {
    const fd = FEATURE_DESCRIPTIONS[key];
    const el = document.getElementById('feat-' + key);
    if (!el) continue;
    if (fd.type === 'toggle') {
      el.checked = false;
    } else {
      const mid = ((fd.min + fd.max) / 2);
      el.value = mid;
      const valEl = document.getElementById('val-' + key);
      if (valEl) valEl.textContent = mid.toFixed(fd.step < 1 ? 1 : 0);
    }
  }
  document.getElementById('results-placeholder').style.display = 'block';
  document.getElementById('results-content').style.display = 'none';
}

// ─── Main predict function ────────────────────────────
async function predict() {
  const features  = collectFeatures();
  const caseName  = document.getElementById('case-name').value || 'Custom Case';

  // Show loading
  const btnText = document.getElementById('predict-btn-text');
  btnText.innerHTML = '<span class="spinner"></span>Analyzing…';

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features, case_name: caseName })
    });
    const data = await res.json();

    if (!data.success) throw new Error(data.error);

    renderResults(data.result);
  } catch (err) {
    alert('Error: ' + err.message);
  } finally {
    btnText.textContent = '⚡ Analyze Case';
  }
}

// ─── Render all results ───────────────────────────────
function renderResults(r) {
  document.getElementById('results-placeholder').style.display = 'none';
  document.getElementById('results-content').style.display = 'block';

  // Verdict card
  const vv = document.getElementById('verdict-value');
  vv.textContent = r.prediction;
  vv.className = 'verdict-value ' + r.prediction.toLowerCase();
  document.getElementById('verdict-confidence').textContent = `Confidence: ${r.confidence}%`;

  const aqPct = r.probabilities['Acquitted'];
  const conPct = r.probabilities['Convicted'];
  document.getElementById('verdict-bar-acquitted').style.width = aqPct + '%';
  document.getElementById('verdict-bar-convicted').style.width = conPct + '%';
  document.getElementById('prob-acq').textContent = aqPct + '%';
  document.getElementById('prob-con').textContent = conPct + '%';

  // NL explanation
  document.getElementById('nl-explanation').innerHTML = r.nl_explanation;

  // Charts
  renderLIME(r.lime_explanation);
  renderSHAP(r.shap_values);
  renderGlobal(r.global_feature_importance.slice(0, 8));
  renderVotes(r.vote_info);
  renderFeatureTable(r.input_features);

  // Scroll into view
  document.getElementById('results-content').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ─── LIME chart ───────────────────────────────────────
function renderLIME(limeData) {
  destroyChart('lime');
  const labels = limeData.map(d => formatLabel(d.feature));
  const values = limeData.map(d => d.coefficient);
  const colors = values.map(v => v > 0 ? 'rgba(255,107,107,0.8)' : 'rgba(62,207,142,0.8)');

  const ctx = document.getElementById('lime-chart').getContext('2d');
  charts['lime'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: 'LIME Coefficient', data: values, backgroundColor: colors, borderRadius: 5 }]
    },
    options: chartOpts('LIME Coefficient (positive → convicted, negative → acquitted)')
  });
}

// ─── SHAP chart ───────────────────────────────────────
function renderSHAP(shapData) {
  destroyChart('shap');
  const top = shapData.slice(0, 8);
  const labels = top.map(d => formatLabel(d.feature));
  const values = top.map(d => d.value);
  const colors = values.map(v => v > 0 ? 'rgba(255,107,107,0.8)' : 'rgba(62,207,142,0.8)');

  const ctx = document.getElementById('shap-chart').getContext('2d');
  charts['shap'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: 'SHAP Value', data: values, backgroundColor: colors, borderRadius: 5 }]
    },
    options: chartOpts('SHAP Value (positive → convicted, negative → acquitted)')
  });
}

// ─── Global importance chart ──────────────────────────
function renderGlobal(globalData) {
  destroyChart('global');
  const labels = globalData.map(d => formatLabel(d.feature));
  const values = globalData.map(d => d.importance);

  const ctx = document.getElementById('global-chart').getContext('2d');
  charts['global'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Feature Importance',
        data: values,
        backgroundColor: 'rgba(201,168,76,0.75)',
        borderRadius: 5
      }]
    },
    options: chartOpts('Mean Decrease in Gini Impurity')
  });
}

// ─── Vote visualization ───────────────────────────────
function renderVotes(vi) {
  const dotContainer = document.getElementById('vote-visual');
  dotContainer.innerHTML = '';
  for (let i = 0; i < vi.total_trees; i++) {
    const d = document.createElement('span');
    d.className = 'vote-dot ' + (i < vi.votes_convicted ? 'conv' : 'acqu');
    d.title = i < vi.votes_convicted ? 'Voted: Convicted' : 'Voted: Acquitted';
    dotContainer.appendChild(d);
  }

  const pctConv = ((vi.votes_convicted / vi.total_trees) * 100).toFixed(1);
  document.getElementById('vote-summary').innerHTML = `
    <span class="vs-conv">🔴 Convicted: ${vi.votes_convicted} trees (${pctConv}%)</span>
    <span class="vs-acqu">🟢 Acquitted: ${vi.votes_acquitted} trees (${(100 - pctConv).toFixed(1)}%)</span>
  `;
}

// ─── Feature table ────────────────────────────────────
function renderFeatureTable(inputFeatures) {
  const tbody = document.getElementById('feature-table-body');
  tbody.innerHTML = '';
  for (const key in inputFeatures) {
    const fd = FEATURE_DESCRIPTIONS[key];
    const label = fd ? fd.label : key;
    let val = inputFeatures[key];

    if (fd && fd.type === 'toggle')  val = val ? 'Yes' : 'No';
    if (fd && fd.type === 'select')  val = fd.options[val] || val;

    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${label}</td><td class="feat-val">${val}</td>`;
    tbody.appendChild(tr);
  }
}

// ─── Chart defaults ───────────────────────────────────
function chartOpts(yLabel) {
  return {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: ctx => ` ${ctx.parsed.x > 0 ? '+' : ''}${ctx.parsed.x.toFixed(4)}`
        }
      }
    },
    scales: {
      x: {
        grid: { color: 'rgba(255,255,255,0.05)' },
        ticks: { color: '#7a8099', font: { family: 'IBM Plex Mono', size: 11 } },
        title: { display: true, text: yLabel, color: '#7a8099', font: { size: 11 } }
      },
      y: {
        grid: { display: false },
        ticks: { color: '#e8eaf0', font: { family: 'IBM Plex Sans', size: 12 } }
      }
    }
  };
}

function formatLabel(key) {
  const fd = FEATURE_DESCRIPTIONS[key];
  return fd ? fd.label : key.replace(/_/g, ' ');
}
