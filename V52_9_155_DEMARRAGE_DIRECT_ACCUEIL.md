# V52.9.155 — Démarrage direct accueil

Objectif : supprimer la dernière page intermédiaire entre le splash Android/PWA et l'accueil JEPALYS.

Cause : le sélecteur de profils historique (`#profile-launcher`) pouvait être peint brièvement et le bloc V50.2 le ré-ouvrait explicitement au chargement.

Correction : sélecteur caché structurellement au boot + autorité de premier rendu portée par `<html>` jusqu'au premier affichage stable de l'accueil.

Les écrans Préparer et Itinéraire prêt sont volontairement inchangés dans cette passe.
