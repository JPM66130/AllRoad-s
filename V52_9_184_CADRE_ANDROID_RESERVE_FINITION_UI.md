# V52.9.184 — Cadre Android réservé + finition UI

- Règle figée : Android peut afficher/masquer ses barres, JEPALYS conserve la même géométrie.
- Une réserve système est mémorisée par orientation dans localStorage et réutilisée aux lancements suivants.
- Si les barres Android sont masquées, leur place est recréée dans le viewport JEPALYS ; si elles sont visibles, aucune double marge n’est ajoutée.
- Le clavier ne redimensionne plus la page métier : seule la bulle de saisie apparaît au-dessus du clavier.
- La bulle n’existe jamais clavier fermé et la validation principale reste la touche Entrée/✓ du clavier.
- Accueil paysage resserré : suppression de la rangée basse vide, cartes et marges compactées sans modifier le contenu métier.
- Gestion véhicule paysage : panneaux resserrés et scroll interne propre, sans chevauchement.
- GPS, routage, carte et conduite non modifiés.
