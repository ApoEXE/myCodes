package com.mss.binrunner;


import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;


import java.io.ByteArrayOutputStream;
import java.io.Closeable;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramSocket;
import java.net.Socket;
import android.util.Log;

public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button button=findViewById(R.id.asyncTask);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AsyncTask.execute(new Runnable() {
                    @Override
                    public void run() {
                        Log.v("RUNNING","starting cmdtpms");
                        executeCommand("cmdtpms -i");
                    }
                });
            }
        });
    }

    
    public void executeCommandWithoutSu(String command) {
        try {
            Log.e("Commands", "executeCommand: " + command);
            writeLog(command);

            Process process = Runtime.getRuntime().exec(command);
            process.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
            Log.e("Commands", "error executing:" + command);
        }
    }
    
    private void writeLog(String command) {
        try {
            File file = new File("/sdcard/SuLog.txt");
    
            FileOutputStream outputStream = new FileOutputStream(file, file.length() < 1024 * 1024);
            outputStream.write((new Timestamp(new Date().getTime()).toString() + ": Executing: " + command + "\n").getBytes());
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
    
   //--------
    public static String sudoForResult(String...strings) {
        String res = "";
        DataOutputStream outputStream = null;
        InputStream response = null;
        try{
            Process su = Runtime.getRuntime().exec("su");
            outputStream = new DataOutputStream(su.getOutputStream());
            response = su.getInputStream();

            for (String s : strings) {
                outputStream.writeBytes(s+"\n");
                outputStream.flush();
            }

           // outputStream.writeBytes("exit\n");
            //outputStream.flush();
            try {
                su.waitFor();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            res = readFully(response);
            Log.v("RESP",res);
        } catch (IOException e){
            e.printStackTrace();
        } finally {
            Closer.closeSilently(outputStream, response);
        }
        return res;
    }
    public static String readFully(InputStream is) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int length = 0;
        while ((length = is.read(buffer)) != -1) {
            baos.write(buffer, 0, length);
        }
        return baos.toString("UTF-8");
    }










        //___________
    public static void sudo(String...strings) {
        try{
            Process su = Runtime.getRuntime().exec("su");
            DataOutputStream outputStream = new DataOutputStream(su.getOutputStream());

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
            outputStream.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }


}

class Closer {
    // closeAll()
    public static void closeSilently(Object... xs) {
        // Note: on Android API levels prior to 19 Socket does not implement Closeable
        final String TAG="closing ";
        for (Object x : xs) {
            if (x != null) {
                try {
                    Log.v(TAG,x.toString());
                    if (x instanceof Closeable) {
                        ((Closeable)x).close();
                    } else if (x instanceof Socket) {
                        ((Socket)x).close();
                    } else if (x instanceof DatagramSocket) {
                        ((DatagramSocket)x).close();
                    } else {
                        final String TAG2 = "cannot close: ";
                        Log.d(TAG2,x.toString());
                        throw new RuntimeException("cannot close "+x);
                    }
                } catch (Throwable e) {
                    final String TAG2 = "error: ";
                    Log.v(TAG2,e.toString());
                }
            }
        }
    }
}