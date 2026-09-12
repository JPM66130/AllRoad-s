# V52.9.60 — coque figée / ordre cartographique unique

- Rejet du mode standalone V58 qui amplifiait les sauts WP35.
- Retour PWA fullscreen prioritaire avec standalone en repli.
- Une seule hauteur de coque capturée au démarrage ; les variations des barres système Android ne redimensionnent plus AllRoad’s.
- Recalcul de la coque uniquement sur vraie rotation. Le contrôleur visualViewport reste réservé au clavier.
- Header ancré au bord utile du viewport avec une marge fixe de 6 px, sans double safe-area.
- Ordre standard cartographique partout : Header → Carte/Relief/Satellite → guidage éventuel → carte.
- Suppression de l’espace mort haut en conduite.
- Écran véhicule V58 conservé comme référence validée.
