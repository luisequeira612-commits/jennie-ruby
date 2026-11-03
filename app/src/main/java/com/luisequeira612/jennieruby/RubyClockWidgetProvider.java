package com.luisequeira612.jennieruby;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class RubyClockWidgetProvider extends AppWidgetProvider {
    private static final Locale SPANISH_NICARAGUA = new Locale("es", "NI");

    @Override
    public void onUpdate(Context context, AppWidgetManager manager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) {
            updateOne(context, manager, appWidgetId);
        }
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        super.onReceive(context, intent);

        if (intent == null || intent.getAction() == null) {
            return;
        }

        String action = intent.getAction();
        if (Intent.ACTION_DATE_CHANGED.equals(action)
                || Intent.ACTION_TIME_CHANGED.equals(action)
                || Intent.ACTION_TIMEZONE_CHANGED.equals(action)
                || Intent.ACTION_LOCALE_CHANGED.equals(action)) {
            updateAll(context);
        }
    }

    private static void updateAll(Context context) {
        AppWidgetManager manager = AppWidgetManager.getInstance(context);
        ComponentName component = new ComponentName(context, RubyClockWidgetProvider.class);
        int[] ids = manager.getAppWidgetIds(component);

        for (int appWidgetId : ids) {
            updateOne(context, manager, appWidgetId);
        }
    }

    private static void updateOne(Context context, AppWidgetManager manager, int appWidgetId) {
        RemoteViews views = new RemoteViews(
                context.getPackageName(),
                R.layout.widget_ruby_clock
        );

        views.setTextViewText(R.id.ruby_clock_date, formatSpanishDate(new Date()));

        Intent launch = new Intent(context, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(
                context,
                appWidgetId,
                launch,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );
        views.setOnClickPendingIntent(R.id.ruby_clock_root, pendingIntent);

        manager.updateAppWidget(appWidgetId, views);
    }

    private static String formatSpanishDate(Date date) {
        SimpleDateFormat formatter = new SimpleDateFormat(
                "EEE, d 'de' MMMM",
                SPANISH_NICARAGUA
        );
        String value = formatter.format(date);

        int comma = value.indexOf(", ");
        if (comma >= 0 && comma + 2 < value.length()) {
            value = value.substring(0, comma + 2)
                    + value.substring(comma + 2, comma + 3).toUpperCase(SPANISH_NICARAGUA)
                    + value.substring(comma + 3);
        }

        int monthStart = value.lastIndexOf(" de ");
        if (monthStart >= 0 && monthStart + 4 < value.length()) {
            int index = monthStart + 4;
            value = value.substring(0, index)
                    + value.substring(index, index + 1).toUpperCase(SPANISH_NICARAGUA)
                    + value.substring(index + 1);
        }

        return value;
    }
}
