// Chess Analysis GUI — vanilla JS, no build step.

const $ = (sel) => document.querySelector(sel);
const SVG_NS = "http://www.w3.org/2000/svg";

const fmtPct = (x) => `${x.toFixed(1)}%`;
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function api(path, params = {}) {
  const qs = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== "" && v != null));
  const res = await fetch(`${path}?${qs}`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

function svgEl(tag, attrs = {}, parent) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  if (parent) parent.appendChild(el);
  return el;
}

// ── Tooltip ──────────────────────────────────────────────
const tooltip = $("#tooltip");
function showTip(evt, html) {
  tooltip.innerHTML = html;
  tooltip.hidden = false;
  const pad = 14;
  const { innerWidth: w } = window;
  const rect = tooltip.getBoundingClientRect();
  let x = evt.clientX + pad;
  if (x + rect.width > w - 8) x = evt.clientX - rect.width - pad;
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${Math.max(8, evt.clientY - rect.height - pad)}px`;
}
const hideTip = () => { tooltip.hidden = true; };

function resultBar(r, thin = false) {
  const t = r.win + r.draw + r.loss || 1;
  return `<div class="rbar${thin ? " thin" : ""}" data-tip="${r.win}W / ${r.draw}D / ${r.loss}L">
    ${r.win ? `<div class="w" style="flex:${r.win / t}"></div>` : ""}
    ${r.draw ? `<div class="d" style="flex:${r.draw / t}"></div>` : ""}
    ${r.loss ? `<div class="l" style="flex:${r.loss / t}"></div>` : ""}
  </div>`;
}

// Generic hover tooltips for any element carrying data-tip
document.addEventListener("mousemove", (e) => {
  const el = e.target.closest?.("[data-tip]");
  if (el) showTip(e, esc(el.dataset.tip));
  else if (!e.target.closest?.(".chart")) hideTip();
});

// ── Tabs ─────────────────────────────────────────────────
const loaded = {};
function showTab(name) {
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === name));
  document.querySelectorAll(".panel").forEach((p) => p.classList.toggle("active", p.id === `tab-${name}`));
  if (!loaded[name]) {
    loaded[name] = true;
    ({ overview: loadOverview, games: loadGames, openings: initOpenings })[name]();
  }
}
document.querySelectorAll(".tab").forEach((t) => t.addEventListener("click", () => showTab(t.dataset.tab)));

// ── Overview ─────────────────────────────────────────────
async function loadOverview() {
  const since = $("#ov-since").value;
  const data = await api("/api/stats", { time_class: $("#ov-time-class").value, since });
  $("#username").textContent = `— ${data.username}`;

  const o = data.overall;
  const trend = data.rating_trend;
  const last = trend[trend.length - 1];
  const first = trend.find((m) => m.games >= 10) || trend[0];
  $("#ov-tiles").innerHTML = [
    tile("Games", o.total.toLocaleString(), `${o.win}W / ${o.loss}L / ${o.draw}D`),
    tile("Score", fmtPct(o.score), "wins + ½ draws"),
    tile("Latest avg rating", last ? last.avg : "—", last ? `${last.month}` : ""),
    tile("Rating change", last && first ? signed(last.avg - first.avg) : "—", first ? `since ${first.month}` : ""),
  ].join("");

  drawRatingChart($("#ov-rating"), trend);

  const rows = [
    ...Object.entries(data.by_time_class).map(([k, r]) => [k[0].toUpperCase() + k.slice(1), r]),
    ["White", data.by_color.white],
    ["Black", data.by_color.black],
  ];
  $("#ov-results").innerHTML = rows.map(([name, r]) => `
    <div class="rbar-row">
      <span class="name">${name}</span>${resultBar(r)}
      <span class="meta">${fmtPct(r.score)} · ${r.total} games</span>
    </div>`).join("");

  const maxTerm = Math.max(...data.terminations.map(([, c]) => c), 1);
  $("#ov-terminations").innerHTML = data.terminations.map(([name, c]) => `
    <div class="hbar-row">
      <span class="name">${esc(name)}</span>
      <div><div class="hbar" style="width:${(c / maxTerm) * 100}%" data-tip="${esc(name)}: ${c} games"></div></div>
      <span class="meta">${c} · ${fmtPct((c / o.total) * 100)}</span>
    </div>`).join("");

  for (const color of ["white", "black"]) {
    $(`#ov-open-${color}`).innerHTML = openingsTable(data.openings[color], color);
  }
}

