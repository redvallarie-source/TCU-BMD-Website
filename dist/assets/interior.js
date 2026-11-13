'use strict';
(()=>{
  const reduced=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
  const animate=el=>{if(el&&!reduced())el.animate([{opacity:.45,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],{duration:290,easing:'ease-out'})};
  const year=document.getElementById('history-year');
  if(year){
    const tabs=[...document.querySelectorAll('[data-year]')],previous=document.querySelector('.history-previous'),next=document.querySelector('.history-next');
    function update(){const index=tabs.findIndex(t=>t.getAttribute('aria-selected')==='true');document.getElementById('history-position').textContent=String(index+1).padStart(2,'0')+' / '+String(tabs.length).padStart(2,'0');previous.disabled=index===0;next.disabled=index===tabs.length-1;document.querySelectorAll('[data-history-illustration]').forEach((art,i)=>art.toggleAttribute('hidden',i!==index));animate(document.querySelector('.history-narrative'));animate(document.querySelector('.history-visual svg:not([hidden])'))}
    previous.addEventListener('click',()=>{const i=tabs.findIndex(t=>t.getAttribute('aria-selected')==='true');tabs[Math.max(0,i-1)].click()});next.addEventListener('click',()=>{const i=tabs.findIndex(t=>t.getAttribute('aria-selected')==='true');tabs[Math.min(tabs.length-1,i+1)].click()});new MutationObserver(update).observe(year,{childList:true});update();
  }
  const programTitle=document.getElementById('learning-title');
  if(programTitle&&document.getElementById('program-photo')){
    const images=[["assets/photos/class-learning.webp", "An educator speaking beside a management presentation in class", "Management learning · In class", 1200, 900], ["assets/photos/digital-learning.webp", "Students use digital tools in their learning", "Digital-learning classroom · Department photo archive", 1200, 800], ["assets/photos/design-thinking.webp", "Collaborative creative learning in the department", "Workshop with a visiting educator · Department archive", 960, 719], ["assets/life/baking-practice.webp", "A student preparing chocolate cake in a baking class", "Hands-on baking · Student practice", 960, 1280]];
    function update(){const tabs=[...document.querySelectorAll('[data-learning-tab]')],i=tabs.findIndex(t=>t.getAttribute('aria-selected')==='true'),photo=document.getElementById('program-photo');photo.src=images[i][0];photo.alt=images[i][1];photo.width=images[i][3];photo.height=images[i][4];document.getElementById('program-photo-caption').textContent=images[i][2];document.getElementById('program-number').textContent=String(i+1).padStart(2,'0');animate(photo)}
    new MutationObserver(update).observe(programTitle,{childList:true});update();
  }
  document.querySelectorAll('.cohort-finder [data-filter]').forEach(button=>button.addEventListener('click',()=>{const ticket=document.querySelector('.cohort-ticket');if(button.dataset.filter!=='all'){document.querySelectorAll('.cohort-card').forEach(card=>card.open=card.dataset.category===button.dataset.filter);if(ticket){ticket.querySelector('b').textContent=button.dataset.filter;ticket.querySelector('small').textContent='Selected cohort'}}else if(ticket){ticket.querySelector('b').textContent=Math.max(...[...document.querySelectorAll('.cohort-card')].map(card=>Number(card.dataset.category)));ticket.querySelector('small').textContent='Latest listed cohort'}}));
  const people=document.getElementById('people-visible');
  if(people){const scope=people.closest('[data-filter-scope]');function count(){const number=[...scope.querySelectorAll('.person')].filter(p=>!p.hidden).length;people.textContent=number;people.nextSibling.textContent=window.BMDI18n?.isZh?' 位成員':(number===1?' person':' people')+' listed'}scope.querySelector('[data-filter-input]')?.addEventListener('input',count);scope.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',count));count()}
  document.querySelectorAll('[data-resource-paginate]').forEach(scope=>{
    let limit=12;const items=[...scope.querySelectorAll('.resource-entry[data-filter-item],.resource-link[data-filter-item]')],more=scope.querySelector('.resource-more'),count=scope.querySelector('.resource-count');
    function render(){const matches=items.filter(item=>!item.hidden);items.forEach(item=>item.classList.remove('resource-page-hidden'));matches.forEach((item,i)=>item.classList.toggle('resource-page-hidden',i>=limit));count.textContent=Math.min(limit,matches.length)+' of '+matches.length+(matches.length===1?' document':' documents');more.hidden=matches.length<=limit}
    scope.querySelector('[data-filter-input]')?.addEventListener('input',()=>{limit=12;render()});more.addEventListener('click',()=>{limit+=12;render()});render();
  });
  const photoDialog=document.getElementById('photo-dialog');
  if(photoDialog){
    const photos=[...document.querySelectorAll('[data-gallery-open]')];let current=0,opener;
    function show(i){current=(i+photos.length)%photos.length;const source=photos[current].querySelector('img'),image=document.getElementById('photo-full');image.src=source.src;image.alt=source.alt;document.getElementById('photo-caption').textContent=photos[current].dataset.galleryCaption||photos[current].closest('figure').querySelector('figcaption').textContent;animate(image)}
    photos.forEach((button,i)=>button.addEventListener('click',()=>{opener=button;show(i);photoDialog.showModal()}));photoDialog.querySelector('.photo-close').addEventListener('click',()=>photoDialog.close());photoDialog.addEventListener('close',()=>opener?.focus());photoDialog.addEventListener('click',event=>{if(event.target===photoDialog)photoDialog.close()});photoDialog.querySelector('.photo-previous').addEventListener('click',()=>show(current-1));photoDialog.querySelector('.photo-next').addEventListener('click',()=>show(current+1));photoDialog.addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();show(current+1)}else if(event.key==='ArrowLeft'){event.preventDefault();show(current-1)}});
  }
  const documentDialog=document.getElementById('document-preview');
  if(documentDialog){
    const frame=document.getElementById('document-preview-frame'),title=document.getElementById('document-preview-title'),original=document.getElementById('document-preview-original');let opener;
    document.querySelectorAll('[data-pdf-url]').forEach(button=>button.addEventListener('click',()=>{const url=new URL(button.dataset.pdfUrl,location.href),preview=new URL(button.dataset.previewSrc,location.href);if(!['https:','http:'].includes(url.protocol)||preview.origin!==location.origin)return;opener=button;title.textContent=button.dataset.pdfTitle;frame.title='PDF preview: '+button.dataset.pdfTitle;original.href=url.href;frame.src=preview.href;documentDialog.showModal()}));
    documentDialog.querySelector('.document-preview-close').addEventListener('click',()=>documentDialog.close());documentDialog.addEventListener('click',event=>{if(event.target===documentDialog)documentDialog.close()});documentDialog.addEventListener('close',()=>{frame.src='about:blank';opener?.focus()});
  }
})();
