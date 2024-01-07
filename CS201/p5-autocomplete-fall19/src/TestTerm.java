import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Random;



public class TestTerm {
	private Random rng = new Random(1234);

	private String[] myNames = { "bhut jolokia", "capsaicin", "carolina reaper", "chipotle", "habanero", "jalapeno",
			"jalapeno membrane" };
	private double[] myWeights = { 855000, 16000000, 2200000, 3500, 100000, 3500, 10000 };

	public Term[] getTerms() {
		Term[] terms = new Term[myNames.length];
		for (int i = 0; i < terms.length; i++)
			terms[i] = new Term(myNames[i], myWeights[i]);
		return terms;
	}

	public int indexOf(Term[] arr, Term item) {
		for (int i = 0; i < arr.length; i++)
			if (arr[i].equals(item))
				return i;
		return -1;
	}

	/**
	 * This test checks if Term throws a NullPointerException when constructed
	 * with a null argument
	 */
	@Test
	public void testConstructorException() {
		try {
			Term test = new Term(null, 1);
			fail("No exception thrown for null String");
		} catch (NullPointerException e) {
		} catch (Throwable e) {
			fail("Wrong exception thrown "+e);
		}

		try {
			Term test = new Term("test", -1);
			fail("No exception thrown for invalid weight");
		} catch (IllegalArgumentException e) {
		} catch (Throwable e) {
			fail("Wrong exception thrown "+e);
		}
	}

	/**
	 * Tests that sorting terms without comparator is the same as sorting
	 * lexicographically
	 */
	@Test
	public void testNativeSortingOrder() {
		Term[] terms = getTerms();
		Term[] sorted = terms.clone();
		for (int i = 0; i < 10; i++) {
			Collections.shuffle(Arrays.asList(terms));
			Arrays.sort(terms);
			assertArrayEquals(sorted, terms);
		}
	}

	/**
	 * Tests WeightOrder sorts correctly
	 */

	@Test
	public void testWeightSortingOrder() {
		Term[] terms = getTerms();
		Term[] sorted = { terms[3], terms[5], terms[6], terms[4], terms[0], terms[2], terms[1] };
		for (int i = 0; i < 10; i++) {
			// preserve chipotle and jalapeno's order
			Collections.shuffle(Arrays.asList(terms));
			if (indexOf(terms, sorted[0]) > indexOf(terms, sorted[1])) {
				int temp = indexOf(terms, sorted[0]);
				terms[indexOf(terms, sorted[1])] = sorted[0];
				terms[temp] = sorted[1];
			}
			Arrays.sort(terms,
					Comparator.comparing(Term::getWeight));
			assertArrayEquals(sorted, terms);
		}
	}

	/**
	 * Tests ReverseWeightSortingOrder
	 */
	@Test
	public void testReverseWeightSortingOrder() {
		Term[] terms = getTerms();
		Term[] sorted = { terms[1], terms[2], terms[0], terms[4], terms[6], terms[3], terms[5] };
		for (int i = 0; i < 10; i++) {
			// preserve chipotle and jalapeno's order
			Collections.shuffle(Arrays.asList(terms));
			if (indexOf(terms, sorted[5]) > indexOf(terms, sorted[6])) {
				int temp = indexOf(terms, sorted[5]);
				terms[indexOf(terms, sorted[6])] = sorted[5];
				terms[temp] = sorted[6];
			}
			Arrays.sort(terms,
					Comparator.comparing(Term::getWeight).reversed());
			assertArrayEquals(sorted, terms);
		}
	}

	@Test
	/**
	 * Tests PrefixOrder
	 */
	public void testPrefixOrder() {
		// Tests basic cases
		Term[] terms1 = getTerms();
		Term[] sorted1 = { terms1[0], terms1[3], terms1[2], terms1[1], terms1[4], terms1[6], terms1[5] };
		for (int i = 0; i < terms1.length / 2; i++) {
			Term temp = terms1[i];
			terms1[i] = terms1[terms1.length - 1 - i];
			terms1[terms1.length - 1 - i] = temp;
		}
		Arrays.sort(terms1, new Term.PrefixOrder(1));
		assertArrayEquals(sorted1, terms1);

		Term[] terms2 = getTerms();
		Term[] sorted2 = { terms2[0], terms2[2], terms2[1], terms2[3], terms2[4], terms2[6], terms2[5] };
		for (int i = 0; i < terms2.length / 2; i++) {
			Term temp = terms2[i];
			terms2[i] = terms2[terms2.length - 1 - i];
			terms2[terms2.length - 1 - i] = temp;
		}
		Arrays.sort(terms2, new Term.PrefixOrder(2));
		assertArrayEquals(sorted2, terms2);

		Term[] terms3 = getTerms();
		Term[] sorted3 = { terms3[0], terms3[1], terms3[2], terms3[3], terms3[4], terms3[6], terms3[5] };
		for (int i = 0; i < terms3.length / 2; i++) {
			Term temp = terms3[i];
			terms3[i] = terms3[terms3.length - 1 - i];
			terms3[terms3.length - 1 - i] = temp;
		}
		Arrays.sort(terms3, new Term.PrefixOrder(3));
		assertArrayEquals(sorted3, terms3);

		// Test prefix case
		Term[] terms4 = getTerms();
		Term[] sorted4 = { terms4[0], terms4[1], terms4[2], terms4[3], terms4[4], terms4[5], terms4[6] };
		Collections.shuffle(Arrays.asList(terms4));
		Arrays.sort(terms4, new Term.PrefixOrder(10));
		assertArrayEquals(sorted4, terms4);

		// Test zero case
		Term[] terms5 = getTerms();
		Collections.shuffle(Arrays.asList(terms5));
		Term[] sorted5 = terms5.clone();
		Arrays.sort(terms5, new Term.PrefixOrder(0));
		assertArrayEquals(sorted5, terms5);
	}

	/**
	 * This test checks that toString returns the expected value
	 */
	@Test
	public void testToString() {
		Term[] terms = getTerms();
		for (Term t : terms) {
			assertTrue(t.toString().contains(String.format("%.1f", t.getWeight())),"weight missing");
			assertTrue(t.toString().contains(t.getWord()),"word missing");
			assertTrue(t.toString().contains(","),"no comma");
		}
	}
}
