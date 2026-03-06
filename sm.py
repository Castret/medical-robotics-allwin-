import time
import browserbotics as bb

# ============================================================
#  HOSPITAL ENVIRONMENT SIMULATION  v5
#  - No ceiling slabs (open top so interior is visible)
#  - No brick floor (plain ground plane only)
#  - All interior details preserved
# ============================================================

bb.setGravity(0, 0, -9.8)
bb.setRealtime(True)

ROT = [0, 0, 0, 1]

# ============================================================
# PRIMITIVE BUILDERS
# ============================================================

def make_box(pos, size, rgba, name="b"):
    r, g, b, a = rgba
    sx, sy, sz = size
    urdf = f"""<?xml version="1.0"?>
<robot name="{name}">
  <link name="base">
    <visual>
      <geometry><box size="{sx} {sy} {sz}"/></geometry>
      <material name="m"><color rgba="{r} {g} {b} {a}"/></material>
    </visual>
    <collision>
      <geometry><box size="{sx} {sy} {sz}"/></geometry>
    </collision>
    <inertial>
      <mass value="0"/>
      <inertia ixx="0" ixy="0" ixz="0" iyy="0" iyz="0" izz="0"/>
    </inertial>
  </link>
</robot>"""
    return bb.loadURDFString(urdf, position=pos, rotation=ROT, fixedBase=True)


def make_cylinder(pos, radius, length, rgba, name="c"):
    r, g, b, a = rgba
    urdf = f"""<?xml version="1.0"?>
<robot name="{name}">
  <link name="base">
    <visual>
      <geometry><cylinder radius="{radius}" length="{length}"/></geometry>
      <material name="m"><color rgba="{r} {g} {b} {a}"/></material>
    </visual>
    <collision>
      <geometry><cylinder radius="{radius}" length="{length}"/></geometry>
    </collision>
    <inertial>
      <mass value="0"/>
      <inertia ixx="0" ixy="0" ixz="0" iyy="0" iyz="0" izz="0"/>
    </inertial>
  </link>
</robot>"""
    return bb.loadURDFString(urdf, position=pos, rotation=ROT, fixedBase=True)


def make_sphere(pos, radius, rgba, name="s"):
    r, g, b, a = rgba
    urdf = f"""<?xml version="1.0"?>
<robot name="{name}">
  <link name="base">
    <visual>
      <geometry><sphere radius="{radius}"/></geometry>
      <material name="m"><color rgba="{r} {g} {b} {a}"/></material>
    </visual>
    <inertial>
      <mass value="0"/>
      <inertia ixx="0" ixy="0" ixz="0" iyy="0" iyz="0" izz="0"/>
    </inertial>
  </link>
</robot>"""
    return bb.loadURDFString(urdf, position=pos, rotation=ROT, fixedBase=True)


# ============================================================
# GROUND PLANE  (plain flat surface, no bricks)
# ============================================================
make_box([8.0, 8.0, -0.05], [80.0, 50.0, 0.10], [0.55, 0.55, 0.55, 1], "ground")

# ============================================================
# COLOURS
# ============================================================
WALL      = [0.93, 0.93, 0.93, 1.0]
CONC      = [0.60, 0.60, 0.62, 1.0]
FLOOR_OT  = [0.78, 0.92, 0.78, 1.0]
FLOOR_W   = [0.85, 0.88, 0.95, 1.0]
FLOOR_SC  = [0.80, 0.86, 0.94, 1.0]
BED       = [0.98, 0.98, 1.00, 1.0]
PILLOW    = [0.75, 0.80, 1.00, 1.0]
STEEL     = [0.68, 0.70, 0.74, 1.0]
STEEL_D   = [0.45, 0.47, 0.52, 1.0]
OT_GRN    = [0.40, 0.78, 0.48, 1.0]
OT_SHEET  = [0.55, 0.85, 0.60, 1.0]
MRI_BODY  = [0.18, 0.38, 0.80, 1.0]
MRI_TRIM  = [0.10, 0.22, 0.55, 1.0]
MRI_BORE  = [0.05, 0.05, 0.10, 1.0]
CT_BODY   = [0.82, 0.84, 0.88, 1.0]
CT_RING   = [0.48, 0.60, 0.72, 1.0]
DARK      = [0.07, 0.07, 0.10, 1.0]
SCREEN    = [0.05, 0.30, 0.55, 1.0]
DOOR      = [0.48, 0.30, 0.14, 1.0]
LIGHT     = [1.00, 1.00, 0.85, 1.0]
SIGN_W    = [0.20, 0.55, 0.95, 1.0]
SIGN_OT   = [0.85, 0.25, 0.25, 1.0]
SIGN_SC   = [0.15, 0.55, 0.35, 1.0]
CHAIR     = [0.30, 0.50, 0.75, 1.0]
WOOD      = [0.68, 0.52, 0.32, 1.0]
IV_BAG    = [0.35, 0.78, 0.40, 0.85]
GLASS     = [0.55, 0.75, 0.90, 0.30]


