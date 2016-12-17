#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: VOR Radio
# Author: Brian McLaughlin
# Description: Decodes a VOR signal
# Generated: Fri Dec 16 20:08:37 2016
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
from optparse import OptionParser
import airnav
import math
import sip
import sys
import utility  # embedded python module


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
        self.tone_samp_rate = tone_samp_rate = 2**9
        self.tone_freq = tone_freq = 30
        self.tone_bandpass_width = tone_bandpass_width = 5
        self.pll_tracking_range = pll_tracking_range = 100
        self.pll_bandwidth = pll_bandwidth = (1.5 * math.pi)/200
        self.input_samp_rate = input_samp_rate = 2**15
        self.ident_freq = ident_freq = 1020
        self.fm_ref_freq = fm_ref_freq = 9960
        self.fm_ref_deviation = fm_ref_deviation = 480
        self.fm_lowpass_width = fm_lowpass_width = 1000
        self.fm_lowpass_cutoff = fm_lowpass_cutoff = 5000
        self.fm_demod_samp_rate = fm_demod_samp_rate = 2**12
        self.am_demod_lowpass_width = am_demod_lowpass_width = 400
        self.am_demod_lowpass_cutoff = am_demod_lowpass_cutoff = 500

        ##################################################
        # Blocks
        ##################################################
        self.monitoring_tabs = Qt.QTabWidget()
        self.monitoring_tabs_widget_0 = Qt.QWidget()
        self.monitoring_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.monitoring_tabs_widget_0)
        self.monitoring_tabs_grid_layout_0 = Qt.QGridLayout()
        self.monitoring_tabs_layout_0.addLayout(self.monitoring_tabs_grid_layout_0)
        self.monitoring_tabs.addTab(self.monitoring_tabs_widget_0, "Baseband")
        self.monitoring_tabs_widget_1 = Qt.QWidget()
        self.monitoring_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.monitoring_tabs_widget_1)
        self.monitoring_tabs_grid_layout_1 = Qt.QGridLayout()
        self.monitoring_tabs_layout_1.addLayout(self.monitoring_tabs_grid_layout_1)
        self.monitoring_tabs.addTab(self.monitoring_tabs_widget_1, "Ident Signal")
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
        self.baseband_tabs = Qt.QTabWidget()
        self.baseband_tabs_widget_0 = Qt.QWidget()
        self.baseband_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.baseband_tabs_widget_0)
        self.baseband_tabs_grid_layout_0 = Qt.QGridLayout()
        self.baseband_tabs_layout_0.addLayout(self.baseband_tabs_grid_layout_0)
        self.baseband_tabs.addTab(self.baseband_tabs_widget_0, "Spectrum")
        self.baseband_tabs_widget_1 = Qt.QWidget()
        self.baseband_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.baseband_tabs_widget_1)
        self.baseband_tabs_grid_layout_1 = Qt.QGridLayout()
        self.baseband_tabs_layout_1.addLayout(self.baseband_tabs_grid_layout_1)
        self.baseband_tabs.addTab(self.baseband_tabs_widget_1, "Waterfall")
        self.monitoring_tabs_layout_0.addWidget(self.baseband_tabs)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=2**10 // 40,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	input_samp_rate, #bw
        	"VOR Baseband Waterfall", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        
        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [6, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-130, -60)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.baseband_tabs_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
        	40 * 4, #size
        	40, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-2.5, 2.5)
        
        self.qtgui_time_sink_x_2.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_2.enable_tags(-1, True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.1, 0.1, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_2.disable_legend()
        
        labels = ["", "", "", "", "",
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
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.pyqwidget(), Qt.QWidget)
        self.monitoring_tabs_layout_1.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	tone_samp_rate, #size
        	tone_samp_rate, #samp_rate
        	"Compared Signals", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-25, 25)
        
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
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")
        
        labels = ["Radial", "", "", "", "",
                  "", "", "", "", ""]
        units = ["degrees", "", "", "", "",
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
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	input_samp_rate, #bw
        	"VOR Baseband Signal", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-150, -60)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.baseband_tabs_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_1 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, 2**10, 16, 16, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, input_samp_rate, am_demod_lowpass_cutoff, am_demod_lowpass_width, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccf(input_samp_rate // 2**10, (firdes.low_pass(10000, input_samp_rate, 500, 500)), ident_freq, input_samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(input_samp_rate // fm_demod_samp_rate, (firdes.low_pass(1000, input_samp_rate, fm_lowpass_cutoff, fm_lowpass_width)), fm_ref_freq, input_samp_rate)
        self.fft_vxx_0_0 = fft.fft_vfc(tone_samp_rate, True, (window.blackmanharris(tone_samp_rate)), 1)
        self.fft_vxx_0 = fft.fft_vfc(tone_samp_rate, True, (window.blackmanharris(tone_samp_rate)), 1)
        self.dc_blocker_xx_1 = filter.dc_blocker_ff(32, True)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, tone_samp_rate)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, tone_samp_rate)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, input_samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(1, 1, 0)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, tone_samp_rate)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, tone_samp_rate)
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, tone_freq)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, tone_freq)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((180 / math.pi, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((500, ))
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, tone_samp_rate)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, tone_samp_rate)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/home/brian/gnur-projects/gr-vor/sample_data/RBT_VOR_Sample_32768kHz.raw", True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 82)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_arg_0_0 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.band_pass_filter_0_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, tone_samp_rate, tone_freq - tone_bandpass_width, tone_freq + tone_bandpass_width, tone_bandpass_width, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_fff(input_samp_rate // tone_samp_rate, firdes.band_pass(
        	800, input_samp_rate, tone_freq - tone_bandpass_width, tone_freq + tone_bandpass_width, tone_bandpass_width, firdes.WIN_HAMMING, 6.76))
        self.analog_pll_carriertracking_cc_0_0 = analog.pll_carriertracking_cc(pll_bandwidth, utility.hz_to_rad_per_sample(pll_tracking_range, input_samp_rate), utility.hz_to_rad_per_sample(-pll_tracking_range, input_samp_rate))
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=fm_demod_samp_rate,
        	audio_decim=fm_demod_samp_rate // tone_samp_rate,
        	deviation=fm_ref_deviation,
        	audio_pass=tone_freq,
        	audio_stop=tone_freq * 2,
        	gain=1.0,
        	tau=0.0,
        )
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=input_samp_rate,
        	audio_decim=1,
        	audio_pass=tone_freq,
        	audio_stop=tone_freq * 2,
        )
        self.analog_agc2_xx_0_0 = analog.agc2_ff(1e-1, 1e-2, 1.0, 1.0)
        self.analog_agc2_xx_0_0.set_max_gain(65536)
        self.analog_agc2_xx_0 = analog.agc2_ff(1e-1, 1e-2, 1.0, 1)
        self.analog_agc2_xx_0.set_max_gain(65536)
        self.airnav_unitcircle_ff_0 = airnav.unitcircle_ff()
        self.airnav_qt_ident_0 = self.airnav_qt_ident_0 = airnav.qt_ident()
        self.top_layout.addWidget(self.airnav_qt_ident_0)
          
        self.airnav_morse_decode_0 = airnav.morse_decode(10, 40)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.airnav_morse_decode_0, 'out'), (self.airnav_qt_ident_0, 'in'))    
        self.connect((self.airnav_unitcircle_ff_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_stream_to_vector_0_0, 0))    
        self.connect((self.analog_agc2_xx_0, 0), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.analog_agc2_xx_0_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.analog_agc2_xx_0_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.analog_am_demod_cf_0, 0), (self.band_pass_filter_0_0, 0))    
        self.connect((self.analog_fm_demod_cf_0, 0), (self.band_pass_filter_0_0_0, 0))    
        self.connect((self.analog_pll_carriertracking_cc_0_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.analog_pll_carriertracking_cc_0_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.analog_pll_carriertracking_cc_0_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.analog_pll_carriertracking_cc_0_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.analog_pll_carriertracking_cc_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    
        self.connect((self.band_pass_filter_0_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.band_pass_filter_0_0_0, 0), (self.dc_blocker_xx_1, 0))    
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.blocks_complex_to_arg_0_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_float_to_uchar_0, 0), (self.airnav_morse_decode_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_arg_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_complex_to_arg_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_number_sink_0, 0))    
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_keep_one_in_n_0, 0))    
        self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.airnav_unitcircle_ff_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_uchar_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.qtgui_time_sink_x_2, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.analog_pll_carriertracking_cc_0_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_skiphead_0_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.analog_agc2_xx_0_0, 0))    
        self.connect((self.dc_blocker_xx_1, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_am_demod_cf_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_threshold_ff_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vor_radio")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_tone_samp_rate(self):
        return self.tone_samp_rate

    def set_tone_samp_rate(self, tone_samp_rate):
        self.tone_samp_rate = tone_samp_rate
        self.blocks_keep_one_in_n_0.set_n(self.tone_samp_rate)
        self.blocks_keep_one_in_n_0_0.set_n(self.tone_samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.tone_samp_rate)
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.tone_samp_rate, self.tone_freq - self.tone_bandpass_width, self.tone_freq + self.tone_bandpass_width, self.tone_bandpass_width, firdes.WIN_HAMMING, 6.76))

    def get_tone_freq(self):
        return self.tone_freq

    def set_tone_freq(self, tone_freq):
        self.tone_freq = tone_freq
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(800, self.input_samp_rate, self.tone_freq - self.tone_bandpass_width, self.tone_freq + self.tone_bandpass_width, self.tone_bandpass_width, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.tone_samp_rate, self.tone_freq - self.tone_bandpass_width, self.tone_freq + self.tone_bandpass_width, self.tone_bandpass_width, firdes.WIN_HAMMING, 6.76))

    def get_tone_bandpass_width(self):
        return self.tone_bandpass_width

    def set_tone_bandpass_width(self, tone_bandpass_width):
        self.tone_bandpass_width = tone_bandpass_width
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(800, self.input_samp_rate, self.tone_freq - self.tone_bandpass_width, self.tone_freq + self.tone_bandpass_width, self.tone_bandpass_width, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.tone_samp_rate, self.tone_freq - self.tone_bandpass_width, self.tone_freq + self.tone_bandpass_width, self.tone_bandpass_width, firdes.WIN_HAMMING, 6.76))

    def get_pll_tracking_range(self):
        return self.pll_tracking_range

    def set_pll_tracking_range(self, pll_tracking_range):
        self.pll_tracking_range = pll_tracking_range
        self.analog_pll_carriertracking_cc_0_0.set_max_freq(utility.hz_to_rad_per_sample(self.pll_tracking_range, self.input_samp_rate))
        self.analog_pll_carriertracking_cc_0_0.set_min_freq(utility.hz_to_rad_per_sample(-self.pll_tracking_range, self.input_samp_rate))

    def get_pll_bandwidth(self):
        return self.pll_bandwidth

    def set_pll_bandwidth(self, pll_bandwidth):
        self.pll_bandwidth = pll_bandwidth
        self.analog_pll_carriertracking_cc_0_0.set_loop_bandwidth(self.pll_bandwidth)

    def get_input_samp_rate(self):
        return self.input_samp_rate

    def set_input_samp_rate(self, input_samp_rate):
        self.input_samp_rate = input_samp_rate
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(800, self.input_samp_rate, self.tone_freq - self.tone_bandpass_width, self.tone_freq + self.tone_bandpass_width, self.tone_bandpass_width, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((firdes.low_pass(10000, self.input_samp_rate, 500, 500)))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.input_samp_rate, self.am_demod_lowpass_cutoff, self.am_demod_lowpass_width, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1000, self.input_samp_rate, self.fm_lowpass_cutoff, self.fm_lowpass_width)))
        self.blocks_throttle_0.set_sample_rate(self.input_samp_rate)
        self.analog_pll_carriertracking_cc_0_0.set_max_freq(utility.hz_to_rad_per_sample(self.pll_tracking_range, self.input_samp_rate))
        self.analog_pll_carriertracking_cc_0_0.set_min_freq(utility.hz_to_rad_per_sample(-self.pll_tracking_range, self.input_samp_rate))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.input_samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.input_samp_rate)

    def get_ident_freq(self):
        return self.ident_freq

    def set_ident_freq(self, ident_freq):
        self.ident_freq = ident_freq
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.ident_freq)

    def get_fm_ref_freq(self):
        return self.fm_ref_freq

    def set_fm_ref_freq(self, fm_ref_freq):
        self.fm_ref_freq = fm_ref_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.fm_ref_freq)

    def get_fm_ref_deviation(self):
        return self.fm_ref_deviation

    def set_fm_ref_deviation(self, fm_ref_deviation):
        self.fm_ref_deviation = fm_ref_deviation

    def get_fm_lowpass_width(self):
        return self.fm_lowpass_width

    def set_fm_lowpass_width(self, fm_lowpass_width):
        self.fm_lowpass_width = fm_lowpass_width
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1000, self.input_samp_rate, self.fm_lowpass_cutoff, self.fm_lowpass_width)))

    def get_fm_lowpass_cutoff(self):
        return self.fm_lowpass_cutoff

    def set_fm_lowpass_cutoff(self, fm_lowpass_cutoff):
        self.fm_lowpass_cutoff = fm_lowpass_cutoff
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1000, self.input_samp_rate, self.fm_lowpass_cutoff, self.fm_lowpass_width)))

    def get_fm_demod_samp_rate(self):
        return self.fm_demod_samp_rate

    def set_fm_demod_samp_rate(self, fm_demod_samp_rate):
        self.fm_demod_samp_rate = fm_demod_samp_rate

    def get_am_demod_lowpass_width(self):
        return self.am_demod_lowpass_width

    def set_am_demod_lowpass_width(self, am_demod_lowpass_width):
        self.am_demod_lowpass_width = am_demod_lowpass_width
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.input_samp_rate, self.am_demod_lowpass_cutoff, self.am_demod_lowpass_width, firdes.WIN_HAMMING, 6.76))

    def get_am_demod_lowpass_cutoff(self):
        return self.am_demod_lowpass_cutoff

    def set_am_demod_lowpass_cutoff(self, am_demod_lowpass_cutoff):
        self.am_demod_lowpass_cutoff = am_demod_lowpass_cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.input_samp_rate, self.am_demod_lowpass_cutoff, self.am_demod_lowpass_width, firdes.WIN_HAMMING, 6.76))


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
