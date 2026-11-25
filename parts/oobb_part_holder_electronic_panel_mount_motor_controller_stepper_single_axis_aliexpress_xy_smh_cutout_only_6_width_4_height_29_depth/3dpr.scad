$fn = 64;

difference() {
	union() {
		translate(v = [-40.8, -20.3, 0]) {
			cube(size = [81.6, 40.6, 3]);
		}
		translate(v = [-43.5, -23.0, 3]) {
			cube(size = [87.0, 46.0, 26]);
		}
	}
	union();
}
