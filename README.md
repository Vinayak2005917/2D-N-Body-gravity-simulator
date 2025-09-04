# 2D N-Body Gravity Simulator


<img width="1602" height="939" alt="image" src="https://github.com/user-attachments/assets/31f9d946-a21b-4447-af73-3972d67e6f01" />


This project simulates the motion of multiple objects under gravity in 2D using Pygame. **It is currently under active development.**

## Features
- Real-time simulation of gravitational interactions
- Baked playback of object trajectories
- Interactive UI with buttons and input fields
- Adjustable simulation parameters (`dt`, `iterations`)
- Object creation, dragging, and resizing
- Grid overlay for spatial reference
- Velocity and simulation info display
- Pause, reset, bake, and replay controls
- Modular code structure (`Object.py`, `bake.py`, `utils.py`)
- Clean and readable UI elements

## Getting Started
1. Install Python 3 and Pygame:
   ```bash
   pip install pygame
   ```
2. Run `App.py` to start the simulation.
3. Use the UI to add objects, start, reset, bake, and replay simulations.
4. Adjust `dt` and `iterations` using the input fields for custom simulation speed and accuracy.

## File Structure
- `App.py`: Main application and UI
- `Object.py`: Physics object class
- `bake.py`: Baked simulation logic
- `utils.py`: UI components (Button, InputBox, Text)
- `Test/`: Screenshots and test scripts

## Planned Features
- Collision handling (merge, bounce)
- Saving/loading simulation states
- More advanced integrators
- Customizable object properties
- Performance optimizations
- Documentation and tutorials

## Contributing
Pull requests and suggestions are welcome! Please open an issue for bugs or feature requests.

## License
MIT

---

*This project is a work in progress. Expect frequent updates and new features.*
