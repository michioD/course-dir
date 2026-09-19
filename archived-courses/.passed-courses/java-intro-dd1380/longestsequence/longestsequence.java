import java.util.*;

class longestsequence {
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        String inputString = scanner.nextLine();
        String[] inputParts = inputString.trim().split("\\s+");
        int n = inputParts.length;

        int[] e = new int[n];

        for (int i = 0; i < n; i+= 1){
            e[i] = Integer.parseInt(inputParts[i]);
        }

        // TO DO 
        // Find longest subsequence in a1 a2 a3... s.t all elements are different
        int k = 0;
        int currentSequenceLength; 
        Set<Integer> hash;
        for (int i = 0; i < n; i +=1){
            hash = new HashSet<>();
            currentSequenceLength = 0;

            for (int j = i; j<n; j+=1){
                // System.out.println(hash.size());

                if (hash.contains(e[j])){
                    currentSequenceLength = j-i;
                    break;

                } else if (j == n-1){
                    currentSequenceLength = n-i;
                    break;
                }
                else{
                    hash.add(e[j]);
                }
            }
            if (k <= currentSequenceLength){
                k = currentSequenceLength;
            }
        }
        System.out.println(k);
    }
}
