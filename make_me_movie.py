'''
This windows-based script iterates within a directory and produces movie using ffmpeg. Particularly this code generates movies for ion density plots however can be readily modified by changing return variable within the file_name function.
'''

import os
import subprocess

O_ions = [5, 6, 7, 8]
C_ions = [2, 4]
N_ions = [5]
Mg_ions = [2, 10]
Si_ions = [3, 4, 5, 6]
Ne_ions = [2, 4, 5, 8]
H_ions = [2]

axes = ['x', 'z']
ions = {'O': O_ions, 'C': C_ions, 'N': N_ions, 'Mg': Mg_ions, 'Si': Si_ions, 'Ne': Ne_ions, 'H': H_ions}

def file_name(axis, atom, ion):
    literal = '%04d'
    return 'DD%s_Projection_%s_%s_p%s_density.png' % (literal, axis, atom, ion)

for axis in axes:
    for atom in ions.keys():
        for ion in ions.get(atom):
            path = '/' + atom + '/' + axis + '/' + atom + '_density/' + atom + '_' + str(ion)
            cwd = os.getcwd()
            cwd_path = cwd + path
            os.chdir(cwd_path)
            cmd = 'ffmpeg -r 45 -f image2 -s 1920x1080 -start_number 3 -i %s \
                 -vf scale=1600:800 -vframes 1200 -vcodec libx264 -crf 25 -pix_fmt yuv420p comp_%s_%s_density.mp4' % (file_name(axis, atom, ion), atom, ion)
            print('\n' + cwd_path + ' in ' + cmd)
            os.chdir('../../../..')

#DD0008_Projection_z_Mg_p1_density
#DD0004_Projection_x_O_p5_density

