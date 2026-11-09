'use strict';
(()=>{
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const savingData=Boolean(navigator.connection?.saveData);
  const regions=[...document.querySelectorAll('.motion-region')];
  const toggle=document.querySelector('.motion-toggle');
  let paused=false;
  function renderToggle(off){
    if(toggle){toggle.disabled=reduced.matches||savingData;toggle.setAttribute('aria-pressed',String(off));toggle.setAttribute('aria-label',off?'Play section animation':'Pause section animation');toggle.querySelector('.motion-state').textContent=off?'▶':'Ⅱ';toggle.querySelector('.motion-label').textContent=off?'Motion off':'Motion on';}
  }
  function update(){
    const off=paused||reduced.matches||savingData;
    document.body.classList.toggle('background-motion-paused',off);
    renderToggle(off);
    document.dispatchEvent(new CustomEvent('bmd:section-motion',{detail:{paused:off,userPaused:paused,origin:'home'}}));
  }
  document.addEventListener('bmd:section-motion',event=>{if(event.detail?.origin==='ambient'){paused=Boolean(event.detail.userPaused);renderToggle(Boolean(event.detail.paused))}});
  toggle?.addEventListener('click',()=>{paused=!paused;update()});
  reduced.addEventListener('change',update);update();
  if('IntersectionObserver' in window){
    const atmosphere=new IntersectionObserver(entries=>entries.forEach(entry=>entry.target.classList.toggle('motion-active',entry.isIntersecting)),{rootMargin:'60px'});
    regions.forEach(region=>atmosphere.observe(region));

  }else regions.forEach(region=>region.classList.add('motion-active'));
  document.addEventListener('visibilitychange',()=>regions.forEach(region=>region.classList.toggle('tab-hidden',document.hidden)));
})();
