# Genereert het stretchfolie-artikel en het Roderick-interview voor .be (NL), .be (FR) en .de (DE).
# Gebruik: python3 -I gen_stretch_interview.py <outdir>
import sys, os

OUT = sys.argv[1]
B = '#0b99bc'
WRAP = '<div style="font-family: inherit; line-height: 1.7; color: #333333; max-width: 860px;">'
def H2(t): return f'<h2 style="font-family: inherit; font-size: 25px; line-height: 1.3; margin: 35px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid {B};">{t}</h2>'
def H3(t): return f'<h3 style="font-family: inherit; font-size: 20px; line-height: 1.3; margin: 25px 0 10px 0;">{t}</h3>'
def P(t): return f'<p style="font-family: inherit;">{t}</p>'
def A(href, t, bold=False): return f'<a style="color: {B};{" font-weight: bold;" if bold else ""}" href="{href}">{t}</a>'
def KORT(t): return f'<div style="background: #f9f9f9; border-left: 5px solid {B}; padding: 15px; border-radius: 5px; margin: 0 0 25px 0;"><p style="font-family: inherit; margin: 0; font-size: 17px;">{t}</p></div>'
def BOX(t): return f'<div style="background: #f9f9f9; border-left: 5px solid {B}; padding: 15px; border-radius: 5px; margin: 20px 0;"><p style="font-family: inherit; margin: 0;">{t}</p></div>'
def TABLE(head, rows):
    h = ''.join(f'<th style="padding: 10px; text-align: left;">{c}</th>' for c in head)
    body = ''
    for i, r in enumerate(rows):
        bg = ' background: #f9f9f9;' if i % 2 else ''
        body += f'<tr style="border-bottom: 1px solid #dddddd;{bg}">' + ''.join(f'<td style="padding: 10px;">{c}</td>' for c in r) + '</tr>'
    return f'<div style="overflow-x: auto; margin: 0 0 20px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 15px;"><thead><tr style="background: {B}; color: #ffffff;">{h}</tr></thead><tbody>{body}</tbody></table></div>'
def CHECKS(title, items):
    s = f'<div style="background: #f9f9f9; border-radius: 5px; padding: 15px 20px; margin: 25px 0 0 0;"><p style="font-family: inherit; margin: 0 0 8px 0;"><strong>{title}</strong></p>'
    for i, it in enumerate(items):
        m = '0' if i == len(items) - 1 else '0 0 6px 0'
        s += f'<p style="font-family: inherit; margin: {m};"><span style="color: {B}; font-weight: bold;">✓</span> {it}</p>'
    return s + '</div>'
def STEPS(items):
    return ''.join(f'<p style="font-family: inherit; margin: 0 0 6px 0;"><span style="color: {B}; font-weight: bold;">✓</span> {it}</p>' for it in items)
def CTA(title, text, href, btn):
    return (f'<div style="background: {B}; color: #ffffff; padding: 20px; border-radius: 5px; margin: 25px 0; text-align: center;">'
            f'<p style="font-family: inherit; margin: 0 0 10px 0; font-size: 19px;"><strong>{title}</strong></p>'
            f'<p style="font-family: inherit; margin: 0 0 15px 0;">{text}</p>'
            f'<p style="font-family: inherit; margin: 0;"><a style="display: inline-block; background: #ffffff; color: {B}; padding: 12px 24px; border-radius: 5px; text-decoration: none; font-weight: bold;" href="{href}">{btn}</a></p></div>')
def COMPARE(a, b, note):
    def card(t, lines, res, col):
        return (f'<div style="flex: 1; min-width: 220px; background: #f9f9f9; border-top: 4px solid {col}; border-radius: 5px; padding: 15px;">'
                f'<p style="font-family: inherit; margin: 0 0 8px 0;"><strong>{t}</strong></p>' +
                ''.join(f'<p style="font-family: inherit; margin: 0 0 4px 0;">{l}</p>' for l in lines) +
                f'<p style="font-family: inherit; margin: 8px 0 0 0; font-size: 18px; color: {col};"><strong>{res}</strong></p></div>')
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0 8px 0;">{card(*a, B)}{card(*b, "#df4f4f")}</div>'
            f'<p style="font-family: inherit; font-size: 13px; color: #777;">{note}</p>')
def FORMULA(t): return f'<div style="background: #eaf7fa; border-radius: 5px; padding: 15px; margin: 15px 0; text-align: center; font-size: 17px;"><strong>{t}</strong></div>'
def IFRAME(src, title, h):
    return f'<p style="font-family: inherit;"><iframe style="border: 1px solid #dddddd; border-radius: 5px; width: 100%; height: {h};" title="{title}" src="{src}" width="100%" height="700" loading="lazy"></iframe></p>'
YT = ('<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin: 20px 0;"><iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; border-radius: 5px;" '
      'title="Handwikkelfolie controleren met een weegschaal: zo doe je dat" src="https://www.youtube.com/embed/fBIjfGYHVtg" allowfullscreen="allowfullscreen" loading="lazy"></iframe></div>')
def AUTHOR(img, alt, head, name_html, text):
    pic = f'<div style="flex: 0 0 120px;"><img style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid {B};" src="{img}" alt="{alt}"></div>' if img else ''
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 25px; align-items: center; border-top: 1px solid #f0f0f0; padding-top: 30px; margin-top: 30px;">{pic}'
            f'<div style="flex: 1; min-width: 280px;"><h4 style="margin: 0 0 5px 0; color: #333; font-size: 1.2em;">{head}</h4>'
            f'<p style="margin: 0 0 15px 0; font-weight: bold; color: {B};">{name_html}</p>'
            f'<p style="margin: 0; line-height: 1.6; color: #555;">{text}</p></div></div>')
RODERICK = 'https://cdn.webshopapp.com/shops/293467/files/495011501/roderick-klein.jpg'
CALC_NL = 'https://sitecom244.github.io/stretchfolie-checker/'
CALC_H = 'clamp(840px, calc(1600px - 100vw), 1240px)'

def write(name, html):
    open(os.path.join(OUT, name), 'w').write(html)

# ---------------------------------------------------------------- STRETCHFOLIE
L = {
 'be': dict(
   p17='https://www.verpakkingenxl.be/nl/6-rollen-stretchfolie-van-17-my.html', p20='https://www.verpakkingenxl.be/nl/6-rollen-stretchfolie-van-20-my.html',
   p23='https://www.verpakkingenxl.be/nl/6-rollen-stretchfolie-van-23-my.html', p30=None,
   zwart='https://www.verpakkingenxl.be/nl/6-rollen-zwarte-stretchfolie-van-20-my.html', nano='https://www.verpakkingenxl.be/nl/inpakken-en-bescherming/wikkelfolie/nano-wikkelfolie/',
   machine='https://www.verpakkingenxl.be/nl/folie/stretchfolie/machinewikkelfolie/', disp='https://www.verpakkingenxl.be/nl/stretchfolie-handwikkelfolie-dispenser.html',
   cat='https://www.verpakkingenxl.be/nl/folie/stretchfolie/handwikkelfolie/', about='https://www.verpakkingenxl.be/nl/service/about/'),
 'fr': dict(
   p17='https://www.verpakkingenxl.be/fr/film-tirable-film-demballage-rouleaux-main-6-pcs-l.html', p20='https://www.verpakkingenxl.be/fr/film-tirable-film-demballage-rouleaux-main-6-pcs-b.html',
   p23='https://www.verpakkingenxl.be/fr/film-tirable-film-demballage-rouleaux-main-6-pices.html', p30=None,
   zwart='https://www.verpakkingenxl.be/fr/film-tirable-rouleaux-main-noir-6-pcs-basic-20-my.html', nano='https://www.verpakkingenxl.be/fr/emballage-et-protection/film-de-banderolage/film-de-banderolage-nano/',
   machine='https://www.verpakkingenxl.be/fr/film-demballage/film-etirable/film-etirable-machine/', disp='https://www.verpakkingenxl.be/fr/distributeur-de-film-demballage-tirable.html',
   cat='https://www.verpakkingenxl.be/fr/film-demballage/film-etirable/film-etirable-manuel/', about='https://www.verpakkingenxl.be/fr/service/about/'),
 'de': dict(
   p17='https://www.verpackungenxl.de/6-rollen-stretchfolie-von-17-my.html', p20='https://www.verpackungenxl.de/6-rollen-stretchfolie-von-20-my.html',
   p23='https://www.verpackungenxl.de/6-rollen-stretchfolie-von-23-my.html', p30='https://www.verpackungenxl.de/stretchfolie-6-handrollen-power-30-my.html',
   zwart='https://www.verpackungenxl.de/6-rollen-schwarze-stretchfolie-von-20-my.html', nano='https://www.verpackungenxl.de/verpackung-und-schutz/wickelfolie/nano-wickelfolie/',
   machine='https://www.verpackungenxl.de/folie/stretchfolie/maschinenwickelfolie/', disp='https://www.verpackungenxl.de/stretchfolien-handwickelfolien-spender.html',
   cat='https://www.verpackungenxl.de/folie/stretchfolie/handwickelfolie/', about='https://www.verpackungenxl.de/service/about/'),
}
def lk(u, t): return A(u, t) if u else t