const tile = (label, value, sub) =>
  `<div class="tile"><div class="label">${label}</div><div class="value">${value}</div><div class="sub">${sub}</div></div>`;
const signed = (n) => (n > 0 ? `+${n}` : `${n}`);

function openingsTable(rows, color) {
  if (!rows.length) return `<p class="muted">No games.</p>`;
  return `<table class="data"><thead><tr><th>Opening</th><th class="num">Games</th><th>Score</th></tr></thead><tbody>
    ${rows.map((r) => `<tr class="clickable" data-opening="${esc(r.name)}" data-color="${color}" title="Explore this opening's move tree">
      <td>${esc(r.name)}</td><td class="num">${r.total}</td>
      <td><div class="score-cell">${resultBar(r, true)}<span class="num">${fmtPct(r.score)}</span></div></td>
    </tr>`).join("")}</tbody></table>`;
}

// Clicking an opening on the overview jumps to its move tree
document.addEventListener("click", (e) => {
  const row = e.target.closest("tr[data-opening]");
  if (!row) return;
  $("#op-name").value = row.dataset.opening;
  $("#op-color").value = row.dataset.color;
  showTab("openings");
  buildTree();
});

function drawRatingChart(container, trend) {
  container.innerHTML = "";
  if (!trend.length) { container.innerHTML = `<p class="muted">No rated games.</p>`; return; }
  const W = 900, H = 260, m = { t: 12, r: 16, b: 28, l: 44 };
  const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Monthly rating trend" }, container);
  const lo = Math.floor(Math.min(...trend.map((d) => d.low)) / 100) * 100;
  const hi = Math.ceil(Math.max(...trend.map((d) => d.peak)) / 100) * 100;
  const x = (i) => m.l + (trend.length === 1 ? (W - m.l - m.r) / 2 : (i / (trend.length - 1)) * (W - m.l - m.r));
  const y = (v) => m.t + (1 - (v - lo) / (hi - lo || 1)) * (H - m.t - m.b);

  const step = (hi - lo) / 100 > 8 ? 200 : 100;
  for (let v = lo; v <= hi; v += step) {
    svgEl("line", { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), class: v === lo ? "baseline" : "gridline" }, svg);
    svgEl("text", { x: m.l - 8, y: y(v) + 4, "text-anchor": "end" }, svg).textContent = v;
  }
  const every = Math.ceil(trend.length / 10);
  trend.forEach((d, i) => {
    if (i % every === 0 || i === trend.length - 1)
      svgEl("text", { x: x(i), y: H - 8, "text-anchor": "middle" }, svg).textContent = d.month;
  });

  const band = trend.map((d, i) => `${x(i)},${y(d.peak)}`).join(" ") + " " +
    trend.map((d, i) => `${x(i)},${y(d.low)}`).reverse().join(" ");
  svgEl("polygon", { points: band, fill: "var(--band)", opacity: 0.6 }, svg);
  svgEl("polyline", { points: trend.map((d, i) => `${x(i)},${y(d.avg)}`).join(" "), fill: "none",
    stroke: "var(--accent)", "stroke-width": 2, "stroke-linejoin": "round" }, svg);

  // Direct label on the latest point
  const li = trend.length - 1;
  svgEl("circle", { cx: x(li), cy: y(trend[li].avg), r: 4, fill: "var(--accent)", stroke: "var(--surface)", "stroke-width": 2 }, svg);

  const cross = svgEl("line", { y1: m.t, y2: H - m.b, class: "crosshair", visibility: "hidden" }, svg);
  const dot = svgEl("circle", { r: 4, fill: "var(--accent)", stroke: "var(--surface)", "stroke-width": 2, visibility: "hidden" }, svg);
  const hit = svgEl("rect", { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: "transparent" }, svg);
  hit.addEventListener("mousemove", (e) => {
    const pt = svg.getBoundingClientRect();
    const sx = ((e.clientX - pt.left) / pt.width) * W;
    const i = Math.max(0, Math.min(li, Math.round(((sx - m.l) / (W - m.l - m.r)) * li)));
    const d = trend[i];
    cross.setAttribute("x1", x(i)); cross.setAttribute("x2", x(i)); cross.setAttribute("visibility", "visible");
    dot.setAttribute("cx", x(i)); dot.setAttribute("cy", y(d.avg)); dot.setAttribute("visibility", "visible");
    showTip(e, `<div class="t-title">${d.month}</div>
      <div class="t-row">Average ${d.avg}</div><div class="t-row">Peak ${d.peak} · Low ${d.low}</div>
      <div class="t-row">${d.games} games</div>`);
  });
  hit.addEventListener("mouseleave", () => { cross.setAttribute("visibility", "hidden"); dot.setAttribute("visibility", "hidden"); hideTip(); });
}

