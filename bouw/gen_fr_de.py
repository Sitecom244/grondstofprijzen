# LET OP (16 nov 2026): artikel_template_fr.html en _de.html zijn daarna met de hand aangevuld (links naar stretchfolie-artikel en interview). Niet opnieuw draaien zonder die links over te nemen.
"""Genereert artikel_template_fr.html en artikel_template_de.html met dezelfde inline-opmaak als het NL-artikel."""
H2 = '<h2 style="font-family: inherit; font-size: 25px; line-height: 1.3; margin: 35px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #0b99bc;">{}</h2>'
H3 = '<h3 style="font-family: inherit; font-size: 20px; line-height: 1.3; margin: 25px 0 10px 0;">{}</h3>'
P = '<p style="font-family: inherit;">{}</p>'
A = '<a style="color: #0b99bc; font-weight: bold;" href="{}">{}</a>'
AL = '<a style="color: #0b99bc;" href="{}">{}</a>'
def UL(items):
    return '<ul style="font-family: inherit; margin: 0 0 15px 0; padding-left: 20px;">' + ''.join('<li style="margin-bottom: 6px;">' + i + '</li>' for i in items) + '</ul>'
def B(t): return '<strong>' + t + '</strong>'
def IFR(src, title, h, style_h):
    return ('<p style="font-family: inherit;"><iframe style="border: 1px solid #dddddd; border-radius: 5px; width: 100%; height: ' + style_h + ';" title="' + title +
            '" src="' + src + '" width="100%" height="' + str(h) + '" loading="lazy"></iframe></p>')
G_H = 'clamp(1080px, calc(1670px - 76vw), 1400px)'
C_H = 'clamp(560px, calc(1420px - 75vw), 1160px)'

def table(head, rows):
    h = '<div style="overflow-x: auto; margin: 0 0 20px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 15px;"><thead><tr style="background: #0b99bc; color: #ffffff;">'
    h += ''.join('<th style="padding: 10px; text-align: left;">' + c + '</th>' for c in head) + '</tr></thead><tbody>'
    for i, r in enumerate(rows):
        bg = ' background: #f9f9f9;' if i % 2 else ''
        h += '<tr style="border-bottom: 1px solid #dddddd;' + bg + '">' + ''.join('<td style="padding: 10px;">' + c + '</td>' for c in r) + '</tr>'
    return h + '</tbody></table></div>'

def usp(title, items):
    h = '<div style="background: #f9f9f9; border-radius: 5px; padding: 15px 20px; margin: 25px 0 0 0;"><p style="font-family: inherit; margin: 0 0 8px 0;"><strong>' + title + '</strong></p>'
    for k, it in enumerate(items):
        m = '0' if k == len(items) - 1 else '0 0 6px 0'
        h += '<p style="font-family: inherit; margin: ' + m + ';"><span style="color: #0b99bc; font-weight: bold;">✓</span> ' + it + '</p>'
    return h + '</div>'

def cta(title, text, url, btn):
    return ('<div style="background: #0b99bc; color: #ffffff; padding: 20px; border-radius: 5px; margin: 25px 0; text-align: center;"><p style="font-family: inherit; margin: 0 0 10px 0; font-size: 19px;"><strong>' + title +
            '</strong></p><p style="font-family: inherit; margin: 0 0 15px 0;">' + text + '</p><p style="font-family: inherit; margin: 0;"><a style="display: inline-block; background: #ffffff; color: #0b99bc; padding: 12px 24px; border-radius: 5px; text-decoration: none; font-weight: bold;" href="' + url + '">' + btn + '</a></p></div>')

def author(head, role, text):
    return ('<div style="display: flex; flex-wrap: wrap; gap: 25px; align-items: center; border-top: 1px solid #f0f0f0; padding-top: 30px; margin-top: 30px;"><div style="flex: 0 0 120px;"><img style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #0b99bc;" src="https://cdn.webshopapp.com/shops/293467/files/495011501/roderick-klein.jpg" alt="Roderick Klaver"></div>'
            '<div style="flex: 1; min-width: 280px;"><h4 style="margin: 0 0 5px 0; color: #333; font-size: 1.2em;">' + head + '</h4><p style="margin: 0 0 15px 0; font-weight: bold; color: #0b99bc;">Roderick Klaver, ' + role +
            '</p><p style="margin: 0; line-height: 1.6; color: #555;">' + text + '</p></div></div>')

