import numpy as np
import matplotlib

# Universal high-performance display engine selector loop
try:
    matplotlib.use('qtagg')
except Exception:
    try:
        matplotlib.use('MacOSX')
    except Exception:
        pass

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Style parameters for clean, minimalist textbook appearance
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'Lucida Grande']
plt.rcParams['text.color'] = '#E0E0E0'
plt.rcParams['axes.labelcolor'] = '#A0A0A0'
plt.rcParams['xtick.color'] = '#707070'
plt.rcParams['ytick.color'] = '#707070'

# 1. Vector Field F(x, y) = <-y, x>
def vector_field(X, Y):
    return -Y, X

# 2. Curve (Ellipse Path)
def parametric_curve(t):
    return np.cos(t), 2*np.sin(t)

a, b = 0, 2*np.pi
t_values = np.linspace(a, b, 800)  # 600 steps for fine granularity
x_all, y_all = parametric_curve(t_values)

# --- CALCULATIONS ---
dx, dy = np.diff(x_all), np.diff(y_all)
ds = np.hypot(dx, dy)
arc_lengths = np.zeros_like(t_values)
arc_lengths[1:] = np.cumsum(ds)

T_x_all, T_y_all = np.zeros_like(t_values), np.zeros_like(t_values)
T_x_all[:-1], T_y_all[:-1] = dx / ds, dy / ds
T_x_all[-1], T_y_all[-1] = T_x_all[-2], T_y_all[-2]
N_x_all, N_y_all = T_y_all, -T_x_all

U_curve, V_curve = vector_field(x_all, y_all)
f_work_all = (U_curve * T_x_all) + (V_curve * T_y_all)
f_flux_all = (U_curve * N_x_all) + (V_curve * N_y_all)

# --- PRE-COMPUTE SHADING VERTS FOR INTERPOLATED POLYGONS ---
work_poly_verts = []
flux_polygons_verts = []
for idx in range(len(t_values)):
    s_curr = arc_lengths[:idx+1]
    
    w_v = np.zeros((len(s_curr) + 2, 2))
    w_v[0] = [s_curr[0], 0]
    w_v[1:-1] = np.column_stack((s_curr, f_work_all[:idx+1]))
    w_v[-1] = [s_curr[-1], 0]
    work_poly_verts.append(w_v)
    
    f_v = np.zeros((len(s_curr) + 2, 2))
    f_v[0] = [s_curr[0], 0]
    f_v[1:-1] = np.column_stack((s_curr, f_flux_all[:idx+1]))
    f_v[-1] = [s_curr[-1], 0]
    flux_polygons_verts.append(f_v)

# 3. Figure Grid
fig = plt.figure(figsize=(12, 10), facecolor='#121212')
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2) 
ax2 = plt.subplot2grid((2, 2), (1, 0))            
ax3 = plt.subplot2grid((2, 2), (1, 1))            

plt.subplots_adjust(hspace=0.35, wspace=0.25, top=0.95, bottom=0.08)

for sub_ax in [ax1, ax2, ax3]:
    sub_ax.set_facecolor('#1E1E1E')
    sub_ax.grid(True, linestyle='--', color='#2D2D2D', alpha=0.5)
    for s in sub_ax.spines.values(): 
        s.set_color('#333333')

# --- AXIS 1: Geometry Tracking ---
X_mesh, Y_mesh = np.meshgrid(np.linspace(-4.5, 4.5, 15), np.linspace(-3.5, 3.5, 15))
U_mesh, V_mesh = vector_field(X_mesh, Y_mesh)
ax1.quiver(X_mesh, Y_mesh, U_mesh, V_mesh, color='#D4AF37', alpha=0.2, 
           width=0.0025, headwidth=3, headlength=4, headaxislength=3.5)
ax1.plot(x_all, y_all, color='#FFFFFF', linestyle='-', linewidth=1.0, alpha=0.15)

curve_line, = ax1.plot(x_all[:1], y_all[:1], color='#CCCCCC', linewidth=2.5, label="Curve r(t)")
moving_dot, = ax1.plot([x_all[0]], [y_all[0]], 'o', color='#CCCCCC', markersize=8)