# ============================================================
# ROOM WALLS  — no ceiling, just 4 walls + floor slab
# ============================================================
def room_walls(ox, oy, oz, W, D, H, floor_color, prefix,
               door_width=1.4, door_height=2.2):
    t = 0.22

    # Floor slab
    make_box([ox+W/2, oy+D/2, oz+0.06], [W, D, 0.12], floor_color, f"{prefix}_fl")

    # South wall with door gap
    seg = (W - door_width) / 2
    make_box([ox+seg/2,     oy, oz+H/2], [seg, t, H], WALL, f"{prefix}_sw1")
    make_box([ox+W-seg/2,   oy, oz+H/2], [seg, t, H], WALL, f"{prefix}_sw2")
    make_box([ox+W/2, oy, oz+door_height+(H-door_height)/2],
             [door_width, t, H-door_height], WALL, f"{prefix}_slin")
    make_box([ox+W/2, oy+t/2, oz+door_height/2],
             [door_width-0.05, 0.06, door_height], DOOR, f"{prefix}_door")

    # North / West / East walls (full height, no ceiling)
    make_box([ox+W/2, oy+D,   oz+H/2], [W, t, H], WALL, f"{prefix}_nw")
    make_box([ox,     oy+D/2, oz+H/2], [t, D, H], WALL, f"{prefix}_ww")
    make_box([ox+W,   oy+D/2, oz+H/2], [t, D, H], WALL, f"{prefix}_ew")


