
// DGO R11.6 Figma UI/UX runtime enhancer: non-invasive, no framework, no endpoint changes.
// Guarded so the module is safely importable in non-browser (diagnostic) contexts.
if (typeof document !== 'undefined' && typeof window !== 'undefined' && typeof MutationObserver !== 'undefined') (function(){
  const root=document.documentElement;
  root.classList.add('dgo-figma-uiux-implemented');
  // R11.6 remediation — keyboard-accessible drawer focus management.
  // Drawers open via [data-open-drawer] are role=dialog/aria-modal but previously
  // received only initial focus. Add a Tab focus-trap and restore focus to the
  // opener on close, matching the shell's palette/dialog behaviour (WCAG 2.1.1, 2.4.3).
  let _drawerOpener=null, _drawerTrap=null, _trappedDrawer=null;
  const focusablesIn=el=>[...el.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])')].filter(x=>x.offsetParent!==null);
  function releaseTrap(){ if(_trappedDrawer&&_drawerTrap){ _trappedDrawer.removeEventListener('keydown',_drawerTrap); } _drawerTrap=null; _trappedDrawer=null; }
  function closeDrawers(){ let hadOpen=false; document.querySelectorAll('.dgo-drawer:not([hidden])').forEach(d=>{ d.hidden=true; hadOpen=true; }); releaseTrap(); if(hadOpen&&_drawerOpener){ try{ _drawerOpener.focus(); }catch{} } _drawerOpener=null; }
  function trapDrawer(d){
    releaseTrap();
    _trappedDrawer=d;
    _drawerTrap=e=>{ if(e.key!=='Tab')return; const f=focusablesIn(d); if(!f.length)return; const first=f[0],last=f[f.length-1],a=document.activeElement;
      if(e.shiftKey){ if(a===first||!d.contains(a)){ e.preventDefault(); last.focus(); } }
      else { if(a===last||!d.contains(a)){ e.preventDefault(); first.focus(); } } };
    d.addEventListener('keydown',_drawerTrap);
  }
  document.addEventListener('click', function(e){
    const close=e.target.closest('[data-drawer-close]'); if(close){ closeDrawers(); }
    const open=e.target.closest('[data-open-drawer]'); if(open){ const d=document.querySelector(`[data-drawer="${CSS.escape(open.dataset.openDrawer)}"]`); if(d){ _drawerOpener=(document.activeElement&&document.activeElement!==document.body)?document.activeElement:open; d.hidden=false; trapDrawer(d); (focusablesIn(d)[0]||d.querySelector('button,input,select,textarea,a'))?.focus(); }}
  }, true);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') closeDrawers(); }, true);
  const obs=new MutationObserver(()=>{
    document.querySelectorAll('table').forEach(t=>{
      const heads=[...t.querySelectorAll('thead th')].map(th=>th.textContent.trim());
      t.querySelectorAll('tbody tr').forEach(tr=>[...tr.children].forEach((td,i)=>{ if(!td.hasAttribute('data-label') && heads[i]) td.setAttribute('data-label',heads[i]); }));
    });
    document.querySelectorAll('.panel h2 + .meta, .panel .meta + h2').forEach(x=>x.closest('.panel')?.classList.add('dgo-panel-contextual'));
  });
  obs.observe(document.body,{childList:true,subtree:true});
})();
