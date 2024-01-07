import java.util.*;

public class EfficientMarkov extends BaseMarkov {
	private Map<String, ArrayList<String>> myMap;

	/**
	 * Construct an EfficientMarkov object with specified order
	 *
	 * @param order
	 */
	public EfficientMarkov(int order) {
		super(order);
		myMap = new HashMap<String, ArrayList<String>>();
	}

	/**
	 * Default constructor has order 3
	 */
	public EfficientMarkov() {
		this(3);
	}

	/**
	 * setTraining puts each unique gram from text into a myMap
	 * as a key, the value of which is an ArrayList consisting
	 * of the characters that follow that gram
	 * @param text
	 */
	@Override
	public void setTraining(String text){
		myText = text;
		myMap.clear();

		for(int i = 0; i <= myText.length() - myOrder; i++) {
			String gram = myText.substring(i, i + myOrder);
			myMap.putIfAbsent(gram, new ArrayList<String>());
			ArrayList<String> tmp = myMap.get(gram);
			if(i == myText.length() - myOrder){
				tmp.add(PSEUDO_EOS);
			}
			else{
				tmp.add(myText.substring(i + myOrder, i + myOrder + 1));
			}
			myMap.put(gram, tmp);
		}
	}

	/**
	 * Returns an ArrayList of the characters (values of a HashMap)
	 * that follow the paramater key in the
	 * HashMap
	 * @param key
	 * @return ArrayList of strings
	 */
	@Override
	public ArrayList<String> getFollows(String key){
		if(! myMap.containsKey(key)){
			throw new NoSuchElementException(key+" not in map");
		}
		else{
			return myMap.get(key);
		}
	}


}

