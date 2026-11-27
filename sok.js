/* Sökfunktion för sabimedia.se – laddas på alla sidor.
   Lägger till en sökknapp i toppmenyn och öppnar en sökruta (även med / eller Cmd/Ctrl+K).
   Allt sökbart innehåll ligger i INDEX nedan. Ändrar du priser, paket eller frågor på sidan – uppdatera här också. */
(() => {
  const INDEX = [
    // Startsidan, Tjänster, Priser, FAQ och Kontakt
    { t: "Startsidan", p: "Hem", u: "/", d: "Hemsidor för småföretag i hela Sverige med fast engångspris från 1 500 kr exkl. moms.", k: "webbyrå borås hemsida borås webbdesign borås digital byrå bästa webbyrå köpa hemsida småföretag sverige" },
    { t: "Tjänster – det här ingår", p: "Tjänster", u: "/tjanster", d: "Egen adminpanel, produkter och varukorg, ditt varumärke, betalning på sidan, beställningar via mejl, information och kontakt.", k: "funktioner adminpanel varukorg betalning beställningar mejl varumärke design" },
    { t: "Webbdesign och webbutveckling", p: "Tjänster", u: "/tjanster#webbdesign", d: "Webbdesign för företag, från första utkast till lansering.", k: "webbdesign webbdesign byrå webbutveckling öppna webbutik webbutik hemsida med produkter hemsida med beställningsformulär onlinebeställningar skapa hemsida bygga hemsida webbdesign företag skapa företagshemsida skapa hemsida företag egen hemsida ny hemsida förbättra hemsida ta emot beställningar online" },
    { t: "Exempel på hemsidor", p: "Hem", u: "/#exempel", d: "Klädbutiken Studio Ofelia, Restaurang Ruta och städföretaget H.F StädService AB.", k: "exempel design studio ofelia restaurang ruta städ städservice klädbutik portfolio" },
    { t: "Kundomdömen", p: "Hem", u: "/#omdomen", d: "Vad kunderna säger, svar inom 24 timmar och vad du kan räkna med.", k: "recension omdöme cookie munch svarstid 24 timmar" },
    { t: "Så funkar det", p: "Tjänster", u: "/tjanster#sa-funkar-det", d: "Från idé till färdig hemsida, steg för steg.", k: "process steg arbetsgång hur går det till leverans lansering" },
    { t: "Priser och paket", p: "Priser", u: "/priser", d: "Start från 1 500 kr, Business från 2 800 kr och Pro från 4 300 kr. Engångspris exkl. moms.", k: "pris priser kostnad kostar paket start business custom offert moms engångspris" },
    { t: "Paket Start – från 1 500 kr", p: "Priser", u: "/priser", d: "Upp till 4 sidor, egen design, mobilanpassning, kontaktformulär, karta och grundläggande Google-anpassning. 1 månads support.", k: "pris kostnad start billigast enkel liten hemsida 1500" },
    { t: "Paket Business – från 2 800 kr", p: "Priser", u: "/priser", d: "Allt i Start plus fler sidor, formulär för offert, bokning eller beställning, recensioner och automatiska mejl. 2 månaders support.", k: "pris kostnad business mest komplett bokning offert recensioner 2800" },
    { t: "Paket Pro – från 4 300 kr", p: "Priser", u: "/priser", d: "Skräddarsydd lösning: bokningssystem med kalender, webbshop med betalning, kundkonton, adminpanel och integrationer.", k: "pris kostnad custom webbshop bokningssystem kalender kundkonton adminpanel integrationer betalning 4000 offert" },
    { t: "Vad kostar en hemsida till företag?", p: "Priser", u: "/priser#vad-kostar", d: "Svar om fast pris, engångskostnad, hemsida utan abonnemang och vilket paket som passar.", k: "hemsida pris kostnad billig billigt billig hemsida för småföretag fast pris utan abonnemang engångskostnad webbyrå priser webbyrå med fast pris småföretag paket" },
    { t: "Jämför paketen i detalj", p: "Priser", u: "/priser#jamfor", d: "Se exakt vilka funktioner som ingår i Start, Business och Pro.", k: "jämför jämförelse tabell skillnad funktioner paket ingår" },
    { t: "Tillägg utanför paketen", p: "Priser", u: "/priser", d: "Vill du ha något som inte ingår i paketet? Då tar vi fram en offert och skräddarsyr funktionen.", k: "tillägg extra funktion offert skräddarsy" },
    { t: "Exempel: Cookie Munch", p: "Tjänster", u: "/tjanster#cookie-munch", d: "Webbshop med betalning och adminsida för ett bageri i Borås, med kundens omdöme.", k: "exempel cookie munch recension omdöme webbshop bageri kundcase" },
    { t: "Du behåller nyckeln", p: "Tjänster", u: "/tjanster#agande", d: "Hemsidan är något du köper, inte hyr. Vill du byta webbyrå tar du med dig alltihop.", k: "äga ägande domän webbhotell inlåst namn" },
    { t: "Vanliga frågor (FAQ)", p: "FAQ", u: "/faq", d: "Svar på de vanligaste frågorna om pris, tid, ägande och support.", k: "faq frågor svar hjälp" },
    { t: "Kontakt och förfrågan", p: "Kontakt", u: "/kontakt", d: "Skicka en förfrågan eller boka ett kostnadsfritt samtal via Microsoft Teams. Vi svarar inom 24 timmar.", k: "kontakt kontakta mejl e-post hej@sabimedia.se formulär förfrågan" },
    // Vanliga frågor
    { t: "Får jag en egen design?", p: "FAQ", u: "/faq#faq-1", d: "Ja. Varje hemsida skräddarsys efter ditt företag – dina färger, din logga, dina bilder och dina texter.", k: "design unik mall logga färger" },
    { t: "Hur lång tid tar det?", p: "FAQ", u: "/faq#faq-2", d: "Första utkastet inom 24 timmar. Hela hemsidan tar från några dagar upp till några veckor.", k: "tid leveranstid veckor dagar snabbt" },
    { t: "Vilka kostnader kan komma senare?", p: "FAQ", u: "/faq#faq-3", d: "Inga som du inte känner till. Du säger ja till en summa före bygget.", k: "dolda kostnader avgift månadsavgift löpande fast pris" },
    { t: "Vad gör vi om jag vill ändra något?", p: "FAQ", u: "/faq#faq-4", d: "Mindre ändringar ingår, och sidan läggs ut på nätet först när du säger ja.", k: "ändringar godkänna nöjd gillar inte" },
    { t: "Hur mycket behöver jag göra själv?", p: "FAQ", u: "/faq#faq-5", d: "Ett uppstartsmöte, ditt material och en titt på utkastet. Bygget sköter vi.", k: "tid upptagen enkelt ingen tid" },
    { t: "Kan någon annan ta över hemsidan?", p: "FAQ", u: "/faq#faq-6", d: "Ja. Inloggningarna är dina, så en annan webbyrå eller webbutvecklare kan fortsätta.", k: "försvinner ta över utvecklare byta byrå" },
    { t: "Är hemsidan säker?", p: "FAQ", u: "/faq#faq-7", d: "Besöken krypteras med SSL, och hemsidan klarar sig utan plugin som ska hållas uppdaterade.", k: "hackad säkerhet ssl underhåll timpris 400 kr uppdateringsavtal säker plugin" },
    { t: "Kan jag ändra produkter och priser själv?", p: "FAQ", u: "/faq#faq-8", d: "Med Pro får du en administrationssida. Annars hjälper vi dig under supportperioden.", k: "ändra själv admin cms uppdatera" },
    { t: "Hur får jag betalt?", p: "FAQ", u: "/faq#faq-9", d: "Med Pro kan kunden betala direkt på hemsidan. Med Business skickas beställningar till dig via mejl.", k: "betalning betalt kort kassa" },
    { t: "Vem äger hemsidan?", p: "FAQ", u: "/faq#faq-10", d: "Det gör du. Du behåller sidan, adressen och webbhotellet.", k: "äga ägare" },
    { t: "Ingår publicering?", p: "FAQ", u: "/faq#faq-11", d: "Ja, i alla paket. Support i 1 månad (Start) eller 2 månader (Business och Pro).", k: "publicering lansering support underhåll" },
    { t: "Passar det mitt företag?", p: "FAQ", u: "/faq#faq-12", d: "Vi är en digital byrå som bygger hemsidor för alla typer av småföretag – butiker, caféer, hantverkare, konsulter och mer.", k: "passar bransch företag" },
    // Branscher
    { t: "Branscher vi hjälper", p: "Branscher", u: "/branscher", d: "Elva branscher vi bygger hemsidor åt – från restauranger till föreningar.", k: "branscher bransch kategorier professionell hemsida företagshemsida hemsida för småföretag billig hemsida för småföretag hemsida till företag hemsida för tjänsteföretag hemsida för nystartat företag företag utan hemsida hemsida som säljer digital närvaro" },
    { t: "Mat & livsmedel", p: "Branscher", u: "/branscher#mat", d: "Restauranger, caféer, bagerier och catering.", k: "restaurang lunch café kafé konditori bageri foodtruck gatukök catering gårdsbutik livsmedel mat" },
    { t: "Hemsida för restaurang, bageri och konditori", p: "Branscher", u: "/branscher#mat", d: "Meny, onlinebeställning och beställning av tårta direkt på hemsidan.", k: "hemsida restaurang restaurang hemsida onlinebeställning restaurang hemsida bageri hemsida för bageri med beställningsformulär hemsida konditori beställa tårta online meny" },
    { t: "Klinik & hälsa", p: "Branscher", u: "/branscher#klinik", d: "Behandlingar, priser, kontakt och bokning på hemsidan.", k: "hemsida klinik hemsida tandläkare hemsida fysioterapeut mottagning patient bokning vård fysioterapeut naprapat psykoterapeut terapeut tandläkare tandklinik optiker gym träning pt personlig tränare" },
    { t: "Hem & fastighet", p: "Branscher", u: "/branscher#hem", d: "Städföretag, mäklare, fastighetsservice och boenden.", k: "städ städföretag lokalvård hotell pensionat stuga stuguthyrning semesterboende mäklare fastighet" },
    { t: "Hantverk & bygg", p: "Branscher", u: "/branscher#hantverk", d: "Hemsida för hantverkare och byggföretag, med bilder på utförda arbeten och offertformulär.", k: "hemsida hantverkare hemsida byggfirma hemsida elektriker hantverkare bygg byggföretag snickare elektriker rörmokare målare trädgård markarbete offert renovering" },
    { t: "Butiker & produkter", p: "Branscher", u: "/branscher#butiker", d: "Detaljhandel, blomsterbutiker och produktvarumärken.", k: "hemsida butik hemsida med produktkatalog hemsida med produkter butik detaljhandel blommor florist present inredning specialbutik produkter varumärke producent webbshop" },
    { t: "Kreativa tjänster", p: "Branscher", u: "/branscher#kreativa", d: "Fotografer och andra kreativa verksamheter.", k: "fotograf bröllopsfotograf porträtt produktfoto event foto kreativ" },
    { t: "Fritid & aktiviteter", p: "Branscher", u: "/branscher#fritid", d: "Föreningar, sportklubbar och aktivitetsföretag.", k: "förening idrottsförening sportklubb träningsförening aktivitet fritid klubb" },
    { t: "Event & fest", p: "Branscher", u: "/branscher#event", d: "Eventplanerare, festlokaler och bröllopsplanerare.", k: "event fest festlokal bröllop bröllopsplanerare" },
    { t: "Hemsida för event och festlokal", p: "Branscher", u: "/branscher#event", d: "Bilder, priser, förfrågningar och bokningssida för event.", k: "hemsida event hemsida festlokal bokningssida event bröllop kalas lokal uthyrning" },
    { t: "Utbildning & kurser", p: "Branscher", u: "/branscher#utbildning", d: "Privata utbildare, kursverksamheter och musikskolor.", k: "utbildning kurs kurser musikskola lärare" },
    { t: "Konsult- & företagstjänster", p: "Branscher", u: "/branscher#konsult", d: "Fristående konsulter, redovisningsbyråer och mindre rådgivningsföretag.", k: "hemsida konsult hemsida coach hemsida rådgivare konsult redovisning bokföring byrå rådgivning" },
    { t: "Personliga tjänster", p: "Branscher", u: "/branscher#personliga", d: "Skräddare, sömmerskor och reparationsföretag.", k: "skräddare sömmerska reparation laga" },
    // Om oss
    { t: "Om oss", p: "Om oss", u: "/om-oss", d: "Sabimedia är en webbyrå i Borås som bygger hemsidor åt småföretag i hela Sverige.", k: "om sabi sabimedia företaget" },
    { t: "Teamet – Safiya och Warda", p: "Om oss", u: "/om-oss#team", d: "Safiya Ibrahim, grundare och lead developer. Warda, head of design och user experience.", k: "team personal safiya warda grundare designer utvecklare" },
    { t: "Företagsuppgifter", p: "Om oss", u: "/om-oss#team", d: "Enskild firma med F-skatt, org.nr 010928-2947, Borås.", k: "org.nr organisationsnummer f-skatt enskild firma adress instagram" },
    // Övriga sidor
    { t: "Boka ett kostnadsfritt samtal", p: "Boka", u: "/boka", d: "Välj dag och tid för ett samtal via Microsoft Teams.", k: "boka samtal möte teams tid kalender gratis kostnadsfritt" },
    { t: "Så tar vi hand om dig", p: "Boka", u: "/boka#omtanke", d: "Vi lyssnar först, du får ett fast pris före start, inget publiceras utan ditt godkännande och support ingår efter lansering.", k: "omtanke trygghet trygg support hjälp kund process godkänna team" },
    { t: "Vad kostar en hemsida?", p: "Guide", u: "/vad-kostar-en-hemsida", d: "Vad du får för 1 500, 2 800 och 4 300 kr, löpande kostnader och hur du räknar ut totalkostnaden.", k: "pris kostnad vad kostar en hemsida totalkostnad domän webbhotell månadsavgift billig hemsida guide" },
    { t: "Så väljer du webbyrå", p: "Guide", u: "/valja-webbyra", d: "Tio frågor om pris, ägande, support och tid att ställa innan du skriver på.", k: "välja webbyrå frågor checklista bästa webbyrå jämföra byrå varningstecken guide" },
    { t: "Hemsida till bageri och café", p: "Branscher", u: "/hemsida-bageri-cafe", d: "Sortiment, öppettider och beställning online. Från 1 500 kr.", k: "bageri café konditori tårta beställa tårta online hemsida bageri hemsida café foodtruck" },
    { t: "Hemsida med bokning och beställning", p: "Funktioner", u: "/hemsida-med-bokning", d: "Bokningsformulär med Business eller bokningssystem med kalender med Pro.", k: "bokning boka tid bokningssystem kalender beställning beställningsformulär onlinebokning" },
    { t: "Så använder vi AI", p: "Om oss", u: "/sa-anvander-vi-ai", d: "AI hjälper till med kod och textutkast. Design och granskning gör vi, och kunddata delas aldrig.", k: "ai artificiell intelligens chatgpt kod texter design kunddata" },
    { t: "Hemsida utan månadskostnad", p: "Guide", u: "/hemsida-utan-manadskostnad", d: "Köpa eller hyra hemsida? Så jämför du totalkostnaden över tre år.", k: "månadskostnad månadsavgift abonnemang hyra köpa hemsida engångspris utan abonnemang" },
    { t: "Sluta ta beställningar i DM", p: "Guide", u: "/bestallningar-instagram", d: "Flytta beställningar från Instagram till ett formulär eller en webbshop.", k: "instagram dm beställningar sociala medier hembagare liten butik webbshop" },
    { t: "Hemsida för nystartat företag", p: "Guide", u: "/hemsida-nystartat-foretag", d: "Checklista: domän, sidor, kontakt och Google-företagsprofil.", k: "nystartat företag starta eget första hemsida checklista domän google företagsprofil" },
    { t: "Vilka är Sabimedia?", p: "FAQ", u: "/faq#faq-14", d: "Webbyrå i Borås som bygger hemsidor åt småföretag i hela Sverige.", k: "sabimedia sabi media vilka är ni om företaget" },
    { t: "Måste jag begära offert?", p: "Priser", u: "/priser#vad-kostar", d: "Nej, inte för Start och Business. Offert behövs bara för Pro och tillägg.", k: "offert fast pris paketpris" },
    { t: "Webbyrå i Borås", p: "Borås", u: "/webbyra-boras", d: "Hemsidor för småföretag i Borås och hela Sverige, från 1 500 kr.", k: "webbyrå borås hemsida borås webbdesign borås sjuhärad lokal webbyrå" },
    { t: "Guider för småföretag", p: "Guider", u: "/guider", d: "Alla guider om pris, funktioner, branscher och att komma igång.", k: "guider guide artiklar tips kunskap blogg" },
    { t: "Går det att få en bra hemsida för under 5 000 kr?", p: "Guide", u: "/hemsida-under-5000-kr", d: "Går det? Vad du får för 1 500, 2 800 och 4 300 kr, och när det inte räcker.", k: "billig hemsida under 5000 kr 10000 kr budget prisvärd hemsida billigt" },
    { t: "Varför syns inte min nya hemsida på Google?", p: "Guide", u: "/hemsida-syns-inte-pa-google", d: "Search Console, sajtkarta, Google-företagsprofil och recensioner.", k: "google syns inte indexering search console sajtkarta synas på google seo" },
    { t: "Checklista inför ny hemsida", p: "Guide", u: "/checklista-ny-hemsida", d: "Logga, bilder, priser och kontaktuppgifter – det här behöver du ha klart.", k: "checklista material logga bilder texter kravspecifikation inför beställning" },
    { t: "Enkel webbshop för små säljare", p: "Funktioner", u: "/enkel-webbshop", d: "Varukorg, betalning och adminpanel. Från 4 300 kr.", k: "webbshop webbutik e-handel sälja online betalning varukorg shopify" },
    { t: "Hemsida till restaurang och catering", p: "Branscher", u: "/hemsida-restaurang", d: "Meny, öppettider, bordsbokning och beställning. Från 1 500 kr.", k: "restaurang lunch catering meny bordsbokning onlinebeställning hemsida restaurang" },
    { t: "Hemsida till hantverkare", p: "Branscher", u: "/hemsida-hantverkare", d: "Utförda jobb, område och offertformulär. Från 1 500 kr.", k: "hantverkare byggfirma elektriker snickare rörmokare målare offert hemsida hantverkare" },
    { t: "Hemsida till städföretag", p: "Branscher", u: "/hemsida-stadforetag", d: "Tjänster, områden, priser och offertförfrågningar. Från 1 500 kr.", k: "städföretag städfirma lokalvård flyttstäd rut hemsida städ" },
    { t: "Hemsida till klinik", p: "Branscher", u: "/hemsida-klinik", d: "Behandlingar, team och tidsbokning. Från 1 500 kr.", k: "klinik tandläkare fysioterapeut naprapat terapeut optiker tidsbokning hemsida klinik" },
    { t: "Hemsida till eventföretag och festlokal", p: "Branscher", u: "/hemsida-event", d: "Bilder, priser och bokningsförfrågningar för datum och gäster.", k: "event festlokal bröllop eventplanerare bokningsförfrågan hemsida event" },
    { t: "Vem äger hemsidan?", p: "Guide", u: "/vem-ager-hemsidan", d: "Domän, webbhotell, inloggningar och själva sidan ska stå i ditt namn.", k: "äga ägande domän webbhotell inloggning byta byrå inlåst" },
    { t: "Använder ni AI?", p: "FAQ", u: "/faq#faq-13", d: "Ja, för kod och textutkast. Designen bestämmer vi tillsammans med dig.", k: "ai artificiell intelligens" },
    { t: "Cookie Munch hembageri: webbshop med betalning och adminpanel", p: "Kundcase", u: "/kundcase-cookie-munch", d: "Hur bageriet Cookie Munch fick beställningarna samlade på en egen hemsida.", k: "kundcase case referens cookie munch bageri resultat" },
    { t: "Synas på Google – guide", p: "Guide", u: "/synas-pa-google", d: "Företagsprofil, hemsidan, AI-översikter och annonser. Checklista, SEO-myter och begreppslista.", k: "synas på google seo sökmotoroptimering företagsprofil maps google my business search console ai översikt chatgpt annonser google ads begrepp ordlista" },
    { t: "Grundläggande SEO – så bygger vi", p: "Tjänster", u: "/grundlaggande-seo", d: "Titlar, rubriker, strukturerad data, fart, mobil och tydliga knappar. Ingår i alla paket.", k: "grundläggande seo google-anpassning sökmotoroptimering ingår titel rubrik sajtkarta snabb mobil ux ui" },
    { t: "Sökordsanalys", p: "Tjänster", u: "/seo-tjanst#sokord", d: "Sökord, sökvolym, sökintention, affärspotential, konkurrens och en sökordskarta med ett huvudsökord per sida.", k: "sökordsanalys keyword research sökord sökvolym sökintention keyword map sökordskarta" },
    { t: "Uppföljning och mätning av SEO", p: "Tjänster", u: "/seo-tjanst#matning", d: "Search Console, sökord, position, organisk trafik i Google Analytics 4 och kontaktförfrågningar.", k: "uppföljning mätning statistik search console google analytics ga4 trafik position" },
    { t: "GEO – optimera för AI-sökningar", p: "Tjänster", u: "/seo-tjanst#geo", d: "Vi gör dina sidor lätta för ChatGPT, Gemini och Googles AI-översikter att förstå och citera.", k: "geo ai-sök ai sökning chatgpt gemini ai-översikt generativ sökmotoroptimering" },
    { t: "Hjälp med befintlig hemsida", p: "Tjänster", u: "/hjalp-med-befintlig-hemsida", d: "Vi hjälper till även om någon annan har byggt hemsidan. Från 300 kr i timmen exkl. moms.", k: "befintlig hemsida gammal hemsida ändra hemsida hjälp med hemsidan felsökning uppdatera" },
    { t: "Varför är Sabimedia billigare?", p: "Pris", u: "/vad-kostar-en-hemsida#billigare", d: "Inga onödiga kostnader, egen kod utan licenser, fasta paket och AI som stöd.", k: "billig varför billigare pris jämför byråer" },
    { t: "Hemsida för småföretag", p: "Tjänster", u: "/hemsida-for-smaforetag", d: "Från 1 500 kr, fast pris och ingen månadsavgift. Vad ett litet företag behöver och om du ska bygga själv.", k: "hemsida för småföretag hemsida till småföretag litet företag småföretagare bygga själv hemsidebyggare" },
    { t: "Vilket paket ska jag välja?", p: "Guide", u: "/vilket-paket", d: "Jämför Start, Business och Pro, med ett exempel för varje.", k: "jämför paket välja paket start business pro skillnad" },
    { t: "Exempel: Start (restaurang)", p: "Exempel", u: "/exempel-start", d: "En påhittad restaurang byggd med Start, punkt för punkt.", k: "exempel start restaurang 1500" },
    { t: "Exempel: Business (städfirma)", p: "Exempel", u: "/exempel-business", d: "En påhittad städfirma med offertformulär, omdömen och automatiska mejl.", k: "exempel business städfirma offert" },
    { t: "Exempel: Pro (Studio Ofelia)", p: "Exempel", u: "/exempel-pro", d: "En påhittad salong med bokningskalender, webbshop, betalning och adminpanel.", k: "exempel pro salong bokningssystem webbshop adminpanel" },
    { t: "SEO-tjänst – mer omfattande SEO", p: "Tjänster", u: "/seo-tjanst", d: "Tillval: sajtkarta och Search Console, sökordsanalys, konkurrentanalys, nya sidor, lokal synlighet och uppföljning. Pris enligt överenskommen offert.", k: "seo tjänst seo-byrå sökmotoroptimering sökord sökordsanalys konkurrentanalys konkurrenter lokal seo tillval omfattande" },
    { t: "Ingår SEO i paketen?", p: "FAQ", u: "/faq#faq-18", d: "Ja, grundläggande SEO ingår i alla paket. Mer omfattande SEO finns som tillval.", k: "seo google-anpassning sökmotoroptimering ingår" },
    { t: "Tillgänglighetslagen och din hemsida", p: "Guide", u: "/tillganglighetslagen-hemsida", d: "Vem lagen gäller, undantaget för mikroföretag och vad som ingår hos oss.", k: "tillgänglighet tillgänglighetslagen wcag eaa pts webbshop e-handel" },
    { t: "Villkor", p: "Villkor", u: "/villkor", d: "Betalning, löpande kostnader, support, uppdateringsavtal och ansvar för säkerheten.", k: "villkor tjänstevillkor avtal betalning faktura support uppsägning" },
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
    empty.innerHTML = `Inga träffar för ”${esc(v)}”. Prova ett annat ord eller <a href="/kontakt">fråga oss direkt</a>.`;
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
