"""Read the device catalog and populate one OOMP entry per holder variant."""
import math
import re
from pathlib import Path
import subprocess

import oobb
import yaml
from oomp_populate_helper import build_oomp_id, write_extras


PROJECT = Path(__file__).resolve().parent
CATALOG = "oomp_electronic_panel_mount_version_5"

PROJECT_TITLE = "OOBB panel-mount electronics holders"
PROJECT_DESCRIPTION = "Snap a rectangular panel-mount device into an OOBB panel or an open-backed box with a removable cable plate. A matching solid cutter brings the same clip shoulder into another CAD design."

# Match the "little" window and side pin offsets in OOBB Electronics get_spacer.
ELECTRONICS_CATALOG = "https://github.com/oomlout/oomlout_oobb_electronic_version_5"
REAR_PLATES = {}
REAR_PLATES["back_plate_"] = dict(label="Bottom wire opening", bottom=True, electronics=False)
REAR_PLATES["back_plate_electronics_"] = dict(label="OOBB Electronics window", bottom=False, electronics=True)
REAR_PLATES["back_plate_both_"] = dict(label="Both openings", bottom=True, electronics=True)


def assembly_steps(style, **kwargs):
    steps = []
    if style == "cutout_only":
        steps.append(dict(view="angle", action="Import the positive cutter alongside the block you want to machine or print."))
        steps.append(dict(view="top", action="Align its narrow end with the outside face of the block. The wider pocket extends inward along positive Z."))
        steps.append(dict(view="angle", action="Subtract the cutter from the block. Inspect the opening and the retaining shoulder in section before exporting."))
    else:
        steps.append(dict(view="part_holder", action="Print one holder using the 3D-print STL. Clear the opening and identify the front face."))
        if style == "box_width_only":
            steps[0]["action"] = "Print the body and your choice of rear plate. Slide one M3 nut into the middle side slot on each body rail."
        steps.append(dict(view="aligned", action="With the device disconnected, align its body with the opening. Keep the bezel outside the holder."))
        steps.append(dict(view="seated", action="Press the body straight into the opening until the bezel sits flat. Check that the clips engage before mounting the holder."))
        if style == "box_width_only":
            steps.append(dict(view="joined", action="If fitting an accessory, drop its M3 nuts into the plate from the rear and fasten the accessory from inside. Route the wires, seat the flat faces together, and fit two M3 × 12 mm countersunk screws from the rear."))
    return steps


def catalog_root(**kwargs):
    override = kwargs.get("catalog_dir")
    local = Path(kwargs.get("local_catalog", Path("C:/gh") / CATALOG))
    cached = Path(kwargs.get("cached_catalog", PROJECT / ".deps" / CATALOG))
    url = kwargs.get("catalog_url", f"https://github.com/oomlout/{CATALOG}.git")

    if override is not None:
        return Path(override)
    if local.is_dir():
        return local
    if not cached.exists():
        cached.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", url, str(cached)], check=True)
    return cached


