package com.luisequeira612.jennieruby;

import android.content.Context;
import android.graphics.*;
import android.text.format.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

final class RubyWidgetBitmap {
    private RubyWidgetBitmap() {}

    static Bitmap clock(Context c, int w, int h) {
        Bitmap b=Bitmap.createBitmap(Math.max(1,w),Math.max(1,h),Bitmap.Config.ARGB_8888);
        Canvas cv=new Canvas(b); float s=Math.min(w/300f,h/112f);
        Paint p=paint(); p.setColor(0xFFE8A0A8);
        String pattern=DateFormat.is24HourFormat(c)?"HH:mm":"h:mm";
        String time=new SimpleDateFormat(pattern,Locale.getDefault()).format(new Date());
        p.setTypeface(font(c,R.font.playfair_display,Typeface.SERIF)); p.setTextSize(49*s);
        float x=2*s, baseline=58*s;
        float timeWidth=p.measureText(time);
        float crownCenter=x+timeWidth/2f;
        Path crown=new Path();
        crown.moveTo(crownCenter-13*s,8*s); crown.lineTo(crownCenter-8*s,18*s);
        crown.lineTo(crownCenter-3*s,11*s); crown.lineTo(crownCenter+2*s,18*s);
        crown.lineTo(crownCenter+8*s,8*s); crown.lineTo(crownCenter+6*s,22*s);
        crown.lineTo(crownCenter-11*s,22*s); crown.close();
        Paint crownPaint=new Paint(p); crownPaint.setStyle(Paint.Style.STROKE);
        crownPaint.setStrokeWidth(Math.max(1.1f,1.25f*s)); crownPaint.setStrokeJoin(Paint.Join.ROUND);
        cv.drawPath(crown,crownPaint);
        cv.drawText(time,x,baseline,p);
        p.setTypeface(font(c,R.font.cormorant_garamond,Typeface.SERIF)); p.setTextSize(17*s);
        Locale locale=Locale.getDefault();
        String datePattern="es".equals(locale.getLanguage())?"EEE, d 'de' MMMM":"EEE, d MMMM";
        String date=new SimpleDateFormat(datePattern,locale).format(new Date());
        date=capitalizeInitials(date,locale);
        cv.drawText(date,3*s,77*s,p);
        p.setStrokeWidth(Math.max(1,s)); cv.drawLine(4*s,94*s,58*s,94*s,p);
        cv.drawLine(91*s,94*s,145*s,94*s,p);
        p.setTextSize(12*s); cv.drawText("✦",68*s,98*s,p);
        return b;
    }

    static Bitmap signature(Context c,int w,int h) {
        Bitmap b=Bitmap.createBitmap(Math.max(1,w),Math.max(1,h),Bitmap.Config.ARGB_8888);
        Canvas cv=new Canvas(b); float s=Math.min(w/240f,h/100f);
        Paint p=paint(); p.setColor(0xFFE8A0A8);
        p.setTypeface(font(c,R.font.allura,Typeface.DEFAULT));
        p.setTextSize(68*s);
        String name="Jennie";
        float nameWidth=p.measureText(name);
        float nameX=(w-nameWidth)/2f;
        float nameBaseline=Math.min(h*.69f,66*s);
        cv.drawText(name,nameX,nameBaseline,p);
        // Small outline heart near the upper-right of the final "e".
        float heartX=nameX+nameWidth-1*s, heartY=nameBaseline-39*s;
        Path heart=new Path();
        heart.moveTo(heartX,heartY+5*s);
        heart.cubicTo(heartX-8*s,heartY-2*s,heartX-13*s,heartY+8*s,heartX,heartY+17*s);
        heart.cubicTo(heartX+13*s,heartY+8*s,heartX+8*s,heartY-2*s,heartX,heartY+5*s);
        Paint heartPaint=new Paint(p); heartPaint.setStyle(Paint.Style.STROKE);
        heartPaint.setStrokeWidth(Math.max(1.0f,1.3f*s)); heartPaint.setStrokeJoin(Paint.Join.ROUND);
        cv.save(); cv.rotate(12,heartX,heartY+8*s); cv.drawPath(heart,heartPaint); cv.restore();

        p.setTypeface(font(c,R.font.cormorant_garamond,Typeface.SERIF));
        p.setTextSize(11*s); p.setColor(0xFFF3E6E6);
        String signature="BLACKPINK";
        float sigWidth=p.measureText(signature);
        float sigX=(w-sigWidth)/2f;
        float sigBaseline=Math.min(h-3*s,92*s);
        cv.drawText(signature,sigX,sigBaseline,p);
        Paint rule=new Paint(p); rule.setColor(0xFFE8A0A8);
        rule.setStyle(Paint.Style.STROKE); rule.setStrokeWidth(Math.max(.8f,.85f*s));
        float ruleY=sigBaseline-4*s;
        cv.drawLine(Math.max(4*s,sigX-38*s),ruleY,sigX-9*s,ruleY,rule);
        cv.drawLine(sigX+sigWidth+9*s,ruleY,Math.min(w-4*s,sigX+sigWidth+38*s),ruleY,rule);
        return b;
    }

    static Bitmap jennieRuby(Context c,int w,int h) {
        Bitmap b=Bitmap.createBitmap(Math.max(1,w),Math.max(1,h),Bitmap.Config.ARGB_8888);
        Canvas cv=new Canvas(b); float s=Math.min(w/941f,h/150f);
        Paint p=paint(); p.clearShadowLayer(); p.setColor(0xFFF3E6E6);
        p.setTypeface(font(c,R.font.cormorant_garamond,Typeface.SERIF));
        p.setTextSize(47*s);
        String j="JENNIE"; float tracking=7*s;
        float jw=p.measureText(j)+tracking*(j.length()-1);
        float start=Math.max(0,(w-jw)/2f), baseline=58*s;
        for(int k=0;k<j.length();k++){
            String letter=j.substring(k,k+1); cv.drawText(letter,start,baseline,p);
            start+=p.measureText(letter)+tracking;
        }
        p.setTypeface(font(c,R.font.allura,Typeface.DEFAULT));
        p.setTextSize(75*s); p.setColor(0xFFC41E3A);
        p.setShadowLayer(7*s,0,1*s,0x99C41E3A);
        cv.save(); cv.rotate(-5,w*.52f,h*.57f);
        cv.drawText("Ruby",w*.40f,87*s,p); cv.restore();
        p.clearShadowLayer(); p.setColor(0xFFE8A0A8); p.setStrokeWidth(Math.max(1,s));
        float lineY=59*s; cv.drawLine(8*s,lineY,w*.23f,lineY,p);
        cv.drawLine(w*.77f,lineY,w-8*s,lineY,p);
        return b;
    }

    private static String capitalizeInitials(String value,Locale locale) {
        if(value==null||value.isEmpty()) return value;
        StringBuilder out=new StringBuilder(value);
        out.setCharAt(0,Character.toTitleCase(out.charAt(0)));
        int marker=value.indexOf(" de ");
        if(marker>=0 && marker+4<out.length()) out.setCharAt(marker+4,Character.toTitleCase(out.charAt(marker+4)));
        return out.toString();
    }
    private static Paint paint() {
        Paint p=new Paint(Paint.ANTI_ALIAS_FLAG|Paint.SUBPIXEL_TEXT_FLAG);
        p.setFilterBitmap(true); p.setShadowLayer(3,0,1,0x557A1624); return p;
    }
    private static Typeface font(Context c,int id,Typeface fallback) {
        try { if(android.os.Build.VERSION.SDK_INT>=26) return c.getResources().getFont(id); } catch(Exception ignored) {}
        return fallback;
    }
}
