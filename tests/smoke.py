"""Test automatique d'Umoral (Playwright + Chrome).
Usage : python3 tests/smoke.py [chemin/vers/index.html]
Simule un iPhone, crée un code, ajoute des moments, vérifie chaque onglet.
Affiche OK ou la liste des problèmes.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

app = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / 'index.html').resolve()
errs, fails = [], []

def check(cond, msg):
    if not cond: fails.append(msg)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg = b.new_page(viewport={'width': 390, 'height': 844})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)
    answers = {'prompt': ['Tuile test', 'Mépris', '1234'], 'confirm': []}
    def on_dialog(d):
        if d.type == 'prompt':
            d.accept(answers['prompt'].pop(0) if answers['prompt'] else '')
        else:
            d.accept()
    pg.on('dialog', on_dialog)
    pg.goto(app.as_uri())

    # 1. création du code
    check(pg.locator('.pad button[data-k="5"]').bounding_box()['width'] >= 88, 'chiffres du code trop petits')
    for k in '12341234':
        pg.click(f'.pad button[data-k="{k}"]'); pg.wait_for_timeout(150)
    pg.wait_for_selector('[data-new="k"]')

    def nxt():
        pg.click('#enext'); pg.wait_for_timeout(100)

    # 2. pastille noire complète, un écran par choix
    pg.click('[data-new="k"]')
    check(pg.is_visible('[data-qui="elle"]'), 'premier écran « Qui ? » absent')
    check(pg.locator('[data-side]').count() == 0, 'les tuiles ne doivent pas être sur l\'écran « Qui ? »')
    pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100)          # avance tout seul
    check(pg.inner_text('.steptitle').startswith('Elle'), 'après « Elle », on doit arriver sur la partie Elle')
    nk = pg.evaluate("TILES.k.acts.length")
    check(pg.locator('.chip[data-side="elle"]').count() == nk, 'noire : seules les tuiles noires doivent être proposées')
    check(pg.locator('.chip[data-side="elle"][data-tile="Pas de vaisselle"]').count() == 0, 'une tuile orange apparaît dans une noire')
    check(pg.inner_text('#enext').startswith('Passer'), 'bouton « Passer » absent quand rien n\'est choisi')
    pg.click('.chip[data-side="elle"][data-tile="Mépris"]')                  # ouvre la bulle
    check(pg.is_visible('#bubbleText'), 'la bulle texte ne s\'ouvre pas en touchant une tuile')
    pg.fill('#bubbleText', 'annotation test'); pg.click('#bubbleOk'); pg.wait_for_timeout(100)
    check(pg.locator('#bubbleText').count() == 0, 'la bulle ne se referme pas après OK')
    check(pg.locator('.chip.on[data-side="elle"][data-tile="Mépris"]').count() == 1, 'tuile non allumée après OK')
    pg.click('.chip[data-side="elle"][data-tile="Mépris"]')                  # rouvrir : le texte est là
    check(pg.input_value('#bubbleText') == 'annotation test', 'bulle : texte non retrouvé')
    pg.click('#bubbleOk')
    check(pg.inner_text('#enext').startswith('Suivant'), 'bouton « Suivant » absent après un choix')
    check(pg.evaluate("TILES.r.acts.includes('Escalade') && !TILES.r.acts.includes('A crié') && TILES.o.acts.includes(\"Risque d'engueulade\")"), 'tuiles rouges/orange non mises à jour')
    check(pg.locator('.chip[data-side="elle"][data-tile="Phrase de trop"]').count() == 1, 'tuile « Phrase de trop » absente')
    check(pg.locator('.chip[data-side="elle"][data-tile="Éloignement urgent"]').count() == 0, '« Éloignement urgent » ne doit être que côté Moi')
    nxt()                                                                # Elle note (plus d'écran « elle se sent »)
    check(pg.locator('#enote').count() == 1, 'l\'écran « comment elle se sent » doit avoir disparu')
    pg.fill('#enote', 'Note sur elle test')
    nxt()                                                                # Moi a fait
    check(pg.inner_text('.steptitle').startswith('Moi'), 'après Elle, on doit passer à Moi')
    check(pg.inner_text('.steptitle') == 'Moi · ma réaction', 'Qui ? Elle : écran « ma réaction » attendu')
    pg.click('[data-rcol="k"]'); pg.wait_for_timeout(100)
    check(pg.locator('.chip[data-react][data-tile="Éloignement urgent"]').count() == 1, '« Éloignement urgent » absent de ma réaction noire')
    check(pg.locator('#air').count() == 0, '« J\'ai pris l\'air » ne doit pas être en noire')
    nxt()                                                                # Moi se sent
    check(pg.locator('.chip[data-feel="moi"][data-tile="Stress énorme"]').count() == 1, 'ressentis noirs absents')
    check(pg.locator('.chip[data-feel="moi"][data-tile="Heureux(se)"]').count() == 0, 'un ressenti vert apparaît dans une noire')
    pg.click('[data-addfeel="moi"]'); pg.wait_for_timeout(100)           # crée « Tuile test » (noire) + bulle
    pg.fill('#bubbleText', 'texte ressenti'); pg.click('#bubbleOk')
    nxt()                                                                # Moi note
    pg.fill('#ewhat', 'Texte de test')
    nxt()                                                                # Elle s'est rattrapée ?
    check(pg.inner_text('.steptitle') == 'Après coup', 'dernier écran « Après coup » absent')
    pg.click('[data-rok="pv"]'); pg.wait_for_timeout(100)
    pg.fill('[data-rhow2]', 'elle a tout rangé')
    pg.click('[data-rex="non"]'); pg.click('[data-grudge="r"]'); pg.wait_for_timeout(100)
    pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.locator('[data-entry]').count() == 1, 'pastille noire non enregistrée')

    # 2b. « Moi » d'abord : l'ordre s'inverse
    pg.click('[data-new="g"]'); pg.click('[data-qui="moi"]'); pg.wait_for_timeout(100)
    check(pg.inner_text('.steptitle').startswith('Moi'), 'après « Moi », on doit commencer par Moi')
    check(pg.locator('[data-goto]').count() == 6, 'verte : pas d\'écran rattrapage attendu')
    pg.click('[data-close]'); pg.wait_for_timeout(200)

    # 3. garde-fou : Mépris (tuile perso) sur une orange
    pg.click('[data-new="o"]'); pg.click('[data-qui="deux"]'); pg.wait_for_timeout(100)
    check(pg.locator('.chip[data-side="elle"][data-tile="Pas de vaisselle"]').count() == 1, 'tuiles orange absentes')
    pg.click('[data-goto="3"]')
    check(pg.locator('#air').count() == 1, '« J\'ai pris l\'air » absent en orange')
    pg.click('[data-goto="1"]')
    pg.click('[data-addact="elle"]'); pg.wait_for_timeout(100); pg.click('#bubbleOk')
    check(pg.is_visible('#sugRed'), 'garde-fou « plutôt rouge ? » absent')
    pg.click('#sugRed')
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)

    # 4. fermer sans valider demande confirmation (accepte => rien d'enregistré)
    pg.click('[data-new="g"]'); pg.click('#enext'); pg.wait_for_timeout(100)
    pg.click('[data-goto="2"]'); pg.fill('#enote', 'test fermeture')
    pg.click('[data-close]'); pg.wait_for_timeout(200)
    check(pg.locator('[data-entry]').count() == 2, 'fermeture sans valider a enregistré quelque chose')

    # 4b. brouillon : on quitte l'appli en pleine saisie, on revient sur le même écran
    pg.click('[data-new="r"]'); pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100)
    pg.click('.chip[data-side="elle"][data-tile="Escalade"]'); pg.click('#bubbleOk'); nxt()
    pg.fill('#enote', 'brouillon en cours'); pg.wait_for_timeout(600)
    pg.reload(); pg.wait_for_timeout(300)
    for k in '1234':
        pg.click(f'.pad button[data-k="{k}"]'); pg.wait_for_timeout(150)
    pg.wait_for_timeout(500)
    check(pg.locator('.overlay.page').count() == 1, 'brouillon non restauré après retour')
    check(pg.locator('#enote').count() == 1 and pg.input_value('#enote') == 'brouillon en cours', 'brouillon : pas revenu au bon écran ou texte perdu')
    pg.click('[data-goto="1"]')
    check(pg.locator('.chip[data-side="elle"][data-tile="Escalade"].on').count() == 1, 'brouillon : tuile perdue')
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.locator('[data-entry]').count() == 3, 'brouillon validé non enregistré')

    # 4c. un ancien moment (avant v1.4) s'ouvre sans erreur et garde ses tuiles
    pg.evaluate("""async () => { await saveItem({id:'old1', type:'e', date:todayStr(), time:'08:00', ts:1, color:'r', qui:'', what:'ancien', need:'', feel:['Seul'], moi:{}, elle:{'Insulte':''}, air:false, photos:[], repair:null}); render(); }""")
    pg.wait_for_timeout(200)
    pg.click('[data-entry="old1"]'); pg.click('[data-goto="1"]')
    check(pg.locator('.chip[data-side="elle"][data-tile="Insulte"].on').count() == 1, 'ancien moment : tuile disparue')
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)

    # 4b-bis. case « Devant… » (prénom réglé sur le téléphone)
    pg.evaluate("S.settings.childName = 'Test'")
    pg.click('[data-new="k"]')
    check(pg.inner_text('#devant').endswith('Devant Test'), 'case « Devant… » absente ou sans le prénom')
    pg.click('#devant'); pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100)
    check(pg.locator('.chip[data-side="elle"][data-tile="Accusation grave"]').count() == 1, 'tuile « Accusation grave » absente')
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)
    check('Devant Test' in pg.inner_text('main'), 'case « Devant… » non enregistrée')
    pg.click('[data-new="g"]')
    check(pg.locator('#devant').count() == 0, 'case « Devant… » ne doit pas être sur une verte')
    pg.click('[data-close]'); pg.wait_for_timeout(200)

    # 4c-bis. ↺ dans le Livre ouvre directement le rattrapage
    pg.click('[data-ratt="old1"]'); pg.wait_for_timeout(150)
    check(pg.inner_text('.steptitle') == 'Après coup', '↺ n\'ouvre pas l\'écran rattrapage')
    pg.click('[data-rok="non"]'); pg.click('#eok'); pg.wait_for_timeout(300)
    pg.click('[data-det="old1"]'); pg.wait_for_timeout(150)
    check('Rattrapée : Non' in pg.inner_text('main'), 'rattrapage non affiché dans les détails')
    pg.click('[data-det="old1"]'); pg.wait_for_timeout(100)

    # 4d. blanche : valider direct
    pg.click('[data-new="w"]'); pg.click('#wquick'); pg.wait_for_timeout(300)
    check(pg.locator('[data-entry]').count() == 6, 'blanche : « Valider direct » n\'enregistre pas')

    # 4e. note rapide : notée sur le coup, rangée plus tard dans une pastille
    pg.click('#quick'); pg.fill('#qtext', 'note rapide test'); pg.click('#qok'); pg.wait_for_timeout(300)
    check(pg.locator('[data-tri]').count() == 1, 'note rapide absente de « À trier »')
    pg.click('[data-tri]'); pg.click('[data-trito="r"]'); pg.wait_for_timeout(200)
    pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100); pg.click('[data-goto="2"]')
    check(pg.input_value('#enote') == 'note rapide test', 'note rapide : texte non repris dans « Note sur elle »')
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.locator('[data-tri]').count() == 0, 'note rapide toujours « À trier » après rangement')
    check(pg.locator('[data-entry]').count() == 7, 'note rapide : pastille non créée')

    # 4f. supprimer des moments par sélection
    for _ in range(2):
        pg.click('[data-new="w"]'); pg.click('#wquick'); pg.wait_for_timeout(300)
    n0 = pg.locator('[data-entry]').count()
    pg.click('#selstart'); pg.wait_for_timeout(100)
    check(pg.locator('.selbox').count() == n0, 'sélection : cases à cocher absentes')
    check(pg.is_disabled('#seldel'), 'sélection : « Supprimer » doit être grisé sans choix')
    pg.locator('[data-entry]').nth(n0-1).click(); pg.locator('[data-entry]').nth(n0-2).click(); pg.wait_for_timeout(100)
    check('(2)' in pg.inner_text('#seldel'), 'sélection : compteur faux')
    check(pg.locator('#eok').count() == 0, 'sélection : toucher un moment ne doit pas l\'ouvrir')
    pg.click('#seldel'); pg.wait_for_timeout(300)
    check(pg.locator('[data-entry]').count() == n0 - 2, 'sélection : moments non supprimés')
    check(pg.locator('#selstart').count() == 1 and pg.locator('.selbox').count() == 0, 'sélection : le mode ne se referme pas')
    pg.click('#selstart'); pg.locator('[data-entry]').nth(0).click(); pg.click('#selcancel'); pg.wait_for_timeout(100)
    check(pg.locator('[data-entry]').count() == n0 - 2, 'sélection : « Annuler » a supprimé quelque chose')

    # 5. plus de cadre « Écris ce que tu as sur le cœur »
    check(pg.locator('#newnote').count() == 0, 'le cadre de note doit avoir disparu')

    # 4g. ma réaction (Qui ? Elle) : sa propre couleur et ses tuiles
    pg.click('[data-new="r"]'); pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100)
    pg.click('[data-goto="3"]')
    check(pg.inner_text('.steptitle') == 'Moi · ma réaction', 'écran « ma réaction » absent avec Qui ? Elle')
    pg.click('[data-rcol="g"]'); pg.click('.chip[data-react][data-tile="Resté calme"]')
    pg.fill('#bubbleText', 'calme test'); pg.click('#bubbleOk'); pg.wait_for_timeout(100)
    check(pg.locator('.chip.on[data-react][data-tile="Resté calme"]').count() == 1, 'réaction : tuile non allumée')
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)
    pg.locator('[data-det]').last.click(); pg.wait_for_timeout(150)
    check('Resté calme (calme test)' in pg.inner_text('.dpanel') and "Dans l'ensemble" in pg.inner_text('.dpanel'), 'réaction absente des détails')
    pg.locator('[data-rev]').last.click(); pg.wait_for_timeout(150)
    pg.fill('.dpanel textarea', 'note réparation'); pg.click('.dpanel [data-v="pv"]'); pg.wait_for_timeout(150)
    pg.click('.dpanel [data-rg][data-v="o"]'); pg.wait_for_timeout(150)
    lst = pg.evaluate("(() => { const e = entries().filter(e => e.reacts && Object.keys(e.reacts).length).slice(-1)[0]; return [e.repair, e.repairNote, e.grudge]; })()")
    check(lst == ['pv', 'note réparation', 'o'], 'revenir dessus mal enregistré ' + str(lst))
    check(pg.locator('.banner [data-repair]').count() == 0, 'les bannières « réparé ? » doivent avoir disparu')
    txt0 = pg.evaluate("periodText(todayStr(), todayStr(), 'test')")
    check('Ma réaction : 🟢 Verte — Resté calme (calme test)' in txt0, 'réaction absente de l\'export')
    pg.click('[data-new="r"]'); pg.click('[data-qui="deux"]'); pg.wait_for_timeout(100)
    check("Moi · ce que j'ai fait" in pg.evaluate("[...document.querySelectorAll('[data-goto]')].map(b => b.getAttribute('aria-label')).join('|')"), '« Les deux » doit garder « ce que j\'ai fait »')
    pg.click('[data-close]'); pg.wait_for_timeout(200)

    # 4h. Je vais
    pg.click('[data-tab="jevais"]'); pg.wait_for_timeout(200)
    pg.fill('#jtext', 'dentiste'); pg.click('#jadd'); pg.wait_for_timeout(200)
    check(pg.locator('[data-jitem]').count() == 0, 'je vais : enregistré sans importance')
    pg.click('[data-jimp="o"]'); pg.click('[data-jday="auj"]'); pg.click('#jadd'); pg.wait_for_timeout(200)
    check(pg.locator('[data-jitem]').count() == 1, 'je vais : non enregistré')
    pg.fill('#jtext', 'mail travail'); pg.click('[data-jwho="moi"]'); pg.click('[data-jimp="r"]'); pg.click('[data-jday="auj"]'); pg.click('#jadd'); pg.wait_for_timeout(200)
    pg.evaluate("S.settings.reminder = '00:00'; render(); checkJeVais(true)"); pg.wait_for_timeout(200)
    check(pg.locator('[data-ja]').count() == 6, 'je vais : point du soir absent')
    pg.locator('[data-ja="non"]').first.click(); pg.wait_for_timeout(200)
    pg.locator('[data-ja="drop"]').first.click(); pg.wait_for_timeout(300)
    check(pg.locator('[data-ja]').count() == 0, 'je vais : point du soir pas refermé')
    jv = pg.evaluate("jvAll().map(j => j.text + ':' + j.status + ':' + j.reports + ':' + (j.due > todayStr()))")
    check('mail travail:open:1:true' in jv and 'dentiste:drop:0:false' in jv, 'je vais : réponses mal enregistrées ' + str(jv))
    check("Paroles en l'air (1)" in pg.inner_text('main'), 'je vais : paroles en l\'air absentes')
    pg.locator('[data-jitem]').first.click(); pg.click('[data-jx="oui"]'); pg.wait_for_timeout(200)
    check('Historique · faits (1)' in pg.inner_text('main'), 'je vais : fait non rangé dans l\'historique')
    check('Je vais (ce qui a été annoncé)' in pg.evaluate("periodText(todayStr(), todayStr(), 'test')"), 'je vais absent de l\'export')
    pg.click('[data-tab="livre"]'); pg.wait_for_timeout(200)

    # 4i. réaction tuile par tuile + tableau
    pg.click('[data-new="k"]'); pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100)
    pg.click('.chip[data-side="elle"][data-tile="Énervement fort"]'); pg.click('#bubbleOk')
    pg.click('.chip[data-side="elle"][data-tile="Mépris"]'); pg.click('#bubbleOk'); pg.wait_for_timeout(100)
    pg.click('[data-goto="3"]')
    check(pg.locator('[data-rcol="g"]').count() == 2, 'réaction : une ligne par tuile attendue')
    pg.click('[data-rcol="k"][data-rt="Mépris"]'); pg.wait_for_timeout(100)
    check(pg.locator('.chip[data-react="Mépris"][data-tile="À bout de nerfs"]').count() == 1, 'réaction noire : « À bout de nerfs » absent')
    check(pg.locator('[data-rnote]').count() == 0, 'les notes de réaction doivent être repliées')
    pg.click('[data-mynote="Mépris"]'); pg.wait_for_timeout(100)
    pg.fill('[data-rnote="Mépris"]', 'note mépris')
    pg.click('[data-rcol="g"][data-rt="Énervement fort"]'); pg.wait_for_timeout(100)
    pg.locator('[data-goto]').last.click(); pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.evaluate("entries().some(e => e.reacts && e.reacts['Mépris'] && e.reacts['Mépris'].c === 'k' && e.reacts['Mépris'].note === 'note mépris')"), 'réaction par tuile non enregistrée')
    pg.click('[data-tab="noires"]'); pg.wait_for_timeout(200)
    check('Notre tableau' in pg.inner_text('main') and pg.locator('.bignum').count() == 1 and pg.locator('.cal').count() == 1, 'tableau incomplet')
    pg.click('[data-tcol="k"]'); pg.wait_for_timeout(200)
    check(pg.locator('[data-open]').count() >= 1, 'tableau : liste des noires vide')
    pg.click('[data-close]'); pg.click('[data-tb="mois"]'); pg.wait_for_timeout(200)
    pg.click('[data-tab="bilans"]'); pg.wait_for_timeout(200)
    check(pg.locator('.pill').count() >= 1 and 'Chez elle' in pg.inner_text('main'), 'bilan en blocs absent')
    check('ligne franchie' not in pg.inner_text('main').lower(), '« ligne franchie » encore présent')
    pg.click('[data-tab="livre"]'); pg.wait_for_timeout(200)

    # 4j. Juste moi : une page, hors stats du couple
    nb = pg.evaluate("entries().length")
    pg.click('[data-new="r"]'); pg.click('[data-qui="seul"]'); pg.wait_for_timeout(100)
    check(pg.inner_text('.steptitle').startswith('Juste moi'), 'Juste moi : page absente')
    check(pg.locator('[data-goto]').count() == 2, 'Juste moi : une seule page attendue')
    check(pg.locator('.chip[data-feel="moi"][data-tile="Joie"]').count() == 0, 'Juste moi : une émotion d\'une autre couleur est proposée')
    check(pg.locator('[data-addmood]').count() == 1, 'Juste moi : un seul « + » attendu')
    pg.click('.chip[data-feel="moi"][data-tile="Colère"]'); pg.click('#bubbleOk')
    pg.click('.chip[data-feel="moi"][data-tile="Tristesse"]'); pg.click('#bubbleOk')
    pg.fill('#ewhat', 'humeur test'); pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.evaluate("entries().length") == nb and pg.evaluate("moods().length") == 1, 'Juste moi compté dans le couple')
    pg.click('[data-tab="noires"]'); pg.click('[data-who="moi"]'); pg.wait_for_timeout(200)
    check('Mon humeur' in pg.inner_text('main') and 'Tristesse' in pg.inner_text('main'), 'Mon tableau incomplet')
    pg.click('[data-who="nous"]'); pg.click('[data-tab="livre"]'); pg.wait_for_timeout(200)

    # 4k. un seul « Détails » ouvert à la fois
    dets = pg.locator('[data-det]')
    if dets.count() >= 2:
        dets.nth(0).click(); pg.wait_for_timeout(100); pg.locator('[data-det]').nth(1).click(); pg.wait_for_timeout(100)
        check(pg.locator('.dpanel').count() == 1, 'plusieurs détails ouverts en même temps')
        pg.locator('[data-det]').nth(1).click(); pg.wait_for_timeout(100)

    # 4l. fusion de moments (même couleur)
    pg.evaluate("(async () => { const d = todayStr(); for (const [t, n] of [['08:00','a'],['09:00','b']]) await saveItem({id:'fz'+n, type:'e', color:'o', qui:'elle', date:d, time:t, ts:Date.now(), elle:{Oubli:n}, moi:{}, feel:[], feelNotes:{}, elleNote:'note '+n, photos:[], ellePhotos:[]}); render(); })()")
    pg.wait_for_timeout(300)
    n1 = pg.evaluate("entries().length")
    pg.click('#mergestart'); pg.click('[data-entry="fza"]'); pg.wait_for_timeout(100)
    check(pg.locator('.item.blocked').count() >= 1, 'fusion : les moments d\'une autre couleur doivent être grisés')
    pg.click('[data-entry="fzb"]'); pg.click('#selmerge'); pg.wait_for_timeout(300)
    m = pg.evaluate("entries().find(e => e.id === 'fza')")
    check(pg.evaluate("entries().length") == n1 - 1 and m and m['elle']['Oubli'] == 'a / b' and m['elleNote'] == 'note a\n\nnote b', 'fusion incorrecte')

    # 4m. énergie du jour 🔥 / 🧊 : compteur, appui long, ratio
    r0 = pg.evaluate("ratioOf(withEnergy(counts(inRange(entries(), todayStr(), todayStr())), todayStr(), todayStr(), 'elle'))")
    for _ in range(3): pg.click('[data-en="elle"][data-ek="f"]'); pg.wait_for_timeout(120)
    pg.click('[data-en="moi"][data-ek="i"]'); pg.wait_for_timeout(120)
    check(pg.inner_text('[data-en="elle"][data-ek="f"] b') == '3', '🔥 : compteur faux')
    t = pg.locator('[data-en="elle"][data-ek="f"]').bounding_box()
    pg.mouse.move(t['x']+20, t['y']+20); pg.mouse.down(); pg.wait_for_timeout(800); pg.mouse.up(); pg.wait_for_timeout(200)
    check(pg.inner_text('[data-en="elle"][data-ek="f"] b') == '2', '🔥 : l\'appui long doit retirer 1')
    r1 = pg.evaluate("ratioOf(withEnergy(counts(inRange(entries(), todayStr(), todayStr())), todayStr(), todayStr(), 'elle'))")
    check(r0 is not None and r1 > r0, '🔥 ne compte pas dans le ratio')
    check(pg.evaluate("energyIn(todayStr(), todayStr(), 'moi').i") == 1, '🧊 moi non compté')
    check(pg.evaluate("TILES.r.acts.includes('Frénésie')"), 'tuile rouge « Frénésie » absente')
    check('🔥' in pg.evaluate("periodText(todayStr(), todayStr(), 'test')"), 'énergie absente de l\'export')

    # 6. onglets
    for tab in ['noires', 'stats', 'bilans']:
        pg.click(f'[data-tab="{tab}"]'); pg.wait_for_timeout(200)
    pg.click('[data-tab="stats"]'); pg.click('[data-seg="resume"]'); pg.wait_for_timeout(200)
    check(pg.locator('svg[role="img"]').count() == 1, 'graphique en colonnes absent')
    check('Tuile test' in pg.inner_text('#statsBody'), 'stats : une tuile ajoutée n\'est pas comptée')
    pg.click('[data-tab="bilans"]'); pg.wait_for_timeout(200)
    txt = pg.evaluate("periodText(mondayOf(todayStr()), addDays(mondayOf(todayStr()),6), 'test')")
    check('Elle a fait : Mépris (annotation test)' in txt and 'Note sur elle : Note sur elle test' in txt and 'Je me sens : Tuile test (texte ressenti)' in txt and 'rattrapée : Pas vraiment (elle a tout rangé)' in txt and 'Excuses : Non' in txt and 'Je lui en veux : 🔴 Rouge' in txt, 'export bilan incomplet')

    # 7. changement de code (demande l'ancien)
    pg.click('[data-tab="livre"]'); pg.click('#settings'); pg.wait_for_timeout(200)
    pg.click('#chpin'); pg.wait_for_timeout(300)
    check(pg.is_visible('.pad'), 'changement de code : écran de code absent')

    pg.screenshot(path='/tmp/umoral-test.png')
    b.close()

if errs: fails += ['Erreur JS : ' + e for e in errs]
print('OK' if not fails else 'PROBLÈMES :\n- ' + '\n- '.join(fails))
sys.exit(1 if fails else 0)
