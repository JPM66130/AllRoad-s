# V52.9.53 — PWA / ADB mise à jour fiable

- Le lanceur choisit explicitement une cible ADB, avec priorité à la cible TCP/IP, afin de ne plus échouer quand le même WP35 apparaît aussi via mDNS.
- `adb reverse` est appliqué avec `-s <serial>` : plus d'ambiguïté « more than one device/emulator ».
- Le manifeste PWA démarre désormais explicitement sur la version courante.
- Le service worker ne met plus en cache le document principal, le manifeste ni le service worker lui-même.
- À l'activation d'un nouveau service worker, les fenêtres PWA ouvertes sont renaviguées vers le document courant.
- L'enregistrement du service worker utilise `updateViaCache: none` et demande une vérification de mise à jour.
- L'icône PWA existante est conservée : aucune désinstallation/réinstallation n'est requise.