def stretch_be():
    l = L['be']
    s = P('Vergelijk je stretchfolie op prijs per rol? Dan vergelijk je vaak geen appels met appels. Twee rollen met exact dezelfde omschrijving kunnen in werkelijkheid flink verschillen. Met een weegschaal en onze gratis calculator check je in twee minuten wat er echt op jouw rol zit.')
    s += WRAP + KORT('<strong>Het korte antwoord:</strong> je controleert handwikkelfolie met een weegschaal. Weeg de volle rol, trek het gewicht van de lege koker eraf en vergelijk de uitkomst met het gewicht dat er volgens de specificaties op hoort te zitten. Dat verwachte gewicht bereken je met <strong>dikte (my) × breedte (cm) × lengte (m) × 0,0092</strong>. Een rol van 20 my, 50 cm breed en 300 meter lang hoort dus <strong>2.760 gram folie</strong> te bevatten. Zit je meer dan 5% lager, dan is de folie dunner of korter dan beloofd.')
    s += P('In gesprekken met klanten krijgen we regelmatig vragen over stretchfolie. Je vergelijkt onze prijs met wat je nu betaalt, en dat is logisch: je wilt niet te veel betalen. Alleen merken we in die gesprekken vaak dat er geen appels met appels worden vergeleken.')
    s += P('In dit artikel lees je hoe je in twee minuten zelf nameet wat er op jouw rol zit, hoe je de uitkomst leest en hoe je daarna twee aanbiedingen eerlijk vergelijkt. Rekenen hoeft niet: verderop staat een gratis calculator die het voor je doet.')
    s += YT
    s += H2('Waarom twee dezelfde rollen toch verschillen')
    s += P('Op papier lijken alle rollen handwikkelfolie van 20 my hetzelfde: 20 my dik, 300 meter lang, 50 cm breed. Leg je ze naast elkaar, dan blijkt er toch verschil te zitten in wat je echt krijgt. Een rol heeft drie maten, en maar één daarvan controleer je met het blote oog.')
    s += TABLE(['Maat', 'Zelf te controleren?', 'Hoe'], [
        ['<strong>Breedte (cm)</strong>', 'Ja, direct', 'Rolmaat erlangs. Een afwijking valt meteen op.'],
        ['<strong>Dikte (my)</strong>', 'Niet op het oog', 'Het verschil tussen 17 en 20 my is 0,003 mm. Dat voel en zie je niet.'],
        ['<strong>Lengte (m)</strong>', 'Niet op het oog', 'Niemand rolt 300 meter af om na te meten.']])
    s += P('Precies bij dikte en lengte gaat het dus mis. Een rol lijkt goedkoop, maar is dunner of korter dan de omschrijving belooft. Dan betaal je per meter folie meer dan je dacht, en wikkel je per pallet ook nog eens meer slagen om dezelfde stevigheid te halen.')
    s += BOX('<strong>My</strong> staat voor micrometer, ook geschreven als micron of µm. Eén my is een duizendste millimeter. Folie van 20 my is dus 0,02 mm dik.')
    s += H2('Zo controleer je handwikkelfolie in 4 stappen')
    s += P('Je hebt alleen een weegschaal en een lege koker nodig. Een keukenweegschaal of pakketweegschaal die tot 5 kilo op de gram nauwkeurig weegt, is genoeg.')
    s += P('<strong>Stap 1. Weeg de volle rol.</strong> Zonder doos en zonder dispenser. Noteer het gewicht in grammen.')
    s += P('<strong>Stap 2. Weeg een lege koker.</strong> Gebruik een koker van dezelfde leverancier, want kokers verschillen in wanddikte en dus in gewicht. Bewaar er daarom altijd één van je vorige doos.')
    s += P('<strong>Stap 3. Trek de koker van het totaal af.</strong> Wat overblijft, is het nettogewicht: de folie die je echt hebt gekocht.')
    s += P('<strong>Stap 4. Vergelijk met het verwachte gewicht.</strong> Reken het uit met de formule hieronder, zoek het op in de tabel of vul de calculator in.')
    s += H2('De formule: wat hoort een rol stretchfolie te wegen?')
    s += P('Handwikkelfolie is gemaakt van LLDPE, een soort polyetheen met een soortelijk gewicht van ongeveer 0,92 gram per cm³. Ken je de dikte, breedte en lengte, dan ken je het volume van de folie. En daarmee ook het gewicht.')
    s += FORMULA('Verwacht foliegewicht (gram) = dikte (my) × breedte (cm) × lengte (m) × 0,0092')
    s += P('Voorbeeld: 20 my × 50 cm × 300 m × 0,0092 = <strong>2.760 gram</strong>')
    s += H3('Een rekenvoorbeeld uit de praktijk')
    s += P('We wogen een rol zwarte handwikkelfolie van 20 my, 300 meter lang en 50 cm breed:')
    s += STEPS(['Totaalgewicht van de rol: 2.977 gram', 'Gewicht van de lege koker: 227 gram', 'Netto folie: 2.977 − 227 = 2.750 gram', 'Verwacht: 2.760 gram. Afwijking: 10 gram, oftewel 0,4%'])
    s += P('Een verschil van 0,4% valt ruim binnen de tolerantie. Deze rol bevat wat de omschrijving belooft.')
    s += H2('Tabel: verwacht foliegewicht per rol')
    s += P('Geen zin om te rekenen? Hieronder staat het verwachte nettogewicht voor de meest gebruikte rollen, met de ondergrens waar een rol niet onder hoort te komen. Alle gewichten zijn exclusief koker.')
    s += TABLE(['Dikte', 'Breedte × lengte', 'Verwacht nettogewicht', 'Ondergrens (−5%)', 'Folie per doos van 6'], [
        ['12 my', '50 cm × 300 m', '1.656 g', '1.573 g', '9,9 kg'], [lk(l['p17'], '17 my'), '50 cm × 300 m', '2.346 g', '2.229 g', '14,1 kg'],
        [lk(l['p20'], '20 my'), '50 cm × 300 m', '2.760 g', '2.622 g', '16,6 kg'], [lk(l['p23'], '23 my'), '50 cm × 300 m', '3.174 g', '3.015 g', '19,0 kg'],
        [lk(l['p30'], '30 my'), '50 cm × 300 m', '4.140 g', '3.933 g', '24,8 kg'], ['20 my (mini)', '10 cm × 150 m', '276 g', '262 g', 'n.v.t.'],
        ['23 my (mini)', '10 cm × 250 m', '529 g', '503 g', 'n.v.t.']])
    s += P('<em>Berekend met een soortelijk gewicht van 0,92 g/cm³ voor LLDPE. Gewichten afgerond op hele grammen, exclusief koker.</em>')
    s += H2('Gratis calculator: handwikkelfolie controleren')
    s += P('Speciaal voor deze check hebben we een rekentool gemaakt. Vul het gewicht van je rol in, het gewicht van de koker en de opgegeven lengte, breedte en dikte. De calculator rekent uit hoeveel folie er op de rol hoort te zitten en of jouw rol binnen de tolerantie valt.')
    s += IFRAME(CALC_NL, 'Calculator: handwikkelfolie controleren op gewicht, dikte en lengte', CALC_H)
    s += H2('Wat betekent de uitkomst?')
    s += P('Geen enkele rol komt op de gram nauwkeurig uit. Folie wordt geproduceerd met een kleine marge in dikte, en een koker weegt nooit precies hetzelfde. Wij hanteren 5% als grens.')
    s += TABLE(['Afwijking', 'Bij 20 my, 50 cm × 300 m', 'Wat het betekent'], [
        ['<strong>Binnen 5%</strong>', '2.622 tot 2.898 g', 'In orde. Je krijgt wat de omschrijving belooft.'],
        ['<strong>Meer dan 5% te licht</strong>', 'Minder dan 2.622 g', 'Te weinig folie. De rol is dunner of korter dan opgegeven. Vraag je leverancier om uitleg.'],
        ['<strong>Meer dan 5% te zwaar</strong>', 'Meer dan 2.898 g', 'Meer folie dan opgegeven. Controleer of je het kokergewicht goed hebt ingevuld.']])
    s += H3('Te licht: hoeveel folie mis je dan echt?')
    s += P('De weegschaal vertelt je dat er folie ontbreekt, niet of dat in de dikte of in de lengte zit. Je kunt wel beide uitersten uitrekenen:')
    s += P('<strong>Werkelijke lengte (m)</strong> = nettogewicht (g) gedeeld door (dikte × breedte × 0,0092)<br><strong>Werkelijke dikte (my)</strong> = nettogewicht (g) gedeeld door (breedte × lengte × 0,0092)')
    s += P('Voorbeeld: een rol die verkocht wordt als 20 my, 50 cm × 300 m weegt netto 2.350 gram. Dan is de folie in werkelijkheid 17 my dik, of er zit maar 255 meter op de rol. In beide gevallen krijg je 15% minder folie dan waarvoor je betaalt.')
    s += H2('Stretchfolie eerlijk vergelijken: reken met de prijs per kilo')
    s += P('De prijs per rol zegt weinig zolang je niet weet hoeveel folie er op die rol zit. Deel de rolprijs daarom door het nettogewicht in kilo\'s. Dan zie je wat je per kilo folie betaalt, en dat getal kun je wel naast elkaar leggen.')
    s += COMPARE(('Rol A: lijkt duurder', ['Prijs per rol: € 6,00', 'Netto folie: 2.760 gram'], '€ 2,17 per kilo folie'),
                 ('Rol B: lijkt goedkoper', ['Prijs per rol: € 5,50', 'Netto folie: 2.350 gram'], '€ 2,34 per kilo folie'),
                 'Rekenvoorbeeld met fictieve prijzen, om het principe te laten zien.')
    s += P('Rol B is per stuk 50 cent goedkoper en per kilo folie toch 8% duurder. Bestel je een pallet per jaar, dan loopt dat verschil snel op.')
    s += P('Let bij offertes ook op deze drie punten:')
    s += P('<strong>Bruto of netto gewicht.</strong> Staat er een rolgewicht in de offerte, vraag dan of dat met of zonder koker is. Een zware koker telt mee op de weegschaal, maar wikkelt geen pallet.')
    s += P('<strong>Rollen per doos.</strong> Vergelijk de prijs per rol, niet per doos. Niet elke doos bevat 6 rollen.')
    s += P('<strong>Zelfde dikte, zelfde lengte.</strong> Een rol van 17 my is geen goedkoper alternatief voor 20 my, maar een ander product met 15% minder materiaal.')
    s += H2('Wat de weegschaal je niet vertelt')
    s += P('De weegtest laat zien hoeveel materiaal je krijgt. Over drie dingen zegt het gewicht niets:')
    s += P('<strong>De kwaliteit van de folie.</strong> Rek, doorprikweerstand en kleefkracht bepalen hoe stevig je pallet staat. Twee folies van hetzelfde gewicht kunnen daarin verschillen. Test een nieuwe folie daarom altijd op een echte pallet.')
    s += P('<strong>Gekleurde folie.</strong> Zwarte, witte en blauwe folie bevat pigment en kan daardoor een fractie zwaarder uitvallen dan transparante folie. In ons praktijkvoorbeeld met zwarte folie bleef dat verschil ruim binnen de 5%.')
    s += P('<strong>Folie met gaten of een open structuur.</strong> Voor gatenfolie en wikkelnet klopt de formule niet, omdat een deel van het oppervlak ontbreekt.')
    s += H2('Welke dikte handwikkelfolie heb je nodig?')
    s += P('Weet je eenmaal wat er op je huidige rol zit, dan is de volgende vraag of die dikte wel bij jouw pallets past. Te dunne folie scheurt of laat de lading schuiven. Te dikke folie kost je bij elke pallet onnodig materiaal. Als richtlijn:')
    s += TABLE(['Dikte', 'Palletlading tot circa', 'Toepassing'], [
        [lk(l['p17'], '17 my (Light)'), '500 kg', 'Lichte, gelijkmatig gestapelde dozen'], [lk(l['p20'], '20 my (Basic)'), '800 kg', 'De standaard voor de meeste pallets in magazijn en webshop'],
        [lk(l['p23'], '23 my (Power)'), '1.200 kg', 'Zware of onregelmatige ladingen'], [lk(l['p30'], '30 my (Ultra)'), 'Zwaarder dan 1.200 kg', 'Zeer zware ladingen en scherpe hoeken']])
    s += P(f'Wil je niet dat de inhoud van je pallet zichtbaar is, kies dan voor {A(l["zwart"], "zwarte handwikkelfolie")}. Wil je juist minder plastic per pallet gebruiken, bekijk dan de {A(l["nano"], "nano wikkelfolie")} van 12 my. Wikkel je meer dan een handvol pallets per dag, dan loont {A(l["machine"], "machinewikkelfolie")}. En met een {A(l["disp"], "handwikkelfolie dispenser")} span je de folie strakker aan, waardoor je per pallet minder meters nodig hebt.')
    s += H2('Veelgestelde vragen (FAQ)')
    for q, a in [
        ('Hoe controleer je of handwikkelfolie klopt?', 'Weeg de volle rol en trek het gewicht van de lege koker eraf. Vergelijk dat nettogewicht met het verwachte gewicht: dikte (my) × breedte (cm) × lengte (m) × 0,0092. Wijkt jouw rol minder dan 5% af, dan klopt de omschrijving.'),
        ('Hoeveel weegt een rol handwikkelfolie van 20 my?', 'Een rol van 20 my, 50 cm breed en 300 meter lang bevat 2.760 gram folie. Daar komt het gewicht van de koker nog bij. In ons voorbeeld was dat 227 gram, wat een totaalgewicht van ongeveer 3 kilo geeft.'),
        ('Wat betekent my bij stretchfolie?', 'My staat voor micrometer, ook wel micron genoemd. Eén my is een duizendste millimeter. Handwikkelfolie van 20 my is dus 0,02 mm dik.'),
        ('Hoeveel mag het gewicht van een rol afwijken?', 'Een afwijking tot 5% naar boven of beneden is normaal. Folie heeft een productiemarge in dikte en kokers verschillen onderling in gewicht. Bij 20 my, 50 cm × 300 m hoort het nettogewicht dus tussen 2.622 en 2.898 gram te liggen.'),
        ('Mijn rol is te licht, wat nu?', 'Leg je meting voor aan je leverancier, met het totaalgewicht, het kokergewicht en de opgegeven specificaties erbij. Reken daarna de prijs per kilo folie uit en vergelijk die met een alternatief. Stuur ons gerust je meting, dan rekenen we met je mee.'),
        ('Wat is het verschil tussen handwikkelfolie en stretchfolie?', 'Stretchfolie, wikkelfolie en rekfolie zijn verzamelnamen voor rekbare folie waarmee je een lading op een pallet vastzet. Handwikkelfolie is de variant op een handzame rol van 50 cm breed die je met de hand of met een dispenser aanbrengt. Machinewikkelfolie zit op grotere rollen voor een wikkelmachine.'),
        ('Hoeveel meter handwikkelfolie heb je nodig per pallet?', 'Dat hangt af van de hoogte van de pallet, het aantal slagen en hoe strak je wikkelt. Tel bij jouw pallets een keer na hoeveel pallets je uit één rol haalt en deel 300 meter door dat aantal. Dan weet je ook meteen wat de folie je per pallet kost.'),
        ('Is handwikkelfolie recyclebaar?', 'Ja. Handwikkelfolie is gemaakt van LLDPE en is recyclebaar als je het schoon en gescheiden inlevert bij het folie-afval. Wil je minder nieuw plastic gebruiken, kijk dan naar dunnere nano wikkelfolie of naar folie met gerecycled materiaal.')]:
        s += P(f'<strong>{q}</strong> {a}')
    s += H2('Handwikkelfolie kopen bij VerpakkingenXL')
    s += P('Bij ons krijg je wat er op de doos staat. Weeg onze rollen gerust na met de calculator hierboven. Kom je er niet uit of wijkt een rol af, dan hoor je van ons waar dat aan ligt.')
    s += CHECKS('Waarom ondernemers hun stretchfolie bij VerpakkingenXL halen', [
        'Handwikkelfolie van 12, 17, 20, 23 en 30 my uit eigen voorraad', 'Geleverd binnen 1-2 werkdagen', 'Staffelprijzen: hoe meer dozen, hoe lager je prijs per rol',
        'Gratis verzending vanaf € 99 excl. btw', 'Transparant, zwart, wit en blauw, plus mini rollen en dispensers', 'Persoonlijk advies van mensen die zelf ondernemen, sinds 2014'])
    s += CTA('Weten wat jouw folie per kilo kost?', 'Bekijk het assortiment en vergelijk zelf. Liever even sparren over de juiste dikte? Bel +31 53 573 84 56 tussen 09:00 en 17:00, of mail naar info@verpakkingenxl.be. Je hebt binnen 4 kantooruren antwoord.', l['cat'], 'Bekijk alle handwikkelfolie →')
    s += AUTHOR(None, '', 'Over de auteur', 'Jeroen Boeve, oprichter VerpakkingenXL',
                f'Jeroen bouwde vanuit Twente sinds 2014 een snelgroeiende webshop voor verpakkingsmateriaal, met inmiddels meer dan 100.000 klanten. Geen poeha, gewoon doen. {A(l["about"], "Lees meer over VerpakkingenXL")}')
    return s + '</div>'

