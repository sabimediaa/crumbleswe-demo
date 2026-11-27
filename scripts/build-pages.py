"""Skapar undersidorna Tjänster, Priser, FAQ och Kontakt samt 404-sidan från startsidan (site/index.html),
och ger alla fristående sidor samma sidfot som startsidan. Körs av build-site.sh. Innehållet ändras alltså bara i sabimedia.html – sidorna följer med."""
import datetime, html as H, json, re

src = open("site/index.html", encoding="utf-8").read()

def one(text, old, new):
    if text.count(old) != 1:
        raise SystemExit(f"build-pages: hittade {text.count(old)} av: {old[:80]}")
    return text.replace(old, new)

def section(sid):
    m = re.search(r'  <section class="section[^"]*" id="%s".*?\n  </section>\n' % sid, src, re.S)
    if not m: raise SystemExit("build-pages: sektionen saknas: " + sid)
    return m.group(0)

def next_step(h, p, btns):
    links = "".join(f'<a class="btn {c}" href="{u}">{t}</a>' for c, u, t in btns)
    return f'''  <section class="section next-step" style="padding-top:0">
    <div class="wrap"><div class="next-box"><div><h2>{h}</h2><p>{p}</p></div><div class="next-btns">{links}</div></div></div>
  </section>
'''

def cookie_munch():
    """Exemplet och omdömet från startsidan, samlade i en egen sektion."""
    stage = re.search(r'        <div class="stage">.*?\n        </div>\n', src, re.S)
    review = re.search(r'        <figure class="review".*?</figure>\n', src, re.S)
    if not stage or not review: raise SystemExit("build-pages: Cookie Munch-exemplet saknas")
    review = re.sub(r'\s*<a class="review-link".*?</a>', "", review.group(0))
    return f'''  <section class="section" id="cookie-munch" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Exempel</span>
        <h2>Så blev det för <em class="hl">Cookie Munch.</em></h2>
        <p class="lead">En webbshop vi har byggt åt ett bageri i Borås, med betalning och en egen adminsida.</p>
      </div>
      <div class="case-grid">
{stage.group(0).replace("<img ", '<img loading="lazy" ')}{review}      </div>
      <div class="case-btns"><a class="btn btn-accent" href="/kundcase-cookie-munch">Läs hela kundcaset →</a><a class="btn btn-line" href="https://cookiemunch.se" target="_blank" rel="noopener">Besök cookiemunch.se ↗</a></div>
    </div>
  </section>
'''

WEBBDESIGN = '''  <section class="section" id="webbdesign" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Webbdesign och webbutveckling</span>
        <h2>Webbdesign för företag, <em class="hl">från början till slut.</em></h2>
        <p class="lead">Att skapa hemsida för företag på egen hand tar tid. Vi tar hand om både hur den ser ut och hur den fungerar, så att du kan fokusera på dina kunder.</p>
      </div>
      <div class="own">
        <div class="own-card"><h3>Webbdesign</h3><p>Som webbdesignbyrå formar vi hemsidan efter ditt varumärke, med dina färger, din logga och dina bilder. Den ska vara lätt att förstå och se bra ut i mobil, surfplatta och dator.</p></div>
        <div class="own-card"><h3>Webbutveckling</h3><p>Vi bygger funktionerna du behöver, till exempel formulär, bokningar, beställningar och betalning. Vad som ingår beror på vilket paket du väljer.</p></div>
        <div class="own-card"><h3>Bygga hemsida utan krångel</h3><p>Du berättar vad du behöver och skickar ditt material. Vi bygger, du säger vad du tycker, och inget publiceras innan du är nöjd.</p></div>
        <div class="own-card"><h3>Ta emot beställningar online</h3><p>Med Business får du en hemsida med beställningsformulär, och alla onlinebeställningar kommer direkt till din mejl.</p></div>
        <div class="own-card"><h3>Skapa företagshemsida</h3><p>Har du ingen egen hemsida än? Vi börjar med ett möte om dina behov, din målgrupp och din stil. Sedan får du ett första utkast att tycka till om. <a href="/branscher">Se exempel för din bransch</a>.</p></div>
        <div class="own-card"><h3>Förbättra hemsida</h3><p>Känns din hemsida gammal, eller hör för få kunder av sig? <a href="/kontakt">Skicka länken till oss</a> så föreslår vi vad som kan bli bättre, eller om det är dags för en ny hemsida.</p></div>
        <div class="own-card"><h3>Öppna webbutik</h3><p>Vill du ha en hemsida med produkter som kunden kan köpa direkt? Med Pro bygger vi en webbutik med varukorg, betalning och en egen adminpanel.</p></div>
        <div class="own-card"><h3>Ta emot bokningar online</h3><p>Låt kunden skicka en bokningsförfrågan på hemsidan. Med Pro kan du få ett bokningssystem med kalender och lediga tider.</p></div>
      </div>
    </div>
  </section>
'''

