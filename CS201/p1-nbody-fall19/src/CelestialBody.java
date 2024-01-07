

/**
 * Celestial Body class for NBody
 * @author ola
 *
 */
public class CelestialBody {

	private double myXPos;
	private double myYPos;
	private double myXVel;
	private double myYVel;
	private double myMass;
	private String myFileName;

	/**
	 * Create a Body from parameters	
	 * @param xp initial x position
	 * @param yp initial y position
	 * @param xv initial x velocity
	 * @param yv initial y velocity
	 * @param mass of object
	 * @param filename of image for object animation
	 */
	public CelestialBody(double xp, double yp, double xv,
			             double yv, double mass, String filename){
		// TODO: complete constructor
		myXPos = xp;
		myYPos = yp;
		myXVel = xv;
		myYVel = yv;
		myMass = mass;
		myFileName = filename;

	}

	/**
	 * Copy constructor: copy instance variables from one
	 * body to this body
	 * @param b used to initialize this body
	 */
	public CelestialBody(CelestialBody b){
		// TODO: complete constructor
		myXPos = b.myXPos;
		myYPos = b.myYPos;
		myYVel = b.myYVel;
		myXVel = b.myXVel;
		myMass = b.myMass;
		myFileName = b.myFileName;
	}

	public double getX() {
		// TODO: complete method
		return myXPos;
	}
	public double getY() {
		// TODO: complete method
		return myYPos;
	}
	public double getXVel() {
		// TODO: complete method
		return myXVel;
	}
	/**
	 * Return y-velocity of this Body.
	 * @return value of y-velocity.
	 */
	public double getYVel() {
		// TODO: complete method
		return myYVel;
	}
	
	public double getMass() {
		// TODO: complete method
		return myMass;
	}
	public String getName() {
		// TODO: complete method
		return myFileName;
	}

	/**
	 * Return the distance between this body and another
	 * @param b the other body to which distance is calculated
	 * @return distance between this body and b
	 */
	public double calcDistance(CelestialBody b) {
		// TODO: complete method
		double dx = b.myXPos - myXPos;
		double dy = b.myYPos - myYPos;
		return Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
	}

	public double calcForceExertedBy(CelestialBody b) {
		// TODO: complete method
		double G = 6.67*1e-11;
		double m1 = myMass;
		double m2 = b.myMass;
		double r = calcDistance(b);
		return G * ((m1*m2)/(Math.pow(r, 2)));
	}

	public double calcForceExertedByX(CelestialBody b) {
		// TODO: complete method
		double dx = b.myXPos - myXPos;
		double r = calcDistance(b);
		double F = calcForceExertedBy(b);
		return (F*dx)/r;
	}
	public double calcForceExertedByY(CelestialBody b) {
		// TODO: complete method
		double dy = b.myYPos - myYPos;
		double r = calcDistance(b);
		double F = calcForceExertedBy(b);
		return (F*dy)/r;
	}

	public double calcNetForceExertedByX(CelestialBody[] bodies) {
		// TODO: complete method
		double ret = 0;
		for(CelestialBody b : bodies){
			if(! b.equals(this)){
				ret += calcForceExertedByX(b);
			}
		}
		return ret;
	}

	public double calcNetForceExertedByY(CelestialBody[] bodies) {
		// TODO: complete method
		double ret = 0;
		for(CelestialBody b : bodies){
			if(! b.equals(this)){
				ret += calcForceExertedByY(b);
			}
		}
		return ret;
	}

	public void update(double deltaT, 
			           double xforce, double yforce) {
		// TODO: complete method
		double ax = xforce/myMass;
		double ay = yforce/myMass;
		double nvx = myXVel + deltaT*ax;
		double nvy = myYVel + deltaT*ay;
		double nx = myXPos + deltaT*nvx;
		double ny = myYPos + deltaT*nvy;
		myXPos = nx;
		myYPos = ny;
		myXVel = nvx;
		myYVel = nvy;
	}

	public void draw() {
		// TODO: complete method
		StdDraw.picture(myXPos,myYPos,"images/"+myFileName);

	}
}
