import java.io.*;
import java.net.*;

public class SMTP {

    public static void main(String args[]) throws IOException,
            UnknownHostException {
        String Message = "Hi, how are you doing?";
        String from = "Bing.Hao@asu.edu";
        String to = "Bing.Hao@asu.edu";
        String mailHost = "smtp.asu.edu";
        String subject = "Test Message";
        SMTPSender mail = new SMTPSender(mailHost);
        if (mail != null) {
            if (mail.send( Message, from, to,subject)) {
                System.out.println("Mail sent.");
            } else {
                System.out.println("Connect to SMTP server failed!");
            }
        }
        System.out.println("Done.");
    }

    static class SMTPSender {
        private final static int SMTP_PORT = 25;

        InetAddress mailHost;
        InetAddress localhost;
        BufferedReader in;
        PrintWriter out;

        public SMTPSender(String host) throws UnknownHostException {
            mailHost = InetAddress.getByName(host);
            localhost = InetAddress.getLocalHost();
            System.out.println("mailhost = " + mailHost);
            System.out.println("localhost= " + localhost);
            System.out.println("SMTP constructor done\n");
        }

        public boolean send(String Message, String from, String to, String subject)
                throws IOException {
            Socket smtpPipe;
            InputStream inn;
            OutputStream outt;
            BufferedReader msg;

            StringReader sr= new StringReader(Message); // wrap  String
            BufferedReader br= new BufferedReader(sr); // wrap StringReader

            msg = new BufferedReader(br);
            smtpPipe = new Socket(mailHost, SMTP_PORT);
            if (smtpPipe == null) {
                return false;
            }
            inn = smtpPipe.getInputStream();
            outt = smtpPipe.getOutputStream();
            in = new BufferedReader(new InputStreamReader(inn));
            out = new PrintWriter(new OutputStreamWriter(outt), true);
            if (inn == null || outt == null) {
                System.out.println("Failed to open streams to socket.");
                return false;
            }
            String initialID = in.readLine();
            System.out.println(initialID);
            System.out.println("HELO " + localhost.getHostName());
            out.println("HELO " + localhost.getHostName());
            String welcome = in.readLine();
            System.out.println(welcome);
            System.out.println("MAIL From:<" + from + ">");
            out.println("MAIL From:<" + from + ">");
            String senderOK = in.readLine();
            System.out.println(senderOK);
            System.out.println("RCPT TO:<" + to + ">");
            out.println("RCPT TO:<" + to + ">");
            String recipientOK = in.readLine();
            System.out.println(recipientOK);

            System.out.println("SUBJECT:<"+subject+">");
            out.println("SUBJECT:<"+subject+">");
            String subjectOK = in.readLine();
            System.out.println(subjectOK);


            System.out.println("DATA");
            out.println("DATA");
            String line;
            while ((line = msg.readLine()) != null) {
                out.println(line);
            }
            System.out.println(".");
            out.println(".");
            String acceptedOK = in.readLine();
            System.out.println(acceptedOK);
            System.out.println("QUIT");
            out.println("QUIT");
            return true;
        }
    }
}