BYGG = '''  <section class="section band" id="anpassa">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Anpassa ditt paket</span>
        <h2>Ta bort det <em class="hl">du redan har.</em></h2>
        <p class="lead">Priset här är detsamma som på paketet. Har du redan domän eller logga kryssar du ur det, så blir priset lägre. Vill du ha uppdateringsavtal lägger du till det. Det här är en uppskattning, inget beställs förrän du har godkänt ett fast pris.</p>
      </div>
      <form class="calc" id="anpassa-form" aria-describedby="anpassa-result">
        <div>
          <fieldset>
            <legend>1. Välj paket</legend>
            <div class="calc-plans">
              <label class="calc-opt"><input type="radio" name="paket" value="Start" data-price="1500" data-avtal="700"><span><b>Start</b><small>1 500 kr</small></span></label>
              <label class="calc-opt"><input type="radio" name="paket" value="Business" data-price="2800" data-avtal="1300" checked><span><b>Business</b><small>2 800 kr</small></span></label>
              <label class="calc-opt"><input type="radio" name="paket" value="Pro" data-price="4300" data-avtal="2100"><span><b>Pro</b><small>från 4 300 kr</small></span></label>
            </div>
          </fieldset>
          <fieldset style="margin-top:18px">
            <legend>2. Ingår i paketet, kryssa ur det du redan har</legend>
            <label class="calc-opt"><input type="checkbox" name="ingar" value="domän" data-price="250" data-label="Hjälp med domän, webbhotell och e-post" checked><span><b>Hjälp med domän, webbhotell och e-post</b><small>Har du redan en adress och e-post? Kryssa ur.</small></span><span class="calc-cost">−250 kr</span></label>
            <label class="calc-opt"><input type="checkbox" name="ingar" value="logotyp" data-price="300" data-label="Logotyp och företagsfärger" checked><span><b>Enklare logotyp och företagsfärger</b><small>Har du redan en logga? Kryssa ur.</small></span><span class="calc-cost">−300 kr</span></label>
          </fieldset>
          <fieldset style="margin-top:18px">
            <legend>3. Lägg till om du vill</legend>
            <label class="calc-opt"><input type="checkbox" name="tillagg" value="avtal" data-label="Uppdateringsavtal, per år"><span><b>Uppdateringsavtal</b><small>Underhåll och 4 mindre ändringar per år, och timpris 200 kr i stället för 400 kr. Faktureras årsvis.</small></span><span class="calc-cost" id="avtal-cost">+1 300 kr/år</span></label>
          </fieldset>
        </div>
        <div class="calc-result" id="anpassa-result" aria-live="polite">
          <span class="plan-kicker">Ditt paket</span>
          <ul class="calc-lines" id="anpassa-lines"></ul>
          <p class="calc-price"><strong id="anpassa-total">2 800 kr</strong><span id="anpassa-terms">Engångskostnad · exkl. moms</span></p>
          <p class="calc-note">Domän och webbhotell betalar du löpande direkt till leverantören. Ingen månadsavgift till oss.</p>
          <div class="calc-btns"><a class="btn btn-accent" id="anpassa-go" href="/kontakt?paket=Business">Skicka förfrågan med detta</a><a class="btn btn-line" href="/boka">Boka samtal</a></div>
        </div>
      </form>
      <script>
      (() => {
        const form = document.getElementById("anpassa-form"), $ = id => document.getElementById(id);
        const kr = n => n.toLocaleString("sv-SE").replace(/\u00a0/g, " ").replace("-", "−") + " kr";
        const esc = s => s.replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
        const update = () => {
          const plan = form.querySelector("input[name=paket]:checked");
          const avtal = +plan.dataset.avtal;
          $("avtal-cost").textContent = "+" + kr(avtal) + "/år";
          let total = +plan.dataset.price;
          const lines = [[plan.value + " (domän och logotyp ingår)", kr(total), true]], utan = [];
          form.querySelectorAll("input[name=ingar]:not(:checked)").forEach(i => {
            total -= +i.dataset.price; utan.push(i.value);
            lines.push(["Utan " + i.dataset.label.toLowerCase(), kr(-i.dataset.price), true]);
          });
          const medAvtal = form.querySelector("input[value=avtal]").checked;
          if (medAvtal) { total += avtal; lines.push(["Uppdateringsavtal, första året", "+" + kr(avtal), true]); }
          $("anpassa-lines").innerHTML = lines.map(([l, p]) => `<li><span>${esc(l)}</span><span>${p}</span></li>`).join("");
          $("anpassa-total").textContent = (plan.value === "Pro" ? "Från " : "") + kr(total);
          $("anpassa-terms").textContent = medAvtal ? "Totalt första året · exkl. moms" : "Engångskostnad · exkl. moms";
          const q = new URLSearchParams({ paket: plan.value });
          if (utan.length) q.set("utan", utan.join(","));
          if (medAvtal) q.set("tillagg", "avtal");
          $("anpassa-go").href = "/kontakt?" + q.toString();
        };
        form.addEventListener("change", update);
        form.addEventListener("submit", e => e.preventDefault());
        update();
      })();
      </script>
    </div>
  </section>
'''

