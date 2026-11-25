"""X and Y span the front face. Positive Z runs from the bezel toward the back."""
import math
from pathlib import Path
import re
import shutil
import subprocess
import time
from tempfile import TemporaryDirectory

import oobb
import opsc
import yaml
from components.oobb_nut.working import describe as nut_description
from working_oomp_populate import REAR_PLATES


def draw_cutout(thing, **kwargs):
    polarity = kwargs.get("polarity", "negative")
    lip = kwargs["depth_cutout_mm"]
    depth = kwargs.get("relief_depth_mm", kwargs["cavity_depth_mm"])
    opening = [kwargs["width_cutout_mm"], kwargs["height_cutout_mm"], lip]
    relief = [kwargs["cavity_width_mm"], kwargs["cavity_height_mm"], depth - lip]
    oobb.append_full(thing, type=polarity, shape="oobb_cube_center", size=opening, pos=[0, 0, 0])
    oobb.append_full(thing, type=polarity, shape="oobb_cube_center", size=relief, pos=[0, 0, lip])


def draw_front_holes(thing, **kwargs):
    width = kwargs["width"]
    height = kwargs["height"]
    depth = kwargs.get("front_hole_depth_mm", kwargs["depth"])
    all_edges = kwargs.get("all_edges", False)
    rotation = kwargs.get("front_bore_rotation", 0)
    half_pitch = oobb.gv("osp") / 2
    last_x = 2 * (width - 1)
    last_y = 2 * (height - 1)
    for ix in range(last_x + 1):
        for iy in range(last_y + 1):
            if ix not in (0, last_x) and not (all_edges and iy in (0, last_y)):
                continue
            x = (ix - last_x / 2) * half_pitch
            y = (iy - last_y / 2) * half_pitch
            name = "m3" if ix % 2 or iy % 2 else "m6"
            oobb.append_full(thing, type="negative", shape="oobb_hole", radius_name=name,
                             depth=depth, pos=[x, y, 0], rot=[0, 0, rotation])


def draw_top_holes(thing, **kwargs):
    width = kwargs["width"]
    height = kwargs["height"]
    depth = kwargs["depth"]
    cavity_width = kwargs["cavity_width_mm"]
    skin = kwargs.get("hole_wall_mm", 1)
    pitch = oobb.gv("osp")
    half_pitch = pitch / 2
    height_mm = height * pitch - oobb.gv("osp_minus")
    radii = {name: max(oobb.gv(f"hole_radius_{name}", mode) for mode in ("true", "3dpr"))
             for name in ("m3", "m6")}
    for row in range(1, math.ceil(depth / half_pitch)):
        if row % 4 == 0:
            continue
        z = row * half_pitch
        for column in range(2 * width - 1):
            x = (column - width + 1) * half_pitch
            name = "m6" if row % 4 == 2 and column % 2 == 0 else "m3"
            if min(z, depth-z, abs(x)-cavity_width/2) < radii[name] + skin:
                continue
            oobb.append_full(thing, type="negative", shape="oobb_hole", radius_name=name,
                             pos=[x, height_mm/2, z], rot=[90, 0, 0], depth=height_mm)


def draw_plate(thing, **kwargs):
    radius = kwargs.get("corner_radius_mm", 7)
    rim = kwargs.get("edge_radius_mm", 1.5)
    rim_top = kwargs.get("edge_radius_top_mm", rim)
    rim_bottom = kwargs.get("edge_radius_bottom_mm", rim)
    pitch, allowance = oobb.gv("osp"), oobb.gv("osp_minus")
    size = [kwargs["width"]*pitch-allowance, kwargs["height"]*pitch-allowance, kwargs["depth"]]
    oobb.append_full(thing, type="positive", shape="oobb_rounded_rectangle_rounded", size=size,
                     radius=radius, radius_rounded=rim, radius_top=rim_top, radius_bottom=rim_bottom, pos=[0, 0, 0])


def draw_holder(thing, **kwargs):
    draw_plate(thing, **kwargs)
    draw_cutout(thing, **kwargs)
    draw_front_holes(thing, **kwargs)


def get_panel_width_only(thing, **kwargs):
    draw_holder(thing, **kwargs)


def get_panel(thing, **kwargs):
    kwargs.setdefault("all_edges", True)
    draw_holder(thing, **kwargs)


