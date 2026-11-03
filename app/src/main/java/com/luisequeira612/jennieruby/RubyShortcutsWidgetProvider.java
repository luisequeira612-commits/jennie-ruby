package com.luisequeira612.jennieruby;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;

public class RubyShortcutsWidgetProvider extends AppWidgetProvider {
    @Override
    public void onUpdate(Context context, AppWidgetManager manager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) {
            RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget_ruby_shortcuts);

            Intent appIntent = new Intent(context, MainActivity.class);
            PendingIntent appPending = PendingIntent.getActivity(
                    context, 101, appIntent,
                    PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            views.setOnClickPendingIntent(R.id.ruby_shortcut_app, appPending);

            Intent wallpaperIntent = new Intent(context, WallpaperActivity.class);
            PendingIntent wallpaperPending = PendingIntent.getActivity(
                    context, 102, wallpaperIntent,
                    PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            views.setOnClickPendingIntent(R.id.ruby_shortcut_wallpapers, wallpaperPending);

            manager.updateAppWidget(appWidgetId, views);
        }
    }
}