def stretch_fr():
    l = L['fr']
    s = P('Vous comparez votre film étirable sur le prix par rouleau ? Vous comparez alors souvent des pommes et des poires. Deux rouleaux avec exactement la même description peuvent être très différents en réalité. Avec une balance et notre calculateur gratuit, vous vérifiez en deux minutes ce qu\'il y a vraiment sur votre rouleau.')
    s += WRAP + KORT('<strong>La réponse courte :</strong> vous contrôlez un film étirable manuel avec une balance. Pesez le rouleau plein, retirez le poids du mandrin vide et comparez le résultat avec le poids prévu par les spécifications. Ce poids attendu se calcule ainsi : <strong>épaisseur (µm) × largeur (cm) × longueur (m) × 0,0092</strong>. Un rouleau de 20 µm, 50 cm de large et 300 mètres de long doit donc contenir <strong>2 760 grammes de film</strong>. S\'il pèse plus de 5 % de moins, le film est plus fin ou plus court que promis.')
    s += P('Lors de nos échanges avec les clients, nous recevons souvent des questions sur le film étirable. Vous comparez notre prix avec ce que vous payez aujourd\'hui, et c\'est logique : vous ne voulez pas payer trop cher. Mais nous constatons souvent que la comparaison ne se fait pas à produit égal.')
    s += P('Dans cet article, vous découvrez comment mesurer vous-même en deux minutes ce qu\'il y a sur votre rouleau, comment lire le résultat et comment comparer ensuite deux offres de façon honnête. Pas besoin de calculer : plus bas, un calculateur gratuit le fait pour vous.')
    s += H2('Pourquoi deux rouleaux identiques sont pourtant différents')
    s += P('Sur le papier, tous les rouleaux de film étirable manuel de 20 µm se ressemblent : 20 µm d\'épaisseur, 300 mètres de long, 50 cm de large. Posez-les côte à côte et vous verrez une différence dans ce que vous recevez vraiment. Un rouleau a trois dimensions, et vous n\'en contrôlez qu\'une seule à l\'œil nu.')
    s += TABLE(['Dimension', 'Contrôlable vous-même ?', 'Comment'], [
        ['<strong>Largeur (cm)</strong>', 'Oui, directement', 'Avec un mètre ruban. Un écart se voit tout de suite.'],
        ['<strong>Épaisseur (µm)</strong>', 'Pas à l\'œil nu', 'La différence entre 17 et 20 µm est de 0,003 mm. Vous ne la voyez pas et ne la sentez pas.'],
        ['<strong>Longueur (m)</strong>', 'Pas à l\'œil nu', 'Personne ne déroule 300 mètres pour mesurer.']])
    s += P('C\'est donc sur l\'épaisseur et la longueur que ça coince. Un rouleau semble bon marché, mais il est plus fin ou plus court que ce que promet la description. Vous payez alors plus cher par mètre de film que prévu, et vous faites en plus davantage de tours par palette pour obtenir la même tenue.')
    s += BOX('<strong>µm</strong> signifie micromètre, aussi appelé micron (souvent noté « my » dans le secteur). Un micromètre est un millième de millimètre. Un film de 20 µm fait donc 0,02 mm d\'épaisseur.')
    s += H2('Contrôler un film étirable manuel en 4 étapes')
    s += P('Il vous faut seulement une balance et un mandrin vide. Une balance de cuisine ou une balance à colis précise au gramme jusqu\'à 5 kilos suffit.')
    s += P('<strong>Étape 1. Pesez le rouleau plein.</strong> Sans carton et sans dévidoir. Notez le poids en grammes.')
    s += P('<strong>Étape 2. Pesez un mandrin vide.</strong> Utilisez un mandrin du même fournisseur : les mandrins diffèrent en épaisseur de paroi et donc en poids. Gardez-en donc toujours un de votre carton précédent.')
    s += P('<strong>Étape 3. Retirez le mandrin du total.</strong> Ce qui reste est le poids net : le film que vous avez réellement acheté.')
    s += P('<strong>Étape 4. Comparez avec le poids attendu.</strong> Calculez-le avec la formule ci-dessous, cherchez-le dans le tableau ou utilisez le calculateur.')
    s += H2('La formule : combien doit peser un rouleau de film étirable ?')
    s += P('Le film étirable manuel est fabriqué en LLDPE, un type de polyéthylène d\'une masse volumique d\'environ 0,92 gramme par cm³. Si vous connaissez l\'épaisseur, la largeur et la longueur, vous connaissez le volume du film. Et donc aussi son poids.')
    s += FORMULA('Poids de film attendu (grammes) = épaisseur (µm) × largeur (cm) × longueur (m) × 0,0092')
    s += P('Exemple : 20 µm × 50 cm × 300 m × 0,0092 = <strong>2 760 grammes</strong>')
    s += H3('Un exemple concret')
    s += P('Nous avons pesé un rouleau de film étirable manuel noir de 20 µm, 300 mètres de long et 50 cm de large :')
    s += STEPS(['Poids total du rouleau : 2 977 grammes', 'Poids du mandrin vide : 227 grammes', 'Film net : 2 977 − 227 = 2 750 grammes', 'Attendu : 2 760 grammes. Écart : 10 grammes, soit 0,4 %'])
    s += P('Un écart de 0,4 % reste largement dans la tolérance. Ce rouleau contient ce que promet la description.')
    s += H2('Tableau : poids de film attendu par rouleau')
    s += P('Pas envie de calculer ? Voici le poids net attendu pour les rouleaux les plus courants, avec la limite basse sous laquelle un rouleau ne devrait pas descendre. Tous les poids sont hors mandrin.')
    s += TABLE(['Épaisseur', 'Largeur × longueur', 'Poids net attendu', 'Limite basse (−5 %)', 'Film par carton de 6'], [
        ['12 µm', '50 cm × 300 m', '1 656 g', '1 573 g', '9,9 kg'], [lk(l['p17'], '17 µm'), '50 cm × 300 m', '2 346 g', '2 229 g', '14,1 kg'],
        [lk(l['p20'], '20 µm'), '50 cm × 300 m', '2 760 g', '2 622 g', '16,6 kg'], [lk(l['p23'], '23 µm'), '50 cm × 300 m', '3 174 g', '3 015 g', '19,0 kg'],
        [lk(l['p30'], '30 µm'), '50 cm × 300 m', '4 140 g', '3 933 g', '24,8 kg'], ['20 µm (mini)', '10 cm × 150 m', '276 g', '262 g', 'n.a.'],
        ['23 µm (mini)', '10 cm × 250 m', '529 g', '503 g', 'n.a.']])
    s += P('<em>Calculé avec une masse volumique de 0,92 g/cm³ pour le LLDPE. Poids arrondis au gramme, hors mandrin.</em>')
    s += H2('Calculateur gratuit : contrôler votre film étirable manuel')
    s += P('Nous avons créé un outil de calcul spécialement pour ce contrôle. Indiquez le poids de votre rouleau, le poids du mandrin et la longueur, la largeur et l\'épaisseur annoncées. Le calculateur indique combien de film le rouleau devrait contenir et si votre rouleau reste dans la tolérance.')
    s += IFRAME('%%CALC_FR%%', 'Calculateur : contrôler le film étirable manuel sur le poids, l\'épaisseur et la longueur', CALC_H)
    s += H2('Que signifie le résultat ?')
    s += P('Aucun rouleau ne tombe juste au gramme près. Le film est produit avec une petite marge d\'épaisseur, et un mandrin ne pèse jamais exactement la même chose. Nous retenons 5 % comme limite.')
    s += TABLE(['Écart', 'Pour 20 µm, 50 cm × 300 m', 'Ce que cela signifie'], [
        ['<strong>Moins de 5 %</strong>', '2 622 à 2 898 g', 'Tout est en ordre. Vous recevez ce que promet la description.'],
        ['<strong>Plus de 5 % trop léger</strong>', 'Moins de 2 622 g', 'Trop peu de film. Le rouleau est plus fin ou plus court qu\'annoncé. Demandez une explication à votre fournisseur.'],
        ['<strong>Plus de 5 % trop lourd</strong>', 'Plus de 2 898 g', 'Plus de film qu\'annoncé. Vérifiez que vous avez bien indiqué le poids du mandrin.']])
    s += H3('Trop léger : combien de film vous manque-t-il vraiment ?')
    s += P('La balance vous dit qu\'il manque du film, pas si c\'est dans l\'épaisseur ou dans la longueur. Vous pouvez en revanche calculer les deux extrêmes :')
    s += P('<strong>Longueur réelle (m)</strong> = poids net (g) divisé par (épaisseur × largeur × 0,0092)<br><strong>Épaisseur réelle (µm)</strong> = poids net (g) divisé par (largeur × longueur × 0,0092)')
    s += P('Exemple : un rouleau vendu comme 20 µm, 50 cm × 300 m pèse 2 350 grammes net. Le film fait alors en réalité 17 µm, ou il n\'y a que 255 mètres sur le rouleau. Dans les deux cas, vous recevez 15 % de film en moins que ce que vous payez.')
    s += H2('Comparer honnêtement : calculez le prix au kilo')
    s += P('Le prix par rouleau ne dit pas grand-chose tant que vous ne savez pas combien de film il contient. Divisez donc le prix du rouleau par le poids net en kilos. Vous voyez alors ce que vous payez par kilo de film, et ce chiffre-là se compare.')
    s += COMPARE(('Rouleau A : semble plus cher', ['Prix par rouleau : 6,00 €', 'Film net : 2 760 grammes'], '2,17 € par kilo de film'),
                 ('Rouleau B : semble moins cher', ['Prix par rouleau : 5,50 €', 'Film net : 2 350 grammes'], '2,34 € par kilo de film'),
                 'Exemple avec des prix fictifs, pour illustrer le principe.')
    s += P('Le rouleau B coûte 50 centimes de moins à l\'unité, mais il est 8 % plus cher par kilo de film. Si vous commandez une palette par an, la différence grimpe vite.')
    s += P('Dans les devis, faites aussi attention à ces trois points :')
    s += P('<strong>Poids brut ou net.</strong> Si un poids de rouleau figure dans le devis, demandez s\'il s\'entend avec ou sans mandrin. Un mandrin lourd compte sur la balance, mais ne banderole aucune palette.')
    s += P('<strong>Rouleaux par carton.</strong> Comparez le prix par rouleau, pas par carton. Tous les cartons ne contiennent pas 6 rouleaux.')
    s += P('<strong>Même épaisseur, même longueur.</strong> Un rouleau de 17 µm n\'est pas une alternative moins chère au 20 µm, mais un autre produit avec 15 % de matière en moins.')
    s += H2('Ce que la balance ne vous dit pas')
    s += P('Le test de pesée montre combien de matière vous recevez. Sur trois points, le poids ne dit rien :')
    s += P('<strong>La qualité du film.</strong> L\'allongement, la résistance à la perforation et l\'adhérence déterminent la tenue de votre palette. Deux films de même poids peuvent différer sur ces points. Testez donc toujours un nouveau film sur une vraie palette.')
    s += P('<strong>Le film coloré.</strong> Le film noir, blanc ou bleu contient des pigments et peut donc peser un peu plus que le film transparent. Dans notre exemple avec du film noir, cet écart est resté largement sous les 5 %.')
    s += P('<strong>Le film perforé ou à structure ouverte.</strong> Pour le film perforé et le filet de banderolage, la formule ne fonctionne pas, car une partie de la surface manque.')
    s += H2('Quelle épaisseur de film étirable manuel vous faut-il ?')
    s += P('Une fois que vous savez ce que contient votre rouleau actuel, reste à savoir si cette épaisseur convient à vos palettes. Un film trop fin se déchire ou laisse glisser la charge. Un film trop épais vous coûte de la matière inutile à chaque palette. À titre indicatif :')
    s += TABLE(['Épaisseur', 'Charge par palette jusqu\'à environ', 'Utilisation'], [
        [lk(l['p17'], '17 µm (Light)'), '500 kg', 'Cartons légers, empilés régulièrement'], [lk(l['p20'], '20 µm (Basic)'), '800 kg', 'Le standard pour la plupart des palettes en entrepôt et e-commerce'],
        [lk(l['p23'], '23 µm (Power)'), '1 200 kg', 'Charges lourdes ou irrégulières'], [lk(l['p30'], '30 µm (Ultra)'), 'Plus de 1 200 kg', 'Charges très lourdes et angles vifs']])
    s += P(f'Vous ne voulez pas que le contenu de votre palette soit visible ? Choisissez le {A(l["zwart"], "film étirable manuel noir")}. Vous voulez au contraire utiliser moins de plastique par palette ? Regardez le {A(l["nano"], "film de banderolage nano")} de 12 µm. Si vous banderolez plus d\'une poignée de palettes par jour, le {A(l["machine"], "film étirable machine")} devient rentable. Et avec un {A(l["disp"], "dévidoir pour film étirable")}, vous tendez mieux le film et utilisez moins de mètres par palette.')
    s += H2('Questions fréquentes (FAQ)')
    for q, a in [
        ('Comment vérifier si un film étirable manuel est conforme ?', 'Pesez le rouleau plein et retirez le poids du mandrin vide. Comparez ce poids net avec le poids attendu : épaisseur (µm) × largeur (cm) × longueur (m) × 0,0092. Si votre rouleau s\'écarte de moins de 5 %, la description est correcte.'),
        ('Combien pèse un rouleau de film étirable manuel de 20 µm ?', 'Un rouleau de 20 µm, 50 cm de large et 300 mètres de long contient 2 760 grammes de film. Il faut y ajouter le poids du mandrin. Dans notre exemple, il pesait 227 grammes, soit un poids total d\'environ 3 kilos.'),
        ('Que signifie « my » ou µm pour le film étirable ?', 'Il s\'agit du micromètre, aussi appelé micron. Un micromètre est un millième de millimètre. Un film étirable manuel de 20 µm fait donc 0,02 mm d\'épaisseur.'),
        ('Quel écart de poids est acceptable ?', 'Un écart jusqu\'à 5 % vers le haut ou vers le bas est normal. Le film a une marge de production sur l\'épaisseur et les mandrins varient en poids. Pour 20 µm, 50 cm × 300 m, le poids net doit donc se situer entre 2 622 et 2 898 grammes.'),
        ('Mon rouleau est trop léger, que faire ?', 'Présentez votre mesure à votre fournisseur, avec le poids total, le poids du mandrin et les spécifications annoncées. Calculez ensuite le prix au kilo de film et comparez-le à une alternative. N\'hésitez pas à nous envoyer votre mesure, nous calculons avec vous.'),
        ('Quelle est la différence entre film étirable manuel et film étirable ?', 'Film étirable, film de banderolage et film stretch sont des noms génériques pour un film extensible qui maintient une charge sur une palette. Le film étirable manuel est la version sur un rouleau maniable de 50 cm de large, posée à la main ou avec un dévidoir. Le film étirable machine est sur des rouleaux plus grands pour une banderoleuse.'),
        ('Combien de mètres de film faut-il par palette ?', 'Cela dépend de la hauteur de la palette, du nombre de tours et de la tension. Comptez une fois combien de palettes vous faites avec un rouleau et divisez 300 mètres par ce nombre. Vous savez alors aussi ce que le film vous coûte par palette.'),
        ('Le film étirable manuel est-il recyclable ?', 'Oui. Il est fabriqué en LLDPE et se recycle s\'il est propre et trié avec les déchets de film plastique. Vous voulez utiliser moins de plastique neuf ? Regardez le film nano plus fin ou un film contenant de la matière recyclée.')]:
        s += P(f'<strong>{q}</strong> {a}')
    s += H2('Acheter du film étirable manuel chez VerpakkingenXL')
    s += P('Chez nous, vous recevez ce qui est indiqué sur le carton. N\'hésitez pas à peser nos rouleaux avec le calculateur ci-dessus. Un doute ou un rouleau qui s\'écarte ? Nous vous expliquons d\'où vient la différence.')
    s += CHECKS('Pourquoi les entrepreneurs achètent leur film étirable chez VerpakkingenXL', [
        'Film étirable manuel de 12, 17, 20, 23 et 30 µm en stock', 'Livré en 1 à 2 jours ouvrables', 'Prix dégressifs : plus vous prenez de cartons, plus le prix par rouleau baisse',
        'Livraison gratuite à partir de 99 € HTVA', 'Transparent, noir, blanc et bleu, plus mini-rouleaux et dévidoirs', 'Des conseils personnalisés par des entrepreneurs, depuis 2014'])
    s += CTA('Vous voulez savoir combien coûte votre film au kilo ?', 'Consultez la gamme et comparez vous-même. Besoin de conseils sur la bonne épaisseur ? Appelez le +31 53 573 84 56 entre 9h00 et 17h00, ou écrivez à info@verpakkingenxl.be. Vous recevez une réponse dans les 4 heures ouvrables.', l['cat'], 'Voir tout le film étirable manuel →')
    s += AUTHOR(None, '', 'À propos de l\'auteur', 'Jeroen Boeve, fondateur de VerpakkingenXL',
                f'Depuis 2014, Jeroen a bâti depuis la région de Twente une boutique en ligne d\'emballages en pleine croissance, qui compte aujourd\'hui plus de 100 000 clients. Pas de chichis, on agit. {A(l["about"], "En savoir plus sur VerpakkingenXL")}')
    return s + '</div>'

