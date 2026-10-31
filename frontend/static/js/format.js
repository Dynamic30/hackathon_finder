const DAY = 86400000;
const SOURCES = { unstop: "Unstop", hackerearth: "HackerEarth", devfolio: "Devfolio", devpost: "Devpost", hack2skill: "Hack2Skill" };
const CURRENCIES = { INR: "₹", USD: "$" };

function sourceLabel(source) {
  return SOURCES[source] || source;
}

function isHttpUrl(url) {
  return /^https?:\/\//i.test(url);
}

function formatPrize(amount, currency) {
  if (!amount) return null;
  const symbol = CURRENCIES[currency] ?? (currency ? currency + " " : "₹");
  const short = (n, unit) => symbol + +n.toFixed(1) + unit;
  const indian = !currency || currency === "INR";
  if (indian && amount >= 100000) return short(amount / 100000, "L");
  if (!indian && amount >= 1000000) return short(amount / 1000000, "M");
  if (amount >= 1000) return short(amount / 1000, "k");
  return symbol + amount;
}

function formatLocation(h) {
  if (h.mode === "online") return "Online";
  const place = [h.city, h.state].filter(Boolean).join(", ");
  if (place) return place;
  if (h.country) return h.country;
  if (h.location_raw) return shorten(h.location_raw, 40);
  return h.mode === "hybrid" ? "Hybrid" : "In-person";
}

function formatTeam(min, max) {
  if (!min && !max) return null;
  if (min === 1 && (!max || max === 1)) return "Solo";
  if (min && max) return min === max ? `Team of ${max}` : `${min}–${max}`;
  return max ? `Up to ${max}` : `${min}+`;
}

function daysLeft(iso, now = Date.now()) {
  const time = Date.parse(iso);
  if (isNaN(time)) return null;
  return time < now ? -1 : Math.floor((time - now) / DAY);
}

function formatCloses(days) {
  if (days === null) return "TBA";
  if (days < 0) return "Closed";
  if (days === 0) return "Today";
  return days === 1 ? "1 day" : days + " days";
}

function isUrgent(days) {
  return days !== null && days >= 0 && days <= 3;
}

function shorten(text, max) {
  return text.length > max ? text.slice(0, max - 1).trimEnd() + "…" : text;
}

function plainText(text, format) {
  const stripped = format === "html"
    ? new DOMParser().parseFromString(text.replace(/<(script|style)[\s\S]*?<\/\1>/gi, "").replace(/<[^>]*>/g, " "), "text/html").body.textContent
    : text.replace(/!?\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/^#+\s*/gm, "").replace(/[*`]/g, "");
  return stripped.replace(/\s+/g, " ").trim();
}