def draw_side_nut(thing, **kwargs):
    x, y, z = kwargs["x"], kwargs["y"], kwargs["z"]
    depth = kwargs["embedded_nut_depth_mm"]
    edge = (kwargs["width"]*oobb.gv("osp") - oobb.gv("osp_minus"))/2
    mouth_x = math.copysign(edge + 1, x)
    length = abs(mouth_x - x)
    native_slot = any(field["name"] == "clearance_side_length" for field in nut_description()["variables"])
    for mode in ("true", "3dpr"):
        flats = 5.5 if mode == "true" else 5.75
        adjustment = flats / math.sqrt(3) - oobb.gv("nut_radius_m3", mode)
        oobb.append_full(thing, type="negative", shape="oobb_nut", radius_name="m3", mode=mode,
                         clearance="side", clearance_side_length=length, clearance_tightness=adjustment,
                         depth=depth, overhang=True, pos=[x, y, z], rot=[0, 0, 180 if mouth_x < x else 0])
        if not native_slot:
            # Older v5 libraries supply the hex and overhangs. Extend the same flats to the edge.
            oobb.append_full(thing, type="negative", shape="oobb_cube_center", inclusion=mode,
                             size=[length, flats, depth], pos=[(x + mouth_x)/2, y, z])


def get_box_width_only(thing, **kwargs):
    body = kwargs["body_depth_mm"]
    skin = kwargs["join_nut_skin_mm"]
    nut_depth = kwargs["embedded_nut_depth_mm"]
    reach = kwargs["join_screw_length_mm"] - kwargs["back_plate_depth_mm"]
    if reach < nut_depth + skin:
        raise ValueError("Rear screw does not span the captive nut")
    # Stagger facets at the perpendicular bore intersections for STL export.
    kwargs.setdefault("front_bore_rotation", 180 / kwargs.get("resolution", 64))
    kwargs.update(depth=body, relief_depth_mm=body, front_hole_depth_mm=body, edge_radius_top_mm=0)
    draw_holder(thing, **kwargs)
    draw_top_holes(thing, **kwargs)
    for x in (-kwargs["join_x_mm"], kwargs["join_x_mm"]):
        draw_side_nut(thing, x=x, y=kwargs["join_y_mm"], z=body-skin-nut_depth, **kwargs)


def draw_rear_nut(thing, **kwargs):
    x, y = kwargs["x"], kwargs["y"]
    depth = kwargs["back_plate_depth_mm"]
    nut_depth = kwargs["patch_nut_depth_mm"]
    oobb.append_full(thing, type="negative", shape="oobb_nut", radius_name="m3",
                     clearance="top", overhang=True, depth=nut_depth, pos=[x, y, depth-nut_depth])
    oobb.append_full(thing, type="negative", shape="oobb_hole", radius_name="m3",
                     depth=depth, pos=[x, y, 0])


def draw_bottom_opening(thing, **kwargs):
    depth = kwargs["back_plate_depth_mm"]
    slot_width = kwargs["wire_width_mm"]
    slot_radius = kwargs.get("wire_corner_radius_mm", 7)
    slot_top = kwargs["wire_bottom_y_mm"] + kwargs["wire_height_mm"]
    bottom = kwargs["wire_bottom_y_mm"] - slot_radius - 1
    oobb.append_full(thing, type="negative", shape="rounded_rectangle", r=slot_radius,
                     size=[slot_width, slot_top-bottom, depth+2], pos=[0, (slot_top+bottom)/2, -1])
    for x in (-kwargs["future_mount_x_mm"], kwargs["future_mount_x_mm"]):
        for y in kwargs["future_mount_rows_mm"]:
            draw_rear_nut(thing, x=x, y=y, **kwargs)


def draw_electronics_opening(thing, **kwargs):
    depth = kwargs["back_plate_depth_mm"]
    center_x, center_y = kwargs["electronics_center_mm"]
    window = kwargs["electronics_window_mm"]
    radius = kwargs["electronics_corner_radius_mm"]
    dx = kwargs["electronics_nut_x_offset_mm"]
    dy = kwargs["electronics_nut_y_offset_mm"]
    oobb.append_full(thing, type="negative", shape="rounded_rectangle", r=radius,
                     size=[window, window, depth+2], pos=[center_x, center_y, -1])
    for x in (center_x-dx, center_x+dx):
        draw_rear_nut(thing, x=x, y=center_y+dy, **kwargs)


def get_back_plate(thing, **kwargs):
    depth = kwargs["back_plate_depth_mm"]
    plate = kwargs.pop("rear_plate")
    kwargs.update(depth=depth, edge_radius_bottom_mm=0)
    draw_plate(thing, **kwargs)
    kwargs.setdefault("front_bore_rotation", 180 / kwargs.get("resolution", 64))
    draw_front_holes(thing, **kwargs)
    y = kwargs["join_y_mm"]
    for x in (-kwargs["join_x_mm"], kwargs["join_x_mm"]):
        oobb.append_full(thing, type="negative", shape="oobb_screw_countersunk", radius_name="m3",
                         depth=kwargs["join_screw_length_mm"], clearance="top", overhang=True, pos=[x,y,depth])
        head_height = oobb.gv("screw_countersunk_depth_m3", "true")
        oobb.append_full(thing, type="negative", shape="cylinder", inclusion="true",
                         r1=1.5, r2=3, h=head_height, pos=[x, y, depth-head_height])
    if plate["bottom"]:
        draw_bottom_opening(thing, **kwargs)
    if plate["electronics"]:
        draw_electronics_opening(thing, **kwargs)