$("#ov-time-class").addEventListener("change", loadOverview);
$("#ov-since").addEventListener("change", loadOverview);

// ── Games list ───────────────────────────────────────────
let gamesTimer;
async function loadGames() {
  const data = await api("/api/games", {
    q: $("#gm-q").value, result: $("#gm-result").value, time_class: $("#gm-time-class").value, limit: 300,
  });
  $("#gm-count").textContent = data.total > data.games.length
    ? `Showing ${data.games.length} of ${data.total} games` : `${data.total} games`;
  $("#gm-rows").innerHTML = data.games.map((g) => `
    <tr class="clickable" data-url="${esc(g.url)}">
      <td>${g.date}</td>
      <td><span class="pill ${g.result}">${g.result}</span></td>
      <td>${g.color === "white" ? "♔ White" : "♚ Black"}</td>
      <td>${esc(g.opponent)} <span class="muted">(${g.opp_rating ?? "?"})</span></td>
      <td>${esc(g.opening)}</td>
      <td>${esc(g.time_class)}</td>
      <td>${esc(g.termination)}</td>
      <td><button class="btn">Analyze</button></td>
    </tr>`).join("");
}
$("#gm-q").addEventListener("input", () => { clearTimeout(gamesTimer); gamesTimer = setTimeout(loadGames, 250); });
$("#gm-result").addEventListener("change", loadGames);
$("#gm-time-class").addEventListener("change", loadGames);
$("#gm-rows").addEventListener("click", (e) => {
  const row = e.target.closest("tr[data-url]");
  if (row) openGame(row.dataset.url);
});

// ── Game analysis view ───────────────────────────────────
const gv = { data: null, ply: 0, url: null };

$("#gv-back").addEventListener("click", () => {
  $("#game-view").hidden = true;
  $("#games-list-view").hidden = false;
});
$("#gv-time").addEventListener("change", () => gv.url && openGame(gv.url));
$("#gv-arrow").addEventListener("change", () => gv.data && renderPly());

async function openGame(url) {
  gv.url = url;
  gv.data = null;
  $("#games-list-view").hidden = true;
  $("#game-view").hidden = false;
  $("#gv-link").href = url;
  $("#gv-content").hidden = true;
  const status = $("#gv-status");
  status.className = "status";
  status.innerHTML = `<span class="spinner"></span>Analyzing with Stockfish (${$("#gv-time").value}s per move)… this can take a little while.`;
  try {
    const data = await api("/api/analyze", { url, time: $("#gv-time").value });
    if (gv.url !== url) return;
    gv.data = data;
    status.innerHTML = "";
    renderGame();
  } catch (err) {
    status.className = "status error";
    status.textContent = err.message;
  }
}

