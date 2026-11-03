package com.luisequeira612.jennieruby;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.text.format.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

final class RubyWidgetBitmap {
    private RubyWidgetBitmap() {}

    static Bitmap clock(Context context) {
        float density=context.getResources().getDisplayMetrics().density;
        int width=Math.round(300*density), height=Math.round(112*density);
        Bitmap bitmap=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);
        Canvas canvas=new Canvas(bitmap);
        Paint p=paint();
        p.setColor(0xFFE8A0A8);
        Typeface playfair=font(context,R.font.playfair_display,Typeface.SERIF);
        Typeface cormorant=font(context,R.font.cormorant_garamond,Typeface.SERIF);
        String pattern=DateFormat.is24HourFormat(context)?"HH:mm":"h:mm";
        String time=new SimpleDateFormat(pattern,Locale.getDefault()).format(new Date());
        p.setTypeface(playfair); p.setTextSize(49*density);
        canvas.drawText(time,2*density,52*density,p);
        p.setTypeface(cormorant); p.setTextSize(17*density);
        String date=new SimpleDateFormat("EEE, d 'de' MMMM",new Locale("es","NI")).format(new Date());
        date=date.substring(0,1).toUpperCase(new Locale("es","NI"))+date.substring(1);
        canvas.drawText(date,3*density,77*density,p);
        p.setStrokeWidth(1*density);
        canvas.drawLine(4*density,94*density,58*density,94*density,p);
        canvas.drawLine(91*density,94*density,145*density,94*density,p);
        p.setTextSize(12*density); canvas.drawText("✦",68*density,98*density,p);
        return bitmap;
    }

    static Bitmap signature(Context context) {
        float density=context.getResources().getDisplayMetrics().density;
        int width=Math.round(240*density), height=Math.round(100*density);
        Bitmap bitmap=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);
        Canvas canvas=new Canvas(bitmap); Paint p=paint();
        p.setColor(0xFFE8A0A8);
        p.setTypeface(font(context,R.font.allura,Typeface.CURSIVE));
        p.setTextSize(68*density); canvas.drawText("Jennie",2*density,62*density,p);
        p.setTypeface(font(context,R.font.cormorant_garamond,Typeface.SERIF));
        p.setTextSize(11*density);
        p.setColor(0xFFF3E6E6);
        canvas.drawText("BLACKPINK",65*density,88*density,p);
        return bitmap;
    }

    private static Paint paint() {
        Paint p=new Paint(Paint.ANTI_ALIAS_FLAG|Paint.SUBPIXEL_TEXT_FLAG);
        p.setFilterBitmap(true); p.setShadowLayer(3,0,1,0x557A1624);
        return p;
    }
    private static Typeface font(Context c,int id,Typeface fallback) {
        try { if (android.os.Build.VERSION.SDK_INT >= 26) return c.getResources().getFont(id); } catch(Exception ignored) {} return fallback;
    }
}
