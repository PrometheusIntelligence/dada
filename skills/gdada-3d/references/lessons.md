# 3D lessons (append at the end of every 3D run)

Format: id, what happened, the rule.

**D1 (Last Frequency run 3).** A flat cutaway of a tower read as a picture with nothing to do; the owner asked for first person. A software 3D view of round rooms was built in HolyC in one run. *Rule:* if the owner says "inside", build a space you stand in, not a diagram.
**D2.** Targets found by projecting the drawn boxes matched the picture exactly; a hand-made hit list would have drifted. *Rule:* one geometry list, drawn and projected.
**D3.** The floor was invisible: at 1.6 m eye height a floor object nearer than 2.6 m is below the view. Hatches became ladders with rails. *Rule:* check what is in the frame from the place the player stands, not from above.
**D4.** The first palette gave wall, floor, door and shade of every wooden prop one brown; new props melted into the wall. *Rule:* separate by hue first (warm brick against violet shade, wood against brick).
**D5.** Shadows drawn in the outline colour were invisible. *Rule:* cast shadows get their own tone or sit on a surface that contrasts with it.
**D6.** A dithered light edge and a halftone glow broke the cel style. *Rule:* light is a flat shape with a hard edge.
**D7.** "Too few edges" (owner, run 6): the same scenes at 734 polygons and lines per view looked sparse; adding pilasters, ring beam, cornice, mouldings, blind arches, bevels, furniture structure took it to 1,432 at 34 ms per view under software emulation. *Rule:* measure edges; set a floor; raise it each pass; watch the time.
**D8.** A test returned early because focus was already on the target from a stale layout. *Rule:* tick after placing the camera before any focus loop.
**D9.** Big flat rugs drawn in distance order covered furniture. *Rule:* two passes, flats first.
**D10.** A hanging lantern at the centre of a room filled the screen when the camera passed under it. *Rule:* keep ceiling objects off the walking paths or give them a clearance radius.
