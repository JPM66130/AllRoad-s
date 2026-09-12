# V52.9.76 — correction de cause + démo vitesse

- Cause V66/V67 identifiée : les règles nouvelles étaient insérées avant des blocs CSS historiques situés après `</html>` ; ces blocs reprenaient l’autorité sur le WP35.
- V68 place une autorité finale au véritable EOF des deux frontends.
- Conduite portrait/paysage : ALLROAD’S → Carte/Relief/Satellite → 450 m → carte.
- Véhicule paysage : panneau compact et CTA visible sans scroll.
- Démo sans GPS : 68 → 73 → 75 → 73 → 68 km/h, 5 s par palier, limite 70 km/h, pour valider blanc → orange → rouge → orange → blanc.
- Sélecteur standard vitesse : curseur coulissant km/h ↔ mph, mémorisé globalement.
