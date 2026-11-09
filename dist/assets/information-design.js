'use strict';
(()=>{
  const guide=document.querySelector('.certificate-guide');
  if(!guide)return;
  const count=guide.querySelector('.certificate-result-count');
  const update=()=>{count.hidden=false;count.textContent=String(guide.querySelectorAll('tr[data-filter-item]:not([hidden])').length)+' '+BMDI18n.t('certificates shown')};
  guide.querySelector('input').addEventListener('input',update);
  guide.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',update));
  update();
  const original=document.getElementById('original-certificate-tables');
  const openFromHash=()=>{if(location.hash==='#original-certificate-tables')original.open=true};
  document.querySelectorAll('a[href="#original-certificate-tables"]').forEach(link=>link.addEventListener('click',()=>{original.open=true}));
  window.addEventListener('hashchange',openFromHash);openFromHash();
})();
