const fs=require('fs');
const path=require('path');
const os=require('os');
let sharp;
try { sharp=require('sharp'); }
catch { sharp=require(path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp')); }
(async()=>{
const root=__dirname;
const a=JSON.parse(fs.readFileSync(path.join(root,'dimension_review.json'))).footprints;
for(const p of a){
 let s=fs.readFileSync(path.join(root,'previews',p.name+'.svg'),'utf8').replaceAll('#C2C2C2','#303030');
 await sharp(Buffer.from(s),{density:180}).resize({width:900,height:1200,fit:'inside'}).flatten({background:'#ffffff'}).png().toFile(path.join(root,'previews',p.name+'.png'));
}
for(let page=0;page<3;page++){
 const entries=a.slice(page*6,page*6+6);const layers=[];
 for(let i=0;i<entries.length;i++){
  let p=entries[i],left=(i%3)*620,top=Math.floor(i/3)*830;
  let img=await sharp(path.join(root,'previews',p.name+'.png')).resize({width:570,height:730,fit:'contain',background:'#ffffff'}).png().toBuffer();
  layers.push({input:img,left:left+25,top:top+85});
  let title=`<svg width="620" height="80"><rect width="620" height="80" fill="white"/><text x="310" y="28" text-anchor="middle" font-family="Arial" font-size="22">${p.name}</text><text x="310" y="57" text-anchor="middle" font-family="Arial" font-size="18">${p.size_mm.map(v=>v.toFixed(3)).join(' × ')} mm</text></svg>`;
  layers.push({input:Buffer.from(title),left,top});
 }
 await sharp({create:{width:1860,height:1660,channels:3,background:'#ffffff'}}).composite(layers).png().toFile(path.join(root,'previews','review-'+(page+1)+'.png'));
}
})().catch(e=>{console.error(e);process.exit(1)});
