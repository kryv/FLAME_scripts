#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides lattice picture from FLAME lattice file(.lat) or FLAME Machine object."""

import numpy as np
import matplotlib.pylab as plt
import matplotlib.patches as ptc
import matplotlib.lines as lin

from flame import Machine

class BasedOn:
    """Lattice picture class from FLAME lattice file or FLAME Machine object
    
    Parameters
    ----------
    source : str or callable
        File path of the lattic file (str) or FLAME Machine object (callable)

    auto_scaling : bool (True), optional
        Flag for y-axis scaling by strength of the optical elements

    starting_offset : float (0.0), optional
        Position offset of starting point in the lattice file


    Class attributes
    ----------------
    types : dict
        Element type list of the lattice. Each element type contains
        on-off 'flag', plotting 'color', and y-axis 'scale'. 

    """
    def __init__(self, source, auto_scaling=True , starting_offset=0.0):
        self._source = source
        self._auto_scaling = auto_scaling
        self._starting_offset = starting_offset

        if type(self._source) == str:
            with open(self._source, 'rb') as lat:
                self.M = Machine(lat)

        elif type(self._source) == Machine:
            self.M = self._source

        else:
            raise ValueError('source must be a file path of .lat or flame.Machine object')

        self.types = {'rfcavity':   {'flag':True, 'color':'orange', 'scale':0.0},
                      'solenoid':   {'flag':True, 'color':'m',      'scale':0.0},
                      'quadrupole': {'flag':True, 'color':'blue',   'scale':0.0},
                      'sextupole':  {'flag':True, 'color':'purple', 'scale':0.0},
                      'sbend':      {'flag':True, 'color':'green',  'scale':0.0},
                      'equad':      {'flag':True, 'color':'navy',   'scale':0.0},
                      'edipole':    {'flag':True, 'color':'lime',   'scale':0.0},
                      'bpm':        {'flag':True, 'color':'red',    'scale':0.0},
                      'orbtrim':    {'flag':True, 'color':'black',  'scale':0.0},
                      'stripper':   {'flag':True, 'color':'y',      'scale':0.0},
                      'marker':     {'flag':True, 'color':'c',      'scale':0.0}
                      }

        if self._auto_scaling:
            for i in range(len(self.M)):
                elem = self.M.conf(i)
                if elem['type'] in self.types.keys():
                    prv_scl = self.types[elem['type']]['scale']
                    tmp_scl = np.abs(self._get_scl(elem))

                    self.types[elem['type']]['scale'] = max(prv_scl,tmp_scl)

    def _get_scl(self, elem):
        """Get arbital strength of the optical element
        """

        scl = 0.0

        if elem['type'] == 'rfcavity':
            scl = elem['scl_fac']*np.cos(2.0*np.pi*elem['phi']/360.0)
        elif elem['type'] == 'solenoid':
            scl = elem['B']
        elif elem['type'] == 'quadrupole':
            scl = elem['B2']
        elif elem['type'] == 'sextuple':
            scl = elem['B3']
        elif elem['type'] == 'sbend':
            scl = elem['phi']
        elif elem['type'] == 'equad':
            scl = elem['V']/elem['radius']**2.0
        elif elem['type'] == 'edipole':
            scl = elem['phi']

        return scl


    def generate(self, xlim=None, aspect=5.0):
        """Generate matplotlib Axes class object from lattice file

        Parameter
        ---------
        xlim : list[2], optinal
            Plot range of the lattice

        aspect : float (5.0), optional
            Aspect ratio of the picture.


        Class attribute
        ---------------
        axes : callable
            Axes class object of matplotlib.
        
        total_length : float
            Total length of the lattice.

        """

        self._fig = plt.figure()
        self.axes = self._fig.add_subplot(111)

        pos = self._starting_offset

        self.axes.add_line(lin.Line2D([-1,1e5], [0,0], color='gray'))

        for i in range(len(self.M)):
            elem = self.M.conf(i)

            try:
                dL = elem['L']
            except:
                dL = 0.0

            if elem['type'] in self.types.keys():
                info = self.types[elem['type']] 
                
                if info['flag']:
                    if dL != 0.0:
                        
                        bp = 0.0

                        if info['scale'] != 0.0:
                            ht = self._get_scl(elem)/info['scale'] + 0.05
                        else:
                            ht = 1.0
                        
                        if elem['type'] == 'rfcavity' or elem['type'] == 'solenoid':
                            bp = bp-ht
                            ht *= 2.0

                        self.axes.add_patch(ptc.Rectangle((pos, bp),dL,ht,
                                                           edgecolor='none',facecolor=info['color']))
                    else:
                        self.axes.add_line(lin.Line2D([pos,pos],[-0.1,0.1],color=info['color']))

            pos += dL

        self.total_length = pos
       
        if xlim != None:
            self.axes.set_xlim(xlim)
        else :
            self.axes.set_xlim((0.0,pos))
        
        self.axes.set_aspect(aspect)
        self.axes.set_ylim((-1.0,1.0))
        self.axes.set_yticks(())
        self.axes.grid()

        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_visible(False)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['bottom'].set_visible(False)

    def output(self,window=True,fname=None,**kwargs):
        """Output the lattice picture to window and/or file.

        Parameters
        ----------
        window : bool (True)
            Output flag to the window.

        fname : str, optional
            File path of the output picutre.

        **kwargs : 
            The same kwargs as pyplot.savefig() are available.
        """

        if type(fname) == str :
            plt.savefig(fname,**kwargs)

        if window: plt.show()


if __name__ == "__main__":
    import sys
    
    try:
        lat = sys.argv[1]
    except:
        raise ValueError('First argument must be a lattice file.')

    try:
        out = sys.argv[2]
    except:
        raise ValueError('Second argument must be a output file name.')

    pl = BasedOn(lat)
    pl.generate()
    pl.output(fname=out)
