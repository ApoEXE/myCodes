package com.mss.tpms;

import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.net.*;
import java.io.*;
import android.util.Log;
import android.content.*;
import android.widget.*;


public class readings extends AppCompatActivity {
    private static int POSCMD = 250;
    private TextView text1p, text1t, text1v, text2p, text2t, text2v, text3p, text3t, text3v, text4p, text4t, text4v, text5p, text5t, text5v, text6p, text6t, text6v;
    private Button btncon, btnclose;
    private EditText etip, etport;
    private float pression[];
    private float voltaje[];
    private float temperatura[];
    private int port = 0;
    private Context context = readings.this;
    private CharSequence text = "Hello toast!";
    int duration = Toast.LENGTH_SHORT;
    public int[] dataIn ;
    public boolean cerrar =false;
    //################################################################################   OnCreate
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_readings);
        setViewithCode();
        Log.d("TPMS", "Iniciando conexion");
        btnclose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                cerrar =true;
            }
        });

    }
    //################################################################################   print
    private void print(CharSequence t) {
        text = t;
        //Toast toast = Toast.makeText(context, text, duration);
        //toast.show();
        Log.d("TPMS", (String) t);
    }
    //################################################################################      readTires
    private void readTires(int[] dataIn) {
        //Nominal Values
        float presion = 758;
        float temperatura = 22;
        float voltaje = (float)2.6;
        boolean band = false;
        int size = 0;
        int[] s1 = new int[72];
        int[] s2 = new int[72];
        int[] s3 = new int[72];
        int[] s4 = new int[72];
        int[] s5 = new int[72];
        int[] s6 = new int[72];

        int[] readings = new int[500];
        for (int i = 0; i < dataIn.length; i++) {
            if (dataIn[i] == 0xA4) {
                size = dataIn[i + 1];
                System.out.println("tamano: " + size);
                ;
                for (int j = 0; j <= size; j++) {
                    readings[j] = dataIn[(i + 2) + j];
                }
                i = 500;
            }
        }

        for (int i = 0; i < size; i++) {
            if (i < 12)
                s1[i] = readings[i];
            if (i >= 12 && i < 24)
                s2[i - 12] = readings[i];
            if (i >= 24 && i < 36)
                s3[i - 24] = readings[i];
            if (i >= 36 && i < 48)
                s4[i - 36] = readings[i];
            if (i >= 48 && i < 60)
                s5[i - 48] = readings[i];
            if (i >= 60 && i < 72)
                s6[i - 60] = readings[i];
        }
        //##############################################RUEDA 1
        Long batt1 = (long) s1[3] << 24;
        batt1 |= (long) s1[2] << 16;
        batt1 |= (long) s1[1] << 8;
        batt1 |= (long) s1[0];
        Float f1b = Float.intBitsToFloat(batt1.intValue());
        if(f1b<2){
            text1p.setBackgroundColor(Color.rgb(0, 0, 0));
            text1t.setBackgroundColor(Color.rgb(0, 0, 0));
            text1v.setBackgroundColor(Color.rgb(0, 0, 0));
        }else
        text1v.setText(String.valueOf(String.format("%.2f",f1b))+" V");

        Long temp1 = (long) s1[7] << 24;
        temp1 |= (long) s1[6] << 16;
        temp1 |= (long) s1[5] << 8;
        temp1 |= (long) s1[4];
        Float f1t = Float.intBitsToFloat(temp1.intValue());
        text1t.setText(String.valueOf(String.format("%.2f",f1t))+"°C");

        Long press1 = (long) s1[11] << 24;
        press1 |= (long) s1[10] << 16;
        press1 |= (long) s1[9] << 8;
        press1 |= (long) s1[8];
        Float f1p = Float.intBitsToFloat(press1.intValue());
        if(f1b>2)
        if(f1p<presion) {
            text1p.setBackgroundColor(Color.rgb(255, 0, 0));
            text1t.setBackgroundColor(Color.rgb(255, 0, 0));
            text1v.setBackgroundColor(Color.rgb(255, 0, 0));
        }
        else {
            text1p.setBackgroundColor(Color.rgb(0, 255, 0));
            text1t.setBackgroundColor(Color.rgb(0, 255, 0));
            text1v.setBackgroundColor(Color.rgb(0, 255, 0));
        }
        f1p=f1p*(float)0.145;
        text1p.setText(String.valueOf(String.format("%.2f",f1p))+"PSI");
        //##############################################RUEDA 2
        Long batt2 = (long) s2[3] << 24;
        batt2 |= (long) s2[2] << 16;
        batt2 |= (long) s2[1] << 8;
        batt2 |= (long) s2[0];
        Float f2b = Float.intBitsToFloat(batt2.intValue());
        if(f2b<2){
            text2p.setBackgroundColor(Color.rgb(0, 0, 0));
            text2t.setBackgroundColor(Color.rgb(0, 0, 0));
            text2v.setBackgroundColor(Color.rgb(0, 0, 0));
        }else
        text2v.setText(String.valueOf(String.format("%.2f",f2b))+" V");

        Long temp2 = (long) s2[7] << 24;
        temp2 |= (long) s2[6] << 16;
        temp2 |= (long) s2[5] << 8;
        temp2 |= (long) s2[4];
        Float f2t = Float.intBitsToFloat(temp2.intValue());
        text2t.setText(String.valueOf(String.format("%.2f",f2t))+"°C");

        Long press2 = (long) s2[11] << 24;
        press2 |= (long) s2[10] << 16;
        press2 |= (long) s2[9] << 8;
        press2 |= (long) s2[8];
        Float f2p = Float.intBitsToFloat(press2.intValue());
        if(f2b>2)
        if(f2p<presion) {
            text2p.setBackgroundColor(Color.rgb(255, 0, 0));
            text2t.setBackgroundColor(Color.rgb(255, 0, 0));
            text2v.setBackgroundColor(Color.rgb(255, 0, 0));
        }
        else {
            text2p.setBackgroundColor(Color.rgb(0, 255, 0));
            text2t.setBackgroundColor(Color.rgb(0, 255, 0));
            text2v.setBackgroundColor(Color.rgb(0, 255, 0));
        }
        f2p=f2p*(float)0.145;
        text2p.setText(String.valueOf(String.format("%.2f",f2p))+"PSI");
        //##############################################RUEDA 3
        Long batt3 = (long) s3[3] << 24;
        batt3 |= (long) s3[2] << 16;
        batt3 |= (long) s3[1] << 8;
        batt3 |= (long) s3[0];
        Float f3b = Float.intBitsToFloat(batt3.intValue());
        if(f3b<2){
            text3p.setBackgroundColor(Color.rgb(0, 0, 0));
            text3t.setBackgroundColor(Color.rgb(0, 0, 0));
            text3v.setBackgroundColor(Color.rgb(0, 0, 0));
        }else
        text3v.setText(String.valueOf(String.format("%.2f",f3b))+" V");

        Long temp3 = (long) s3[7] << 24;
        temp3 |= (long) s3[6] << 16;
        temp3 |= (long) s3[5] << 8;
        temp3 |= (long) s3[4];
        Float f3t = Float.intBitsToFloat(temp3.intValue());
        text3t.setText(String.valueOf(String.format("%.2f",f3t))+"°C");

        Long press3 = (long) s3[11] << 24;
        press3 |= (long) s3[10] << 16;
        press3 |= (long) s3[9] << 8;
        press3 |= (long) s3[8];
        Float f3p = Float.intBitsToFloat(press3.intValue());
        if(f3b>2)
        if(f3p<presion) {
            text3p.setBackgroundColor(Color.rgb(255, 0, 0));
            text3t.setBackgroundColor(Color.rgb(255, 0, 0));
            text3v.setBackgroundColor(Color.rgb(255, 0, 0));
        }
        else {
            text3p.setBackgroundColor(Color.rgb(0, 255, 0));
            text3t.setBackgroundColor(Color.rgb(0, 255, 0));
            text3v.setBackgroundColor(Color.rgb(0, 255, 0));
        }
        f3p=f3p*(float)0.145;
        text3p.setText(String.valueOf(String.format("%.2f",f3p))+"PSI");
        //##############################################RUEDA 4
        Long batt4 = (long) s4[3] << 24;
        batt4 |= (long) s4[2] << 16;
        batt4 |= (long) s4[1] << 8;
        batt4 |= (long) s4[0];
        Float f4b = Float.intBitsToFloat(batt4.intValue());
        if(f4b<2){
            text4p.setBackgroundColor(Color.rgb(0, 0, 0));
            text4t.setBackgroundColor(Color.rgb(0, 0, 0));
            text4v.setBackgroundColor(Color.rgb(0, 0, 0));
        }else
        text4v.setText(String.valueOf(String.format("%.1f",f4b))+" V");

        Long temp4 = (long) s4[7] << 24;
        temp4 |= (long) s4[6] << 16;
        temp4 |= (long) s4[5] << 8;
        temp4 |= (long) s4[4];
        Float f4t = Float.intBitsToFloat(temp4.intValue());
        text4t.setText(String.valueOf(String.format("%.2f",f4t))+"°C");

        Long press4 = (long) s4[11] << 24;
        press4 |= (long) s4[10] << 16;
        press4 |= (long) s4[9] << 8;
        press4 |= (long) s4[8];
        Float f4p = Float.intBitsToFloat(press4.intValue());
        if(f4b>2)
        if(f4p<presion) {
            text4p.setBackgroundColor(Color.rgb(255, 0, 0));
            text4t.setBackgroundColor(Color.rgb(255, 0, 0));
            text4v.setBackgroundColor(Color.rgb(255, 0, 0));
        }
        else {
            text4p.setBackgroundColor(Color.rgb(0, 255, 0));
            text4t.setBackgroundColor(Color.rgb(0, 255, 0));
            text4v.setBackgroundColor(Color.rgb(0, 255, 0));
        }
        f4p=f4p*(float)0.145;
        text4p.setText(String.valueOf(String.format("%.2f",f4p))+"PSI");
        //##############################################RUEDA 5
        Long batt5 = (long) s5[3] << 24;
        batt5 |= (long) s5[2] << 16;
        batt5 |= (long) s5[1] << 8;
        batt5 |= (long) s5[0];
        Float f5b = Float.intBitsToFloat(batt5.intValue());
        if(f5b<2){
            text5p.setBackgroundColor(Color.rgb(0, 0, 0));
            text5t.setBackgroundColor(Color.rgb(0, 0, 0));
            text5v.setBackgroundColor(Color.rgb(0, 0, 0));
        }else
        text5v.setText(String.valueOf(String.format("%.2f",f5b))+" V");

        Long temp5 = (long) s5[7] << 24;
        temp5 |= (long) s5[6] << 16;
        temp5 |= (long) s5[5] << 8;
        temp5 |= (long) s5[4];
        Float f5t = Float.intBitsToFloat(temp5.intValue());
        text5t.setText(String.valueOf(String.format("%.2f",f5t))+"°C");

        Long press5 = (long) s5[11] << 24;
        press5 |= (long) s5[10] << 16;
        press5 |= (long) s5[9] << 8;
        press5 |= (long) s5[8];
        Float f5p = Float.intBitsToFloat(press5.intValue());
        if(f5b>2)
        if(f5p<presion) {
            text5p.setBackgroundColor(Color.rgb(255, 0, 0));
            text5t.setBackgroundColor(Color.rgb(255, 0, 0));
            text5v.setBackgroundColor(Color.rgb(255, 0, 0));
        }
        else {
            text5p.setBackgroundColor(Color.rgb(0, 255, 0));
            text5t.setBackgroundColor(Color.rgb(0, 255, 0));
            text5v.setBackgroundColor(Color.rgb(0, 255, 0));
        }
        f5p=f5p*(float)0.145;
        text5p.setText(String.valueOf(String.format("%.2f",f5p))+"PSI");
        //##############################################RUEDA 6
        Long batt6 = (long) s6[3] << 24;
        batt6 |= (long) s6[2] << 16;
        batt6 |= (long) s6[1] << 8;
        batt6 |= (long) s6[0];
        Float f6b = Float.intBitsToFloat(batt6.intValue());
        if(f6b<2){
            text6p.setBackgroundColor(Color.rgb(0, 0, 0));
            text6t.setBackgroundColor(Color.rgb(0, 0, 0));
            text6v.setBackgroundColor(Color.rgb(0, 0, 0));
        }else
        text6v.setText(String.valueOf(String.format("%.2f",f6b))+" V");

        Long temp6 = (long) s6[7] << 24;
        temp6 |= (long) s6[6] << 16;
        temp6 |= (long) s6[5] << 8;
        temp6 |= (long) s6[4];
        Float f6t = Float.intBitsToFloat(temp6.intValue());
        text6t.setText(String.valueOf(String.format("%.2f",f6t))+"°C");

        Long press6 = (long) s6[11] << 24;
        press6 |= (long) s6[10] << 16;
        press6 |= (long) s6[9] << 8;
        press6 |= (long) s6[8];
        Float f6p = Float.intBitsToFloat(press6.intValue());
        if(f6b>2)
        if(f6p<presion) {
            text6p.setBackgroundColor(Color.rgb(255, 0, 0));
            text6t.setBackgroundColor(Color.rgb(255, 0, 0));
            text6v.setBackgroundColor(Color.rgb(255, 0, 0));
        }
        else {
            text6p.setBackgroundColor(Color.rgb(0, 255, 0));
            text6t.setBackgroundColor(Color.rgb(0, 255, 0));
            text6v.setBackgroundColor(Color.rgb(0, 255, 0));
        }
        f6p=f6p*(float)0.145;
        text6p.setText(String.valueOf(String.format("%.2f",f6p))+"PSI");

    }
    //################################################################################   setView
    private void setViewithCode() {
        btncon = (Button) findViewById(R.id.btnCon);
        btnclose = (Button) findViewById(R.id.btnClose);

        text1p = (TextView) findViewById(R.id.text1P);
        text2p = (TextView) findViewById(R.id.text2P);
        text3p = (TextView) findViewById(R.id.text3P);
        text4p = (TextView) findViewById(R.id.text4P);
        text5p = (TextView) findViewById(R.id.text5P);
        text6p = (TextView) findViewById(R.id.text6P);
        text1t = (TextView) findViewById(R.id.text1T);
        text2t = (TextView) findViewById(R.id.text2T);
        text3t = (TextView) findViewById(R.id.text3T);
        text4t = (TextView) findViewById(R.id.text4T);
        text5t = (TextView) findViewById(R.id.text5T);
        text6t = (TextView) findViewById(R.id.text6T);
        text1v = (TextView) findViewById(R.id.text1V);
        text2v = (TextView) findViewById(R.id.text2V);
        text3v = (TextView) findViewById(R.id.text3V);
        text4v = (TextView) findViewById(R.id.text4V);
        text5v = (TextView) findViewById(R.id.text5V);
        text6v = (TextView) findViewById(R.id.text6V);

        etip = (EditText) findViewById(R.id.etIP);
        etport = (EditText) findViewById(R.id.etPort);
        etport.setText("6789");
        String ip = "192.168.1.200";
        etip.setText(ip);
    }
    //################################################################################   startProcess
    public void startProgress(View view) throws IOException{
        // do something long
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                //------------------------------
                cerrar=false;
                if (etip.getText().toString() != "0") {
                    if (Integer.parseInt(etport.getText().toString()) > 1023) {
                        //code for connecting right here
                        print("Creando Socket");
                        Log.d("socket","creando Socket");
                        //####################################################################################
                        Socket client = null;
                        int m=1;
                        pression=new float[7];
                        temperatura=new float[7];
                        voltaje=new float[7];
                        try {
                            client = new Socket(etip.getText().toString(), Integer.parseInt(etport.getText().toString()));

                            DataInputStream dis = new DataInputStream(client.getInputStream());//creo el input
                            DataOutputStream output = new DataOutputStream(client.getOutputStream());
                           output.writeByte(250);
                            m=1;
                            byte []raw=new byte[72];
                            /*
                            do {
                                //raw[m]=dis.readByte();

                                //m++;
                                Log.d("Float",Float.toString(dis.readFloat()));
                                //Log.d("bytes",Integer.toHexString(dis.readByte()));

                            }while(m<7);
*/
                            do {

                                pression[m] = dis.readFloat();
                                Log.d("Readings",Float.toString(pression[m]));
                                temperatura[m] = dis.readFloat();
                                Log.d("Readings",Float.toString(temperatura[m]));
                                voltaje[m] = dis.readFloat();
                                Log.d("Readings",Float.toString(voltaje[m]));
                                m++;
                            }while(m<7);
                            btncon.post(new Runnable() {
                                @Override
                                public void run() {
                                    //String.valueOf(String.format("%.2f",f5p))+"PSI"
                                    text1p.setText(String.valueOf(String.format("%.2f",pression[1])+"kPa"));
                                    text1t.setText(String.valueOf(String.format("%.2f",temperatura[1])+"C"));
                                    text1v.setText(String.valueOf(String.format("%.2f",voltaje[1])+"V"));
                                    text2p.setText(String.valueOf(String.format("%.2f",pression[2])+"kPa"));
                                    text2t.setText(String.valueOf(String.format("%.2f",temperatura[2])+"C"));
                                    text2v.setText(String.valueOf(String.format("%.2f",voltaje[2])+"V"));
                                    text3p.setText(String.valueOf(String.format("%.2f",pression[3])+"kPa"));
                                    text3t.setText(String.valueOf(String.format("%.2f",temperatura[3])+"C"));
                                    text3v.setText(String.valueOf(String.format("%.2f",voltaje[3])+"V"));
                                    text4p.setText(String.valueOf(String.format("%.2f",pression[4])+"kPa"));
                                    text4t.setText(String.valueOf(String.format("%.2f",temperatura[4])+"C"));
                                    text4v.setText(String.valueOf(String.format("%.2f",voltaje[4])+"V"));
                                    text5p.setText(String.valueOf(String.format("%.2f",pression[5])+"kPa"));
                                    text5t.setText(String.valueOf(String.format("%.2f",temperatura[5])+"C"));
                                    text5v.setText(String.valueOf(String.format("%.2f",voltaje[5])+"V"));
                                    text6p.setText(String.valueOf(String.format("%.2f",pression[6])+"kPa"));
                                    text6t.setText(String.valueOf(String.format("%.2f",temperatura[6])+"C"));
                                    text6v.setText(String.valueOf(String.format("%.2f",voltaje[6])+"V"));
                                }
                            });

                            if(cerrar)
                                client.close();
                        } catch(IOException e) {
                            //error = true;
                        }

                    } else {

                        print("Must set PORT>1024");
                    }
                } else {
                    print("Must set IP local");
                }




                //-------------------------------

            }
        };
        new Thread(runnable).start();
    }


}