def kort(label, body):
    return ('<!-- VXL:KORT-ANTWOORD:START --><div style="background: #f9f9f9; border-left: 5px solid #0b99bc; padding: 15px; border-radius: 5px; margin: 0 0 25px 0;"><p style="font-family: inherit; margin: 0; font-size: 17px;"><strong>' + label + '</strong> ' + body + '</p></div><!-- VXL:KORT-ANTWOORD:END -->')

def faq(items):
    return ''.join(P.format(B(q) + ' ' + a) for q, a in items)

def page(intro, parts):
    return '<p>' + intro + '</p><div style="font-family: inherit; line-height: 1.7; color: #333333; max-width: 860px;">' + ''.join(parts) + '</div>\n'

# ---------------------------------------------------------------- FR
U = {k: 'https://www.verpakkingenxl.be/fr/' + v for k, v in {
    'nop': 'emballage-et-protection/papier-bulle/', 'coex': 'sacs/sacs-dexpedition-coex/', 'ldpe': 'sacs/sacs-ldpe/', 'zip': 'sacs/sachets-zip/sachets-zip-ldpe/',
    'stretch': 'film-demballage/film-etirable/', 'afval': 'hygiene/gestion-des-dechets/sacs-poubelles/', 'nano': 'emballage-et-protection/film-de-banderolage/film-de-banderolage-nano/', 'folie': 'film-demballage/'}.items()}
