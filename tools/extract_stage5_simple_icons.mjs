import fs from "node:fs";
import path from "node:path";
import * as simpleIcons from "simple-icons";
import svgpath from "svgpath";

const catalogPath=process.argv[2], outDir=process.argv[3];
const catalog=JSON.parse(fs.readFileSync(catalogPath,"utf8"));
fs.mkdirSync(outDir,{recursive:true});
for(const app of catalog.apps){
  const icon=Object.values(simpleIcons).find(x=>x && x.slug===app.glyph);
  if(!icon || !icon.path) throw new Error("Simple Icons slug not found: "+app.glyph);
  const scaled=svgpath(icon.path).scale(0.55).translate(5.4,5.4).round(3).toString();
  const xml='<?xml version="1.0" encoding="utf-8"?>\\n'
    +'<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">\\n'
    +'<path /><path /><path /><path /><path /><path />\\n'
    +'<path android:fillColor="#FFFFFF" android:pathData="'+scaled+'" />\\n'
    +'</vector>\\n';
  fs.writeFileSync(path.join(outDir,"ruby_"+app.drawable.replace(/^ruby_/,"")+".xml"),xml);
}
console.log("Extracted "+catalog.apps.length+" pinned Simple Icons glyph paths.");
