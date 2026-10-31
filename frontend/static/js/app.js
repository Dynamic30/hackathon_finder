const BATCH = 30;
const state = { tier: "", status: "active", sort: "Urgency" };
let items = [];
let hasMore = true;
let loading = false;
let failed = false;
let notice = "";
let listRequest;
let detailRequest;

const $ = id => document.getElementById(id);
const list = $("list");
const sentinel = $("sentinel");
const search = $("search");
const clearBtn = $("clearBtn");
const modal = $("modal");
const settings = $("settingsOverlay");
const sortMenu = $("sortMenu");
const aiPopover = $("aiPopover");
const viewToggle = $("viewToggle");
const listSwitch = $("listSwitch");
const darkSwitch = $("darkSwitch");

const saved = key => { try { return localStorage.getItem(key); } catch (e) { return null; } };
const save = (key, value) => { try { localStorage.setItem(key, value); } catch (e) {} };

const field = (root, name) => root.querySelector(`[data-f="${name}"]`);
const setText = (root, values) => {
  for (const [name, text] of Object.entries(values)) field(root, name).textContent = text;
};

function chip(label, className = "tag") {
  const el = document.createElement("span");
  el.className = className;
  el.textContent = label;
  return el;
}

const deadline = h => h.reg_end_at || h.end_at;

function basics(h) {
  const label = sourceLabel(h.source);
  return {
    logo: [...h.title.trim()][0]?.toUpperCase() || "?",
    pill: h.priority_tier,
    org: h.organizer || label,
    src: "via " + label,
    title: h.title,
    location: formatLocation(h),
    mode: h.mode === "unknown" ? "—" : h.mode,
  };
}

function buildCard(h) {
  const card = $("cardTpl").content.firstElementChild.cloneNode(true);
  const days = daysLeft(deadline(h));
  const chips = h.tags.slice(0, 4).map(tag => chip(tag));
  const team = formatTeam(h.team_min, h.team_max);
  if (h.is_paid !== true) chips.push(chip("Free", "tag free"));
  if (team) chips.push(chip(team));

  card.classList.add("p-" + h.priority_tier);
  card.dataset.mode = h.mode;
  setText(card, { ...basics(h), prize: formatPrize(h.prize_amount, h.prize_currency) || "—", closes: formatCloses(days) });
  field(card, "pill").classList.add(h.priority_tier);
  field(card, "closesStat").classList.toggle("urgent", isUrgent(days));
  field(card, "tags").replaceChildren(...chips);
  card.addEventListener("click", () => openModal(h));
  card.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openModal(h);
    }
  });
  return card;
}

const matches = (h, q) =>
  !q || [h.title, h.organizer, formatLocation(h), ...h.tags].some(text => text?.toLowerCase().includes(q));

const query = () => search.value.trim().toLowerCase();

const observer = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting && !failed && !query()) loadMore();
}, { rootMargin: "300px" });

function watch(on) {
  observer.unobserve(sentinel);
  if (on) observer.observe(sentinel);
}

function updateStatus() {
  let text = "";
  if (failed) text = notice;
  else if (loading) text = items.length ? "Loading more…" : "Loading hackathons…";
  else if (!items.length) text = "No hackathons found.";
  else if (!list.children.length) text = "None of the hackathons loaded so far match your search.";
  else if (!hasMore) text = "No more hackathons";
  else if (query()) text = "Search covers loaded hackathons only. Clear it to load more.";
  $("status").hidden = !text;
  $("statusText").textContent = text;
  $("retry").hidden = !failed;
}

function renderAll() {
  const q = query();
  list.replaceChildren(...items.filter(h => matches(h, q)).map(buildCard));
  updateStatus();
  watch(hasMore && !failed && !loading);
}

async function loadMore() {
  if (loading || !hasMore) return;
  loading = true;
  failed = false;
  watch(false);
  updateStatus();
  listRequest = new AbortController();
  try {
    const rows = await fetchCards(state, items.length, BATCH, listRequest.signal);
    const fresh = rows.slice(0, BATCH);
    const q = query();
    hasMore = rows.length > BATCH;
    items.push(...fresh);
    list.append(...fresh.filter(h => matches(h, q)).map(buildCard));
    $("updatedAt").textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    $("updated").hidden = false;
  } catch (err) {
    if (err.name === "AbortError") return;
    failed = true;
    notice = err.message;
  }
  loading = false;
  updateStatus();
  watch(hasMore && !failed);
}

function reset() {
  listRequest?.abort();
  items = [];
  hasMore = true;
  loading = false;
  list.replaceChildren();
  window.scrollTo(0, 0);
  loadMore();
}

