'use strict';
(()=>{
 const root=document.querySelector('.bmd-life'),data=document.getElementById('life-project-data');if(!root||!data)return;
 const projects=JSON.parse(data.textContent),tabs=[...root.querySelectorAll('[data-life-project]')],panel=root.querySelector('#life-project-panel');
 const image=root.querySelector('#life-project-image'),caption=root.querySelector('#life-project-caption'),photo=image.closest('[data-gallery-open]');
 function choose(index,focus=false){
  const current=projects[index];tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(index===i));tab.tabIndex=index===i?0:-1});panel.setAttribute('aria-labelledby',tabs[index].id);
  root.querySelector('#life-project-subject').textContent=current.label;root.querySelector('#life-project-title').textContent=current.title;root.querySelector('#life-project-description').textContent=current.body;
  image.src=current.image;image.alt=current.alt;caption.textContent=current.caption;photo.dataset.galleryCaption=current.caption;
  photo.setAttribute('aria-label',(window.BMDI18n?.isZh?'查看照片：':'View photo: ')+current.caption);
  if(!matchMedia('(prefers-reduced-motion:reduce)').matches)image.animate([{opacity:.4},{opacity:1}],{duration:300,easing:'ease-out'});
  if(focus)tabs[index].focus();
 }
 tabs.forEach((tab,index)=>{tab.addEventListener('click',()=>choose(index));tab.addEventListener('keydown',event=>{let next;if(['ArrowRight','ArrowDown'].includes(event.key))next=(index+1)%tabs.length;else if(['ArrowLeft','ArrowUp'].includes(event.key))next=(index+tabs.length-1)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else return;event.preventDefault();choose(next,true)})});
})();
