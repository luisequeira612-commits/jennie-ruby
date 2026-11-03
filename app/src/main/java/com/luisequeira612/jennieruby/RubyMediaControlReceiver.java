package com.luisequeira612.jennieruby;
import android.content.*; import android.media.session.*;
public class RubyMediaControlReceiver extends BroadcastReceiver {
 @Override public void onReceive(Context c,Intent i){
  String a=i==null?"":i.getAction();if(a==null)return;
  try{MediaSessionManager m=(MediaSessionManager)c.getSystemService(Context.MEDIA_SESSION_SERVICE);MediaController chosen=null;
   for(MediaController mc:m.getActiveSessions(new ComponentName(c,RubyMediaSessionService.class))){PlaybackState p=mc.getPlaybackState();if(p!=null&&p.getState()==PlaybackState.STATE_PLAYING){chosen=mc;break;}if(chosen==null)chosen=mc;}
   if(chosen==null)return;MediaController.TransportControls t=chosen.getTransportControls();
   if(a.endsWith("PREVIOUS"))t.skipToPrevious();else if(a.endsWith("NEXT"))t.skipToNext();else if(a.endsWith("PLAY_PAUSE")){PlaybackState p=chosen.getPlaybackState();if(p!=null&&p.getState()==PlaybackState.STATE_PLAYING)t.pause();else t.play();}
  }catch(SecurityException ignored){}
 }
}
