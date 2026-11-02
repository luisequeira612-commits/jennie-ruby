package com.luisequeira612.jennieruby;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setPadding(32, 32, 32, 32);
        layout.setBackgroundColor(Color.rgb(12, 8, 11));
        TextView title = new TextView(this);
        title.setText("JENNIE RUBY");
        title.setTextColor(Color.rgb(190, 35, 65));
        title.setTextSize(28);
        title.setGravity(Gravity.CENTER);
        TextView status = new TextView(this);
        status.setText("Icon pack in development\\nRuby artwork and app mappings are being prepared.");
        status.setTextColor(Color.rgb(235, 210, 218));
        status.setTextSize(14);
        status.setGravity(Gravity.CENTER);
        status.setPadding(0, 20, 0, 0);
        layout.addView(title);
        layout.addView(status);
        setContentView(layout);
    }
}
