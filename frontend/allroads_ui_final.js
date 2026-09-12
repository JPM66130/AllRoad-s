/* ALLROAD'S V52.9.94 — SOURCE D'AUTORITE COMPORTEMENT UI UNIQUE */
(()=>{
 'use strict';
 const ROOT=()=>document.getElementById('ar-mobile-nav');
 const docEl=document.documentElement;
 const KEY='allroads-theme-mode';
 const RECOVERY_DELAY=4000;
 let resizeTimer=0,recoveryTimer=0,lastOrientation='';
 const coarsePointer=()=>window.matchMedia&&window.matchMedia('(pointer:coarse)').matches;
 const standalone=()=>window.matchMedia('(display-mode: standalone)').matches||window.matchMedia('(display-mode: fullscreen)').matches||window.navigator.standalone===true;
 const valid=m=>['day','auto','night'].includes(m)?m:'auto';
 function autoNight(){
   /* Fallback local déterministe. La future couche solaire GPS remplacera ce fallback. */
   const h=new Date().getHours(); return h<7||h>=20;
 }
 function isNight(mode){return mode==='night'||(mode==='auto'&&autoNight())}
 function ensureOverlay(){
   const map=document.getElementById('map'); if(!map)return;
   let o=document.getElementById('ar52977-night-overlay');
   if(!o){o=document.createElement('div');o.id='ar52977-night-overlay';o.setAttribute('aria-hidden','true');map.appendChild(o)}
 }
 function ensureSwitch(){
   const r=ROOT();if(!r)return;
   let d=r.querySelector('.ar52977-theme-switch');
   if(!d){d=document.createElement('div');d.className='ar52977-theme-switch';d.setAttribute('role','group');d.setAttribute('aria-label','Affichage jour ou nuit');d.innerHTML='<button type="button" data-theme-mode="day">Jour</button><button type="button" data-theme-mode="auto">Auto</button><button type="button" data-theme-mode="night">Nuit</button>';r.appendChild(d)}
 }
 function applyTheme(mode){
   mode=valid(mode||localStorage.getItem(KEY)||'auto'); localStorage.setItem(KEY,mode);
   const night=isNight(mode);document.body.classList.toggle('ar-night',night);document.documentElement.dataset.arTheme=night?'night':'day';
   document.querySelectorAll('.ar52977-theme-switch [data-theme-mode]').forEach(b=>{const on=b.dataset.themeMode===mode;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on?'true':'false')});
   ensureOverlay();
 }
 function setTheme(mode){applyTheme(valid(mode))}
 function normalizeVehicleSelection(){
   document.querySelectorAll('.ar52-card.selected').forEach(card=>{
     const check=card.querySelector('.ar52-selected-check');
     const actions=card.querySelector('.ar52-card-actions');
     if(check&&actions&&check.parentElement!==actions)actions.appendChild(check);
   });
 }
 function layoutSize(){
   /* Autorité = layout viewport. visualViewport varie lors d'un pinch-zoom ou avec les barres Android. */
   const w=Math.max(1,Math.round(window.innerWidth||docEl.clientWidth||1));
   const h=Math.max(1,Math.round(window.innerHeight||docEl.clientHeight||1));
   return {w,h,orientation:w>=h?'landscape':'portrait'};
 }
 function adaptScreen(){
   const {w,h,orientation}=layoutSize();
   const short=Math.min(w,h), long=Math.max(w,h);
   const size=short<380?'compact':short<520?'phone':short<760?'large':'tablet';
   docEl.dataset.arSize=size;
   docEl.dataset.arOrientation=orientation;
   docEl.style.setProperty('--ar-screen-w',w+'px');
   docEl.style.setProperty('--ar-screen-h',h+'px');
   docEl.style.setProperty('--ar-screen-short',short+'px');
   docEl.style.setProperty('--ar-screen-long',long+'px');
   lastOrientation=orientation;
 }
 function recoverFrame(){
   /* Ne jamais interrompre une saisie ou une action critique de conduite. */
   const active=document.activeElement;
   if(active&&/^(INPUT|TEXTAREA|SELECT)$/.test(active.tagName))return;
   const r=ROOT();
   const state=r?.dataset?.state||'';
   if(['incident','turnaround'].includes(state))return;
   if(window.scrollX||window.scrollY)window.scrollTo(0,0);
   document.body.style.removeProperty('zoom');
   docEl.style.removeProperty('zoom');
   adaptScreen();
   normalizeVehicleSelection();
 }
 function scheduleRecovery(){
   clearTimeout(recoveryTimer);
   recoveryTimer=setTimeout(recoverFrame,RECOVERY_DELAY);
 }
 function handleResize(){
   const {orientation}=layoutSize();
   clearTimeout(resizeTimer);
   /* Mobile/PWA : les variations de même orientation viennent le plus souvent des barres système.
      PC : un vrai redimensionnement de fenêtre doit rester adaptatif. */
   if((standalone()||coarsePointer())&&lastOrientation&&orientation===lastOrientation){scheduleRecovery();return;}
   resizeTimer=setTimeout(()=>{
     adaptScreen();
     if(window.AllRoadsShell61?.recapture)window.AllRoadsShell61.recapture();
     scheduleRecovery();
   },260);
 }
 function handleOrientation(){
   clearTimeout(resizeTimer);
   resizeTimer=setTimeout(()=>{adaptScreen();if(window.AllRoadsShell61?.recapture)window.AllRoadsShell61.recapture();scheduleRecovery();},620);
 }

 const vehicleProfile=()=>{
   const raw=(document.getElementById('ar52-profile')?.textContent||document.getElementById('profil')?.value||'bus').toLowerCase();
   return raw.includes('camping')?'camping_car':raw.includes('poids')?'poids_lourd':raw.includes('utilitaire')?'utilitaire':raw.includes('bus')?'bus':raw.replace(/[^a-z_]/g,'');
 };
 const vehicleStoreKey=p=>`allroads-vehicles-v52-${p}`;
 const vehicleActiveKey=p=>`allroads-vehicles-v52-active-${p}`;
 function readVehicles(p){try{return JSON.parse(localStorage.getItem(vehicleStoreKey(p))||'[]')}catch(_){return[]}}
 function writeVehicles(p,v){try{localStorage.setItem(vehicleStoreKey(p),JSON.stringify(v.slice(0,5)))}catch(_){}}
 function normalizeIdentifier(v){return String(v||'').trim().toUpperCase().replace(/\s+/g,' ')}
 function activeVehicle(){const p=vehicleProfile(),list=readVehicles(p),id=localStorage.getItem(vehicleActiveKey(p));return {profile:p,list,vehicle:list.find(v=>v.id===id)||null}}
 function ensureVehicleIdentification(){
   const editor=document.getElementById('ar52-editor'); if(!editor)return;
   let box=document.getElementById('ar83-vehicle-id-box');
   if(!box){
     box=document.createElement('section');box.id='ar83-vehicle-id-box';box.className='ar83-vehicle-id';box.setAttribute('aria-label','Identification du véhicule');
     box.innerHTML='<div class="ar83-vehicle-id-title">Identification du véhicule</div><label>Identifiant / n° de parc<input id="ar83-vehicle-id" maxlength="40" autocomplete="off" placeholder="Ex. 331241"></label><button id="ar83-vehicle-load" type="button">Valider</button><div id="ar83-vehicle-id-status" class="ar83-vehicle-id-status">Saisissez un identifiant connu pour charger automatiquement son gabarit.</div>';
     editor.parentNode.insertBefore(box,editor);
     const input=box.querySelector('#ar83-vehicle-id'); const load=box.querySelector('#ar83-vehicle-load');
     input.setAttribute('enterkeyhint','done'); input.setAttribute('inputmode','text');
     const doIdentify=()=>identifyOrAssignVehicle(input.value);
     load.addEventListener('click',doIdentify);input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();doIdentify()}});
   }
   syncVehicleIdentifier();
 }
 function setVehicleIdStatus(text,kind=''){const s=document.getElementById('ar83-vehicle-id-status');if(!s)return;s.textContent=text;s.className='ar83-vehicle-id-status'+(kind?' '+kind:'')}
 function syncVehicleIdentifier(){
   const input=document.getElementById('ar83-vehicle-id');if(!input)return;
   const {vehicle}=activeVehicle();
   if(document.activeElement!==input)input.value=vehicle?.identifier||'';
   if(vehicle?.identifier)setVehicleIdStatus(`Véhicule identifié : ${vehicle.identifier}`,'ok');
 }
 function loadVehicleByIdentifier(raw){
   const identifier=normalizeIdentifier(raw); if(!identifier){setVehicleIdStatus('Saisissez un identifiant de véhicule.','warn');return false}
   const p=vehicleProfile(),list=readVehicles(p);const found=list.find(v=>normalizeIdentifier(v.identifier)===identifier);
   if(!found){setVehicleIdStatus(`Identifiant ${identifier} inconnu : sélectionnez/configurez le véhicule puis enregistrez-le pour l’associer.`,'warn');return false}
   localStorage.setItem(vehicleActiveKey(p),found.id);
   if(window.AllRoadsVehicleGarage?.open)window.AllRoadsVehicleGarage.open(p);
   setTimeout(()=>{const input=document.getElementById('ar83-vehicle-id');if(input)input.value=identifier;setVehicleIdStatus(`Identifiant ${identifier} reconnu : caractéristiques chargées automatiquement.`,'ok');normalizeVehicleSelection()},0);
   return true;
 }
 function identifyOrAssignVehicle(raw){
   const identifier=normalizeIdentifier(raw); if(!identifier){setVehicleIdStatus('Saisissez un identifiant de véhicule.','warn');return false}
   const p=vehicleProfile(),list=readVehicles(p),activeId=localStorage.getItem(vehicleActiveKey(p))||localStorage.getItem(`allroads-vehicles-v52-default-${p}`)||list[0]?.id||'';
   const found=list.find(v=>normalizeIdentifier(v.identifier)===identifier);
   if(found){
     localStorage.setItem(vehicleActiveKey(p),found.id);
     setVehicleIdStatus(`Identifiant ${identifier} reconnu : véhicule chargé.`,'ok');
     setTimeout(()=>{syncVehicleIdentifier();normalizeVehicleSelection();syncVehicleSummaryIdentifier();window.AllRoadsHome177?.refresh?.()},0);
     return true;
   }
   if(!activeId){setVehicleIdStatus('Sélectionnez d’abord un véhicule à identifier.','warn');return false}
   let changed=false;
   const next=list.map(v=>v.id===activeId?(changed=true,{...v,identifier}):v);
   if(!changed){setVehicleIdStatus('Le véhicule actif est introuvable. Sélectionnez-le à nouveau.','warn');return false}
   writeVehicles(p,next);localStorage.setItem(vehicleActiveKey(p),activeId);
   setVehicleIdStatus(`Identification ${identifier} enregistrée pour ce véhicule.`,'ok');
   setTimeout(()=>{syncVehicleIdentifier();syncVehicleSummaryIdentifier();normalizeVehicleSelection();window.AllRoadsHome177?.refresh?.()},0);
   return true;
 }
 function persistIdentifierAfterVehicleSave(){
   setTimeout(()=>{
     const input=document.getElementById('ar83-vehicle-id');if(!input)return;
     const identifier=normalizeIdentifier(input.value);if(!identifier){syncVehicleIdentifier();return}
     const p=vehicleProfile(),list=readVehicles(p),activeId=localStorage.getItem(vehicleActiveKey(p));
     if(!activeId)return;
     const duplicate=list.find(v=>v.id!==activeId&&normalizeIdentifier(v.identifier)===identifier);
     if(duplicate){setVehicleIdStatus(`Identifiant ${identifier} déjà associé à ${duplicate.name||'un autre véhicule'}.`,'warn');return}
     let changed=false;const next=list.map(v=>v.id===activeId?(changed=true,{...v,identifier}):v);if(changed){writeVehicles(p,next);setVehicleIdStatus(`Identifiant ${identifier} enregistré avec ce véhicule.`,'ok')}
   },0);
 }
 function currentVehicleIdentifier(){return activeVehicle().vehicle?.identifier||''}
 function syncVehicleSummaryIdentifier(){
   const el=document.getElementById('ar51-vehicle-summary');if(!el)return;
   const id=currentVehicleIdentifier();const base=(el.textContent||'').replace(/\s*·\s*ID\s+[^·]+$/,'').trim();
   if(id)el.textContent=`${base} · ID ${id}`;
 }
 function setSpeedUnitFinal(next){
   const unit=next==='mph'?'mph':'kmh';
   if(window.AllRoadsSpeed67?.setUnit)window.AllRoadsSpeed67.setUnit(unit);else localStorage.setItem('allroads-speed-unit',unit);
   const g=document.querySelector('.ar52967-speed-units');if(g)g.dataset.unit=unit==='mph'?'mph':'kmh';
   document.querySelectorAll('.ar52967-speed-units [data-speed-unit]').forEach(b=>{const on=b.dataset.speedUnit===unit;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on?'true':'false')});
 }
 function syncSpeedUnitFinal(){const unit=window.AllRoadsSpeed67?.getState?.().unit||localStorage.getItem('allroads-speed-unit')||'kmh';setSpeedUnitFinal(unit)}

 function ensureDrivingAttribution(){
   const r=ROOT();if(!r)return;
   let a=r.querySelector('.ar-map-attribution-driving');
   if(!a){
     a=document.createElement('div');a.className='ar-map-attribution-driving';a.setAttribute('aria-label','Attribution cartographique');
     a.innerHTML='<a href="https://leafletjs.com" target="_blank" rel="noopener noreferrer">Leaflet</a> | © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap contributors</a> © <a href="https://carto.com/attributions" target="_blank" rel="noopener noreferrer">CARTO</a>';
     r.appendChild(a);
   }
 }
 function enforce(){adaptScreen();ensureSwitch();ensureOverlay();ensureDrivingAttribution();applyTheme();normalizeVehicleSelection();ensureVehicleIdentification();syncSpeedUnitFinal();syncVehicleSummaryIdentifier();scheduleRecovery();}
 document.addEventListener('click',e=>{const b=e.target.closest?.('.ar52977-theme-switch [data-theme-mode]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();setTheme(b.dataset.themeMode)},true);
 document.addEventListener('pointerdown',e=>{const b=e.target.closest?.('.ar52977-theme-switch [data-theme-mode]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();setTheme(b.dataset.themeMode)},{passive:false,capture:true});

 document.addEventListener('pointerdown',e=>{const b=e.target.closest?.('.ar52967-speed-units [data-speed-unit]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();setSpeedUnitFinal(b.dataset.speedUnit)},{passive:false,capture:true});
 document.addEventListener('click',e=>{const b=e.target.closest?.('.ar52967-speed-units [data-speed-unit]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();setSpeedUnitFinal(b.dataset.speedUnit)},true);
 document.getElementById('ar52-save')?.addEventListener('click',persistIdentifierAfterVehicleSave);

 const boot=()=>{enforce();const r=ROOT();if(r)new MutationObserver(enforce).observe(r,{attributes:true,attributeFilter:['data-state']});const v=document.getElementById('ar52-list');if(v)new MutationObserver(normalizeVehicleSelection).observe(v,{childList:true,subtree:true})};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
 window.addEventListener('load',enforce);
 window.addEventListener('resize',handleResize,{passive:true});
 window.addEventListener('orientationchange',handleOrientation,{passive:true});
 ['pointerup','touchend','wheel','scroll'].forEach(ev=>window.addEventListener(ev,scheduleRecovery,{passive:true}));
 window.AllRoadsUIFinal={setTheme,applyTheme,enforce,adaptScreen,recoverFrame,loadVehicleByIdentifier,identifyOrAssignVehicle,currentVehicleIdentifier,setSpeedUnit:setSpeedUnitFinal};
})();
