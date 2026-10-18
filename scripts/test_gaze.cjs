const assert = require('node:assert/strict');
const {frameForPointer} = require('../viewer/gaze.js');
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