tangent_arrow = ax1.quiver(x_all[0], y_all[0], T_x_all[0], T_y_all[0], angles='xy', scale_units='xy', scale=1, color='#E74C3C', 
                          width=0.0035, headwidth=3.5, headlength=4.5, headaxislength=4, label="Tangent T")
normal_arrow = ax1.quiver(x_all[0], y_all[0], N_x_all[0], N_y_all[0], angles='xy', scale_units='xy', scale=1, color='#3498DB', 
                          width=0.0035, headwidth=3.5, headlength=4.5, headaxislength=4, label="Normal N")

ax1.axis('equal')
ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-3.5, 3.5)
ax1.axhline(0, color='#555555', linewidth=0.5, alpha=0.3)
ax1.axvline(0, color='#555555', linewidth=0.5, alpha=0.3)
ax1.legend(loc='upper right', facecolor='#121212', edgecolor='#333333')

math_text_box = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=10, color='#E0E0E0',
                         verticalalignment='top', bbox=dict(facecolor='#121212', alpha=0.85, edgecolor='#333333', boxstyle='round,pad=0.5'))

# --- AXIS 2: Work Plot ---
ax2.plot(arc_lengths, f_work_all, color='#FFFFFF', linestyle='-', linewidth=1.0, alpha=0.2)
work_profile_line, = ax2.plot(arc_lengths[:1], f_work_all[:1], color='#E74C3C', linewidth=2.5)
work_dot, = ax2.plot([arc_lengths[0]], [f_work_all[0]], 'o', color='#E74C3C', markersize=6)
work_fill_poly = ax2.fill(work_poly_verts[0][:, 0], work_poly_verts[0][:, 1], facecolor='#E74C3C', alpha=0.25)[0]

ax2.set_xlim(0, np.max(arc_lengths))
ax2.set_ylim(np.min(f_work_all)-0.5, np.max(f_work_all)+0.5)
ax2.axhline(0, color='#555555', linewidth=0.8, alpha=0.5)
ax2.set_title(r"Flow Integrand: $f_{flow}(s) = \vec{F}(\vec{R}(s)) \cdot \hat{T}(s)$", fontsize=11, fontweight='bold', color='#E0E0E0')
ax2.set_xlabel("Arc Length (s)")

# --- AXIS 3: Flux Plot ---
ax3.plot(arc_lengths, f_flux_all, color='#FFFFFF', linestyle='-', linewidth=1.0, alpha=0.2)
flux_profile_line, = ax3.plot(arc_lengths[:1], f_flux_all[:1], color='#3498DB', linewidth=2.5)
flux_dot, = ax3.plot([arc_lengths[0]], [f_flux_all[0]], 'o', color='#3498DB', markersize=6)
flux_fill_poly = ax3.fill(flux_polygons_verts[0][:, 0], flux_polygons_verts[0][:, 1], facecolor='#3498DB', alpha=0.25)[0]

ax3.set_xlim(0, np.max(arc_lengths))
ax3.set_ylim(np.min(f_flux_all)-0.5, np.max(f_flux_all)+0.5)
ax3.axhline(0, color='#555555', linewidth=0.8, alpha=0.5)
ax3.set_title(r"Flux Integrand: $f_{flux}(s) = \vec{F}(\vec{R}(s)) \cdot \hat{N}(s)$", fontsize=11, fontweight='bold', color='#E0E0E0')
ax3.set_xlabel("Arc Length (s)")

# Global Application Control State Dictionary
state = {
    'is_dragging': False,
    'current_idx': 0,
    'is_playing': False,
    'step_speed': 3
}

