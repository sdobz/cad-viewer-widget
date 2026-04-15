import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Viewer
    """)
    return


@app.cell
def _():
    import numpy as np
    import json
    import time
    import ipywidgets as widgets
    from cad_viewer_widget import AnimationTrack, CadViewer, show, open_viewer, get_sidecar, get_sidecars, close_sidecar, close_sidecars, get_default_sidecar, set_default_sidecar
    from cad_viewer_widget.utils import numpyify
    names = ['b123d_assembly', 'box1', 'boxes', 'dirbox', 'edges', 'faces', 'hexapod', 'orientbox', 'profile4040', 'single_edges', 'torus_knot']
    objects = {}
    states = {}
    for _name in names:
        with open(f'../examples/{_name}.json', 'r') as fd:
            objects[_name] = numpyify(json.load(fd))
    return (
        AnimationTrack,
        close_sidecars,
        get_sidecar,
        get_sidecars,
        names,
        np,
        objects,
        open_viewer,
        set_default_sidecar,
        show,
        time,
        widgets,
    )


@app.cell
def _(open_viewer):
    cv = open_viewer("Test")
    return


@app.cell
def _(objects, show):
    _name = 'boxes'
    cv_1 = show(objects[_name], glass=True, tools=True, grid=(True, False, True), title='CVW 1', anchor='right', height=500, cad_width=700, debug=True)
    return (cv_1,)


@app.cell
def _(cv_1):
    cv_1.status()
    return


@app.cell
def _(cv_1):
    cv_1.widget.id
    return


@app.cell
def _(cv_1):
    (cv_1.widget.selectedShapeIDs, cv_1.widget.activeTool)
    return


@app.cell
def _():
    # theme=OK,
    # glass=OK,
    # tools=OK,
    # pinning=OK,
    #     #
    #     # render options
    # normal_len=OK,
    # default_edgecolor=OK,
    # default_opacity=OK,
    # ambient_intensity=OK,
    # direct_intensity=OK,
    # metalness=OK,
    # roughness=OK,
    #     #
    #     # add_shapes options
    # up=OK,
    # control=OK,
    # ortho=OK,
    # axes=OK,
    # axes0=OK,
    # grid=OK,
    # center_grid=OK,
    # explode=OK,
    # ticks=OK,
    # transparent=OK,
    # black_edges=OK,
    # collapse=OK,
    # reset_camera=OK,
    # clip_slider_0=OK,
    # clip_slider_1=OK,
    # clip_slider_2=OK,
    # clip_normal_0=OK,
    # clip_normal_1=OK,
    # clip_normal_2=OK,
    # clip_intersection=OK,
    # clip_planes=OK,
    # clip_object_colors=OK,
    # position=OK,
    # quaternion=OK,
    # target=OK,
    # zoom=OK,
    # zoom_speed=OK,
    # pan_speed=OK,
    # rotate_speed=OK,
    #     timeit=FAIL,
    # debug=OK,
    return


@app.cell
def _(cv_1):
    (cv_1.widget.cad_width, cv_1.widget.height)
    return


@app.cell
def _(objects, show):
    _name = 'hexapod'
    cv2 = show(objects[_name], title='CVW 2', collapse='1', anchor='split-right', cad_width=1200, glass=True, reset_camera='reset')
    return (cv2,)


@app.cell
def _(get_sidecars):
    get_sidecars()
    return


@app.cell
def _(cv2):
    cv2.widget.cad_width, cv2.widget.height
    return


@app.cell
def _(cv_1):
    (cv_1.widget.cad_width, cv_1.widget.height)
    return


@app.cell
def _(cv2, cv_1):
    cv_1.close()
    cv2.close()
    return


@app.cell
def _(get_sidecars):
    get_sidecars()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell view
    """)
    return


@app.cell
def _(objects, show):
    _name = 'boxes'
    _control = 'orbit'
    cv_2 = show(objects[_name], control=_control, up='Z', cad_width=750, tree_width=250, height=500, glass=True, debug=False, collapse='1', theme='browser')
    return (cv_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exports

    **Modify view before exporting**
    """)
    return


@app.cell
def _(cv_2):
    cv_2.export_png('boxes2.png')
    return


@app.cell
def _(cv_2):
    cv_2.export_html()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Pin as PNG**
    """)
    return


