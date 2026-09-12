# Audit Conduire — V52.9.104 à V52.9.107

## Cause principale trouvée

Les versions successives ont empilé de nouvelles règles CSS sur des dizaines de règles historiques déjà actives pour les mêmes composants (`.ar51-topbar`, `.ar51-maneuver`, `.ar525-mapviews`, `.ar51-center-map`, `.ar52967-speed`). Le résultat dépendait de la cascade CSS au lieu d'une autorité unique.

## Incohérences concrètes

- Le fichier de la 107 contient 37 occurrences visant `.ar52967-speed`, 43 pour `.ar525-mapviews`, 34 pour `.ar51-center-map`, 37 pour `.ar51-topbar` et 48 pour `.ar51-maneuver`.
- Les correctifs 104/105/106/107 se contredisent sur les mêmes propriétés : `top`, `bottom`, `width`, `height`, `display`, `transform`, `grid-template-columns`.
- Le bloc 107 a été écrit avec des séquences littérales `\n` dans le HTML/CSS, ce qui rend ce correctif mal formé et explique pourquoi une partie des règles n'était pas interprétée comme prévu.
- Les blocs 105/106 ont aussi été empilés sans retirer l'ancienne autorité visuelle, donc les anciennes règles continuaient à influencer le rendu WP35.

## Décision

Repartir de V52.9.102, dernière base visuellement validée et fonctionnelle, sans embarquer les blocs expérimentaux 103–107. Ajouter un seul bloc d'autorité visuelle pour Conduire, avec dimensions explicites pour les composants qui se déformaient. GPS, géocodage et routage restent intacts.
