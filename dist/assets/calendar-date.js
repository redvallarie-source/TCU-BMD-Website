'use strict';
(function(root){
  const parts=(instant=new Date())=>Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(instant).filter(p=>p.type!=='literal').map(p=>[p.type,Number(p.value)]));
  const months=config=>{const start=config.start.split('-').map(Number),end=config.end.split('-').map(Number),list=[];for(let y=start[0],m=start[1]-1;y<end[0]||(y===end[0]&&m<=end[1]-1);m++){if(m===12){m=0;y++}if(y>end[0]||(y===end[0]&&m>end[1]-1))break;list.push(new Date(y,m,1))}return list};
  const initialIndex=(list,instant=new Date())=>{const current=parts(instant),found=list.findIndex(d=>d.getFullYear()===current.year&&d.getMonth()===current.month-1);return found>=0?found:current.year<list[0].getFullYear()||(current.year===list[0].getFullYear()&&current.month<=list[0].getMonth())?0:list.length-1};
  const eventState=(event,todayKey)=>event.end<todayKey?'completed':event.start>todayKey?'upcoming':'ongoing';
  const api={parts,months,initialIndex,eventState};root.BMDCalendarDate=api;if(typeof module==='object'&&module.exports)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
