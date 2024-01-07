import java.util.*;

/**
 * Facilitates using fast binary search with
 * a Comparator. The methods firstIndex and lastIndex
 * run in time ceiling(1 + log(n)) where n is size of list.
 * @author ola
 *
 */
public class BinarySearchLibrary {

	/**
	 * Return smallest index of target in list using comp
	 * @param list is list of Items being searched
	 * @param target is Item searched for
	 * @param comp how Items are compared for binary search
	 * @return smallest index k such that list.get(k).equals(target)
	 */
	public static <T>
	    int firstIndexSlow(List<T> list,
	    		           T target, Comparator<T> comp) {
		int index = Collections.binarySearch(list, target,comp);

		if (index < 0) return index;

		while (0 <= index && comp.compare(list.get(index),target) == 0) {
			index -= 1;
		}
		return index+1;
	}

	/**
	 * Return smallest index of target in list using comp. 
	 * Guaranteed to make ceiling(1 + log(list.size())) comparisons
	 * @param list is list of Items being searched
	 * @param target is Item searched for
	 * @param comp how Items are compared for binary search
	 * @return smallest index k such that list.get(k).equals(target),
	 * Return -1 if there is no such object in list.               
	 */
	public static <T>
    	int firstIndex(List<T> list,
	               	   T target, Comparator<T> comp) {

		int low = -1;
		int high = list.size()-1;

		// (low,high] contains target
		// TODO: write method
		if(list.size() == 0){
			return -1;
		}
		while(low + 1 != high) {
			int mid = (low + high) / 2;
			T midValue = list.get(mid);
			int compared = comp.compare(midValue, target);
			if (compared >= 0) {
				high = mid;
			} else {
				low = mid;
			}

		}
		if (comp.compare(list.get(high), target) == 0) {
			return high;
		} else {
			return -1;
		}
	}

	 /**
     * Return the index of the last object in parameter
     * list -- the first object o such that
     * comp.compare(o,target) == 0.
     *
     * This method should not call comparator.compare() more
     * than 1+log n times, where n is list.size()
     * @param list is the list of objects being searched
     * @param target is the object being searched for
     * @param comp is how comparisons are made
     * @return index i such that comp.compare(list.get(i),target) == 0
     * and there is no index > i such that this is true. Return -1
     * if there is no such object in list.
     */
	public static <T>
	int lastIndex(List<T> list,
               	  T target, Comparator<T> comp) {

		int low = 0;
		int high = list.size();

		// target in [low,high)
		// TODO: write  method
		if(list.size() == 0){
			return -1;
		}
		while(low + 1 != high) {
			int mid = (low + high) / 2;
			T midValue = list.get(mid);
			int compared = comp.compare(midValue, target);
			if(compared > 0){
				high = mid;
			}
			else{
				low = mid;
			}
		}
		if (comp.compare(list.get(low), target) == 0) {
			return low;
		} else {
			return -1;
		}
	}

}
