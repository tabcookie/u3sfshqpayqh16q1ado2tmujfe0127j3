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
    check(pg.locator('.chip[data-side="elle"][data-tile="Phrase de trop"]').count() == 1, 'tuile « Phrase de trop » absente')
    check(pg.locator('.chip[data-side="elle"][data-tile="Éloignement urgent"]').count() == 0, '« Éloignement urgent » ne doit être que côté Moi')
    nxt()                                                                # Elle note (plus d'écran « elle se sent »)
    check(pg.locator('#enote').count() == 1, 'l\'écran « comment elle se sent » doit avoir disparu')
    pg.fill('#enote', 'Note sur elle test')
    nxt()                                                                # Moi a fait
    check(pg.inner_text('.steptitle').startswith('Moi'), 'après Elle, on doit passer à Moi')
    check(pg.locator('.chip[data-side="moi"][data-tile="Éloignement urgent"]').count() == 1, '« Éloignement urgent » absent côté Moi')
    check(pg.locator('#air').count() == 0, '« J\'ai pris l\'air » ne doit pas être en noire')
    nxt()                                                                # Moi se sent
    check(pg.locator('.chip[data-feel="moi"][data-tile="Stress énorme"]').count() == 1, 'ressentis noirs absents')
    check(pg.locator('.chip[data-feel="moi"][data-tile="Heureux(se)"]').count() == 0, 'un ressenti vert apparaît dans une noire')
    pg.click('[data-addfeel="moi"]'); pg.wait_for_timeout(100)           # crée « Tuile test » (noire) + bulle
    pg.fill('#bubbleText', 'texte ressenti'); pg.click('#bubbleOk')
    nxt()                                                                # Moi note
    pg.fill('#ewhat', 'Texte de test')
    nxt()                                                                # Elle s'est rattrapée ?
    check(pg.inner_text('.steptitle').startswith('Elle s'), 'dernier écran « Elle s\'est rattrapée ? » absent')
    pg.click('[data-rok="oui"]'); pg.wait_for_timeout(100)
    pg.click('[data-rlvl="g"][data-tile="Mépris"]'); pg.wait_for_timeout(100)
    pg.fill('[data-rhow="Mépris"]', 'elle a tout rangé')
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
    pg.click('.chip[data-side="elle"][data-tile="Mur"]'); pg.click('#bubbleOk'); nxt()
    pg.fill('#enote', 'brouillon en cours'); pg.wait_for_timeout(600)
    pg.reload(); pg.wait_for_timeout(300)
    for k in '1234':
        pg.click(f'.pad button[data-k="{k}"]'); pg.wait_for_timeout(150)
    pg.wait_for_timeout(500)
    check(pg.locator('.overlay.page').count() == 1, 'brouillon non restauré après retour')
    check(pg.locator('#enote').count() == 1 and pg.input_value('#enote') == 'brouillon en cours', 'brouillon : pas revenu au bon écran ou texte perdu')
    pg.click('[data-goto="1"]')
    check(pg.locator('.chip[data-side="elle"][data-tile="Mur"].on').count() == 1, 'brouillon : tuile perdue')
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
    check(pg.inner_text('.steptitle').startswith('Elle s'), '↺ n\'ouvre pas l\'écran rattrapage')
    pg.click('[data-rok="non"]'); pg.click('#eok'); pg.wait_for_timeout(300)
    check('Rattrapée : non' in pg.inner_text('main'), 'rattrapage non affiché dans le Livre')

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

    # 5. note
    pg.fill('#newnote', 'Note de test'); pg.click('#addnote'); pg.wait_for_timeout(200)
    check(pg.locator('[data-note]').count() == 1, 'note non ajoutée')

    # 6. onglets
    for tab in ['noires', 'stats', 'bilans']:
        pg.click(f'[data-tab="{tab}"]'); pg.wait_for_timeout(200)
    pg.click('[data-tab="stats"]'); pg.click('[data-seg="resume"]'); pg.wait_for_timeout(200)
    check(pg.locator('svg[role="img"]').count() == 1, 'graphique en colonnes absent')
    check('Tuile test' in pg.inner_text('#statsBody'), 'stats : une tuile ajoutée n\'est pas comptée')
    pg.click('[data-tab="bilans"]'); pg.wait_for_timeout(200)
    txt = pg.evaluate("periodText(mondayOf(todayStr()), addDays(mondayOf(todayStr()),6), 'test')")
    check('Elle a fait : Mépris (annotation test)' in txt and 'Note sur elle : Note sur elle test' in txt and 'Je me sens : Tuile test (texte ressenti)' in txt and 'Mépris : Le gros (elle a tout rangé)' in txt, 'export bilan incomplet')

    # 7. changement de code (demande l'ancien)
    pg.click('[data-tab="livre"]'); pg.click('#settings'); pg.wait_for_timeout(200)
    pg.click('#chpin'); pg.wait_for_timeout(300)
    check(pg.is_visible('.pad'), 'changement de code : écran de code absent')

    pg.screenshot(path='/tmp/umoral-test.png')
    b.close()

if errs: fails += ['Erreur JS : ' + e for e in errs]
print('OK' if not fails else 'PROBLÈMES :\n- ' + '\n- '.join(fails))
sys.exit(1 if fails else 0)
