package com.luisequeira612.jennieruby;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.Button;
import android.content.Intent;
import android.widget.TextView;

public class MainActivity extends Activity {
    private static final int BACKGROUND = Color.rgb(12, 8, 11);
    private static final int RUBY = Color.rgb(190, 35, 65);
    private static final int ROSE = Color.rgb(235, 210, 218);
    private static final int MUTED = Color.rgb(177, 151, 160);

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(dp(28), dp(36), dp(28), dp(36));
        root.setBackgroundColor(BACKGROUND);

        TextView eyebrow = text("A PERSONAL ICON COLLECTION", 10, MUTED, true);
        eyebrow.setLetterSpacing(0.18f);
        root.addView(eyebrow, centered());

        TextView title = text("JENNIE", 42, ROSE, true);
        title.setLetterSpacing(0.12f);
        LinearLayout.LayoutParams titleParams = centered();
        titleParams.topMargin = dp(12);
        root.addView(title, titleParams);

        TextView ruby = text("R U B Y", 16, RUBY, true);
        ruby.setLetterSpacing(0.28f);
        root.addView(ruby, centered());

        View divider = new View(this);
        GradientDrawable line = new GradientDrawable();
        line.setColor(RUBY);
        line.setCornerRadius(dp(2));
        divider.setBackground(line);
        LinearLayout.LayoutParams lineParams = new LinearLayout.LayoutParams(dp(52), dp(2));
        lineParams.gravity = Gravity.CENTER_HORIZONTAL;
        lineParams.topMargin = dp(28);
        lineParams.bottomMargin = dp(28);
        root.addView(divider, lineParams);

        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setPadding(dp(22), dp(22), dp(22), dp(22));
        GradientDrawable panelBackground = new GradientDrawable();
        panelBackground.setColor(Color.rgb(25, 16, 21));
        panelBackground.setCornerRadius(dp(18));
        panelBackground.setStroke(dp(1), Color.rgb(83, 31, 48));
        panel.setBackground(panelBackground);

        TextView heading = text("THE RUBY EDITION", 13, ROSE, true);
        heading.setLetterSpacing(0.08f);
        panel.addView(heading);

        TextView description = text(
                "A dark, elegant icon collection in black, crimson and dusty rose, made for Nova Launcher.",
                14, MUTED, false);
        description.setLineSpacing(dp(4), 1f);
        LinearLayout.LayoutParams descriptionParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        descriptionParams.topMargin = dp(12);
        panel.addView(description, descriptionParams);

        TextView status = text("146 CUSTOM ICONS  •  NOVA FILTER READY", 11, RUBY, true);
        status.setLetterSpacing(0.12f);
        LinearLayout.LayoutParams statusParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        statusParams.topMargin = dp(22);
        panel.addView(status, statusParams);

        TextView note = text(
                "The icon pack has been installed and applied successfully on a TECNO POVA 4 "
                        + "with Nova Launcher. To review or change it, open Nova Settings → "
                        + "Look & feel → Icon style → Icon theme and choose JENNIE RUBY.",
                12, ROSE, false);
        note.setLineSpacing(dp(3), 1f);
        LinearLayout.LayoutParams noteParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        noteParams.topMargin = dp(8);
        panel.addView(note, noteParams);

        LinearLayout.LayoutParams panelParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        root.addView(panel, panelParams);

        Button wallpapers = new Button(this);
        wallpapers.setText("EXPLORE RUBY WALLPAPERS");
        wallpapers.setTextColor(ROSE);
        wallpapers.setAllCaps(false);
        wallpapers.setTextSize(13);
        wallpapers.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(112, 18, 43)));
        LinearLayout.LayoutParams wallpaperParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(52));
        wallpaperParams.topMargin = dp(18);
        root.addView(wallpapers, wallpaperParams);
        wallpapers.setOnClickListener(v ->
                startActivity(new Intent(this, WallpaperActivity.class)));

        TextView footer = text("MADE FOR YOUR TECNO POVA 4  •  NOVA LAUNCHER", 9, MUTED, true);
        footer.setLetterSpacing(0.06f);
        LinearLayout.LayoutParams footerParams = centered();
        footerParams.topMargin = dp(30);
        root.addView(footer, footerParams);

        setContentView(root);
    }

    private TextView text(String value, int size, int color, boolean bold) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(color);
        view.setGravity(Gravity.CENTER);
        view.setTypeface(Typeface.create("sans-serif", bold ? Typeface.BOLD : Typeface.NORMAL));
        return view;
    }

    private LinearLayout.LayoutParams centered() {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        params.gravity = Gravity.CENTER_HORIZONTAL;
        return params;
    }

    private int dp(int value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }
}
