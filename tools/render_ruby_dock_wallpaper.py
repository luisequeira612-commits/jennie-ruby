#!/usr/bin/env python3
"""Render real Jennie source photo into calibrated 720x1640 wallpapers.

No rotation, blur extension, image duplication or non-uniform scaling.
Uniform edge trimming is detected and removed before composition.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "app/src/main/res/drawable-nodpi/jennie_ruby_wallpaper.jpg"
CONFIG = ROOT / "tools/dock_bar.json"
OUT = ROOT / "app/build/reports"
DARK = np.array([8, 3, 4], dtype=np.float32)

def edge_report(a):
    h,w,_=a.shape
    report={}
    # Uniform near-black/near-white strips on each margin; tolerance is deliberately strict.
    for side, lines in (("top",a),("bottom",a[::-1]),("left",np.transpose(a,(1,0,2))),("right",np.transpose(a[:,::-1,:],(1,0,2)))):
        count=0
        for line in lines:
            p=line.astype(np.int16)
            if (p.max()-p.min() <= 9 and (p.mean() < 24 or p.mean() > 232)):
                count+=1
            else: break
        report[side]={"uniform_light_or_dark_px":count}
    # Locate strong vertical edge transitions row-by-row; report slope of the leftmost
    # content boundary to flag a diagonal edge rather than rotate/correct it blindly.
    gray=a.mean(axis=2)
    candidates=[]
    for y in np.linspace(0,h-1,min(h,80),dtype=int):
        row=gray[y]
        dif=np.abs(np.diff(row))
        candidates.append(int(np.argmax(dif[:max(1,w//3)])))
    report["left_edge_transition_px"]={"min":int(min(candidates)),"max":int(max(candidates)),"range":int(max(candidates)-min(candidates))}
    # Row variance and average luminance expose flat fills / blurred lower extensions.
    bands=[]
    for y in range(0,h,32):
        b=a[y:min(h,y+32)].astype(np.float32)
        bands.append({"y_start":y,"variance":round(float(b.var()),2),"mean_rgb":[round(float(v),1) for v in b.mean(axis=(0,1))]})
    report["bottom_bands"]=bands[-8:]
    return report

def trim_uniform(a):
    h,w,_=a.shape
    top,bottom,left,right=0,h,0,w
    def uniform(line):
        p=line.astype(np.int16)
        return p.max()-p.min()<=9 and (p.mean()<24 or p.mean()>232)
    while top<bottom-20 and uniform(a[top]): top+=1
    while bottom>top+20 and uniform(a[bottom-1]): bottom-=1
    while left<right-20 and uniform(a[top:bottom,left]): left+=1
    while right>left+20 and uniform(a[top:bottom,right-1]): right-=1
    return a[top:bottom,left:right],(left,top,w-right,h-bottom)

def gradient(color0,color1,n):
    t=np.linspace(0,1,max(1,n),dtype=np.float32)[:,None,None]
    return np.clip(color0[None,None,:]*(1-t)+color1[None,None,:]*t,0,255)

def fit_width(photo,W):
    h,w,_=photo.shape
    nh=round(h*W/w)
    return np.asarray(Image.fromarray(photo).resize((W,nh),Image.Resampling.LANCZOS)),nh

def make_ab(photo,cfg,offset):
    W,H=cfg["canvas_width"],cfg["canvas_height"]
    scaled,ph=fit_width(photo,W)
    y=offset
    if y<0 or y+ph>H: raise ValueError("A/B photo does not fit without crop; refusing distortion.")
    out=np.empty((H,W,3),dtype=np.uint8); out[:]=DARK.astype(np.uint8)
    # Fill the upper gap using a clean darkening gradient sampled from the top edge colour.
    if y:
        top=scaled[0].mean(axis=0).astype(np.float32)
        out[:y]=np.clip(gradient(top,DARK,y),0,255).astype(np.uint8)
    out[y:y+ph]=scaled
    # Remaining area is a clean monotonic gradient, not blur or duplicated pixels.
    if y+ph<H:
        start=scaled[-1].mean(axis=0).astype(np.float32)
        out[y+ph:]=np.clip(gradient(start,DARK,H-y-ph),0,255).astype(np.uint8)
    # A gentle dark overlay across the lower third for widget/dock contrast.
    start=max(0,int(H*0.64))
    overlay=np.linspace(0,0.58,H-start,dtype=np.float32)[:,None,None]
    region=out[start:].astype(np.float32)
    out[start:]=np.clip(region*(1-overlay)+DARK[None,None,:]*overlay,0,255).astype(np.uint8)
    return Image.fromarray(out)

def make_cover(photo,cfg,offset):
    W,H=cfg["canvas_width"],cfg["canvas_height"]
    h,w,_=photo.shape
    scale=max(W/w,H/h); nw,nh=round(w*scale),round(h*scale)
    scaled=np.asarray(Image.fromarray(photo).resize((nw,nh),Image.Resampling.LANCZOS))
    excess=nw-W
    # offset is normalized [-1,1]: -1 keeps left, +1 keeps right.
    x=round((excess/2)*(1+max(-1,min(1,offset))))
    crop=scaled[:,x:x+W]
    if nh>H:
        y=(nh-H)//2; crop=crop[y:y+H]
    elif nh<H:
        pad=np.empty((H,W,3),dtype=np.uint8); pad[:]=DARK.astype(np.uint8); pad[:nh]=crop; crop=pad
    # darken lower third without blur.
    start=int(H*.64); alpha=np.linspace(0,.58,H-start,dtype=np.float32)[:,None,None]
    crop=crop.copy(); crop[start:]=np.clip(crop[start:].astype(np.float32)*(1-alpha)+DARK[None,None,:]*alpha,0,255)
    return Image.fromarray(crop),{"scaled_width":nw,"scaled_height":nh,"crop_left_px":x,"crop_right_px":nw-x-W,"source_width_loss_px":round((x+(nw-x-W))/scale)}

def glass(img,bar):
    x,y,w,h,r,b=(int(bar[k]) for k in ("x","y","width","height","radius","border_px"))
    layer=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=(14,4,8,166),outline=(122,22,36,210),width=b)
    d.line((x+r,y+2,x+w-r,y+2),fill=(194,58,75,100),width=1)
    return Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB")

def save_pair(img,name,bar):
    img.save(OUT/f"fondo_{name}_sin_barra.png",optimize=True)
    glass(img,bar).save(OUT/f"fondo_{name}_con_barra.png",optimize=True)

def main():
    cfg=json.loads(CONFIG.read_text())
    with Image.open(SOURCE) as im: raw=np.asarray(im.convert("RGB"))
    report={"source":str(SOURCE.relative_to(ROOT)),"original_dimensions":[int(raw.shape[1]),int(raw.shape[0])],"original_aspect_ratio":round(raw.shape[1]/raw.shape[0],6),"edges_before_trim":edge_report(raw)}
    photo,trim=trim_uniform(raw)
    photo=photo.copy()  # trim view is read-only; cleanup edits a private buffer.
    # The source JPEG contains a narrow near-white edge artifact on the upper-right
    # border (about the first 260 source rows). Extend the adjacent dark pixels
    # across only that artifact; do not rotate, scale non-uniformly, or crop Jennie.
    edge_rows=min(260,photo.shape[0]); edge_cols=min(12,photo.shape[1]//20)
    if edge_rows and edge_cols:
        photo[:edge_rows,-edge_cols:]=photo[:edge_rows,-edge_cols-1:-edge_cols]
    report["upper_right_edge_cleanup"]={"rows":edge_rows,"columns":edge_cols,"method":"extend adjacent edge pixels"}
    report["trimmed_uniform_border_ltrb_px"]=list(trim)
    report["trimmed_dimensions"]=[int(photo.shape[1]),int(photo.shape[0])]
    report["edges_after_trim"]=edge_report(photo)
    OUT.mkdir(parents=True,exist_ok=True)
    bar=cfg["bar"]; tall=cfg["bar_tall"]
    a=make_ab(photo,cfg,0); b=make_ab(photo,cfg,int(cfg["photo_offset_y"]))
    save_pair(a,"A",bar); save_pair(b,"B",bar)
    c,cover=make_cover(photo,cfg,float(cfg["cover_crop_offset_x"]))
    save_pair(c,"C",bar)
    glass(a,tall).save(OUT/"fondo_A_con_barra_alta.png",optimize=True)
    report["cover_crop"]=cover
    report["photo_offset_y_px"]=cfg["photo_offset_y"]
    report["outputs"]=["fondo_A_con_barra.png","fondo_A_sin_barra.png","fondo_B_con_barra.png","fondo_B_sin_barra.png","fondo_C_con_barra.png","fondo_C_sin_barra.png","fondo_A_con_barra_alta.png"]
    (OUT/"diagnostico_wallpaper.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    for name in report["outputs"]:
        with Image.open(OUT/name) as check:
            if check.size!=(720,1640): raise RuntimeError(f"Invalid output {name}: {check.size}")
    print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__": main()
