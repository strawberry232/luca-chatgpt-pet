const assert = require('node:assert/strict');
const {frameForPointer,frameForIndex,shortestDelta,createGazeController} = require('../viewer/gaze.js');
const rect={left:10,top:20,width:192,height:208};
const center={x:106,y:124};
assert.equal(frameForPointer(rect,center),null);
assert.equal(frameForPointer(rect,{x:400,y:300},1),null);
for(let index=0;index<16;index++){
 const radians=index*Math.PI/8;
 const frame=frameForPointer(rect,{x:center.x+Math.sin(radians)*200,y:center.y-Math.cos(radians)*200});
 assert.equal(frame.index,index);
 assert.equal(frame.row,9+Math.floor(index/8));
 assert.equal(frame.column,index%8);
}
console.log('PASS: sixteen clockwise directions, center deadzone and v1 exclusion');
function target(degrees) {return {...frameForIndex(Math.round(degrees/22.5)),targetDegrees:degrees};}
function trajectory(from,to) {
 const controller=createGazeController();const frames=[controller.update(target(from),0).index];
 for(let time=16;time<=1200;time+=16){const frame=controller.update(target(to),time);if(frame.index!==frames.at(-1))frames.push(frame.index);}
 return {frames,controller};
}
const quarter=trajectory(0,90);
assert.deepEqual(quarter.frames,[0,1,2,3,4]);
assert.ok(Math.abs(shortestDelta(quarter.controller.getState().angle,90))<.1);
assert.deepEqual(trajectory(337.5,22.5).frames,[15,0,1]);
assert.deepEqual(trajectory(22.5,337.5).frames,[1,0,15]);
const half=trajectory(270,90).frames;assert.equal(half.length,9);
for(let i=1;i<half.length;i++)assert.equal(Math.abs(shortestDelta(half[i-1]*22.5,half[i]*22.5)),22.5);
const jitter=createGazeController();jitter.update(target(10),0);const changes=[];
for(let time=16;time<2000;time+=16)changes.push(jitter.update(target(time%32===0?10.8:11.8),time).index);
assert.ok(changes.every(index=>index===0),'Boundary jitter must not alternate poses');
const paused=createGazeController();paused.update(target(0),0);const afterPause=paused.update(target(180),10000);
assert.ok([0,1,15].includes(afterPause.index),'A tab pause must not jump to a distant pose');
paused.update(null,10016);assert.equal(paused.getState().angle,null);
assert.equal(paused.update(target(90),10032).index,4);
console.log('PASS: eased neighboring turns, both wrap directions, shortest half-turn, boundary stability and pause/reset behavior');
