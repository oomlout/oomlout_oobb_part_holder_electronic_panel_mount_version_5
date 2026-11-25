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
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						cylinder(h = 250, r = 3.6);
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.8);
						}
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
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						cylinder(h = 250, r = 3.6);
						translate(v = [0, 0, -12.0]) {
							cylinder(h = 12, r = 1.8);
						}
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
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 52.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 52.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						linear_extrude(height = 102.45) {
							polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 102.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 102.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 152.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 152.75]) {
							cube(size = [3.5, 3.5, 0.3]);
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
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 52.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 52.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						linear_extrude(height = 102.45) {
							polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 102.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 102.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 152.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 152.75]) {
							cube(size = [3.5, 3.5, 0.3]);
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
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 52.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 52.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						linear_extrude(height = 102.45) {
							polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 102.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 102.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 152.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 152.75]) {
							cube(size = [3.5, 3.5, 0.3]);
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
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 52.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 52.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						linear_extrude(height = 102.45) {
							polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 102.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 102.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 152.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 152.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
					}
					union();
				}
			}
		}
		translate(v = [15.0, 7.5, 0.5499999999999998]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 52.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 52.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						linear_extrude(height = 102.45) {
							polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 102.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 102.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 152.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 152.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
					}
					union();
				}
			}
		}
		translate(v = [45.0, 7.5, 0.5499999999999998]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 52.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 52.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						linear_extrude(height = 102.45) {
							polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 102.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 102.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, -0.3]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, -0.6]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
						translate(v = [-1.75, -3.25, 152.45]) {
							cube(size = [3.5, 6.5, 0.3]);
						}
						translate(v = [-1.75, -1.75, 152.75]) {
							cube(size = [3.5, 3.5, 0.3]);
						}
					}
					union();
				}
			}
		}
		translate(v = [-52.5, -22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [-52.5, -15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.8);
			}
		}
		translate(v = [-52.5, -7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [-52.5, 0.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.8);
			}
		}
		translate(v = [-52.5, 7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [-52.5, 15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.8);
			}
		}
		translate(v = [-52.5, 22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [52.5, -22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [52.5, -15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.8);
			}
		}
		translate(v = [52.5, -7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [52.5, 0.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.8);
			}
		}
		translate(v = [52.5, 7.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
		}
		translate(v = [52.5, 15.0, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 1.8);
			}
		}
		translate(v = [52.5, 22.5, 0]) {
			rotate(a = [0, 0, 2.8125]) {
				cylinder(h = 3, r = 3.25);
			}
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
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [-22.5, -7.5, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [22.5, -22.5, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [22.5, -7.5, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [30.0, 15.0, -1]) {
			hull() {
				translate(v = [-6.375, 6.375, 0]) {
					cylinder(h = 5, r = 3.75);
				}
				translate(v = [6.375, 6.375, 0]) {
					cylinder(h = 5, r = 3.75);
				}
				translate(v = [-6.375, -6.375, 0]) {
					cylinder(h = 5, r = 3.75);
				}
				translate(v = [6.375, -6.375, 0]) {
					cylinder(h = 5, r = 3.75);
				}
			}
		}
		translate(v = [15.0, 7.5, 0]) {
			cylinder(h = 3, r = 1.8);
		}
		translate(v = [45.0, 7.5, 0]) {
			cylinder(h = 3, r = 1.8);
		}
	}
}
