package Java;

import com.example.app_tst1.Sender;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class listener {
    public static void main(String[] args) {
        try {
            start();
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    public static Sender getSender(byte[] buffer) throws Exception{
        ByteArrayInputStream bis = new ByteArrayInputStream(buffer);
        ObjectInput in = new ObjectInputStream(bis);
        Object o = in.readObject();
        return (Sender) o;
    }

    public static String arr2Str(float[] arr){
        if(arr==null){
            return "/./";
        }
        String str = "";
        for(int i=0;i<arr.length;i++){
            str+=String.valueOf(arr[i]) + " ";
        }
        return str;
    }

    public static void print(Sender s){
        s.getValues().forEach((key,value)->{
            System.out.println(key+" ==  "+arr2Str((float[])value));
        });
        System.out.println();
    }

    public static void start() throws Exception{
        System.out.println(InetAddress.getLocalHost().getHostName());
        ServerSocket ss = new ServerSocket(9000);
        System.out.println(ss.getInetAddress());
        System.out.println("Server listening....");
        DataInputStream dis = null;
        Socket accepted = ss.accept();
        dis = new DataInputStream(accepted.getInputStream());
        System.out.println("Connected to "+accepted.getRemoteSocketAddress());
        while(true){
            byte[] reader = new byte[4096];
            int read = dis.read(reader);
            if(read<0){
                continue;
            }
            byte[] buffer = new byte[read];
            System.out.println(buffer.length);
            java.lang.System.arraycopy(reader,0,buffer,0,read);
            Sender s = getSender(buffer);
            print(s);
        }
        
    }
}
