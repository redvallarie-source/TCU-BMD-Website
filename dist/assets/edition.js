'use strict';
(()=>{
 const data=document.getElementById('editorial-story-data');
 const dialog=document.getElementById('edition-story-dialog');
 if(!data||!dialog)return;
 const stories=new Map(JSON.parse(data.textContent).map(story=>[story.id,story]));
 const title=document.getElementById('edition-story-title'),label=document.getElementById('edition-story-label');
 const body=document.getElementById('edition-story-body'),images=document.getElementById('edition-story-images'),links=document.getElementById('edition-story-links');
 const close=dialog.querySelector('.edition-story-close');
 let opener;
 function figure(photo){
  const figure=document.createElement('figure'),image=document.createElement('img'),caption=document.createElement('figcaption');
  image.src=photo.src;image.alt=photo.alt;image.width=photo.width;image.height=photo.height;image.decoding='async';
  caption.textContent=photo.caption;
  if(photo.credit&&photo.credit_href){const credit=document.createElement('a');credit.textContent=photo.credit;credit.href=photo.credit_href;credit.target='_blank';credit.rel='noopener';caption.append(document.createTextNode(' · '),credit)}
  figure.append(image,caption);return figure;
 }
 document.querySelectorAll('[data-story-open]').forEach(trigger=>trigger.addEventListener('click',event=>{
  if(event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||event.button!==0)return;
  const story=stories.get(trigger.dataset.storyOpen);if(!story)return;
  event.preventDefault();opener=trigger;
  title.textContent=story.title;label.textContent=story.label;body.textContent=story.body;
  images.replaceChildren();images.classList.toggle('edition-story-single',story.images.length===1);
  images.append(figure(story.images[0]));
  if(story.images.length>1){const stack=document.createElement('div');stack.className='edition-story-stack';story.images.slice(1).forEach(photo=>stack.append(figure(photo)));images.append(stack)}
  links.replaceChildren();story.links.forEach(link=>{const a=document.createElement('a');a.href=link.href;a.textContent=link.label;if(link.href.startsWith('https:')){a.target='_blank';a.rel='noopener'}links.append(a)});
  dialog.showModal();dialog.scrollTop=0;close.focus();
 }));
 close.addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
 dialog.addEventListener('close',()=>opener?.focus({preventScroll:true}));
 links.addEventListener('click',event=>{
  const a=event.target.closest('a');if(!a)return;
  const destination=new URL(a.href,location.href);
  if(destination.origin===location.origin&&destination.pathname===location.pathname&&destination.hash){
   const target=document.getElementById(decodeURIComponent(destination.hash.slice(1)));
   const details=target?.closest('details');if(details)details.open=true;
   dialog.close();
  }
 });
})();
