/* Kör sidans egen kod för paketen (CONFIG och Pricing i sabimedia.html) och sparar resultatet i HTML-koden.
   Priser och innehåll ändras alltså fortfarande bara i CONFIG. Körs av build-site.sh. */
const fs = require("fs");
const vm = require("vm");

const cut = (text, from, to) => {
  const a = text.indexOf(from), b = text.indexOf(to, a);
  if (a < 0 || b < 0) throw new Error(`prerender-priser: hittar inte "${from}" … "${to}"`);
  return text.slice(a, b);
};

for (const file of ["site/index.html", "site/priser.html"]) {
  let html = fs.readFileSync(file, "utf8");
  const ids = ["plans", "prices", "price-note"].filter(id => html.includes(`id="${id}"></`));
  if (!ids.includes("plans")) throw new Error("prerender-priser: paketen saknas i " + file);
  const els = Object.fromEntries(ids.map(id => ["#" + id, { children: [], innerHTML: "", textContent: "", addEventListener() {} }]));
  const code = cut(html, "const CONFIG = {", "const $ =")
    + cut(html, "const esc =", "\n")
    + "\n" + cut(html, "if ($(\"#plans\")) {", "if (CONFIG.booking)");
  vm.runInNewContext(code, { $: s => els[s] ?? null });
  for (const id of ids) {
    const content = els["#" + id].innerHTML || els["#" + id].textContent;
    if (!content) throw new Error(`prerender-priser: #${id} blev tom i ${file}`);
    html = html.replace(`id="${id}"></`, () => `id="${id}">${content}</`);
  }
  fs.writeFileSync(file, html);
}
