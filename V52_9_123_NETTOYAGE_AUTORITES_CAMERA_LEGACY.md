# V52.9.123 — Nettoyage des autorités caméra legacy

Objectif : empêcher toute commande cartographique historique de reprendre la main pendant la conduite mobile GPS réelle.

## Fantômes identifiés

Trois chemins historiques pouvaient encore appeler directement Leaflet en dehors de l’autorité E7 :

1. le sélecteur d'ancienne perspective (`setMapPerspective`) via `setView` / `fitBounds` ;
2. l'ancien lanceur de simulation/cockpit (`navLaunchButton`) via `setZoom`, `panTo` puis `setView` à chaque frame ;
3. le bouton de localisation legacy (`ar51-locate`) via un `setView(..., 15)` direct.

Ces chemins ne sont pas nécessaires à la conduite mobile réelle et pouvaient, s'ils étaient déclenchés, écraser le centre ou le zoom calculés par `focusDrivingRoute()`.

## Nettoyage

Ajout d'un garde unique `arE7MobileDrivingOwnsCamera()` : lorsque l'application est ouverte en conduite mobile réelle (`driving`, `incident`, `turnaround`), ces anciens chemins ne peuvent plus écrire directement dans la caméra. Ils rendent la main à `focusDrivingRoute()`.

Aucune modification GPS, géocodage, routage, géométrie d'itinéraire ou style du ruban bleu.
