"""
Mollview - primitive skymap image

Arguments:
  in_field: payload field name for skymap
  title: title to put on image
  units: unit label text
  coord: 'C' celestial, 'E' ecliptic, 'G' galactic; list of conversion
  filename: output filename, {0} module name, {1} count, {2} burst_id
  range: (optional, default none), none, (min,) or (min,max)
  min: minimum value (default 0)
  max: maximum value (default -1). If max <= min, get max from data
  on: list of 'alert', 'reset', 'revoke', 'report' (default ['alert'])
"""
import logging
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp

from snewpdag.dag import Node
from snewpdag.values import LMap

class Mollview(Node):
  def __init__(self, in_field, title, units, coord, filename, **kwargs):
    self.in_field = in_field
    self.title = title
    self.units = units
    self.coord = coord
    self.filename = filename
    self.range = kwargs.pop('range', None)
    #self.min = kwargs.pop('min', 0)
    #self.max = kwargs.pop('max', -1)
    self.on = kwargs.pop('on', ['alert'])
    self.count = 0
    super().__init__(**kwargs)

  def plot(self, data):
    burst_id = data.get('burst_id', 0)
    if self.in_field in data:
      m = data[self.in_field]
      # replace a lot of these options later
      kwargs = {}
      if isinstance(self.range, (list, tuple, np.ndarray)):
        if len(self.range) >= 1:
          kwargs['min'] = self.range[0]
        if len(self.range) >= 2:
          kwargs['max'] = self.range[1]
      hp.mollview(m,
                  coord=self.coord,
                  title=self.title,
                  unit=self.units,
                  #min=self.min,
                  #max=self.max,
                  nest=True,
                  **kwargs,
                 )
      hp.graticule()
      fname = self.filename.format(self.name, self.count, burst_id)
      plt.savefig(fname)
      self.count += 1
    return True

  def alert(self, data):
    logging.debug('{}: alert'.format(self.name))
    return self.plot(data) if 'alert' in self.on else True

  def revoke(self, data):
    logging.debug('{}: revoke'.format(self.name))
    return self.plot(data) if 'revoke' in self.on else True

  def reset(self, data):
    logging.debug('{}: reset'.format(self.name))
    return self.plot(data) if 'reset' in self.on else True

  def report(self, data):
    logging.debug('{}: report'.format(self.name))
    return self.plot(data) if 'report' in self.on else True

