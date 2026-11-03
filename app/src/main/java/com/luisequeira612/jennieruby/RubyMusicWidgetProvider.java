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
 static void render(Context c,CharSequence title,CharSequence artist,Bitmap art,boolean playing,String packageName){
  AppWidgetManager m=AppWidgetManager.getInstance(c);int[] ids=m.getAppWidgetIds(new ComponentName(c,RubyMusicWidgetProvider.class));
  for(int id:ids){RemoteViews v=new RemoteViews(c.getPackageName(),R.layout.widget_ruby_music);
   v.setTextViewText(R.id.music_title,title==null||title.length()==0?"Sin reproducción":title);
   v.setTextViewText(R.id.music_artist,artist==null?"":artist);
   if(art!=null)v.setImageViewBitmap(R.id.music_art,art);else v.setImageViewResource(R.id.music_art,R.drawable.ruby_music_placeholder);
   v.setImageViewResource(R.id.music_play,playing?R.drawable.ruby_music_pause:R.drawable.ruby_music_play);
   int logo=appLogoResource(c,packageName);
   v.setImageViewResource(R.id.music_app_logo,logo);
   Intent launch=null;
   if(packageName!=null&&!packageName.isEmpty()){
    launch=c.getPackageManager().getLaunchIntentForPackage(packageName);
    if(launch==null) launch=new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER).setPackage(packageName);
   }
   if(launch!=null){
    launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    v.setOnClickPendingIntent(R.id.music_app_logo,PendingIntent.getActivity(c,id+7000,launch,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE));
   }
   v.setOnClickPendingIntent(R.id.music_previous,action(c,"PREVIOUS",id));
   v.setOnClickPendingIntent(R.id.music_play,action(c,"PLAY_PAUSE",id));
   v.setOnClickPendingIntent(R.id.music_next,action(c,"NEXT",id));
   m.updateAppWidget(id,v);
  }
 }
 private static int appLogoResource(Context c,String packageName){
  String name="ruby_music_note";
  if("com.spotify.music".equals(packageName)) name="ruby_spotify";
  else if("com.google.android.apps.youtube.music".equals(packageName)) name="ruby_youtube_music";
  else if(packageName!=null){
   String[] parts=packageName.split("\\.");
   String candidate="ruby_"+parts[parts.length-1].toLowerCase(java.util.Locale.ROOT);
   if("ruby.katana".equals(candidate)) candidate="ruby_facebook";
   int found=c.getResources().getIdentifier(candidate,"drawable",c.getPackageName());
   if(found!=0)return found;
  }
  int id=c.getResources().getIdentifier(name,"drawable",c.getPackageName());
  return id==0?R.drawable.ruby_music_note:id;
 }
 private static PendingIntent action(Context c,String a,int id){
  Intent i=new Intent(c,RubyMediaControlReceiver.class).setAction("com.luisequeira612.jennieruby."+a);
  return PendingIntent.getBroadcast(c,id*10+a.hashCode(),i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
 }
}
