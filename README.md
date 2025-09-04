# 2D N-Body Gravity Simulator

<img width="1602" height="939" alt="image" src="https://github.com/user-attachments/assets/31f9d946-a21b-4447-af73-3972d67e6f01" />

Real-time 2D n-body gravity simulator built with Pygame. The codebase now spans over a thousand lines of Python across the app, physics, UI, and tooling, and is under active development.

## Features
- Real-time gravitational interactions with multiple bodies (n-body)
- Safe post-step collision merging in the live sim; elastic bounce in baked runs
- Baked playback of trajectories for smooth, deterministic replays
- Presets: Random, Three planet system, Four planet system (binary stars with two planets), Small star cluster
- Interactive UI: add/delete bodies, drag to move, edge-hover resize, mass and velocity editors
- Adjustable simulation parameters (`dt`, `iterations`)
- Pause/Stop/Resume with a non-resetting timer; Reset to clear sim
- Grid overlay, optional trails toggle, and velocity arrows for direction/speed
- Modular structure: Physics, UI widgets, bake tooling, presets

## Getting Started
1. Install dependencies:
   - Python 3.10+
   - Pygame (or use the provided `requirements.txt`)
   
   Optional (recommended):
   - Create and activate a virtual environment
   - Install from requirements
   
2. Run the app: launch `App.py`.
3. Use the UI to add objects, start/stop, bake, and replay. Tune `dt` and `iterations` for speed/accuracy.

## Controls and UI
- Buttons: Add, Start, Stop, Reset, Trail, Bake, Run Bake
- Inputs: dt, iterations (global); mass, horizontal/vertical velocity (selected object)
- Dropdowns: Integrator (placeholder), Presets
- Interactions: drag inside a body to move; hover near edge to resize

## File Structure
- `App.py`: Main loop, UI wiring, simulation step
- `Object.py`: `Physics_Object` (state, gravity, integration, interactions)
- `bake.py`: Bake trajectories to `temp_bake.txt` and replay
- `utils.py`: UI widgets (Button, InputBox, Text, DropdownMenu)
- `arrow.py`: Velocity arrow rendering utility
- `Object_systems.py`: Ready-made preset systems
- `requirements.txt`: Python dependencies

## Contributing
Contributions are welcome. Check the repository’s Issues tab for open items and ideas to tackle—there are issues filed for bugs and enhancements to help new contributors get started. If you don’t see your idea there, open a new issue and we can discuss.

Suggestions, bug reports, and pull requests are appreciated.

## License
MIT

---

This project is a work in progress; expect updates and ongoing improvements.
