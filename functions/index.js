// Tar emot kontaktformuläret och bokningen från sabimedia.se och mejlar allt till hej@sabimedia.se.
const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const nodemailer = require("nodemailer");

const SMTP_PASSWORD = defineSecret("SMTP_PASSWORD");
const MAILBOX = "hej@sabimedia.se";
const ALLOWED_HOSTS = new Set(["sabimedia.se", "www.sabimedia.se", "sabimedia.web.app", "sabimedia.firebaseapp.com", "localhost", "127.0.0.1"]);
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// Fälten som får komma in, i den ordning de visas i mejlet
const FIELDS = [
  ["when", "Önskad tid för samtal", 100],
  ["how", "Samtalsform", 40],
  ["name", "Namn", 200],
  ["company", "Företag", 200],
  ["phone", "Telefon", 40],
  ["email", "E-post", 254],
  ["website", "Nuvarande hemsida", 300],
  ["plan", "Paket", 100],
  ["message", "Meddelande", 5000],
  ["source", "Skickat från", 60],
];

// Enkel broms mot spam: högst 5 utskick per 10 minuter från samma adress, per igång instans
const WINDOW_MS = 10 * 60 * 1000, MAX_PER_WINDOW = 5;
const recent = new Map();
function tooMany(ip, now = Date.now()) {
  const hits = (recent.get(ip) || []).filter(t => now - t < WINDOW_MS);
  hits.push(now);
  recent.set(ip, hits);
  if (recent.size > 5000) recent.clear();
  return hits.length > MAX_PER_WINDOW;
}

const esc = s => String(s).replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const oneLine = s => String(s).replace(/[\r\n]+/g, " ").trim();

function allowedOrigin(req) {
  const origin = req.get("origin");
  if (!origin) return true;
  try { return ALLOWED_HOSTS.has(new URL(origin).hostname); } catch { return false; }
}

// Plockar ut kända fält och klipper dem till maxlängd
function cleanFields(body) {
  const out = {};
  for (const [key, , max] of FIELDS) {
    const value = typeof body[key] === "string" ? body[key].trim().slice(0, max) : "";
    if (value) out[key] = key === "message" ? value : oneLine(value);
  }
  return out;
}

function buildMail(f) {
  const rows = FIELDS.filter(([key]) => f[key]).map(([key, label]) => [label, f[key]]);
  const subject = f.when ? `Bokat samtal: ${f.when} – ${f.name}` : `Ny hemsideförfrågan från ${f.company || f.name}`;
  return {
    from: `"Sabimedia hemsida" <${MAILBOX}>`,
    to: MAILBOX,
    replyTo: { name: f.name, address: f.email },
    subject,
    text: rows.map(([label, value]) => `${label}: ${value}`).join("\n"),
    html: `<table cellpadding="8" style="border-collapse:collapse;font-family:sans-serif;font-size:15px">${rows.map(([label, value]) =>
      `<tr><th align="left" valign="top" style="border-bottom:1px solid #e8e1d7">${esc(label)}</th><td style="border-bottom:1px solid #e8e1d7;white-space:pre-wrap">${esc(value)}</td></tr>`).join("")}</table>`,
  };
}

exports.kontakt = onRequest(
  { region: "europe-north1", secrets: [SMTP_PASSWORD], maxInstances: 3, memory: "256MiB", timeoutSeconds: 30 },
  async (req, res) => {
    res.set("Cache-Control", "no-store");
    const fail = (status, code) => res.status(status).json({ ok: false, code });

    if (req.method !== "POST") return fail(405, "METHOD");
    if (!allowedOrigin(req)) return fail(403, "ORIGIN");
    const body = req.body && typeof req.body === "object" ? req.body : {};
    if (body._honey) return res.json({ ok: true }); // Fälla för botar: låtsas att allt gick bra
    if (tooMany(req.ip || "okänd")) return fail(429, "RATE-LIMIT");

    const fields = cleanFields(body);
    if (!fields.name) return fail(400, "NAME");
    if (!fields.email || !EMAIL_RE.test(fields.email)) return fail(400, "EMAIL");

    const port = Number(process.env.SMTP_PORT || 465);
    const transport = nodemailer.createTransport({
      host: process.env.SMTP_HOST || "mail.sabimedia.se",
      port,
      secure: port === 465,
      auth: { user: MAILBOX, pass: SMTP_PASSWORD.value() },
    });
    try {
      await transport.sendMail(buildMail(fields));
      return res.json({ ok: true });
    } catch (err) {
      console.error("Mejlet kunde inte skickas:", err.code, err.responseCode, err.message);
      return fail(502, err.code === "EAUTH" ? "MAIL-AUTH" : "MAIL-FAILED");
    }
  }
);
