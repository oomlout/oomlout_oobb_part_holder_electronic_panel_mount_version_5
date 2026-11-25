"""Section and clearance checks against the CAD files published by make_all."""
import math
from pathlib import Path
import unittest

import trimesh
import yaml


class RearPlateSections(unittest.TestCase):
    def test_mounts_and_wire_exit(self):
        root = Path(__file__).resolve().parents[1] / "parts"
        boxes = sorted(root.glob("*_box_width_only_*/working.yaml"))
        self.assertTrue(boxes)
        for path in boxes:
            dimensions = yaml.safe_load(path.read_text(encoding="utf-8"))["oobb_details"]
            for mode in ("true", "3dpr"):
                with self.subTest(part=path.parent.name, mode=mode):
                    self.check_box(path.parent, dimensions, mode)

    def check_box(self, folder, d, mode):
        body = trimesh.load_mesh(folder / f"body_{mode}.stl")
        plate = trimesh.load_mesh(folder / f"back_plate_{mode}.stl")
        box = trimesh.load_mesh(folder / f"{mode}.stl")
        for mesh in (body, plate, box):
            self.assertTrue(mesh.is_volume)
        self.assertAlmostEqual(plate.extents[2], 3)
        self.assertAlmostEqual(body.extents[2] + plate.extents[2], d["depth"])
        pieces = sorted(box.split(only_watertight=False), key=lambda item: item.extents[2])
        if mode == "3dpr":
            self.assertEqual(len(pieces), 2)
            for placed, single in zip(pieces, (plate, body)):
                self.assertAlmostEqual(placed.bounds[0, 2], 0)
                self.assertAlmostEqual(placed.volume, single.volume, places=2)
            self.assertGreater(pieces[0].bounds[0, 1], pieces[1].bounds[1, 1])
        else:
            self.assertEqual(len(pieces), 1)
            self.assertAlmostEqual(box.extents[2], d["depth"])

        # A circle of parallel rays catches stopped bores and narrowed passages.
        origins = []
        through_top = []
        for side in (-1, 1):
            x = side * d["join_x_mm"]
            for half_step in range(2*d["height"]-1):
                y = (half_step - d["height"] + 1)*7.5
                radius = 1.5 if half_step % 2 else 3.0
                for angle in range(0, 360, 45):
                    a = math.radians(angle)
                    origins.append([x+(radius-.05)*math.cos(a), y+(radius-.05)*math.sin(a), -1])
            for i in range(1, math.ceil(d["body_depth_mm"]/7.5)):
                z = i*7.5
                radius = 3.0 if i%4 == 2 else 1.5
                if i%4 and z+radius+1 <= d["body_depth_mm"]:
                    for angle in range(0, 360, 45):
                        a = math.radians(angle)
                        through_top.append([x+(radius-.05)*math.cos(a), -body.extents[1], z+(radius-.05)*math.sin(a)])
        for mesh in (body, plate):
            self.assertFalse(mesh.ray.intersects_any(origins, [[0, 0, 1]]*len(origins)).any())
        self.assertFalse(body.ray.intersects_any(through_top, [[0, 1, 0]]*len(through_top)).any())

        y = d["join_y_mm"]
        plate_depth = plate.extents[2]
        flat = (5.5 if mode == "true" else 5.75)/2
        nut_z = body.extents[2] - d["join_nut_skin_mm"] - d["embedded_nut_depth_mm"]/2
        for side in (-1, 1):
            x = side*d["join_x_mm"]
            self.assertFalse(plate.contains([[x+2.55, y, plate_depth-.1]])[0])
            self.assertTrue(plate.contains([[x+2.55, y, .3]])[0])
            self.assertLess(d["depth"]-d["join_screw_length_mm"], nut_z-d["embedded_nut_depth_mm"]/2)
            self.check_slot(body, x, y, nut_z, side*(body.extents[0]/2-1), flat)
            for row in d["future_mount_rows_mm"]:
                x_patch = side*d["future_mount_x_mm"]
                self.check_slot(plate, x_patch, row, plate_depth/2, side*(d["wire_width_mm"]/2+2), flat)
                self.assertFalse(plate.ray.intersects_any([[x_patch, row, -1]], [[0, 0, 1]])[0])
                land = side*(abs(x_patch)-4.5)
                self.assertTrue(plate.contains([[land,row,.10], [land,row,plate_depth-.10]]).all())
        top = d["wire_bottom_y_mm"] + d["wire_height_mm"]
        opening = [[0, d["wire_bottom_y_mm"]+1, plate_depth/2], [0, top-.2, plate_depth/2]]
        self.assertFalse(plate.contains(opening).any())
        self.assertTrue(plate.contains([[0, top+.2, plate_depth/2]])[0])
        self.assertTrue(plate.contains([[d["wire_width_mm"]/2-.3, top-.3, plate_depth/2]])[0])
        self.assertFalse(body.contains([[0, 0, body.extents[2]-.3]])[0])

    def check_slot(self, mesh, x, y, z, end, half_flat):
        points = [[x+(end-x)*i/12, y+j, z] for i in range(13) for j in (-half_flat+.08, 0, half_flat-.08)]
        self.assertFalse(mesh.contains(points).any())
        for side in (-1, 1):
            self.assertTrue(mesh.contains([[end, y+side*(half_flat+.08), z]])[0])


if __name__ == "__main__":
    unittest.main()
