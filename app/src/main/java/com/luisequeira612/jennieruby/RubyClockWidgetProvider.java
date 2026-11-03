package com.luisequeira612.jennieruby;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.os.SystemClock;
import android.widget.RemoteViews;

public class RubyClockWidgetProvider extends AppWidgetProvider {
    @Override public void onEnabled(Context context) {
        scheduleMinuteRefresh(context);
    }

    @Override public void onDisabled(Context context) {
        PendingIntent pi=PendingIntent.getBroadcast(context,991,
            new Intent(context,RubyClockWidgetProvider.class).setAction("com.luisequeira612.jennieruby.MINUTE"),
            PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
        AlarmManager alarms=(AlarmManager)context.getSystemService(Context.ALARM_SERVICE);
        if(alarms!=null) alarms.cancel(pi);
    }

    @Override public void onUpdate(Context context, AppWidgetManager manager, int[] ids) {
        for(int id:ids) updateOne(context,manager,id);
        scheduleMinuteRefresh(context);
    }

    @Override public void onReceive(Context context, Intent intent) {
        super.onReceive(context,intent);
        if(intent==null || intent.getAction()==null) return;
        String a=intent.getAction();
        if("com.luisequeira612.jennieruby.MINUTE".equals(a)
            || Intent.ACTION_DATE_CHANGED.equals(a) || Intent.ACTION_TIME_CHANGED.equals(a)
            || Intent.ACTION_TIMEZONE_CHANGED.equals(a) || Intent.ACTION_LOCALE_CHANGED.equals(a)) {
            updateAll(context);
        }
    }

    private static void scheduleMinuteRefresh(Context context) {
        Intent i=new Intent(context,RubyClockWidgetProvider.class).setAction("com.luisequeira612.jennieruby.MINUTE");
        PendingIntent pi=PendingIntent.getBroadcast(context,991,i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
        AlarmManager alarms=(AlarmManager)context.getSystemService(Context.ALARM_SERVICE);
        if(alarms!=null) alarms.setInexactRepeating(AlarmManager.ELAPSED_REALTIME,
            SystemClock.elapsedRealtime()+60000,60000,pi);
    }

    private static void updateAll(Context context) {
        AppWidgetManager manager=AppWidgetManager.getInstance(context);
        int[] ids=manager.getAppWidgetIds(new ComponentName(context,RubyClockWidgetProvider.class));
        for(int id:ids) updateOne(context,manager,id);
    }

    private static void updateOne(Context context,AppWidgetManager manager,int id) {
        RemoteViews views=new RemoteViews(context.getPackageName(),R.layout.widget_ruby_clock);
        views.setImageViewBitmap(R.id.ruby_clock_bitmap,RubyWidgetBitmap.clock(context));
        Intent launch=new Intent(context,MainActivity.class);
        PendingIntent pi=PendingIntent.getActivity(context,id,launch,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
        views.setOnClickPendingIntent(R.id.ruby_clock_root,pi);
        manager.updateAppWidget(id,views);
    }
}
