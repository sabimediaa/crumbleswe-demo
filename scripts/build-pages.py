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
        <details><summary>Vad betyder Google-anpassning i paketen?</summary><p>Det är grundläggande SEO, alltså hur hemsidan är byggd: tydliga rubriker och titlar, snabb i mobilen och lätt att använda, så att den både hittas och leder till köp. Det ingår i alla paket. <a href="/grundlaggande-seo">Se exakt vad som ingår</a>.</p></details>
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
        <details><summary>Ingår SEO?</summary><p>Ja, grundläggande SEO ingår i alla paket. Vi bygger hemsidan rätt från början, så att den både hittas på Google och leder besökaren till att boka eller köpa. <a href="/grundlaggande-seo">Se exakt vad som ingår</a>. Mer omfattande SEO? <a href="/seo-tjanst">Se vår SEO-tjänst</a>.</p></details>
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
    page, n = re.subn(r'(<li(?: class="[^"]*")?><a (?:class="[^"]*" )?href="/%s")' % name, r'\1 aria-current="page"', page, count=1)
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
.own-card .tag-name.tag-red::before{background:var(--accent)}
.seo-demo{display:grid;grid-template-columns:1.25fr 1fr;gap:clamp(16px,3vw,28px);margin-top:clamp(22px,3vw,32px)}
.demo-col{display:grid;gap:12px;align-content:start}
.demo-label{margin:0;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft)}
.demo-note{margin:0;font-size:.82rem;color:var(--ink-soft)}
.pin{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;font:700 .72rem/1 var(--body);font-style:normal;vertical-align:middle;margin-left:6px;flex:none;box-shadow:0 0 0 3px rgba(212,44,51,.18)}
.demo-key{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.demo-key li{display:flex;gap:10px;align-items:flex-start;font-size:.93rem;color:var(--ink-soft)}
.demo-key .pin{margin:0}
.demo-key b{color:var(--ink)}
.serp{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px 20px;box-shadow:0 24px 50px -34px rgba(15,15,20,.35);font-family:Arial,Helvetica,sans-serif}
.serp-q{display:flex;align-items:center;gap:10px;border:1px solid #dfe1e5;border-radius:99px;padding:8px 14px;font-size:.92rem;color:#202124;margin-bottom:16px}
.serp-g{font-weight:700;color:#4285f4}
.serp-site{display:flex;gap:10px;align-items:center;margin-bottom:6px}
.serp-site b{display:block;font-size:.85rem;color:#202124;font-weight:400}
.serp-site small{display:flex;align-items:center;font-size:.78rem;color:#4d5156}
.serp-fav{display:grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#f1e3c8;color:#8a5a12;font-weight:700;font-size:.8rem}
.serp-title{margin:0 0 4px;font-size:1.15rem;line-height:1.3;color:#1a0dab;display:flex;align-items:center;flex-wrap:wrap}
.serp-desc{margin:0;font-size:.88rem;line-height:1.5;color:#4d5156}
.serp-extra{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px}
.serp-extra span{font-size:.76rem;color:#202124;background:#f1f3f4;border-radius:99px;padding:4px 10px}
.share{position:relative;background:#e9e4dc;border-radius:18px;padding:18px;display:grid;gap:8px;justify-items:end}
.share-bubble{background:#d42c33;color:#fff;border-radius:16px 16px 4px 16px;padding:9px 13px;font-size:.88rem;max-width:85%}
.share-card{width:85%;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 10px 24px -16px rgba(0,0,0,.4)}
.share-img{height:110px;background:linear-gradient(135deg,#f6d38a,#e59a4c 55%,#b8632a);display:grid;place-items:center}
.share-img span{font-family:var(--display);font-weight:700;color:#fff;font-size:1.15rem;text-shadow:0 2px 10px rgba(0,0,0,.25)}
.share-text{display:grid;gap:2px;padding:10px 12px;font-size:.82rem}
.share-text small{color:#6b6b6b;font-size:.72rem}
.share-text b{font-size:.88rem}
.share-text span{color:#555}
.pin-abs{position:absolute;left:10px;top:10px;margin:0}
.phone-demo{display:grid;grid-template-columns:auto 1fr;gap:clamp(18px,4vw,48px);align-items:center;margin-top:clamp(22px,3vw,32px)}
.phone{width:260px;border-radius:34px;background:#fff;border:8px solid #1b1620;box-shadow:0 30px 60px -30px rgba(15,15,20,.5);overflow:hidden;font-size:.82rem}
.phone-top{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;border-bottom:1px solid #eee}
.phone-top b{font-family:var(--display)}
.phone-menu{width:16px;height:2px;background:#1b1620;box-shadow:0 5px 0 #1b1620,0 -5px 0 #1b1620}
.phone-hero{padding:16px 14px;background:#fbf3e4;display:grid;gap:8px}
.phone-hero h4{margin:0;font-family:var(--display);font-size:1.25rem;line-height:1.15;letter-spacing:-.02em}
.phone-hero p{margin:0;color:#555}
.phone-btn{display:inline-flex;align-items:center;justify-self:start;background:#d42c33;color:#fff;font-weight:700;border-radius:10px;padding:8px 12px}
.phone-btn .pin{background:#fff;color:var(--accent)}
.phone-facts{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:12px 14px}
.phone-facts span{display:grid;font-size:.7rem;color:#666;background:#f6f3ee;border-radius:8px;padding:6px}
.phone-facts b{font-size:.74rem;color:#1b1620}
.phone-facts .pin{position:absolute;right:6px;top:-8px;margin:0}
.phone-img{height:90px;margin:0 14px 16px;border-radius:12px;background:linear-gradient(135deg,#f6d38a,#e59a4c 55%,#b8632a)}
@media (max-width:860px){.seo-demo{grid-template-columns:1fr}.phone-demo{grid-template-columns:1fr;justify-items:center}}
.center-head{text-align:center;margin-left:auto;margin-right:auto}
.center-head .lead{margin-left:auto;margin-right:auto}
.demo-note.center{text-align:center;margin-top:16px}
.anno{--gap:72px;position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,470px) minmax(0,1fr);column-gap:var(--gap);row-gap:0;max-width:1120px;margin:clamp(24px,4vw,40px) auto 0;align-items:center}
.anno-note{position:relative;display:flex;gap:10px;align-items:flex-start;padding:12px 0}
.anno-note.left{grid-column:1;text-align:right;flex-direction:row-reverse}
.anno-note.right{grid-column:3}
.anno-note small{display:block;font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-deep)}
.anno-note h3{font-size:1rem;margin:.1rem 0 .2rem}
.anno-note p{margin:0;font-size:.86rem;line-height:1.5;color:var(--ink-soft)}
.anno-num{display:grid;place-items:center;width:24px;height:24px;flex:none;border-radius:50%;background:var(--accent);color:#fff;font:700 .75rem/1 var(--body);box-shadow:0 0 0 3px rgba(212,44,51,.18)}
.anno-lines{position:absolute;inset:0;pointer-events:none;overflow:visible;z-index:2}
.anno-lines path{fill:none;stroke:var(--accent);stroke-width:2;stroke-dasharray:5 4}
.anno-lines circle{fill:var(--accent)}
.mock-part .pin{position:relative;z-index:3}
.mock-part .pin.pre{margin:0 8px 0 0}
.mock-part{grid-column:2;font-size:.92em;align-self:stretch;display:flex;flex-direction:column;justify-content:center;background:#fff;border-left:1px solid #e4ddd2;border-right:1px solid #e4ddd2;padding:14px 22px;font-family:var(--body);color:#2a2118}
.mock-part .pin{margin-left:6px}
.mock-bar{flex-direction:row;flex-wrap:wrap;align-items:center;gap:8px 12px;background:#efe9df;border-top:1px solid #e4ddd2;border-radius:18px 18px 0 0;padding:12px 16px}
.mock-bar .dots{display:flex;gap:5px}.mock-bar .dots i{width:9px;height:9px;border-radius:50%;background:#d6cdbf}
.mock-bar .tab{background:#fff;border-radius:8px 8px 0 0;padding:5px 10px;font-size:.78rem;font-weight:600;display:inline-flex;align-items:center}
.mock-bar .url{flex:1 1 100%;background:#fff;border-radius:99px;padding:5px 12px;font-size:.78rem;color:#555;display:flex;align-items:center}
.mock-nav{flex-direction:row;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-bottom:1px solid #f0ebe3}
.mock-nav .logo{font-family:var(--display);font-size:1rem;color:#8a4b12}
.mock-nav .links{display:flex;gap:12px;align-items:center;font-size:.82rem}
.mock-nav u{text-decoration:none;color:#2a2118}
.mock-hero{background:linear-gradient(180deg,#fbf3e4,#fff);gap:8px;padding:24px 22px}
.tagh{align-self:flex-start;font:700 .62rem/1 var(--body);letter-spacing:.08em;color:#8a4b12;background:#f6e3c2;border-radius:5px;padding:3px 6px}
.mock-hero .h1{margin:0;font-family:var(--display);font-weight:700;font-size:clamp(1.5rem,3vw,2rem);line-height:1.1;letter-spacing:-.03em;display:flex;align-items:center;flex-wrap:wrap}
.mock-hero .lead{margin:0;font-size:.9rem;color:#5a4f45;max-width:44ch}
.mock-hero .cta{align-self:flex-start;display:inline-flex;align-items:center;background:#d42c33;color:#fff;font-weight:700;font-size:.9rem;border-radius:10px;padding:9px 14px}
.mock-hero .cta .pin{background:#fff;color:var(--accent)}
.mock-facts{flex-direction:row;gap:8px;align-items:center}
.mock-facts span{flex:1;display:grid;font-size:.72rem;color:#6b6157;background:#f7f2ea;border-radius:10px;padding:8px 10px}
.mock-facts b{font-size:.85rem;color:#2a2118}
.mock-img{flex-direction:row;align-items:center}
.mock-img .img{position:relative;flex:1;height:120px;border-radius:14px;background:linear-gradient(160deg,#fbeedd,#f3dcc0);overflow:hidden;display:grid;place-items:center}
.mock-img .cake{width:62%;max-width:240px;height:auto;margin-top:-30px}
.mock-img .alt,.mock-img .file{position:absolute;left:10px;font:600 .7rem/1.3 ui-monospace,Menlo,monospace;background:rgba(255,255,255,.92);color:#2a2118;border-radius:6px;padding:4px 7px}
.mock-img .alt{bottom:36px}.mock-img .file{bottom:10px}
.mock-sec{gap:8px}
.mock-sec .h2{margin:0;font-family:var(--display);font-weight:700;font-size:1.2rem;display:flex;align-items:center}
.mock-sec .cards{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.mock-sec .cards div{display:grid;gap:3px;justify-items:start;background:#f7f2ea;border-radius:10px;padding:10px}
.mock-sec .cards b{font-size:.88rem}.mock-sec .cards small{font-size:.75rem;color:#6b6157}
.mock-foot{flex-direction:row;align-items:center;justify-content:space-between;gap:8px;background:#2a2118;color:#efe6da;font-size:.75rem;border-radius:0 0 18px 18px;border-bottom:1px solid #2a2118;padding:14px 20px}
.anno-left{grid-template-columns:minmax(0,400px) minmax(0,320px);max-width:none;margin-left:0;justify-content:start;align-items:start}
.serp-card{background:#fff;border:1px solid #e4ddd2;border-radius:18px;box-shadow:0 30px 50px -30px rgba(15,15,20,.35);font-family:Arial,Helvetica,sans-serif;display:grid;gap:6px;position:relative}
.serp-card>*{position:relative}
.serp-card .pin.edge{position:absolute;right:-30px;top:50%;margin:-11px 0 0;z-index:3}
.anno-left .serp-card{grid-column:1;grid-row:1 / span 4;align-self:start;margin:0;padding:16px 18px}
.anno-left .serp-card .serp-q{margin-bottom:12px}
.anno-left .serp-card .serp-title{font-size:1.05rem}
.anno-left .serp-card .serp-desc{font-size:.84rem}
.anno-left .anno-note{padding:8px 0}
.anno-right{grid-template-columns:minmax(0,300px) minmax(0,320px);max-width:none;margin-right:0;margin-top:34px;justify-content:end}
.share-part{align-self:center;position:relative;display:grid;gap:8px;justify-items:end;background:#e9e4dc;border-radius:18px;padding:16px 18px;font-family:var(--body);box-shadow:0 30px 50px -30px rgba(15,15,20,.3)}
.share-part>.pin{position:absolute;left:-11px;top:50%;margin:-11px 0 0;z-index:3}
.share-part .share-card{width:88%}
.share-part .share-img{height:90px}
.mock-part:last-of-type{box-shadow:0 30px 50px -30px rgba(15,15,20,.35)}
@media (max-width:1000px){
  .anno{grid-template-columns:minmax(0,600px);justify-content:center}
  .anno>*{grid-row:auto!important;grid-column:1!important;order:var(--o)}
  .anno-left,.anno-right{grid-template-columns:minmax(0,520px);justify-content:center;margin-left:auto;margin-right:auto}
  .anno-note{flex-direction:row!important;text-align:left!important;padding:10px 4px}
  .anno-lines{display:none}
  .serp-card .pin.edge{right:-6px}
  .share-part>.pin{left:-6px}
  .anno-note[style*="--o:11"]{margin-top:22px}
}
.own.four{grid-template-columns:repeat(4,1fr)}
@media (max-width:1000px){.own.four{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){.own.four{grid-template-columns:1fr}}
.link-row .link-note{align-self:center;font-size:.9rem;color:var(--ink-soft)}
.card-list{margin:.2rem 0 0;padding-left:1.1rem;display:grid;gap:.35rem;color:var(--ink-soft)}
.card-list li::marker{color:var(--accent)}
.own-card .card-fine{font-size:.85rem;padding-top:.5rem;border-top:1px solid var(--line)}
.own-card[id]{scroll-margin-top:110px}
/* Exempelsidor för paketen (sidor/exempel-*.html) */
.mx-resto{background:linear-gradient(180deg,#eef3e6,#fff)}
.mx-clean{background:linear-gradient(180deg,#e8f1f6,#fff)}
.mx-btns{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.mock-hero .cta.ghost{background:#fff;color:#1d3b4a;border:1.5px solid #1d3b4a}
.mx-menu,.mx-contact,.mx-map,.mx-quote,.mx-reviews,.mx-mail,.mx-cal,.mx-pay,.mx-shop,.mx-sms,.mx-admin{gap:8px}
.mx-menu{flex-direction:column}
.mx-row{display:flex;justify-content:space-between;gap:10px;font-size:.82rem;border-bottom:1px dashed #e7dfd3;padding:5px 0}
.mx-row span{color:#5a4f45;text-align:right}
.mx-menu>.pin,.mx-reviews>.pin,.mx-shop>.pin{align-self:flex-start}
.mx-form{display:grid;gap:6px}
.mx-form.two{grid-template-columns:1fr 1fr}
.mx-contact{flex-direction:row!important;align-items:center}
.mx-contact .mx-form{flex:1}
.mx-in{display:block;background:#f6f3ee;border:1px solid #e6dfd4;border-radius:8px;padding:7px 10px;font-size:.75rem;color:#8a7f73}
.mx-in.tall{height:44px}
.mx-btn{justify-self:start;align-self:flex-start;display:inline-flex;align-items:center;background:#2a2118;color:#fff;font-weight:700;font-size:.8rem;border-radius:8px;padding:7px 12px}
.mx-map{flex-direction:row!important;align-items:center;gap:12px}
.mx-mapbox{position:relative;width:110px;height:70px;flex:none;border-radius:10px;background:linear-gradient(135deg,#dfe9d6 0 40%,#cfe0ec 40% 55%,#e9e3d2 55%);overflow:hidden}
.mx-mapbox::before{content:"";position:absolute;left:0;right:0;top:46%;height:6px;background:#fff;opacity:.9}
.mx-pin{position:absolute;left:44%;top:18%;font-size:1.3rem}
.mx-map b{display:block;font-size:.85rem}.mx-map small{font-size:.72rem;color:#6b6157}
.mx-h{font-family:var(--display);font-size:.95rem;display:flex;align-items:center}
.mx-choice{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.mx-choice span{font-size:.75rem;border:1.5px solid #d8d0c4;border-radius:99px;padding:5px 10px}
.mx-choice span.on{border-color:#1d3b4a;background:#1d3b4a;color:#fff}
.mx-reviews{flex-direction:row!important;align-items:stretch}
.mx-rev{flex:1;display:grid;gap:3px;background:#f7f2ea;border-radius:10px;padding:9px 10px;font-size:.76rem}
.mx-rev b{color:#e2a400;letter-spacing:.05em}.mx-rev small{color:#6b6157}
.mx-mail{background:#f2f5f8!important}
.mx-mailhead{display:grid;font-size:.75rem;border-bottom:1px solid #dde3ea;padding-bottom:6px}
.mx-mail p{margin:0;font-size:.8rem;color:#33404a;display:flex;align-items:center;flex-wrap:wrap}
.mx-days,.mx-slots{display:flex;flex-wrap:wrap;gap:6px}
.mx-days span{text-align:center;font-size:.7rem;line-height:1.25;border:1px solid #e3dbcf;border-radius:8px;padding:5px 8px}
.mx-slots span{font-size:.75rem;border:1.5px solid #d8c7cf;border-radius:8px;padding:5px 9px}
.mx-days .on,.mx-slots .on{background:#7a3e5c;border-color:#7a3e5c;color:#fff}
.mx-days .off,.mx-slots .off{opacity:.35;text-decoration:line-through}
.mx-pay{flex-direction:row!important;justify-content:space-between;align-items:center;flex-wrap:wrap;background:#faf5f8!important;font-size:.82rem}
.mx-paybtns{display:flex;gap:6px}.mx-paybtns span{font-size:.72rem;font-weight:700;border:1px solid #e0d2da;background:#fff;border-radius:8px;padding:5px 9px}
.mx-shop{flex-direction:row!important;align-items:stretch}
.mx-prod{flex:1;display:grid;gap:3px;font-size:.76rem}
.mx-img{display:block;height:58px;border-radius:10px}
.mx-img.a{background:linear-gradient(160deg,#f3d9e4,#d9a7bd)}.mx-img.b{background:linear-gradient(160deg,#f6e7c8,#e0b56a)}.mx-img.c{background:linear-gradient(160deg,#e6e0f3,#a99bd1)}
.mx-prod small{color:#6b6157}
.mx-add{font-size:.68rem;font-weight:700;text-align:center;background:#7a3e5c;color:#fff;border-radius:7px;padding:5px}
.mx-sms{flex-direction:row!important;align-items:center;background:#f3f3f5!important}
.mx-bubble{flex:1;background:#e5e5ea;border-radius:16px 16px 16px 4px;padding:9px 12px;font-size:.78rem;color:#1c1c1e}
.mx-admin{background:#1b1620!important;color:#efe6ef;border-color:#1b1620!important}
.mx-admin .mx-h{color:#fff}
.mx-arow{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:.76rem;background:rgba(255,255,255,.06);border-radius:8px;padding:6px 9px}
.mx-arow em{font-style:normal;font-size:.66rem;font-weight:700;border-radius:99px;padding:3px 8px}
.mx-arow .ok{background:#2f7d4f}.mx-arow .new{background:#d42c33}.mx-arow .wait{background:#a7741a}
.mock-part.mx-admin:last-of-type{border-radius:0 0 18px 18px}
.mx-acc{display:inline-flex;align-items:center}
.mx-cart{font-weight:700}
.mock-nav .links{flex-wrap:wrap;row-gap:4px}
@media (max-width:640px){.mx-reviews,.mx-shop{flex-direction:column!important}.mx-form.two{grid-template-columns:1fr}}
.mk{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(18px,3vw,28px)}
.mk-list{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.mk-list li{display:grid;grid-template-columns:170px 1fr 92px;align-items:center;gap:12px;font-size:.92rem}
.mk-label{color:var(--ink-soft)}
.mk-bar{height:14px;border-radius:99px;background:var(--bg);overflow:hidden}
.mk-bar span{display:block;height:100%;border-radius:99px;background:#b9b1a6}
.mk-list li.sabi .mk-label{color:var(--ink);font-weight:700}
.mk-list li.sabi .mk-bar span{background:var(--accent)}
.mk-val{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
@media (max-width:640px){.mk-list li{grid-template-columns:1fr 84px}.mk-bar{grid-column:1/-1;grid-row:2}}
.mk-cols{display:grid;grid-template-columns:repeat(8,1fr);gap:clamp(6px,1.6vw,18px);align-items:end;height:340px;padding-top:28px;background:repeating-linear-gradient(to top,transparent 0 69px,var(--line) 69px 70px)}
.mk-cols li{display:flex!important;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:8px}
.mk-cols .mk-val{display:none}
.mk-cols .mk-bar{width:100%;max-width:58px;flex:1;display:flex;align-items:flex-end;background:none;border-radius:0;overflow:visible}
.mk-cols .mk-bar span{position:relative;width:100%;border-radius:10px 10px 0 0}
.mk-cols .mk-bar span::before{content:attr(data-v);position:absolute;bottom:100%;left:50%;transform:translateX(-50%);margin-bottom:6px;font-size:.8rem;font-weight:700;white-space:nowrap;color:var(--ink)}
.mk-cols .mk-label{text-align:center;font-size:.78rem;line-height:1.25;min-height:2.5em}
@media (max-width:640px){
  .mk-cols{display:grid;grid-template-columns:1fr;height:auto;gap:10px;padding-top:0;background:none}
  .mk-cols li{display:grid!important;grid-template-columns:1fr auto;height:auto;gap:4px 10px;align-items:center}
  .mk-cols .mk-label{grid-column:1;grid-row:1;text-align:left;min-height:0;font-size:.88rem}
  .mk-cols .mk-label br{display:none}
  .mk-cols .mk-val{display:block;grid-column:2;grid-row:1;font-size:.88rem}
  .mk-cols .mk-bar{grid-column:1/-1;grid-row:2;max-width:none;height:12px;flex:none;background:var(--bg);border-radius:99px;overflow:hidden;align-items:stretch}
  .mk-cols .mk-bar span{height:100%!important;width:var(--w);border-radius:99px}
  .mk-cols .mk-bar span::before{content:none}
}
.mk2{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(20px,3.5vw,36px)}
.mk2-stats{display:grid;grid-template-columns:1fr auto 1fr auto;gap:clamp(12px,2.5vw,28px);align-items:center}
.mk2-stat{display:grid;gap:2px;padding:18px 20px;border-radius:16px;background:var(--bg)}
.mk2-stat small{font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.mk2-stat strong{font-family:var(--display);font-size:clamp(1.8rem,4vw,2.6rem);letter-spacing:-.04em;line-height:1.05;color:var(--ink-soft)}
.mk2-stat span{font-size:.85rem;color:var(--ink-soft)}
.mk2-stat.sabi{background:var(--plum);box-shadow:0 20px 40px -24px rgba(36,26,43,.7)}
.mk2-stat.sabi small,.mk2-stat.sabi span{color:#cfc6d3}
.mk2-stat.sabi strong{color:#fff;font-size:clamp(2.2rem,5vw,3.2rem)}
.mk2-vs{font-size:.85rem;color:var(--ink-soft);font-style:italic}
.mk2-save{display:grid;justify-items:center;text-align:center}
.mk2-save strong{font-family:var(--display);font-size:clamp(2.4rem,5.5vw,3.6rem);line-height:1;letter-spacing:-.04em;color:var(--accent)}
.mk2-save span{font-size:.85rem;font-weight:600;color:var(--ink)}
.ps{position:relative;height:110px;margin:34px 12px 6px}
.ps-line{position:absolute;left:0;right:0;top:46px;height:4px;border-radius:99px;background:var(--line)}
.ps-zone{position:absolute;left:-8px;top:22px;height:52px;border-radius:14px;background:rgba(212,44,51,.1);border:1.5px dashed rgba(212,44,51,.55)}
.ps-zone span{position:absolute;left:10px;top:-24px;font-size:.78rem;font-weight:700;color:var(--accent-deep);white-space:nowrap}
.ps-sabi,.ps-other{position:absolute;top:48px;transform:translate(-50%,-50%)}
.ps-sabi i{display:block;width:18px;height:18px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px #fff,0 4px 10px rgba(212,44,51,.5)}
.ps-other i{display:block;width:12px;height:12px;border-radius:50%;background:#b9b1a6;box-shadow:0 0 0 3px #fff}
.ps-other b{position:absolute;top:18px;left:50%;transform:translateX(-50%);font-size:.78rem;font-weight:600;color:var(--ink-soft);white-space:nowrap}
.ps-end{position:absolute;top:84px;font-size:.72rem;color:var(--ink-soft)}
.ps-end.l{left:0}.ps-end.r{right:0}
.ps-legend{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;font-size:.85rem;color:var(--ink-soft);margin-top:8px}
.ps-legend .k{width:12px;height:12px;border-radius:50%;display:inline-block}
.ps-legend .k.sabi{background:var(--accent)}.ps-legend .k.other{background:#b9b1a6;margin-left:12px}
@media (max-width:760px){.mk2-stats{grid-template-columns:1fr 1fr}.mk2-vs{display:none}.mk2-save{grid-column:1/-1;grid-row:1;justify-items:start;text-align:left;grid-auto-flow:column;gap:10px;align-items:baseline}.ps,.ps-legend{display:none}.mk2-stat{padding:14px}}
.qa4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.qa4-card{position:relative;display:flex;flex-direction:column;gap:.45rem;padding:22px 20px 18px;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);color:var(--ink);text-decoration:none;transition:border-color .2s,transform .2s,box-shadow .2s}
.qa4-card:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 20px 40px -28px rgba(15,15,20,.4)}
.qa4-n{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--plum);color:#fff;font-weight:700;font-size:.85rem}
.qa4-card h3{font-size:1.05rem}
.qa4-big{margin:0;font-family:var(--display);font-weight:700;font-size:1.6rem;letter-spacing:-.03em;color:var(--accent)}
.qa4-card p:not(.qa4-big){margin:0;font-size:.9rem;color:var(--ink-soft);flex:1}
.qa4-more{font-size:.88rem;font-weight:700;color:var(--accent-deep);padding-top:.5rem;border-top:1px solid var(--line)}
@media (max-width:1000px){.qa4{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.qa4{grid-template-columns:1fr}}
.plan-demo{display:block;margin-top:.5rem;font-size:.88rem;font-weight:600;color:var(--accent-deep);text-align:center}
.pt-panel{background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border:1px solid rgba(232,225,215,.9);border-radius:var(--radius);padding:clamp(18px,3vw,30px);box-shadow:0 24px 50px -36px rgba(15,15,20,.35)}
.pt-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(20px,4vw,48px)}
.pt-list li{position:relative;padding:14px 0 14px 40px;border-bottom:1px solid var(--line);color:var(--ink-soft);line-height:1.5}
.pt-list li::before{content:"";position:absolute;left:0;top:13px;width:26px;height:26px;border-radius:50%;background:rgba(212,44,51,.1) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23d42c33' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12.5 10 17 19 7'/%3E%3C/svg%3E") center/14px no-repeat}
.pt-list b{display:block;color:var(--ink);font-family:var(--display);font-size:1.02rem;margin-bottom:2px}
.pt-foot{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;margin-top:18px;font-size:.92rem;color:var(--ink-soft)}
@media (max-width:700px){.pt-list{grid-template-columns:1fr}}
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
.incl-table caption{caption-side:top;text-align:left;font-family:var(--display);font-weight:700;font-size:1.25rem;letter-spacing:-.02em;color:var(--ink);padding-bottom:12px}
.incl-table{width:100%;border-collapse:collapse;font-size:.97rem;table-layout:fixed}
.incl-table col.incl-feat{width:52%}
.incl-table th,.incl-table td{padding:12px 10px;border-bottom:1px solid var(--line);text-align:center}
.incl-table thead th{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft)}
.incl-table th[scope=row],.incl-table thead th:first-child{text-align:left;font-weight:500}
.incl-table tr.incl-group th{padding-top:18px;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-deep);text-align:left}
.incl-table tr.incl-group a{color:inherit}
.incl-table tbody tr:last-child th,.incl-table tbody tr:last-child td{border-bottom:0}
.incl-table td{vertical-align:middle}
.incl-table .yes,.incl-table .no{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;vertical-align:middle;line-height:0}
.incl-table .yes{background:var(--accent)}
.incl-table .no{background:var(--line);color:var(--ink-soft)}
.incl-table .no svg{width:14px;height:14px;display:block}
@media (max-width:760px){.check-list,.glossary{grid-template-columns:1fr}.incl-table{font-size:.88rem}.incl-table th,.incl-table td{padding:10px 6px}.incl-table col.incl-feat{width:46%}.incl-table thead th{font-size:.6rem;letter-spacing:0;padding-left:2px;padding-right:2px}}
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
