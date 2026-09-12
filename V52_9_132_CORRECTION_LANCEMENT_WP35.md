# V52.9.132 — CORRECTION LANCEMENT WP35

- Recherche fantôme 130 → 131 : la correction cartographique 131 n'empêchait pas le serveur de démarrer.
- Cause exacte du non-lancement automatique WP35 : le lanceur 131 attendait `/version = V52.9.131`, alors que l'autorité serveur `APP_VERSION` reste volontairement `V52.9.102`. La condition ADB ne pouvait donc jamais devenir vraie.
- Nettoyage : le lanceur vérifie de nouveau la version moteur réellement exposée (`V52.9.102`) avant d'ouvrir l'application sur le WP35.
- La correction 131 de persistance du fond cartographique est conservée sans autre modification.
- Aucun changement GPS, routage, caméra, horizon ou rendu de route.