@app.cell
def _(cv_2):
    cv_2.pin_as_png()  # same as pressing the pin top right button
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sidecar handling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## openviewer and add_shapes
    """)
    return


@app.cell
def _(open_viewer):
    cv1 = open_viewer(
        title="CVW 1",
        anchor="split-right",
        cad_width=750,
        tree_width=250,
        height=525,
        glass=True
    )
    return (cv1,)


@app.cell
def _(cv1, objects):
    _name = 'hexapod'
    #    position = (865.4844022079983, -276.23389988421786, 335.21716816984906),
    #    quaternion = (0.43557639340677845, 0.3648618806188253, 0.4409953598863984, 0.6947460731351442),
    #    zoom=0.8,
    cv1.add_shapes(objects[_name], control='trackball', axes=False, axes0=False, grid=(True, True, False), ticks=10, transparent=False, normal_len=2, default_edgecolor='#707070', default_opacity=0.5, ambient_intensity=1.0, direct_intensity=1.1, timeit=False, reset_camera='reset', zoom_speed=0.5, pan_speed=0.5, rotate_speed=1.0, debug=True, up='Z', explode=True)  #tools=False,  #ortho=False,  #black_edges=True,
    return


@app.cell
def _(objects, show):
    _name = 'boxes'
    show(objects[_name], title='CVW 1', cad_width=800, height=600, glass=True, up='Y')
    return


@app.cell
def _(cv1):
    cv1.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Show command
    """)
    return


@app.cell
def _(objects, show):
    _name = 'boxes'
    cv2_1 = show(objects[_name], title='CVW 2', anchor='split-top', ortho=False, control='orbit', axes=True, grid=(True, False, False), ticks=40, normal_len=2, default_edgecolor='#f0f0f0', default_opacity=0.5, ambient_intensity=0.5, direct_intensity=0.3)
    return (cv2_1,)


@app.cell
def _(get_sidecars):
    get_sidecars()
    return


@app.cell
def _(cv2_1):
    cv2_1.close()
    return


@app.cell
def _(objects, show):
    _name = 'box1'
    show(objects[_name], glass=False, reset_camera='reset', title='CVW 2')
    return


@app.cell
def _(objects, show):
    _name = 'hexapod'
    cv_3 = show(objects[_name], title='CVW 2', collapse='R', glass=True, reset_camera='reset')
    return (cv_3,)


