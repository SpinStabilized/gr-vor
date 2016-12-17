# gr-vor

A VOR radio built on GNU Radio. More to come. Probably merge as an example or an app in my [gr-airnav][1] library in the near future. The `VOR_flowgraph.png` file in the images directory shows an overview snapshot of a working version of the flow so folks can look at it without having to download the flowgraph first. I wil try to keep this current to any major structural changes but can't promise it will stay up to date as I am continuing a lot of development work.

## Phase Shift Note

A couple equations I worked out for phase shifting in time using the [`Delay`][2] block. There is nothing ground breaking here and I am sure most DSP practitioners would consider this very basic but I had to account for a phase delay in one of the processing pipelines and didn't find these equations written down explicitly anywhere.

### Minimum Sample Rate

Depending on the resolution of the frequency shift you'll need a minimum sampling frequency. This equation tells you the minimum sample rate for a phase resolution in:

* Degrees

  ```python
  samp_rate = (360 * target_frequency) / phase_resolution
  ```

* Radians

  ```python
  samp_rate = ((2/math.pi) * target_frequency) / phase_resolution
  ```

Where a single sample shift with the `Delay` block will equal 1 resolution unit of phase shift.

### Delays For A Shift

Once you're satisfied you're at a sampling rate that meets your phase control resolution needs, you'll want to know how many samples to delay to meet your shift requirement.

* Degrees

  ```python
  delay = (phase_shift * samp_rate) / (target_frequency * 360)
  ```

* Radians

  ```python
  delay = (phase_shift * samp_rate) / (target_frequency * (2* math.pi))
  ```

## Sample Data Sources

Planning to gather some more sample files for testing (as well as field test) soon.

* `sample_data/RBT_VOR_Sample_32768kHz.raw`

  Sourced from the wave file sample on the website of [sylvain (F4GKR)][4]. Down-sampled to 32,768 samples/second and saved as a complex, GNURadio compatible file. Source VOR is the [Rambouillet VOR][5] in France. The identifier is RBT (.-. -... -). I estimate the radial the data is taken from based on the website as being 291 deg (magnetic). I've used this for phase-delay calibrations but we'll see how accurate I am when I take the radio out to capture more data.


## VOR Signal Reference

Referenced from the [Wikipedia VOR Article][3].

| GNURadio Variable  | Description                          | Value    |
|--------------------|--------------------------------------|---------:|
| `tone_freq`        | Signal Tone                          | 30  Hz   |
| `fm_ref_freq`      | FM Reference Tone Subcarrier         | 9960 kHz |
| `fm_ref_deviation` | FM Reference Tone Max Freq Deviation | 480  Hz  |
| `ident_freq`       | Morse Ident Tones Subcarrier         | 1020  Hz |


[1]: https://github.com/SpinStabilized/gr-airnav
[2]: http://gnuradio.org/doc/doxygen/classgr_1_1blocks_1_1delay.html
[3]: https://en.wikipedia.org/wiki/VHF_omnidirectional_range
[4]: http://www.f4gkr.org/in-depth-study-of-the-vor-signals/
[5]: http://bit.ly/2hQqpSf
