/* Sökfunktion för sabimedia.se – laddas på alla sidor.
   Lägger till en sökknapp i toppmenyn och öppnar en sökruta (även med / eller Cmd/Ctrl+K).
   Allt sökbart innehåll ligger i INDEX nedan. Ändrar du priser, paket eller frågor på sidan – uppdatera här också. */
(() => {
  const INDEX = [
    // Startsidan
    { t: "Startsidan", p: "Hem", u: "/", d: "Hemsidor för småföretag i hela Sverige med fast engångspris från 1 200 kr exkl. moms.", k: "webbyrå borås hemsida småföretag sverige" },
    { t: "Tjänster – det här ingår", p: "Hem", u: "/#ingar", d: "Egen adminpanel, produkter och varukorg, ditt varumärke, betalning på sidan, beställningar via mejl, information och kontakt.", k: "funktioner adminpanel varukorg betalning beställningar mejl varumärke design" },
    { t: "Exempel på hemsidor", p: "Hem", u: "/#exempel", d: "Klädbutiken Studio Ofelia, Restaurang Ruta och städföretaget H.F StädService AB.", k: "exempel design studio ofelia restaurang ruta städ städservice klädbutik portfolio" },
    { t: "Kundomdömen", p: "Hem", u: "/#omdomen", d: "Vad kunderna säger, svar inom 24 timmar och vad du kan räkna med.", k: "recension omdöme cookie munch svarstid 24 timmar" },
    { t: "Så funkar det", p: "Hem", u: "/#sa-funkar-det", d: "Från idé till färdig hemsida, steg för steg.", k: "process steg arbetsgång hur går det till leverans lansering" },
    { t: "Priser och paket", p: "Hem", u: "/#priser", d: "Start från 1 200 kr, Business från 2 500 kr och Custom från 4 000 kr. Engångspris exkl. moms.", k: "pris priser kostnad kostar paket start business custom offert moms engångspris" },
    { t: "Paket Start – från 1 200 kr", p: "Priser", u: "/#priser", d: "Upp till 3 sidor, egen design, mobilanpassning, kontaktformulär, karta och grundläggande Google-anpassning. 1 månads support.", k: "pris kostnad start billigast enkel liten hemsida 1200" },
    { t: "Paket Business – från 2 500 kr", p: "Priser", u: "/#priser", d: "Allt i Start plus fler sidor, formulär för offert, bokning eller beställning, recensioner, gallerier och automatiska mejl. 2 månaders support.", k: "pris kostnad business mest komplett bokning offert recensioner galleri 2500" },
    { t: "Paket Custom – från 4 000 kr", p: "Priser", u: "/#priser", d: "Skräddarsydd lösning: bokningssystem med kalender, webbshop med betalning, kundkonton, adminpanel och integrationer.", k: "pris kostnad custom webbshop bokningssystem kalender kundkonton adminpanel integrationer betalning 4000 offert" },
    { t: "Tillägg utanför paketen", p: "Priser", u: "/#priser", d: "Vill du ha något som inte ingår i paketet? Då tar vi fram en offert och skräddarsyr funktionen.", k: "tillägg extra funktion offert skräddarsy" },
    { t: "Allt står i ditt namn", p: "Hem", u: "/#agande", d: "Domän, webbhotell och hemsida står på dig – du är aldrig inlåst hos oss.", k: "äga ägande domän webbhotell inlåst" },
    { t: "Vanliga frågor (FAQ)", p: "Hem", u: "/#fragor", d: "Svar på de vanligaste frågorna om pris, tid, ägande och support.", k: "faq frågor svar hjälp" },
    { t: "Kontakt och förfrågan", p: "Hem", u: "/#kontakt", d: "Skicka en förfrågan eller boka ett kostnadsfritt samtal via Microsoft Teams. Vi svarar inom 24 timmar.", k: "kontakt kontakta mejl e-post hej@sabimedia.se formulär förfrågan" },
    // Vanliga frågor
    { t: "Får jag en egen design?", p: "FAQ", u: "/#faq-1", d: "Ja. Varje hemsida skräddarsys efter ditt företag – dina färger, din logga, dina bilder och dina texter.", k: "design unik mall logga färger" },
    { t: "Hur lång tid tar det?", p: "FAQ", u: "/#faq-2", d: "Allt från några dagar upp till några veckor, beroende på paket och funktioner.", k: "tid leveranstid veckor dagar snabbt" },
    { t: "Tillkommer det dolda kostnader?", p: "FAQ", u: "/#faq-3", d: "Nej. Priset är fast och godkänns innan vi börjar. Domän och webbhotell betalar du direkt till leverantören.", k: "dolda kostnader avgift månadsavgift löpande" },
    { t: "Tänk om jag inte gillar sidan?", p: "FAQ", u: "/#faq-4", d: "Du får se en klickbar första version som du kan påverka. Inget går live innan du har godkänt det.", k: "ändringar godkänna nöjd" },
    { t: "Jag har ingen tid för en hemsida", p: "FAQ", u: "/#faq-5", d: "Du behöver vara så lite inblandad som möjligt – du läser bara igenom och godkänner.", k: "tid upptagen enkelt" },
    { t: "Vad händer om ni försvinner?", p: "FAQ", u: "/#faq-6", d: "Sidan byggs med beprövad teknik som vilken webbutvecklare som helst kan ta över.", k: "försvinner ta över utvecklare" },
    { t: "Vad händer om hemsidan blir hackad?", p: "FAQ", u: "/#faq-7", d: "Modern teknik utan tillägg som måste uppdateras, och SSL. Hjälp efter supportperioden tar vi per timme.", k: "hackad säkerhet ssl underhåll timpris" },
    { t: "Kan jag ändra produkter och priser själv?", p: "FAQ", u: "/#faq-8", d: "Med Custom får du en administrationssida. Annars hjälper vi dig under supportperioden.", k: "ändra själv admin cms uppdatera" },
    { t: "Hur får jag betalt?", p: "FAQ", u: "/#faq-9", d: "Med Custom kan kunden betala direkt på hemsidan. Med Business skickas beställningar till dig via mejl.", k: "betalning betalt swish kort kassa" },
    { t: "Vem äger hemsidan?", p: "FAQ", u: "/#faq-10", d: "Du. Domän, webbhotell och hemsida står i ditt namn.", k: "äga ägare" },
    { t: "Ingår publicering?", p: "FAQ", u: "/#faq-11", d: "Ja, i alla paket. Support i 1 månad (Start), 2 månader (Business) eller enligt offert (Custom).", k: "publicering lansering support underhåll" },
    { t: "Passar det mitt företag?", p: "FAQ", u: "/#faq-12", d: "Vi bygger hemsidor för alla typer av småföretag – butiker, salonger, caféer, hantverkare, konsulter och mer.", k: "passar bransch företag" },
    // Branscher
    { t: "Branscher vi hjälper", p: "Branscher", u: "/branscher", d: "Tio branscher vi bygger hemsidor åt – från restauranger till föreningar.", k: "branscher bransch kategorier" },
    { t: "Mat & livsmedel", p: "Branscher", u: "/branscher#mat", d: "Restauranger, caféer, bagerier och catering.", k: "restaurang lunch café kafé konditori bageri foodtruck gatukök catering gårdsbutik livsmedel mat" },
    { t: "Skönhet & välmående", p: "Branscher", u: "/branscher#skonhet", d: "Salonger, kliniker, terapeuter och träningsverksamheter.", k: "frisör barberare massage spa fysioterapeut naprapat psykoterapeut terapeut tandläkare tandklinik optiker gym träning pt personlig tränare skönhet salong" },
    { t: "Hem & fastighet", p: "Branscher", u: "/branscher#hem", d: "Städföretag, mäklare, fastighetsservice och boenden.", k: "städ städföretag lokalvård hotell pensionat stuga stuguthyrning semesterboende mäklare fastighet" },
    { t: "Butiker & produkter", p: "Branscher", u: "/branscher#butiker", d: "Detaljhandel, blomsterbutiker och produktvarumärken.", k: "butik detaljhandel blommor florist present inredning specialbutik produkter varumärke producent webbshop" },
    { t: "Kreativa tjänster", p: "Branscher", u: "/branscher#kreativa", d: "Fotografer och andra kreativa verksamheter.", k: "fotograf bröllopsfotograf porträtt produktfoto event foto kreativ" },
    { t: "Fritid & aktiviteter", p: "Branscher", u: "/branscher#fritid", d: "Föreningar, sportklubbar och aktivitetsföretag.", k: "förening idrottsförening sportklubb träningsförening aktivitet fritid klubb" },
    { t: "Event & fest", p: "Branscher", u: "/branscher#event", d: "Eventplanerare, festlokaler och bröllopsplanerare.", k: "event fest festlokal bröllop bröllopsplanerare" },
    { t: "Utbildning & kurser", p: "Branscher", u: "/branscher#utbildning", d: "Privata utbildare, kursverksamheter och musikskolor.", k: "utbildning kurs kurser musikskola lärare" },
    { t: "Konsult- & företagstjänster", p: "Branscher", u: "/branscher#konsult", d: "Fristående konsulter, redovisningsbyråer och mindre rådgivningsföretag.", k: "konsult redovisning bokföring byrå rådgivning" },
    { t: "Personliga tjänster", p: "Branscher", u: "/branscher#personliga", d: "Skräddare, sömmerskor och reparationsföretag.", k: "skräddare sömmerska reparation laga" },
    // Om oss
    { t: "Om oss", p: "Om oss", u: "/om-oss", d: "Sabimedia är en webbyrå i Borås som bygger hemsidor åt småföretag i hela Sverige.", k: "om sabi sabimedia företaget" },
    { t: "Teamet – Safiya och Warda", p: "Om oss", u: "/om-oss#team", d: "Safiya Ibrahim, grundare och lead developer. Warda, head of design och user experience.", k: "team personal safiya warda grundare designer utvecklare" },
    { t: "Företagsuppgifter", p: "Om oss", u: "/om-oss#team", d: "Enskild firma med F-skatt, org.nr 010928-2947, Borås.", k: "org.nr organisationsnummer f-skatt enskild firma adress instagram" },
    // Övriga sidor
    { t: "Boka ett kostnadsfritt samtal", p: "Boka", u: "/boka", d: "Välj dag och tid för ett samtal via Microsoft Teams.", k: "boka samtal möte teams tid kalender gratis kostnadsfritt" },
    { t: "Kundcase: Cookie Munch", p: "Kundcase", u: "/kundcase-cookie-munch", d: "Hur bageriet Cookie Munch fick beställningarna samlade på en egen hemsida.", k: "kundcase case referens cookie munch bageri resultat" },
    { t: "Integritetspolicy", p: "Integritet", u: "/integritetspolicy", d: "Hur vi behandlar personuppgifter, dina rättigheter och hur länge vi sparar uppgifter.", k: "integritet gdpr personuppgifter cookies dataskydd policy" },
    { t: "Dina rättigheter (GDPR)", p: "Integritet", u: "/integritetspolicy#rattigheter", d: "Rätt till information, rättelse, radering och att invända.", k: "gdpr rättigheter radera" },
    { t: "Hur länge vi sparar uppgifter", p: "Integritet", u: "/integritetspolicy#lagring", d: "Hur länge dina personuppgifter sparas.", k: "lagring spara radering" }
  ];

  const norm = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const esc = s => String(s).replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
  const items = INDEX.map(x => ({ ...x, nt: norm(x.t), nd: norm(x.d), nk: norm(x.k || "") }));

  function search(q) {
    const words = norm(q).split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    return items.map(x => {
      let score = 0;
      for (const w of words) {
        const s = (x.nt.startsWith(w) ? 12 : 0) + (new RegExp("\\b" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(x.nt) ? 8 : x.nt.includes(w) ? 5 : 0)
          + (x.nk.includes(w) ? 4 : 0) + (x.nd.includes(w) ? 2 : 0);
        if (!s) return null; // alla ord måste träffa
        score += s;
      }
      return { x, score };
    }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 8).map(r => r.x);
  }
  // Markerar sökorden i texten (även när användaren skriver utan å, ä, ö)
  function mark(text, q) {
    const words = norm(q).split(/\s+/).filter(w => w.length > 1);
    if (!words.length) return esc(text);
    const n = norm(text); const hits = new Array(text.length).fill(false);
    words.forEach(w => { let i = n.indexOf(w); while (i > -1) { for (let j = i; j < i + w.length; j++) hits[j] = true; i = n.indexOf(w, i + 1); } });
    let out = "", open = false;
    [...text].forEach((c, i) => { if (hits[i] && !open) { out += "<mark>"; open = true; } if (!hits[i] && open) { out += "</mark>"; open = false; } out += esc(c); });
    return out + (open ? "</mark>" : "");
  }

  const css = `
.sok-btn{display:inline-flex;align-items:center;justify-content:center;gap:.45rem;height:44px;min-width:44px;padding:0 .8rem;border-radius:12px;border:1.5px solid rgba(255,255,255,.3);background:transparent;color:#ece8e2;font:inherit;font-weight:600;font-size:.92rem;cursor:pointer;transition:border-color .2s,color .2s}
.sok-btn:hover{border-color:#fff;color:#fff}
.sok-btn svg{width:19px;height:19px;flex:none}
@media (max-width:900px){.sok-btn{margin-left:auto;padding:0;width:44px}.sok-btn span{display:none}.sok-btn + .nav-cta{margin-left:.5rem}}
.sok{border:0;padding:0;margin:0;max-width:none;max-height:none;width:100%;height:100%;background:transparent;color:var(--ink)}
.sok::backdrop{background:rgba(20,16,24,.18)}
.sok-panel{width:min(640px,calc(100% - 32px));margin:min(12vh,96px) auto 0;background:var(--paper);border:1px solid var(--line);border-radius:20px;box-shadow:0 30px 80px -20px rgba(0,0,0,.45);overflow:hidden;animation:sok-in .22s cubic-bezier(.2,.7,.2,1)}
@keyframes sok-in{from{opacity:0;transform:translateY(-10px) scale(.98)}to{opacity:1;transform:none}}
.sok-field{display:flex;align-items:center;gap:.7rem;padding:0 14px 0 18px;border-bottom:1px solid var(--line)}
.sok-field svg{width:22px;height:22px;flex:none;color:var(--accent)}
.sok-field input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:1.1rem;color:var(--ink);padding:18px 0;outline:none}
.sok-field input::-webkit-search-cancel-button{display:none}
.sok-close{border:0;background:var(--bg);color:var(--ink);border-radius:10px;font:inherit;font-size:.8rem;font-weight:600;padding:.45rem .7rem;cursor:pointer}
.sok-body{max-height:min(60vh,480px);overflow:auto;padding:8px;animation:sok-drop .2s ease}
.sok-panel:not(.has-q) .sok-body{display:none}
.sok-panel:not(.has-q) .sok-field{border-bottom:0}
@keyframes sok-drop{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.sok-head{margin:8px 10px 6px;font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.sok-list{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.sok-list a{display:grid;grid-template-columns:1fr auto;gap:.15rem 1rem;padding:12px 12px;border-radius:12px;text-decoration:none;color:var(--ink)}
.sok-list b{font-weight:600;font-size:1rem}
.sok-list small{grid-column:1;color:var(--ink-soft);font-size:.88rem;line-height:1.45}
.sok-list em{grid-row:1;grid-column:2;font-style:normal;font-size:.75rem;font-weight:600;color:var(--accent-deep);background:var(--bg);border-radius:999px;padding:.15rem .6rem;align-self:start;white-space:nowrap}
.sok-list [aria-selected="true"] a,.sok-list a:hover{background:var(--bg)}
.sok-list [aria-selected="true"] a{box-shadow:inset 3px 0 0 var(--accent)}
.sok-list mark{background:rgba(212,44,51,.14);color:inherit;border-radius:3px;padding:0 1px}
.sok-empty{padding:22px 12px;color:var(--ink-soft)}
.sok-empty a{color:var(--accent-deep);font-weight:600}
@media (max-width:600px){.sok-panel{margin-top:12px}.sok-body{max-height:calc(100dvh - 120px)}}
@media (prefers-reduced-motion:reduce){.sok-panel,.sok-body{animation:none}}
.faq details:target{box-shadow:0 0 0 2px var(--accent)}
.faq details{scroll-margin-top:110px}`;
  document.head.insertAdjacentHTML("beforeend", `<style>${css}</style>`);

  const icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
  const mac = /Mac|iPhone|iPad/.test(navigator.platform);
  const btn = document.createElement("button");
  btn.type = "button"; btn.className = "sok-btn"; btn.setAttribute("aria-label", "Sök på sidan"); btn.setAttribute("aria-haspopup", "dialog"); btn.setAttribute("aria-keyshortcuts", mac ? "Meta+K /" : "Control+K /");
  btn.innerHTML = `${icon}<span>Sök</span>`;
  const navIn = document.querySelector(".nav-in");
  if (!navIn) return;
  navIn.insertBefore(btn, navIn.querySelector(".nav-cta") || navIn.querySelector(".menu-btn"));
  document.documentElement.classList.add("has-sok");

  const dlg = document.createElement("dialog");
  dlg.className = "sok"; dlg.setAttribute("aria-label", "Sök på sabimedia.se");
  dlg.innerHTML = `<div class="sok-panel">
    <div class="sok-field">${icon}
      <label for="sok-q" class="sok-sr" style="position:absolute;left:-9999px">Sök</label>
      <input id="sok-q" type="search" placeholder="Sök efter pris, bransch, fråga …" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="false" aria-controls="sok-list" aria-autocomplete="list">
      <button class="sok-close" type="button">Stäng</button>
    </div>
    <div class="sok-body"><p class="sok-head" id="sok-head"></p><ul class="sok-list" id="sok-list" role="listbox" aria-labelledby="sok-head"></ul><div class="sok-empty" id="sok-empty" hidden></div></div>
    <p id="sok-status" role="status" style="position:absolute;left:-9999px"></p>
  </div>`;
  document.body.append(dlg);
  const q = dlg.querySelector("#sok-q"), list = dlg.querySelector("#sok-list"), head = dlg.querySelector("#sok-head"),
    empty = dlg.querySelector("#sok-empty"), panel = dlg.querySelector(".sok-panel"), status = dlg.querySelector("#sok-status");
  let results = [], active = 0;

  function render() {
    const v = q.value.trim();
    results = v ? search(v) : []; active = 0;
    panel.classList.toggle("has-q", !!v); q.setAttribute("aria-expanded", String(!!v));
    head.textContent = v ? (results.length ? `${results.length} träff${results.length === 1 ? "" : "ar"}` : "") : "";
    empty.hidden = !!results.length || !v;
    empty.innerHTML = `Inga träffar för ”${esc(v)}”. Prova ett annat ord eller <a href="/#kontakt">fråga oss direkt</a>.`;
    list.innerHTML = results.map((r, i) => `<li role="option" id="sok-o${i}" aria-selected="${i === 0}"><a href="${r.u}" tabindex="-1"><b>${mark(r.t, v)}</b><em>${esc(r.p)}</em><small>${mark(r.d, v)}</small></a></li>`).join("");
    q.setAttribute("aria-activedescendant", results.length ? "sok-o0" : "");
    status.textContent = v ? (results.length ? `${results.length} träffar` : "Inga träffar") : "";
  }
  function move(d) {
    if (!results.length) return;
    list.children[active]?.setAttribute("aria-selected", "false");
    active = (active + d + results.length) % results.length;
    const li = list.children[active]; li.setAttribute("aria-selected", "true");
    q.setAttribute("aria-activedescendant", li.id); li.scrollIntoView({ block: "nearest" });
  }
  function go(url) {
    dlg.close();
    const u = new URL(url, location.href);
    if (u.pathname === location.pathname && u.hash) { history.pushState(null, "", u.hash); openTarget(); }
    else location.href = url;
  }
  function open() {
    document.getElementById("nav-links")?.classList.remove("open");
    document.getElementById("menu-btn")?.setAttribute("aria-expanded", "false");
    q.value = ""; render(); dlg.showModal(); q.focus();
  }
  btn.addEventListener("click", open);
  dlg.querySelector(".sok-close").addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener("close", () => btn.focus());
  q.addEventListener("input", render);
  q.addEventListener("keydown", e => {
    if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
    else if (e.key === "Enter" && results[active]) { e.preventDefault(); go(results[active].u); }
  });
  list.addEventListener("click", e => { const a = e.target.closest("a"); if (a) { e.preventDefault(); go(a.getAttribute("href")); } });
  document.addEventListener("keydown", e => {
    const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing)) {
      e.preventDefault(); dlg.open ? dlg.close() : open();
    }
  });

  // Öppnar en vanlig fråga när man kommer till den från sökningen (t.ex. /#faq-3) och scrollar dit
  function openTarget() {
    const el = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!el) return;
    if (el.tagName === "DETAILS") el.open = true;
    el.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  }
  window.addEventListener("hashchange", openTarget);
  if (/^#faq-/.test(location.hash)) setTimeout(openTarget, 50);
})();