@app.cell
def _(AnimationTrack, cv_3, np):
    _horizontal_angle = 25

    def _intervals(count):
        r = [min(180, (90 + _i * (360 // count)) % 360) for _i in range(count)]
        return r

    def _times(end, count):
        return np.linspace(0, end, count + 1)

    def vertical(count, end, offset, reverse):
        ints = _intervals(count)
        heights = [round(35 * np.sin(np.deg2rad(x)) - 15, 1) for x in ints]
        heights.append(heights[0])
        return (_times(end, count), heights[offset:] + heights[1:offset + 1])

    def horizontal(end, reverse):
        factor = 1 if reverse else -1
        return (_times(end, 4), [0, factor * _horizontal_angle, 0, -factor * _horizontal_angle, 0])
    leg_group = ('left_front', 'right_middle', 'left_back')
    leg_names = ['right_back', 'right_middle', 'right_front', 'left_back', 'left_middle', 'left_front']
    for _name in leg_names:
        cv_3.add_track(AnimationTrack(f'/hexapod/{_name}_leg', 'rz', *horizontal(4, 'middle' in _name)))
        cv_3.add_track(AnimationTrack(f'/hexapod/{_name}_leg/{_name}_lower_leg', 'rz', *vertical(8, 4, 0 if _name in leg_group else 4, 'left' in _name)))
    cv_3.animate(3)
    return


@app.cell
def _(cv_3):
    cv_3.close()
    cv_3.disposed
    return


@app.cell
def _(get_sidecars):
    get_sidecars()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Use default sidecar
    """)
    return


@app.cell
def _(set_default_sidecar):
    set_default_sidecar("CVW 1")
    return


@app.cell
def _(objects, show):
    _name = 'edges'
    cv_4 = show(objects[_name], height=600, cad_width=800, reset_camera='reset', debug=True)
    return (cv_4,)


@app.cell
def _(objects, show):
    _name = 'faces'
    cv2_2 = show(objects[_name], cad_width=1000, title='CVW 2')
    return


@app.cell
def _(cv_4):
    cv_4.dump_model()
    return


@app.cell
def _(get_sidecars):
    get_sidecars()
    return


@app.cell
def _(cv_4, get_sidecar):
    get_sidecar('CVW 1') == cv_4
    return


@app.cell
def _(cv_4, get_sidecar):
    get_sidecar('CVW 2') == cv_4
    return


@app.cell
def _(close_sidecars):
    close_sidecars()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Cell Viewer Handling
    """)
    return


@app.cell
def _(objects, show):
    _name = 'hexapod'
    cv3 = show(objects[_name], height=600, cad_width=800, control='trackball', tools=True, axes=True, axes0=True, grid=[True, False, True], transparent=True, black_edges=True, ortho=False, timeit=True)  # normal_len=5,
    return


@app.cell
def _(objects, show):
    _name = 'faces'
    cv4 = show(objects[_name], cad_width=750, height=400, glass=True, collapse='C', pinning=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Camera location handling

    ## Trackball controls
    """)
    return


@app.cell
def _(objects, show):
    _name = 'edges'
    cv1_1 = show(objects[_name], cad_width=800, title='Trackball', reset_camera='reset', debug=True)
    return (cv1_1,)


@app.cell
def _(cv1_1):
    cv1_1.position = (96.5764, -1.7474, 37.7064)
    cv1_1.quaternion = (0.338779, 0.378157, 0.6416827, 0.574865)
    cv1_1.zoom = 0.6
    cv1_1.target = (6.9493, -11.6226, -12.2272)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Do not reset camera location**
    """)
    return


@app.cell
def _(objects, show):
    _name = 'faces'
    show(objects[_name], title='Trackball', reset_camera='keep')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Reset camera location**
    """)
    return


@app.cell
def _(objects, show):
    _name = 'faces'
    cv_5 = show(objects[_name], title='Trackball', reset_camera='reset')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Orbit controls
    """)
    return


@app.cell
def _(open_viewer):
    cv_6 = open_viewer(title='Orbit', height=525)
    return (cv_6,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Setting camera location during show will also set the reset location of the camera**
    """)
    return


@app.cell
def _(cv_6, objects, show):
    _name = 'edges'
    show(objects[_name], title='Orbit', control='orbit', position=(-43.3, 73.7, -39.3), zoom=0.5, reset_camera='reset')
    (cv_6.position, cv_6.quaternion, cv_6.target, cv_6.zoom)
    return


@app.cell
def _(cv_6):
    cv_6.position = (85, 25, 55)
    cv_6.target = (0, 0, 0)
    cv_6.zoom = 0.8
    return


@app.cell
def _(cv_6):
    (cv_6.position, cv_6.target, cv_6.zoom)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quaternions with orbit control can be accessed from widget, however, for information only**
    """)
    return


@app.cell
def _(cv_6):
    cv_6.widget.quaternion
    return


@app.cell
def _(close_sidecars):
    close_sidecars()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Property access
    """)
    return


@app.cell
def _(open_viewer):
    cv_7 = open_viewer(title='Examples', anchor='right', cad_width=700, height=525, glass=False)
    return (cv_7,)


@app.cell
def _(names, objects, show, widgets):
    menu = widgets.Dropdown(options=names, value=names[0], description='Number:', disabled=False)
    _control = 'trackball'

    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            _name = change['new']
            show(objects[_name], title='Examples', control=_control, debug=True)
    menu.observe(on_change)
    show(objects[names[0]], title='Examples', control=_control, debug=True)
    #    zoom=0.75,
    menu
    return


@app.cell
def _(cv_7):
    cv_7.widget.cad_width = 900
    cv_7.widget.tree_width = 300
    cv_7.widget.height = 700
    cv_7.widget.glass = True
    return


@app.cell
def _(cv_7):
    cv_7.widget.cad_width = 700
    cv_7.widget.tree_width = 250
    cv_7.widget.height = 525
    cv_7.widget.glass = False
    return


@app.cell
def _(close_sidecars):
    close_sidecars()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Widget interaction
    """)
    return


@app.cell
def _(objects, show):
    cv_8 = show(objects['hexapod'], title='Examples', collapse='E', debug=True)
    return (cv_8,)


@app.cell
def _(cv_8):
    cv_8.update_states({'/hexapod/bottom': (1, 0), '/hexapod/top': [0, 0], '/hexapod/left_front_leg/upper_leg': [0, 0]})
    return


@app.cell
def _(cv_8):
    cv_8.update_states({'/hexapod/bottom': (1, 1), '/hexapod/top': [1, 1], '/hexapod/left_front_leg/upper_leg': [1, 1]})
    return


@app.cell
def _(cv_8):
    cv_8.widget.collapse = 'C'
    return


@app.cell
def _(cv_8):
    cv_8.widget.collapse = 'R'
    return


@app.cell
def _(cv_8):
    cv_8.widget.collapse = 'E'
    return


@app.cell
def _(cv_8):
    cv_8.widget.collapse = '1'
    return


@app.cell
def _(cv_8):
    cv_8.ambient_intensity = 1.2
    cv_8.direct_intensity = 1.5
    return


@app.cell
def _(cv_8):
    cv_8.ambient_intensity = 0.5
    cv_8.direct_intensity = 0.3
    return


@app.cell
def _(cv_8):
    ec = cv_8.default_edgecolor
    return (ec,)


@app.cell
def _(cv_8):
    cv_8.default_edgecolor = '#ff0000'
    return


@app.cell
def _(cv_8, ec):
    cv_8.default_edgecolor = ec
    return


@app.cell
def _(cv_8):
    cv_8.grid = [not g for g in cv_8.widget.grid]
    return


@app.cell
def _(cv_8):
    cv_8.axes = not cv_8.axes
    cv_8.axes0 = not cv_8.axes0
    cv_8.transparent = not cv_8.transparent
    cv_8.black_edges = not cv_8.black_edges
    return


@app.cell
def _(cv_8):
    cv_8.tools = not cv_8.tools
    return


@app.cell
def _(cv_8):
    cv_8.ortho = not cv_8.ortho
    return


@app.cell
def _(cv_8):
    cv_8.grid = [not g for g in cv_8.widget.grid]
    cv_8.axes = not cv_8.axes
    cv_8.axes0 = not cv_8.axes0
    cv_8.transparent = not cv_8.transparent
    cv_8.black_edges = not cv_8.black_edges
    cv_8.tools = not cv_8.tools
    cv_8.glass = not cv_8.glass
    cv_8.ortho = not cv_8.ortho
    return


@app.cell
def _(cv_8):
    cv_8.glass = not cv_8.glass
    return


@app.cell
def _(cv_8):
    cv_8.zoom_speed = 5
    cv_8.pan_speed = 5
    cv_8.rotate_speed = 5
    return


@app.cell
def _(cv_8):
    cv_8.zoom_speed = 1
    cv_8.pan_speed = 1
    cv_8.rotate_speed = 1
    return


@app.cell
def _(cv_8):
    cv_8.last_pick
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Clipping handling
    """)
    return


@app.cell
def _(cv_8):
    cv_8.select_clipping()
    return


@app.cell
def _(cv_8):
    cv_8.clip_intersection = not cv_8.clip_intersection
    return


@app.cell
def _(cv_8):
    cv_8.clip_planes = not cv_8.clip_planes
    return


@app.cell
def _(cv_8):
    cv_8.clip_value_0 = 10
    cv_8.clip_value_1 = -50
    cv_8.clip_value_2 = 40
    return


@app.cell
def _(cv_8):
    cv_8.clip_normal_0
    return


@app.cell
def _(cv_8):
    cv_8.clip_value_2
    return


@app.cell
def _(cv_8):
    cv_8.clip_normal_0 = (-0.35, -0.35, -0.35)
    return


@app.cell
def _(cv_8):
    cv_8.clip_normal_0 = (-1, 0, 0)
    return


@app.cell
def _(cv_8):
    cv_8.select_tree()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rotations
    ## Trackball Control
    """)
    return


