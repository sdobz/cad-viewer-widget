import uuid
from ._version import __version__

from .widget import AnimationTrack, CadViewer, get_viewer_by_id, get_viewers_by_id

from .utils import display_args, viewer_args


def _normalize_cad_width(cad_width):
    if cad_width is not None and cad_width < 320:
        cad_width = 320
        print("`cad_width` cannot be smaller than 320, setting to 320")
    return cad_width


def open_viewer(
    title=None,
    cad_width=800,
    tree_width=250,
    height=600,
    aspect_ratio=0.75,
    theme="browser",
    glass=True,
    tools=True,
    pinning=True,
):
    cad_width = _normalize_cad_width(cad_width)

    id_ = str(uuid.uuid4())

    viewer = CadViewer(
        title=None if title in (None, "") else title,
        cad_width=cad_width,
        tree_width=tree_width,
        aspect_ratio=aspect_ratio,
        height=height,
        theme=theme,
        glass=glass,
        tools=tools,
        pinning=pinning,
        id_=id_,
    )

    viewer.register_viewer()
    return viewer


def show(
    shapes,
    tracks=None,
    #
    # Viewer options
    title=None,
    cad_width=None,
    tree_width=None,
    aspect_ratio=None,
    height=None,
    theme=None,
    glass=None,
    tools=None,
    pinning=None,
    new_tree_behavior=True,
    #
    # render options
    normal_len=None,
    default_edgecolor=None,
    default_opacity=None,
    ambient_intensity=None,
    direct_intensity=None,
    metalness=None,
    roughness=None,
    #
    # add_shapes options
    up=None,
    control=None,
    ortho=None,
    axes=None,
    axes0=None,
    grid=None,
    center_grid=None,
    explode=None,
    ticks=None,
    transparent=None,
    black_edges=None,
    collapse=None,
    reset_camera=None,
    clip_slider_0=None,
    clip_slider_1=None,
    clip_slider_2=None,
    clip_normal_0=None,
    clip_normal_1=None,
    clip_normal_2=None,
    clip_intersection=None,
    clip_planes=None,
    clip_object_colors=None,
    position=None,
    quaternion=None,
    target=None,
    zoom=None,
    zoom_speed=None,
    pan_speed=None,
    rotate_speed=None,
    timeit=None,
    debug=None,
):
    """
    Show CAD objects with the current viewer runtime

    - shapes:            Serialized nested tessellated shapes

    Valid keywords:

    - UI
        glass:             Use glass mode where tree is an overlay over the cad object (default=True)
        tools:             Show tools (default=True)
        cad_width:         Width of the cad canvas (default=800)
        height:            Height of the cad canvas (default=600)
        tree_width:        Width of the object tree (default=240)
        theme:             Theme "light" or "dark" (default="light")
        pinning:           Allow replacing the CAD View by a canvas screenshot (default=True in cells, else False)
        new_tree_behavior: Whether to  hide the complete shape when clicking on the eye (True, default) or only
                           the faces (False)

    - Viewer
        axes:              Show axes (default=False)
        axes0:             Show axes at (0,0,0) (default=False)
        grid:              Show grid (default=False)
        ortho:             Use orthographic projections (default=True)
        transparent:       Show objects transparent (default=False)
        default_opacity:   Opacity value for transparent objects (default=0.5)
        black_edges:       Show edges in black color (default=False)
        control:           Mouse control use "orbit" control instead of "trackball" control (default="trackball")
        collapse:          "1": collapse all single leaf nodes,
                           "R": expand root only,
                           "C": collapse all nodes,
                           "E"": expand all nodes
                           (default="R"")
        ticks:             Hint for the number of ticks in both directions (default=10)
        center_grid:       Center the grid at the origin or center of mass (default=False)
        up:                Use z-axis ('Z') or y-axis ('Y') as up direction for the camera (default="Z")
        explode:           Turn on explode mode (default=False)

        zoom:              Zoom factor of view (default=1.0)
        position:          Camera position
        quaternion:        Camera orientation as quaternion
        target:            Camera look at target
        reset_camera:      Camera.RESET: Reset camera position, rotation, zoom and target
                           Camera.CENTER: Keep camera position, rotation, zoom, but look at center
                           Camera.KEEP: Keep camera position, rotation, zoom, and target
                           (default=Camera.RESET)
        clip_slider_0:     Setting of clipping slider 0 (default=None)
        clip_slider_1:     Setting of clipping slider 1 (default=None)
        clip_slider_2:     Setting of clipping slider 2 (default=None)
        clip_normal_0:     Setting of clipping normal 0 (default=[-1,0,0])
        clip_normal_1:     Setting of clipping normal 1 (default=[0,-1,0])
        clip_normal_2:     Setting of clipping normal 2 (default=[0,0,-1])
        clip_intersection: Use clipping intersection mode (default=[False])
        clip_planes:       Show clipping plane helpers (default=False)
        clip_object_colors: Use object color for clipping caps (default=False)

        pan_speed:         Speed of mouse panning (default=1)
        rotate_speed:      Speed of mouse rotate (default=1)
        zoom_speed:        Speed of mouse zoom (default=1)

    - Renderer
        default_edgecolor: Default mesh color (default=(128, 128, 128))
        ambient_intensity: Intensity of ambient light (default=1.00)
        direct_intensity:  Intensity of direct light (default=1.10)
        metalness:         Metalness property of the default material (default=0.30)
        roughness:         Roughness property of the default material (default=0.65)

    - Debug
        debug:             Show debug statements to the VS Code browser console (default=False)
        timeit:            Show timing information from level 0-3 (default=False)
    """

    def preset(val, default):
        return default if val is None else val

    kwargs = {}

    kwargs["glass"] = preset(glass, True)
    kwargs["tools"] = preset(tools, True)
    kwargs["height"] = preset(height, 600)
    kwargs["cad_width"] = _normalize_cad_width(preset(cad_width, 800))
    kwargs["tree_width"] = preset(tree_width, 250)
    kwargs["aspect_ratio"] = preset(aspect_ratio, 0.75)

    kwargs["new_tree_behavior"] = preset(new_tree_behavior, True)
    kwargs["theme"] = preset(theme, "browser")
    kwargs["normal_len"] = preset(normal_len, 0)
    kwargs["default_edgecolor"] = preset(default_edgecolor, "#707070")
    kwargs["default_opacity"] = preset(default_opacity, 0.5)
    kwargs["ambient_intensity"] = preset(ambient_intensity, 1.0)
    kwargs["direct_intensity"] = preset(direct_intensity, 1.1)
    kwargs["metalness"] = preset(metalness, 0.3)
    kwargs["roughness"] = preset(roughness, 0.65)
    kwargs["control"] = preset(control, "trackball")
    kwargs["up"] = preset(up, "Z")
    kwargs["ortho"] = preset(ortho, True)
    kwargs["axes"] = preset(axes, False)
    kwargs["axes0"] = preset(axes0, False)
    kwargs["grid"] = preset(grid, [False, False, False])
    kwargs["center_grid"] = preset(center_grid, False)
    kwargs["ticks"] = preset(ticks, 10)
    kwargs["explode"] = preset(explode, False)
    kwargs["transparent"] = preset(transparent, False)
    kwargs["black_edges"] = preset(black_edges, False)
    kwargs["collapse"] = preset(collapse, "R")
    kwargs["reset_camera"] = preset(reset_camera, "reset")
    kwargs["zoom_speed"] = preset(zoom_speed, 0.5)
    kwargs["pan_speed"] = preset(pan_speed, 0.5)
    kwargs["rotate_speed"] = preset(rotate_speed, 1.0)
    kwargs["timeit"] = preset(timeit, False)
    kwargs["debug"] = preset(debug, False)
    if position is not None:
        kwargs["position"] = position
    if quaternion is not None:
        kwargs["quaternion"] = quaternion
    if target is not None:
        kwargs["target"] = target
    if zoom is not None:
        kwargs["zoom"] = zoom
    kwargs["clip_slider_0"] = preset(clip_slider_0, None)
    kwargs["clip_slider_1"] = preset(clip_slider_1, None)
    kwargs["clip_slider_2"] = preset(clip_slider_2, None)
    kwargs["clip_normal_0"] = preset(clip_normal_0, [-1, 0, 0])
    kwargs["clip_normal_1"] = preset(clip_normal_1, [0, -1, 0])
    kwargs["clip_normal_2"] = preset(clip_normal_2, [0, 0, -1])
    kwargs["clip_intersection"] = preset(clip_intersection, False)
    kwargs["clip_planes"] = preset(clip_planes, False)
    kwargs["clip_object_colors"] = preset(clip_object_colors, False)

    viewer = open_viewer(
        title=title,
        pinning=True if pinning is None else pinning,
        **display_args(kwargs),
    )

    viewer.add_shapes(shapes, tracks, **viewer_args(kwargs))
    return viewer
