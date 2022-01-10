//Subject: CSE434 Project 1
//Bing Hao 1203169937 26-Feb-14
import java.io.*;
import java.net.*;

class UDPClient
{

  public static void main(String args[]) throws Exception
  {
      //InputStram in is used to send data to server with port number which saved in variable port
    InputStream in = null;
    int port;

      //If the port number is provided by the command line argument,use it.
      // Otherwise, the 9980 will be used as the default port
    if (args.length != 1)
    {
      System.out.println("Usage: Simplex-talk No Selected <port>");
      System.out.println("Usage: Simplex-talk Using Default Port 9980 for the packte");
      port = 9980;
    }
    else
      port = Integer.parseInt(args[0]);
//Show user how to use this program
    System.out.println("***Enter SPACE Key to Send Packet*****");
    System.out.println("***Enter ' . ' to Send packet and exit Client*****");

    try
    {
        //in is used to read user's inputs
      in = System.in;

        //Init the byte array output stream using the available length of input stream
      ByteArrayOutputStream inPut = new  ByteArrayOutputStream(in.available());

        //Variables for send loop
      boolean done = false;
      boolean send = false;
      Integer i = null;

        //Loop for sending data
      while(!done)
      {
        while(!send)
        {
            //init integer i to the value read from the input
          i = new Integer((int)in.read());

            //The user finished the inputting if the last character is space or dot
          if(i.toString().equals("32")||i.toString().equals("46"))
            send = true;
          else
            inPut.write(i.intValue());
        }
          //Finish sending data if read the dot
        if(i.toString().equals("46"))
          done = true;

          //Create a buffer for the datagram packet
        byte buffer[] = inPut.toByteArray();

          //Create a socket to connect the server
        DatagramSocket sock = new DatagramSocket();

          //The datagram is created using buffer as packet data, buffer.length as packet length, destination IP and port
        DatagramPacket pack = new DatagramPacket(buffer, buffer.length,
                                      InetAddress.getByName("localhost"),port);

          //Send the packet
        sock.send(pack);

          //Continue to send more data
        send = false;
      }
    }
    catch (Exception e)
    {
      e.printStackTrace();
    }
  }
}