PRISFRAGOR = '''  <section class="section" id="vad-kostar" style="padding-top:0">
    <div class="wrap faq-grid">
      <div class="section-head" style="margin:0">
        <span class="eyebrow">Webbyrå · Priser</span>
        <h2>Vad kostar en hemsida <em class="hl">till företag?</em></h2>
        <p class="lead">Vi är en webbyrå med fast pris. Hos oss kostar en hemsida från 1&nbsp;500&nbsp;kr med Start, från 2&nbsp;800&nbsp;kr med Business och från 4&nbsp;300&nbsp;kr med Pro. Priset är en engångskostnad exklusive moms.</p>
      </div>
      <div class="faq">
        <details open><summary>Får jag en hemsida till fast pris?</summary><p>Ja. Priserna ovan är från-priser, men innan vi börjar får du ett fast pris att godkänna. Då vet du vad din hemsida kostar.</p></details>
        <details><summary>Hur många sidor ingår?</summary><p>Start har upp till 4 sidor och Business upp till 12. Varje extra sida kostar 200 kr exkl. moms. I Pro bestäms antalet i offerten.</p></details>
        <details><summary>Vad betyder Google-anpassning i paketen?</summary><p>Det är grundläggande SEO, alltså hur hemsidan är byggd: tydliga rubriker och titlar, snabb i mobilen och lätt att använda, så att den både hittas och leder till köp. Det ingår i alla paket. <a href="/synas-pa-google">Läs mer om att synas på Google</a>.</p></details>
        <details><summary>Kan jag köpa en hemsida utan abonnemang?</summary><p>Ja, hos oss får du en hemsida utan abonnemang. Du betalar en gång, och sedan är hemsidan din. Vi tar ingen månadsavgift.</p></details>
        <details><summary>Vilken kostnad har en hemsida efter lansering?</summary><p>Räkna med avgifter för domän och webbhotell, som du betalar till den leverantör du väljer. När supporttiden är slut kostar vår hjälp 400 kr i timmen exkl. moms (200 kr med uppdateringsavtal).</p></details>
        <details><summary>Är en billig hemsida för småföretag bra nog?</summary><p>Det kan den vara. Med Start får du en billig hemsida med egen design, mobilanpassning och kontaktformulär. Vill du ha en hemsida billigt till att börja med kan du lägga till funktioner senare mot offert.</p></details>
        <details><summary>Hemsida för småföretag: vilket pris och paket passar?</summary><p>Start räcker långt om du vill synas och bli kontaktad. Business passar dig som tar emot förfrågningar, bokningar eller beställningar. Pro är för dig som behöver till exempel webbshop eller bokningssystem. Alla våra paket för en ny hemsida är gjorda för småföretag, och du ser priset innan du bestämmer dig.</p></details>
        <details><summary>Hur jämför jag priser hos olika webbyråer?</summary><p>När du jämför pris på hemsida bör du titta på vad som ingår, om det tillkommer månadsavgifter och vem som äger hemsidan. Jämför också med hemsidebyggare, som ofta tar en avgift varje månad. <a href="#jamfor">Här ser du vad som ingår hos oss.</a></p></details>
        <details><summary>Måste jag begära offert?</summary><p>Nej, inte för Start och Business. Där gäller paketpriset, och innan vi börjar får du ett fast pris att godkänna. Offert behövs bara för Pro och för tillägg som inte ingår i något paket. Den kostar inget.</p></details>
        <details><summary>Hur räknar jag ut vad hemsidan kostar totalt?</summary><p>Lägg ihop priset för hemsidan med domän och webbhotell under några år, och eventuella månadsavgifter. <a href="/vad-kostar-en-hemsida">Så räknar du ut totalkostnaden</a> eller läs om <a href="/hemsida-utan-manadskostnad">hemsida utan månadskostnad</a>.</p></details>
      </div>
    </div>
  </section>
  <section class="section band" id="ingar-inte">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Ärligt</span>
        <h2>Det här <em class="hl">ingår inte.</em></h2>
        <p class="lead">Ett lågt pris ska gå att lita på. Därför säger vi rakt ut vad varje paket inte innehåller. Behöver du det, finns det i nästa paket eller som tillägg till fast pris.</p>
      </div>
      <div class="own">
        <div class="own-card"><span class="tag-name tag-no">Start</span><h3>Ingår inte i Start</h3><p>Fler än 4 sidor, formulär för bokning, offert eller beställning, kundomdömen, betalning och adminpanel. Support i 1 månad.</p></div>
        <div class="own-card"><span class="tag-name tag-no">Business</span><h3>Ingår inte i Business</h3><p>Bokningssystem med kalender, betalning på sidan, webbshop, kundkonton och adminpanel. Support i 2 månader.</p></div>
        <div class="own-card"><span class="tag-name tag-no">Pro</span><h3>Bestäms i offerten</h3><p>Integrationer med andra system och specialfunktioner prissätts efter vad du behöver. Du godkänner priset innan vi börjar.</p></div>
      </div>
      <div class="link-row"><a class="btn btn-ink" href="/priskalkylator">Räkna ut ditt paket →</a></div>
    </div>
  </section>
  <section class="section" id="tillagg">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Efter lanseringen</span>
        <h2>Tillägg, avtal <em class="hl">och timpris.</em></h2>
        <p class="lead">Allt här är frivilligt. Du betalar bara för det du väljer, och alla priser är exklusive moms.</p>
      </div>
      <div class="own">
        <div class="own-card"><span class="tag-name">Frivilligt</span><h3>Uppdateringsavtal</h3><p>Underhåll av hemsidan och temat, plus mindre ändringar 4 gånger per år. Faktureras årsvis.</p><p class="answer-line">Start 700 kr · Business 1 300 kr · Pro 2 100 kr per år</p></div>
        <div class="own-card"><span class="tag-name">Ingår</span><h3>Domän och logotyp</h3><p>Hjälp med domän, webbhotell och e-post och en enklare logotyp med företagsfärger ingår i alla paket. Har du redan det dras 250 kr respektive 300 kr av. <a href="#anpassa">Anpassa ditt paket</a></p></div>
        <div class="own-card"><span class="tag-name">Vid behov</span><h3>Timpris</h3><p>När supportperioden är slut hjälper vi dig per timme.</p><p class="answer-line">400 kr i timmen, 200 kr med uppdateringsavtal</p></div>
      </div>
      <div class="change-note" style="margin-top:18px">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg></div>
        <div><h3>Bra att veta</h3><p>Hemsidan blir din när den är betald i sin helhet. Du ansvarar för innehållet, alltså text och bilder, men vi kan ta fram textutkast som du går igenom och godkänner.</p></div>
      </div>
    </div>
  </section>
  <section class="section band" id="hemsidebyggare">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Jämför</span>
        <h2>Hemsidebyggare <em class="hl">eller Sabi?</em></h2>
        <p class="lead">Med en hemsidebyggare bygger du sidan själv och betalar oftast en avgift varje månad så länge den ligger uppe. Hos oss betalar du en gång, och du har riktiga människor vid din sida hela vägen.</p>
      </div>
      <div class="plans two">
        <article class="plan">
          <div class="plan-head"><span class="plan-kicker">Gör det själv</span><h3>Hemsidebyggare</h3><p>Färdiga mallar som du fyller i på egen hand.</p></div>
          <ul><li>Oftast en avgift varje månad</li><li>Du bygger och skriver allt själv</li><li>Support via chatt eller hjälpartiklar</li><li>Samma mallar som många andra använder</li></ul>
        </article>
        <article class="plan featured">
          <span class="pill">Sabi</span>
          <div class="plan-head"><span class="plan-kicker">Vi bygger åt dig</span><h3>Sabimedia</h3><p>En hemsida formad efter ditt företag, från 1&nbsp;500&nbsp;kr.</p></div>
          <ul><li>Fast engångspris, ingen månadsavgift till oss</li><li>Du pratar med Safiya och Warda, inte med en bot</li><li>Vi bygger ditt varumärke tillsammans: dina färger, din logga, dina bilder</li><li>Du äger hemsidan, domänen och webbhotellet</li></ul>
          <a class="btn btn-accent" href="/boka">Boka ett kostnadsfritt samtal</a>
        </article>
      </div>
      <div class="link-row"><a class="btn btn-ink" href="/hemsida-utan-manadskostnad">Räkna på tre år →</a><a class="btn btn-line" href="/om-oss">Möt teamet</a></div>
    </div>
  </section>
'''

