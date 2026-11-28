# Render recipes (software painter's algorithm; the same ideas port to GPU)

Reference implementation: TempleOS fork `Backend/Lib/View3.HC` and `Gfx.HC`; the game using it: Last Frequency `Src/Fpv.HC`.

1. **Camera.** World x east, y up, z north. Translate by (cam - eye), rotate by yaw about y, then pitch about x; screen x = mid_x + x*F/z, y = mid_y - y*F/z with F about 330 for a 90 degree view across 640 px.
2. **Polygons.** Transform all vertices; if none are in front of the near plane, drop it; otherwise clip against z = near (Sutherland-Hodgman, one plane), project, fill convex polygons by scanline, then draw an ink edge.
3. **Boxes.** Draw only faces whose horizontal normal faces the camera (dot of normal with camera-minus-face-centre); the top only if the eye is above it. Tones: top lit, front mid, sides shade.
4. **Cast shadow.** Sweep the footprint away from the lamp by min(height, 2) * 0.3: one flat parallelogram per edge plus the shifted footprint, drawn first, in a tone that contrasts with the floor.
5. **Round things.** `V3Cyl`: 16 facets; tone per facet by the angle to the lamp (lit, mid, shade; thresholds 0.55 and -0.1); ink only on the silhouette, at each tone change, and round the top. Emissive objects set the lamp to the camera while drawn.
6. **Curved walls.** 48 narrow quads for the base colour and lighting bands; decor (pilasters, arches, mouldings) on a 16-chord lattice. Far segments take the next shade (depth band).
7. **Targets.** Project the 8 corners of every clickable box, clamp z at the near plane, take the 2D bounding box, merge per id (except spread-out objects: one target each), add far to near. Never keep a hand-made hit list.
8. **Windows.** `WindowDraw`: reveal quads (sill, jambs, 8 head strips), glass in two polygons split at the horizon, head triangles, details, mullions, ink at the inner edge.
9. **Order.** Floor, ceiling, walls, halos, flat floor items (rugs, puddles), then upright objects sorted far to near.
10. **Counters.** `v3_npoly`, `v3_nline` per frame; the edge budget test sweeps positions and yaws and prints mean, fewest, most, and time per view.
11. **Keyboard.** Arrows and WASD walk and turn; TAB cycles targets; ENTER uses; the pointer at the window edge turns the head (never when over a target).
