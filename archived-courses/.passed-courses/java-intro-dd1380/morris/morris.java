import java.util.*;
class morris{

    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        int n = Integer.parseInt(scanner.nextLine());
        List<Integer> seq = new ArrayList<>();
        seq.add(1);
        for (int i = 1; i < n; i++){
            List<Integer> nextSeq = new ArrayList<>();
            int m = seq.size();
            int count = 0;

            // starting observer value
            int observeValue = seq.get(0);

            for (int j = 0; j < m; j++){
                if (seq.get(j) == observeValue){
                    count += 1;
                    
                }else{
                    nextSeq.add(count);
                    nextSeq.add(observeValue);
                    count = 1;
                    observeValue = seq.get(j);
                }
            }
            nextSeq.add(count);
            nextSeq.add(observeValue);
            seq = nextSeq;
        }
        StringBuilder ans = new StringBuilder();
        for (int x : seq){
            ans.append(x);
        }
        System.out.println(ans);
        
    }
}
