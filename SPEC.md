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
- Page de la pastille (plein écran) : Elle · ce qu'elle a fait (tuiles annotées) ; Moi · comment je me sens (tuiles) ; « Et moi, ce que j'ai fait » replié (tuiles annotées + J'ai pris l'air) ; « Raconter » replié (ce qui s'est passé, besoin, photos) ; Qui ? en bas, facultatif.
- Brouillon automatique : on retrouve la saisie en cours après avoir quitté l'appli.
- Ancienne description : 3 questions douces facultatives (Qu'est-ce qui s'est passé ? Comment te sens-tu ? De quoi tu aurais eu besoin ?), tuiles de ressenti, « Qui ? Elle / Moi / Les deux », sections « Elle » et « Moi » avec tuiles (Critique, Mépris, Défensive, Mur, Colère…) et une annotation par tuile, « J'ai pris l'air », photos.
- Il peut créer ses propres tuiles.
- Garde-fou : Mépris ou Insulte sur une pastille sous le rouge → « Ce serait plutôt une rouge ? » (suggestion seulement).
- Pastille validée : modifier le contenu, changer la couleur, supprimer.

## Livre
Une page par jour, datée, qui change toute seule. Pastilles en haut, liste des moments, notes séparées avec l'heure automatique. Le lendemain d'une 🔴/⚫ : « Ça s'est réparé ? Oui / En partie / Non ».

## Noires
Liste de toutes les noires (date, texte, étiquettes, réparation).

## Stats
- Mois : calendrier coloré, filtre par couleur, toucher un jour ouvre sa page.
- Résumé : ratio bons/mauvais (⚪=2, 🟢=1 / 🟠=1, 🔴=2) avec repère Gottman 5 pour 1 ; noires comptées à part, jamais compensées ; colonnes colorées par semaine avec chiffres à gauche ; 4 cavaliers Elle/Moi (mépris mis en avant) ; Qui ? ; Réparé ? ; ressentis.

## Bilans
Résumé automatique par semaine et par mois + bouton qui exporte un fichier texte de la période seulement, à envoyer à Claude pour débriefer.

## Rappels
- « Pense à toi » dans l'appli : 3 jours mauvais de suite ou 2 noires en 7 jours.
- Rappel du soir à heure réglable : impossible seul en appli web → automatisation Raccourcis expliquée dans les réglages.

## Sauvegarde
Bouton « Sauvegarder tout » → menu de partage → Enregistrer dans Fichiers (dossier Umoral). Restauration possible.
- Tous les fichiers exportés ont un nom clair et daté (sauvegardes et bilans).
