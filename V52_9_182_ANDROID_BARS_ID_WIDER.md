# JEPALYS V52.9.182 — Barres Android + deux accueils harmonisés

## Modifications
- Pastille d’identification légèrement élargie sans augmenter sa hauteur.
- Les barres système Android sont intégrées comme limites normales de l’écran ; la coque suit la zone réellement disponible au lieu de dépendre du plein écran immersif.
- Deux compositions d’accueil harmonisées, en portrait et paysage :
  - avec « Mon véhicule sélectionné » pour Voiture, Utilitaire, Camping-car, Bus et Poids lourd ;
  - sans ce bloc pour Piéton, Vélo et Moto.
- Quand le bloc véhicule est absent, l’espace est redistribué : aucun trou vide n’est conservé.
- Le style général, les cartes profils, les cartes promotionnelles, les marges et les actions restent communs aux deux accueils.

## Non modifié
GPS, routage, calcul d’itinéraire, conduite et caméra.

## Étape suivante après validation
Fusion des deux fenêtres déjà convenue avec Jean-Paul.


## Correctif lanceur V182
- Le lanceur ne modifie plus `settings global policy_control` : diagnostic Android en lecture seule uniquement.
- Fichier BAT réécrit sans BOM UTF-8 pour garantir `@echo off` sous Windows CMD.
- Aucun changement GPS, routage, carte ou conduite.
