

public class LinkStrand implements IDnaStrand {

    private class Node {
        String info;
        Node next;

        public Node (String s){
            info = s;
            next = null;
        }
    }
    private Node myFirst, myLast;
    private long mySize;
    private int myAppends;
    private Node myCurrent;
    private int myIndex;
    private int myLocalIndex;

    /**
     * Create a strand representing s. No error checking is done to see if s
     * represents valid genomic/DNA data.
     *
     * @param s
     *            is the source of cgat data for this strand
     */
    public LinkStrand(String s) {
        initialize(s);
    }

    /**
     * default constructor
     */
    public LinkStrand(){
        this("");
    }


    /**
     * returns size of the dna strand measured in number of characters
     * @return long
     */
    @Override
    public long size() {
        return mySize;
    }

    /**
     * initialize strand so that it represents value of source
     * no error checking performed
     * @param source is the source of this enzyme
     */
    @Override
    public void initialize(String source) {
        myFirst = new Node(source);
        myLast = myFirst;
        myAppends = 0;
        mySize = source.length();
        myIndex = 0;
        myLocalIndex = 0;
        myCurrent = this.myFirst;
    }


    /**
     * get an instance of a link strand object
     * @param source is data from which object constructed
     * @return IDnaStrand
     */
    @Override
    public IDnaStrand getInstance(String source) {
        return new LinkStrand(source);
    }

    /**
     * Appends a new String of DNA info to the list and updates
     * instance variables
     * @param dna is the string appended to this strand
     * @return IDnaStrand
     */
    @Override
    public IDnaStrand append(String dna) {
        Node temp = new Node(dna);
        myLast.next = temp;
        mySize += dna.length();
        myAppends += 1;
        myLast = temp;
        return this;
    }

    /**
     * reverses the order of the notes and strings which make
     * up an IDnaStrand
     * @return new IDnaStrand ret which is a reversed version
     * of DNA strand reverse was called on
     */
    @Override
    public IDnaStrand reverse() {
        LinkStrand ret = new LinkStrand();
        Node head = this.myFirst;
        while (head != null){
            StringBuilder buf = new StringBuilder(head.info);
            buf = buf.reverse();
            String n = buf.toString();
            Node reversed = new Node(n);
            reversed.next = ret.myFirst;
            ret.myFirst = reversed;
            head = head.next;
            ret.mySize = ret.mySize + ret.myFirst.info.length();
        }
        return ret;
    }

    /**
     * returns the number of Appends made to
     * a list
     * @return an int
     */
    @Override
    public int getAppendCount() {
        return myAppends;
    }

    /**
     * returns the character at index point in the Linked List
     * by efficiently iterating through the linked list
     * @param index specifies which character will be returned
     * @return char
     */
    @Override
    public char charAt(int index) {
        if (index < 0 || index >= this.mySize) {
            throw new IndexOutOfBoundsException("Index " + index + " is out of bound.");
        }
        if(index < myIndex){
            myIndex = 0;
            myCurrent = myFirst;
            myLocalIndex = 0;
        }

        while (myIndex != index) {
            myIndex++;
            myLocalIndex++;
            if (myLocalIndex >= myCurrent.info.length()) {
                myLocalIndex = 0;
                myCurrent = myCurrent.next;
            }
        }
        return myCurrent.info.charAt(myLocalIndex);

    }

    /**
     * returns a string version of the IDnaStrand object
     * @return string
     */
    @Override
    public String toString(){
        StringBuilder buf = new StringBuilder();
        Node temp = myFirst;
        while(temp != null){
            buf.append(temp.info);
            temp = temp.next;
        }
        return buf.toString();
    }
}
