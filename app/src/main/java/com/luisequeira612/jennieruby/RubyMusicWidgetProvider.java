package com.luisequeira612.jennieruby;
import android.app.PendingIntent;
import android.appwidget.*;
import android.content.*;
import android.graphics.Bitmap;
import android.widget.RemoteViews;
public class RubyMusicWidgetProvider extends AppWidgetProvider {
 @Override public void onUpdate(Context c,AppWidgetManager m,int[] ids){RubyMediaSessionService.refresh(c);}
 @Override public void onEnabled(Context c){RubyMediaSessionService.refresh(c);}
 @Override public void onReceive(Context c,Intent i){super.onReceive(c,i);if(i!=null&&"com.luisequeira612.jennieruby.MUSIC_REFRESH".equals(i.getAction()))RubyMediaSessionService.refresh(c);}
 static void render(Context c,CharSequence title,CharSequence artist,Bitmap art,boolean playing){
  AppWidgetManager m=AppWidgetManager.getInstance(c);int[] ids=m.getAppWidgetIds(new ComponentName(c,RubyMusicWidgetProvider.class));
  for(int id:ids){RemoteViews v=new RemoteViews(c.getPackageName(),R.layout.widget_ruby_music);
   v.setTextViewText(R.id.music_title,title==null||title.length()==0?"Sin reproducción":title);
   v.setTextViewText(R.id.music_artist,artist==null?"":artist);
   if(art!=null)v.setImageViewBitmap(R.id.music_art,art);else v.setImageViewResource(R.id.music_art,R.drawable.ruby_music_placeholder);
   v.setImageViewResource(R.id.music_play,playing?R.drawable.ruby_music_pause:R.drawable.ruby_music_play);
   v.setOnClickPendingIntent(R.id.music_previous,action(c,"PREVIOUS",id));
   v.setOnClickPendingIntent(R.id.music_play,action(c,"PLAY_PAUSE",id));
   v.setOnClickPendingIntent(R.id.music_next,action(c,"NEXT",id));
   m.updateAppWidget(id,v);
  }
 }
 private static PendingIntent action(Context c,String a,int id){
  Intent i=new Intent(c,RubyMediaControlReceiver.class).setAction("com.luisequeira612.jennieruby."+a);
  return PendingIntent.getBroadcast(c,id*10+a.hashCode(),i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
 }
}