TJANSTFRAGOR = '''  <section class="section band" id="tjanst-fragor">
    <div class="wrap faq-grid">
      <div class="section-head" style="margin:0">
        <span class="eyebrow">Vanliga frågor</span>
        <h2>Frågor om <em class="hl">hur vi arbetar.</em></h2>
        <div><a class="btn btn-ink" href="/faq">Alla frågor →</a></div>
      </div>
      <div class="faq">
        <details open><summary>Hur lång tid tar det?</summary><p>Första utkastet får du inom 24 timmar. Hela hemsidan tar från några dagar upp till några veckor, beroende på paket och funktioner. Tiden räknas från att vi fått ditt material.</p></details>
        <details><summary>Vad behöver jag skicka?</summary><p>Logga, bilder, produkter eller tjänster och priser. <a href="/checklista-ny-hemsida">Se checklistan</a>.</p></details>
        <details><summary>Vem äger hemsidan?</summary><p>Du. Domän, webbhotell och hemsida står i ditt namn. <a href="/vem-ager-hemsidan">Så fungerar ägandet</a>.</p></details>
        <details><summary>Ingår SEO?</summary><p>Ja, grundläggande SEO ingår i alla paket. Vi bygger hemsidan rätt från början, så att den både hittas på Google och leder besökaren till att boka eller köpa. Mer omfattande SEO? <a href="/boka">Boka ett möte med Safiya</a>. <a href="/synas-pa-google">Så syns du på Google</a>.</p></details>
        <details><summary>Använder ni AI?</summary><p>Ja, för kod och textutkast. Designen bestämmer vi tillsammans med dig, och vi granskar allt. <a href="/sa-anvander-vi-ai">Så använder vi AI</a>.</p></details>
        <details><summary>Vad kostar hjälp efter lanseringen?</summary><p>400 kr i timmen exkl. moms (200 kr med uppdateringsavtal) när supportperioden är slut. Ingen månadsavgift.</p></details>
      </div>
    </div>
  </section>
'''

PAGES = {
    "tjanster": dict(
        menu="Tjänster", title="Skapa hemsida för företag – webbdesign · Sabimedia",
        desc="Vill du skapa hemsida för företag? Vi jobbar med webbdesign och webbutveckling och bygger funktioner som förenklar vardagen. Se vad som ingår.",
        eyebrow="Tjänster", h1='Webbdesign och hemsidor <em class="hl">för småföretag.</em>', parts=["ingar", "sa-funkar-det", "agande"],
        after=TJANSTFRAGOR + next_step("Vad kostar det?", "Tre paket med fast pris. Jämför dem eller fråga oss vad som passar dig.",
                        [("btn-accent", "/priser", "Se priserna →"), ("btn-line", "/kontakt", "Kontakta oss")])),
    "priser": dict(
        menu="Priser", title="Billig hemsida till fast pris – priser och paket · Sabimedia",
        desc="Billig hemsida från 1 500 kr exkl. moms. Se vad en hemsida kostar och jämför tre paket med fast engångspris, utan månadsavgift till Sabimedia.",
        eyebrow="Priser", h1='Billig hemsida <em class="hl">till fast pris.</em>', parts=["priser"],
        after=next_step("Osäker på vilket paket som passar?", "Boka ett kostnadsfritt samtal så går vi igenom vad du behöver.",
                        [("btn-accent", "/boka", "Boka samtal →"), ("btn-line", "/faq", "Vanliga frågor")])),
    "faq": dict(
        menu="FAQ", title="Vanliga frågor om hemsidor · Sabimedia",
        desc="Svar på vanliga frågor om pris, tid, ägande, publicering och support när Sabimedia bygger din hemsida.",
        eyebrow="FAQ", h1='Vanliga frågor <em class="hl">om hemsidor.</em>', parts=["fragor"], after=""),
    "kontakt": dict(
        menu="Kontakt", title="Kontakt – skicka en förfrågan · Sabimedia",
        desc="Berätta om ditt företag och välj en tid för ett kostnadsfritt samtal. Sabimedia svarar inom 24 timmar.",
        eyebrow="Kontakt", h1=None, parts=["kontakt"], after=""),
}

