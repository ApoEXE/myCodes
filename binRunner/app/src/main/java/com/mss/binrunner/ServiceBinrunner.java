package com.mss.binrunner;

import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;

public class ServiceBinrunner extends Service {
    private int counter;
    private String TAG = "binrunner";
    @Override
    public void onCreate() {
        Toast.makeText(this, "Service was Created", Toast.LENGTH_LONG).show();
        Log.e(TAG, "Service was Created");
    }
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        counter=0;

        runMultipleAsyncTask(); // Start Async Task
        return Service.START_NOT_STICKY;
    }


    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    private void writeLog(String command) {
        try {
            File file = new File("/sdcard/SuLog.txt");

            FileOutputStream outputStream = new FileOutputStream(file, file.length() < 1024 * 1024);
            outputStream.write(("Executing: " + command + "\n").getBytes());
            outputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void executeCommand(String command) {
        try {
            Log.e(TAG, "executeCommand: " + command);
            writeLog(command);

            Process process = Runtime.getRuntime().exec(new String[]{"su", "-c", command});
            process.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
            Log.e(TAG, "error executing:" + command);
        }
    }





    private void runMultipleAsyncTask() // Run Multiple Async Task
    {
        FirstAsyncTask asyncTask = new FirstAsyncTask(); // First

            asyncTask.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);

        SecondAsyncTask asyncTask2 = new SecondAsyncTask(); // Second

            asyncTask2.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
        //executeCommand("input keyevent 4");

    }

    //Start First Async Task:
    private class FirstAsyncTask extends AsyncTask<Void, Void, Void>
    {
        @Override
        protected void onPreExecute()
        {
            Log.i(TAG ,"FirstOnPreExecute()");
        }
        @Override
        protected Void doInBackground(Void... params)
        {
                Log.i(TAG ,"FirstAsyncTask");
                try
                {

                    while(true) {
                        Log.d(TAG, "STARTING cmdtpms");
                        executeCommand("cmdtpms -i");
                        Log.d(TAG,"CLOSED cmdtpms");
                        Thread.sleep(1000);
                    }

                }
                catch (InterruptedException exception) {
                    exception.printStackTrace();
                }
            return null;
        }
        @Override
        protected void onPostExecute(Void result)
        {
            Log.d(TAG ,"FirstonPostExecute() DONE");
        }
    }
    //Start Second Async Task:
    private class SecondAsyncTask extends AsyncTask<Void, Void, Void>
    {
        @Override
        protected void onPreExecute()
        {
            Log.i(TAG ,"SecondOnPreExecute()");
        }
        @Override
        protected Void doInBackground(Void... params)
        {
                Log.d(TAG ,"SecondAsyncTask");
                try
                {
                    while(true) {
                        Log.d(TAG, "SAVING PID");
                        executeCommand("ps | echo $(grep cmdtpms) > /sdcard/pid.txt ");
                        Log.d(TAG, "SAVED PID /sdcard/pid.txt");

                        if (counter >= 360) {
                            File fileEvents = new File("/sdcard/pid.txt");
                            StringBuilder text = new StringBuilder();
                            try {
                                BufferedReader br = new BufferedReader(new FileReader(fileEvents));
                                String line;
                                while ((line = br.readLine()) != null) {
                                    text.append(line);
                                    //text.append('\n');
                                }
                                br.close();
                            } catch (IOException e) {
                            }
                            String result = text.toString();
                            String[] PID = result.split(" ");
                            Log.d(TAG, PID[1]);
                            Log.d(TAG, "KILLING cmdtpms");
                            executeCommand("kill "+PID[1]);
                            Log.d(TAG, "KILLED cmdtpms");
                            counter=0;

                        }

                        Thread.sleep(10000);
                        counter+=1;
                    }


                }
                catch (InterruptedException exception)
                {
                    exception.printStackTrace();
                }
            return null;
        }
        @Override
        protected void onPostExecute(Void result)
        {
            Log.d("AsyncTask" ,"SecondOnPostExecute()");
        }
    }




}