function renderGame() {
  const d = gv.data;
  const s = d.summary;
  $("#gv-content").hidden = false;
  $("#gv-title").innerHTML = `${esc(d.white)} vs ${esc(d.black)} <span class="pill ${s.result}">${s.result}</span>
    <span class="muted"> · ${s.date} · ${esc(s.time_class)} · ${esc(s.opening)}</span>`;

  const mine = d.moves.filter((m) => m.is_user);
  const count = (c) => mine.filter((m) => m.classification === c).length;
  // Average centipawn loss, capped per move so one mate swing doesn't dominate
  const acpl = mine.length ? Math.round(mine.reduce((a, m) => a + Math.min(Math.max(m.cp_loss, 0), 1000), 0) / mine.length) : 0;
  $("#gv-tiles").innerHTML = [
    tile(`<i class="sev blunder">??</i> Blunders`, count("blunder"), `≥ ${d.thresholds.blunder / 100} pawns lost`),
    tile(`<i class="sev mistake">?</i> Mistakes`, count("mistake"), `${d.thresholds.mistake / 100}–${d.thresholds.blunder / 100} pawns`),
    tile(`<i class="sev inaccuracy">?!</i> Inaccuracies`, count("inaccuracy"), `${d.thresholds.inaccuracy / 100}–${d.thresholds.mistake / 100} pawns`),
    tile("Avg centipawn loss", acpl, `over ${mine.length} of your moves`),
  ].join("");

  const errs = mine.filter((m) => m.classification);
  $("#gv-errors").innerHTML = errs.length ? errs.map((m) => `
    <div class="error-row" data-ply="${m.ply - 1}" title="Show the position before this move, with the engine's best move">
      <i class="sev ${m.classification}">${SEV[m.classification]}</i>
      <b>${esc(m.label)}</b>
      <span class="detail">best was <b>${esc(m.best)}</b></span>
      <span class="delta">${fmtEval(m.s1)} → ${fmtEval(m.s2)}</span>
    </div>`).join("") : `<p class="muted">No inaccuracies, mistakes, or blunders — clean game!</p>`;

  const rows = [];
  for (let i = 0; i < d.moves.length; i += 2) {
    rows.push(`<div class="num">${i / 2 + 1}.</div>${moveCell(d.moves[i])}${d.moves[i + 1] ? moveCell(d.moves[i + 1]) : "<div></div>"}`);
  }
  $("#gv-moves").innerHTML = rows.join("");

  drawEvalChart();
  gv.ply = 0;
  renderPly();
}

const SEV = { inaccuracy: "?!", mistake: "?", blunder: "??" };
const moveCell = (m) => `<div class="mv${m.is_user ? "" : " opp"}" data-ply="${m.ply}">
  ${esc(m.actual)}${m.is_user && m.classification ? ` <i class="sev ${m.classification}">${SEV[m.classification]}</i>` : ""}</div>`;

function fmtEval(cp) {
  if (cp >= 9000) return "+M";
  if (cp <= -9000) return "−M";
  return `${cp >= 0 ? "+" : "−"}${Math.abs(cp / 100).toFixed(1)}`;
}

document.addEventListener("click", (e) => {
  const el = e.target.closest("#gv-moves [data-ply], #gv-errors [data-ply]");
  if (el) { gv.ply = +el.dataset.ply; renderPly(); }
});
document.querySelectorAll("[data-nav]").forEach((b) => b.addEventListener("click", () => navigate(b.dataset.nav)));
document.addEventListener("keydown", (e) => {
  if (!gv.data || $("#game-view").hidden || e.target.matches("input, select")) return;
  const map = { ArrowLeft: "prev", ArrowRight: "next", Home: "start", End: "end" };
  if (map[e.key]) { e.preventDefault(); navigate(map[e.key]); }
});

function navigate(dir) {
  const n = gv.data.moves.length;
  gv.ply = { start: 0, prev: Math.max(0, gv.ply - 1), next: Math.min(n, gv.ply + 1), end: n }[dir];
  renderPly();
}

function renderPly() {
  const d = gv.data;
  const moves = d.moves;
  const cur = gv.ply > 0 ? moves[gv.ply - 1] : null;
  const next = moves[gv.ply]; // the move played from this position, whose "best" is the engine's choice here
  const params = new URLSearchParams({ fen: cur ? cur.fen : d.start_fen, flip: d.user_color === "black" ? "1" : "0" });
  if (cur) params.set("lastmove", cur.uci);
  if (next?.best_uci && $("#gv-arrow").checked) params.set("best", next.best_uci);
  $("#gv-board").src = `/api/board.svg?${params}`;

  let info = cur
    ? `<b>${esc(cur.label)}</b>${cur.classification && cur.is_user ? ` <i class="sev ${cur.classification}">${SEV[cur.classification]}</i>` : ""} · eval <b>${fmtEval(cur.s2)}</b>`
    : `<b>Starting position</b> · eval <b>${moves.length ? fmtEval(moves[0].s1) : "—"}</b>`;
  if (next) {
    const agreed = next.best === next.actual;
    info += `<br>Engine's best here: <b style="color:var(--best)">${esc(next.best)}</b>` +
      (agreed ? " (played)" : ` · played <b>${esc(next.actual)}</b>`);
  }
  $("#gv-move-info").innerHTML = info;

  document.querySelectorAll("#gv-moves .mv").forEach((el) => el.classList.toggle("current", +el.dataset.ply === gv.ply));
  $("#gv-moves .mv.current")?.scrollIntoView({ block: "nearest" });
  gv.cursor?.(gv.ply);
}