def stretch_de():
    l = L['de']
    s = P('Vergleichen Sie Stretchfolie anhand des Preises pro Rolle? Dann vergleichen Sie oft Äpfel mit Birnen. Zwei Rollen mit exakt derselben Beschreibung können sich in Wirklichkeit deutlich unterscheiden. Mit einer Waage und unserem kostenlosen Rechner prüfen Sie in zwei Minuten, was wirklich auf Ihrer Rolle ist.')
    s += WRAP + KORT('<strong>Die kurze Antwort:</strong> Handwickelfolie prüfen Sie mit einer Waage. Wiegen Sie die volle Rolle, ziehen Sie das Gewicht der leeren Hülse ab und vergleichen Sie das Ergebnis mit dem Gewicht, das laut Spezifikation drauf sein sollte. Dieses Sollgewicht berechnen Sie mit <strong>Dicke (my) × Breite (cm) × Länge (m) × 0,0092</strong>. Eine Rolle mit 20 my, 50 cm Breite und 300 Metern Länge sollte also <strong>2.760 Gramm Folie</strong> enthalten. Liegen Sie mehr als 5 % darunter, ist die Folie dünner oder kürzer als versprochen.')
    s += P('In Gesprächen mit Kunden bekommen wir regelmäßig Fragen zu Stretchfolie. Sie vergleichen unseren Preis mit dem, was Sie jetzt bezahlen, und das ist logisch: Niemand möchte zu viel bezahlen. Wir merken in diesen Gesprächen aber oft, dass nicht Gleiches mit Gleichem verglichen wird.')
    s += P('In diesem Artikel lesen Sie, wie Sie in zwei Minuten selbst nachmessen, was auf Ihrer Rolle ist, wie Sie das Ergebnis lesen und wie Sie danach zwei Angebote fair vergleichen. Rechnen müssen Sie nicht: Weiter unten finden Sie einen kostenlosen Rechner, der das für Sie übernimmt.')
    s += H2('Warum zwei gleiche Rollen trotzdem unterschiedlich sind')
    s += P('Auf dem Papier sehen alle Rollen Handwickelfolie mit 20 my gleich aus: 20 my dick, 300 Meter lang, 50 cm breit. Legt man sie nebeneinander, zeigt sich trotzdem ein Unterschied in dem, was man wirklich bekommt. Eine Rolle hat drei Maße, und nur eines davon prüfen Sie mit bloßem Auge.')
    s += TABLE(['Maß', 'Selbst prüfbar?', 'Wie'], [
        ['<strong>Breite (cm)</strong>', 'Ja, sofort', 'Maßband anlegen. Eine Abweichung fällt sofort auf.'],
        ['<strong>Dicke (my)</strong>', 'Nicht mit dem Auge', 'Der Unterschied zwischen 17 und 20 my beträgt 0,003 mm. Das sieht und fühlt man nicht.'],
        ['<strong>Länge (m)</strong>', 'Nicht mit dem Auge', 'Niemand wickelt 300 Meter ab, um nachzumessen.']])
    s += P('Genau bei Dicke und Länge geht es also schief. Eine Rolle wirkt günstig, ist aber dünner oder kürzer als in der Beschreibung versprochen. Dann zahlen Sie pro Meter Folie mehr als gedacht und wickeln pro Palette auch noch mehr Lagen, um dieselbe Stabilität zu erreichen.')
    s += BOX('<strong>My</strong> steht für Mikrometer, auch Mikron oder µm geschrieben. Ein my ist ein Tausendstel Millimeter. Folie mit 20 my ist also 0,02 mm dick.')
    s += H2('So prüfen Sie Handwickelfolie in 4 Schritten')
    s += P('Sie brauchen nur eine Waage und eine leere Hülse. Eine Küchen- oder Paketwaage, die bis 5 Kilo grammgenau wiegt, reicht aus.')
    s += P('<strong>Schritt 1. Wiegen Sie die volle Rolle.</strong> Ohne Karton und ohne Abroller. Notieren Sie das Gewicht in Gramm.')
    s += P('<strong>Schritt 2. Wiegen Sie eine leere Hülse.</strong> Nehmen Sie eine Hülse vom selben Lieferanten, denn Hülsen unterscheiden sich in der Wandstärke und damit im Gewicht. Heben Sie deshalb immer eine aus dem vorherigen Karton auf.')
    s += P('<strong>Schritt 3. Ziehen Sie die Hülse vom Gesamtgewicht ab.</strong> Was übrig bleibt, ist das Nettogewicht: die Folie, die Sie wirklich gekauft haben.')
    s += P('<strong>Schritt 4. Vergleichen Sie mit dem Sollgewicht.</strong> Berechnen Sie es mit der Formel unten, schlagen Sie es in der Tabelle nach oder nutzen Sie den Rechner.')
    s += H2('Die Formel: Wie viel sollte eine Rolle Stretchfolie wiegen?')
    s += P('Handwickelfolie besteht aus LLDPE, einer Polyethylen-Art mit einer Dichte von etwa 0,92 Gramm pro cm³. Kennen Sie Dicke, Breite und Länge, kennen Sie das Volumen der Folie. Und damit auch das Gewicht.')
    s += FORMULA('Sollgewicht Folie (Gramm) = Dicke (my) × Breite (cm) × Länge (m) × 0,0092')
    s += P('Beispiel: 20 my × 50 cm × 300 m × 0,0092 = <strong>2.760 Gramm</strong>')
    s += H3('Ein Rechenbeispiel aus der Praxis')
    s += P('Wir haben eine Rolle schwarze Handwickelfolie mit 20 my, 300 Metern Länge und 50 cm Breite gewogen:')
    s += STEPS(['Gesamtgewicht der Rolle: 2.977 Gramm', 'Gewicht der leeren Hülse: 227 Gramm', 'Netto Folie: 2.977 − 227 = 2.750 Gramm', 'Soll: 2.760 Gramm. Abweichung: 10 Gramm, also 0,4 %'])
    s += P('Eine Abweichung von 0,4 % liegt deutlich innerhalb der Toleranz. Diese Rolle enthält, was die Beschreibung verspricht.')
    s += H2('Tabelle: Sollgewicht Folie pro Rolle')
    s += P('Keine Lust zu rechnen? Hier sehen Sie das erwartete Nettogewicht der gängigsten Rollen, mit der Untergrenze, unter die eine Rolle nicht fallen sollte. Alle Gewichte ohne Hülse.')
    s += TABLE(['Dicke', 'Breite × Länge', 'Erwartetes Nettogewicht', 'Untergrenze (−5 %)', 'Folie pro Karton à 6'], [
        ['12 my', '50 cm × 300 m', '1.656 g', '1.573 g', '9,9 kg'], [lk(l['p17'], '17 my'), '50 cm × 300 m', '2.346 g', '2.229 g', '14,1 kg'],
        [lk(l['p20'], '20 my'), '50 cm × 300 m', '2.760 g', '2.622 g', '16,6 kg'], [lk(l['p23'], '23 my'), '50 cm × 300 m', '3.174 g', '3.015 g', '19,0 kg'],
        [lk(l['p30'], '30 my'), '50 cm × 300 m', '4.140 g', '3.933 g', '24,8 kg'], ['20 my (Mini)', '10 cm × 150 m', '276 g', '262 g', 'entfällt'],
        ['23 my (Mini)', '10 cm × 250 m', '529 g', '503 g', 'entfällt']])
    s += P('<em>Berechnet mit einer Dichte von 0,92 g/cm³ für LLDPE. Gewichte auf ganze Gramm gerundet, ohne Hülse.</em>')
    s += H2('Kostenloser Rechner: Handwickelfolie prüfen')
    s += P('Speziell für diesen Check haben wir ein Rechentool entwickelt. Geben Sie das Gewicht Ihrer Rolle, das Gewicht der Hülse und die angegebene Länge, Breite und Dicke ein. Der Rechner zeigt, wie viel Folie auf der Rolle sein sollte und ob Ihre Rolle innerhalb der Toleranz liegt.')
    s += IFRAME('%%CALC_DE%%', 'Rechner: Handwickelfolie auf Gewicht, Dicke und Länge prüfen', CALC_H)
    s += H2('Was bedeutet das Ergebnis?')
    s += P('Keine Rolle stimmt aufs Gramm genau. Folie wird mit einer kleinen Toleranz in der Dicke produziert, und eine Hülse wiegt nie exakt gleich viel. Wir setzen 5 % als Grenze an.')
    s += TABLE(['Abweichung', 'Bei 20 my, 50 cm × 300 m', 'Was das bedeutet'], [
        ['<strong>Innerhalb von 5 %</strong>', '2.622 bis 2.898 g', 'In Ordnung. Sie bekommen, was die Beschreibung verspricht.'],
        ['<strong>Mehr als 5 % zu leicht</strong>', 'Weniger als 2.622 g', 'Zu wenig Folie. Die Rolle ist dünner oder kürzer als angegeben. Fragen Sie Ihren Lieferanten nach einer Erklärung.'],
        ['<strong>Mehr als 5 % zu schwer</strong>', 'Mehr als 2.898 g', 'Mehr Folie als angegeben. Prüfen Sie, ob Sie das Hülsengewicht richtig eingegeben haben.']])
    s += H3('Zu leicht: Wie viel Folie fehlt Ihnen wirklich?')
    s += P('Die Waage sagt Ihnen, dass Folie fehlt, nicht ob das an der Dicke oder an der Länge liegt. Sie können aber beide Extreme berechnen:')
    s += P('<strong>Tatsächliche Länge (m)</strong> = Nettogewicht (g) geteilt durch (Dicke × Breite × 0,0092)<br><strong>Tatsächliche Dicke (my)</strong> = Nettogewicht (g) geteilt durch (Breite × Länge × 0,0092)')
    s += P('Beispiel: Eine Rolle, die als 20 my, 50 cm × 300 m verkauft wird, wiegt netto 2.350 Gramm. Dann ist die Folie in Wirklichkeit 17 my dick, oder es sind nur 255 Meter auf der Rolle. In beiden Fällen bekommen Sie 15 % weniger Folie, als Sie bezahlen.')
    s += H2('Stretchfolie fair vergleichen: Rechnen Sie mit dem Kilopreis')
    s += P('Der Preis pro Rolle sagt wenig, solange Sie nicht wissen, wie viel Folie auf der Rolle ist. Teilen Sie den Rollenpreis daher durch das Nettogewicht in Kilo. Dann sehen Sie, was Sie pro Kilo Folie bezahlen, und diese Zahl lässt sich vergleichen.')
    s += COMPARE(('Rolle A: wirkt teurer', ['Preis pro Rolle: 6,00 €', 'Netto Folie: 2.760 Gramm'], '2,17 € pro Kilo Folie'),
                 ('Rolle B: wirkt günstiger', ['Preis pro Rolle: 5,50 €', 'Netto Folie: 2.350 Gramm'], '2,34 € pro Kilo Folie'),
                 'Rechenbeispiel mit fiktiven Preisen, um das Prinzip zu zeigen.')
    s += P('Rolle B ist pro Stück 50 Cent günstiger und pro Kilo Folie trotzdem 8 % teurer. Bestellen Sie eine Palette pro Jahr, summiert sich dieser Unterschied schnell.')
    s += P('Achten Sie bei Angeboten auch auf diese drei Punkte:')
    s += P('<strong>Brutto- oder Nettogewicht.</strong> Steht ein Rollengewicht im Angebot, fragen Sie, ob es mit oder ohne Hülse gilt. Eine schwere Hülse zählt auf der Waage mit, wickelt aber keine Palette.')
    s += P('<strong>Rollen pro Karton.</strong> Vergleichen Sie den Preis pro Rolle, nicht pro Karton. Nicht jeder Karton enthält 6 Rollen.')
    s += P('<strong>Gleiche Dicke, gleiche Länge.</strong> Eine Rolle mit 17 my ist keine günstigere Alternative zu 20 my, sondern ein anderes Produkt mit 15 % weniger Material.')
    s += H2('Was die Waage Ihnen nicht verrät')
    s += P('Der Wiegetest zeigt, wie viel Material Sie bekommen. Über drei Dinge sagt das Gewicht nichts aus:')
    s += P('<strong>Die Qualität der Folie.</strong> Dehnung, Durchstoßfestigkeit und Haftung bestimmen, wie stabil Ihre Palette steht. Zwei Folien mit gleichem Gewicht können sich darin unterscheiden. Testen Sie eine neue Folie daher immer an einer echten Palette.')
    s += P('<strong>Farbige Folie.</strong> Schwarze, weiße und blaue Folie enthält Pigmente und kann dadurch etwas schwerer ausfallen als transparente Folie. In unserem Praxisbeispiel mit schwarzer Folie blieb dieser Unterschied deutlich unter 5 %.')
    s += P('<strong>Folie mit Löchern oder offener Struktur.</strong> Für Lochfolie und Wickelnetz stimmt die Formel nicht, weil ein Teil der Fläche fehlt.')
    s += H2('Welche Dicke Handwickelfolie brauchen Sie?')
    s += P('Wissen Sie, was auf Ihrer aktuellen Rolle ist, stellt sich die nächste Frage: Passt diese Dicke zu Ihren Paletten? Zu dünne Folie reißt oder lässt die Ladung rutschen. Zu dicke Folie kostet Sie bei jeder Palette unnötig Material. Als Richtwert:')
    s += TABLE(['Dicke', 'Palettenlast bis ca.', 'Einsatz'], [
        [lk(l['p17'], '17 my (Light)'), '500 kg', 'Leichte, gleichmäßig gestapelte Kartons'], [lk(l['p20'], '20 my (Basic)'), '800 kg', 'Der Standard für die meisten Paletten in Lager und Onlineshop'],
        [lk(l['p23'], '23 my (Power)'), '1.200 kg', 'Schwere oder unregelmäßige Ladungen'], [lk(l['p30'], '30 my (Ultra)'), 'Über 1.200 kg', 'Sehr schwere Ladungen und scharfe Kanten']])
    s += P(f'Soll der Inhalt Ihrer Palette nicht sichtbar sein, wählen Sie {A(l["zwart"], "schwarze Handwickelfolie")}. Möchten Sie weniger Kunststoff pro Palette verbrauchen, sehen Sie sich die {A(l["nano"], "Nano-Wickelfolie")} mit 12 my an. Wickeln Sie mehr als eine Handvoll Paletten pro Tag, lohnt sich {A(l["machine"], "Maschinenwickelfolie")}. Und mit einem {A(l["disp"], "Handwickelfolien-Abroller")} spannen Sie die Folie straffer und brauchen pro Palette weniger Meter.')
    s += H2('Häufige Fragen (FAQ)')
    for q, a in [
        ('Wie prüfen Sie, ob Handwickelfolie stimmt?', 'Wiegen Sie die volle Rolle und ziehen Sie das Gewicht der leeren Hülse ab. Vergleichen Sie dieses Nettogewicht mit dem Sollgewicht: Dicke (my) × Breite (cm) × Länge (m) × 0,0092. Weicht Ihre Rolle weniger als 5 % ab, stimmt die Beschreibung.'),
        ('Wie viel wiegt eine Rolle Handwickelfolie mit 20 my?', 'Eine Rolle mit 20 my, 50 cm Breite und 300 Metern Länge enthält 2.760 Gramm Folie. Dazu kommt das Gewicht der Hülse. In unserem Beispiel waren das 227 Gramm, also ein Gesamtgewicht von etwa 3 Kilo.'),
        ('Was bedeutet my bei Stretchfolie?', 'My steht für Mikrometer, auch Mikron genannt. Ein my ist ein Tausendstel Millimeter. Handwickelfolie mit 20 my ist also 0,02 mm dick.'),
        ('Wie stark darf das Gewicht einer Rolle abweichen?', 'Eine Abweichung bis 5 % nach oben oder unten ist normal. Folie hat eine Produktionstoleranz in der Dicke, und Hülsen unterscheiden sich im Gewicht. Bei 20 my, 50 cm × 300 m sollte das Nettogewicht also zwischen 2.622 und 2.898 Gramm liegen.'),
        ('Meine Rolle ist zu leicht, was nun?', 'Legen Sie Ihre Messung Ihrem Lieferanten vor, mit Gesamtgewicht, Hülsengewicht und den angegebenen Spezifikationen. Berechnen Sie danach den Kilopreis der Folie und vergleichen Sie ihn mit einer Alternative. Schicken Sie uns gern Ihre Messung, wir rechnen mit.'),
        ('Was ist der Unterschied zwischen Handwickelfolie und Stretchfolie?', 'Stretchfolie, Wickelfolie und Dehnfolie sind Sammelbegriffe für dehnbare Folie, mit der Sie eine Ladung auf einer Palette sichern. Handwickelfolie ist die Variante auf einer handlichen Rolle mit 50 cm Breite, die Sie von Hand oder mit einem Abroller anbringen. Maschinenwickelfolie gibt es auf größeren Rollen für eine Wickelmaschine.'),
        ('Wie viele Meter Handwickelfolie brauchen Sie pro Palette?', 'Das hängt von der Palettenhöhe, der Anzahl der Lagen und davon ab, wie straff Sie wickeln. Zählen Sie einmal, wie viele Paletten Sie mit einer Rolle schaffen, und teilen Sie 300 Meter durch diese Zahl. Dann wissen Sie auch gleich, was die Folie pro Palette kostet.'),
        ('Ist Handwickelfolie recycelbar?', 'Ja. Handwickelfolie besteht aus LLDPE und ist recycelbar, wenn Sie sie sauber und getrennt mit dem Folienabfall entsorgen. Möchten Sie weniger neuen Kunststoff verbrauchen, sehen Sie sich dünnere Nano-Wickelfolie oder Folie mit Recyclinganteil an.')]:
        s += P(f'<strong>{q}</strong> {a}')
    s += H2('Handwickelfolie kaufen bei VerpackungenXL')
    s += P('Bei uns bekommen Sie, was auf dem Karton steht. Wiegen Sie unsere Rollen gern mit dem Rechner oben nach. Kommen Sie nicht weiter oder weicht eine Rolle ab, erklären wir Ihnen, woran das liegt.')
    s += CHECKS('Warum Unternehmer ihre Stretchfolie bei VerpackungenXL kaufen', [
        'Handwickelfolie mit 12, 17, 20, 23 und 30 my ab Lager', 'Lieferung in 1-2 Werktagen', 'Staffelpreise: je mehr Kartons, desto niedriger Ihr Preis pro Rolle',
        'Kostenloser Versand ab 99 €', 'Transparent, schwarz, weiß und blau, dazu Minirollen und Abroller', 'Persönliche Beratung von Menschen, die selbst Unternehmer sind, seit 2014'])
    s += CTA('Wissen, was Ihre Folie pro Kilo kostet?', 'Sehen Sie sich das Sortiment an und vergleichen Sie selbst. Lieber kurz über die richtige Dicke sprechen? Rufen Sie uns an unter +31 53 573 84 56 zwischen 9:00 und 17:00 Uhr oder schreiben Sie an info@verpackungenxl.de. Sie erhalten innerhalb von 4 Geschäftsstunden eine Antwort.', l['cat'], 'Alle Handwickelfolien ansehen →')
    s += AUTHOR(None, '', 'Über den Autor', 'Jeroen Boeve, Gründer von VerpakkingenXL',
                f'Jeroen hat seit 2014 aus Twente heraus einen schnell wachsenden Onlineshop für Verpackungsmaterial aufgebaut, mit inzwischen mehr als 100.000 Kunden. Kein Schnickschnack, einfach machen. {A(l["about"], "Mehr über VerpackungenXL")}')
    return s + '</div>'

