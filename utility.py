# this module will be imported in the into your flowgraph
import math

def hz_to_rad_per_sample(f_hz, sample_rate):
    return f_hz * ((2 * math.pi) / sample_rate)
