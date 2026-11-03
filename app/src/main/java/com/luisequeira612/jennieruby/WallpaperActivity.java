package com.luisequeira612.jennieruby;

import android.app.Activity;
import android.app.WallpaperManager;
import android.content.Intent;
import android.graphics.*;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.*;

import java.io.OutputStream;

public class WallpaperActivity extends Activity {
    private static final int[] NAMES = {0, 1, 2};
    private int pendingDesign = 0;
    private static final int BG = Color.rgb(12, 8, 11);
    private static final int ROSE = Color.rgb(235, 210, 218);
    private static final int MUTED = Color.rgb(177, 151, 160);

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        ScrollView scroll = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(20), dp(28), dp(20), dp(32));
        root.setBackgroundColor(BG);
        scroll.addView(root);

        TextView title = label("RUBY WALLPAPERS", 24, ROSE, true);
        title.setLetterSpacing(0.12f);
        root.addView(title);
        TextView intro = label("Tres conceptos originales para combinar con tus iconos. Guarda el PNG y aplícalo desde tu galería.", 14, MUTED, false);
        intro.setPadding(0, dp(8), 0, dp(20));
        root.addView(intro);

        String[] names = {"01  •  CRIMSON BLOOM", "02  •  RUBY ORBIT", "03  •  VELVET NIGHT"};
        String[] notes = {
            "Flores abstractas y tonos carmesí",
            "Órbita luminosa sobre negro profundo",
            "Capas suaves en borgoña y rosa"
        };
        for (int i = 0; i < 3; i++) {
            final int design = i;
            LinearLayout card = new LinearLayout(this);
            card.setOrientation(LinearLayout.VERTICAL);
            card.setPadding(dp(12), dp(12), dp(12), dp(12));
            GradientDrawable surface = new GradientDrawable();
            surface.setColor(Color.rgb(26, 16, 22));
            surface.setCornerRadius(dp(18));
            surface.setStroke(dp(1), Color.rgb(83, 31, 48));
            card.setBackground(surface);
            WallpaperPreview preview = new WallpaperPreview(this, design);
            card.addView(preview, new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT, dp(270)));
            TextView name = label(names[i], 13, ROSE, true);
            name.setPadding(0, dp(12), 0, dp(3));
            card.addView(name);
            card.addView(label(notes[i], 12, MUTED, false));
            Button save = new Button(this);
            save.setText("GUARDAR FONDO");
            save.setAllCaps(false);
            save.setTextColor(ROSE);
            save.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(112, 18, 43)));
            card.addView(save);
            Button apply = new Button(this);
            apply.setText("APLICAR EN INICIO");
            apply.setAllCaps(false);
            apply.setTextColor(ROSE);
            apply.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(70, 24, 42)));
            card.addView(apply);
            apply.setOnClickListener(v -> applyWallpaper(design));
            save.setOnClickListener(v -> {
                pendingDesign = design;
                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("image/png");
                intent.putExtra(Intent.EXTRA_TITLE, "Jennie-Ruby-" + (design + 1) + ".png");
                startActivityForResult(intent, 71);
            });
            LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
            cp.bottomMargin = dp(18);
            root.addView(card, cp);
        }
        setContentView(scroll);
    }

    private void applyWallpaper(int design) {
        Bitmap bitmap = Bitmap.createBitmap(1080, 2400, Bitmap.Config.ARGB_8888);
        try {
            Canvas canvas = new Canvas(bitmap);
            drawDesign(canvas, 1080, 2400, design);
            WallpaperManager.getInstance(this).setBitmap(bitmap);
            Toast.makeText(this, "Fondo aplicado a la pantalla de inicio.", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Toast.makeText(this, "Android no pudo aplicar el fondo. Puedes guardarlo como PNG.", Toast.LENGTH_LONG).show();
        } finally {
            bitmap.recycle();
        }
    }

    @Override protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 71 && resultCode == RESULT_OK && data != null && data.getData() != null) {
            try (OutputStream out = getContentResolver().openOutputStream(data.getData())) {
                if (out != null) {
                    Bitmap bitmap = Bitmap.createBitmap(1080, 2400, Bitmap.Config.ARGB_8888);
                    Canvas canvas = new Canvas(bitmap);
                    drawDesign(canvas, 1080, 2400, pendingDesign);
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, out);
                    bitmap.recycle();
                    Toast.makeText(this, "Fondo guardado. Ahora puedes aplicarlo desde Galería.", Toast.LENGTH_LONG).show();
                }
            } catch (Exception e) {
                Toast.makeText(this, "No se pudo guardar el fondo.", Toast.LENGTH_LONG).show();
            }
        }
    }

    private TextView label(String value, int size, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setText(value); t.setTextSize(size); t.setTextColor(color);
        t.setTypeface(Typeface.create("sans-serif", bold ? Typeface.BOLD : Typeface.NORMAL));
        return t;
    }
    private int dp(int value) { return (int)(value * getResources().getDisplayMetrics().density + 0.5f); }

    private static class WallpaperPreview extends View {
        private final int design;
        WallpaperPreview(Activity context, int design) { super(context); this.design = design; setLayerType(View.LAYER_TYPE_SOFTWARE, null); }
        @Override protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            drawDesign(canvas, getWidth(), getHeight(), design);
        }
    }

    private static void drawDesign(Canvas c, int w, int h, int design) {
        c.save();
        c.scale(w / 1080f, h / 2400f);
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        int[] colors = design == 0
                ? new int[]{Color.rgb(12,5,10), Color.rgb(85,8,34), Color.rgb(19,7,15)}
                : design == 1
                ? new int[]{Color.rgb(7,7,12), Color.rgb(49,9,31), Color.rgb(10,7,12)}
                : new int[]{Color.rgb(16,7,14), Color.rgb(65,13,35), Color.rgb(8,6,10)};
        p.setShader(new LinearGradient(0, 0, 900, 2400, colors, null, Shader.TileMode.CLAMP));
        c.drawRect(0, 0, 1080, 2400, p);
        p.setShader(null);
        if (design == 0) {
            for (int i = 0; i < 7; i++) {
                c.save(); c.rotate(i * 51f, 540, 1000);
                p.setColor(i % 2 == 0 ? Color.argb(70, 235, 130, 160) : Color.argb(55, 167, 25, 67));
                c.drawOval(390, 560, 690, 1130, p); c.restore();
            }
            p.setColor(Color.argb(180, 246, 220, 229)); c.drawCircle(540, 1000, 38, p);
            p.setColor(Color.argb(45, 255, 210, 225)); c.drawCircle(540, 1000, 250, p);
            p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(3); c.drawCircle(540, 1000, 250, p); p.setStyle(Paint.Style.FILL);
        } else if (design == 1) {
            p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(7);
            p.setColor(Color.argb(150, 232, 160, 181)); c.drawCircle(540, 1020, 320, p);
            p.setStrokeWidth(3); p.setColor(Color.argb(90, 246, 220, 229)); c.drawCircle(540, 1020, 410, p);
            p.setStyle(Paint.Style.FILL); p.setColor(Color.argb(220, 190, 35, 75)); c.drawCircle(790, 820, 45, p);
            p.setColor(Color.argb(90, 246, 220, 229)); c.drawCircle(340, 1190, 18, p);
            p.setColor(Color.argb(40, 235, 210, 218)); c.drawCircle(540, 1020, 90, p);
        } else {
            for (int i = 0; i < 6; i++) {
                p.setColor(Color.argb(24 + i * 7, 220, 75, 110));
                c.drawRoundRect(-120 + i * 110, 620 + i * 135, 1120, 1150 + i * 145, 180, 180, p);
            }
            p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4);
            p.setColor(Color.argb(110, 232, 160, 181));
            Path path = new Path(); path.moveTo(80, 1550); path.cubicTo(300, 1200, 760, 1900, 1000, 1420); c.drawPath(path, p);
            p.setStyle(Paint.Style.FILL);
        }
        p.setShader(null);
        p.setColor(Color.argb(180, 235, 210, 218)); p.setTextAlign(Paint.Align.CENTER); p.setTypeface(Typeface.create("serif", Typeface.BOLD)); p.setTextSize(48);
        c.drawText("J E N N I E", 540, 1980, p);
        p.setColor(Color.argb(210, 190, 35, 65)); p.setTextSize(30); c.drawText("R U B Y", 540, 2040, p);
        c.restore();
    }
}
