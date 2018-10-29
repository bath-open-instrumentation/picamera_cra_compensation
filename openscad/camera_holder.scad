/*

This is a little holder for the Pi Camera, to allow us to vary its angle in the testing jig

(c) Richard Bowman 2018, released under CERN Open Hardware License.  Enjoy!

*/

use <./cameras/picamera_2.scad>;
use <./utilities.scad>;

function cylinder_d() = 30;
function cylinder_h() = 30;

cyl_d = cylinder_d();
cyl_h = cylinder_h();
wall_t = 4;
tube_l = 150;
d=0.05;

module ground_plane(){
    // cut off everything below the height of the PCB.
    // NB this may not be z=0, as the sensor needs to be at z=0
    // For the pi camera, this should be z= -2mm
    translate([0,0,-picamera_2_camera_sensor_height()]) mirror([0,0,1]) cylinder(r=999,h=999,$fn=4);
}

module camera_holder(expand=0, holes=true){
    // A cylindrical mount for the pi camera, allowing it to be tilted.
    difference(){
        union(){
            // Most of the part is contained within a cylindrical block to allow rotation
            hull(){
                rotate([0,90,0]) cylinder(d=cyl_d+expand, h=cyl_h-expand, center=true);
                rotate([0,90,0]) cylinder(d=cyl_d-4-expand, h=cyl_h+4+expand, center=true);
            }
            // This shaft is what holds the camera module in
            rotate([0,90,0]) cylinder(d=8+expand, h=cyl_h + 4 + 2*10, center=true);
            // Make the shaft thicker at the ends, to keep elastic bands on
            reflect([1,0,0]) translate([cyl_h/2 + 2 + 10 - 3, 0,0]) rotate([0,90,0]) 
                        cylinder(d=12, h=3);
            // Add a pointer on one side to show the angle
            translate([cyl_h/2 + 2 + 10 - 3, 0,0]) hull(){
                translate([0,-4,0]) cube([3,8,12]);
                translate([0,-d,0]) cube([3,2*d,24]);
            }
        }
        
        // The ground plane should be below zero so the pi sensor is at z=0
        ground_plane();
        
        if(holes){
            // Cut-out for the camera
            translate([0,0,-picamera_2_camera_sensor_height()]) picam2_cutout();
            
            // Extended cut-out for the beam
            hull() reflect([0,1,0]) rotate([40,0,0]) cylinder(d=8, h=999);
        }
    }
}

module illumination_tube(){
    // A tube to "collimate" light from an LED and shine it on the camera
    difference(){
        sequential_hull(){
            rotate([0,90,0]) cylinder(d=cyl_d+4, h=cyl_h+4+4*2, center=true);
            translate([0,0,cyl_d/2+2]) cylinder(d=30,h=1);
            translate([0,0,tube_l - 20]) cylinder(d=30,h=1);
            translate([0,0,tube_l - 1]) cylinder(d=50,h=1);
        }
        
        // make the bottom (or top) flat
        ground_plane();
        
        // void for the camera holder
        camera_holder(expand=2, holes=false);
        
        // mounting screws on top
        reflect([1,0,0]) reflect([0,1,0]){
            translate([15,15,tube_l - 10]) cylinder(d=2.9,h=20);
            translate([8,8,tube_l - 10]) cylinder(d=2.9,h=20); 
        }
        
        // mounting screws for elastic bands
        reflect([1,0,0]) reflect([0,1,0]){
            yz_pos = (cyl_d/2 - 2) / sqrt(2);
            translate([cyl_h/2+3, yz_pos, yz_pos]) rotate([0,90,0]) cylinder(d=2.9,h=999);
        }
        
        // beam clearance
        lighttrap_cylinder(r1=5, r2=5, h=tube_l); //beam path
    }
}

mirror([0,0,1]) illumination_tube();
            
                