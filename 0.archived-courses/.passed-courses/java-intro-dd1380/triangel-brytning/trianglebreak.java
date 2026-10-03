import java.util.*;

public class trianglebreak {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String inputString = scanner.nextLine();

        // write out solution to the problem here
        // looping line that prints nextLine
        // get length of string
        int n = inputString.length();

        String currentLine = inputString;

        // take substring of whats remaining everytime, 0 to i
        // i = desired lineLength
        for (int i = 1; i <= n; i+=1){

            String ansLine;
            
            int currentLength = currentLine.length(); 

            if (i <= currentLength){
                ansLine = currentLine.substring(0, i);
                currentLine = currentLine.substring(i);
                System.out.println(ansLine);
            }
            else{
                ansLine = currentLine;
                System.out.println(ansLine);
                break;
            }
        }
    }
}
