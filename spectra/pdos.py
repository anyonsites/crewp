
import csv
import numpy as np
import pandas as pd
from crewp.spectra.func_distrib import gaussian, slater

class PDOS:

    def __init__(self, pdos_df):
        self.pdos_df = pdos_df

    def shift_fermi(self, fermi):
        en_arry = self.pdos_df.index.values
        en_arry -= fermi
        self.pdos_df.set_index(en_arry)

    def ldos1d(self, coordinates, axis=0, margin=1., broaden='Slater'):
        '''
        !!!
        Move this to new class after all features are developed.
        !!!
        1D-LDOS from atomic resolved PDOS:
            rho(x,E) = Sum_i rho_i(E) Delta(x-x_i) 
            for i in all atoms,
            Delta(x) could be broadening function of Gaussian, Lorentzian ...
        coordinates: All atom 3D-array, must match the order in self.pdos_df columns.
        axis: broadening LDOS along 0, 1, 2; for x, y, z, respectively.
        '''
        self.pdos_df = self.pdos_df.sum(axis=1, level=[0])
        atom_idx_list = self.pdos_df.columns.values
        atom_positions = coordinates[ atom_idx_list, axis ]
        x_arry = np.linspace(np.amin(atom_positions)-margin, np.amax(atom_positions)+margin, 1000 )
        en_arry = self.pdos_df.index.values
        ldos = np.zeros((x_arry.size, en_arry.size))
        for i, atom_idx in enumerate(atom_idx_list):
            x_mesh, en_mesh = np.meshgrid( x_arry, self.pdos_df.loc[:, atom_idx] , indexing='ij')
            if broaden=='Gaussian':
                ldos += en_mesh * gaussian( x_mesh, atom_positions[i], sigma=.5)
            elif broaden=='Slater':
                ldos += en_mesh * slater( x_mesh, atom_positions[i], sigma=3.2*0.247/0.529177249 )
        return ldos, x_arry, en_arry

    def write_df(self, fname='pdos_df.dat'):
        self.pdos_df.to_csv(
                fname, 
                float_format='%15.10e', 
                sep=' ', 
                quoting=csv.QUOTE_NONE, escapechar=" ", 
                #header=,
                )

    def read_df(self, fname='pdos_df.dat', header=[0,1]):
        '''
        header = [0] for atomic resolved.
        header = [0, 1] for shell resolved.
        '''
        self.pdos_df = pd.read_csv( 
                fname, 
                header=header, 
                delim_whitespace=True, 
                #index_col=,
                #names=,
                ) 
        '''
        !!!
        read_csv change column order
        !!!
        '''
        col_idx = self.pdos_df.columns
        col_idx = col_idx.set_levels(col_idx.levels[0].astype(int), level=0)
        self.pdos_df.columns = col_idx

    '''
    Methods only for return things
    '''

