import java.util.*;

public class EfficientWordMarkov extends BaseWordMarkov {
    private Map<WordGram, ArrayList<String>> myMap;

    /**
     * Construct an EfficientMarkov object with specified order
     *
     * @param order
     */
    public EfficientWordMarkov(int order) {
        super(order);
        myMap = new HashMap<WordGram, ArrayList<String>>();
    }

    /**
     * Default constructor has order 3
     */
    public EfficientWordMarkov() {
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
        myWords = text.split("\\s+");
        myMap.clear();

        for(int i = 0; i <= myWords.length - myOrder; i++) {
            WordGram gram = new WordGram(myWords, i, myOrder);
            myMap.putIfAbsent(gram, new ArrayList<String>());
            ArrayList<String> tmp = myMap.get(gram);
            if(i == myWords.length - myOrder){
                tmp.add(PSEUDO_EOS);
            }
            else{
                tmp.add(myWords[i+myOrder]);
            }
            myMap.put(gram, tmp);
        }
    }

    /**
     * Returns an ArrayList of the words (values of a HashMap)
     * that follow the paramater key in the
     * HashMap
     * @param kGram
     * @return ArrayList of strings
     */
    @Override
    public ArrayList<String> getFollows(WordGram kGram){
        if(! myMap.containsKey(kGram)){
            throw new NoSuchElementException(kGram+" not in map");
        }
        else{
            return myMap.get(kGram);
        }
    }


}
