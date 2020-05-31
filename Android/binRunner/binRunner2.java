import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;


import android.widget.EditText;
import android.widget.TextView;
import android.app.Activity;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class MainActivity extends Activity {

    EditText input;
    Button btn;
    TextView out;
    String command;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        input = (EditText)findViewById(R.id.txt);
        btn = (Button)findViewById(R.id.btn);
        out = (TextView)findViewById(R.id.out);
        btn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                /*
                ShellExecuter exe = new ShellExecuter();
                command = "cmdtpms -l";

                String outp = exe.Executer(command);
                out.setText(outp);
                Log.d("Output", outp);
                */
                sudo("cmdtpms -l");
            }
        });

    }
    public void sudo(String...strings) {
        StringBuffer output = new StringBuffer();
        try{
            Process su = Runtime.getRuntime().exec("su");
            DataOutputStream outputStream = new DataOutputStream(su.getOutputStream());

            BufferedReader reader = new BufferedReader(new InputStreamReader(su.getInputStream()));
            for (String s : strings) {
                outputStream.writeBytes(s+"\n");
                outputStream.flush();
            }

            outputStream.writeBytes("exit\n");
            outputStream.flush();
            try {
                su.waitFor();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            String line = "";
            while ((line = reader.readLine())!= null) {
                output.append(line + "\n");
            }

            outputStream.close();
        }catch(IOException e){
            e.printStackTrace();
        }
        String response = output.toString();
        out.setText(response);
        Log.d("Output", response);
    }

}


package com.mss.binrunner;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class ShellExecuter {
    public ShellExecuter() {

    }

    public String Executer(String command) {

        StringBuffer output = new StringBuffer();

        Process p;
        try {
            p = Runtime.getRuntime().exec(command);
            p.waitFor();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));

            String line = "";
            while ((line = reader.readLine())!= null) {
                output.append(line + "\n");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        String response = output.toString();
        return response;

    }
}


