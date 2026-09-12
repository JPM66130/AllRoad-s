# V52.9.58 — panneau compact + stabilité WP35

- Portrait : la poignée de `Préparer le trajet` sort du flux et le fronton est compacté pour rejoindre le gabarit visuel de `Itinéraire prêt`.
- La marge basse standard validée reste à 6 px.
- Suppression de la navigation forcée `clients.navigate()` lors de l'activation du service worker : elle pouvait provoquer un rechargement visible différé.
- Le pont de banc `/test-bridge/sync` ne sonde plus toutes les 3 secondes en usage conducteur ; il ne s'active qu'avec `?testbridge=1`.
- Mise à jour PWA conservée réseau-first, cache versionné V52.9.58, sans désinstallation de l'application.
- Lanceur ADB ciblé conservé.

Validation atelier : suite complète + groupes navigation/chauffeur/data_route + géographie + syntaxe JS/SW + smoke serveur avant ZIP.
