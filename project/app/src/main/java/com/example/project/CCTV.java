package com.example.project;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class CCTV extends AppCompatActivity implements View.OnClickListener {
    //EditText editTextEmail;
    //EditText editTextPassword;
    //Button buttonSignup;
    //TextView textviewSingin;
    //TextView textviewMessage;
    //on create 밖에 onclik으로 분기할때는 private 하고 oncreate안에 작성할거면 private지우기
    // oncreate밖에 작성할 때는 calltext.setOnclickListner(this)지우기
    //안에 작성할 때는 calltext.seronclick~~{}
    private Button callText,cctvOnButton,cctvOffButton;
    ProgressDialog progressDialog;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.webview);
        callText=findViewById(R.id.callText);
        cctvOnButton=findViewById(R.id.cctvOnButton);
        cctvOffButton=findViewById(R.id.cctvOffButton);
        WebView webView = (WebView)findViewById(R.id.cctvWeb);
        String url ="http://192.168.0.9:8091/?action=stream";
        webView.loadUrl(url);
        webView.setPadding(0,0,0,0);
        //webView.setInitialScale(100);
        webView.getSettings().setBuiltInZoomControls(false);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);

        callText.setOnClickListener(this);
        cctvOnButton.setOnClickListener(this);
        cctvOffButton.setOnClickListener(this);
//        callText.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                AlertDialog.Builder builder = new AlertDialog.Builder(CCTV.this);
//                builder.setTitle("신고");
//                builder.setMessage("신고하시겠습니까?");
//                builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
//                    @Override
//                    public void onClick(DialogInterface dialog, int which) {
//                        Intent intent = new Intent(Intent.ACTION_DIAL, Uri.parse("tel:119"));
//                        startActivity(intent);
//                    }
//                });
//                builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
//                    @Override
//                    public void onClick(DialogInterface dialog, int which) {
//
//                    }
//                });
//                AlertDialog alertDialog = builder.create();
//                alertDialog.show();
//            }
//        });//신고


    }


    @Override
    public void onClick(View view) {
        if(view==callText){
            AlertDialog.Builder builder = new AlertDialog.Builder(CCTV.this);
            builder.setTitle("신고");
            builder.setMessage("신고하시겠습니까?");
            builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    Intent intent = new Intent(Intent.ACTION_DIAL, Uri.parse("tel:119"));
                    startActivity(intent);
                }
            });
            builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {

                }
            });
            AlertDialog alertDialog = builder.create();
            alertDialog.show();
        }
        else if(view==cctvOnButton){
            Toast.makeText(CCTV.this,"LED켜짐",Toast.LENGTH_SHORT).show();
            OkHttpClient client=new OkHttpClient();
            Request request=new Request.Builder()
                    .url("http://192.168.0.9:5000/on")
                    .build();
            client.newCall(request).enqueue(new Callback(){

                @Override
                public void onFailure(Call call, IOException e) {
                    call.cancel();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    final String myResponse=response.body().string();
                    CCTV.this.runOnUiThread(new Runnable(){

                        @Override
                        public void run() {
                            cctvOnButton.setText(myResponse);
                        }
                    });
                }
            });
        }
        else if(view==cctvOffButton){
            Toast.makeText(CCTV.this,"LED꺼짐",Toast.LENGTH_SHORT).show();
            OkHttpClient client=new OkHttpClient();
            Request request=new Request.Builder()
                    .url("http://192.168.0.9:5000/off")
                    .build();
            client.newCall(request).enqueue(new Callback(){

                @Override
                public void onFailure(Call call, IOException e) {
                    call.cancel();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    final String myResponse=response.body().string();
                    CCTV.this.runOnUiThread(new Runnable(){

                        @Override
                        public void run() {
                            cctvOffButton.setText(myResponse);
                        }
                    });
                }
            });
        }
    }
}