def holder_entries(device, **kwargs):
    pitch = oobb.gv("osp")
    edge_allowance = oobb.gv("osp_minus")
    panel_depth = kwargs.get("panel_depth_mm", 3)
    wall = kwargs.get("wall_mm", 3)
    clip_clearance = kwargs.get("clip_clearance_mm", 0.5)  # per side
    rear_clearance = kwargs.get("rear_clearance_mm", 1)
    back_plate = kwargs.get("back_plate_depth_mm", 3)
    screw_length = kwargs.get("join_screw_length_mm", 12)
    embedded_depth = kwargs.get("embedded_nut_depth_mm", 3)
    patch_nut_depth = kwargs.get("patch_nut_depth_mm", 2.45)
    electronics_window = kwargs.get("electronics_window_mm", 20.25)
    electronics_radius = kwargs.get("electronics_corner_radius_mm", 3.75)

    dimensions = {}
    for key in ("width_mm", "height_mm", "depth_mm", "width_cutout_mm",
                "height_cutout_mm", "depth_cutout_mm"):
        value = device.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{device['id']} needs a positive, finite {key}, got {value!r}")
        dimensions[key] = value

    lip = dimensions["depth_cutout_mm"]
    cavity_depth = dimensions["depth_mm"] + rear_clearance
    if clip_clearance < 0 or rear_clearance < 0 or wall <= 0 or panel_depth <= 0 or cavity_depth <= lip:
        raise ValueError(f"Invalid wall, clearance or lip dimensions for {device['id']}")
    cavity_width = max(dimensions["width_mm"], dimensions["width_cutout_mm"]) + 2 * clip_clearance
    cavity_height = max(dimensions["height_mm"], dimensions["height_cutout_mm"]) + 2 * clip_clearance
    width = math.ceil((cavity_width + edge_allowance) / pitch) + 2
    height = math.ceil((cavity_height + 2 * wall + edge_allowance) / pitch)
    box_width = max(width, 5)
    box_height = max(height, 4)
    half_pitch = pitch / 2
    body_depth = math.ceil(math.ceil((cavity_depth + wall) / half_pitch) * half_pitch)
    box_depth = body_depth + back_plate

    variants = []
    variants.append(dict(variant="panel_width_only", width=width, height=height, depth=panel_depth))
    variants.append(dict(variant="panel", width=width, height=height + 2, depth=panel_depth))
    variants.append(dict(variant="box_width_only", width=box_width, height=box_height, depth=box_depth))
    variants.append(dict(variant="cutout_only", width=math.ceil((cavity_width + edge_allowance) / pitch),
                         height=math.ceil((cavity_height + edge_allowance) / pitch), depth=cavity_depth))

    entries = []
    # Keep the original catalog ID as a foreign key. Only omit dimension segments
    # in the local taxonomy, where the holder's own dimensions follow its style.
    device_segments = [str(device.get(f"taxonomy_{i}", "")) for i in range(1, 16)]
    device_name = "_".join(s for s in device_segments if s and not re.fullmatch(
        r"[\d._]+_mm_(width|height|depth)", s))
    if not device_name:
        raise ValueError(f"Missing catalog taxonomy for {device['id']}")
    for variant in variants:
        details = dict(variant)
        if variant["variant"] == "box_width_only":
            join_x = (box_width - 1) * half_pitch
            # M3 infill is an odd half-step from the first M6 on each side rail.
            join_y = 0 if box_height % 2 == 0 else half_pitch
            if back_plate - patch_nut_depth < 0.4:
                raise ValueError("Allow at least 0.4 mm for the seat below each rear-loaded nut")
            wire_bottom = -(box_height*pitch-edge_allowance)/2
            electronics_center = [join_x - 1.5*pitch, (box_height - 2)*half_pitch]
            details.update(back_plate_depth_mm=back_plate, body_depth_mm=body_depth,
                           join_screw_length_mm=screw_length, join_nut_skin_mm=1.5,
                           join_x_mm=join_x, join_y_mm=join_y, wire_width_mm=2*pitch,
                           wire_height_mm=2*pitch, wire_bottom_y_mm=wire_bottom,
                           embedded_nut_depth_mm=embedded_depth,
                           patch_nut_depth_mm=patch_nut_depth, future_mount_x_mm=1.5*pitch,
                           future_mount_rows_mm=[-(box_height-1)*half_pitch, -(box_height-3)*half_pitch],
                           electronics_center_mm=electronics_center, electronics_window_mm=electronics_window,
                           electronics_corner_radius_mm=electronics_radius, electronics_nut_x_offset_mm=pitch,
                           electronics_nut_y_offset_mm=-half_pitch)
        details.update(dimensions)
        details.update(corner_radius_mm=kwargs.get("corner_radius_mm", 7),
                       edge_radius_mm=kwargs.get("edge_radius_mm", 1.5),
                       cavity_width_mm=cavity_width, cavity_height_mm=cavity_height,
                       cavity_depth_mm=cavity_depth, oobb_type=variant["variant"], run_scad=True)
        entry = dict(taxonomy_1="oobb", taxonomy_2="part", taxonomy_3="holder",
                     taxonomy_4=device_name, taxonomy_5=variant["variant"],
                     taxonomy_6=f"{variant['width']}_width", taxonomy_7=f"{variant['height']}_height",
                     taxonomy_8=f"{variant['depth']:g}_depth".replace(".", "_"),
                     source_oomp_id=device["id"], device_label=device.get("manufacturer_part_number") or device_name,
                     assembly_steps=assembly_steps(variant["variant"]), oobb_details=details)
        entries.append(entry)
    return entries


def main(**kwargs):
    root = catalog_root(**kwargs)
    files = sorted((root / "parts").glob("*/working.yaml"))
    if not files:
        raise FileNotFoundError(f"No device entries in {root / 'parts'}")
    entries = []
    for path in files:
        device = yaml.safe_load(path.read_text(encoding="utf-8"))
        if device["id"] != path.parent.name:
            raise ValueError(f"Catalog ID does not match its directory at {path}")
        for entry in holder_entries(device, **kwargs):
            entries.append(entry)
    part_ids = [build_oomp_id(entry) for entry in entries]
    if len(set(part_ids)) != len(part_ids):
        raise ValueError("Duplicate holder ID after removing device dimensions. Give the devices distinct catalog model names.")
    for entry, part_id in zip(entries, part_ids):
        old_id = f"oobb_part_holder_{entry['source_oomp_id']}_{entry['taxonomy_5']}"
        for base in (Path("parts_source"), Path("parts")):
            old, new = base / old_id, base / part_id
            if old != new and old.is_dir():
                if new.exists():
                    raise FileExistsError(f"Both old and new entries exist: {old}, {new}")
                old.rename(new)
    write_extras(entries)
    return part_ids


if __name__ == "__main__":
    main()
