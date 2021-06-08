import os
import argparse
import os
import json
import numpy as np
import errno
import pypianoroll
from pypianoroll import Multitrack, Track
import pretty_midi
import shutil

origin_midi_path = './MIDI/data'


def get_midi_path(root):
    """Return a list of paths to MIDI files in `root` (recursively)"""
    filepaths = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.mid'):
                filepaths.append(os.path.join(dirpath, filename))
    return filepaths


def print_instruments(f, midi_paths):
    sucess_list = []
    fail_list = []
    sucess_cnt = 0
    fail_cnt = 0
    total_cnt = 0
    for midi_path in midi_paths:
        total_cnt = total_cnt+1
        try:
            midi_name = os.path.splitext(os.path.basename(midi_path))[0]
            print("analysising midi : ", midi_name)
            pm = pretty_midi.PrettyMIDI(midi_path)
            instrument_list = pm.instruments
            sucess_list.append(midi_name)
            sucess_cnt = sucess_cnt+1
            for element in instrument_list:
                f.write(str(element)+"\n")
            # f.write(pm.instruments)
            # print(pm.instruments)

        except:
            print("\t\terror in ", midi_name)
            fail_list.append(midi_name)
            fail_cnt = fail_cnt+1
    return sucess_cnt, fail_cnt, total_cnt, sucess_list, fail_list


def main():
    midi_paths = get_midi_path(origin_midi_path)
    f = open("analysis_result.txt", 'w')
    sucess_cnt, fail_cnt, total_cnt, sucess_list, fail_list = print_instruments(f, midi_paths)
    print("Total : {} Sucessed : {} Failed : {}\n".format(total_cnt, sucess_cnt, fail_cnt))
    print("Failed list :\n {}\n".format(fail_list))

if __name__ == "__main__":
    main()
