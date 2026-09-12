# J234 — Simulation GPS robuste + HUD anti-chevauchement

- Base : J233, sans toucher à J227 secours.
- Simulation sans GPS : durée recoupée entre donnée calculée, durée visible et géométrie réelle ; garde-fous physiques pour empêcher une fin instantanée.
- Position simulée : progression continue sur le vrai tracé, état diagnostic exposé dans `window.__allroadsRouteSimulationState`.
- HUD : recalage dynamique des commandes cartographiques et du compteur vitesse après resize/orientation afin d'éviter les chevauchements entre fenêtres flottantes.
- GPS réel, routage, accueil et clavier inchangés.
