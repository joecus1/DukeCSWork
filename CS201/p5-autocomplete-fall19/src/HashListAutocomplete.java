import java.util.*;


public class HashListAutocomplete implements Autocompletor {

    private static final int MAX_PREFIX = 10;
    private HashMap<String, List<Term>> myMap;
    private int mySize;


    /**
     * constructor which causes initialize in order to initialize variables
     * @param terms array of strings
     * @param weights array of doubles, will be the weight of each term
     */
    public HashListAutocomplete(String[] terms, double[] weights) {
        if (terms == null || weights == null) {
            throw new NullPointerException("One or more arguments null");
        }
        if (terms.length != weights.length) {
            throw new IllegalArgumentException("There are not the same amount of terms and weights");
        }

        initialize(terms,weights);

    }


    @Override
    public List<Term> topMatches(String prefix, int k) {
        if(prefix.length() > MAX_PREFIX){prefix = prefix.substring(0, MAX_PREFIX); }
        if (k < 1 || myMap.get(prefix) == null) {
            return new ArrayList<>();
        }
        List<Term> all = myMap.get(prefix);
        List<Term> list = all.subList(0, Math.min(k, all.size()));
        return list;
    }

    /**
     * called in constructor in order to initialize variables
     * creates a hashmap with prefixes as keys and lists of terms as values
     * @param terms is array of Strings for words in each Term
     * @param weights is corresponding weight for word in terms
     */
    @Override
    public void initialize(String[] terms, double[] weights) {
        myMap = new HashMap();
        for(int i = 0; i < terms.length; i++){
            String term = terms[i];
            double weight = weights[i];

            int k = 0;
            while(k <= term.length() && k <= MAX_PREFIX){
                String pre = term.substring(0, k);
                Term t = new Term(term, weight);
                myMap.putIfAbsent(pre, new ArrayList<Term>());
                myMap.get(pre).add(t);
                k++;
            }
        }

        for(String p : myMap.keySet()){
            List<Term> l = myMap.get(p);
            Collections.sort(l, Comparator.comparing(Term::getWeight).reversed());
            myMap.put(p, l);
        }



    }

    /**
     * mesasures the size of the HashMap in bytes
     * @return int mySize
     */
    @Override
    public int sizeInBytes() {
        if (mySize == 0){
            for(String k : myMap.keySet()){
                mySize += BYTES_PER_CHAR*k.length();
                for (Term t : myMap.get(k))
                {
                    mySize += BYTES_PER_CHAR*t.getWord().length() +
                            BYTES_PER_DOUBLE;
                }
            }
        }
        return mySize;
    }
}