@app.cell
def _(objects, show):
    _name = 'hexapod'
    cv_9 = show(objects[_name], control='trackball', title='Examples', reset_camera='reset', glass=False)
    return (cv_9,)


@app.cell
def _(cv_9, time):
    for _i in range(10):
        cv_9.rotate_x(1)
        cv_9.rotate_y(3)
        cv_9.rotate_z(5)
        time.sleep(0.05)
    return


@app.cell
def _(cv_9, time):
    for _i in range(10):
        cv_9.rotate_z(-5)
        cv_9.rotate_y(-3)
        cv_9.rotate_x(-1)
        time.sleep(0.05)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Orbit control
    """)
    return


@app.cell
def _(objects, show):
    _name = 'hexapod'
    cv_10 = show(objects[_name], control='orbit', title='Examples', reset_camera='reset')
    return (cv_10,)


@app.cell
def _(cv_10, time):
    for _i in range(10):
        cv_10.rotate_up(3)
        cv_10.rotate_left(1)
        time.sleep(0.05)
    return


@app.cell
def _(cv_10, time):
    for _i in range(10):
        cv_10.rotate_left(-1)
        cv_10.rotate_up(-3)
        time.sleep(0.05)
    return


@app.cell
def _(close_sidecars):
    close_sidecars()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Animation
    """)
    return