CSS = """/* Undersidor skapade av scripts/build-pages.py */
.section-head h1{font-size:clamp(2.2rem,5vw,3.8rem)}
.contact h1{font-size:clamp(2rem,4.4vw,3.2rem);margin:.8rem 0 1rem}
.band + .section{padding-top:clamp(64px,9vw,120px)!important}
.head-btns{margin-top:.6rem}
.case-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,4vw,56px);align-items:center}
.case-grid .stage{min-height:0}
.case-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(24px,3vw,36px)}
#cookie-munch{scroll-margin-top:60px}
.plan[id^="paket-"]{scroll-margin-top:110px}
#hemsidebyggare .plans{margin-bottom:0}
.calc{display:grid;grid-template-columns:1.3fr 1fr;gap:clamp(20px,3vw,36px);align-items:start}
.calc fieldset{border:0;margin:0;padding:0;display:grid;gap:10px;min-width:0}
.calc legend{font-family:var(--display);font-weight:700;font-size:1.25rem;margin-bottom:6px}
.calc-opt{display:flex;gap:14px;align-items:flex-start;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px 18px;cursor:pointer;transition:border-color .2s}
.calc-opt:hover,.calc-opt:has(input:checked){border-color:var(--accent)}
.calc-opt input{width:20px;height:20px;margin-top:2px;accent-color:var(--accent);flex:none}
.calc-opt span{display:grid;gap:2px}
.calc-opt small{color:var(--ink-soft);font-size:.92rem}
.calc-result{position:sticky;top:100px;background:var(--paper);border:2px solid var(--accent);border-radius:var(--radius);padding:26px;display:grid;gap:.8rem;box-shadow:0 30px 60px -34px rgba(15,15,20,.25)}
.calc-result h2{font-size:2rem}
.calc-price{display:grid;gap:.15rem;margin:0}
.calc-price strong{font-family:var(--display);font-size:2.4rem;line-height:1.05;color:var(--accent);letter-spacing:-.04em}
.calc-price span,.calc-note{font-size:.88rem;color:var(--ink-soft)}
.calc-btns{display:flex;flex-wrap:wrap;gap:10px}
@media (max-width:900px){.calc{grid-template-columns:minmax(0,1fr)}.calc-result{position:static}}
.calc-opt .calc-cost{margin-left:auto;font-weight:700;white-space:nowrap;padding-left:12px}
.calc>*{min-width:0}
.calc-opt>span:not(.calc-cost){min-width:0;flex:1}
.calc-opt .calc-cost{flex:none}
@media (max-width:480px){.calc-opt:has(.calc-cost){flex-wrap:wrap}.calc-opt .calc-cost{padding-left:34px;margin-left:0;width:100%}}
.calc-opt:has(input[name=ingar]:not(:checked)) .calc-cost{color:var(--ink-soft);text-decoration:line-through}
.calc-plans{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:8px}
.calc-plans .calc-opt{flex-direction:column;gap:6px}
.calc-plans .calc-opt input{position:absolute;opacity:0}
.calc-plans .calc-opt{position:relative}
.calc-plans .calc-opt:has(input:focus-visible){outline:3px solid var(--accent);outline-offset:2px}
.calc-plans .calc-opt:has(input:checked){background:var(--plum);color:#fff;border-color:var(--plum)}
.calc-plans .calc-opt:has(input:checked) small{color:#d9cfdc}
.calc-lines{list-style:none;margin:0;padding:0;display:grid;gap:.35rem;font-size:.95rem}
.calc-lines li{display:flex;justify-content:space-between;gap:12px}
.calc-lines li.off{color:var(--ink-soft);text-decoration:line-through}
.calc-lines li span:last-child{white-space:nowrap}
.calc-save{background:var(--accent-soft);color:var(--accent-deep);border-radius:10px;padding:8px 12px;font-weight:600;margin:0}
@media (max-width:560px){.calc-plans{grid-template-columns:1fr}}
.own-card .answer-line{color:var(--ink);font-weight:600;padding-top:.6rem;border-top:1px solid var(--line);margin-top:.2rem}
.own-card .tag-name.tag-no::before{content:"!";background:var(--accent)}
.plans.two{grid-template-columns:repeat(2,1fr);max-width:820px}
@media (max-width:900px){.plans.two{grid-template-columns:1fr}}
.link-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(24px,3vw,36px)}
.link-row .btn{white-space:normal;text-align:center;max-width:100%}
#webbdesign .own{grid-template-columns:repeat(4,1fr)}
@media (max-width:1100px){#webbdesign .own{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){#webbdesign .own{grid-template-columns:1fr}}
@media (max-width:900px){.case-grid{grid-template-columns:minmax(0,1fr)}}
.only-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.page-first{padding-top:clamp(40px,6vw,72px)!important}
.next-box{display:grid;grid-template-columns:1.4fr auto;gap:24px;align-items:center;background:var(--plum);color:#fff;border-radius:24px;padding:clamp(28px,5vw,56px)}
.next-box h2{font-size:clamp(1.8rem,3.6vw,2.6rem)}
.next-box p{color:#cfc4d4;margin-top:.6rem;max-width:52ch}
.next-btns{display:flex;flex-wrap:wrap;gap:10px}
.next-btns .btn-line{background:transparent;color:#fff;border:0;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.45)}
.next-btns .btn-line:hover{box-shadow:inset 0 0 0 1.5px #fff}
@media (max-width:760px){.next-box{grid-template-columns:1fr}}
</style>
</head>"""

# Jämförelsetabellen finns bara på /priser, knappen dit bara på startsidan
def only(text, keep):
    for tag in ("bara-hem", "bara-priser"):
        text, n = re.subn(r"[ \t]*<!-- %s\b.*?-->\n(.*?)[ \t]*<!-- /%s -->\n" % (tag, tag), (lambda m: m[1]) if tag == keep else "", text, flags=re.S)
        if n > 1: raise SystemExit("build-pages: dubbla märken " + tag)
    return text

main0, main1 = src.index('<main id="top"'), src.index("</main>")

