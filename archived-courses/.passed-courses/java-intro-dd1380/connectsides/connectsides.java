import java.util.*;

class connectsides {
    

    public static void main(String[] args) {
        // String[] rowStrings;
        Scanner scanner = new Scanner(System.in);
        String[] dims = scanner.nextLine().trim().split("\\s+");
        // row count
        int m = Integer.parseInt(dims[0]);
        // column count
        int n = Integer.parseInt(dims[1]);

        BitSet containsX = new BitSet(m * n);
        BitSet containsO = new BitSet(m*n);

        for (int i = 0; i < m; i++){
            String input = scanner.nextLine();
            for (int j = 0; j<n; j++){
                if (input.charAt(j)=='x'){
                    // # of elements in each row is = n and # of rows we've gone thru is i
                    containsX.set(j+i*n);
                }else{
                    containsO.set(j+i*n);
                }
            }

        }

        if (1<n && 1<m){
            int xCount = 0;
            int oCount = 0;
            for (int i = 0; i < m; i++){
                for (int j = 0; j < n; j++){
                    if (containsX.get(j+i*n)){
                        xCount++;
                    }
                    else{
                        oCount++;
                    }
                }
            }
            if (xCount!=oCount){
                System.out.println("fusk");
                return;
            }
        }

        // TO DO 
        // Make a LIFO queue of nodes (row,column pairs)
        // Make a visited node array
        boolean[][] visited = new boolean[m][n];
        int[] rawStack = new int[m*n]; 
        int tailIdx = -1; 

        for (int j = 0; j<n; j++){
            if (containsX.get(j + (m-1)*n)){
                visited[m-1][j] = true;
                rawStack[++tailIdx] = j + (m-1)*n;
            } 
        }

        while (tailIdx>-1){
            // tailIdx will always match the last non empty element
            // after popping the last element isnt technically removed in memory but its poised to be replaced. tailIdx will stand to the left of it regardless indicating that its symbolically "empty" 
            int node = rawStack[tailIdx--];

            int rowIdx = node / n;
            int colIdx = node % n; 
            if (rowIdx == 0){
                System.out.print("x");
                return;
            }
            if (0<rowIdx){
                if (containsX.get(colIdx + n*(rowIdx-1)) && !visited[rowIdx-1][colIdx]){
                    visited[rowIdx-1][colIdx] = true;
                    // never replace the tail element always replace the element to the right of it
                    rawStack[++tailIdx] = colIdx + n*(rowIdx-1);
                }
            }
            if (rowIdx<m-1){
                if (containsX.get( colIdx + (rowIdx + 1) * n) && !visited[rowIdx+1][colIdx]){
                    visited[rowIdx+1][colIdx] = true;
                    rawStack[++tailIdx] = colIdx + (rowIdx + 1) * n;
                }

            }
            if (0<colIdx){
                if (containsX.get(colIdx-1 + n*(rowIdx)) && !visited[rowIdx][colIdx-1]){
                    visited[rowIdx][colIdx-1] = true;
                    rawStack[++tailIdx] = colIdx-1 + n*(rowIdx);
                }
            }
            if (colIdx<n-1){
                if (containsX.get(colIdx + 1 + n * (rowIdx)) && !visited[rowIdx][colIdx+1]){
                    visited[rowIdx][colIdx+1] = true;
                    rawStack[++tailIdx] = colIdx + 1 + n * (rowIdx);
                }
            }
        }

        visited = new boolean[m][n];
        stack = new Stack<>();
        rawStack = new int[m*n];
        tailIdx = -1;

        for (int i = 0; i<m; i++){
            if (containsO.get(n-1 + n*i)){
                visited[i][n-1] = true;
                // int[] startNode = {i,n-1};
                rawStack[++tailIdx] = n-1 + i*n;
            } 
        }

        while (tailIdx>-1){
            int node = rawStack[tailIdx--];
            int rowIdx = node / n;
            int colIdx = node % n; 
            if (colIdx == 0){
                System.out.print("o");
                return;
            }
            if (0<rowIdx){
                if (containsO.get(colIdx + n*(rowIdx-1)) && !visited[rowIdx-1][colIdx]){
                    int[] newNode = {rowIdx-1,colIdx};
                    visited[rowIdx-1][colIdx] = true;
                    stack.push(newNode);
                    rawStack[++tailIdx] = colIdx + n*(rowIdx-1);
                }
            }
            if (rowIdx<m-1){
                if (containsO.get(colIdx + n * (rowIdx + 1)) && !visited[rowIdx+1][colIdx]){
                    visited[rowIdx+1][colIdx] = true;
                    rawStack[++tailIdx] = colIdx + (rowIdx + 1) * n;
                }

            }
            if (0<colIdx){
                if (containsO.get(colIdx - 1 + n * (rowIdx)) && !visited[rowIdx][colIdx-1]){
                    visited[rowIdx][colIdx-1] = true;
                    rawStack[++tailIdx] = colIdx-1 + n*(rowIdx);
                }
            }
            if (colIdx<n-1){
                if (containsO.get(colIdx + 1 + n * (rowIdx)) && !visited[rowIdx][colIdx+1]){
                    visited[rowIdx][colIdx+1] = true;
                    rawStack[++tailIdx] = colIdx + 1 + n * (rowIdx);
                }
            }
        }
        System.out.println("ingen");
        return;


    }
}
