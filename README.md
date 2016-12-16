# gr-vor

A VOR radio built on GNU Radio. More to come. Probably merge as an example or an app in my gr-airnav library in the near future.

## Phase Shift Note

A couple equations I worked out for phase shifting in time using the `Delay` block. There is nothing ground breaking here but I had to account for a phase delay in one of the processing pipelines and didn't find these equations written down explicitly anywhere.

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
