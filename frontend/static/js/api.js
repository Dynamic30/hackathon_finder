const ERRORS = {
  404: "Not found.",
  429: "Too many requests, wait a moment.",
  network: "Can't reach the server. Check your connection.",
  other: "Something went wrong. Try again.",
};

async function getJSON(url, signal) {
  const res = await fetch(url, { signal }).catch(err => {
    throw err.name === "AbortError" ? err : new Error(ERRORS.network);
  });
  if (!res.ok) throw new Error(ERRORS[res.status] || ERRORS.other);
  return res.json();
}

function fetchCards({ tier, status, sort }, skip, batch, signal) {
  const params = new URLSearchParams({ sort_by: sort, status, skip, limit: batch + 1 });
  if (tier) params.set("tier", tier);
  return getJSON(`/v1/all_cards?${params}`, signal);
}

function fetchCard(source, sourceId, signal) {
  return getJSON(`/v1/cards/${encodeURIComponent(source)}/${encodeURIComponent(sourceId)}`, signal);
}