# ============================================================
# DEPARTMENT 1 – OPERATION THEATRE  (ground floor)
#   x=0..12, y=0..14, z=0,  H=4.0 m
# ============================================================
def build_operation_theatre():
    ox, oy, oz = 0.0, 0.0, 0.0
    W, D, H = 12.0, 14.0, 4.0

    room_walls(ox, oy, oz, W, D, H, FLOOR_OT, "ot",
               door_width=1.6, door_height=2.4)

    cx, cy = ox+W/2, oy+D/2

    # ── OT Table ─────────────────────────────────────────
    make_box([cx, cy, oz+0.40],          [0.30, 0.30, 0.80], STEEL_D,  "ot_ped")
    make_box([cx, cy, oz+0.88],          [0.70, 2.00, 0.08], STEEL,    "ot_platform")
    make_box([cx, cy, oz+0.95],          [0.65, 1.90, 0.08], OT_GRN,   "ot_mattress")
    make_box([cx, cy-0.20, oz+1.02],     [0.62, 1.50, 0.03], OT_SHEET, "ot_sheet")
    make_box([cx, cy+0.85, oz+1.00],     [0.40, 0.25, 0.06], [0.9,0.9,0.9,1], "ot_hrest")
    make_box([cx-0.55, cy, oz+0.92],     [0.20, 1.40, 0.04], STEEL,    "ot_armL")
    make_box([cx+0.55, cy, oz+0.92],     [0.20, 1.40, 0.04], STEEL,    "ot_armR")
    for dx, dy in [(-0.45,-1.0),(0.45,-1.0),(-0.45,1.0),(0.45,1.0)]:
        make_cylinder([cx+dx, cy+dy, oz+0.44], 0.04, 0.88, STEEL_D, "ot_tleg")

    # ── IV Pole ───────────────────────────────────────────
    make_cylinder([cx-0.80, cy+0.80, oz+1.50], 0.025, 2.0, STEEL,  "ot_ivpole")
    make_sphere([cx-0.80, cy+0.80, oz+2.52],   0.07,       IV_BAG,  "ot_ivbag")

    # ── Overhead Surgical Light ───────────────────────────
    make_box([cx, cy, oz+H-0.18],          [1.80, 0.12, 0.12], STEEL_D, "ot_rail")
    make_cylinder([cx, cy, oz+H-0.55],     0.04, 0.70, STEEL_D,         "ot_arm1")
    make_cylinder([cx, cy, oz+H-1.00],     0.45, 0.18, LIGHT,           "ot_lamp_big")
    make_cylinder([cx, cy, oz+H-1.00],     0.38, 0.22, [1,1,0.95,0.9],  "ot_lamp_inner")
    make_cylinder([cx+0.80, cy-0.30, oz+H-1.10], 0.28, 0.14, LIGHT,    "ot_lamp2")

    # ── Anaesthesia Machine ───────────────────────────────
    ax, ay = cx-2.0, cy-1.0
    make_box([ax, ay, oz+0.90],          [0.65, 0.50, 1.80], [0.75,0.75,0.88,1], "ot_an_body")
    make_box([ax, ay-0.22, oz+1.72],     [0.55, 0.08, 0.65], SCREEN,             "ot_an_screen")
    make_box([ax, ay+0.22, oz+0.62],     [0.50, 0.06, 0.40], STEEL_D,            "ot_an_ctrl")
    make_cylinder([ax-0.25, ay+0.28, oz+0.70], 0.07, 1.0, [0.3,0.6,0.3,1], "ot_cyl_O2")
    make_cylinder([ax+0.25, ay+0.28, oz+0.70], 0.07, 1.0, [0.7,0.7,0.2,1], "ot_cyl_N2")

    # ── Instrument Trolley ────────────────────────────────
    tx, ty = cx+1.8, cy+0.6
    for dx, dy in [(-0.35,-0.22),(0.35,-0.22),(-0.35,0.22),(0.35,0.22)]:
        make_cylinder([tx+dx, ty+dy, oz+0.42], 0.022, 0.84, STEEL_D, "ot_tleg")
    make_box([tx, ty, oz+0.30], [0.75, 0.50, 0.04], STEEL, "ot_tshelf_lo")
    make_box([tx, ty, oz+0.86], [0.75, 0.50, 0.04], STEEL, "ot_tshelf_hi")
    for ix, iy in [(-0.25,0),(-0.08,0),(0.08,0),(0.25,0)]:
        make_box([tx+ix, ty+iy, oz+0.92], [0.07, 0.30, 0.04], [0.85,0.85,0.88,1], "ot_instr")

    # ── Vitals Monitor ────────────────────────────────────
    make_cylinder([cx+2.2, cy-1.2, oz+0.80], 0.035, 1.60, STEEL_D,       "ot_mon_pole")
    make_box([cx+2.46, cy-1.2, oz+1.65],     [0.52, 0.06, 0.36], DARK,   "ot_monitor")
    make_box([cx+2.46, cy-1.2, oz+1.65],     [0.44, 0.02, 0.28], SCREEN, "ot_mon_scr")

    # ── Scrub Sink ────────────────────────────────────────
    make_box([ox+0.55, oy+D-0.80, oz+0.50],  [0.80, 0.55, 1.00], [0.80,0.82,0.90,1], "ot_sink")
    make_cylinder([ox+0.55, oy+D-0.55, oz+1.18], 0.02, 0.25, STEEL, "ot_tap")

    # ── Electrosurgical Unit ──────────────────────────────
    make_box([cx+2.0, cy+1.0, oz+0.55],      [0.50, 0.38, 1.10], [0.6,0.6,0.7,1], "ot_esu")
    make_box([cx+2.0, cy+0.82, oz+0.95],     [0.42, 0.06, 0.35], SCREEN,          "ot_esu_scr")

    # ── OT Sign (on south wall interior) ─────────────────
    make_box([cx, oy+0.14, oz+3.20], [2.8, 0.08, 0.55], SIGN_OT, "ot_sign")


