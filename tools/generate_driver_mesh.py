#!/usr/bin/env python3
"""Generate a sitting human driver Collada mesh for BeamNG.drive."""

from __future__ import annotations

import math
import os
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "vehicles" / "common" / "drivingPedestrians"
TEX_DIR = OUT_DIR / "textures"


def write_png(path: Path, width: int, height: int, pixels) -> None:
    """Write a minimal RGBA PNG."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(channel for px in row for channel in px) for row in pixels)
    compressed = zlib.compress(raw, 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def skin_pixel(x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    t = (x / max(w - 1, 1) + y / max(h - 1, 1)) * 0.5
    r = int(lerp(198, 168, t))
    g = int(lerp(152, 118, t))
    b = int(lerp(118, 88, t))
    return r, g, b, 255


def cloth_pixel(base: tuple[int, int, int], x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    weave = ((x // 4) ^ (y // 4)) & 1
    r, g, b = base
    shade = 12 if weave else 0
    return max(0, r - shade), max(0, g - shade), max(0, b - shade), 255


def hair_pixel(x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    noise = ((x * 13 + y * 7) % 17) - 8
    return 42 + noise, 32 + noise, 24 + noise, 255


def make_textures() -> None:
    size = 128
    skin = [[skin_pixel(x, y, size, size) for x in range(size)] for y in range(size)]
    shirt = [[cloth_pixel((58, 92, 148), x, y, size, size) for x in range(size)] for y in range(size)]
    pants = [[cloth_pixel((48, 52, 62), x, y, size, size) for x in range(size)] for y in range(size)]
    hair = [[hair_pixel(x, y, size, size) for x in range(size)] for y in range(size)]
    shoes = [[cloth_pixel((34, 34, 38), x, y, size, size) for x in range(size)] for y in range(size)]
    write_png(TEX_DIR / "dp_skin.color.png", size, size, skin)
    write_png(TEX_DIR / "dp_shirt.color.png", size, size, shirt)
    write_png(TEX_DIR / "dp_pants.color.png", size, size, pants)
    write_png(TEX_DIR / "dp_hair.color.png", size, size, hair)
    write_png(TEX_DIR / "dp_shoes.color.png", size, size, shoes)


def box(name: str, material: str, cx: float, cy: float, cz: float, sx: float, sy: float, sz: float, rx=0.0, ry=0.0, rz=0.0):
  """Return vertices, normals, uvs, and indices for an axis-aligned box."""
  hx, hy, hz = sx / 2, sy / 2, sz / 2
  corners = [
      (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
      (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
  ]

  def rot(x, y, z):
      # intrinsic rotations: Z then Y then X
      czr, szr = math.cos(rz), math.sin(rz)
      cyr, syr = math.cos(ry), math.sin(ry)
      cxr, sxr = math.cos(rx), math.sin(rx)
      x1 = x * czr - y * szr
      y1 = x * szr + y * czr
      z1 = z
      x2 = x1 * cyr + z1 * syr
      y2 = y1
      z2 = -x1 * syr + z1 * cyr
      x3 = x2
      y3 = y2 * cxr - z2 * sxr
      z3 = y2 * sxr + z2 * cxr
      return x3 + cx, y3 + cy, z3 + cz

  verts = [rot(*c) for c in corners]
  faces = [
      (0, 1, 2, 3, (0, 0, -1)),
      (4, 7, 6, 5, (0, 0, 1)),
      (0, 4, 5, 1, (0, -1, 0)),
      (2, 6, 7, 3, (0, 1, 0)),
      (0, 3, 7, 4, (-1, 0, 0)),
      (1, 5, 6, 2, (1, 0, 0)),
  ]
  positions = []
  normals = []
  uvs = []
  indices = []
  base = 0
  for a, b, c, d, n in faces:
      quad = [a, b, c, d]
      for vid in quad:
          x, y, z = verts[vid]
          positions.extend([x, y, z])
          normals.extend(n)
          uvs.extend([0.5, 0.5])
      indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])
      base += 4
  return {
      "name": name,
      "material": material,
      "positions": positions,
      "normals": normals,
      "uvs": uvs,
      "indices": indices,
      "vertex_count": base,
  }


def make_meshes():
    parts = []
    # Sitting driver pose in BeamNG vehicle space (+X left, +Y back, +Z up, forward = -Y)
    parts.append(box("dp_driver_head", "dp_hair", 0.42, -0.38, 0.98, 0.17, 0.19, 0.20, rx=0.08))
    parts.append(box("dp_driver_face", "dp_skin", 0.42, -0.36, 0.97, 0.15, 0.11, 0.14, rx=0.08))
    parts.append(box("dp_driver_neck", "dp_skin", 0.42, -0.37, 0.86, 0.10, 0.09, 0.10))
    parts.append(box("dp_driver_torso", "dp_shirt", 0.44, -0.40, 0.72, 0.34, 0.28, 0.42, rx=0.12))
    parts.append(box("dp_driver_pelvis", "dp_pants", 0.44, -0.42, 0.52, 0.30, 0.24, 0.18))
    parts.append(box("dp_driver_thigh_L", "dp_pants", 0.58, -0.46, 0.46, 0.16, 0.42, 0.20, rz=0.15))
    parts.append(box("dp_driver_thigh_R", "dp_pants", 0.30, -0.46, 0.46, 0.16, 0.42, 0.20, rz=-0.15))
    parts.append(box("dp_driver_calf_L", "dp_pants", 0.60, -0.18, 0.30, 0.14, 0.16, 0.38, rx=-1.35))
    parts.append(box("dp_driver_calf_R", "dp_pants", 0.28, -0.18, 0.30, 0.14, 0.16, 0.38, rx=-1.35))
    parts.append(box("dp_driver_foot_L", "dp_shoes", 0.61, -0.08, 0.08, 0.12, 0.24, 0.08, rx=-0.1))
    parts.append(box("dp_driver_foot_R", "dp_shoes", 0.27, -0.08, 0.08, 0.12, 0.24, 0.08, rx=-0.1))
    parts.append(box("dp_driver_upperarm_L", "dp_shirt", 0.56, -0.44, 0.74, 0.12, 0.12, 0.28, rx=0.55, rz=0.35))
    parts.append(box("dp_driver_lowerarm_L", "dp_skin", 0.62, -0.36, 0.58, 0.10, 0.10, 0.24, rx=1.05, rz=0.15))
    parts.append(box("dp_driver_hand_L", "dp_skin", 0.64, -0.34, 0.48, 0.08, 0.06, 0.05))
    # Right arm mesh used as steering prop
    parts.append(box("dp_driver_upperarm_R", "dp_shirt", 0.30, -0.44, 0.74, 0.12, 0.12, 0.28, rx=0.55, rz=-0.35))
    parts.append(box("dp_driver_lowerarm_R", "dp_skin", 0.24, -0.36, 0.58, 0.10, 0.10, 0.24, rx=1.05, rz=-0.15))
    parts.append(box("dp_driver_hand_R", "dp_skin", 0.22, -0.34, 0.48, 0.08, 0.06, 0.05))
    return parts


def write_dae(path: Path, meshes) -> None:
    materials = {
        "dp_skin": "dp_skin",
        "dp_hair": "dp_hair",
        "dp_shirt": "dp_shirt",
        "dp_pants": "dp_pants",
        "dp_shoes": "dp_shoes",
    }
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">',
        "  <asset><unit meter=\"1\" name=\"meter\"/><up_axis>Z_UP</up_axis></asset>",
        "  <library_effects>",
    ]
    for mat_id, mat_name in materials.items():
        lines.extend([
            f'    <effect id="{mat_id}-effect">',
            "      <profile_COMMON>",
            f'        <newparam sid="{mat_name}_surface"><surface type="2D"><init_from>{mat_name}</init_from></surface></newparam>',
            f'        <newparam sid="{mat_name}_sampler"><sampler2D><source>{mat_name}_surface</source></sampler2D></newparam>',
            "        <technique sid=\"common\">",
            "          <phong>",
            f'            <diffuse><texture texture="{mat_name}_sampler" texcoord="UVMap"/></diffuse>',
            "          </phong>",
            "        </technique>",
            "      </profile_COMMON>",
            "    </effect>",
        ])
    lines.append("  </library_effects>")
    lines.append("  <library_images>")
    for mat_name in materials.values():
        lines.append(f'    <image id="{mat_name}" name="{mat_name}"><init_from>{mat_name}.png</init_from></image>')
    lines.append("  </library_images>")
    lines.append("  <library_materials>")
    for mat_id, mat_name in materials.items():
        lines.append(f'    <material id="{mat_id}" name="{mat_id}"><instance_effect url="#{mat_id}-effect"/></material>')
    lines.append("  </library_materials>")
    lines.append("  <library_geometries>")
    for mesh in meshes:
        pos = " ".join(f"{v:.6f}" for v in mesh["positions"])
        nrm = " ".join(f"{v:.6f}" for v in mesh["normals"])
        uv = " ".join(f"{v:.6f}" for v in mesh["uvs"])
        idx = " ".join(str(i) for i in mesh["indices"])
        vc = mesh["vertex_count"]
        lines.extend([
            f'    <geometry id="{mesh["name"]}-mesh" name="{mesh["name"]}">',
            "      <mesh>",
            f'        <source id="{mesh["name"]}-mesh-positions"><float_array id="{mesh["name"]}-mesh-positions-array" count="{vc*3}">{pos}</float_array><technique_common><accessor source="#{mesh["name"]}-mesh-positions-array" count="{vc}" stride="3"><param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>',
            f'        <source id="{mesh["name"]}-mesh-normals"><float_array id="{mesh["name"]}-mesh-normals-array" count="{vc*3}">{nrm}</float_array><technique_common><accessor source="#{mesh["name"]}-mesh-normals-array" count="{vc}" stride="3"><param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/></accessor></technique_common></source>',
            f'        <source id="{mesh["name"]}-mesh-uvs"><float_array id="{mesh["name"]}-mesh-uvs-array" count="{vc*2}">{uv}</float_array><technique_common><accessor source="#{mesh["name"]}-mesh-uvs-array" count="{vc}" stride="2"><param name="S" type="float"/><param name="T" type="float"/></accessor></technique_common></source>',
            '        <vertices id="' + mesh["name"] + '-mesh-vertices"><input semantic="POSITION" source="#' + mesh["name"] + '-mesh-positions"/></vertices>',
            f'        <triangles material="{mesh["material"]}" count="{len(mesh["indices"])//3}"><input semantic="VERTEX" source="#{mesh["name"]}-mesh-vertices" offset="0"/><input semantic="NORMAL" source="#{mesh["name"]}-mesh-normals" offset="0"/><input semantic="TEXCOORD" source="#{mesh["name"]}-mesh-uvs" offset="0" set="0"/><p>{idx}</p></triangles>',
            "      </mesh>",
            "    </geometry>",
        ])
    lines.append("  </library_geometries>")
    lines.append("  <library_visual_scenes><visual_scene id=\"Scene\" name=\"Scene\">")
    for mesh in meshes:
        lines.append(f'    <node id="{mesh["name"]}" name="{mesh["name"]}" type="NODE"><matrix>1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1</matrix><instance_geometry url="#{mesh["name"]}-mesh"><bind_material><technique_common>')
        lines.append(f'      <instance_material symbol="{mesh["material"]}" target="#{mesh["material"]}"/>')
        lines.append("    </technique_common></bind_material></instance_geometry></node>")
    lines.append("  </visual_scene></library_visual_scenes>")
    lines.append('  <scene><instance_visual_scene url="#Scene"/></scene>')
    lines.append("</COLLADA>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    make_textures()
    meshes = make_meshes()
    write_dae(OUT_DIR / "dp_driver.dae", meshes)
    print(f"Wrote driver mesh to {OUT_DIR}")


if __name__ == "__main__":
    main()
