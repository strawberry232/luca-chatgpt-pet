(function () {
  'use strict';
  const text = {
    zh: {title:'卢卡的陪伴时刻',intro:'移动鼠标，卢卡会顺着方向慢慢转过去。',directions:'十六方向过渡 · 缓起缓停',action:'选择动作',follow:'跟随鼠标',demo:'演示转向',idle:'待机 · 眨眼',failed:'失落 · 轻轻垂头',leave:'转向会经过相邻姿态；轻微抖动时保持视线稳定。',timing:'待机播放节奏',natural:'自然眨眼预览',client:'当前客户端固定节奏',sameHead:'待机与失落复用同一头部原图',scope:'此页面已实现窗口内鼠标跟随和平缓转向。ChatGPT 浮窗的全局跟随、过渡和眨眼帧率由客户端控制，上传图集不会改写客户端行为。',naturalNote:'此预览的闭眼帧停留约 75 毫秒。',clientNote:'此客户端的最短待机帧约 660 毫秒；图集只能减少闭眼帧数。',resting:'待机',sad:'失落',watching:'望向：',turning:'正在转向：',compass:['上方','右上方','右上方','右上方','右方','右下方','右下方','右下方','下方','左下方','左下方','左下方','左方','左上方','左上方','左上方']},
    en: {title:'A moment with Luca',intro:'Move your pointer and Luca will gently turn toward it.',directions:'Sixteen look poses · gentle starts and stops',action:'Choose an action',follow:'Follow pointer',demo:'Show turning demo',idle:'Idle · blink',failed:'Disappointed · gentle nod',leave:'Turns pass through neighboring poses; small pointer movements stay steady.',timing:'Idle playback timing',natural:'Natural blink preview',client:'Current client timing',sameHead:'Idle and disappointment use the same head artwork',scope:'This page implements pointer tracking and gradual turns inside the window. Global tracking, transitions and blink timing in ChatGPT are controlled by its client; uploading an atlas does not change the client.',naturalNote:'The closed-eye frame lasts about 75 ms in this preview.',clientNote:'The shortest idle frame in this client is about 660 ms. The atlas can only reduce closed frames.',resting:'Idle',sad:'Disappointed',watching:'Looking: ',turning:'Turning: ',compass:['up','up-right','up-right','up-right','right','down-right','down-right','down-right','down','down-left','down-left','down-left','left','up-left','up-left','up-left']}
  };
  const canvas = document.getElementById('pet');
  const ctx = canvas.getContext('2d');
  const timing = document.getElementById('timing');
  const status = document.getElementById('status');
  const image = new Image();
  image.src = window.LUCA_ATLAS_URL || '../assets/luca-v2.png';
  let lang = 'zh', mode = 'follow', pointer = null, started = performance.now(), lastStatus = '';
  let drawFrame = {row:0,column:0};
  const natural = [3200,75,85,900,900,1000];
  const nativeIdle = [1680,660,660,840,840,1920];
  const failed = [140,140,140,140,140,140,140,240];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const gaze = PetGaze.createGazeController();
  const demoTargets = [270,90,0,180,337.5,22.5];
  function frameAt(elapsed, durations) {
    const total = durations.reduce((a,b)=>a+b,0);let t = elapsed % total;
    for (let i=0;i<durations.length;i++) {if(t<durations[i])return i;t-=durations[i];}
    return 0;
  }
  function updateLanguage() {
    const strings = text[lang];document.documentElement.lang = lang==='zh'?'zh-CN':'en';
    document.querySelectorAll('[data-i18n]').forEach(node=>{node.textContent=strings[node.dataset.i18n];});
    document.getElementById('language').textContent = lang==='zh'?'English':'中文';
    document.getElementById('timing-note').textContent = timing.value==='natural'?strings.naturalNote:strings.clientNote;
    lastStatus='';
  }
  function selectMode(next) {
    mode=next;started=performance.now();gaze.reset();
    document.querySelectorAll('[data-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.mode===mode)));
  }
  document.querySelectorAll('[data-mode]').forEach(button=>button.addEventListener('click',()=>selectMode(button.dataset.mode)));
  document.getElementById('language').addEventListener('click',()=>{lang=lang==='zh'?'en':'zh';updateLanguage();});
  timing.addEventListener('change',()=>{started=performance.now();updateLanguage();});
  window.addEventListener('pointermove',event=>{pointer={x:event.clientX,y:event.clientY};},{passive:true});
  document.documentElement.addEventListener('pointerleave',()=>{pointer=null;});
  window.addEventListener('blur',()=>{pointer=null;});
  image.addEventListener('error',()=>{document.getElementById('load-error').style.display='block';});
  function render(now) {
    const strings=text[lang];let frame, label, target=null;
    if (mode==='follow' && pointer && !reduced.matches) {
      target=PetGaze.frameForPointer(canvas.getBoundingClientRect(),pointer,2,20);
    } else if (mode==='demo' && !reduced.matches) {
      const degrees=demoTargets[Math.floor((now-started)/1100)%demoTargets.length];
      target={...PetGaze.frameForIndex(Math.round(degrees/22.5)),targetDegrees:degrees};
    }
    frame=gaze.update(target,now);
    if(frame) label=(frame.turning?strings.turning:strings.watching)+strings.compass[frame.index];
    if (!frame) {
      const isSad=mode==='failed';
      frame={row:isSad?5:0,column:reduced.matches?0:frameAt(now-started,isSad?failed:(timing.value==='client'?nativeIdle:natural))};
      label=isSad?strings.sad:strings.resting;
    }
    drawFrame=frame;
    if(image.complete && image.naturalWidth===1536){
      ctx.clearRect(0,0,canvas.width,canvas.height);ctx.imageSmoothingEnabled=false;
      ctx.drawImage(image,frame.column*192,frame.row*208,192,208,0,0,canvas.width,canvas.height);
    }
    if(label!==lastStatus){status.textContent=label;lastStatus=label;}
    requestAnimationFrame(render);
  }
  // Read-only state used by the local browser checks; no pet account integration.
  window.LucaPreview={getState:()=>({mode,lang,timing:timing.value,frame:{...drawFrame},gaze:gaze.getState(),loaded:image.naturalWidth===1536}),frameAt};
  updateLanguage();requestAnimationFrame(render);
})();