# ============================================================
# DEPARTMENT 2 – NORMAL WARD  (stacked on top of OT)
#   Same X/Y footprint.  oz = 4.12 (on top of OT)  H=3.6 m
# ============================================================
def build_normal_ward():
    oz = 4.12
    ox, oy = 0.0, 0.0
    W, D, H = 12.0, 14.0, 3.6

    room_walls(ox, oy, oz, W, D, H, FLOOR_W, "wd",
               door_width=1.4, door_height=2.2)

    # ── 5 Beds ────────────────────────────────────────────
    bed_positions = [
        [ox+2.0, oy+2.0],
        [ox+2.0, oy+5.5],
        [ox+2.0, oy+9.0],
        [ox+9.0, oy+3.5],
        [ox+9.0, oy+8.0],
    ]
    for i, (bx, by) in enumerate(bed_positions):
        bz = oz
        make_box([bx, by, bz+0.18],       [1.95, 2.05, 0.36], STEEL_D,  f"w_frame{i}")
        make_box([bx, by, bz+0.42],       [1.80, 1.95, 0.20], BED,      f"w_mat{i}")
        make_box([bx, by+0.82, bz+0.55],  [0.55, 0.38, 0.14], PILLOW,   f"w_pil{i}")
        make_box([bx, by-0.20, bz+0.56],  [1.70, 1.20, 0.08], [0.75,0.80,0.92,1], f"w_blank{i}")
        make_box([bx, by+1.05, bz+0.65],  [1.85, 0.08, 0.70], STEEL,    f"w_hbrd{i}")
        make_box([bx, by-1.05, bz+0.55],  [1.85, 0.08, 0.40], STEEL,    f"w_fbrd{i}")
        for dx, dy in [(-0.88,-0.98),(0.88,-0.98),(-0.88,0.98),(0.88,0.98)]:
            make_cylinder([bx+dx, by+dy, bz+0.09], 0.04, 0.18, STEEL_D, f"w_leg{i}")
        make_box([bx+1.30, by+0.40, bz+0.40],  [0.48, 0.48, 0.80], WOOD,   f"w_tbl{i}")
        make_box([bx+1.30, by+0.40, bz+0.82],  [0.44, 0.44, 0.06], STEEL,  f"w_tbl_top{i}")
        make_cylinder([bx+1.30, by-0.55, bz+1.00], 0.025, 2.00, STEEL,     f"w_ivpole{i}")
        make_sphere([bx+1.30, by-0.55, bz+2.02],   0.075,          IV_BAG,  f"w_ivbag{i}")
        make_box([bx-1.00, by+0.50, bz+0.55],  [0.10, 0.06, 0.18], [0.85,0.30,0.25,1], f"w_callbtn{i}")

    # ── Nurse Station ─────────────────────────────────────
    nx, ny = ox+W/2, oy+D-1.80
    make_box([nx, ny, oz+0.55],          [3.60, 0.90, 1.10], WOOD,   "w_desk")
    make_box([nx-0.80, ny-0.38, oz+1.55],[0.55, 0.06, 0.38], SCREEN, "w_mon1")
    make_box([nx+0.80, ny-0.38, oz+1.55],[0.55, 0.06, 0.38], SCREEN, "w_mon2")
    make_box([nx, ny+0.70, oz+0.24],     [0.46, 0.46, 0.48], CHAIR,  "w_chair_seat")
    make_cylinder([nx, ny+0.70, oz+0.12], 0.04, 0.24, STEEL_D, "w_chair_pole")

    # ── Windows (north wall) ──────────────────────────────
    for wx_pos in [ox+3.0, ox+9.0]:
        make_box([wx_pos, oy+D-0.08, oz+1.60], [1.80, 0.12, 1.20], GLASS,  "w_win")
        make_box([wx_pos, oy+D-0.08, oz+1.60], [1.84, 0.06, 1.24], STEEL,  "w_winframe")

    # ── Ward Sign ─────────────────────────────────────────
    make_box([ox+W/2, oy+0.14, oz+3.00], [2.8, 0.08, 0.55], SIGN_W, "wd_sign")

    # ── Staircase shaft (exterior west side) ──────────────
    make_box([ox-0.30, oy+D/2, oz/2], [0.60, 3.0, oz], CONC, "stair_shaft")


