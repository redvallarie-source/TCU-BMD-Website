'use strict';
(()=>{
 const target=document.querySelector('meta[name="bmd-redirect"]')?.content;
 if(target)location.replace(new URL(target,location.href).href);
})();
