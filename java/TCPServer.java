//Subject: CSE434 Project 1
//Bing Hao 1203169937 26-Feb-14
import java.net.*;
import java.io.*;

public class TCPServer {
    public static void main(String args[]) throws Exception {
        //The integer variable which store the port number
        int port;

        //If the port number is provided by the command line argument,use it.
        // Otherwise, the 9080 will be used as the default port
        if (args.length != 1) {
            System.out.println("Usage: No Selected <port>");
            System.out.println("Usage: Using Port 9080");
            port = 9080;
        } else
            port = Integer.parseInt(args[0]);

        //Create a new server socket object to listen on the port stored in the variable port
        //The port number is assumed available (not used by another program)
        ServerSocket server = new ServerSocket(port);
        System.out.println("Server Started...at Port " + port);

        //print out the port which is listened by this server
        System.out.println("This server is listening on: " + port);

        //This server supports multi-clients
        while (true) {
            //Accept a connection
            Socket sock = server.accept();

            //Print out the client's IP address, port number, and notify the user that the
            //connection has been created
            System.out.println("Client's IP: " + sock.getInetAddress().toString());
            System.out.println("Client Port: " + sock.getPort());
            System.out.println("Accepting a Request...");

            //Call the performRequest method and pass the client socket to it
            performRequest(sock);
        }
    }

    //Get the data from datagram
    public static void performRequest(Socket sock) throws Exception {
        //Stream reader reads data from the socket
        //For TCP connection, the client's data is received as stream.
        BufferedReader inChara = new BufferedReader(new InputStreamReader(sock.getInputStream()));

        //variables for while loop
        boolean done = false;
        int i = 0;

        //the loop will exist if the sting is empty or get the message exit, otherwise print out
        //the data and continue the loop
        while (!done) {
            i++;
            String str = inChara.readLine();
            if (str == null || str.equals("exit"))
                done = true;
            else
                System.out.println("From Client :" + str);
        }

        //Close all input, output streams and the client socket
        //The socket is still open for following clients
        inChara.close();
        sock.close();
        System.out.println("Waiting for Client.....");
    }
}
