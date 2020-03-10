package com.mss.binrunner;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

public class StartMyServiceAtBootReceiver extends BroadcastReceiver {
    private String TAG = "binrunner";
    @Override
    public void onReceive(Context context, Intent intent)
    {


        Toast.makeText(context, "Broadcast received", Toast.LENGTH_LONG).show();
        Log.e(TAG, "Broacast was Created");
        Intent myIntent=new Intent(context,ServiceBinrunner.class);
        myIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        context.startService(myIntent);
    }
}
