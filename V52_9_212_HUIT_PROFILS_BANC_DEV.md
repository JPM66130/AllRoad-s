# V52.9.212 — 8 profils cohérents sur le banc développeur

## Cause racine
Le frontend de développement forçait déjà l’accès visuel aux 8 profils, mais le serveur démarrait sans variable d’accès et retombait donc sur l’état TEST, où seuls `voiture` et `bus` sont déverrouillés. Les autres appels `/itineraire/calcul` étaient correctement refusés en `403 PROFILE_LOCKED`.

## Correction
Le lanceur principal WP35 démarre désormais le serveur avec `ALLROADS_ACCESS_STATE=PRO` et `ENVIRONMENT=development`. Cela aligne le banc local sur son objectif de validation des 8 profils.

## Sécurité commerciale conservée
La valeur par défaut du serveur reste `TEST`. Sans le lanceur développeur, seuls Voiture et Bus sont déverrouillés comme prévu pour le lancement initial.

## Hors périmètre
Aucun changement GPS, géocodage, moteur de routage, sécurité HGV, carte, conduite ou clavier JEPALYS.