function drawEvalChart() {
  const container = $("#gv-eval");
  container.innerHTML = "";
  const moves = gv.data.moves;
  const W = 720, H = 200, m = { t: 10, r: 10, b: 20, l: 34 };
  const CAP = 1000; // clamp evals to ±10 pawns so the chart stays readable
  const pts = [{ ply: 0, v: moves[0]?.s1 ?? 0 }, ...moves.map((mv) => ({ ply: mv.ply, v: mv.s2 }))];
  const n = Math.max(1, pts.length - 1);
  const x = (ply) => m.l + (ply / n) * (W - m.l - m.r);
  const y = (cp) => m.t + (1 - (Math.max(-CAP, Math.min(CAP, cp)) + CAP) / (2 * CAP)) * (H - m.t - m.b);
  const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Evaluation over the game" }, container);

  for (const v of [-1000, -500, 500, 1000]) {
    svgEl("line", { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), class: "gridline" }, svg);
    svgEl("text", { x: m.l - 6, y: y(v) + 4, "text-anchor": "end" }, svg).textContent = `${v > 0 ? "+" : ""}${v / 100}`;
  }
  svgEl("text", { x: m.l - 6, y: y(0) + 4, "text-anchor": "end" }, svg).textContent = "0";

  const line = pts.map((p) => `${x(p.ply)},${y(p.v)}`).join(" ");
  svgEl("polygon", { points: `${x(0)},${y(0)} ${line} ${x(n)},${y(0)}`, fill: "var(--eval-white)" }, svg);
  svgEl("line", { x1: m.l, x2: W - m.r, y1: y(0), y2: y(0), class: "baseline" }, svg);
  svgEl("polyline", { points: line, fill: "none", stroke: "var(--eval-line)", "stroke-width": 2, "stroke-linejoin": "round" }, svg);

  const cursor = svgEl("line", { y1: m.t, y2: H - m.b, stroke: "var(--accent)", "stroke-width": 2 }, svg);
  const cross = svgEl("line", { y1: m.t, y2: H - m.b, class: "crosshair", visibility: "hidden" }, svg);

  for (const mv of moves) {
    if (!mv.is_user || !mv.classification) continue;
    svgEl("circle", { cx: x(mv.ply), cy: y(mv.s2), r: 5, fill: `var(--${mv.classification})`,
      stroke: "var(--surface)", "stroke-width": 2, "pointer-events": "none" }, svg);
  }

  gv.cursor = (ply) => { cursor.setAttribute("x1", x(ply)); cursor.setAttribute("x2", x(ply)); };

  const plyAt = (e) => {
    const r = svg.getBoundingClientRect();
    const sx = ((e.clientX - r.left) / r.width) * W;
    return Math.max(0, Math.min(n, Math.round(((sx - m.l) / (W - m.l - m.r)) * n)));
  };
  const hit = svgEl("rect", { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: "transparent", style: "cursor:pointer" }, svg);
  hit.addEventListener("mousemove", (e) => {
    const ply = plyAt(e);
    cross.setAttribute("x1", x(ply)); cross.setAttribute("x2", x(ply)); cross.setAttribute("visibility", "visible");
    const mv = moves[ply - 1];
    showTip(e, mv
      ? `<div class="t-title">${esc(mv.label)} ${mv.is_user && mv.classification ? `<i class="sev ${mv.classification}">${SEV[mv.classification]}</i>` : ""}</div>
         <div class="t-row">Eval ${fmtEval(mv.s2)}</div>${mv.best !== mv.actual ? `<div class="t-row">Best: ${esc(mv.best)}</div>` : ""}`
      : `<div class="t-title">Start</div>`);
  });
  hit.addEventListener("mouseleave", () => { cross.setAttribute("visibility", "hidden"); hideTip(); });
  hit.addEventListener("click", (e) => { gv.ply = plyAt(e); renderPly(); });
}

