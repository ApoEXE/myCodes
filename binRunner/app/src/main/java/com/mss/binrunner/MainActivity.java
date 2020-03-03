package com.mss.binrunner;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.SystemClock;
import android.util.Log;


import java.io.File;
import java.io.FileOutputStream;



public class MainActivity extends Activity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
       // setContentView(R.layout.activity_main);

                AsyncTask.execute(new Runnable() {
                    @Override
                    public void run() {
                        while(true) {
                            Log.v("RUNNING", "starting cmdtpms");

                            executeCommand("cmdtpms -i");
                            Log.v("RESTART","Receptor reset");
                            SystemClock.sleep(1000);

                        }
                    }
                });
    }



    private void writeLog(String command) {
        try {
            File file = new File("/sdcard/SuLog.txt");

            FileOutputStream outputStream = new FileOutputStream(file, file.length() < 1024 * 1024);
            outputStream.write((": Executing: " + command + "\n").getBytes());
            outputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void executeCommand(String command) {
        try {
            Log.e("Commands", "executeCommand: " + command);
            writeLog(command);

            Process process = Runtime.getRuntime().exec(new String[]{"su", "-c", command});
            process.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
            Log.e("Commands", "error executing:" + command);
        }
    }

}

