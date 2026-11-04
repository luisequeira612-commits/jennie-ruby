import fs from "node:fs";
import path from "node:path";
import * as simpleIcons from "simple-icons";
import svgpath from "svgpath";

const catalogPath=process.argv[2], outDir=process.argv[3];
const catalog=JSON.parse(fs.readFileSync(catalogPath,"utf8"));
fs.mkdirSync(outDir,{recursive:true});
const sources={};
for(const app of catalog.apps){
  const icon=Object.values(simpleIcons).find(x=>x && x.slug===app.glyph);
  let resolved=app.glyph_type, sourcePath=null, source="none", slug=null;
  if(app.glyph_type==="brand"){
    if(icon?.path){ sourcePath=icon.path; source="simple-icons"; slug=icon.slug; }
    else if(app.fallback_path){ sourcePath=app.fallback_path; resolved="generic"; source="generic-fallback"; }
    else if(app.monogram){ resolved="monogram"; source="monogram-fallback"; }
    else throw new Error("Simple Icons slug missing and no safe fallback: "+app.label+" ("+app.glyph+")");
  } else if(app.glyph_type==="generic"){
    if(app.fallback_path){ sourcePath=app.fallback_path; source="generic-fallback"; }
    else if(icon?.path){ sourcePath=icon.path; source="simple-icons"; slug=icon.slug; resolved="brand"; }
    else if(app.monogram){ resolved="monogram"; source="monogram-fallback"; }
    else throw new Error("Generic glyph has no drawable path or monogram: "+app.label);
  } else if(app.glyph_type==="monogram"){
    if(!app.monogram) throw new Error("Monogram text missing: "+app.label);
    resolved="monogram"; source="monogram"; 
  } else throw new Error("Invalid glyph_type for "+app.label+": "+app.glyph_type);
  sources[app.drawable]={resolved_type:resolved,source,slug,glyph:app.glyph};
  if(!sourcePath) continue;
  const scaled=svgpath(sourcePath).scale(0.55).translate(5.4,5.4).round(3).toString();
  const xml='<?xml version="1.0" encoding="utf-8"?>\n'
    +'<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">\n'
    +'<path /><path /><path /><path /><path /><path />\n'
    +'<path android:fillColor="#FFFFFF" android:pathData="'+scaled+'" />\n'
    +'</vector>\n';
  fs.writeFileSync(path.join(outDir,"ruby_"+app.drawable.replace(/^ruby_/,"")+".xml"),xml);
}
fs.writeFileSync(path.join(outDir,"stage5-glyph-sources.json"),JSON.stringify(sources,null,2)+"\n");
console.log("Resolved "+catalog.apps.length+" glyphs; brand labels are assigned only to real Simple Icons slugs.");
