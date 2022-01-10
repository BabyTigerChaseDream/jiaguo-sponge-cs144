//Subject: CSE434 Project 1
//Bing Hao 1203169937 26-Feb-14
import java.net.*;
import java.io.*;

public class UDPServer
{
  public static void main(String args[]) throws Exception
  {
     //Integer variable for storing port number
    int port;

      //If the port number is provided by the command line argument,use it.
      // Otherwise, the 9080 will be used as the default port
    if (args.length != 1)
    {
      System.out.println("Usage: No Selected <port>");
      System.out.println("Usage: Using Port 9980");
      port = 9980;
    }
    else
      port = Integer.parseInt(args[0]);

      //Using loop to receives data and print them out
    while(true)
    {
      try
      {
        //Create buffer for receiving data packets. For UDP connection the data is not stream but block of data
        byte buffer[] = new byte[1024];

          //Create buffer for the clients
        DatagramPacket pack = new DatagramPacket(buffer, 1024);

          //Create the server socket for clients
        DatagramSocket sock = new DatagramSocket(port);

          //Wait for a client to connect
        sock.receive(pack);

          //print out client's IP and port
          System.out.println("Client's IP: "+pack.getAddress().toString());
          System.out.println("Client's port: "+pack.getPort());

          //print out the content of the packet
        System.out.println("" +
		 new String(pack.getData(),pack.getOffset(),pack.getLength()));
          //close the server socket
        sock.close();
      }
      catch (Exception e)
      {
        e.printStackTrace();
      }
      System.out.println("Waitting for Client.....");
    }
  }
}
