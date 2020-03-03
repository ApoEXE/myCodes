package com.mss.jav.getsdectec;

import android.content.Context;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.ImageFormat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.os.Handler;
import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;

import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
public class MainActivity extends AppCompatActivity {
 TextView tv_data,tv_1,tv_2,tv_3,tv_4,tv_5,tv_6;
 Button btn_open, btn_close;
 EditText et_ip, et_port;
 ImageView iv_pala;
    Handler timerHandler = new Handler();
    Runnable timerRunnable = new Runnable() {

        @Override
        public void run() {
            startProgress();

            timerHandler.postDelayed(this, 500);
        }
    };
    private CharSequence text = "Hello toast!";
    boolean cerrar=false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tv_data=(TextView) findViewById(R.id.tv_data);
        tv_1=(TextView) findViewById(R.id.tv_1);
        tv_2=(TextView) findViewById(R.id.tv_2);
        tv_3=(TextView) findViewById(R.id.tv_3);
        tv_4=(TextView) findViewById(R.id.tv_4);
        tv_5=(TextView) findViewById(R.id.tv_5);
        tv_6=(TextView) findViewById(R.id.tv_6);
        et_ip=(EditText) findViewById(R.id.et_ip);
        iv_pala = (ImageView) findViewById(R.id.iv_pala);
        et_port=(EditText) findViewById(R.id.et_port);
        btn_close=(Button)findViewById(R.id.btn_close);
        btn_open =(Button)findViewById(R.id.btn_open);
        btn_close.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                cerrar =true;
            }
        });
        btn_open.setText("open");
        btn_open.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                Button btn_open = (Button) v;
                if (btn_open.getText().equals("opened") ) {
                    timerHandler.removeCallbacks(timerRunnable);
                    btn_open.setText("open");
                } else{
                    timerHandler.postDelayed(timerRunnable, 0);
                    btn_open.setText("opened");
                }
            }
        });
    }
    //runs without a timer by reposting this handler at the end of the runnable
