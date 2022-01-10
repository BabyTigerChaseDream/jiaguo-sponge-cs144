//Subject: CSE434 Project 1
//Bing Hao 1203169937 26-Feb-14
import java.io.*;
import java.net.*;

class TCPClient
{

  public static void main(String args[]) throws Exception
  {

      //Init the client socket to null
    Socket sock = null;

      //Init stream reader and writer, since the TCP server receives stream
    PrintWriter outChara = null;
    BufferedReader sendLine = null;

      //Integer variable for storing port number of server
    int port;

      //If the port number is provided by the command line argument,use it.
      // Otherwise, the 9080 will be used as the default port
    if (args.length != 1)
    {
       System.out.println("Usage: Simplex-talk No Selected <port>");
       System.out.println("Usage: Simplex-talk Using Default Port 9080");
       port = 9080;
    }
    else
       port = Integer.parseInt(args[0]);

    try
    {
        //Create a client socket and connecting to the server which is running on the localhost, the port number is the
        //server's port
       sock = new Socket("localhost", port);

        //notify the user how to exit the client and prompt the user to send data
       System.out.println("Sending Request...");
       System.out.println("***Enter 'exit' for exit Client*****");

        //The new writer is created using the client socket output stream, the AUTO flush is set to be true, thus the output buffer will be flushed
       outChara = new PrintWriter(sock.getOutputStream(), true);

        // Create a reader to read the user inputs
       sendLine = new BufferedReader(
                                new InputStreamReader(System.in));

        //variables for while loop
       boolean done = false;
       int i=0;

        //Continue until the user sent exit or empty string
       while (!done)
       {
           //read a line of user input buffer and print it out
          String str= sendLine.readLine();
          outChara.println(str);

           //Exist the loop if the user input is empty or exit
          if (str == null || str.equals("exit"))
             done = true;
       }
        //flush the writer
       outChara.flush();
    }

    //Throw exceptions for host connection
    catch (UnknownHostException e)
    {
       System.err.println("Simplex-talk: Unknow host: "+args[0]);
       System.exit(1);
    }
    catch (IOException e)
    {
       System.err.println("Simplex-talk: Can not do the connection to: "+args[0]);
       System.exit(1);
    }
    catch(Exception e)
    {
       e.printStackTrace();
    }
    finally
    {
        //Close all input, output and client socket
       sendLine.close();
       outChara.close();
       sock.close();
    }
  }
}


