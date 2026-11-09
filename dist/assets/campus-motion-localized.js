'use strict';
(()=>{
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const savingData=Boolean(navigator.connection?.saveData);
  const hero=document.querySelector('.cinema-hero');
  if(hero){
    const video=hero.querySelector('video'),photos=[...hero.querySelectorAll('.campus-slide')];
    const choices=[...hero.querySelectorAll('[data-hero-mode]')],pause=hero.querySelector('.campus-pause');
    const scene=hero.querySelector('#campus-scene'),credit=hero.querySelector('#campus-credit'),announcement=hero.querySelector('#campus-announcement');
    const labels=[BMDI18n.t('Campus architecture'),BMDI18n.t('Hualien, Taiwan'),BMDI18n.t('The BMD community')];
    let mode=(reduced.matches||savingData)?choices.findIndex(b=>b.dataset.heroMode==='0'):0;
    let paused=reduced.matches||savingData,visible=true,timer,failed=false;
    function moving(){return !paused&&!reduced.matches&&!document.hidden&&visible}
    function schedule(){
      clearTimeout(timer);
      if(moving()&&choices[mode].dataset.heroMode!=='film'&&(!hero.contains(document.activeElement)||document.activeElement===pause)){
        timer=setTimeout(()=>{
          const options=choices.map((b,i)=>({b,i})).filter(x=>x.b.dataset.heroMode!=='film');
          const current=options.findIndex(x=>x.i===mode);select(options[(current+1)%options.length].i,false);
        },9000);
      }
    }
    function update(){
      const allowed=moving(),film=choices[mode].dataset.heroMode==='film';
      hero.classList.toggle('hero-paused',!allowed);
      pause.disabled=reduced.matches;
      pause.setAttribute('aria-pressed',String(paused||reduced.matches));
      pause.setAttribute('aria-label',reduced.matches?BMDI18n.t('Hero motion disabled by device preference'):paused?BMDI18n.t('Play hero motion'):BMDI18n.t('Pause hero motion'));
      pause.innerHTML='<span aria-hidden="true">'+(paused||reduced.matches?'▶':'Ⅱ')+'</span>';
      if(video){
        if(allowed&&film&&!failed){
          if(!video.getAttribute('src')){
            video.muted=true;
            video.src=innerWidth<700?video.dataset.filmSmall:video.dataset.filmSrc;
          }
          const promise=video.play();
          promise?.catch(()=>{if(choices[mode].dataset.heroMode==='film'){paused=true;hero.classList.add('hero-paused');pause.setAttribute('aria-pressed','true');pause.setAttribute('aria-label',BMDI18n.t('Play hero motion'));pause.innerHTML='<span aria-hidden="true">▶</span>'}});
        }else video.pause();
      }
      schedule();
    }
    function select(index,manual=true){
      mode=(index+choices.length)%choices.length;
      if(failed&&choices[mode].dataset.heroMode==='film')mode=choices.findIndex(b=>b.dataset.heroMode==='0');
      const value=choices[mode].dataset.heroMode,film=value==='film';
      hero.classList.toggle('film-selected',film);
      photos.forEach((photo,i)=>photo.classList.toggle('active',i===(film?0:Number(value))));
      choices.forEach((button,i)=>{button.classList.toggle('selected',i===mode);button.setAttribute('aria-pressed',String(i===mode))});
      scene.textContent=film?BMDI18n.t('Campus film'):labels[Number(value)];
      if(credit){
      if(film){credit.href=credit.dataset.initialHref;credit.textContent=credit.dataset.initialLabel+''}
      else if(value==='2'){credit.href='https://mdm.tcu.edu.tw/p/412-1021-3692.php?Lang=zh-tw';credit.textContent=BMDI18n.t('Department photo archive')}
      else{credit.href='https://www.tcu.edu.tw/';credit.textContent=BMDI18n.t('Tzu Chi University')}
      }
      if(manual)announcement.textContent=film?BMDI18n.t('Campus film selected.'):labels[Number(value)]+BMDI18n.t(' selected.');
      update();
    }
    choices.forEach((button,i)=>button.addEventListener('click',()=>select(i)));
    pause.addEventListener('click',()=>{paused=!paused;update()});
    hero.querySelector('.campus-prev').addEventListener('click',()=>select(mode-1));
    hero.querySelector('.campus-next').addEventListener('click',()=>select(mode+1));
    hero.addEventListener('focusin',schedule);hero.addEventListener('focusout',()=>setTimeout(schedule,0));
    video?.addEventListener('playing',()=>hero.classList.add('film-ready'));
    video?.addEventListener('error',()=>{failed=true;hero.classList.remove('film-ready');const filmChoice=choices.find(b=>b.dataset.heroMode==='film');if(filmChoice)filmChoice.disabled=true;select(choices.findIndex(b=>b.dataset.heroMode==='0'),false);announcement.textContent=BMDI18n.t('Showing campus photographs.')});
    if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;update()},{threshold:.08}).observe(hero);
    document.addEventListener('visibilitychange',update);
    reduced.addEventListener('change',()=>{paused=reduced.matches;if(reduced.matches&&choices[mode].dataset.heroMode==='film')select(choices.findIndex(b=>b.dataset.heroMode==='0'),false);else update()});
    select(Math.max(mode,0),false);
  }

  const section=document.querySelector('.editorial-motion');
  if(section){
    const track=section.querySelector('.word-track'),scenes=[...section.querySelectorAll('[data-life-scene]')];
    const buttons=[...section.querySelectorAll('[data-life-step]')],caption=section.querySelector('#life-scene-caption');
    const captions=JSON.parse(section.querySelector('#life-scene-data').textContent);
    let index=0,visible=false,timer;
    function isOff(){return reduced.matches||document.hidden||document.body.classList.contains('background-motion-paused')}
    function schedule(){clearTimeout(timer);if(visible&&!isOff()&&(!section.contains(document.activeElement)||document.activeElement===section.querySelector('.motion-toggle')))timer=setTimeout(()=>{choose((index+1)%scenes.length);},4600)}
    function choose(next){
      index=next;track.style.setProperty('--word-y',`${-index*1.2}em`);
      scenes.forEach((photo,i)=>{photo.classList.toggle('active',i===index);if(i===index)photo.removeAttribute('aria-hidden');else photo.setAttribute('aria-hidden','true')});
      buttons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
      caption.textContent=captions[index];schedule();
    }
    buttons.forEach((button,i)=>button.addEventListener('click',()=>choose(i)));
    section.addEventListener('focusin',schedule);section.addEventListener('focusout',()=>setTimeout(schedule,0));
    document.addEventListener('bmd:section-motion',schedule);document.addEventListener('visibilitychange',schedule);reduced.addEventListener('change',schedule);
    if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;schedule()},{threshold:.2}).observe(section);
    else{visible=true;schedule()}
  }

  // Reveal only selected headings. Their default HTML stays fully visible.
  const revealTargets=[...document.querySelectorAll('[data-editorial-reveal],[data-reveal-line]')];
  if(!reduced.matches&&'IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('is-read');observer.unobserve(entry.target)}
    }),{threshold:.12,rootMargin:'0px 0px -25px 0px'});
    revealTargets.forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.82){el.classList.add('is-read');return}el.classList.add('editorial-reveal-pending');observer.observe(el)});
    reduced.addEventListener('change',()=>{if(reduced.matches){revealTargets.forEach(el=>el.classList.add('is-read'));observer.disconnect()}});
  }

  // A few pixels of image travel, with no pinned sections or scroll interception.
  const drifts=[...document.querySelectorAll('[data-photo-drift]')];
  const desktop=matchMedia('(min-width: 901px)');let frame=0;
  function drift(){
    frame=0;
    const off=reduced.matches||savingData||!desktop.matches||document.body.classList.contains('background-motion-paused');
    drifts.forEach(el=>{
      const rect=el.getBoundingClientRect();
      if(off){el.style.setProperty('--photo-y','0px');return}
      if(rect.bottom<0||rect.top>innerHeight)return;
      const distance=Math.max(-12,Math.min(12,(innerHeight/2-rect.top-rect.height/2)*.025));
      el.style.setProperty('--photo-y',distance.toFixed(2)+'px');
    });
  }
  function requestDrift(){if(!frame&&!document.hidden)frame=requestAnimationFrame(drift)}
  if(drifts.length){addEventListener('scroll',requestDrift,{passive:true});addEventListener('resize',requestDrift,{passive:true});reduced.addEventListener('change',requestDrift);document.addEventListener('bmd:section-motion',requestDrift);requestDrift()}
})();