# ============================================================
# DEPARTMENT 3 – SCAN CENTRE  (ground floor, separate)
#   x=16..32, y=0..16,  H=4.5 m
# ============================================================
def build_scan_centre():
    ox, oy, oz = 16.0, 0.0, 0.0
    W, D, H = 16.0, 16.0, 4.5

    room_walls(ox, oy, oz, W, D, H, FLOOR_SC, "sc",
               door_width=1.6, door_height=2.4)

    # Internal divider: control room (south) vs scan room (north)
    div_y = oy + 6.0
    t = 0.22
    make_box([ox+W/2, div_y, oz+H/2], [W, t, H], [0.82,0.86,0.90,1], "sc_div")

    # Lead-glass window
    make_box([ox+4.0, div_y, oz+1.60], [3.20, 0.16, 1.40], GLASS, "sc_lglass")
    make_box([ox+4.0, div_y, oz+1.60], [3.26, 0.10, 1.46], STEEL, "sc_lglass_frame")

    # Control room door
    make_box([ox+W-2.0, div_y+t/2, oz+1.20], [1.20, 0.07, 2.40], DOOR, "sc_ctrl_door")

    # ── MRI SCANNER ───────────────────────────────────────
    mx, my = ox+5.5, oy+11.0

    make_box([mx, my, oz+1.20],          [2.80, 2.80, 2.40], [0.88,0.90,0.94,1], "mri_shell")
    make_box([mx, my, oz+1.20],          [2.50, 1.30, 2.20], MRI_BODY,            "mri_magX")
    make_box([mx, my, oz+1.20],          [1.30, 2.50, 2.20], MRI_BODY,            "mri_magY")
    make_box([mx, my, oz+1.20],          [2.90, 0.85, 0.85], MRI_BORE,            "mri_bore")
    make_box([mx-1.38, my, oz+1.20],     [0.06, 0.92, 0.92], MRI_TRIM,            "mri_boreL")
    make_box([mx+1.38, my, oz+1.20],     [0.06, 0.92, 0.92], MRI_TRIM,            "mri_boreR")
    make_box([mx, my, oz+2.42],          [1.60, 0.80, 0.18], MRI_TRIM,            "mri_top_coil")
    make_box([mx-1.26, my-1.20, oz+1.20],[0.06, 0.55, 1.60], [0.75,0.78,0.84,1], "mri_front")
    make_box([mx-1.28, my-1.20, oz+2.10],[0.04, 0.50, 0.08], [0.2,0.8,0.3,1],    "mri_status")

    # Patient table
    make_box([mx, my, oz+0.86],          [0.72, 2.20, 0.12], [0.90,0.90,0.94,1], "mri_tbl_top")
    make_box([mx, my+0.60, oz+0.44],     [0.45, 0.45, 0.88], STEEL_D,            "mri_tbl_col")
    make_box([mx, my+0.60, oz+0.07],     [0.80, 1.20, 0.14], STEEL,              "mri_tbl_base")
    make_box([mx, my-0.10, oz+0.96],     [0.60, 1.80, 0.10], BED,                "mri_tbl_mat")
    make_box([mx, my-1.05, oz+1.00],     [0.38, 0.28, 0.28], MRI_TRIM,           "mri_head_coil")

    # ── CT SCANNER ────────────────────────────────────────
    ctx, cty = ox+12.0, oy+11.0

    make_box([ctx, cty, oz+1.00],        [1.90, 1.70, 2.00], CT_BODY,            "ct_outer")
    make_box([ctx, cty, oz+1.00],        [1.95, 1.10, 1.10], CT_RING,            "ct_ringX")
    make_box([ctx, cty, oz+1.00],        [1.10, 1.95, 1.10], CT_RING,            "ct_ringY")
    make_box([ctx, cty, oz+1.00],        [2.00, 0.68, 0.68], MRI_BORE,           "ct_bore")
    make_box([ctx-0.96, cty, oz+1.00],   [0.05, 0.75, 0.75], CT_RING,            "ct_boreL")
    make_box([ctx+0.96, cty, oz+1.00],   [0.05, 0.75, 0.75], CT_RING,            "ct_boreR")
    make_box([ctx-0.96, cty-0.80, oz+1.00],[0.05,0.45,1.80], CT_BODY,            "ct_face")
    make_box([ctx-0.98, cty-0.80, oz+1.70],[0.04,0.30,0.22], SCREEN,             "ct_disp")

    # CT patient table
    make_box([ctx, cty, oz+0.84],        [0.55, 2.40, 0.10], [0.88,0.88,0.92,1], "ct_tbl_top")
    make_box([ctx, cty+0.70, oz+0.44],   [0.38, 0.55, 0.88], STEEL_D,            "ct_tbl_col")
    make_box([ctx, cty+0.70, oz+0.07],   [0.65, 1.10, 0.14], STEEL,              "ct_tbl_base")
    make_box([ctx, cty-0.10, oz+0.92],   [0.48, 1.80, 0.08], BED,                "ct_tbl_mat")

    # ── Control Console ───────────────────────────────────
    ccx, ccy = ox+5.5, oy+3.5
    make_box([ccx, ccy, oz+0.56],            [3.80, 0.85, 1.12], [0.22,0.25,0.30,1], "sc_desk")
    for i, mx_off in enumerate([-1.15, 0.0, 1.15]):
        make_box([ccx+mx_off, ccy-0.40, oz+1.46], [0.65, 0.06, 0.42], DARK,   f"sc_mon{i}")
        make_box([ccx+mx_off, ccy-0.40, oz+1.46], [0.58, 0.03, 0.35], SCREEN, f"sc_monscr{i}")
    make_box([ccx, ccy-0.35, oz+1.18],       [1.20, 0.08, 0.04], [0.3,0.3,0.35,1], "sc_kbd")

    # ── Waiting Chairs ────────────────────────────────────
    for i in range(5):
        sx = ox + 1.0 + i*2.8
        sy = oy + 1.6
        make_box([sx, sy,      oz+0.24], [0.72, 0.72, 0.48], CHAIR, f"sc_cseat{i}")
        make_box([sx, sy-0.34, oz+0.58], [0.72, 0.10, 0.60], CHAIR, f"sc_cback{i}")
        for dx in [-0.32, 0.32]:
            make_cylinder([sx+dx, sy-0.02, oz+0.12], 0.03, 0.24, STEEL_D, f"sc_cleg{i}")

    # ── Reception Desk ────────────────────────────────────
    rx, ry = ox+W-3.5, oy+3.0
    make_box([rx, ry, oz+0.56],       [3.20, 0.85, 1.12], WOOD,   "sc_rec_desk")
    make_box([rx, ry-0.40, oz+1.46],  [0.65, 0.06, 0.42], DARK,   "sc_rec_mon")
    make_box([rx, ry-0.40, oz+1.46],  [0.58, 0.03, 0.35], SCREEN, "sc_rec_scr")

    # ── Scan Centre Sign ──────────────────────────────────
    make_box([ox+W/2, oy+0.14, oz+3.80], [3.2, 0.08, 0.55], SIGN_SC, "sc_sign")