// ── Openings ─────────────────────────────────────────────
async function initOpenings() {
  const names = await api("/api/openings");
  $("#op-names").innerHTML = names.slice(0, 300)
    .map((o) => `<option value="${esc(o.name)}">${o.games} games</option>`).join("");
  if (!$("#op-content").hidden || $("#op-status").textContent) return;
  buildTree();
}

$("#op-go").addEventListener("click", buildTree);
$("#op-name").addEventListener("keydown", (e) => { if (e.key === "Enter") buildTree(); });

async function buildTree() {
  const status = $("#op-status");
  status.className = "status";
  status.innerHTML = `<span class="spinner"></span>Building tree…`;
  try {
    const data = await api("/api/opening_tree", {
      opening: $("#op-name").value, color: $("#op-color").value,
      depth: $("#op-depth").value, min_games: $("#op-min").value,
    });
    status.innerHTML = "";
    renderTree(data);
  } catch (err) {
    status.className = "status error";
    status.textContent = err.message;
    $("#op-content").hidden = true;
  }
}

function renderTree(data) {
  $("#op-content").hidden = false;
  const t = data.tree;
  $("#op-title").textContent = `${data.opening}${data.color ? ` as ${data.color}` : ""} — ${t.win}W / ${t.loss}L / ${t.draw}D (${fmtPct(t.score)}, ${t.games} games)`;
  const myFirst = data.my_color === "white";
  const flip = data.my_color === "black" ? "1" : "0";

  const nodeHtml = (node, ply) => {
    // With mixed colors we can't say whose move it is, so flag weak branches on every row
    const isMine = data.color ? (ply % 2 === 0) === myFirst : true;
    const who = data.color ? (isMine ? "You" : "Opp") : "";
    const num = Math.floor(ply / 2) + 1;
    const label = ply % 2 === 0 ? `${num}. ${node.move}` : `${num}… ${node.move}`;
    const warn = isMine && node.score < 45;
    const kids = node.children.map((c) => nodeHtml(c, ply + 1)).join("");
    return `<li${ply >= 6 ? ' class="collapsed"' : ""}>
      <div class="tree-row" data-path="${esc(node.path.join(","))}">
        <span class="toggle">${node.children.length ? (ply >= 6 ? "▸" : "▾") : ""}</span>
        <span class="mvname">${esc(label)} ${warn ? '<span class="warn" title="You score below 45% after this move">⚠</span>' : ""}</span>
        <span class="who">${who}</span>
        <span class="count">${node.games} g</span>
        ${resultBar(node, true)}
        <span class="pct">${node.score.toFixed(0)}%</span>
      </div>
      ${kids ? `<ul>${kids}</ul>` : ""}
    </li>`;
  };
  $("#op-tree").innerHTML = t.children.length
    ? `<ul>${t.children.map((c) => nodeHtml(c, 0)).join("")}</ul>`
    : `<p class="muted">No branches with at least ${$("#op-min").value} games — try lowering “Min games”.</p>`;

  $("#op-tree").dataset.flip = flip;
  showOpeningPosition([]);
}

function showOpeningPosition(path) {
  const params = new URLSearchParams({ flip: $("#op-tree").dataset.flip });
  if (path.length) params.set("moves", path.join(","));
  $("#op-board").src = `/api/board.svg?${params}`;
  $("#op-line").innerHTML = path.length
    ? `<b>${path.map((mv, i) => (i % 2 === 0 ? `${i / 2 + 1}. ${esc(mv)}` : esc(mv))).join(" ")}</b>`
    : `<b>Starting position</b> — click a move in the tree`;
}

$("#op-tree").addEventListener("click", (e) => {
  const row = e.target.closest(".tree-row");
  if (!row) return;
  const li = row.parentElement;
  if (e.target.closest(".toggle") && li.querySelector("ul")) {
    li.classList.toggle("collapsed");
    row.querySelector(".toggle").textContent = li.classList.contains("collapsed") ? "▸" : "▾";
    return;
  }
  document.querySelectorAll(".tree-row.selected").forEach((r) => r.classList.remove("selected"));
  row.classList.add("selected");
  if (li.classList.contains("collapsed")) {
    li.classList.remove("collapsed");
    row.querySelector(".toggle").textContent = "▾";
  }
  showOpeningPosition(row.dataset.path.split(","));
});

showTab("overview");
