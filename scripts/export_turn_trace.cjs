// Export the same controller used by the viewer for a reproducible comparison.
const {createGazeController,frameForIndex}=require('../viewer/gaze.js');
const controller=createGazeController();
const segments=[{duration:900,degrees:270},{duration:1100,degrees:90},{duration:900,degrees:337.5},{duration:1100,degrees:22.5},{duration:1000,degrees:180},{duration:1100,degrees:0}];
const frames=[];let time=0;
for(const segment of segments){
 const target={...frameForIndex(Math.round(segment.degrees/22.5)),targetDegrees:segment.degrees};
 for(let offset=0;offset<segment.duration;offset+=20){
  const frame=controller.update(target,time);
  frames.push({time_ms:time,duration_ms:20,target_index:target.index,displayed_index:frame.index});time+=20;
 }
}
const output=JSON.stringify({duration_ms:time,frames},null,2)+'\n';
if(process.argv[2]){
 const fs=require('node:fs'),path=require('node:path');
 fs.mkdirSync(path.dirname(process.argv[2]),{recursive:true});
 fs.writeFileSync(process.argv[2],output,'utf8');
}else process.stdout.write(output);