# ============================================================
# CORRIDOR  (connects OT/Ward block to Scan Centre)
# ============================================================
def build_corridor():
    make_box([12.50, -1.20, 0.06], [9.0, 2.40, 0.12], [0.68,0.68,0.70,1], "corr_fl")
    make_box([12.50, -2.42, 1.20], [9.0, 0.22, 2.40], WALL, "corr_wS")
    make_box([12.50,  0.02, 1.20], [9.0, 0.22, 2.40], WALL, "corr_wN")
    for xi in range(9):
        x = 8.5 + xi * 0.9
        make_box([x, -1.20, 0.13], [0.12, 2.00, 0.02], [0.90,0.85,0.15,1], "corr_stripe")


# ============================================================
# BUILD ALL
# ============================================================
build_operation_theatre()
build_normal_ward()
build_scan_centre()
build_corridor()

# ============================================================
# DEBUG LABELS
# ============================================================
bb.createDebugText("OPERATION THEATRE", position=[6.0,  -0.8, 0.6],  color=[0.9, 0.3, 0.3])
bb.createDebugText("NORMAL WARD (L2)",  position=[6.0,  -0.8, 4.8],  color=[0.3, 0.5, 1.0])
bb.createDebugText("SCAN CENTRE",       position=[24.0, -0.8, 0.6],  color=[0.2, 0.8, 0.4])
bb.createDebugText("MRI",               position=[21.5, 11.0, 2.8],  color=[0.4, 0.7, 1.0])
bb.createDebugText("CT",                position=[28.0, 11.0, 2.8],  color=[0.4, 0.7, 1.0])

# ============================================================
# DEBUG UI
# ============================================================
bb.addDebugSlider('mri_table_pos', minValue=0.0, maxValue=1.8)
bb.addDebugButton('reset_patient')

# ============================================================
# PATIENT  (inline URDF)
# ============================================================
patient_urdf = """<?xml version="1.0"?>
<robot name="patient">
  <link name="base">
    <visual>
      <geometry><box size="0.38 0.22 0.88"/></geometry>
      <material name="m"><color rgba="0.90 0.74 0.60 1"/></material>
    </visual>
    <collision>
      <geometry><box size="0.38 0.22 0.88"/></geometry>
    </collision>
    <inertial>
      <mass value="70"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="0.5"/>
    </inertial>
  </link>
</robot>"""

patient_start = [6.0, -1.5, 0.50]
patient = bb.loadURDFString(patient_urdf, position=patient_start, rotation=ROT)
reset_count = 0

# ============================================================
# MAIN LOOP
# ============================================================
while True:
    new_reset = bb.readDebugParameter('reset_patient')
    if new_reset != reset_count:
        bb.resetBasePose(patient, patient_start, [0, 0, 0, 1])
        reset_count = new_reset
    time.sleep(0.05)
