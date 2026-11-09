'use strict';
(()=>{
 const scope=document.querySelector('.bmd-internships');
 if(!scope)return;
 const reduce=matchMedia('(prefers-reduced-motion: reduce)');
 const story=scope.querySelector('#japan-field-journal');
 function storyTarget(hash){
  try{const target=document.getElementById(decodeURIComponent(hash.slice(1)));return target&&(target===story||story.contains(target))?target:null}catch{return null}
 }
 function openStoryTarget(target){for(let el=target;el&&story.contains(el);el=el.parentElement){if(el.tagName==='DETAILS')el.open=true}story.open=true}
 function revealStoryHash(){const target=storyTarget(location.hash);if(target){openStoryTarget(target);requestAnimationFrame(()=>target.scrollIntoView({behavior:'instant',block:'start'}))}}
 scope.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',()=>{const target=storyTarget(link.hash);if(target)openStoryTarget(target)}));
 window.addEventListener('hashchange',revealStoryHash);revealStoryHash();
 const small=matchMedia('(max-width:650px)');
 const tabs=[...scope.querySelectorAll('[data-intern-tab]')];
 const panels=[...scope.querySelectorAll('.intern-work-panel')];
 const list=scope.querySelector('.intern-work-tabs');
 function select(index,focus=false){
  tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;panels[i].hidden=i!==index});
  if(focus)tabs[index].focus();
  if(!reduce.matches)panels[index].animate([{opacity:.35,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:250,easing:'ease-out'});
 }
 tabs.forEach((tab,index)=>{
  tab.addEventListener('click',()=>select(index));
  tab.addEventListener('keydown',event=>{
   let next;
   if(event.key==='Home')next=0;
   if(event.key==='End')next=tabs.length-1;
   if(['ArrowDown','ArrowRight'].includes(event.key))next=(index+1)%tabs.length;
   if(['ArrowUp','ArrowLeft'].includes(event.key))next=(index-1+tabs.length)%tabs.length;
   if(next!==undefined){event.preventDefault();select(next,true)}
  });
 });
 function orientation(){list.setAttribute('aria-orientation',list.closest('.intern-extra-notes')||small.matches?'horizontal':'vertical')}
 small.addEventListener('change',orientation);orientation();select(0);
 const headings=[...scope.querySelectorAll('[data-intern-reveal]')];
 if(!reduce.matches&&'IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-read');observer.unobserve(entry.target)}}),{threshold:.15});
  headings.forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.85)el.classList.add('is-read');else{el.classList.add('intern-reveal-pending');observer.observe(el)}});
  reduce.addEventListener('change',()=>{if(reduce.matches){headings.forEach(el=>el.classList.add('is-read'));observer.disconnect()}});
 }
})();