# ---------------------------------------------------------------- INTERVIEW
def interview(lang):
    if lang == 'be':
        T = dict(lead='Bij VerpakkingenXL staan we nooit stil. Om onze groei van meer dan 100.000 klanten te faciliteren en onze belofte van snelheid en scherpe prijzen waar te maken, is een ijzersterk inkoopbeleid essentieel. Sinds kort is Roderick Klaver officieel toegetreden als mede-eigenaar. In dit interview vertelt hij over zijn reis van stagiair naar ondernemer en hoe hij de wereldwijde markt afspeurt naar de beste fabrieken voor jouw verpakkingen.',
          h1='Interview: hoe Roderick Klaver zorgt voor de scherpste deal en slimste maatwerkoplossingen',
          qa=[('Roderick, gefeliciteerd! Hoe voelt het om nu mede-eigenaar te zijn?', ['Dank je! Het voelt eigenlijk heel natuurlijk. Ik ben vier jaar geleden binnengekomen als stagiair en heb sindsdien alle facetten van het bedrijf gezien. De samenwerking met Jeroen en het team verloopt zo goed dat dit een logische volgende stap is om de continuïteit van VerpakkingenXL te waarborgen.']),
              ('Jij gaat over de inkoop. Wat is jouw geheim?', ['Het draait om het vinden van de perfecte match tussen product en fabriek. Ik ben dagelijks bezig met het schakelen met producenten wereldwijd. Of het nu gaat om standaard voorraad of complexe producties: ik weet precies welke fabriek de juiste kwaliteit levert tegen de beste prijs. Dat direct schakelen zonder tussenpersonen zorgt ervoor dat onze klanten onderaan de streep minder betalen.']),
              ("Wat betekent jouw expertise specifiek voor klanten die 'dozen op maat' zoeken?", ['Dat is waar we echt het verschil maken. Maatwerk is vaak een puzzel van levertijd, materiaalgebruik en prijs. Doordat ik een netwerk van gespecialiseerde fabrieken heb opgebouwd, kunnen we producties heel slim wegzetten. Zo realiseren we maximale efficiëntie. We kijken niet alleen naar de doos zelf, maar naar het hele proces:', 'LIST']),
              ('Waarom past de Twentse aanpak zo goed bij jou?', ['Net als Jeroen hou ik van nuchterheid. We doen niet aan ingewikkelde contracten of vage beloftes. Als een klant een logistiek probleem heeft, lossen we het op. Punt. Die snelheid en eerlijkheid is waarom klanten bij ons blijven. We groeien hard, maar we blijven die persoonlijke partner die gewoon de telefoon opneemt.'])],
          lst=[('Prijsoptimalisatie', 'de juiste productiehoeveelheid bij de juiste machine.'), ('Snelheid', 'korte lijnen met fabrikanten in binnen- en buitenland.'), ('Duurzaamheid', "geen 'gebakken lucht' verzenden door exact passende verpakkingen.")],
          adv_t='Advies van Roderick', adv='Wil je weten of jouw huidige verpakkingen efficiënter ingekocht kunnen worden? Of ben je benieuwd naar de mogelijkheden van maatwerk om jouw verzendkosten te verlagen? Ik kijk graag mee naar jouw inkoopproces om te zien waar we direct winst kunnen behalen. Mail naar info@verpakkingenxl.be of bel +31 53 573 84 56.',
          btn='Naar dozen op maat →', href='https://www.verpakkingenxl.be/nl/dozen/doos-op-maat/', cta_t='Bekijk direct onze maatwerkoplossingen',
          ah='Over de auteur', an='Roderick Klaver, mede-eigenaar VerpakkingenXL', at='Roderick is specialist in wereldwijde inkoop en logistieke optimalisatie. Met zijn scherpe blik op de markt zorgt hij voor de beste deals en meest efficiënte maatwerkoplossingen voor ondernemers. Elke week volgt hij de %%GP%%.',
          gp='grondstofprijzen van kunststof')
    elif lang == 'fr':
        T = dict(lead='Chez VerpakkingenXL, nous ne restons jamais immobiles. Pour accompagner notre croissance à plus de 100 000 clients et tenir notre promesse de rapidité et de prix serrés, une politique d\'achat solide est indispensable. Roderick Klaver est récemment devenu officiellement copropriétaire. Dans cette interview, il raconte son parcours de stagiaire à entrepreneur et comment il parcourt le marché mondial à la recherche des meilleures usines pour vos emballages.',
          h1='Interview : comment Roderick Klaver décroche les meilleurs prix et les solutions sur mesure les plus malignes',
          qa=[('Roderick, félicitations ! Qu\'est-ce que ça fait d\'être copropriétaire ?', ['Merci ! En fait, ça me semble très naturel. Je suis arrivé il y a quatre ans comme stagiaire et j\'ai vu depuis toutes les facettes de l\'entreprise. La collaboration avec Jeroen et l\'équipe se passe si bien que c\'est une étape logique pour assurer la continuité de VerpakkingenXL.']),
              ('Vous êtes responsable des achats. Quel est votre secret ?', ['Tout tourne autour de la bonne combinaison entre produit et usine. Je suis chaque jour en contact avec des producteurs du monde entier. Qu\'il s\'agisse de stock standard ou de productions complexes : je sais exactement quelle usine fournit la bonne qualité au meilleur prix. Ce contact direct, sans intermédiaires, fait qu\'au final nos clients paient moins.']),
              ('Que signifie votre expertise pour les clients qui cherchent des boîtes sur mesure ?', ['C\'est là que nous faisons vraiment la différence. Le sur-mesure est souvent un puzzle entre délai, consommation de matière et prix. Grâce au réseau d\'usines spécialisées que j\'ai construit, nous pouvons placer les productions de façon très intelligente. Nous obtenons ainsi une efficacité maximale. Nous ne regardons pas seulement la boîte, mais tout le processus :', 'LIST']),
              ('Pourquoi l\'approche de Twente vous correspond-elle si bien ?', ['Comme Jeroen, j\'aime le pragmatisme. Chez nous, pas de contrats compliqués ni de promesses vagues. Si un client a un problème logistique, nous le résolvons. Point. Cette rapidité et cette honnêteté expliquent pourquoi nos clients restent. Nous grandissons vite, mais nous restons ce partenaire personnel qui décroche simplement le téléphone.'])],
          lst=[('Optimisation du prix', 'la bonne quantité de production sur la bonne machine.'), ('Rapidité', 'des contacts directs avec les fabricants, aux Pays-Bas et à l\'étranger.'), ('Durabilité', 'pas d\'air expédié inutilement grâce à des emballages parfaitement ajustés.')],
          adv_t='Le conseil de Roderick', adv='Vous voulez savoir si vos emballages actuels peuvent être achetés plus efficacement ? Ou vous êtes curieux des possibilités du sur-mesure pour réduire vos frais d\'envoi ? Je regarde volontiers votre processus d\'achat pour voir où nous pouvons gagner tout de suite. Écrivez à info@verpakkingenxl.be ou appelez le +31 53 573 84 56.',
          btn='Voir les boîtes sur mesure →', href='https://www.verpakkingenxl.be/fr/boites/boite-sur-mesure/', cta_t='Découvrez nos solutions sur mesure',
          ah='À propos de l\'auteur', an='Roderick Klaver, copropriétaire de VerpakkingenXL', at='Roderick est spécialiste des achats internationaux et de l\'optimisation logistique. Avec son regard aiguisé sur le marché, il décroche les meilleurs prix et les solutions sur mesure les plus efficaces pour les entrepreneurs. Chaque semaine, il suit les %%GP%%.',
          gp='prix des matières premières plastiques')
    else:
        T = dict(lead='Bei VerpackungenXL stehen wir nie still. Um unser Wachstum auf mehr als 100.000 Kunden zu tragen und unser Versprechen von Schnelligkeit und scharfen Preisen einzuhalten, ist eine starke Einkaufspolitik unverzichtbar. Seit Kurzem ist Roderick Klaver offiziell Miteigentümer. In diesem Interview erzählt er von seinem Weg vom Praktikanten zum Unternehmer und wie er den Weltmarkt nach den besten Fabriken für Ihre Verpackungen durchsucht.',
          h1='Interview: Wie Roderick Klaver für den schärfsten Preis und die cleversten Maßlösungen sorgt',
          qa=[('Roderick, herzlichen Glückwunsch! Wie fühlt es sich an, jetzt Miteigentümer zu sein?', ['Danke! Es fühlt sich eigentlich ganz natürlich an. Ich bin vor vier Jahren als Praktikant eingestiegen und habe seitdem alle Bereiche des Unternehmens kennengelernt. Die Zusammenarbeit mit Jeroen und dem Team läuft so gut, dass dies ein logischer nächster Schritt ist, um die Kontinuität von VerpackungenXL zu sichern.']),
              ('Sie sind für den Einkauf zuständig. Was ist Ihr Geheimnis?', ['Es geht darum, die perfekte Kombination aus Produkt und Fabrik zu finden. Ich stehe täglich mit Herstellern weltweit in Kontakt. Ob Standardware ab Lager oder komplexe Produktionen: Ich weiß genau, welche Fabrik die richtige Qualität zum besten Preis liefert. Dieser direkte Draht ohne Zwischenhändler sorgt dafür, dass unsere Kunden unterm Strich weniger bezahlen.']),
              ('Was bedeutet Ihre Erfahrung für Kunden, die Kartons nach Maß suchen?', ['Genau da machen wir den Unterschied. Maßanfertigung ist oft ein Puzzle aus Lieferzeit, Materialeinsatz und Preis. Weil ich ein Netzwerk spezialisierter Fabriken aufgebaut habe, können wir Produktionen sehr geschickt platzieren. So erreichen wir maximale Effizienz. Wir schauen nicht nur auf den Karton selbst, sondern auf den ganzen Prozess:', 'LIST']),
              ('Warum passt die Art aus Twente so gut zu Ihnen?', ['Wie Jeroen mag ich es bodenständig. Bei uns gibt es keine komplizierten Verträge und keine vagen Versprechen. Hat ein Kunde ein logistisches Problem, lösen wir es. Punkt. Diese Schnelligkeit und Ehrlichkeit sind der Grund, warum Kunden bei uns bleiben. Wir wachsen stark, bleiben aber der persönliche Partner, der einfach ans Telefon geht.'])],
          lst=[('Preisoptimierung', 'die richtige Produktionsmenge auf der richtigen Maschine.'), ('Schnelligkeit', 'kurze Wege zu Herstellern im In- und Ausland.'), ('Nachhaltigkeit', 'keine Luft verschicken dank exakt passender Verpackungen.')],
          adv_t='Rodericks Tipp', adv='Möchten Sie wissen, ob Ihre aktuellen Verpackungen günstiger eingekauft werden können? Oder interessieren Sie die Möglichkeiten von Maßanfertigungen, um Ihre Versandkosten zu senken? Ich schaue mir gern Ihren Einkaufsprozess an, um zu sehen, wo wir direkt sparen können. Schreiben Sie an info@verpackungenxl.de oder rufen Sie uns an unter +31 53 573 84 56.',
          btn='Zu Kartons nach Maß →', href='https://www.verpackungenxl.de/kartonagen/karton-nach-mass/', cta_t='Entdecken Sie unsere Maßlösungen',
          ah='Über den Autor', an='Roderick Klaver, Miteigentümer von VerpackungenXL', at='Roderick ist Spezialist für weltweiten Einkauf und logistische Optimierung. Mit seinem scharfen Blick auf den Markt sorgt er für die besten Preise und die effizientesten Maßlösungen für Unternehmer. Jede Woche verfolgt er die %%GP%%.',
          gp='Rohstoffpreise für Kunststoff')
    s = P(T['lead']) + WRAP
    s += H2(T['h1'])
    for q, parts in T['qa']:
        s += H3(q)
        for pt in parts:
            if pt == 'LIST':
                s += '<ul style="font-family: inherit; margin: 0 0 15px 0; padding-left: 20px;">' + ''.join(f'<li style="margin-bottom: 6px;"><strong>{a}:</strong> {b}</li>' for a, b in T['lst']) + '</ul>'
            else:
                s += P(pt)
    s += BOX(f'<strong>{T["adv_t"]}</strong><br>{T["adv"]}')
    s += CTA(T['cta_t'], '', T['href'], T['btn']).replace('<p style="font-family: inherit; margin: 0 0 15px 0;"></p>', '')
    at = T['at'].replace('%%GP%%', f'<a href="%%GP_URL%%">{T["gp"]}</a>')
    s += AUTHOR(RODERICK, 'Roderick Klaver', T['ah'], T['an'], at)
    return s + '</div>'

write('stretch_be.html', stretch_be())
write('stretch_fr.html', stretch_fr())
write('stretch_de.html', stretch_de())
for lg in ('be', 'fr', 'de'):
    write(f'interview_{lg}.html', interview(lg))
print('ok')