//####################################################################################
    public static int calculateSampleSize(BitmapFactory.Options options,
                                          int reqWidth, int reqHeight) {

        final int width = options.outWidth;
        final int height = options.outHeight;
        int inSampleSize = 1;

        if (width > reqWidth || height > reqHeight) {
            if (width > height) {
                inSampleSize = Math.round((float) height / (float) reqHeight);
            } else {
                inSampleSize = Math.round((float) width / (float) reqWidth);
            }
        }
        return inSampleSize;
    }

    //################################################################################   print
    private void print(CharSequence t) {
        text = t;
        //Toast toast = Toast.makeText(context, text, duration);
        //toast.show();
        Log.d("GETsDetect", (String) t);
    }
    //################################################################################ Socket Client
    byte diente[]=new byte[6];
    Bitmap bitmap;
    InputStream in=null;
    OutputStream out=null;
    DataOutputStream output =null;
    public void startProgress() {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                //------------------------------

                if (et_ip.getText().toString() != "0") {
                    if (Integer.parseInt(et_port.getText().toString()) > 1023) {
                        //code for connecting right here
                        print("Creando Socket");
                        Socket client = null;
                        try {
                            client = new Socket(et_ip.getText().toString(), Integer.parseInt(et_port.getText().toString()));
                            in = client.getInputStream();
                            out = client.getOutputStream();

                            //envio 100 a la Apalis TK1 para solicitar envio de data
                            out.write('d');

                            //recolecto la informacion enviada por el TK1 sobre estado de GETs
                            ByteArrayOutputStream baos = new ByteArrayOutputStream();
                            int valor = -1;
                            byte recibio[]=new byte[2048];
                            while((valor=in.read(recibio))!=-1){
                                baos.write(recibio,0,valor);
                            }
                            //extraigo los archivos obtenidos a un arreglo de bytes
                            byte byteArray[] = baos.toByteArray();
                            baos.flush();
                            baos.close();


                            //extraigo el tamaño total de byte recibido
                            byte[] sizeAr = new byte[4];

                            for (int i = 0; i < 4 ; ++i ) {
                                sizeAr[i] = byteArray[i];//     toByteArray()
                            }

                            //extraigo los dientes son 6 dientes
                             int sizeAll = ByteBuffer.wrap(sizeAr).asIntBuffer().get();

                            for (int i = 4; i < 10; ++i) {
                                System.out.print("  " + byteArray[i]);// imprimo tamano de imagen a recibir
                                diente[i-4] = byteArray[i];
                            }
                            System.out.println("");


                            //extraigo el tamaño de la imagen
                            byte sizeImagen[] = new byte[4];
                            for (int i = 10; i < 14 ; i++ ) {
                                sizeImagen[i - 10] = byteArray[i];
                            }
                            int size = ByteBuffer.wrap(sizeImagen).asIntBuffer().get();


                            //extraigo la imagen
                            byte[] imagen = new byte[size];
                            for (int i = 14; i < (size+14) ; ++i ) {

                                imagen[i - 14] = byteArray[i];
                            }



                            System.out.println("sizeAll: " + sizeAll);
                            System.out.println("size Imagen: " + size);
                            System.out.println();

                            /// Loads a Bitmap from a byte array

                            if(size>0) {

                              //cargo la imagen
                              bitmap = BitmapFactory.decodeByteArray(imagen,0,size);
                              System.out.println("Received " + bitmap.getWidth() + "x" + bitmap.getHeight());
                            }

  //proceso los datos obtenidos
                            btn_open.post(new Runnable() {
                                @Override
                                public void run() {
                                    iv_pala.setImageBitmap(bitmap);
                                    iv_pala.invalidate();

                                    String data="";
                                    for(int i=0;i<6;i++) {
                                        data += diente[i] + " ";
                                        switch(i) {
                                            case 0:
                                                if (diente[i] > 90)
                                                tv_1.setBackgroundColor(Color.GREEN);
                                                if (diente[i] > 80 && diente[i]<=90)
                                                    tv_1.setBackgroundColor(Color.YELLOW);
                                                if (diente[i] <= 80 && diente[i] >= 0)
                                                    tv_1.setBackgroundColor(Color.RED);
                                                if (diente[i] ==-1)
                                                    tv_1.setBackgroundColor(Color.BLACK);
                                            break;
                                            case 1:
                                                if (diente[i] > 90)
                                                    tv_2.setBackgroundColor(Color.GREEN);
                                                if (diente[i] > 80 && diente[i]<=90)
                                                    tv_2.setBackgroundColor(Color.YELLOW);
                                                if (diente[i] <= 80 && diente[i] >= 0)
                                                    tv_2.setBackgroundColor(Color.RED);
                                                if (diente[i] ==-1)
                                                    tv_2.setBackgroundColor(Color.BLACK);
                                                break;
                                            case 2:
                                                if (diente[i] > 90)
                                                    tv_3.setBackgroundColor(Color.GREEN);
                                                if (diente[i] > 80 && diente[i]<=90)
                                                    tv_3.setBackgroundColor(Color.YELLOW);
                                                if (diente[i] <= 80 && diente[i] >= 0)
                                                    tv_3.setBackgroundColor(Color.RED);
                                                if (diente[i] ==-1)
                                                    tv_3.setBackgroundColor(Color.BLACK);
                                                break;
                                            case 3:
                                                if (diente[i] > 90)
                                                    tv_4.setBackgroundColor(Color.GREEN);
                                                if (diente[i] > 80 && diente[i]<=90)
                                                    tv_4.setBackgroundColor(Color.YELLOW);
                                                if (diente[i] <= 80 && diente[i] >= 0)
                                                    tv_4.setBackgroundColor(Color.RED);
                                                if (diente[i] ==-1)
                                                    tv_4.setBackgroundColor(Color.BLACK);
                                                break;
                                            case 4:
                                                if (diente[i] > 90)
                                                    tv_5.setBackgroundColor(Color.GREEN);
                                                if (diente[i] > 80 && diente[i]<=90)
                                                    tv_5.setBackgroundColor(Color.YELLOW);
                                                if (diente[i] <= 80 && diente[i] >= 0)
                                                    tv_5.setBackgroundColor(Color.RED);
                                                if (diente[i] ==-1)
                                                    tv_5.setBackgroundColor(Color.BLACK);
                                                break;
                                            case 5:
                                                if (diente[i] > 90)
                                                    tv_6.setBackgroundColor(Color.GREEN);
                                                if (diente[i] > 80 && diente[i]<=90)
                                                    tv_6.setBackgroundColor(Color.YELLOW);
                                                if (diente[i] <= 80 && diente[i] >= 0)
                                                    tv_6.setBackgroundColor(Color.RED);
                                                if (diente[i] ==-1)
                                                    tv_6.setBackgroundColor(Color.BLACK);
                                                break;
                                        }
                                    }
                                    tv_data.setText(data.toString());

                                    try {
                                        in.close();
                                        out.close();
                                    } catch (IOException e) {
                                        System.out.println(e);

                                        System.out.println("Error de desconnexion");

                                    }

                                }
                            });
                            if(cerrar)
                                client.close();

                        } catch (IOException e) {
                            e.printStackTrace();
                            try {
                                in.close();
                                out.close();
                            } catch (IOException e1) {
                                e1.printStackTrace();

                                System.out.println("Error de desconnexion3");
                            }

                            System.out.println("Error de desconnexion2");
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
