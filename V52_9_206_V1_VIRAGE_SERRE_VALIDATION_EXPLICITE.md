# V52.9.206 — V1 Virage Serré — validation explicite

- Destination : bouton **Valider** visible pendant la saisie.
- Entrée Android : même autorité de validation que le bouton.
- Formulaires multi-champs : Entrée avance au champ suivant ; dernier champ = Enregistrer.
- ID véhicule / Mes tournées : les boutons d’appel restent au-dessus du panneau ouvert et restent accessibles.
- Correction de l’attribut `hidden` : un bouton masqué ne reste plus visible à cause de `display:flex`.
- Piéton : itinéraire uniquement, aucune gestion véhicule/tournée.
- Vélo / Moto : mode professionnel léger (ID + tournées), sans caractéristiques de gabarit lourd.
- Profils routiers : gestion véhicule complète.
- Architecture inchangée : Accueil + Conduite uniquement.
- Moteur stable inchangé : V52.9.102.
