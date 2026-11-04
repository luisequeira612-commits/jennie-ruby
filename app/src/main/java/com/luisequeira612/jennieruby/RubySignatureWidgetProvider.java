package com.luisequeira612.jennieruby;
import android.appwidget.*; import android.content.*; import android.widget.RemoteViews;
public class RubySignatureWidgetProvider extends AppWidgetProvider {
 @Override public void onUpdate(Context c,AppWidgetManager m,int[] ids){for(int id:ids)update(c,m,id);}
 @Override public void onAppWidgetOptionsChanged(Context c,AppWidgetManager m,int id,android.os.Bundle o){update(c,m,id);}
 private static void update(Context c,AppWidgetManager m,int id){
  android.os.Bundle o=m.getAppWidgetOptions(id); float d=c.getResources().getDisplayMetrics().density;
  int w=Math.max(1,Math.round(o.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_WIDTH,180)*d));
  int h=Math.max(1,Math.round(o.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_HEIGHT,55)*d));
  RemoteViews v=new RemoteViews(c.getPackageName(),R.layout.widget_ruby_signature);
  v.setImageViewBitmap(R.id.ruby_signature_bitmap,RubyWidgetBitmap.signature(c,w,h)); m.updateAppWidget(id,v);
 }
}
