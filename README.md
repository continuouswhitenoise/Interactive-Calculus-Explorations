# calc-lab

An interactive visual exploration of **Archimedes' Method of Exhaustion**, demonstrating how regular inscribed and circumscribed polygons sandwich the true area (π) and perimeter (2π) of a unit circle (R=1) as side count n → ∞.

![Preview](assets/preview.gif)

## Features
- **Dual-Bound Visualization**: Side-by-side comparison of inner (inscribed) and outer (circumscribed) polygonal bounds with dark-mode aesthetic.
- **Precomputed Geometry Cache**: Fast, lag-free stepping across n ∈ using cached NumPy arrays.
- **Interactive Controls**:
  - **Sides (n) Slider**: Manually scrub vertex counts.
  - **Speed (ms) Slider**: Adjust animation frame interval dynamically (20 ms to 400 ms).
  - **Play / Pause & Reset Buttons**: Standard GUI playback toggles.
- **Keyboard Shortcuts**: Full desktop control without touching the mouse.

---

## Keyboard & UI Controls

| Key / Control | Action |
| :--- | :--- |
| `SPACE` | Play / Pause animation |
| `RIGHT ARROW` | Step n + 1 |
| `LEFT ARROW` | Step n - 1 |
| `UP ARROW` | Increase speed (lower interval) |
| `DOWN ARROW` | Decrease speed (higher interval) |
| **Sides (n) Slider** | Jump directly to any n ∈ |
| **Interval (ms) Slider** | Fine-tune playback speed |
| **Reset Button** | Reset to n=6 and pause |

---

## Mathematical Foundations

For a unit circle (R=1, Area = π ≈ 3.14159, Perimeter = 2π ≈ 6.28318):

### 1. Inscribed Polygon (Inner Bound)
- **Vertex Radius**: R = 1
- **Side Length**: \(s_{\text{in}} = 2 \sin\left(\frac{\pi}{n}\right)\)
- **Perimeter**: \(P_{\text{in}} = n \cdot s_{\text{in}} = 2n \sin\left(\frac{\pi}{n}\right)\)
- **Area**: \(A_{\text{in}} = \frac{1}{2} n \sin\left(\frac{2\pi}{n}\right)\)

### 2. Circumscribed Polygon (Outer Bound)
- **Apothem**: \(r = 1 \implies\) **Outer Radius**: \(R_{\text{out}} = \frac{1}{\cos(\pi/n)}\)
- **Side Length**: \(s_{\text{out}} = 2 \tan\left(\frac{\pi}{n}\right)\)
- **Perimeter**: \(P_{\text{out}} = n \cdot s_{\text{out}} = 2n \tan\left(\frac{\pi}{n}\right)\)
- **Area**: \(A_{\text{out}} = n \tan\left(\frac{\pi}{n}\right)\)

### Sandwich Convergence Table

| n (Sides) | Inscribed Area (\(A_{\text{in}}\)) | True Area (π) | Circumscribed Area (\(A_{\text{out}}\)) | Gap (Δ A) |
| :---: | :---: | :---: | :---: | :---: |
| **3** (Triangle) | 1.29904 | 3.14159 | 5.19615 | 3.89711 |
| **6** (Hexagon) | 2.59808 | 3.14159 | 3.46410 | 0.86602 |
| **12** (Dodecagon) | 3.00000 | 3.14159 | 3.21539 | 0.21539 |
| **24** | 3.10583 | 3.14159 | 3.15966 | 0.05383 |
| **60** | 3.13585 | 3.14159 | 3.14447 | 0.00862 |

---

## Project Structure

```text
calc-lab/
├── assets/
│   └── preview.gif     # Generated visualization preview
├── approx_pi.py        # Main interactive Matplotlib script
├── generate_preview.py # Script to render assets/preview.gif
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## Quickstart

1. **Clone the repository**:
   ```bash
   git clone https://github.com
   cd calc-lab
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the interactive app**:
   ```bash
   python approx_pi.py
   ```

---

## Performance & Architecture Notes
- Uses **`cache_frame_data=False`** in `FuncAnimation` to prevent RAM accumulation during indefinite loops.
- All polygon vertex calculations (`x`, `y`, patches) and monospace text readouts are pre-populated into a dictionary (`POLYGON_CACHE`) at startup, ensuring O(1) frame updates.
