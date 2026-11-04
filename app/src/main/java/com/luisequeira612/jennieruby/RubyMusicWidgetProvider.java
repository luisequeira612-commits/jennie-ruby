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
  if(packageName!=null){
   switch(packageName){
    case "com.spotify.music": name="ruby_spotify"; break;
    case "com.google.android.apps.youtube.music": name="ruby_youtube_music"; break;
    case "com.google.android.apps.maps": name="ruby_maps"; break;
    case "com.google.android.gm": name="ruby_gmail"; break;
    case "com.google.android.apps.docs": name="ruby_drive"; break;
    case "com.google.android.apps.photos": name="ruby_fotos"; break;
    case "com.google.android.calendar": name="ruby_calendario"; break;
    case "com.facebook.katana": name="ruby_facebook"; break;
    case "com.facebook.orca": name="ruby_messenger"; break;
    case "org.telegram.messenger": name="ruby_telegram"; break;
    case "com.snapchat.android": name="ruby_snapchat"; break;
    case "com.twitter.android": name="ruby_x"; break;
    case "com.pinterest": name="ruby_pinterest"; break;
    case "com.reddit.frontpage": name="ruby_reddit"; break;
    case "com.netflix.mediaclient": name="ruby_netflix"; break;
    case "com.disney.disneyplus": name="ruby_disney"; break;
    case "com.wbd.stream": name="ruby_hbo_max"; break;
    case "com.crunchyroll.crunchyroid": name="ruby_crunchyroll"; break;
    case "tv.twitch.android.app": name="ruby_twitch"; break;
    case "com.openai.chatgpt": name="ruby_chatgpt"; break;
    case "com.anthropic.claude": name="ruby_claude"; break;
    case "org.videolan.vlc": name="ruby_vlc"; break;
   }
  }
  int id=c.getResources().getIdentifier(name,"drawable",c.getPackageName());
  return id==0?R.drawable.ruby_music_note:id;
 }
 private static PendingIntent action(Context c,String a,int id){
  Intent i=new Intent(c,RubyMediaControlReceiver.class).setAction("com.luisequeira612.jennieruby."+a);
  return PendingIntent.getBroadcast(c,id*10+a.hashCode(),i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
 }
}
