module body() {
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
						oobb_rounded_rectangle_edges(radius = 7, radius_bottom = 1.5, radius_top = 0, size = [119, 59, 38]);
					}
					union();
				}
			}
		}
	}
	union() {
		translate(v = [-52.5, 0, 33.5]) {
			rotate(a = [0, 0, 180]) {
				difference() {
					union() {
						translate(v = [0, -2.75, 0]) {
							cube(size = [8.0, 5.5, 3]);
						}
						linear_extrude(height = 3) {
							polygon(points = [[3.1754264805429417, 0.0], [1.5877132402714713, 2.75], [-1.5877132402714702, 2.7500000000000004], [-3.1754264805429417, 3.888775875324659e-16], [-1.5877132402714722, -2.7499999999999996], [1.5877132402714687, -2.7500000000000013]]);
						}
					}
					union();
				}
			}
		}
		translate(v = [-52.5, 0, 33.5]) {
			rotate(a = [0, 0, 180]) {
				difference() {
					union();
					union();
				}
			}
		}
		translate(v = [52.5, 0, 33.5]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, -2.75, 0]) {
							cube(size = [8.0, 5.5, 3]);
						}
						linear_extrude(height = 3) {
							polygon(points = [[3.1754264805429417, 0.0], [1.5877132402714713, 2.75], [-1.5877132402714702, 2.7500000000000004], [-3.1754264805429417, 3.888775875324659e-16], [-1.5877132402714722, -2.7499999999999996], [1.5877132402714687, -2.7500000000000013]]);
						}
					}
					union();
				}
			}
		}
		translate(v = [52.5, 0, 33.5]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union();
					union();
				}
			}
		}
		translate(v = [-40.8, -20.3, 0]) {
			cube(size = [81.6, 40.6, 3]);
		}
		translate(v = [-43.5, -23.0, 3]) {
			cube(size = [87.0, 46.0, 35]);
		}
		translate(v = [-52.5, -22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [-52.5, -15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 1.5);
			}
		}
		translate(v = [-52.5, -7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [-52.5, 0.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 1.5);
			}
		}
		translate(v = [-52.5, 7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [-52.5, 15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 1.5);
			}
		}
		translate(v = [-52.5, 22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [52.5, -22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [52.5, -15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 1.5);
			}
		}
		translate(v = [52.5, -7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [52.5, 0.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 1.5);
			}
		}
		translate(v = [52.5, 7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [52.5, 15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 1.5);
			}
		}
		translate(v = [52.5, 22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 38, r = 3.0);
			}
		}
		translate(v = [-52.5, 29.5, 7.5]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 59, r = 1.5);
			}
		}
		translate(v = [52.5, 29.5, 7.5]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 59, r = 1.5);
			}
		}
		translate(v = [-52.5, 29.5, 15.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 59, r = 3.0);
			}
		}
		translate(v = [52.5, 29.5, 15.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 59, r = 3.0);
			}
		}
		translate(v = [-52.5, 29.5, 22.5]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 59, r = 1.5);
			}
		}
		translate(v = [52.5, 29.5, 22.5]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 59, r = 1.5);
			}
		}
	}
}

}
module rear_plate() {
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
						oobb_rounded_rectangle_edges(radius = 7, radius_bottom = 0, radius_top = 1.5, size = [119, 59, 3]);
					}
					union();
				}
			}
		}
	}
	union() {
		translate(v = [-52.5, 0, 3]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.5);
						}
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.8);
						}
						translate(v = [0, 0, -1.7]) {
							cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
						}
						cylinder(h = 250, r = 2.9);
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [52.5, 0, 3]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.5);
						}
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.8);
						}
						translate(v = [0, 0, -1.7]) {
							cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
						}
						cylinder(h = 250, r = 2.9);
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [-22.5, -22.5, 0.5499999999999998]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						linear_extrude(height = 152.45) {
							polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
						}
					}
					union();
				}
			}
		}
		translate(v = [-22.5, -7.5, 0.5499999999999998]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						linear_extrude(height = 152.45) {
							polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
						}
					}
					union();
				}
			}
		}
		translate(v = [22.5, -22.5, 0.5499999999999998]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						linear_extrude(height = 152.45) {
							polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
						}
					}
					union();
				}
			}
		}
		translate(v = [22.5, -7.5, 0.5499999999999998]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						linear_extrude(height = 152.45) {
							polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
						}
					}
					union();
				}
			}
		}
		translate(v = [-52.5, -22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [-52.5, -15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.5);
			}
		}
		translate(v = [-52.5, -7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [-52.5, 0.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.5);
			}
		}
		translate(v = [-52.5, 7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [-52.5, 15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.5);
			}
		}
		translate(v = [-52.5, 22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [52.5, -22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [52.5, -15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.5);
			}
		}
		translate(v = [52.5, -7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [52.5, 0.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.5);
			}
		}
		translate(v = [52.5, 7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [52.5, 15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.5);
			}
		}
		translate(v = [52.5, 22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.0);
			}
		}
		translate(v = [-52.5, 0, 1.3]) {
			cylinder(h = 1.7, r1 = 1.5, r2 = 3);
		}
		translate(v = [52.5, 0, 1.3]) {
			cylinder(h = 1.7, r1 = 1.5, r2 = 3);
		}
		translate(v = [0, -18.5, -1]) {
			hull() {
				translate(v = [-8.0, 12.0, 0]) {
					cylinder(h = 5, r = 7);
				}
				translate(v = [8.0, 12.0, 0]) {
					cylinder(h = 5, r = 7);
				}
				translate(v = [-8.0, -12.0, 0]) {
					cylinder(h = 5, r = 7);
				}
				translate(v = [8.0, -12.0, 0]) {
					cylinder(h = 5, r = 7);
				}
			}
		}
		translate(v = [-22.5, -22.5, 0]) {
			cylinder(h = 3, r = 1.5);
		}
		translate(v = [-22.5, -7.5, 0]) {
			cylinder(h = 3, r = 1.5);
		}
		translate(v = [22.5, -22.5, 0]) {
			cylinder(h = 3, r = 1.5);
		}
		translate(v = [22.5, -7.5, 0]) {
			cylinder(h = 3, r = 1.5);
		}
	}
}

}
body();
translate([0, 0, 38]) rear_plate();
