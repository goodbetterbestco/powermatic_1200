const fs=require('fs'),path=require('path');
const sharp=require(path.join(require('os').homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'));
(async()=>{
const parts=JSON.parse(fs.readFileSync(path.join(__dirname,'config.json'))).parts,dir=path.join(__dirname,'previews');
for(let page=0;page<2;page++){
 const layers=[];
 for(let i=0;i<4;i++){
  const p=parts[page*4+i],left=(i%2)*900,top=Math.floor(i/2)*750;
  layers.push({input:Buffer.from(`<svg width="900" height="60"><rect width="900" height="60" fill="white"/><text x="450" y="30" font-family="Arial" font-size="24" text-anchor="middle">${p.part}: footprint / native 3D</text></svg>`),left,top});
  const svg=fs.readFileSync(path.join(dir,p.name+'.svg'),'utf8').replaceAll('#C2C2C2','#303030');
  const a=await sharp(Buffer.from(svg),{density:160}).resize(450,680,{fit:'contain',background:'white'}).flatten({background:'white'}).png().toBuffer();
  const b=await sharp(path.join(dir,p.name+'-3d.png')).resize(450,680,{fit:'contain',background:'white'}).flatten({background:'white'}).png().toBuffer();
  layers.push({input:a,left,top:top+60},{input:b,left:left+450,top:top+60});
 }
 await sharp({create:{width:1800,height:1500,channels:3,background:'white'}}).composite(layers).png().toFile(path.join(dir,'aligned-'+(page+1)+'.png'));
}
})().catch(e=>{console.error(e);process.exit(1)});
