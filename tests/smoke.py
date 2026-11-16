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
    answers = {'prompt': ['Tuile test', '1234'], 'confirm': []}
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
    check(pg.locator('[data-side="elle"]').count() == 4, 'tuiles de départ : seulement les 4 (Critique, Mépris, Défensive, Mur)')
    check(pg.inner_text('#enext').startswith('Passer'), 'bouton « Passer » absent quand rien n\'est choisi')
    pg.click('[data-side="elle"][data-tile="Mépris"]')
    pg.fill('[data-annot="elle"][data-tile="Mépris"]', 'annotation test')
    check(pg.inner_text('#enext').startswith('Suivant'), 'bouton « Suivant » absent après un choix')
    nxt()                                                                # Elle se sent
    check(pg.locator('[data-feel="elle"]:not(.add)').count() == 0, 'ressentis : doivent être vierges au départ')
    pg.click('[data-addfeel="elle"]')                                    # crée « Tuile test »
    nxt()                                                                # Elle note
    pg.fill('#enote', 'Note sur elle test')
    nxt()                                                                # Moi a fait
    check(pg.inner_text('.steptitle').startswith('Moi'), 'après Elle, on doit passer à Moi')
    nxt()                                                                # Moi se sent
    pg.click('[data-feel="moi"][data-tile="Tuile test"]')
    nxt()                                                                # Moi note
    pg.fill('#ewhat', 'Texte de test')
    pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.locator('[data-entry]').count() == 1, 'pastille noire non enregistrée')

    # 2b. « Moi » d'abord : l'ordre s'inverse
    pg.click('[data-new="g"]'); pg.click('[data-qui="moi"]'); pg.wait_for_timeout(100)
    check(pg.inner_text('.steptitle').startswith('Moi'), 'après « Moi », on doit commencer par Moi')
    pg.click('[data-close]'); pg.wait_for_timeout(200)

    # 3. garde-fou : Mépris sur une orange
    pg.click('[data-new="o"]'); pg.click('[data-qui="deux"]'); pg.wait_for_timeout(100)
    pg.click('[data-side="elle"][data-tile="Mépris"]')
    check(pg.is_visible('#sugRed'), 'garde-fou « plutôt rouge ? » absent')
    pg.click('#sugRed')
    pg.click('[data-goto="6"]'); pg.click('#eok'); pg.wait_for_timeout(300)

    # 4. fermer sans valider demande confirmation (accepte => rien d'enregistré)
    pg.click('[data-new="g"]'); pg.click('#enext'); pg.wait_for_timeout(100)
    pg.click('[data-goto="3"]'); pg.fill('#enote', 'test fermeture')
    pg.click('[data-close]'); pg.wait_for_timeout(200)
    check(pg.locator('[data-entry]').count() == 2, 'fermeture sans valider a enregistré quelque chose')

    # 4b. brouillon : on quitte l'appli en pleine saisie, on revient sur le même écran
    pg.click('[data-new="r"]'); pg.click('[data-qui="elle"]'); pg.wait_for_timeout(100)
    pg.click('[data-side="elle"][data-tile="Mur"]'); nxt(); nxt()
    pg.fill('#enote', 'brouillon en cours'); pg.wait_for_timeout(600)
    pg.reload(); pg.wait_for_timeout(300)
    for k in '1234':
        pg.click(f'.pad button[data-k="{k}"]'); pg.wait_for_timeout(150)
    pg.wait_for_timeout(500)
    check(pg.locator('.overlay.page').count() == 1, 'brouillon non restauré après retour')
    check(pg.locator('#enote').count() == 1 and pg.input_value('#enote') == 'brouillon en cours', 'brouillon : pas revenu au bon écran ou texte perdu')
    pg.click('[data-goto="1"]')
    check(pg.locator('[data-side="elle"][data-tile="Mur"].on').count() == 1, 'brouillon : tuile perdue')
    pg.click('[data-goto="6"]'); pg.click('#eok'); pg.wait_for_timeout(300)
    check(pg.locator('[data-entry]').count() == 3, 'brouillon validé non enregistré')

    # 4c. un ancien moment (avant v1.4) s'ouvre sans erreur et garde ses tuiles
    pg.evaluate("""async () => { await saveItem({id:'old1', type:'e', date:todayStr(), time:'08:00', ts:1, color:'r', qui:'', what:'ancien', need:'', feel:['Seul'], moi:{}, elle:{'Insulte':''}, air:false, photos:[], repair:null}); render(); }""")
    pg.wait_for_timeout(200)
    pg.click('[data-entry="old1"]'); pg.click('[data-goto="1"]')
    check(pg.locator('[data-side="elle"][data-tile="Insulte"].on').count() == 1, 'ancien moment : tuile disparue')
    pg.click('[data-goto="6"]'); pg.click('#eok'); pg.wait_for_timeout(300)

    # 5. note
    pg.fill('#newnote', 'Note de test'); pg.click('#addnote'); pg.wait_for_timeout(200)
    check(pg.locator('[data-note]').count() == 1, 'note non ajoutée')

    # 6. onglets
    for tab in ['noires', 'stats', 'bilans']:
        pg.click(f'[data-tab="{tab}"]'); pg.wait_for_timeout(200)
    pg.click('[data-tab="stats"]'); pg.click('[data-seg="resume"]'); pg.wait_for_timeout(200)
    check(pg.locator('svg[role="img"]').count() == 1, 'graphique en colonnes absent')
    pg.click('[data-tab="bilans"]'); pg.wait_for_timeout(200)
    txt = pg.evaluate("periodText(mondayOf(todayStr()), addDays(mondayOf(todayStr()),6), 'test')")
    check('Elle a fait : Mépris (annotation test)' in txt and 'Note sur elle : Note sur elle test' in txt and 'Elle se sent : Tuile test' in txt, 'export bilan incomplet')

    # 7. changement de code (demande l'ancien)
    pg.click('[data-tab="livre"]'); pg.click('#settings'); pg.wait_for_timeout(200)
    pg.click('#chpin'); pg.wait_for_timeout(300)
    check(pg.is_visible('.pad'), 'changement de code : écran de code absent')

    pg.screenshot(path='/tmp/umoral-test.png')
    b.close()

if errs: fails += ['Erreur JS : ' + e for e in errs]
print('OK' if not fails else 'PROBLÈMES :\n- ' + '\n- '.join(fails))
sys.exit(1 if fails else 0)