def update_artists(idx):
    state['current_idx'] = idx
    s_curr = arc_lengths[:idx+1]
    curr_t = t_values[idx]
    curr_s = arc_lengths[idx]
    curr_x = x_all[idx]
    curr_y = y_all[idx]
    curr_u = U_curve[idx]
    curr_v = V_curve[idx]
    
    # Push updated coordinates directly to artists without redrawing the entire axes canvas
    curve_line.set_data(x_all[:idx+1], y_all[:idx+1])
    moving_dot.set_data([curr_x], [curr_y])
    tangent_arrow.set_offsets([curr_x, curr_y])
    tangent_arrow.set_UVC(T_x_all[idx], T_y_all[idx])
    normal_arrow.set_offsets([curr_x, curr_y])
    normal_arrow.set_UVC(N_x_all[idx], N_y_all[idx])
    
    math_text_box.set_text(
        rf"$\mathbf{{Vector\ Field:}}$" "\n"
        rf"$\vec{{F}}(x,y) = \langle -y, x \rangle = \langle {curr_u:+.2f}, {curr_v:+.2f} \rangle$" "\n\n"
        rf"$\mathbf{{Parametric\ Curve:}}$" "\n"
        rf"$\vec{{r}}(t) = \langle \cos(t), 2\sin(t) \rangle = \langle {curr_x:.2f}, {curr_y:.2f} \rangle$ at $t = {curr_t:.2f}$" "\n\n"
        rf"$\mathbf{{Arc\ Length\ Linear\ Re-parameterization:}}$" "\n"
        rf"$\vec{{R}}(s) = \langle {curr_x:.2f}, {curr_y:.2f} \rangle$ at distance $s = {curr_s:.2f}$"
    )
    
    work_profile_line.set_data(s_curr, f_work_all[:idx+1])
    work_dot.set_data([curr_s], [f_work_all[idx]])
    flux_profile_line.set_data(s_curr, f_flux_all[:idx+1])
    flux_dot.set_data([curr_s], [f_flux_all[idx]])
    
    work_fill_poly.set_xy(work_poly_verts[idx])
    flux_fill_poly.set_xy(flux_polygons_verts[idx])
    
    mode_str = "Automatic" if state['is_playing'] else "Manual"
    ax1.set_title(f"Line Integrals of Vector Fields  |  Mode: {mode_str}  |  [Space] Play/Pause", fontsize=12, fontweight='bold', color='#E0E0E0')
    
    return curve_line, moving_dot, tangent_arrow, normal_arrow, work_profile_line, work_dot, flux_profile_line, flux_dot, math_text_box, work_fill_poly, flux_fill_poly

# --- HIGH-PERFORMANCE BLITTING FRAME SEQUENCER ---
def frame_generator():
    while True:
        if state['is_playing']:
            state['current_idx'] = (state['current_idx'] + state['step_speed']) % len(t_values)
        yield state['current_idx']

# --- INTERACTIVE DRAG EVENT HANDLERS ---
def on_press(event):
    if event.inaxes == ax1 and not state['is_playing']:
        distances = np.hypot(x_all - event.xdata, y_all - event.ydata)
        closest_idx = np.argmin(distances)
        if distances[closest_idx] < 0.5:
            state['is_dragging'] = True
            update_artists(closest_idx)
            fig.canvas.draw_idle()

def on_motion(event):
    if state['is_dragging'] and event.inaxes == ax1 and event.xdata is not None and event.ydata is not None:
        distances = np.hypot(x_all - event.xdata, y_all - event.ydata)
        closest_idx = np.argmin(distances)
        update_artists(closest_idx)
        fig.canvas.draw_idle()

def on_release(event):
    state['is_dragging'] = False

# Keyboard Hook for Dual Mode Play/Pause Toggle
def on_key(event):
    if event.key == ' ':
        state['is_playing'] = not state['is_playing']
        if state['is_playing']:
            state['is_dragging'] = False  
            ani.resume()
        else:
            ani.pause()
        update_artists(state['current_idx'])
        fig.canvas.draw_idle()

# Connect interactive event listeners
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('key_press_event', on_key)

# Bind the fast blitting engine sequence loop
ani = FuncAnimation(fig, update_artists, frames=frame_generator, interval=16, blit=True, cache_frame_data=False)
ani.pause()  # Start in Manual Drag mode

update_artists(0)

try:
    fig.canvas.manager.window.raise_()
except Exception:
    pass

plt.show(block=True)
