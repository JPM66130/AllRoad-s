// Référence historique de compatibilité tests : VERSION='52.9.235' ; jepalys-v52-9-220
const VERSION='52.9.240';
const CACHE='jepalys-v52-9-240-final';
const ASSETS=['/app/icon-192.png','/app/icon-512.png'];
self.addEventListener('install',event=>{
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)));
});
self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)));
    await self.clients.claim();
    // V52.9.60 : aucune navigation forcée des fenêtres ouvertes. Le précédent
    // c.navigate() pouvait provoquer un rechargement visible plusieurs secondes
    // après l'ouverture de la PWA. La coque est déjà réseau-first et versionnée.
    const clients=await self.clients.matchAll({type:'window',includeUncontrolled:true});
    await Promise.all(clients.map(c=>c.postMessage({type:'ALLROADS_SW_READY',version:VERSION}).catch(()=>null)));
  })());
});
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET') return;
  const url=new URL(event.request.url);
  if(url.origin===self.location.origin && (url.pathname==='/app/' || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/manifest.webmanifest') || url.pathname.endsWith('/sw.js'))){
    // Jamais de document/manifest/SW ancien : réseau obligatoire.
    event.respondWith(fetch(event.request,{cache:'no-store'}));
    return;
  }
  event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)));
});
