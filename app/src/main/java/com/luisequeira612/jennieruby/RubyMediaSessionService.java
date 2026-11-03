package com.luisequeira612.jennieruby;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.content.*; import android.media.session.*; import android.os.*; import android.graphics.Bitmap;
import java.util.List;
public class RubyMediaSessionService extends NotificationListenerService {
 private MediaSessionManager manager; private MediaSessionManager.OnActiveSessionsChangedListener listener;
 @Override public void onListenerConnected(){super.onListenerConnected();manager=(MediaSessionManager)getSystemService(MEDIA_SESSION_SERVICE);
  listener=controllers->{render(controllers);};try{manager.addOnActiveSessionsChangedListener(listener,new ComponentName(this,RubyMediaSessionService.class));render(manager.getActiveSessions(new ComponentName(this,RubyMediaSessionService.class)));}catch(SecurityException ignored){}
 }
 @Override public void onListenerDisconnected(){if(manager!=null&&listener!=null)manager.removeOnActiveSessionsChangedListener(listener);super.onListenerDisconnected();}
 @Override public void onNotificationPosted(StatusBarNotification s){if(manager!=null)try{render(manager.getActiveSessions(new ComponentName(this,RubyMediaSessionService.class)));}catch(SecurityException ignored){}}
 static void refresh(Context c){Intent i=new Intent(c,RubyMediaSessionService.class);try{c.startService(i);}catch(Exception ignored){}}
 private void render(List<MediaController> sessions){
  MediaController chosen=null;
  if(sessions!=null)for(MediaController mc:sessions){PlaybackState ps=mc.getPlaybackState();if(ps!=null&&ps.getState()==PlaybackState.STATE_PLAYING){chosen=mc;break;}}
  if(chosen==null&&sessions!=null&&!sessions.isEmpty())chosen=sessions.get(0);
  if(chosen==null){RubyMusicWidgetProvider.render(this,"Sin reproducción","",null,false);return;}
  MediaMetadata md=chosen.getMetadata();CharSequence title=md==null?"":md.getDescription().getTitle();
  CharSequence artist=md==null?"":md.getDescription().getSubtitle();
  Bitmap art=md==null?null:md.getBitmap(MediaMetadata.METADATA_KEY_ART);
  if(art==null&&md!=null)art=md.getBitmap(MediaMetadata.METADATA_KEY_ALBUM_ART);
  PlaybackState ps=chosen.getPlaybackState();boolean playing=ps!=null&&ps.getState()==PlaybackState.STATE_PLAYING;
  RubyMusicWidgetProvider.render(this,title,artist,art,playing);
 }
}