fr = page(
    "Chaque semaine, notre service achats reçoit un aperçu des prix actuels des matières premières plastiques. Nous le consultons avant d'acheter du film, des sacs d'expédition et du papier bulle. Ces chiffres, nous ne les gardons pas pour nous. Vous voyez ci-dessous exactement ce que nous voyons, pour juger vous-même pourquoi un prix monte ou baisse.",
    [kort('La réponse courte :', 'au %%DATUM%%, le <strong>LDPE en Europe coûte %%LDPE%% par tonne</strong>, le <strong>LLDPE %%LLDPE%%</strong> et le <strong>HDPE %%HDPE%% par tonne</strong>. C\'est %%VS_PIEK%% de moins qu\'au pic de début juin 2026, mais toujours %%VS_JAN%% de plus qu\'en janvier 2026. Le graphique ci-dessous affiche chaque semaine la dernière cotation.'),
     H2.format('Pourquoi nous partageons les prix des matières premières'),
     P.format("Un rouleau de film étirable ou un carton de sacs d'expédition coex est composé en grande partie de granulés de plastique. Si le prix de ces granulés augmente, le produit fini devient plus cher quelques semaines plus tard. S'il baisse, le produit fini doit devenir moins cher."),
     P.format("En tant que client, vous ne voyez généralement que le résultat : un nouveau prix dans la boutique en ligne ou sur votre devis. La raison de ce changement reste floue. Nous trouvons cela dommage. Vous devez pouvoir voir d'où vient une variation de prix. C'est pourquoi nous publions sur cette page les chiffres de marché que nous utilisons, avec des explications."),
     H2.format('Prix actuels des matières premières : LDPE, LLDPE, HDPE et plus'),
     P.format("Le graphique montre les prix hebdomadaires par tonne de huit plastiques, depuis janvier 2024. Choisissez " + B('Europe') + " ou " + B('Asie') + ", activez ou désactivez des matières et choisissez une période. Avec " + B('Indice') + ", toutes les courbes partent de 100 au début de la période. Vous voyez ainsi d'un coup d'œil quelle matière a le plus augmenté ou baissé."),
     IFR('%%WIDGET%%?shop=befr', 'Graphique : prix actuels des matières premières plastiques par tonne (LDPE, LLDPE, HDPE, PP, PET, PVC, PS, ABS)', 1200, G_H),
     H2.format('LDPE, LLDPE et HDPE : quelle différence ?'),
     P.format("Ce sont trois types de polyéthylène (PE), le plastique le plus utilisé pour les emballages. La différence tient à la façon dont les molécules sont liées. Cela détermine si le matériau est souple, extensible ou rigide."),
     table(['Matière', 'Propriétés', 'Utilisée dans'], [
         [B('LDPE') + '<br>(Low Density PE)', 'Doux, souple, facile à souder', AL.format(U['nop'], 'Papier bulle') + ', ' + AL.format(U['coex'], "sacs d'expédition coex") + ', ' + AL.format(U['ldpe'], 'sacs LDPE') + ', ' + AL.format(U['zip'], 'sachets zip')],
         [B('LLDPE') + '<br>(Linear Low Density PE)', 'Résistant et très extensible, se déchire difficilement', AL.format(U['stretch'], 'Film étirable') + " (manuel et machine), souvent aussi mélangé dans les sacs d'expédition"],
         [B('HDPE') + '<br>(High Density PE)', 'Plus rigide, bruissant, résistant même en faible épaisseur', 'Sachets fins, ' + AL.format(U['afval'], 'sacs poubelles') + ', sacs de transport'],
         [B('PP') + '<br>(Polypropylène)', 'Rigide, transparent, résistant à la chaleur', 'Ruban adhésif, feuillard PP, sacs PP transparents']]),
     P.format("Le PET, le PVC, le PS et l'ABS figurent aussi dans le graphique. Nous les utilisons moins dans notre assortiment, mais ils montrent bien l'évolution de tout le marché du plastique."),
     H2.format("Qu'est-ce qui détermine le prix du LDPE et du HDPE ?"),
     P.format("Le polyéthylène est fabriqué à partir d'éthylène, lui-même issu du pétrole et du gaz naturel. Le prix d'une tonne de LDPE dépend donc de plusieurs facteurs :"),
     UL([B('Prix du pétrole et du gaz.') + " C'est la matière de base de l'éthylène. Quand le pétrole augmente, le PE suit généralement en quelques semaines.",
         B("Coûts de l'énergie.") + " Transformer le gaz et le pétrole en granulés demande beaucoup d'énergie. L'Europe la paie plus cher que les États-Unis ou le Moyen-Orient.",
         B("L'offre et la demande.") + " Si des usines sont en maintenance ou à l'arrêt, l'offre se raréfie et le prix monte.",
         B('Importation et transport.') + " L'Europe importe une grande partie de son PE des États-Unis, du Moyen-Orient et d'Asie. Un fret maritime plus cher ou une route bloquée se ressent donc vite.",
         B('Taux de change.') + " Les matières premières se négocient souvent en dollars. Un euro plus faible rend l'importation plus chère."]),
     H3.format("L'Europe et l'Asie n'évoluent pas au même rythme"),
     P.format("Comparez " + B('Asie') + " et " + B('Europe') + " dans le graphique. Deux choses ressortent. En Asie, le prix par tonne est nettement plus bas. Et l'Europe réagit plus tard : en 2026, le LDPE a atteint son pic en Chine à la mi-avril, et en Europe seulement début juin. Une hausse en Asie annonce donc souvent une hausse en Europe."),
     H2.format('Évolution des prix des matières premières depuis 2024'),
     P.format(B('2024 et 2025 : calme.') + " En Europe, le LDPE a oscillé entre 1 648 et 1 858 par tonne en 2024, et entre 1 818 et 1 968 en 2025. Le HDPE est resté entre 1 378 et 1 558 ces deux années. De petits mouvements, à peine visibles dans le prix de vente."),
     P.format(B('Mars à juin 2026 : une forte hausse.') + " Début mars, le LDPE était encore à 1 903 par tonne. La guerre autour de l'Iran a fait grimper le pétrole et les matières premières. Le 1er juin, le LDPE coûtait 3 053 par tonne : 60 % de plus que trois mois plus tôt. Sur cette période, le LLDPE a augmenté de 71 % et le HDPE de 76 %."),
     P.format(B("De juin 2026 à aujourd'hui : un lent repli.") + " Depuis le pic, les prix baissent à nouveau. Fin août, le LDPE était à 2 528 par tonne. C'est 17 % sous le pic, mais encore 37 % au-dessus du niveau de janvier 2026."),
     H2.format("Comment une hausse des matières premières se répercute sur notre prix"),
     P.format("Pour les films et les sacs plastiques, la matière première représente environ " + B('60 à 70 % du prix de revient') + ". Le reste correspond à la production, l'énergie, l'emballage et le transport. Une hausse de la matière première ne se répercute donc pas à 100 % sur le prix, mais en grande partie."),
     H3.format('Un exemple chiffré'),
     P.format("Imaginons qu'un carton de sacs d'expédition nous coûte 100 € à l'achat. Dont 65 € de matière première."),
     UL(["Le LDPE augmente de 20 %. La matière première de ce carton passe à 65 € × 1,20 = 78 €.",
         "Le carton nous coûte désormais 113 € au lieu de 100 €.",
         "Une hausse de 20 % de la matière première rend donc le produit environ " + B('13 % plus cher') + "."]),
     P.format("L'inverse fonctionne de la même façon. Si le LDPE baisse de 10 %, le prix de revient diminue d'environ 6,5 %."),
     H2.format('Calculateur : que signifie cela pour vos achats ?'),
     P.format("Choisissez votre produit et indiquez votre budget annuel. Le calculateur reprend l'évolution de la matière première du graphique et calcule l'effet possible sur vos coûts. Vous pouvez aussi saisir votre propre pourcentage, par exemple pour simuler un scénario."),
     IFR('%%WIDGET%%?shop=befr&amp;view=calculator', "Calculateur : effet des prix des matières premières sur vos achats de film et de sacs", 950, C_H),
     H2.format('Pourquoi notre prix ne bouge pas chaque semaine'),
     P.format("Le graphique bouge chaque semaine, nos prix en ligne non. Il y a trois raisons à cela :"),
     UL([B('Le stock.') + " Ce qui est en stock aujourd'hui a été acheté il y a plusieurs semaines, au prix de l'époque.",
         B('Le temps de production.') + " Les fabricants calculent avec le prix de la matière première au moment de produire. Entre le granulé et le carton sur la palette, il s'écoule quelques semaines.",
         B('Nous lissons les petites variations.') + " Une semaine +2 % et la suivante -2 % : nous n'adaptons pas le prix à chaque fois. Ce n'est que lorsqu'un mouvement se confirme que nous le répercutons."]),
     P.format("Cela vaut dans les deux sens. Si les prix des matières premières baissent durablement, vous le verrez aussi dans nos prix."),
     H2.format('Bien acheter quand les prix des matières premières fluctuent'),
     UL([B('Regardez la tendance, pas une seule semaine.') + " Les prix augmentent en Asie et en Europe depuis plusieurs semaines ? Il est alors judicieux de constituer un peu de stock avant que la hausse n'arrive dans le prix final.",
         B('Achetez par carton ou par palette.') + " De plus grandes quantités donnent un prix unitaire plus bas. Vous absorbez ainsi vous-même une partie de la hausse.",
         B("Choisissez la bonne épaisseur.") + " Un film plus fin et plus résistant utilise moins de matière par palette. Découvrez par exemple notre " + A.format(U['nano'], 'film de banderolage nano') + ".",
         B('Comparez au kilo.') + " Pour le film, le prix par rouleau ne dit pas grand-chose. Calculez le prix au kilo : c'est la seule façon de comparer honnêtement."]),
     H2.format('Questions fréquentes (FAQ)'),
     faq([("Combien coûte le LDPE par tonne ?", "Fin août 2026, le LDPE coûtait 2 528 par tonne en Europe et 1 260 par tonne en Asie. Le prix actuel figure en haut de cette page dans le graphique. Il s'agit du prix de la matière première en granulés, donc sans transformation en film ou en sacs."),
          ("Combien coûte le HDPE par tonne ?", "Fin août 2026, le HDPE coûtait 2 038 par tonne en Europe et 997 par tonne en Asie. Le HDPE est généralement un peu moins cher que le LDPE."),
          ("Quelle est la différence entre LDPE et HDPE ?", "Le LDPE est doux et souple, il sert pour le papier bulle, les sacs d'expédition et les sacs LDPE. Le HDPE est plus rigide, bruissant et résistant même en faible épaisseur. On le trouve dans les sachets fins et les sacs poubelles."),
          ("Pourquoi les prix du plastique ont-ils autant augmenté en 2026 ?", "À partir de mars 2026, le pétrole et les matières premières ont fortement augmenté à cause de la guerre autour de l'Iran. En Europe, le LDPE est passé de 1 903 par tonne début mars à 3 053 par tonne le 1er juin. Depuis, les prix baissent à nouveau."),
          ("En combien de temps une hausse se répercute-t-elle sur le prix ?", "Généralement après quelques semaines. Le stock déjà acheté est d'abord vendu. Ensuite arrive la nouvelle production, achetée au nouveau prix de la matière première."),
          ("D'où viennent ces chiffres ?", "Notre service achats reçoit chaque semaine un aperçu des prix de marché des matières premières plastiques en Europe et en Asie. Nous publions ces chiffres sur cette page. Il s'agit de cotations de marché, pas de nos propres prix d'achat."),
          ("À quelle fréquence cette page est-elle mise à jour ?", "Chaque semaine. En haut du graphique, vous voyez la date de la dernière cotation et un court point marché de notre service achats."),
          ("Vos prix augmentent-ils quand le graphique monte ?", "Pas immédiatement et pas à chaque fluctuation. Si une hausse se confirme pendant quelques semaines, elle se retrouve dans le prix lors des nouveaux achats. En cas de baisse durable, c'est l'inverse.")]),
     usp('Pourquoi acheter chez VerpakkingenXL', ['Transparence sur les prix : vous voyez les mêmes chiffres de marché que nous', 'Livraison rapide depuis le stock', 'Prix dégressifs par carton et par palette', 'Conseils personnalisés de la part d\'entrepreneurs, depuis 2014']),
     cta('Besoin d\'une grande quantité ?', 'Demandez un devis pour du film ou des sacs par palette. Appelez le +31 53 573 84 56 entre 9h00 et 17h00, ou écrivez à info@verpakkingenxl.be. Vous recevez une réponse dans les 4 heures ouvrables.', U['folie'], 'Voir tous les films →'),
     author("À propos de l'auteur", 'copropriétaire de VerpakkingenXL', "Roderick est responsable des achats. Il suit chaque semaine le marché des matières premières et décide sur cette base quand et combien nous achetons. Des questions sur les prix ou les grandes quantités ? Écrivez à info@verpakkingenxl.be.")])
