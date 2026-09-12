# V52.9.33 — Routage grand gabarit fail-safe

Objectif : empêcher AllRoad’s de présenter comme sûre une route calculée par un moteur automobile de secours pour un Bus, Utilitaire, Camping-car ou Poids lourd.

- Une route ORS `driving-hgv` avec contraintes de véhicule peut autoriser le guidage réel, tout en conservant l’obligation de vérifier la signalisation sur place.
- Une route GraphHopper/OSRM automobile ou une estimation directe peut rester visible à titre informatif, mais `guidage_autorise=false` pour un grand véhicule.
- L’interface désactive techniquement le bouton de démarrage GPS, affiche `NON GARANTI` et explique que le gabarit n’est pas garanti.
- Voiture et profils légers conservent leurs secours habituels.
- Le lanceur a été corrigé : le paramètre anti-cache de l’adresse WP35 utilise désormais automatiquement la version du paquet V52.9.33 au lieu de l’ancien `52.9.29`.

Principe de sécurité : en cas d’incertitude sur la compatibilité de gabarit, AllRoad’s informe mais n’autorise pas un guidage réel présenté comme sûr.
