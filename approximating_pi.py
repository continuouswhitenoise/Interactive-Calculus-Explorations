import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.widgets import Slider
import numpy as np

# Dark mode styling parameters
plt.style.use("dark_background")
BG_COLOR = "#121212"
AXES_COLOR = "#1e1e1e"
TEXT_COLOR = "#e2e8f0"
INSCRIBED_COLOR = "#2dd4bf"  # Bright Teal
CIRCUMSCRIBED_COLOR = "#fb923c"  # Bright Orange
CIRCLE_COLOR = "#64748b"  # Muted Slate
SLIDER_COLOR = "#b74980"
FILL_ALPHA = 0.22

# Precompute geometries and clear text metrics for n = 3 to 60
POLYGON_CACHE = {}
for n in range(3, 61):
    # Inscribed: vertices on unit circle R=1
    angles_in = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / n
    x_in_c = np.append(np.cos(angles_in), np.cos(angles_in))
    y_in_c = np.append(np.sin(angles_in), np.sin(angles_in))
    verts_in = np.column_stack([np.cos(angles_in), np.sin(angles_in)])

    side_in = 2 * np.sin(np.pi / n)
    perim_in = n * side_in
    area_in = 0.5 * n * np.sin(2 * np.pi / n)

    # Circumscribed: apothem r=1, so radius R_out = 1 / cos(pi/n)
    r_out = 1.0 / np.cos(np.pi / n)
    angles_out = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / n
    x_out_c = np.append(r_out * np.cos(angles_out), r_out * np.cos(angles_out))
    y_out_c = np.append(r_out * np.sin(angles_out), r_out * np.sin(angles_out))
    verts_out = np.column_stack([r_out * np.cos(angles_out), r_out * np.sin(angles_out)])

    side_out = 2 * np.tan(np.pi / n)
    perim_out = n * side_out
    area_out = n * np.tan(np.pi / n)

    # Clean, non-colliding readout string
    text_str = (
        f"n = {n} sides   |   True Area: π = {np.pi:.5f}   |   True Perimeter = 2π = {2*np.pi:.5f}\n"
        f"INSCRIBED:       Area = {area_in:.5f}    |    Perimeter = {perim_in:.5f}\n"
        f"CIRCUMSCRIBED:   Area = {area_out:.5f}   |    Perimeter = {perim_out:.5f}"
    )
    POLYGON_CACHE[n] = (x_in_c, y_in_c, verts_in, x_out_c, y_out_c, verts_out, text_str)

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(12, 7.2))
fig.patch.set_facecolor(BG_COLOR)
plt.subplots_adjust(bottom=0.28, top=0.85, wspace=0.22)

fig.suptitle(
    "Approximating π Using Regular Polygons\n",
    fontsize=14,
    fontweight="bold",
    color=TEXT_COLOR,
    y=0.95,
)

# Subtitle directly beneath
fig.text(
    0.5,
    0.905,
    "[Press SPACEBAR to Play / Pause or Drag!]",
    ha="center",
    va="center",
    fontsize=9.5,
    color="#94a3b8",  # Muted slate/gray
)

theta = np.linspace(0, 2 * np.pi, 500)
circle_x, circle_y = np.cos(theta), np.sin(theta)

def setup_axes(ax, title):
    ax.set_facecolor(AXES_COLOR)
    ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT_COLOR, pad=10)
    ax.set_aspect("equal")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.65, 1.65)
    ax.axhline(0, color="#475569", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="#475569", linewidth=0.8, linestyle="--")
    ax.grid(True, color="#334155", alpha=0.5, linestyle=":")
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#475569")
    ax.set_xlabel("x", color=TEXT_COLOR)
    ax.set_ylabel("y", color=TEXT_COLOR)

setup_axes(ax_left, "Inscribed Polygon")
setup_axes(ax_right, "Circumscribed Polygon")

# Static unit circles
ax_left.plot(circle_x, circle_y, color=CIRCLE_COLOR, linewidth=1.5)
ax_right.plot(circle_x, circle_y, color=CIRCLE_COLOR, linewidth=1.5)

# Initial artists (n=6)
init_n = 6
x_in_c, y_in_c, verts_in, x_out_c, y_out_c, verts_out, init_text = POLYGON_CACHE[init_n]

(inscribed_line,) = ax_left.plot(x_in_c, y_in_c, "o-", color=INSCRIBED_COLOR, linewidth=2, markersize=4)
(circumscribed_line,) = ax_right.plot(x_out_c, y_out_c, "o-", color=CIRCUMSCRIBED_COLOR, linewidth=2, markersize=4)

inscribed_patch = MplPolygon(verts_in, closed=True, facecolor=INSCRIBED_COLOR, alpha=FILL_ALPHA)
circumscribed_patch = MplPolygon(verts_out, closed=True, facecolor=CIRCUMSCRIBED_COLOR, alpha=FILL_ALPHA)
ax_left.add_patch(inscribed_patch)
ax_right.add_patch(circumscribed_patch)

# Prominent, fixed-position metrics readout banner
info_text = fig.text(
    0.5,
    0.16,
    init_text,
    ha="center",
    va="center",
    fontsize=10.5,
    color=TEXT_COLOR,
    family="monospace",
    bbox=dict(boxstyle="round,pad=0.6", facecolor=AXES_COLOR, edgecolor="#475569", linewidth=1),
)

# Slider setup
ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03], facecolor=AXES_COLOR)
n_slider = Slider(ax=ax_slider, label="Sides (n)", valmin=3, valmax=60, valinit=init_n, valstep=1, color=SLIDER_COLOR)
n_slider.label.set_color(TEXT_COLOR)
n_slider.valtext.set_color(TEXT_COLOR)

def apply_state(val):
    n_int = int(round(val))
    if n_int not in POLYGON_CACHE:
        return
    x_in_c, y_in_c, verts_in, x_out_c, y_out_c, verts_out, text_str = POLYGON_CACHE[n_int]
    inscribed_line.set_data(x_in_c, y_in_c)
    circumscribed_line.set_data(x_out_c, y_out_c)
    inscribed_patch.set_xy(verts_in)
    circumscribed_patch.set_xy(verts_out)
    info_text.set_text(text_str)
    fig.canvas.draw_idle()

n_slider.on_changed(apply_state)

is_playing = False

def animate_step(frame):
    if not is_playing:
        return
    current_n = int(round(n_slider.val))
    next_n = 3 if current_n >= 60 else current_n + 1
    n_slider.set_val(next_n)

# Smooth ~30 FPS loop without backend crashes
anim = animation.FuncAnimation(fig, animate_step, interval=50, cache_frame_data=False)

def on_key_press(event):
    global is_playing
    if event.key == " ":
        is_playing = not is_playing

fig.canvas.mpl_connect("key_press_event", on_key_press)
plt.show()
