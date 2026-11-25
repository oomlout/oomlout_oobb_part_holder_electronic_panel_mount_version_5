"""Render canonical meshes, then publish the catalog sheets and installation books."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps
import yaml

from presentation import assembly_booklet, assembly_viewer
from working_oomp_populate import REAR_PLATES

ROOT = Path(__file__).resolve().parent
NOTICE = "AI-generated CAD images and instructions. Errors possible."
CATALOG = "https://github.com/oomlout/oomp_electronic_panel_mount_version_5"
PROJECT_URL = "https://github.com/oomlout/oomlout_oobb_part_holder_electronic_panel_mount_version_5"
NAMES = dict(panel="Four-sided panel", panel_width_only="Side-mount panel",
             box_width_only="Side-mount box", cutout_only="Clip-in cutter")


def render_jobs(records, **kwargs):
    blender = kwargs.get("blender") or shutil.which("blender")
    cache = Path(kwargs.get("render_dir", ROOT / ".build")).resolve()
    if not blender:
        raise FileNotFoundError("Add Blender to PATH or pass blender= to make_all.main()")
    jobs = []
    for folder, record in records:
        for mode in ("true", "3dpr"):
            directory = cache / folder.name / mode
            box = record["taxonomy_5"] == "box_width_only"
            directory.mkdir(parents=True, exist_ok=True)
            views = ["angle", "top"]
            if mode == "3dpr" and record["taxonomy_5"] != "cutout_only":
                views.extend(["part_holder", "part_device", "aligned", "seated"])
            if box:
                views.extend(["rear", "inside_plate", "outside_plate"])
                if mode == "3dpr":
                    views.extend(["joined", "part_plate", "part_screw", "part_nut"])
            jobs.append(dict(key=folder.name, directory=str(directory), dimensions=record["oobb_details"],
                             source=str(folder / (f"body_{mode}.stl" if box else f"{mode}.stl")),
                             back_plate=str(folder / f"back_plate_{mode}.stl"),
                             views=views))
            if box:
                for prefix in REAR_PLATES:
                    if prefix == "back_plate_":
                        continue
                    plate_dir = directory / prefix.rstrip("_")
                    plate_dir.mkdir(exist_ok=True)
                    jobs.append(dict(key=folder.name + "/" + prefix.rstrip("_"), directory=str(plate_dir),
                                     dimensions=record["oobb_details"], source=str(folder / f"body_{mode}.stl"),
                                     back_plate=str(folder / f"{prefix}{mode}.stl"),
                                     views=["inside_plate", "outside_plate"]))
    job_path = cache / "render_jobs.json"
    job_path.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    subprocess.run([blender, "--background", "--factory-startup", "--python-exit-code", "1",
                    "--python", str(ROOT / "presentation/render_holder.py"), "--", str(job_path)], check=True)
    return cache


def font(size, **kwargs):
    face = kwargs.get("face", "segoeui.ttf")
    try:
        return ImageFont.truetype(face, size)
    except OSError:
        return ImageFont.load_default(size=size)


def catalog_sheet(folder, record, raw, mode, **kwargs):
    prefix = kwargs.get("plate_prefix", "")
    d = record["oobb_details"]
    sheet = Image.new("RGB", (1440, 730), "#faf9f6")
    draw = ImageDraw.Draw(sheet)
    name = NAMES[d["variant"]]
    views, captions = ("angle", "top"), ("Three-quarter view", "Front face")
    depth = d["depth"]
    if prefix:
        name = REAR_PLATES[prefix]["label"]
        views, captions = ("inside_plate", "outside_plate"), ("Flat inside face", "Rear nut pockets and countersinks")
        depth = d["back_plate_depth_mm"]
    elif d["variant"] == "box_width_only":
        views, captions = ("angle", "rear"), ("Open body", "Rear plate fitted")
    draw.text((50, 32), f"{name}   /   {record['device_label'].upper().replace('_', '-')}",
              fill="#202529", font=font(43, face="seguisb.ttf"))
    draw.text((52, 101), f"{d['width']} × {d['height']} OOBB   ·   {depth:g} mm depth",
              fill="#384349", font=font(25))
    for idx, view in enumerate(views):
        with Image.open(raw / f"{view}.png") as source:
            image = ImageOps.contain(source.convert("RGBA"), (660, 445))
        x = 44 + idx * 694
        sheet.paste(image, (x + (660 - image.width)//2, 155), image)
        draw.text((x + 8, 615), captions[idx], fill="#263036", font=font(22))
    draw.line((50, 665, 1390, 665), fill="#c3c9c6", width=2)
    draw.text((52, 680), NOTICE, fill="#3c4446", font=font(18))
    draw.text((1140, 680), "Print clearances" if mode == "3dpr" else "Nominal geometry",
              fill="#3c4446", font=font(18))
    sheet.save(folder / f"{prefix}{mode}_presentation.png", optimize=True)


def assembly_book(folder, record, raw, **kwargs):
    source_id = record["source_oomp_id"]
    digest = hashlib.md5(source_id.encode()).hexdigest()
    number = int(digest[:6], 16)
    code = ""
    while number:
        number, digit = divmod(number, 36)
        code = "0123456789abcdefghijklmnopqrstuvwxyz"[digit] + code
    code = code or "0"
    label = record["device_label"].replace("_", "-").upper()
    style_name = NAMES[record["taxonomy_5"]]
    d = record["oobb_details"]
    parts = dict(holder=dict(key="holder", name=style_name, id=record["id"], quantity=1),
                 device=dict(key="device", name=label, id=source_id, quantity=1,
                             md5=digest, md5_6_alpha=code, short_label=f"oom.lt/a/{code}",
                             identity_provenance="OOMP panel-mount catalog record",
                             short_url=f"https://oom.lt/a/{code}", source_url=f"{CATALOG}/tree/main/parts/{source_id}"))
    steps = []
    additions = dict(part_holder={"holder": 1}, aligned={"device": 1}, seated={})
    printed_keys = ["holder"]
    if d["variant"] == "box_width_only":
        parts["plate"] = dict(key="plate", name="Rear cable plate", quantity=1, id=record["id"]+"/back_plate")
        printed_keys.append("plate")
        for key, name, part_id, code, repo in (
            ("nut", "M3 hex nut", "hardware_nut_m3", "3vb5b", "oomlout_oomp_version_1_messy"),
            ("screw", "M3 × 12 countersunk hex screw", "hardware_screw_countersunk_hex_head_black_m3_diameter_12_mm_length",
             "1qf1u", "oomp_hardware_screw_version_5"),
        ):
            parts[key] = dict(key=key, name=name, id=part_id, quantity=2, md5_6_alpha=code,
                              md5=hashlib.md5(part_id.encode()).hexdigest(), short_label=f"oom.lt/a/{code}",
                              short_url=f"https://oom.lt/a/{code}",
                              source_url=f"https://github.com/oomlout/{repo}/tree/main/parts/{part_id}")
        additions["part_holder"]["nut"] = 2
        additions["joined"] = dict(plate=1, screw=2)
    for index, step in enumerate(record["assembly_steps"], 1):
        steps.append(dict(key=step["view"], title=f"Operation {index}", action=step["action"],
                          loose_parts=additions[step["view"]]))
    style = dict(page_mm=[297, 210], margin_mm=6, gutter_mm=4, rows=2, columns=2,
                 border="000000", border_width_pt=3, component_border_width_pt=1.1, border_radius_mm=3,
                 thumbnail_height_mm=8.5, quantity_shift_mm=1, quantity_pt=5.8, font_code_pt=6.4,
                 font_body_pt=7, font_url_prefix_pt=4.8)
    book = dict(cover_title=style_name, cover_subtitle=f"{label} / {d['width']} x {d['height']} OOBB",
                project_name="oomlout_oobb_part_holder_electronic_panel_mount_version_5",
                project_url=kwargs.get("project_url") or PROJECT_URL,
                logo_svg="oomlout-LOGO-unshaded-vector.svg", logo_symbol_subpaths=3,
                summary_view="seated", signature_pages=4, summary_step=True,
                summary_title="Printed part", hardware_title="Panel-mount device", details_title="Installation notes",
                viewer_layout="a4-landscape-four-step", viewer_start="page-03")
    book["details"] = [
        f"Front opening: {d['width_cutout_mm']:g} x {d['height_cutout_mm']:g} mm. Retaining shoulder: {d['depth_cutout_mm']:g} mm.",
        f"Device envelope: {d['width_mm']:g} x {d['height_mm']:g} x {d['depth_mm']:g} mm.",
        "The gray envelope shows insertion direction. The catalog supplies dimensions only. Controls and clips are omitted.",
        "The compact OOMP code identifies the purchased device. Its link opens the source catalog record.",
        "Print one holder. Chassis fasteners depend on the receiving structure.",
        "Clip engagement and physical fit still need a sample print.",
        "Regenerate the CAD, booklet and offline viewer with python make_all.py.", NOTICE]
    output = folder / "assembly"
    output.mkdir(exist_ok=True)
    mesh_hash = hashlib.sha256((folder / "3dpr.stl").read_bytes()).hexdigest()
    data = dict(configuration_title=f"{style_name} / {label}", parts=parts, printed_keys=printed_keys,
                physical_item_count=sum(item["quantity"] for item in parts.values()),
                steps=steps, style=style, book=book, production_stl_sha256=mesh_hash,
                logo_sha256=hashlib.sha256((ROOT / "presentation" / book["logo_svg"]).read_bytes()).hexdigest())
    if d["variant"] == "box_width_only":
        book["hardware_title"] = "Device and fasteners"
        book["summary_view"] = "joined"
        book["details"][4] = "The print STL contains the body and all three rear plates. Choose one plate for assembly and secure it with two M3 screws."
        book["details"].append("Choose the bottom wire opening, the small top-right OOBB Electronics window, or both. The flat faces mate together.")
        book["details"].append("Load four optional M3 patch-panel nuts at the bottom opening and two M3 accessory nuts at the electronics window, as applicable. Drop them in from the rear.")
        data["body_stl_sha256"] = hashlib.sha256((folder / "body_3dpr.stl").read_bytes()).hexdigest()
        data["rear_plate_stl_sha256"] = {
            prefix: hashlib.sha256((folder / f"{prefix}3dpr.stl").read_bytes()).hexdigest()
            for prefix in REAR_PLATES
        }
    for key, item in parts.items():
        if sum(s["loose_parts"].get(key, 0) for s in steps) != item["quantity"]:
            raise ValueError(f"Incorrect assembly quantity for {key}")
    shutil.copyfile(raw / (book["summary_view"] + ".png"), raw / "book_cover.png")
    assembly_booklet.publish(output=output, data=data, raw=raw)
    assembly_booklet.review_outputs(output=output, data=data)
    assembly_viewer.publish(output=output, data=data)
    with (output / "parts.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(k for item in parts.values() for k in item)))
        writer.writeheader()
        writer.writerows(parts.values())


def main(**kwargs):
    parts_dir = Path(kwargs.get("parts_dir", "parts")).resolve()
    part_ids = kwargs.get("part_ids")
    if part_ids is None:
        part_ids = sorted(path.parent.name for path in parts_dir.glob("*/working.yaml"))
    records = []
    for part_id in part_ids:
        folder = parts_dir / part_id
        records.append((folder, yaml.safe_load((folder / "working.yaml").read_text(encoding="utf-8"))))
    cache = render_jobs(records, **kwargs)
    for folder, record in records:
        for mode in ("true", "3dpr"):
            raw = cache / folder.name / mode
            catalog_sheet(folder, record, raw, mode)
            if record["taxonomy_5"] == "box_width_only":
                for prefix in REAR_PLATES:
                    plate_raw = raw if prefix == "back_plate_" else raw / prefix.rstrip("_")
                    catalog_sheet(folder, record, plate_raw, mode, plate_prefix=prefix)
        if record["taxonomy_5"] != "cutout_only":
            assembly_book(folder, record, cache / folder.name / "3dpr", **kwargs)


if __name__ == "__main__":
    main()
