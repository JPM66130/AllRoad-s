# V52.9.209 — Clavier JEPALYS : couche de frappe dédiée

- Base : J208.
- Constat WP35 : aucune saisie n’ouvrait le clavier JEPALYS malgré la délégation globale.
- Nettoyage conservé : aucune réactivation du clavier Android natif.
- Chaque champ JEPALYS reçoit désormais une surface tactile dédiée, posée directement au-dessus du champ, qui appelle l’autorité unique `openBoundEditable()` ; le déclenchement ne dépend plus du comportement d’un champ HTML `readonly` sous Android.
- Les champs dynamiques ID, caractéristiques, tournées et destination passent tous par le même mécanisme.
- Jeton de lancement et service worker portés à J209 pour exclure une ancienne page/cache.
- GPS, routage, carte et conduite inchangés.
