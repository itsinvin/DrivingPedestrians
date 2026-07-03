# Driving Pedestrians

> **Realistic human drivers for every car in BeamNG.drive** — no more ghost vehicles.

## Description

**Driving Pedestrians** is a BeamNG.drive mod that fills empty driver seats with visible, human-looking pedestrians so your world feels alive. Whether you are cruising through traffic, filming a chase, testing crashes, or just driving around, cars finally look like someone is behind the wheel.

Each driver is a fully modeled seated character with skin tones, hair, clothing, and shoes. They are anchored to the vehicle with JBeam flexbodies, so they move, lean, and deform with the car during hard braking, cornering, and collisions. The right arm is rigged as a steering prop, rotating with the wheel so it genuinely looks like the pedestrian is driving — not just sitting there.

The mod supports **30+ official BeamNG vehicles** out of the box with hand-tuned seat positions, plus a **generic fallback** for modded cars and anything with an Additional Modification slot. You can pick from multiple driver appearances, add an optional front passenger, fine-tune placement in the Tuning menu, or let the built-in auto-enable system populate drivers on every spawned vehicle — including traffic and AI.

**[Download the latest release (DrivingPedestrians.zip)](https://github.com/itsinvin/DrivingPedestrians/releases/latest)**

---

A BeamNG.drive mod that places **realistic human pedestrian drivers** inside vehicles so they no longer look empty. Drivers sit in a natural driving pose, track vehicle movement, and animate their steering arm with the wheel.

## Features

- **Visible human drivers** with skin, hair, clothing, and shoes
- **Sitting pose** designed for left-hand-drive vehicle seats
- **Steering arm animation** — the right arm follows steering input like a real driver
- **30+ vanilla vehicle presets** with per-car seat offsets (pickup, ETK, Gavril, Hirochi, Cherrier, etc.)
- **Generic fallback** for modded vehicles and anything with an Additional Modification slot
- **Optional front passenger** via the parts menu
- **Driver appearance variants**: Casual Male, Casual Female, Business
- **Tuning menu offsets** to fine-tune driver position per vehicle
- **Auto-enable mode** adds drivers to spawned vehicles automatically
- **Traffic / AI support** when auto-enable is on

## Installation

1. Download **[DrivingPedestrians.zip](https://github.com/itsinvin/DrivingPedestrians/releases/latest)** from Releases (or build it yourself — see Packaging below).
2. Place the zip in your BeamNG mods folder:
   - **Windows:** `%LOCALAPPDATA%/BeamNG.drive/current/mods/`
   - **Linux:** `~/.local/share/BeamNG.drive/current/mods/`
   - **macOS:** `~/Library/Application Support/BeamNG.drive/current/mods/`
3. Enable **Driving Pedestrians** in the in-game Mod Manager.
4. Restart the game or reload the level.

You can also use the unpacked folder directly in `mods/unpacked/DrivingPedestrians/`.

## Usage

### Manual (recommended for fine control)

1. Spawn any supported vehicle.
2. Open **Vehicle Configuration** (`Ctrl+W` or the parts icon).
3. Go to **Additional Modification**.
4. Select **Pedestrian Driver**.
5. Optionally choose **Driver Appearance** and **Front Passenger** in sub-slots.
6. Use **Tuning** → **Driving Pedestrians** to adjust seat position if needed.

### Automatic

With default settings, drivers are added automatically when you spawn a vehicle. Bindings (configure in **Options → Controls → Gameplay**):

| Action | Default | Description |
|--------|---------|-------------|
| Toggle Auto Pedestrian Drivers | *(unbound)* | Turn auto-driver on/off |
| Add Pedestrian Driver to Current Vehicle | *(unbound)* | Force-add a driver to your current car |

Settings are saved to `settings/drivingPedestrians.json` in your BeamNG user folder.

## Supported Vehicles

Pre-tuned offsets are included for:

`pickup`, `hseries`, `roamer`, `etk800`, `etkc`, `etki`, `coupe`, `fullsize`, `barstow`, `bluebuck`, `burnside`, `moonhawk`, `pessima`, `pessima2`, `legran`, `vivace`, `wendover`, `scintilla`, `sunburst`, `sunburst2`, `covet`, `miramar`, `hopper`, `midsize`, `bastion`, `autobello`, `lansdale`, `us_semi`, `citybus`

Other vehicles with an **Additional Modification** slot can use the **Pedestrian Driver (Generic)** part. Use the Tuning menu offsets to align the driver if they clip through the roof or sit too low.

## Mod Structure

```
DrivingPedestrians/
├── scripts/drivingPedestrians/modScript.lua    # Loads GE extensions
├── lua/ge/extensions/drivingPedestrians/       # Auto-driver logic, settings
├── lua/vehicle/extensions/auto/                # Per-vehicle GFX hooks
├── vehicles/common/drivingPedestrians/         # Meshes, materials, JBeam parts
└── tools/generate_driver_mesh.py               # Mesh/texture generator
```

## Rebuilding Assets

If you modify the mesh generator:

```bash
python3 tools/generate_driver_mesh.py
```

This regenerates `dp_driver.dae` and texture maps under `vehicles/common/drivingPedestrians/`.

## Packaging

```bash
zip -r DrivingPedestrians.zip \
  scripts lua vehicles tools README.md \
  -x "*.git*" -x "*__pycache__*"
```

## Tips

- If a driver clips through the roof on a specific car, open **Tuning** and lower **Driver Height Offset** or move them with the lateral/fore-aft sliders.
- For low sports cars (Scintilla, Autobello), presets already use lower Z offsets; tweak further if needed.
- For trucks and buses, presets raise the driver toward the cab seat height.
- Disable **Auto Pedestrian Drivers** when you want empty cars for screenshots or crash tests.

## Credits

Created for the BeamNG modding community. Uses BeamNG's standard JBeam flexbody/prop systems and Lua extension hooks.

## License

MIT License — see repository for details.