@app.cell
def _(objects, show):
    _name = 'hexapod'
    cv_11 = show(objects[_name], title='Animation', height=600, cad_width=800, control='trackball', tools=True, axes=True, axes0=True, grid=[True, False, False])
    return (cv_11,)


@app.cell
def _(np):
    _horizontal_angle = 25
    leg_names_1 = {'right_back', 'right_middle', 'right_front', 'left_back', 'left_middle', 'left_front'}

    def _intervals(count):
        r = [min(180, (90 + _i * (360 // count)) % 360) for _i in range(count)]
        return r

    def _times(end, count):
        return np.linspace(0, end, count + 1).tolist()

    def vertical_1(count, end, offset, reverse):
        ints = _intervals(count)
        heights = [round(35 * np.sin(np.deg2rad(x)) - 15, 1) for x in ints]
        heights.append(heights[0])
        return (_times(end, count), heights[offset:] + heights[1:offset + 1])

    def horizontal_1(end, reverse):
        factor = 1 if reverse else -1
        return (_times(end, 4), [0, factor * _horizontal_angle, 0, -factor * _horizontal_angle, 0])
    leg_group_1 = ('left_front', 'right_middle', 'left_back')
    return horizontal_1, leg_group_1, leg_names_1, vertical_1


@app.cell
def _(AnimationTrack, cv_11, horizontal_1, leg_names_1):
    tracks = []
    for _name in leg_names_1:
        cv_11.add_track(AnimationTrack(f'/hexapod/{_name}_leg', 'rz', *horizontal_1(4, 'middle' in _name)))
    cv_11.animate(3)
    cv_11.play()
    return


@app.cell
def _(cv_11):
    cv_11.stop()
    return


@app.cell
def _(AnimationTrack, cv_11, leg_group_1, leg_names_1, vertical_1):
    for _name in leg_names_1:
        cv_11.add_track(AnimationTrack(f'/hexapod/{_name}_leg/{_name}_lower_leg', 'rz', *vertical_1(8, 4, 0 if _name in leg_group_1 else 4, 'left' in _name)))
    cv_11.animate(2)
    cv_11.play()
    return


@app.cell
def _(cv_11):
    cv_11.clear_tracks()
    return


@app.cell
def _(close_sidecars):
    close_sidecars()
    return


if __name__ == "__main__":
    app.run()
