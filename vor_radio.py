#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: VOR Radio
# Author: Brian McLaughlin
# Description: Decodes a VOR signal
# Generated: Thu Dec 15 21:36:53 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import airnav
import math
import sip
import sys


class vor_radio(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "VOR Radio")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("VOR Radio")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "vor_radio")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2**15
        self.gui_range_variable_gain = gui_range_variable_gain = 2740
        self.gui_range_variable_delay = gui_range_variable_delay = 83
        self.gui_range_ref_gain = gui_range_ref_gain = 10
        self.fm_freq = fm_freq = 9960
        self.fm_deviation = fm_deviation = 480

        ##################################################
        # Blocks
        ##################################################
        self.monitoring_tabs = Qt.QTabWidget()
        self.monitoring_tabs_widget_0 = Qt.QWidget()
        self.monitoring_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.monitoring_tabs_widget_0)
        self.monitoring_tabs_grid_layout_0 = Qt.QGridLayout()
        self.monitoring_tabs_layout_0.addLayout(self.monitoring_tabs_grid_layout_0)
        self.monitoring_tabs.addTab(self.monitoring_tabs_widget_0, "IF Signal")
        self.monitoring_tabs_widget_1 = Qt.QWidget()
        self.monitoring_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.monitoring_tabs_widget_1)
        self.monitoring_tabs_grid_layout_1 = Qt.QGridLayout()
        self.monitoring_tabs_layout_1.addLayout(self.monitoring_tabs_grid_layout_1)
        self.monitoring_tabs.addTab(self.monitoring_tabs_widget_1, "Baseband Signal")
        self.monitoring_tabs_widget_2 = Qt.QWidget()
        self.monitoring_tabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.monitoring_tabs_widget_2)
        self.monitoring_tabs_grid_layout_2 = Qt.QGridLayout()
        self.monitoring_tabs_layout_2.addLayout(self.monitoring_tabs_grid_layout_2)
        self.monitoring_tabs.addTab(self.monitoring_tabs_widget_2, "Phase Compare")
        self.monitoring_tabs_widget_3 = Qt.QWidget()
        self.monitoring_tabs_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.monitoring_tabs_widget_3)
        self.monitoring_tabs_grid_layout_3 = Qt.QGridLayout()
        self.monitoring_tabs_layout_3.addLayout(self.monitoring_tabs_grid_layout_3)
        self.monitoring_tabs.addTab(self.monitoring_tabs_widget_3, "Scratch")
        self.top_layout.addWidget(self.monitoring_tabs)
        self._gui_range_variable_gain_range = Range(0, 10000, 10, 2740, 200)
        self._gui_range_variable_gain_win = RangeWidget(self._gui_range_variable_gain_range, self.set_gui_range_variable_gain, "Variable Gain", "counter_slider", float)
        self.monitoring_tabs_layout_2.addWidget(self._gui_range_variable_gain_win)
        self._gui_range_variable_delay_range = Range(0, 512, 1, 83, 200)
        self._gui_range_variable_delay_win = RangeWidget(self._gui_range_variable_delay_range, self.set_gui_range_variable_delay, "Variable Delay", "counter_slider", int)
        self.monitoring_tabs_layout_2.addWidget(self._gui_range_variable_delay_win)
        self._gui_range_ref_gain_range = Range(0, 10000, 10, 10, 200)
        self._gui_range_ref_gain_win = RangeWidget(self._gui_range_ref_gain_range, self.set_gui_range_ref_gain, "Reference Gain", "counter_slider", float)
        self.monitoring_tabs_layout_2.addWidget(self._gui_range_ref_gain_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	2**9, #size
        	2**9, #samp_rate
        	"Compared Signals", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["Variable", "Reference", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.monitoring_tabs_layout_2.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"IF Signal", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.monitoring_tabs_layout_0.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(False)
        
        
          
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        units = ["", "", "", "", "",
                 "", "", "", "", ""]
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, 360)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])
        
        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 500, 400, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(samp_rate // 2**12, (firdes.low_pass(1000, samp_rate, 5000, 1000)), fm_freq, samp_rate)
        self.fft_vxx_0_0 = fft.fft_vfc(512, True, (window.blackmanharris(512)), 1)
        self.fft_vxx_0 = fft.fft_vfc(512, True, (window.blackmanharris(512)), 1)
        self.dc_blocker_xx_1 = filter.dc_blocker_ff(32, True)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 512)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 512)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, 512)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, 512)
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 30)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 30)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((57.2958, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((gui_range_ref_gain, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((gui_range_variable_gain, ))
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 512)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 512)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/home/brian/gnur-projects/gr-vor/sample_data/RBT_VOR_Sample_32768kHz.raw", True)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, 0)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, gui_range_variable_delay)
        self.blocks_complex_to_arg_0_0 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.band_pass_filter_0_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, 2**9, 25, 35, 5, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_fff(samp_rate // 2**9, firdes.band_pass(
        	200, samp_rate, 25, 35, 5, firdes.WIN_HAMMING, 6.76))
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=2**12,
        	audio_decim=2**12 // 2**9,
        	deviation=fm_deviation,
        	audio_pass=30,
        	audio_stop=60,
        	gain=1.0,
        	tau=0.0,
        )
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate,
        	audio_decim=1,
        	audio_pass=30,
        	audio_stop=60,
        )
        self.airnav_unitcircle_ff_0 = airnav.unitcircle_ff()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.airnav_unitcircle_ff_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_am_demod_cf_0, 0), (self.band_pass_filter_0_0, 0))    
        self.connect((self.analog_fm_demod_cf_0, 0), (self.band_pass_filter_0_0_0, 0))    
        self.connect((self.band_pass_filter_0_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.band_pass_filter_0_0_0, 0), (self.dc_blocker_xx_1, 0))    
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.blocks_complex_to_arg_0_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_arg_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_complex_to_arg_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_delay_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_number_sink_0, 0))    
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_keep_one_in_n_0, 0))    
        self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.airnav_unitcircle_ff_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_skiphead_0_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.dc_blocker_xx_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_am_demod_cf_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vor_radio")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(200, self.samp_rate, 25, 35, 5, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1000, self.samp_rate, 5000, 1000)))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 500, 400, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_gui_range_variable_gain(self):
        return self.gui_range_variable_gain

    def set_gui_range_variable_gain(self, gui_range_variable_gain):
        self.gui_range_variable_gain = gui_range_variable_gain
        self.blocks_multiply_const_vxx_0.set_k((self.gui_range_variable_gain, ))

    def get_gui_range_variable_delay(self):
        return self.gui_range_variable_delay

    def set_gui_range_variable_delay(self, gui_range_variable_delay):
        self.gui_range_variable_delay = gui_range_variable_delay
        self.blocks_delay_0.set_dly(self.gui_range_variable_delay)

    def get_gui_range_ref_gain(self):
        return self.gui_range_ref_gain

    def set_gui_range_ref_gain(self, gui_range_ref_gain):
        self.gui_range_ref_gain = gui_range_ref_gain
        self.blocks_multiply_const_vxx_0_0.set_k((self.gui_range_ref_gain, ))

    def get_fm_freq(self):
        return self.fm_freq

    def set_fm_freq(self, fm_freq):
        self.fm_freq = fm_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.fm_freq)

    def get_fm_deviation(self):
        return self.fm_deviation

    def set_fm_deviation(self, fm_deviation):
        self.fm_deviation = fm_deviation


def main(top_block_cls=vor_radio, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