function fillModal(h) {
  const days = daysLeft(deadline(h));
  const label = sourceLabel(h.source);
  const about = h.description ? shorten(plainText(h.description, h.description_format), 400) : "";
  const linked = isHttpUrl(h.source_url);
  const date = new Date(deadline(h)).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });

  setText(modal, {
    ...basics(h),
    prize: formatPrize(h.prize_amount, h.prize_currency) || "Not listed",
    closes: formatCloses(days),
    team: formatTeam(h.team_min, h.team_max) || "Any",
    entry: h.is_paid === true ? "Paid" : "Free",
    regVerb: days === null ? "Registration deadline:" : days < 0 ? "Registration closed on" : "Registration closes",
    regDate: days === null ? "To be announced" : date,
    regCount: h.registrations ? ` · ${h.registrations.toLocaleString("en-IN")} registered so far` : "",
    description: about,
    sourceName: label,
    sourceUrl: h.source_url.replace(/^https?:\/\//i, "").slice(0, 44),
  });
  field(modal, "pill").classList.add(h.priority_tier);
  field(modal, "tags").replaceChildren(...h.tags.map(tag => chip(tag)));
  field(modal, "themes").hidden = !h.tags.length;
  field(modal, "about").hidden = !about;
  field(modal, "source").hidden = !linked;
  if (linked) field(modal, "link").href = h.source_url;
}

function setNote(text) {
  const note = field(modal, "note");
  note.textContent = text;
  note.hidden = !text;
}

async function openModal(h) {
  detailRequest?.abort();
  detailRequest = new AbortController();
  modal.replaceChildren($("modalTpl").content.cloneNode(true));
  fillModal(h);
  setNote("Loading details…");
  $("overlay").classList.add("open");
  try {
    const detail = await fetchCard(h.source, h.source_id, detailRequest.signal);
    fillModal({ ...detail, priority_tier: h.priority_tier });
    setNote("");
  } catch (err) {
    if (err.name === "AbortError") return;
    setNote("Couldn't load full details. " + err.message);
  }
}

function bindGroup(id, key) {
  const group = $(id);
  group.addEventListener("click", e => {
    const button = e.target.closest("button");
    if (!button || button.dataset.value === state[key]) return;
    group.querySelector(".active").classList.remove("active");
    button.classList.add("active");
    state[key] = button.dataset.value;
    reset();
  });
}

function setView(view) {
  list.classList.toggle("mode-list", view === "list");
  for (const button of viewToggle.children) button.classList.toggle("active", button.dataset.view === view);
  listSwitch.classList.toggle("on", view === "list");
  save("view", view);
}

function setDark(on) {
  document.documentElement.dataset.theme = on ? "dark" : "light";
  darkSwitch.classList.toggle("on", on);
  save("theme", on ? "dark" : "light");
}

bindGroup("tabs", "tier");
bindGroup("statusToggle", "status");

$("sortBtn").addEventListener("click", () => sortMenu.classList.toggle("open"));
sortMenu.addEventListener("click", e => {
  const item = e.target.closest(".sort-item");
  if (!item) return;
  sortMenu.classList.remove("open");
  if (item.dataset.value === state.sort) return;
  state.sort = item.dataset.value;
  $("sortLabel").textContent = item.textContent;
  reset();
});

viewToggle.addEventListener("click", e => {
  const button = e.target.closest("button");
  if (button) setView(button.dataset.view);
});
listSwitch.addEventListener("click", () => setView(listSwitch.classList.contains("on") ? "card" : "list"));
darkSwitch.addEventListener("click", () => setDark(!darkSwitch.classList.contains("on")));
$("themeToggle").addEventListener("click", () => setDark(!darkSwitch.classList.contains("on")));

search.addEventListener("input", () => {
  clearBtn.hidden = !search.value;
  renderAll();
});
clearBtn.addEventListener("click", () => {
  search.value = "";
  clearBtn.hidden = true;
  renderAll();
});

$("retry").addEventListener("click", loadMore);

$("settingsToggle").addEventListener("click", () => settings.classList.add("open"));
$("bannerBtn").addEventListener("click", () => {
  settings.classList.add("open");
  setTimeout(() => settings.querySelector(".about-block").scrollIntoView({ behavior: "smooth", block: "nearest" }), 200);
});
$("aiToggle").addEventListener("click", () => aiPopover.classList.toggle("open"));

document.addEventListener("click", e => {
  const overlay = e.target.closest(".overlay");
  if (overlay && (e.target === overlay || e.target.closest(".modal-close"))) overlay.classList.remove("open");
  if (!e.target.closest(".sort-wrap")) sortMenu.classList.remove("open");
  if (!e.target.closest(".ai-widget")) aiPopover.classList.remove("open");
});
document.addEventListener("keydown", e => {
  if (e.key === "Escape") document.querySelectorAll(".overlay.open").forEach(overlay => overlay.classList.remove("open"));
});

setView(saved("view") === "list" ? "list" : "card");
setDark(document.documentElement.dataset.theme === "dark");
loadMore();
