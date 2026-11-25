$fn = 64;

module oobb_rounded_rectangle_edges(size, radius, radius_top, radius_bottom) {
      rt=radius_top; rb=radius_bottom; depth=size[2]; n=16;
      lower=rb==0 ? [[radius,0]] :
        [for(i=[0:n]) let(a=-90+90*i/n) [radius-rb+rb*cos(a),rb+rb*sin(a)]];
      upper=rt==0 ? [[radius,depth]] :
        [for(i=[0:n]) let(a=90*i/n) [radius-rt+rt*cos(a),depth-rt+rt*sin(a)]];
      hull() for(x=[-size[0]/2+radius,size[0]/2-radius])
        for(y=[-size[1]/2+radius,size[1]/2-radius])
          translate([x,y,0]) rotate_extrude()
            polygon(concat([[0,0]],lower,upper,[[0,depth]]));
    }
difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						oobb_rounded_rectangle_edges(radius = 7, radius_bottom = 1.5, radius_top = 1.5, size = [119, 59, 3]);
					}
					union();
				}
			}
		}
	}
	union() {
		translate(v = [-40.8, -20.3, 0]) {
			cube(size = [81.6, 40.6, 3]);
		}
		translate(v = [-43.5, -23.0, 3]) {
			cube(size = [87.0, 46.0, 26]);
		}
		translate(v = [-52.5, -22.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [-52.5, -15.0, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [-52.5, -7.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [-52.5, 0.0, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [-52.5, 7.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [-52.5, 15.0, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [-52.5, 22.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [52.5, -22.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [52.5, -15.0, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [52.5, -7.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [52.5, 0.0, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [52.5, 7.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
		translate(v = [52.5, 15.0, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [52.5, 22.5, 0]) {
			cylinder(h = 3, r = 3.25);
		}
	}
}
