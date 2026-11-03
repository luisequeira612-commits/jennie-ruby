package com.luisequeira612.jennieruby;
import android.content.*; import android.media.session.*; import android.content.ComponentName; import android.net.Uri;
public class RubyMediaControlReceiver extends BroadcastReceiver {
 @Override public void onReceive(Context c,Intent i){
  String a=i==null?"":i.getAction(); if(a==null)return;
  if(a.endsWith("OPEN_SPOTIFY")){Intent launch=c.getPackageManager().getLaunchIntentForPackage("com.spotify.music");if(launch!=null){launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);c.startActivity(launch);}return;}
  try{MediaSessionManager m=(MediaSessionManager)c.getSystemService(Context.MEDIA_SESSION_SERVICE);
   for(MediaController mc:m.getActiveSessions(new ComponentName(c,RubyMediaSessionService.class))){
    MediaController.TransportControls t=mc.getTransportControls();
    if(a.endsWith("PREVIOUS"))t.skipToPrevious();else if(a.endsWith("NEXT"))t.skipToNext();else if(a.endsWith("PLAY_PAUSE")){PlaybackState p=mc.getPlaybackState();if(p!=null&&p.getState()==PlaybackState.STATE_PLAYING)t.pause();else t.play();}
   }
  }catch(SecurityException ignored){}
 }
}
