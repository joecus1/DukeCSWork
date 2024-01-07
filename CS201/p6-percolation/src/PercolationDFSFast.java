public class PercolationDFSFast extends PercolationDFS {

    /**
     * Initialize a grid so that all cells are blocked.
     *
     * @param n is the size of the simulated (square) grid
     */
    public PercolationDFSFast(int n) {
        super(n);
    }

    /**
     * A more efficient version of updateOnOpen compared to the one in PercolationDFS.
     * Calls dsf function on the cell if the cell is in the top row or if any cells next to
     * it are full.
     * @param row the row of the cell
     * @param col the column of the cell
     */
    @Override
    protected void updateOnOpen(int row, int col) {
        if(row == 0){
            dfs(row, col);
        }
        else if(inBounds(row - 1, col) && isFull(row -1, col)){
            dfs(row, col);
        }
        else if(inBounds(row + 1, col) && isFull(row + 1, col)){
            dfs(row, col);
        }
        else if(inBounds(row, col - 1) && isFull(row, col - 1)){
            dfs(row, col);
        }
        else if(inBounds(row, col +1) && isFull(row, col + 1)){
            dfs(row, col);
        }
    }
}
