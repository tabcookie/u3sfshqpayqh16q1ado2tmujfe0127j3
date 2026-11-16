# Journal des versions

## v1.6 — 16 nov. 2026
- Noire : « Insultes / Humiliation » en une tuile, nouvelle tuile « Phrase de trop », « Dépassement de limite » retiré ; côté Moi « Éloignement urgent ».
- « J'ai pris l'air » seulement sur l'orange.
- Écran « comment elle se sent » retiré (les anciennes données restent dans les bilans).
- Nouveau dernier écran sur orange, rouge et noire : « Elle s'est rattrapée ? » avec ⚪/🟢/🟠 et un texte par tuile ; bouton ↺ dans le Livre pour l'ajouter plus tard ; compté dans les stats et les bilans.

## v1.5 — 16 nov. 2026
- Tuiles de base triées par couleur (positif en blanc/vert, petits accrocs en orange, prises de tête en rouge, le pire en noir), séparées entre ce qui a été fait et comment on se sent.
- Toucher une tuile ouvre une bulle pour écrire ; OK la referme.
- « + Ma tuile » range la tuile dans la couleur en cours ; gestion par couleur dans Réglages.
- Pastille blanche : « Valider direct ».
- Stats : toutes les tuiles du mois comptées une par une, en quatre groupes.

## v1.4 — 16 nov. 2026
- La pastille se remplit écran par écran : Qui ? → Elle (ce qu'elle a fait, comment elle se sent, note) → Moi (pareil), ou Moi d'abord si on choisit « Moi ». « Passer » quand il n'y a rien.
- Nouveau : comment elle se sent, note sur elle et ses propres photos.
- Tuiles vierges au départ, sauf Critique · Mépris · Défensive · Mur.
- Barre d'étapes en haut pour revenir sur un écran ; le brouillon rouvre sur le bon écran.
- Les anciens moments restent intacts.

## v1.3 — 16 nov. 2026
- La pastille s'ouvre en page plein écran, réorganisée : Elle (ce qu'elle a fait) · Moi (comment je me sens) · « Et moi, ce que j'ai fait » (replié) · Raconter (texte, besoin, photos, replié) · Qui ? en bas.
- Brouillon automatique : si on quitte l'appli en pleine saisie, elle rouvre la pastille là où on en était (après le code).
- L'appli se rouvre sur le même onglet et le même jour.
- Titres corrigés (« Ligne franchie » au lieu de « Moment noire ») et dates abrégées propres (« 16 nov. »).

## v1.2 — 16 nov. 2026
- Noms de fichiers clairs et datés : `Umoral_sauvegarde_AAAA-MM-JJ_HHhMM.json`, `Umoral_bilan_semaineNN_du_au.txt`, `Umoral_bilan_mois-année.txt`.
- Appli mise en ligne sur GitHub Pages.

## v1.1 — 16 nov. 2026
- Fermer une pastille ou une note sans valider demande confirmation (avant : tout était perdu d'un tap à côté).
- Changer le code demande d'abord l'ancien code.
- Les photos ajoutées ne consomment plus de mémoire à chaque retouche de l'écran.
- L'appli demande au téléphone de ne pas effacer ses données (stockage persistant).
- Ajout d'un test automatique (`tests/smoke.py`), du cahier des charges (`SPEC.md`) et de ce journal.

## v1 — 16 nov. 2026
Première version complète : PIN, Livre, pastilles, Noires, Stats, Bilans, Réglages, sauvegarde.

## À faire plus tard
- Affiner les tuiles de base à l'usage ; creuser le vert et le blanc.
- Page « Non » du rattrapage (idée à venir).
- Voir si « Ça s'est réparé ? » reste utile à côté du rattrapage.
- Icône d'écran d'accueil (PNG) et fonctionnement hors connexion (service worker) au moment de la mise en ligne.
- Design (plus tard, à sa demande).