for name, p in PAGES.items():
    url = f"https://sabimedia.se/{name}"
    body = only("".join(section(s) for s in p["parts"]), "bara-priser")
    if name == "tjanster":  # knapp under ingressen och exemplet direkt efter det som ingår
        body = re.sub(r'(<p class="lead">.*?</p>\n)', lambda m: m[1] + '        <div class="head-btns"><a class="btn btn-ink" href="#cookie-munch">Se exempel: Cookie Munch ↓</a></div>\n', body, count=1, flags=re.S)
        cut = body.index("</section>\n") + len("</section>\n")
        body = body[:cut] + cookie_munch() + WEBBDESIGN + body[cut:]
        body = one(body, "Vi jobbar med webbdesign i Borås och i hela Sverige. Varje hemsida är byggd för små företag som", "Vi bygger hemsidor med funktioner som förenklar företagets vardag. Vårt jobb är webbdesign och webbutveckling för små företag som")
        body = one(body, "ett proffsigare sätt att ta emot beställningar.", "ett proffsigare sätt att ta emot beställningar online.")
    if name == "priser":
        body = one(body, "Vill du köpa hemsida till ditt företag? Sabi media är en webbyrå med fast pris och tydligt innehåll. Prisvärt, men aldrig slarvigt: innan något publiceras testar vi varje sida i mobil och dator, provar formulär och länkar och korrekturläser texterna. Välj den hemsida som passar din budget och hur ditt företag tar emot kunder.", "Att köpa hemsida ska vara enkelt. Alla våra paket börjar under 5 000 kr, och du betalar en gång, utan abonnemang och utan månadsavgift till Sabimedia. Prisvärt, men aldrig slarvigt: innan något publiceras testar vi varje sida i mobil och dator, provar formulär och länkar och korrekturläser texterna. Välj det paket som passar din budget och hur ditt företag tar emot kunder.") + PRISFRAGOR
    body = re.sub(r'<section class="section([^"]*)" id="([^"]+)"( style="padding-top:0")?', r'<section class="section\1 page-first" id="\2"', body, count=1)
    body = re.sub(r'<span class="eyebrow">[^<]*</span>', f'<span class="eyebrow">{p["eyebrow"]}</span>', body, count=1)
    body = re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h1>{p["h1"] or m[1]}</h1>', body, count=1, flags=re.S)
    # Osynlig mellanrubrik så att rubriknivåerna följer varandra (h1, h2, h3)
    for before, text in (('<div class="features">', "Det här ingår"), ('<div class="plans" id="plans">', "Paketen")):
        body = body.replace(before, f'<h2 class="only-sr">{text}</h2>\n      {before}', 1)
    if name == "priser":  # "Ta bort det du redan har" direkt under paketkorten
        body = one(body, '  <section class="section" id="vad-kostar" style="padding-top:0">',
                   BYGG + '  <section class="section" id="vad-kostar">')
    page = src[:main0] + '<main id="top" tabindex="-1">\n' + body + p["after"] + src[main1:]

    page = re.sub(r"<title>.*?</title>", f'<title>{p["title"]}</title>', page, count=1)
    page = one(page, '<link rel="canonical" href="https://sabimedia.se/">', f'<link rel="canonical" href="{url}">')
    page = one(page, '<meta property="og:url" content="https://sabimedia.se/">', f'<meta property="og:url" content="{url}">')
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m[1] + p["desc"], page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m[1] + p["desc"], page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m[1] + p["title"], page, count=1)
    data = {"@context": "https://schema.org", "@type": "ContactPage" if name == "kontakt" else "WebPage", "name": p["title"].split(" · ")[0], "url": url, "about": {"@id": "https://sabimedia.se/#foretag"}}
    if name == "faq":
        qa = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body, re.S)
        data.update({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": H.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub("<[^>]+>", "", a))}} for q, a in qa]})
    blocks = [data]
    qa = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body + p["after"], re.S)
    if qa and name != "faq":  # frågorna sist på sidan får eget FAQ-schema
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": H.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub("<[^>]+>", "", a))}} for q, a in qa]})
    page, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: "\n".join('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>" for d in blocks), page, flags=re.S)
    if n != 1: raise SystemExit("build-pages: JSON-LD")

    page = one(page, '<li><a href="/" aria-current="page">Hem</a></li>', '<li><a href="/">Hem</a></li>')
    page, n = re.subn(r'(<li><a (?:class="[^"]*" )?href="/%s")' % name, r'\1 aria-current="page"', page, count=1)
    if n != 1: raise SystemExit("build-pages: menyn saknar /" + name)
    page = one(page, "</style>\n</head>", CSS)
    page = re.sub(r'href="#(ingar|priser|fragor|kontakt)"', lambda m: 'href="/%s"' % {"ingar": "tjanster", "priser": "priser", "fragor": "faq", "kontakt": "kontakt"}[m[1]], page)
    if 'class="hl"' not in body:
        page = re.sub(r'<link rel="preload" href="typsnitt/fraunces[^\n]*\n', "", page)
    open(f"site/{name}.html", "w", encoding="utf-8").write(page)

open("site/index.html", "w", encoding="utf-8").write(only(src, "bara-hem"))

# Sidfoten på de fristående sidorna byts mot startsidans, så att länkarna är lika överallt
footer = re.search(r"\n<footer>\n.*?\n</footer>\n", src, re.S)
if not footer: raise SystemExit("build-pages: sidfoten saknas")
footer = one(footer[0], '<span id="year"></span>', str(datetime.date.today().year))
foot_css = "\n".join(re.findall(r"^(?:\.foot[ {][^\n]*|\.brand-foot [^\n]*|\.legal\{[^\n]*)", src, re.M))
FOOT_CSS = "/* Sidfot från startsidan (scripts/build-pages.py) */\nfooter{border-top:0;padding:56px 0 calc(40px + env(safe-area-inset-bottom,0px));font-size:1rem}\nfooter a{color:var(--ink-soft)}\n" + foot_css + "\n.legal{margin:0}\n.foot .brand img{height:44px}\n@media (max-width:900px){.foot .brand img{height:28px}}\n</style>\n</head>"
for name in ("integritetspolicy", "om-oss", "branscher", "boka", "kundcase-cookie-munch"):
    with open(f"site/{name}.html", encoding="utf-8") as f: page = f.read()
    page, n = re.subn(r"\n<footer>\n.*?\n</footer>\n", lambda m: footer, page, flags=re.S)
    if n != 1: raise SystemExit("build-pages: sidfot i " + name)
    page = one(page, "</style>\n</head>", FOOT_CSS)
    with open(f"site/{name}.html", "w", encoding="utf-8") as f: f.write(page)

# Guider, bransch- och funktionssidor från mappen sidor/. De byggs med startsidans mall och komponenter.
# Varje fil börjar med en kommentar (title, description, updated) och innehåller sedan sidans sektioner.
SIDOR_CSS = """/* Sidor från sidor/ (scripts/build-pages.py) */
.own.two{grid-template-columns:repeat(2,1fr)}
.own-card .tag-name.tag-no::before{content:"!";background:var(--accent)}
.own-card .tag-num::before{content:none}
.own-card h3 a{color:inherit;text-decoration:none}
.own-card h3 a:hover{color:var(--accent-deep)}
.own-card:has(h3 a){position:relative}
.own-card h3 a::before{content:"";position:absolute;inset:0;border-radius:inherit}
.own-card h3 a::after{content:" →";color:var(--accent)}
.own-card .answer-line{color:var(--ink);font-weight:600;padding-top:.6rem;border-top:1px solid var(--line);margin-top:.2rem}
.sidor .plans{margin-bottom:0}
.plans.two{grid-template-columns:repeat(2,1fr);max-width:820px}
@media (max-width:900px){.plans.two{grid-template-columns:1fr}}
.sidor .change-note{margin-top:0;margin-bottom:0}
.sidor .head-btns{display:flex;flex-wrap:wrap;gap:10px}
.sidor .trust{margin-top:.4rem}
.link-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(24px,3vw,36px)}
.link-row .btn{white-space:normal;text-align:center;max-width:100%}
.case-grid img{display:block;width:100%;height:auto;border-radius:var(--radius);box-shadow:0 30px 60px -28px rgba(15,15,20,.45),0 0 0 1px rgba(15,15,20,.06)}
.case-text{display:grid;gap:1rem;align-content:start}
.case-text p{color:var(--ink-soft)}
@media (max-width:820px){.own.two{grid-template-columns:1fr}}
.calc{display:grid;grid-template-columns:1.3fr 1fr;gap:clamp(20px,3vw,36px);align-items:start}
.calc fieldset{border:0;margin:0;padding:0;display:grid;gap:10px;min-width:0}
.calc legend{font-family:var(--display);font-weight:700;font-size:1.25rem;margin-bottom:6px}
.calc-opt{display:flex;gap:14px;align-items:flex-start;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px 18px;cursor:pointer;transition:border-color .2s}
.calc-opt:hover,.calc-opt:has(input:checked){border-color:var(--accent)}
.calc-opt input{width:20px;height:20px;margin-top:2px;accent-color:var(--accent);flex:none}
.calc-opt span{display:grid;gap:2px}
.calc-opt small{color:var(--ink-soft);font-size:.92rem}
.calc-result{position:sticky;top:100px;background:var(--paper);border:2px solid var(--accent);border-radius:var(--radius);padding:26px;display:grid;gap:.8rem;box-shadow:0 30px 60px -34px rgba(15,15,20,.25)}
.calc-result h2{font-size:2rem}
.calc-price{display:grid;gap:.15rem;margin:0}
.calc-price strong{font-family:var(--display);font-size:2.4rem;line-height:1.05;color:var(--accent);letter-spacing:-.04em}
.calc-price span,.calc-note{font-size:.88rem;color:var(--ink-soft)}
.calc-btns{display:flex;flex-wrap:wrap;gap:10px}
@media (max-width:900px){.calc{grid-template-columns:minmax(0,1fr)}.calc-result{position:static}}
.sidor-note{margin-top:18px;font-size:.92rem;color:var(--ink-soft)}
.check-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.check-list li{position:relative;padding:14px 16px 14px 46px;background:var(--paper);border:1px solid var(--line);border-radius:14px;font-weight:500}
.check-list li::before{content:"";position:absolute;left:14px;top:50%;width:20px;height:20px;margin-top:-10px;border-radius:6px;border:2px solid var(--accent)}
.glossary{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:0}
.glossary div{padding:16px 18px;background:var(--paper);border:1px solid var(--line);border-radius:14px}
.glossary dt{font-family:var(--display);font-weight:700;font-size:1.05rem;margin-bottom:.25rem}
.glossary dd{margin:0;color:var(--ink-soft)}
.check-list li{padding:0}
.check-list li::before{content:none}
.check-list label{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;cursor:pointer;border-radius:14px}
.check-list input{width:20px;height:20px;margin:2px 0 0;flex:none;accent-color:var(--accent)}
.check-list li:has(input:checked){border-color:var(--accent);background:rgba(212,44,51,.05)}
.check-list li:has(input:checked) span{color:var(--ink-soft);text-decoration:line-through;text-decoration-color:rgba(212,44,51,.5)}
.check-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px}
.check-head p{margin:0;font-weight:700;font-family:var(--display);font-size:1.1rem}
.check-btns{display:flex;gap:8px}
.check-bar{height:8px;border-radius:99px;background:var(--line);overflow:hidden;margin-bottom:14px}
.check-bar span{display:block;height:100%;width:0;background:var(--accent);border-radius:99px;transition:width .3s}
.incl{margin-top:22px;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(18px,3vw,28px)}
.incl h3{margin-bottom:12px}
.incl-table{width:100%;border-collapse:collapse;font-size:.97rem}
.incl-table th,.incl-table td{padding:12px 10px;border-bottom:1px solid var(--line);text-align:center}
.incl-table thead th{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft)}
.incl-table th[scope=row],.incl-table thead th:first-child{text-align:left;font-weight:500}
.incl-table tbody tr:last-child th,.incl-table tbody tr:last-child td{border-bottom:0}
.incl-table .yes{color:var(--accent);font-weight:700;font-size:1.1rem}
.incl-table .no{color:var(--ink-soft)}
@media (max-width:760px){.check-list,.glossary{grid-template-columns:1fr}.incl-table{font-size:.88rem}.incl-table th,.incl-table td{padding:10px 6px}}
@media print{.nav,header,footer,.next-step,.sabi-chat,.check-btns{display:none!important}.section:not(#checklista){display:none!important}#checklista{padding:0!important;background:#fff!important}.check-list{grid-template-columns:1fr}}
</style>
</head>"""
import glob, os
for path in sorted(glob.glob("sidor/*.html")):
    slug = os.path.basename(path)[:-5]
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"<!--\n(.*?)\n-->\n", raw, re.S)
    if not m: raise SystemExit("build-pages: rubrikkommentar saknas i " + path)
    meta = dict(line.split(": ", 1) for line in m[1].splitlines())
    body, url, title = raw[m.end():], f"https://sabimedia.se/{slug}", meta["title"]
    h1 = re.sub("<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", body, re.S)[1])
    page = src[:main0] + '<main id="top" class="sidor" tabindex="-1">\n' + body + next_step(meta["cta"], meta["cta_text"],
        [("btn-accent", "/boka", "Boka ett kostnadsfritt samtal"), ("btn-line", "/priser", "Se paketen")]) + src[main1:]
    page = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", page, count=1)
    page = one(page, '<link rel="canonical" href="https://sabimedia.se/">', f'<link rel="canonical" href="{url}">')
    page = one(page, '<meta property="og:url" content="https://sabimedia.se/">', f'<meta property="og:url" content="{url}">')
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda x: x[1] + H.escape(meta["description"]), page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda x: x[1] + H.escape(meta["description"]), page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x[1] + H.escape(title), page, count=1)
    page = one(page, '<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    data = [{"@context": "https://schema.org", "@type": meta.get("type", "Article"), "headline": h1, "url": url, "inLanguage": "sv",
             "description": meta["description"], "dateModified": meta["updated"],
             "author": {"@type": "Organization", "name": "Sabimedia", "@id": "https://sabimedia.se/#foretag"},
             "publisher": {"@id": "https://sabimedia.se/#foretag"}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Startsida", "item": "https://sabimedia.se/"},
                {"@type": "ListItem", "position": 2, "name": h1, "item": url}]}]
    qa = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body, re.S)
    if qa:
        data.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": H.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub("<[^>]+>", "", a))}} for q, a in qa]})
    page, n = re.subn(r'<script type="application/ld\+json">.*?</script>',
                      lambda x: "\n".join('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>" for d in data), page, flags=re.S)
    if n != 1: raise SystemExit("build-pages: JSON-LD i " + slug)
    page = one(page, '<li><a href="/" aria-current="page">Hem</a></li>', '<li><a href="/">Hem</a></li>')
    page = one(page, "</style>\n</head>", CSS.replace("</style>\n</head>", "") + SIDOR_CSS)
    page = re.sub(r'href="#(ingar|priser|fragor|kontakt)"', lambda m: 'href="/%s"' % {"ingar": "tjanster", "priser": "priser", "fragor": "faq", "kontakt": "kontakt"}[m[1]], page)
    open(f"site/{slug}.html", "w", encoding="utf-8").write(page)

# 404-sidan: Firebase Hosting visar site/404.html när en adress saknas
links = "".join(f'<a class="btn {c}" href="{u}">{t}</a>' for c, u, t in
                [("btn-accent", "/", "Till startsidan"), ("btn-line", "/priser", "Se priserna"), ("btn-line", "/kontakt", "Kontakta oss")])
page = src[:main0] + f'''<main id="top" tabindex="-1">
  <section class="section page-first">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">404</span>
        <h1>Sidan <em class="hl">hittades inte.</em></h1>
        <p class="lead">Länken kan vara gammal eller felskriven. Här kommer du vidare.</p>
        <div class="case-btns">{links}</div>
      </div>
    </div>
  </section>
''' + src[main1:]
page = re.sub(r"<title>.*?</title>", "<title>Sidan hittades inte · Sabimedia</title>", page, count=1)
page = one(page, '<link rel="canonical" href="https://sabimedia.se/">\n', '<meta name="robots" content="noindex">\n')
page = re.sub(r'<meta name="description"[^>]*>\n', "", page, count=1)
page = re.sub(r'<meta (?:property="og:|name="twitter:)[^>]*>\n', "", page)
page = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", page, flags=re.S)
page = one(page, '<li><a href="/" aria-current="page">Hem</a></li>', '<li><a href="/">Hem</a></li>')
page = one(page, "</style>\n</head>", CSS)
# Sidan kan visas på vilken adress som helst, därför räknas alla sökvägar från roten
page = re.sub(r"(?<![\w/.-])(bilder|typsnitt)/", r"/\1/", page)
open("site/404.html", "w", encoding="utf-8").write(page)
