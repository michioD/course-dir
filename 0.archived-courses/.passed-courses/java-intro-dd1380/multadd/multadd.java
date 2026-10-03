import java.util.*;

class multadd {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String inputString = scanner.nextLine();
        String[] inputParts = inputString.trim().split("\\s+");
        int n = inputParts.length;

        long[] e = new long[n];

        for (int i = 0; i < n; i+= 1){
            e[i] = Long.parseLong(inputParts[i]);
        }
        // Check addition first
        long additionFirst = e[0];
        if (n % 2 == 0) {
            additionFirst += e[n-1];
            for (int i = 1; i < n-1; i+=2){
                additionFirst += e[i] * e[i+1];
            }
        } else{
            for (int i = 1; i < n-1; i+=2){
                additionFirst += e[i] * e[i+1];
            }
        }
        long multFirst = 0;
        if (n % 2 == 0){
            for (int i = 0; i < n-1; i+=2){
                multFirst += e[i] * e[i+1];
            }
        }else{
            multFirst += e[n-1];
            for (int i = 0; i < n-2; i+=2){
                multFirst += e[i] * e[i+1];
            }
        }
        if (multFirst < additionFirst){
            System.out.println(additionFirst);
        } else{
            System.out.println(multFirst);
        }
    }
}
