package com.luisequeira612.jennieruby;

import android.app.*;
import android.appwidget.*;
import android.content.*;
import android.os.Build;
import android.provider.Settings;
import android.widget.RemoteViews;

public class RubyClockWidgetProvider extends AppWidgetProvider {
    static final String ACTION_MINUTE="com.luisequeira612.jennieruby.MINUTE";
    @Override public void onEnabled(Context c){ schedule(c); }
    @Override public void onDisabled(Context c){
        AlarmManager a=(AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if(a!=null)a.cancel(pending(c));
    }
    @Override public void onUpdate(Context c,AppWidgetManager m,int[] ids){
        for(int id:ids) update(c,m,id); schedule(c);
    }
    @Override public void onAppWidgetOptionsChanged(Context c,AppWidgetManager m,int id,android.os.Bundle options){update(c,m,id);}
    @Override public void onReceive(Context c,Intent i){
        super.onReceive(c,i); if(i==null)return; String a=i.getAction();
        if(ACTION_MINUTE.equals(a)||Intent.ACTION_DATE_CHANGED.equals(a)||Intent.ACTION_TIME_CHANGED.equals(a)
            ||Intent.ACTION_TIMEZONE_CHANGED.equals(a)||Intent.ACTION_LOCALE_CHANGED.equals(a)
            ||Intent.ACTION_BOOT_COMPLETED.equals(a)||Intent.ACTION_USER_PRESENT.equals(a)){
            updateAll(c); schedule(c);
        }
    }
    static void schedule(Context c){
        AlarmManager a=(AlarmManager)c.getSystemService(Context.ALARM_SERVICE); if(a==null)return;
        long now=System.currentTimeMillis(), next=((now/60000L)+1L)*60000L;
        PendingIntent pi=pending(c);
        if(Build.VERSION.SDK_INT>=31 && !a.canScheduleExactAlarms()){
            a.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,next,pi);
        } else if(Build.VERSION.SDK_INT>=23) a.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,next,pi);
        else a.setExact(AlarmManager.RTC_WAKEUP,next,pi);
    }
    private static PendingIntent pending(Context c){
        Intent i=new Intent(c,RubyClockWidgetProvider.class).setAction(ACTION_MINUTE);
        return PendingIntent.getBroadcast(c,991,i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
    }
    static void updateAll(Context c){
        AppWidgetManager m=AppWidgetManager.getInstance(c);
        for(int id:m.getAppWidgetIds(new ComponentName(c,RubyClockWidgetProvider.class)))update(c,m,id);
    }
    static void update(Context c,AppWidgetManager m,int id){
        android.os.Bundle o=m.getAppWidgetOptions(id); float d=c.getResources().getDisplayMetrics().density;
        int w=Math.max(1,Math.round(o.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_WIDTH,180)*d));
        int h=Math.max(1,Math.round(o.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_HEIGHT,110)*d));
        RemoteViews v=new RemoteViews(c.getPackageName(),R.layout.widget_ruby_clock);
        v.setImageViewBitmap(R.id.ruby_clock_bitmap,RubyWidgetBitmap.clock(c,w,h));
        Intent launch=new Intent(c,MainActivity.class);
        v.setOnClickPendingIntent(R.id.ruby_clock_root,PendingIntent.getActivity(c,id,launch,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE));
        m.updateAppWidget(id,v);
    }
}
