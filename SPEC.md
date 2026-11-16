# Umoral — cahier des charges

Journal personnel pour noter les moments d'une relation et y voir clair. Soutien émotionnel pour rationaliser : l'appli invite à écrire, on se laisse porter.

## Règles de fond
- Appli web iPhone, un seul fichier `index.html`, publiée sur GitHub Pages avec une URL longue et introuvable.
- Tout reste sur le téléphone (IndexedDB). Rien n'est envoyé sur Internet.
- Code PIN à 4 chiffres à l'ouverture.
- Fond sombre. Le reste du design se verra plus tard.
- Ne jamais changer un point validé sans l'accord du propriétaire.

## Pastilles
⚪ blanche = journée parfaite · 🟢 bon moment · 🟠 tendu · 🔴 difficile · ⚫ noire = elle est allée trop loin (argument pour la rupture).
- La noire n'écrase pas les autres couleurs de la journée.
- Un clic ouvre toujours l'écran de la pastille, il faut « Valider » (on peut valider vide et compléter plus tard).
- Page de la pastille (plein écran), un écran par choix : « Qui ? » (Elle / Moi / Les deux) → partie de la personne choisie (« Les deux » : Elle d'abord), puis l'autre. Elle : ce qu'elle a fait (tuiles) → note (texte, photos). Pas d'écran « comment elle se sent » : on ne peut pas savoir à sa place. Moi : ce que j'ai fait (tuiles ; « J'ai pris l'air » en orange seulement) → comment je me sens (tuiles) → note (texte, « De quoi j'aurais eu besoin ? », photos). Sur chaque écran : choisir, ou « Passer ». Barre d'étapes en haut pour sauter d'un écran à l'autre. Valider au dernier écran (avec couleur, réparation, suppression pour un moment déjà enregistré).
- « Qui ? Elle » : côté Moi, l'écran « Ma réaction » remplace « Ce que j'ai fait » : couleur de la réaction (⚪🟢🟠🔴⚫, indépendante de la pastille) puis tuiles de cette couleur (bulle commentaire, « + Ma tuile »), puis « Comment je me sens », puis note et photos à la fin. « Les deux » garde « Ce que j'ai fait ». Stats : « Elle 🔴 → moi 🟢 : n fois ».
- Dernier écran sur 🟠🔴⚫ : « Elle s'est rattrapée ? » Oui / Non. Oui → pour chaque tuile côté Elle : ⚪ totalement · 🟢 le gros · 🟠 un peu, + texte « Comment ? ». Non → page dédiée à définir plus tard. Bouton ↺ sur chaque moment du Livre pour l'ajouter après coup.
- Case « Devant [prénom] » sur 🟠🔴⚫ (écran Qui ?), prénom réglé dans Réglages et stocké sur le téléphone seulement ; comptée dans les stats et les bilans.
- Tuiles d'accusation : 🟠 Mauvaise interprétation · 🔴 Accusation · ⚫ Accusation grave.
- L'appli sert surtout à gérer le négatif ; le vert et le blanc seront creusés plus tard.
- Brouillon automatique : on retrouve la saisie en cours, sur le même écran, après avoir quitté l'appli.
- Tuiles de base triées par couleur : une pastille ne propose que celles de sa couleur. « Ce qu'elle a fait / ce que j'ai fait » = ce qui a été dit ou fait ; « comment elle se sent / je me sens » = ressentis (le stress est un ressenti). ⚪ et 🟢 : positif · 🟠 : petits accrocs (oubli, petit reproche, vaisselle, téléphone… / stress, ennui, flemme…) · 🔴 : prise de tête, communication risquée, risque d'engueulade, Critique, Défensive, Mur… / gros stress, tendu… · ⚫ : Mépris, Insultes / Humiliation, Phrase de trop, Reproches, Laisser tomber, Menace (Moi : + Éloignement urgent) / stress énorme… Liste exacte dans `TILES` (index.html).
- Toucher une tuile ouvre une bulle (texte moyen + OK) ; OK la referme et on revient aux tuiles. Retoucher une tuile allumée rouvre son texte, avec « Retirer ».
- « + Ma tuile » crée une tuile pour la couleur et l'écran en cours ; on les retire dans Réglages. Les tuiles d'un ancien moment restent affichées.
- ⚪ : bouton « Journée parfaite · Valider direct » sur le premier écran.
- Il peut créer ses propres tuiles.
- Garde-fou : Mépris ou Insulte sur une pastille sous le rouge → « Ce serait plutôt une rouge ? » (suggestion seulement).
- Pastille validée : modifier le contenu, changer la couleur, supprimer.

## Livre
Une page par jour, datée, qui change toute seule. Pastilles en haut, liste des moments, notes séparées avec l'heure automatique. Le lendemain d'une 🔴/⚫ : « Ça s'est réparé ? Oui / En partie / Non ».

- Sous le cadre Moments : bouton « Supprimer des moments » → case à cocher devant chaque moment → « Supprimer (n) » / « Annuler » → confirmation « C'est définitif ».

- ⚡ Note rapide en haut du Livre : on écrit sur le coup (heure auto), elle va dans « À trier » (tous jours confondus). En la touchant : choisir une couleur → la pastille s'ouvre avec le texte dans « Note sur elle », à la même date et heure ; une fois validée, la note disparaît de « À trier ». On peut aussi la garder ou la supprimer.

## Je vais
Onglet entre Stats et Bilans. Noter ce qui est annoncé : Elle / Moi, texte, importance obligatoire (gris neutre · 🟠 important · 🔴 urgent), jour (Aujourd'hui · Demain par défaut · Autre date).
- À l'ouverture, à partir de l'heure du rappel du soir (et pour tout ce qui est en retard) : « Est-ce qu'elle l'a fait ? / Est-ce que tu l'as fait ? » Oui (fait, barré, dans l'historique) · Non (reporté au lendemain, compteur de reports) · Laisser tomber (zone « Paroles en l'air »). « Plus tard » remet à la prochaine ouverture.
- Laisser tomber aussi en touchant l'élément, à tout moment.
- Historique, Paroles en l'air, filtre Elle / Moi, stats propres (indépendantes des pastilles) ; présent dans les bilans et l'export.

## Noires
Liste de toutes les noires (date, texte, étiquettes, réparation).

## Stats
- Mois : calendrier coloré, filtre par couleur, toucher un jour ouvre sa page.
- Résumé : ratio bons/mauvais (⚪=2, 🟢=1 / 🟠=1, 🔴=2) avec repère Gottman 5 pour 1 ; noires comptées à part, jamais compensées ; colonnes colorées par semaine avec chiffres à gauche ; 4 cavaliers Elle/Moi (mépris mis en avant) ; Qui ? ; Réparé ? ; toutes les tuiles comptées une par une (ce qu'elle a fait, comment elle se sent, ce que j'ai fait, comment je me sens).

## Bilans
Résumé automatique par semaine et par mois + bouton qui exporte un fichier texte de la période seulement, à envoyer à Claude pour débriefer.

## Rappels
- « Pense à toi » dans l'appli : 3 jours mauvais de suite ou 2 noires en 7 jours.
- Rappel du soir à heure réglable : impossible seul en appli web → automatisation Raccourcis expliquée dans les réglages.

## Sauvegarde
Bouton « Sauvegarder tout » → menu de partage → Enregistrer dans Fichiers (dossier Umoral). Restauration possible.
- Tous les fichiers exportés ont un nom clair et daté (sauvegardes et bilans).
