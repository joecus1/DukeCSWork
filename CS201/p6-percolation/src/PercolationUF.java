import java.util.Arrays;

public class PercolationUF implements IPercolate {
    private IUnionFind myFinder;
    private boolean[][] myGrid;
    private final int VTOP;
    private final int VBOTTOM;
    private int myOpenCount;

    /**
     * Creates a grid with all cells closed at the start
     * @param finder is the finder used to make a set of all connected, open cells
     * @param size is the size of the grid
     */
    public PercolationUF(IUnionFind finder, int size){
        myGrid = new boolean[size][size];
        for (boolean[] row : myGrid)
            Arrays.fill(row, false);
        myOpenCount = 0;
        VTOP = size * size;
        VBOTTOM = size * size + 1;
        finder.initialize(size*size + 2);
        myFinder = finder;
    }

    /**
     * Opens a cell if it is not already open and is in bounds
     * @param row the row of the cell
     * @param col the column of the cell
     */
    @Override
    public void open(int row, int col) {
        if (! inBounds(row,col)) {
            throw new IndexOutOfBoundsException(
                    String.format("(%d,%d) not in bounds", row,col));
        }

        if(!isOpen(row, col)){
            myGrid[row][col] = true;
            myOpenCount += 1;
            if(row == 0){
                myFinder.union(row * myGrid.length + col, VTOP);
            }
            if(row == myGrid.length - 1 ){
                myFinder.union(row * myGrid.length + col, VBOTTOM);
            }
            if(inBounds(row, col + 1) && isOpen(row, col + 1)){
                myFinder.union(row * myGrid.length + col, row * myGrid.length + col + 1);
            }
            if(inBounds(row, col - 1) && isOpen(row, col -1)){
                myFinder.union(row * myGrid.length + col, row * myGrid.length + col - 1);
            }
            if(inBounds(row + 1, col) && isOpen(row + 1, col)){
                myFinder.union(row * myGrid.length + col, (row + 1) * myGrid.length + col);
            }
            if(inBounds(row - 1, col) && isOpen(row - 1, col)){
                myFinder.union(row * myGrid.length + col, (row - 1) * myGrid.length + col);
            }
        }
    }

    /**
     * Returns true if a cell is open and false if it is not
     * @param row the row of the cell
     * @param col the column of the cell
     * @return boolean
     */
    @Override
    public boolean isOpen(int row, int col) {
        if (! inBounds(row,col)) {
            throw new IndexOutOfBoundsException(
                    String.format("(%d,%d) not in bounds", row,col));
        }
        return myGrid[row][col] == true;
    }

    /**
     * Returns true if a cell is full and false if it is not
     * @param row the row of the cell
     * @param col the column of the cell
     * @return boolean
     */
    @Override
    public boolean isFull(int row, int col) {
        if (! inBounds(row,col)) {
            throw new IndexOutOfBoundsException(
                    String.format("(%d,%d) not in bounds", row,col));
        }

        return myFinder.connected(row * myGrid.length + col, VTOP);
    }

    /**
     * Returns true if the system percolates and false if not
     * @return boolean
     */
    @Override
    public boolean percolates() {
        return myFinder.connected(VTOP, VBOTTOM);
    }

    /**
     * Returns the number of opened sites
     * @return int
     */
    @Override
    public int numberOfOpenSites() {
        return myOpenCount;
    }

    /**
     * Determine if (row,col) is valid for given grid
     * @param row specifies row
     * @param col specifies column
     * @return true if (row,col) on grid, false otherwise
     */
    protected boolean inBounds(int row, int col) {
        if (row < 0 || row >= myGrid.length) return false;
        if (col < 0 || col >= myGrid[0].length) return false;
        return true;
    }
}
