import java.util.LinkedList;
import java.util.Queue;

public class PercolationBFS extends PercolationDFSFast {

    /**
     * Initialize a grid so that all cells are blocked.
     *
     * @param n is the size of the simulated (square) grid
     */
    public PercolationBFS(int n) {
        super(n);
    }

    /**
     * fills a cell if it is open and not already full.  Also fills open cells connected to the cell
     * @param row is the row coordinate of the cell being checked/marked
     * @param col is the column of the cell being checked/marked
     */
    @Override
    protected void dfs(int row, int col) {
        // out of bounds?
        if (!inBounds(row, col)) return;

        // full or NOT open, don't process
        if (isFull(row, col) || !isOpen(row, col))
            return;

        myGrid[row][col] = FULL;
        Queue<Integer> qp = new LinkedList<>();
        qp.add(row * myGrid.length + col);
        while(qp.size() != 0){
            int i = qp.remove();
            int r = i / myGrid.length;
            int c = i % myGrid.length;
            if(inBounds(r - 1, c) && !isFull(r - 1, c) && isOpen(r -1 , c)){
                myGrid[r - 1][c] = FULL;
                qp.add((r -1) * myGrid.length + c);
            }
            if(inBounds(r + 1, c) && !isFull(r + 1, c) && isOpen(r +1 , c)){
                myGrid[r + 1][c] = FULL;
                qp.add((r +1) * myGrid.length + c);
            }
            if(inBounds(r, c + 1) && !isFull(r, c + 1) && isOpen(r , c + 1)){
                myGrid[r][c + 1] = FULL;
                qp.add(r * myGrid.length + c + 1);
            }
            if(inBounds(r, c - 1) && !isFull(r, c - 1) && isOpen(r , c - 1)){
                myGrid[r][c - 1] = FULL;
                qp.add(r * myGrid.length + c - 1);
            }
        }
    }


}
