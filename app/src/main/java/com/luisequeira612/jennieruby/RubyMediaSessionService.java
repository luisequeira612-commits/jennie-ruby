package com.luisequeira612.jennieruby;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.content.*; import android.media.MediaMetadata; import android.media.session.*; import android.os.*; import android.graphics.Bitmap;
import java.util.List;
public class RubyMediaSessionService extends NotificationListenerService {
 private MediaSessionManager manager; private MediaSessionManager.OnActiveSessionsChangedListener listener;
 private BroadcastReceiver screenReceiver;
 @Override public void onListenerConnected(){super.onListenerConnected();manager=(MediaSessionManager)getSystemService(MEDIA_SESSION_SERVICE);
  listener=this::render; try{manager.addOnActiveSessionsChangedListener(listener,new ComponentName(this,RubyMediaSessionService.class));render(manager.getActiveSessions(new ComponentName(this,RubyMediaSessionService.class)));}catch(SecurityException ignored){}
  screenReceiver=new BroadcastReceiver(){@Override public void onReceive(Context c,Intent i){RubyClockWidgetProvider.updateAll(c);try{render(manager.getActiveSessions(new ComponentName(c,RubyMediaSessionService.class)));}catch(Exception ignored){}}};
  IntentFilter f=new IntentFilter();f.addAction(Intent.ACTION_SCREEN_ON);f.addAction(Intent.ACTION_USER_PRESENT);
  if(Build.VERSION.SDK_INT>=33)registerReceiver(screenReceiver,f,Context.RECEIVER_NOT_EXPORTED);else registerReceiver(screenReceiver,f);
 }
 @Override public void onListenerDisconnected(){if(manager!=null&&listener!=null)manager.removeOnActiveSessionsChangedListener(listener);if(screenReceiver!=null)try{unregisterReceiver(screenReceiver);}catch(Exception ignored){}super.onListenerDisconnected();}
 @Override public void onNotificationPosted(StatusBarNotification s){if(manager!=null)try{render(manager.getActiveSessions(new ComponentName(this,RubyMediaSessionService.class)));}catch(SecurityException ignored){}}
 static void refresh(Context c){try{MediaSessionManager m=(MediaSessionManager)c.getSystemService(Context.MEDIA_SESSION_SERVICE);renderNow(c,m.getActiveSessions(new ComponentName(c,RubyMediaSessionService.class)));}catch(Exception ignored){}}
 private static void renderNow(Context c,List<MediaController> sessions){MediaController mc=select(sessions);if(mc==null){RubyMusicWidgetProvider.render(c,"Sin reproducción","",null,false);return;}MediaMetadata md=mc.getMetadata();CharSequence title=md==null?"":md.getDescription().getTitle();CharSequence artist=md==null?"":md.getString(MediaMetadata.METADATA_KEY_ARTIST);if(artist==null||artist.length()==0)artist=md==null?"":md.getDescription().getSubtitle();Bitmap art=md==null?null:md.getBitmap(MediaMetadata.METADATA_KEY_ART);if(art==null&&md!=null)art=md.getBitmap(MediaMetadata.METADATA_KEY_ALBUM_ART);PlaybackState ps=mc.getPlaybackState();RubyMusicWidgetProvider.render(c,title,artist,art,ps!=null&&ps.getState()==PlaybackState.STATE_PLAYING);}
 private void render(List<MediaController> sessions){renderNow(this,sessions);}
 private static MediaController select(List<MediaController> sessions){if(sessions==null)return null;for(MediaController mc:sessions){PlaybackState ps=mc.getPlaybackState();if(ps!=null&&ps.getState()==PlaybackState.STATE_PLAYING)return mc;}return sessions.isEmpty()?null:sessions.get(0);}
}
