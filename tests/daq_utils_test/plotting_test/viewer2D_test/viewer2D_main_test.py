from PyQt5 import QtWidgets
from pymodaq.daq_utils.plotting.viewer2D import Viewer2D
from pymodaq.daq_utils.exceptions import ExpectedError, Expected_1, Expected_2
from pyqtgraph import ROI
from pyqtgraph.parametertree import Parameter
from pymodaq.daq_utils.plotting.graph_items import PlotCurveItem
from unittest import mock

import pytest
import numpy as np
import pyqtgraph as pg

from pyqtgraph import ROI


@pytest.fixture
def init_prog(qtbot):
    form = QtWidgets.QWidget()
    prog = Viewer2D()
    qtbot.addWidget(form)
    return prog


class TestViewer2D:
    def test_init(self, init_prog):
        prog = init_prog

        assert isinstance(prog, Viewer2D)

    def test_remove_ROI(self, init_prog):
        prog = init_prog
        prog.setupROI()

        roi_dict = {'ROI_00': ROI((0, 0))}

        prog.roi_manager.ROIs = roi_dict

        item_param_0 = Parameter(name='ROI_00')

        math_param = Parameter(name='math_function')
        math_param.setValue('Mean')
        channel_param = Parameter(name='use_channel')
        channel_param.setValue(1)
        test_list = [0, 1, 2, 3]
        channel_param.opts['limits'] = test_list
        color_param = Parameter(name='Color')
        color_param.setValue(1)

        children = [math_param, channel_param, color_param]
        item_param_0.addChildren(children)

        item_params = [item_param_0]

        rois_param = Parameter(name='ROIs', children=item_params)

        prog.roi_manager.settings = Parameter(name='settings', children=[rois_param])

        prog.lo_items = prog.roi_manager.ROIs

        prog.add_ROI(newindex=0, roi_type='ROI_00')

        prog.remove_ROI(roi_name='ROI_00')

        assert 'ROI_00' not in prog.ui.RoiCurve_H
        assert 'ROI_00' not in prog.ui.RoiCurve_V
        assert 'ROI_00' not in prog.ui.RoiCurve_integrated

    def test_add_ROI(self, init_prog):
        prog = init_prog
        prog.setupROI()

        roi_dict = {'ROI_00': ROI((0, 0)), 'ROI_01': ROI((1, 1)),
                    'ROI_02': ROI((2, 2)), 'ROI_03': ROI((3, 3))}

        prog.roi_manager.ROIs = roi_dict

        item_param_0 = Parameter(name='ROI_00')
        item_param_1 = Parameter(name='ROI_01')
        item_param_2 = Parameter(name='ROI_02')
        item_param_3 = Parameter(name='ROI_03')

        item_params = [item_param_0, item_param_1, item_param_2, item_param_3]

        for ind, item_param in enumerate(item_params):
            math_param = Parameter(name='math_function')
            math_param.setValue('Mean')
            channel_param = Parameter(name='use_channel')
            channel_param.setValue(1)
            test_list = [0, 1, 2, 3]
            channel_param.opts['limits'] = test_list
            color_param = Parameter(name='Color')
            color_param.setValue(1)

            children = [math_param, channel_param, color_param]
            item_param.addChildren(children)

        rois_param = Parameter(name='ROIs', children=item_params)

        prog.roi_manager.settings = Parameter(name='settings', children=[rois_param])

        prog.lo_items = prog.roi_manager.ROIs

        prog.isdata['red'] = True

        prog.add_ROI(newindex=0, roi_type='ROI_00')

        assert isinstance(prog.ui.RoiCurve_H['ROI_00'], PlotCurveItem)
        assert isinstance(prog.ui.RoiCurve_V['ROI_00'], PlotCurveItem)
        assert isinstance(prog.ui.RoiCurve_integrated['ROI_00'], PlotCurveItem)
        assert prog.roi_manager.settings.child('ROIs', 'ROI_00', 'use_channel').value() == 'red'

        prog.isdata['red'] = False
        prog.isdata['green'] = True

        prog.add_ROI(newindex=0, roi_type='ROI_00')

        assert prog.roi_manager.settings.child('ROIs', 'ROI_00', 'use_channel').value() == 'green'

        prog.isdata['green'] = False
        prog.isdata['blue'] = True

        prog.add_ROI(newindex=0, roi_type='ROI_00')

        assert prog.roi_manager.settings.child('ROIs', 'ROI_00', 'use_channel').value() == 'blue'

        prog.isdata['blue'] = False
        prog.isdata['spread'] = True

        prog.add_ROI(newindex=0, roi_type='ROI_00')

        assert prog.roi_manager.settings.child('ROIs', 'ROI_00', 'use_channel').value() == 'spread'

    @pytest.mark.skip(reason="Test not implemented")
    def test_crosshairChanged(self, init_prog):
        prog = init_prog

    def test_crosshairClicked(self, init_prog):
        prog = init_prog

        prog.ui.crosshair.setVisible(False)
        prog.position_action.setVisible(False)

        prog.ui.crosshair_H_blue.setVisible(False)
        prog.ui.crosshair_V_blue.setVisible(False)

        prog.ui.crosshair_H_green.setVisible(False)
        prog.ui.crosshair_V_green.setVisible(False)

        prog.ui.crosshair_H_red.setVisible(False)
        prog.ui.crosshair_V_red.setVisible(False)

        prog.ui.crosshair_H_spread.setVisible(False)
        prog.ui.crosshair_V_spread.setVisible(False)

        prog.isdata["blue"] = True
        prog.isdata["green"] = True
        prog.isdata["red"] = True
        prog.isdata["spread"] = True

        prog.crosshair_action.setChecked(True)

        prog.crosshairClicked()

        assert prog.ui.crosshair.isVisible()
        assert prog.position_action.isVisible()

        assert prog.ui.crosshair_H_blue.isVisible()
        assert prog.ui.crosshair_V_blue.isVisible()

        assert prog.ui.crosshair_H_green.isVisible()
        assert prog.ui.crosshair_V_green.isVisible()

        assert prog.ui.crosshair_H_red.isVisible()
        assert prog.ui.crosshair_V_red.isVisible()

        assert prog.ui.crosshair_H_spread.isVisible()
        assert prog.ui.crosshair_V_spread.isVisible()

    def test_double_clicked(self, init_prog):
        prog = init_prog

        prog.double_clicked(posx=10, posy=20)

        assert prog.ui.crosshair.vLine.value() == 10
        assert prog.ui.crosshair.hLine.value() == 20

    def test_ini_plot(self, init_prog):
        prog = init_prog

        for ind in range(10):
            prog.data_integrated_plot['plot_{:02d}'.format(ind)] = None

        prog.ini_plot()

        for key in prog.data_integrated_plot.keys():
            assert np.array_equal(prog.data_integrated_plot[key], np.zeros((2, 1)))

    def test_lock_aspect_ratio(self, init_prog):
        prog = init_prog

        prog.image_widget.plotitem.vb.setAspectLocked(lock=False)
        assert not prog.image_widget.plotitem.vb.state['aspectLocked']

        prog.aspect_ratio_action.setChecked(True)
        assert prog.aspect_ratio_action.isChecked()

        prog.lock_aspect_ratio()

        assert prog.image_widget.plotitem.vb.state['aspectLocked']

        prog.aspect_ratio_action.setChecked(False)
        assert not prog.aspect_ratio_action.isChecked()

        prog.lock_aspect_ratio()

        assert not prog.image_widget.plotitem.vb.state['aspectLocked']

    @pytest.mark.skip(reason="Access violation problem")
    def test_move_left_splitter(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Access violation problem")
    def test_move_right_splitter(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_restore_state(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not finished")
    def test_roi_changed(self, init_prog):
        prog = init_prog

        prog.raw_data = {}

        prog.raw_data['blue'] = np.linspace(np.linspace(1, 10, 10), np.linspace(11, 20, 10), 2)
        prog.raw_data['green'] = np.linspace(np.linspace(11, 20, 10), np.linspace(21, 30, 10), 2)
        prog.raw_data['red'] = np.linspace(np.linspace(21, 30, 10), np.linspace(31, 40, 10), 2)
        prog.raw_data['spread'] = np.linspace(np.linspace(31, 40, 10), np.linspace(41, 50, 10), 2)

        roi_dict = {'ROI_00': ROI((0, 0)), 'ROI_01': ROI((1, 1)),
                    'ROI_02': ROI((2, 2)), 'ROI_03': ROI((3, 3)),
                    'ROI_04': ROI((4, 4))}

        prog.roi_manager.ROIs = roi_dict

        item_params = []

        colors = mock.Mock()
        colors.value.side_effect = ['blue', 'green', 'red', 'spread', None]

        for ind in range(5):
            item_param = Parameter(name='ROI_{:02d}'.format(ind))

            channel_param = Parameter(name='use_channel')
            channel_param.setValue(colors.value())
            color_param = Parameter(name='Color')
            color_param.setValue(1)

            children = [channel_param, color_param]
            item_param.addChildren(children)

            item_params.append(item_param)

        rois_param = Parameter(name='ROIs', children=item_params)

        prog.roi_manager.settings = Parameter(name='settings', children=[rois_param])

        prog.roi_changed()

    def test_update_roi(self, init_prog):
        prog = init_prog

        roi_dict = {'ROI_00': ROI((0, 0)), 'ROI_01': ROI((1, 1)),
                    'ROI_02': ROI((2, 2)), 'ROI_03': ROI((3, 3))}

        prog.roi_manager.ROIs = roi_dict

        item_param_0 = Parameter(name='ROI_00')
        item_param_1 = Parameter(name='ROI_01')
        item_param_2 = Parameter(name='ROI_02')
        item_param_3 = Parameter(name='ROI_03')

        item_params = [item_param_0, item_param_1, item_param_2, item_param_3]

        for ind, item_param in enumerate(item_params):
            math_param = Parameter(name='math_function')
            math_param.setValue('Mean')
            channel_param = Parameter(name='use_channel')
            channel_param.setValue(1)
            test_list = [0, 1, 2, 3]
            channel_param.opts['limits'] = test_list
            color_param = Parameter(name='Color')
            color_param.setValue(1)

            children = [math_param, channel_param, color_param]
            item_param.addChildren(children)

        rois_param = Parameter(name='ROIs', children=item_params)

        prog.roi_manager.settings = Parameter(name='settings', children=[rois_param])

        for ind in range(4):
            prog.add_ROI(ind, 'ROI_{:02d}'.format(ind))

        change_1 = [prog.roi_manager.settings.child('ROIs', 'ROI_00', 'Color'), 'value', 1]
        change_2 = [None, 'childAdded', None]
        change_3 = [prog.roi_manager.settings.child('ROIs', 'ROI_01'), 'parent', None]

        changes = [change_1, change_2, change_3]

        prog.update_roi(changes)

        assert prog.ui.RoiCurve_H['ROI_00'].opts['pen'].color().getRgb() == (255, 170, 0, 255)
        assert prog.ui.RoiCurve_V['ROI_00'].opts['pen'].color().getRgb() == (255, 170, 0, 255)
        assert prog.ui.RoiCurve_integrated['ROI_00'].opts['pen'].color().getRgb() == (255, 170, 0, 255)

        assert 'ROI_01' not in prog.ui.RoiCurve_H
        assert 'ROI_01' not in prog.ui.RoiCurve_V
        assert 'ROI_01' not in prog.ui.RoiCurve_integrated

    def test_roi_clicked(self, init_prog):
        prog = init_prog

        roi_dict = {'ROI_00': ROI((0, 0))}

        prog.roi_manager.ROIs = roi_dict

        item_param_0 = Parameter(name='ROI_00')

        color_param = Parameter(name='Color')
        color_param.setValue(1)

        children = [color_param]
        item_param_0.addChildren(children)

        item_params = [item_param_0]

        rois_param = Parameter(name='ROIs', children=item_params)

        prog.roi_manager.settings = Parameter(name='settings', children=[rois_param])

        prog.add_ROI(0, 'ROI_00')

        color_param = Parameter(name='Color')
        color_param.setValue(1)

        prog.roi_action.setChecked(True)

        prog.roi_clicked()

        assert prog.ui.RoiCurve_H['ROI_00'].isVisible()
        assert prog.ui.RoiCurve_V['ROI_00'].isVisible()
        assert prog.ui.RoiCurve_integrated['ROI_00'].isVisible()

        prog.roi_action.setChecked(False)

        prog.roi_clicked()

        assert not prog.ui.RoiCurve_H['ROI_00'].isVisible()
        assert not prog.ui.RoiCurve_V['ROI_00'].isVisible()
        assert not prog.ui.RoiCurve_integrated['ROI_00'].isVisible()

    def test_scale_axis(self, init_prog):
        prog = init_prog

        x_data = np.linspace(2, 10, 5)
        label = 'label'
        units = 'nm'

        x_axis = {'data': x_data, 'label': label, 'units': units}

        prog.x_axis = x_axis

        y_data = np.linspace(10, 2, 5)
        label = 'label'
        units = 'nm'

        y_axis = {'data': y_data, 'label': label, 'units': units}

        prog.y_axis = y_axis

        x, y = prog.scale_axis(xaxis_pxl=1, yaxis_pxl=1)

        assert x == 4
        assert y == 8

    def test_unscale_axis(self, init_prog):
        prog = init_prog

        x_data = np.linspace(2, 10, 5)
        label = 'label'
        units = 'nm'

        x_axis = {'data': x_data, 'label': label, 'units': units}

        prog.x_axis = x_axis

        y_data = np.linspace(10, 2, 5)
        label = 'label'
        units = 'nm'

        y_axis = {'data': y_data, 'label': label, 'units': units}

        prog.y_axis = y_axis

        x, y = prog.unscale_axis(xaxis=4, yaxis=8)

        assert x == 1
        assert y == 1

    def test_selected_region_changed(self, init_prog):
        prog = init_prog

        roi_select_signal = mock.Mock()
        roi_select_signal.emit.side_effect = [ExpectedError]

        prog.setupUI()
        prog.ROI_select_signal = roi_select_signal

        prog.ROIselect_action.setChecked(True)

        with pytest.raises(ExpectedError):
            prog.selected_region_changed()

    def test_set_autolevels(self, init_prog):
        prog = init_prog

        prog.ui.histogram_blue.imageItem().setLevels(None)
        prog.ui.histogram_green.imageItem().setLevels(None)
        prog.ui.histogram_red.imageItem().setLevels(None)

        prog.ui.histogram_blue.region.setVisible(True)
        prog.ui.histogram_green.region.setVisible(True)
        prog.ui.histogram_red.region.setVisible(True)
        prog.auto_levels_action.setChecked(True)

        prog.set_autolevels()

        assert not prog.ui.histogram_blue.region.isVisible()
        assert not prog.ui.histogram_green.region.isVisible()
        assert not prog.ui.histogram_red.region.isVisible()

        prog.auto_levels_action.setChecked(False)

        prog.set_autolevels()

        blue = prog.ui.histogram_blue
        green = prog.ui.histogram_green
        red = prog.ui.histogram_red

        assert np.array_equal(blue.imageItem().getLevels(), blue.getLevels())
        assert np.array_equal(green.imageItem().getLevels(), green.getLevels())
        assert np.array_equal(red.imageItem().getLevels(), red.getLevels())

        assert prog.ui.histogram_blue.region.isVisible()
        assert prog.ui.histogram_green.region.isVisible()
        assert prog.ui.histogram_red.region.isVisible()

    def test_set_scaling_axes(self, init_prog):
        prog = init_prog

        scaled_xaxis = dict(scaling=1, offset=3, label='x_axis', units='nm')

        scaled_yaxis = dict(scaling=3, offset=2.5, label='y_axis', units='dm')

        scaling_options = dict(scaled_xaxis=scaled_xaxis, scaled_yaxis=scaled_yaxis)

        prog.set_scaling_axes(scaling_options=scaling_options)

        x_axis = prog.scaled_xaxis
        y_axis = prog.scaled_yaxis

        assert x_axis.scaling == scaled_xaxis['scaling']
        assert x_axis.offset == scaled_xaxis['offset']
        assert x_axis.labelText == scaled_xaxis['label']
        assert x_axis.labelUnits == scaled_xaxis['units']

        assert y_axis.scaling == scaled_yaxis['scaling']
        assert y_axis.offset == scaled_yaxis['offset']
        assert y_axis.labelText == scaled_yaxis['label']
        assert y_axis.labelUnits == scaled_yaxis['units']

        assert x_axis.range == pytest.approx([-4.1981733, 10.1981733], 0.01)
        assert y_axis.range == pytest.approx([-14.0014728, 19.0014728], 0.01)

    def test_transform_image(self, init_prog):
        prog = init_prog

        data = np.linspace(np.linspace(np.linspace(1, 10, 10), np.linspace(11, 20, 10), 2),
                           np.linspace(np.linspace(21, 30, 10), np.linspace(31, 40, 10), 2), 2)

        prog.FlipUD_action.setChecked(False)
        prog.FlipLR_action.setChecked(False)
        prog.rotate_action.setChecked(False)

        result = prog.transform_image(data=data)
        data_2 = np.mean(data, axis=0)

        assert np.array_equal(result, data_2)

        prog.FlipUD_action.setChecked(True)

        result = prog.transform_image(data=data)
        data_3 = np.flipud(data_2)

        assert np.array_equal(result, data_3)

        prog.FlipLR_action.setChecked(True)

        result = prog.transform_image(data=data)
        data_4 = np.fliplr(data_3)

        assert np.array_equal(result, data_4)

        prog.rotate_action.setChecked(True)

        result = prog.transform_image(data=data)
        data_5 = np.flipud(np.transpose(data_4))

        assert np.array_equal(result, data_5)

        assert not prog.transform_image(data=None)

    @pytest.mark.skip(reason="Test not implemented")
    def test_set_image_transform(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_set_visible_items(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_setImage(self, init_prog):
        prog = init_prog

    def test_setImageTemp(self, init_prog):
        prog = init_prog

        prog.setImageTemp()

        assert not prog.isdata['blue']
        assert not prog.isdata['green']
        assert not prog.isdata['red']
        assert not prog.isdata['spread']

        data_blue = np.linspace(np.linspace(1, 10, 10), np.linspace(11, 20, 10), 2)
        data_green = np.linspace(np.linspace(11, 20, 10), np.linspace(21, 30, 10), 2)
        data_red = np.linspace(np.linspace(21, 30, 10), np.linspace(31, 40, 10), 2)
        data_spread = np.linspace(np.linspace(31, 40, 10), np.linspace(41, 50, 10), 2)

        prog.setImageTemp(data_blue=data_blue, data_green=data_green, data_red=data_red, data_spread=data_spread)

        assert prog.isdata['blue']
        assert prog.isdata['green']
        assert prog.isdata['red']
        assert prog.isdata['spread']

        assert np.array_equal(prog.ui.img_blue.image, data_blue)
        assert np.array_equal(prog.ui.img_green.image, data_green)
        assert np.array_equal(prog.ui.img_red.image, data_red)
        assert np.array_equal(prog.ui.img_spread.image, data_spread)

    def test_mapfromview(self, init_prog):
        prog = init_prog

        graphitem = 'None'
        x = None
        y = None

        prog.mapfromview(graphitem=graphitem, x=x, y=y)

        graphitem = 'red'
        x = 1
        y = 2

        result = prog.mapfromview(graphitem=graphitem, x=x, y=y)
        assert result == (x, y)

    def test_setObjectName(self, init_prog):
        prog = init_prog

        prog.setObjectName('test')

        assert prog.parent.objectName() == 'test'

    def test_show_hide_histogram(self, init_prog):
        prog = init_prog

        prog.parent.show()

        prog.raw_data = {}
        prog.raw_data['blue'] = np.linspace(1, 10, 10)
        prog.raw_data['green'] = np.linspace(11, 20, 10)
        prog.raw_data['red'] = np.linspace(21, 30, 10)
        prog.raw_data['spread'] = np.linspace(31, 40, 10)

        prog.isdata = {}
        prog.isdata['blue'] = True
        prog.isdata['green'] = True
        prog.isdata['red'] = True
        prog.isdata['spread'] = True

        prog.blue_action.setChecked(True)
        prog.green_action.setChecked(True)
        prog.red_action.setChecked(True)
        prog.spread_action.setChecked(True)
        prog.histo_action.setChecked(True)

        prog.show_hide_histogram()

        assert prog.ui.histogram_blue.isVisible()
        assert prog.ui.histogram_blue.region.getRegion() == (1, 10)
        assert prog.ui.histogram_green.isVisible()
        assert prog.ui.histogram_green.region.getRegion() == (11, 20)
        assert prog.ui.histogram_red.isVisible()
        assert prog.ui.histogram_red.region.getRegion() == (21, 30)
        assert prog.ui.histogram_spread.isVisible()
        assert prog.ui.histogram_spread.region.getRegion() == (31, 40)

    def test_show_hide_iso(self, init_prog):
        prog = init_prog

        prog.isocurve_action.setChecked(True)
        prog.histo_action.setChecked(False)

        prog.raw_data = {}
        prog.raw_data['red'] = np.linspace(1, 10, 10)

        prog.show_hide_iso()

        assert prog.histo_action.isChecked()
        result = pg.gaussianFilter(prog.raw_data['red'], (2, 2))
        for val1, val2 in zip(prog.ui.iso.data, result):
            assert val1 == pytest.approx(val2)

    @pytest.mark.skip(reason="Test not implemented")
    def test_show_lineouts(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_show_ROI_select(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_update_image(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_update_selection_area_visibility(self, init_prog):
        prog = init_prog

    @pytest.mark.skip(reason="Test not implemented")
    def test_update_crosshair_data(self, init_prog):
        prog = init_prog

    def test_updateIsocurve(self, init_prog):
        prog = init_prog

        prog.ui.isoLine.setValue(5)

        prog.updateIsocurve()

        assert prog.ui.iso.level == 5

    def test_x_axis(self, init_prog):
        prog = init_prog

        prog.x_axis_scaled = 'x_axis_scaled'

        assert prog.x_axis == 'x_axis_scaled'

    def test_x_axis_setter(self, init_prog):
        prog = init_prog

        data = np.linspace(1, 10, 10)
        label = 'label'
        units = 'nm'

        x_axis = {'data': data, 'label': label, 'units': units}

        prog.x_axis = x_axis

        scaled_axis = prog.scaling_options['scaled_xaxis']
        assert scaled_axis['offset'] == 1
        assert scaled_axis['scaling'] == 1
        assert scaled_axis['label'] == label
        assert scaled_axis['units'] == units

        x_axis = np.linspace(10, 1, 10)

        prog.x_axis = x_axis

        scaled_axis = prog.scaling_options['scaled_xaxis']
        assert scaled_axis['offset'] == 10
        assert scaled_axis['scaling'] == -1
        assert scaled_axis['label'] == ''
        assert scaled_axis['units'] == ''

        x_axis = [10]

        prog.x_axis = x_axis

        scaled_axis = prog.scaling_options['scaled_xaxis']
        assert scaled_axis['offset'] == 0
        assert scaled_axis['scaling'] == 1

    def test_set_axis_label(self, init_prog):
        prog = init_prog

        prog.set_axis_label()

        scaled_xaxis = prog.scaling_options['scaled_xaxis']
        assert scaled_xaxis['orientation'] == 'bottom'
        assert scaled_xaxis['label'] == 'x axis'
        assert scaled_xaxis['units'] == 'pxls'

        axis_settings = dict(orientation='left', label='y axis', units='nm')

        prog.set_axis_label(axis_settings=axis_settings)

        scaled_xaxis = prog.scaling_options['scaled_yaxis']
        assert scaled_xaxis['orientation'] == 'left'
        assert scaled_xaxis['label'] == 'y axis'
        assert scaled_xaxis['units'] == 'nm'

    def test_y_axis(self, init_prog):
        prog = init_prog

        prog.y_axis_scaled = 'y_axis_scaled'

        assert prog.y_axis == 'y_axis_scaled'

    def test_y_axis_setter(self, init_prog):
        prog = init_prog

        data = np.linspace(1, 10, 10)
        label = 'label'
        units = 'nm'

        y_axis = {'data': data, 'label': label, 'units': units}

        prog.y_axis = y_axis

        scaled_axis = prog.scaling_options['scaled_yaxis']
        assert scaled_axis['offset'] == 1
        assert scaled_axis['scaling'] == 1
        assert scaled_axis['label'] == label
        assert scaled_axis['units'] == units

        y_axis = np.linspace(10, 1, 10)

        prog.y_axis = y_axis

        scaled_axis = prog.scaling_options['scaled_yaxis']
        assert scaled_axis['offset'] == 10
        assert scaled_axis['scaling'] == -1
        assert scaled_axis['label'] == ''
        assert scaled_axis['units'] == ''

        y_axis = [10]

        prog.y_axis = y_axis

        scaled_axis = prog.scaling_options['scaled_yaxis']
        assert scaled_axis['offset'] == 0
        assert scaled_axis['scaling'] == 1