open('artikel_template_fr.html', 'w', encoding='utf-8').write(fr)

# ---------------------------------------------------------------- DE
D = {k: 'https://www.verpackungenxl.de/' + v for k, v in {
    'nop': 'verpackung-und-schutz/luftpolsterfolie/', 'coex': 'beutel-taschen/coex-versandtaschen/', 'ldpe': 'beutel-taschen/ldpe-beutel/', 'zip': 'beutel-taschen/druckverschlussbeutel/ldpe-druckverschlussbeutel/',
    'stretch': 'folie/stretchfolie/', 'afval': 'hygiene/abfallmanagement/muellsaecke/', 'nano': 'verpackung-und-schutz/wickelfolie/nano-wickelfolie/', 'folie': 'folie/'}.items()}
de = page(
    "Unser Einkauf erhält jede Woche eine Übersicht mit den aktuellen Preisen für Kunststoff-Rohstoffe. Diese schauen wir uns an, bevor wir Folie, Versandtaschen und Luftpolsterfolie einkaufen. Diese Zahlen behalten wir nicht für uns. Unten sehen Sie genau, was wir sehen, damit Sie selbst beurteilen können, warum ein Preis steigt oder sinkt.",
    [kort('Die kurze Antwort:', 'Am %%DATUM%% kostet <strong>LDPE in Europa %%LDPE%% pro Tonne</strong>, <strong>LLDPE %%LLDPE%%</strong> und <strong>HDPE %%HDPE%% pro Tonne</strong>. Das ist %%VS_PIEK%% weniger als beim Höchststand Anfang Juni 2026, aber immer noch %%VS_JAN%% mehr als im Januar 2026. In der Grafik unten sehen Sie jede Woche die neueste Notierung.'),
     H2.format('Warum wir Rohstoffpreise mit Ihnen teilen'),
     P.format("Eine Rolle Stretchfolie oder ein Karton Coex-Versandtaschen besteht zum größten Teil aus Kunststoffgranulat. Steigt der Preis dieses Granulats, wird das Endprodukt einige Wochen später teurer. Sinkt er, sollte das Endprodukt günstiger werden."),
     P.format("Als Kunde sehen Sie meist nur das Ergebnis: einen neuen Preis im Onlineshop oder auf Ihrem Angebot. Warum sich der Preis ändert, bleibt unklar. Das finden wir schade. Sie sollten sehen können, woher eine Preisänderung kommt. Deshalb veröffentlichen wir auf dieser Seite die Marktzahlen, die wir selbst nutzen, mit Erklärung."),
     H2.format('Aktuelle Rohstoffpreise: LDPE, LLDPE, HDPE und mehr'),
     P.format("Die Grafik zeigt die Wochenpreise pro Tonne für acht Kunststoffe seit Januar 2024. Wählen Sie " + B('Europa') + " oder " + B('Asien') + ", blenden Sie Rohstoffe ein oder aus und wählen Sie einen Zeitraum. Mit " + B('Index') + " starten alle Linien bei 100 zu Beginn des Zeitraums. So sehen Sie auf einen Blick, welcher Rohstoff am stärksten gestiegen oder gefallen ist."),
     IFR('%%WIDGET%%?shop=de', 'Grafik: aktuelle Rohstoffpreise Kunststoff pro Tonne (LDPE, LLDPE, HDPE, PP, PET, PVC, PS, ABS)', 1200, G_H),
     H2.format('LDPE, LLDPE und HDPE: Was ist der Unterschied?'),
     P.format("Alle drei sind Polyethylen-Arten (PE), der am häufigsten verwendete Kunststoff für Verpackungen. Der Unterschied liegt darin, wie die Moleküle miteinander verbunden sind. Das bestimmt, ob das Material weich, dehnbar oder steif ist."),
     table(['Rohstoff', 'Eigenschaften', 'Zu finden in'], [
         [B('LDPE') + '<br>(Low Density PE)', 'Weich, geschmeidig, gut verschweißbar', AL.format(D['nop'], 'Luftpolsterfolie') + ', ' + AL.format(D['coex'], 'Coex-Versandtaschen') + ', ' + AL.format(D['ldpe'], 'LDPE-Beutel') + ', ' + AL.format(D['zip'], 'Druckverschlussbeutel')],
         [B('LLDPE') + '<br>(Linear Low Density PE)', 'Stark und sehr dehnbar, reißt nicht schnell', AL.format(D['stretch'], 'Stretchfolie') + ' (Hand- und Maschinenfolie), oft auch in Versandtaschen beigemischt'],
         [B('HDPE') + '<br>(High Density PE)', 'Steifer, knistert, stabil schon bei geringer Stärke', 'Dünne Beutel, ' + AL.format(D['afval'], 'Müllsäcke') + ', Tragetaschen'],
         [B('PP') + '<br>(Polypropylen)', 'Steif, klar, hitzebeständig', 'Klebeband, PP-Umreifungsband, transparente PP-Beutel']]),
     P.format("PET, PVC, PS und ABS sind ebenfalls in der Grafik. Diese verwenden wir in unserem Sortiment seltener, sie zeigen aber gut, wie sich der gesamte Kunststoffmarkt bewegt."),
     H2.format('Was bestimmt den Preis von LDPE und HDPE?'),
     P.format("Polyethylen wird aus Ethylen hergestellt, und Ethylen stammt aus Erdöl und Erdgas. Der Preis einer Tonne LDPE hängt deshalb von mehreren Faktoren ab:"),
     UL([B('Öl- und Gaspreis.') + " Der Ausgangsstoff für Ethylen. Steigt der Ölpreis, folgt PE meist innerhalb weniger Wochen.",
         B('Energiekosten.') + " Die Umwandlung von Gas und Öl in Granulat braucht viel Energie. Europa zahlt dafür mehr als die USA oder der Nahe Osten.",
         B('Angebot und Nachfrage.') + " Gehen Werke in Wartung oder fallen aus, wird das Angebot knapp und der Preis steigt.",
         B('Import und Transport.') + " Europa bezieht einen großen Teil seines PE aus den USA, dem Nahen Osten und Asien. Teurere Seefracht oder eine blockierte Route spürt man daher schnell.",
         B('Wechselkurs.') + " Rohstoffe werden weltweit oft in Dollar gehandelt. Ein schwächerer Euro verteuert den Import."]),
     H3.format('Europa und Asien bewegen sich nicht gleich'),
     P.format("Vergleichen Sie in der Grafik " + B('Asien') + " und " + B('Europa') + ". Zwei Dinge fallen auf. In Asien liegt der Preis pro Tonne deutlich niedriger. Und Europa reagiert später: 2026 erreichte LDPE in China Mitte April den Höchststand, in Europa erst Anfang Juni. Ein Anstieg in Asien ist also oft ein Vorbote für Europa."),
     H2.format('So haben sich die Rohstoffpreise seit 2024 entwickelt'),
     P.format(B('2024 und 2025: ruhig.') + " LDPE in Europa schwankte 2024 zwischen 1.648 und 1.858 pro Tonne und 2025 zwischen 1.818 und 1.968. HDPE lag in beiden Jahren zwischen 1.378 und 1.558. Kleine Bewegungen, die im Verkaufspreis kaum zu sehen waren."),
     P.format(B('März bis Juni 2026: ein kräftiger Anstieg.') + " Anfang März lag LDPE noch bei 1.903 pro Tonne. Durch den Krieg rund um den Iran stiegen Öl und Rohstoffe stark an. Am 1. Juni kostete LDPE 3.053 pro Tonne: 60 % mehr als drei Monate zuvor. LLDPE stieg in diesem Zeitraum um 71 %, HDPE um 76 %."),
     P.format(B('Juni 2026 bis heute: langsam zurück.') + " Seit dem Höchststand sinken die Preise wieder. Ende August lag LDPE bei 2.528 pro Tonne. Das sind 17 % unter dem Höchststand, aber noch 37 % über dem Niveau von Januar 2026."),
     H2.format('So wirkt sich ein Rohstoffanstieg auf unseren Preis aus'),
     P.format("Bei Folien und Kunststoffbeuteln macht der Rohstoff etwa " + B('60 bis 70 % des Selbstkostenpreises') + " aus. Der Rest entfällt auf Produktion, Energie, Verpackung und Transport. Ein Rohstoffanstieg landet also nicht eins zu eins im Preis, aber zu einem großen Teil."),
     H3.format('Ein Rechenbeispiel'),
     P.format("Angenommen, ein Karton Versandtaschen kostet uns im Einkauf 100 €. Davon sind 65 € Rohstoff."),
     UL(["LDPE steigt um 20 %. Der Rohstoff in diesem Karton kostet dann 65 € × 1,20 = 78 €.",
         "Der Karton kostet uns jetzt 113 € statt 100 €.",
         "Ein Rohstoffanstieg von 20 % macht das Produkt also etwa " + B('13 % teurer') + "."]),
     P.format("Umgekehrt funktioniert es genauso. Sinkt LDPE um 10 %, sinkt der Selbstkostenpreis um etwa 6,5 %."),
     H2.format('Rechner: Was bedeutet das für Ihren Einkauf?'),
     P.format("Wählen Sie Ihr Produkt und geben Sie ein, wie viel Sie pro Jahr dafür ausgeben. Der Rechner übernimmt die Rohstoffentwicklung aus der Grafik und berechnet, was das für Ihre Kosten bedeuten kann. Sie können auch einen eigenen Prozentsatz eingeben, zum Beispiel um ein Szenario durchzurechnen."),
     IFR('%%WIDGET%%?shop=de&amp;view=calculator', 'Rechner: Auswirkung der Rohstoffpreise auf Ihren Einkauf von Folie und Beuteln', 950, C_H),
     H2.format('Warum sich unser Preis nicht jede Woche ändert'),
     P.format("Die Grafik bewegt sich jede Woche, unsere Shoppreise nicht. Dafür gibt es drei Gründe:"),
     UL([B('Lagerbestand.') + " Was jetzt auf Lager liegt, wurde vor Wochen zum damaligen Preis eingekauft.",
         B('Produktionszeit.') + " Hersteller rechnen mit dem Rohstoffpreis zum Zeitpunkt der Produktion. Zwischen Granulat und Karton auf der Palette liegen einige Wochen.",
         B('Kleine Schwankungen gleichen wir aus.') + " Eine Woche +2 % und die nächste -2 %: Darauf passen wir den Preis nicht jedes Mal an. Erst wenn sich eine Bewegung fortsetzt, geben wir sie weiter."]),
     P.format("Das gilt in beide Richtungen. Sinken die Rohstoffpreise dauerhaft, sehen Sie das auch in unseren Preisen."),
     H2.format('Clever einkaufen bei schwankenden Rohstoffpreisen'),
     UL([B('Achten Sie auf den Trend, nicht auf eine Woche.') + " Steigen die Preise in Asien und Europa schon mehrere Wochen in Folge? Dann ist es sinnvoll, etwas mehr einzukaufen, bevor der Anstieg im Endpreis ankommt.",
         B('Kaufen Sie pro Karton oder Palette.') + " Größere Mengen bedeuten einen niedrigeren Stückpreis. So fangen Sie einen Teil eines Anstiegs selbst ab.",
         B('Wählen Sie die richtige Stärke.') + " Dünnere, stärkere Folie verbraucht weniger Rohstoff pro Palette. Sehen Sie sich zum Beispiel unsere " + A.format(D['nano'], 'Nano-Wickelfolie') + " an.",
         B('Vergleichen Sie pro Kilo.') + " Bei Folie sagt der Preis pro Rolle wenig aus. Rechnen Sie den Preis pro Kilo aus: Nur so vergleichen Sie fair."]),
     H2.format('Häufige Fragen (FAQ)'),
     faq([("Was kostet LDPE pro Tonne?", "Ende August 2026 kostete LDPE in Europa 2.528 pro Tonne und in Asien 1.260 pro Tonne. Den aktuellen Preis sehen Sie oben auf dieser Seite in der Grafik. Es handelt sich um den Preis des Rohstoffs als Granulat, also ohne Verarbeitung zu Folie oder Beuteln."),
          ("Was kostet HDPE pro Tonne?", "Ende August 2026 kostete HDPE in Europa 2.038 pro Tonne und in Asien 997 pro Tonne. HDPE ist meist etwas günstiger als LDPE."),
          ("Was ist der Unterschied zwischen LDPE und HDPE?", "LDPE ist weich und geschmeidig und wird für Luftpolsterfolie, Versandtaschen und LDPE-Beutel verwendet. HDPE ist steifer, knistert und ist schon bei geringer Stärke stabil. Sie finden es in dünnen Beuteln und Müllsäcken."),
          ("Warum sind die Kunststoffpreise 2026 so stark gestiegen?", "Ab März 2026 stiegen Öl und Rohstoffe durch den Krieg rund um den Iran stark an. LDPE in Europa stieg von 1.903 pro Tonne Anfang März auf 3.053 pro Tonne am 1. Juni. Seitdem sinken die Preise wieder."),
          ("Wie schnell zeigt sich ein Rohstoffanstieg im Preis?", "Meist nach einigen Wochen. Zuerst wird der bereits eingekaufte Bestand verkauft. Danach kommt neue Ware, eingekauft zum neuen Rohstoffpreis."),
          ("Woher stammen diese Zahlen?", "Unser Einkauf erhält jede Woche eine Übersicht der Marktpreise für Kunststoff-Rohstoffe in Europa und Asien. Diese Zahlen veröffentlichen wir auf dieser Seite. Es handelt sich um Marktnotierungen, nicht um unsere eigenen Einkaufspreise."),
          ("Wie oft wird diese Seite aktualisiert?", "Jede Woche. Oben in der Grafik sehen Sie das Datum der letzten Notierung und ein kurzes Marktupdate unseres Einkaufs."),
          ("Steigen Ihre Preise, wenn die Grafik steigt?", "Nicht sofort und nicht bei jeder Schwankung. Hält ein Anstieg einige Wochen an, fließt er beim nächsten Einkauf in den Preis ein. Bei einem dauerhaften Rückgang funktioniert es umgekehrt.")]),
     usp('Warum bei VerpackungenXL einkaufen', ['Offen bei Preisen: Sie sehen dieselben Marktzahlen wie wir', 'Schnelle Lieferung ab Lager', 'Staffelpreise pro Karton und pro Palette', 'Persönliche Beratung von Menschen, die selbst Unternehmer sind, seit 2014']),
     cta('Größere Menge benötigt?', 'Fordern Sie ein Angebot für Folie oder Beutel pro Palette an. Rufen Sie uns an unter +31 53 573 84 56 zwischen 9:00 und 17:00 Uhr oder schreiben Sie an info@verpackungenxl.de. Sie erhalten innerhalb von 4 Geschäftsstunden eine Antwort.', D['folie'], 'Alle Folien ansehen →'),
     author('Über den Autor', 'Mitinhaber von VerpackungenXL', "Roderick ist für den Einkauf verantwortlich. Er verfolgt jede Woche den Rohstoffmarkt und entscheidet auf dieser Grundlage, wann und wie viel wir einkaufen. Fragen zu Preisen oder größeren Mengen? Schreiben Sie an info@verpackungenxl.de.")])
open('artikel_template_de.html', 'w', encoding='utf-8').write(de)
print(len(fr), len(de))
