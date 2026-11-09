'use strict';
(()=>{
 const t=window.BMDI18n?.t||((s)=>s);
 const play=document.querySelector('[data-film-play]');
 play?.addEventListener('click',()=>{
  const container=play.closest('[data-campus-video]'),frame=document.createElement('iframe');
  frame.src='https://www.youtube-nocookie.com/embed/8ODH3C1lykA?autoplay=1&rel=0';
  frame.title=t('Why Should You Study at Tzu Chi University in Taiwan?');
  frame.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
  frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';
  container.classList.add('is-playing');container.replaceChildren(frame);frame.focus();
 });
 const reduce=matchMedia('(prefers-reduced-motion: reduce)'),savingData=Boolean(navigator.connection?.saveData),edges=[...document.querySelectorAll('.campus-edge')];
 const controls=[...document.querySelectorAll('.ambient-control')],surfaces=[...document.querySelectorAll('[data-ambient-surface]')];
 let ambientPaused=document.body.classList.contains('background-motion-paused');
 function syncControls(){
  const off=reduce.matches||savingData||document.body.classList.contains('background-motion-paused');
  controls.forEach(button=>{button.disabled=reduce.matches||savingData;button.setAttribute('aria-pressed',String(off));button.textContent=t(off?'Play background motion':'Pause background motion');button.setAttribute('aria-label',button.textContent)});
 }
 function setMotion(paused){
  ambientPaused=paused;const off=paused||reduce.matches||savingData;
  document.body.classList.toggle('background-motion-paused',off);
  document.dispatchEvent(new CustomEvent('bmd:section-motion',{detail:{paused:off,userPaused:paused,origin:'ambient'}}));
 }
 controls.forEach(button=>button.addEventListener('click',()=>setMotion(!document.body.classList.contains('background-motion-paused'))));
 function pauseEdges(){edges.forEach(e=>e.classList.toggle('motion-off',document.hidden||reduce.matches||savingData||document.body.classList.contains('background-motion-paused')||e.dataset.visible==='false'))}
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>entry.target.dataset.visible=String(entry.isIntersecting));pauseEdges()});edges.forEach(e=>observer.observe(e))}
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>entry.target.classList.toggle('motion-active',entry.isIntersecting)),{rootMargin:'50px'});surfaces.forEach(surface=>observer.observe(surface))}else surfaces.forEach(surface=>surface.classList.add('motion-active'));
 document.addEventListener('visibilitychange',()=>{surfaces.forEach(surface=>surface.classList.toggle('tab-hidden',document.hidden));pauseEdges()});
 document.addEventListener('bmd:section-motion',event=>{if(event.detail?.origin!=='ambient')ambientPaused=Boolean(event.detail?.userPaused??event.detail?.paused);syncControls();pauseEdges()});
 reduce.addEventListener('change',()=>{if(!document.querySelector('.motion-toggle'))setMotion(ambientPaused);else{syncControls();pauseEdges()}});
 if(!document.querySelector('.motion-toggle')||savingData)setMotion(false);else{syncControls();pauseEdges()}
 document.querySelectorAll('.language-switch').forEach(a=>{a.addEventListener('click',()=>{a.hash=location.hash})});
})();
