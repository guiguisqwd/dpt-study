const fs=require('fs'), path=require('path');
const sharp=require('/Users/guigui/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const base=path.resolve(__dirname,'..'),root=path.resolve(base,'../..');
const dir=path.join(base,'2026-10-06-肩袖-阅读优化版-资源');
const out=path.join(root,'tmp/pdfs/shoulder-export');fs.mkdirSync(out,{recursive:true});
(async()=>{for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.svg'))){
 const svg=fs.readFileSync(path.join(dir,f),'utf8').replace(/\sfilter="url\(#[^"]+\)"/g,'');
 await sharp(Buffer.from(svg),{density:220}).flatten({background:'#f8f5ec'}).png().toFile(path.join(out,f.slice(0,2)+'.png'));
}console.log('17 diagrams rendered at 220 DPI; decorative rough filter omitted in export only.');})();