def get_cutout_only(thing, **kwargs):
    kwargs["polarity"] = "positive"
    draw_cutout(thing, **kwargs)


def main(**kwargs):
    root = Path(kwargs.get("parts_dir", "parts"))
    part_ids = kwargs.get("part_ids")
    modes = kwargs.get("modes", ("true", "3dpr"))
    resolution = kwargs.get("resolution", 64)
    layout_gap = kwargs.get("print_gap_mm", 8)
    generate_stl = kwargs.get("generate_stl", True)
    openscad = kwargs.get("openscad") or shutil.which("openscad.com") or shutil.which("openscad")
    if generate_stl and not openscad:
        raise FileNotFoundError("Add the OpenSCAD CLI to PATH or pass openscad= to main()")
    if part_ids is None:
        part_ids = sorted(path.parent.name for path in root.glob("*/working.yaml"))
    builders = dict(panel_width_only=get_panel_width_only, panel=get_panel,
                    box_width_only=get_box_width_only, cutout_only=get_cutout_only)
    for part_id in part_ids:
        folder = root / part_id
        part = yaml.safe_load((folder / "working.yaml").read_text(encoding="utf-8"))
        details = part["oobb_details"]
        box = details["variant"] == "box_width_only"
        pieces = {"body_" if box else "": (builders[details["oobb_type"]], {})}
        if box:
            for prefix, plate in REAR_PLATES.items():
                pieces[prefix] = (get_back_plate, dict(rear_plate=plate))
        with TemporaryDirectory(dir=folder) as temporary:
            outputs = []
            staging = Path(temporary) / "cad"
            staging.mkdir()
            for prefix, (draw, options) in pieces.items():
                thing = oobb.get_default_thing(type=details["oobb_type"])
                draw(thing, resolution=resolution, **details, **options)
                for mode in modes:
                    scad = staging / f"{prefix}{mode}.scad"
                    opsc.opsc_make_object(str(scad), thing["components"], mode=mode, resolution=resolution)
                    # Keep each downloadable SCAD self-contained.
                    source = scad.read_text(encoding="utf-8")
                    source = re.sub(r"(?m)^use\s*<([^>]+)>;?\s*$",
                                    lambda match: (staging / match[1]).read_text(encoding="utf-8"), source)
                    scad.write_text(source, encoding="utf-8")
                    outputs.append(scad)
            if box:
                for mode in modes:
                    body = (staging / f"body_{mode}.scad").read_text(encoding="utf-8")
                    source = [f"module body() {{\n{body}\n}}\n"]
                    placements = ["body();\n"]
                    prefixes = REAR_PLATES if mode == "3dpr" else ("back_plate_",)
                    pitch, allowance = oobb.gv("osp"), oobb.gv("osp_minus")
                    width = details["width"] * pitch - allowance
                    height = details["height"] * pitch - allowance
                    for index, prefix in enumerate(prefixes):
                        plate = (staging / f"{prefix}{mode}.scad").read_text(encoding="utf-8")
                        module = prefix.rstrip("_") if mode == "3dpr" else "rear_plate"
                        source.append(f"module {module}() {{\n{plate}\n}}\n")
                        if mode == "3dpr":
                            # Turn the three plates a quarter turn so the set fits a smaller bed.
                            x = (index - (len(prefixes) - 1) / 2) * (height + layout_gap)
                            y = (width + height) / 2 + layout_gap
                            placements.append(f"translate([{x}, {y}, 0]) rotate([0, 0, 90]) {module}();\n")
                        else:
                            placements.append(f"translate([0, 0, {details['body_depth_mm']}]) {module}();\n")
                    scad = staging / f"{mode}.scad"
                    scad.write_text("".join(source + placements), encoding="utf-8")
                    outputs.append(scad)
            if generate_stl:
                for scad in outputs.copy():
                    stl = scad.with_suffix(".stl")
                    subprocess.run([openscad, "--export-format", "binstl", "-o", stl, scad], check=True)
                    outputs.append(stl)
            for output in outputs:
                for attempt in range(12):
                    try:
                        output.replace(folder / output.name)
                        break
                    except PermissionError as error:
                        if getattr(error, "winerror", None) != 32 or attempt == 11:
                            raise
                        time.sleep(.5)
        print(f"Built {part_id}")


if __name__ == "__main__":
    main()
