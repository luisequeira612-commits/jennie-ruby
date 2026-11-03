package com.luisequeira612.jennieruby;

import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.widget.RemoteViews;

public class RubySignatureWidgetProvider extends AppWidgetProvider {
    @Override public void onUpdate(Context context,AppWidgetManager manager,int[] ids) {
        RemoteViews views=new RemoteViews(context.getPackageName(),R.layout.widget_ruby_signature);
        views.setImageViewBitmap(R.id.ruby_signature_bitmap,RubyWidgetBitmap.signature(context));
        for(int id:ids) manager.updateAppWidget(id,views);
    }
}
