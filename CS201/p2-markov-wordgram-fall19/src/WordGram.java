
/**
 * A WordGram represents a sequence of strings
 * just as a String represents a sequence of characters
 * 
 * @author Joe Cusano
 *
 */
import java.util.Arrays;
public class WordGram {
	
	private String[] myWords;   
	private String myToString;  // cached string
	private int myHash;         // cached hash value

	/**
	 * Create WordGram by creating instance variable myWords and copying
	 * size strings from source starting at index start
	 * @param source is array of strings from which copying occurs
	 * @param start starting index in source for strings to be copied
	 * @param size the number of strings copied
	 */
	public WordGram(String[] source, int start, int size) {
		myWords = new String[size];
		myToString = null;
		myHash = 0;
		// TODO: initialize all instance variable
		for(int i = 0; i < size; i++){
			myWords[i] = source[start + i];
		}
	}

	/**
	 * Return string at specific index in this WordGram
	 * @param index in range [0..length() ) for string 
	 * @return string at index
	 */
	public String wordAt(int index) {
		if (index < 0 || index >= myWords.length) {
			throw new IndexOutOfBoundsException("bad index in wordAt "+index);
		}
		return myWords[index];
	}

	/**
	 * This function returns the length of the myWords variable
	 * @return int of length of myWords
	 */
	public int length(){
		// TODO: change this
		return myWords.length;
	}


	/**
	 * Returns true if param passed is a WordGram object with the same strings in the
	 * same order as this object
	 * @param o is a WordGram object
	 * @return boolean
	 */
	@Override
	public boolean equals(Object o) {
		if (! (o instanceof WordGram) || o == null){
			return false;
		}
		// TODO: Complete this method
		WordGram wg = (WordGram) o;
		return Arrays.equals(this.myWords, wg.myWords);
	}

	/**
	 * Returns an int based on all the strings in instance field myWords
	 * @return int
	 */
	@Override
	public int hashCode(){
		// TODO: complete this method
		if(myHash == 0){
			this.toString();
			myHash = myToString.hashCode();
		}
		return myHash;
	}
	

	/**
	 * Creates and returns a new WordGram object with k entries
	 * (where k is the order of this WordGram)
	 * whose first k-1 entries are the same as the last k-1
	 * entries of this WordGram,
	 * and whose last entry is the parameter last
	 * @param last is last String of returned WordGram
	 * @return WordGram object
	 */
	public WordGram shiftAdd(String last) {
		WordGram wg = new WordGram(myWords,0,myWords.length);
		// TODO: Complete this method
		for(int i = 0; i < myWords.length; i++){
			if(i != 0){
				wg.myWords[i - 1] = this.myWords[i];
			}
		}
		wg.myWords[this.myWords.length - 1] = last;
		return wg;
	}

	/**
	 * toString method returns a printable string representing all the strings stored
	 * in WordGram
	 * @return String
	 */
	@Override
	public String toString(){
		// TODO: Complete this method
		myToString = String.join(" ", myWords);
		return myToString;
	}
}
