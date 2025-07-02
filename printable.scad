$fa=2;
module hollowSphere(d, wt) {
  difference() {
    sphere(r = d/2);
    sphere(r = (d - wt)/2);
  }
}
module asalato(d=55, hd=6, wt=4) {
  difference() {
    union(){
      hollowSphere(d = d, wt = wt);
        difference(){
        intersection(){
          union(){
            cylinder(h = d/2, r1=0,r2=d/2);
            translate([0,0,-d/2]) cylinder(h = d/2, r1=d/2,r2=0);
            cylinder(h = d, r = hd/2 + wt/2, center=true, $fn=20);
          }
          sphere(r = d/2);
        }
        rotate([90,0,0]) cylinder(h = d, r = hd/2, center=true, $fn=20);
      }
    }
    cylinder(h = d, r = hd/2, center=true, $fn=20);
  }

}

asalato();