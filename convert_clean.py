from __future__ import print_function
import os
import json
import numpy as np
import errno
import pypianoroll
from pypianoroll import Multitrack, Track
import pretty_midi
import shutil

# change data_path & converted_path

ROOT_PATH = '.'
data_path = os.path.join(ROOT_PATH, 'MIDI/datasets/BD_D/test')
converted_path = os.path.join(ROOT_PATH, 'datasets/BD_D/test')
LAST_BAR_MODE = 'remove'


def make_sure_path_exists(path):
    """Create all intermediate-level directories if the given path does not
    exist"""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_midi_path(root):
    """Return a list of paths to MIDI files in `root` (recursively)"""
    filepaths = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.mid'):
                filepaths.append(os.path.join(dirpath, filename))
    return filepaths


def get_midi_info(pm):
    """Return useful information from a pretty_midi.PrettyMIDI instance"""
    if pm.time_signature_changes:
        pm.time_signature_changes.sort(key=lambda x: x.time)
        first_beat_time = pm.time_signature_changes[0].time
    else:
        first_beat_time = pm.estimate_beat_start()

    tc_times, tempi = pm.get_tempo_changes()

    if len(pm.time_signature_changes) == 1:
        time_sign = '{}/{}'.format(pm.time_signature_changes[0].numerator,
                                   pm.time_signature_changes[0].denominator)
    else:
        time_sign = None

    midi_info = {
        'first_beat_time': first_beat_time,
        'num_time_signature_change': len(pm.time_signature_changes),
        'time_signature': time_sign,
        'tempo': tempi[0] if len(tc_times) == 1 else None
    }

    return midi_info


def midi_filter(midi_info, midi_name):
    """Return True for qualified midi files and False for unwanted ones"""
    if midi_info['first_beat_time'] > 0.0:
        #print("first beat", midi_name)
        return False
    elif midi_info['num_time_signature_change'] > 1:
        #print("beat change", midi_name)
        return False
    elif midi_info['time_signature'] not in ['4/4']:
        #print("total beat", midi_name)
        return False
    #print("ok", midi_name)
    return True


def get_merged(multitrack, midi_name):
    """Return a `pypianoroll.Multitrack` instance with piano-rolls merged to
    five tracks (Bass, Drums, Guitar, Piano and Strings)"""
    category_list = {'Piano': [], 'Drums': []}
    program_dict = {'Piano': 0, 'Drums': 0}

    for idx, track in enumerate(multitrack.tracks):
        if track.is_drum:
            category_list['Drums'].append(idx)
        else:
            category_list['Piano'].append(idx)

    merged = multitrack[category_list['Piano']].get_merged_pianoroll()
    pr = get_bar_piano_roll(merged)
    pr_clip = pr[:, :, 24:108]
    if int(pr_clip.shape[0] % 4) != 0:
        pr_clip = np.delete(pr_clip, np.s_[-int(pr_clip.shape[0] % 4):], axis=0)
    pr_re = pr_clip.reshape(-1, 64, 84, 1)
    return pr_re

def get_bar_piano_roll(piano_roll):
    if int(piano_roll.shape[0] % 64) is not 0:
        if LAST_BAR_MODE == 'fill':
            piano_roll = np.concatenate((piano_roll, np.zeros((64 - piano_roll.shape[0] % 64, 128))), axis=0)
        elif LAST_BAR_MODE == 'remove':
            piano_roll = np.delete(piano_roll,  np.s_[-int(piano_roll.shape[0] % 64):], axis=0)
    piano_roll = piano_roll.reshape(-1, 64, 128)
    return piano_roll
    

def converter(filepath):
    """Save a multi-track piano-roll converted from a MIDI file to target
    dataset directory and update MIDI information to `midi_dict`"""
    try:
        midi_name = os.path.splitext(os.path.basename(filepath))[0]
        multitrack = Multitrack(beat_resolution=4, name=midi_name)
        pm = pretty_midi.PrettyMIDI(filepath)
        midi_info = get_midi_info(pm)
        multitrack.parse_pretty_midi(pm)
        merged = get_merged(multitrack, midi_name)
        print(midi_name, " merged: ", merged.shape)
        return merged
    except:
        print("\t\terror in ", midi_name)
        return None 



def main():
    """Main function of the converter"""
    midi_paths = get_midi_path(data_path)
    npys = [converter(midi_path) for midi_path in midi_paths]
    count = 0
    converted_list = []
    for npy in npys:
        if npy is not None:
            count += 1
            converted_list.append(npy)
    
    total_npy = np.concatenate(converted_list, axis=0)
    print("total npy: ", total_npy.shape)

    make_sure_path_exists(converted_path)
    print("num of npy: ", total_npy.shape[0])
    for i in range(total_npy.shape[0]):
        np.save(os.path.join(converted_path, 'kpop_{}.npy'.format(i+1)), total_npy[i])

    print("[Done] {} files out of {} have been successfully cleaned".format(count, len(npys)))


if __name__ == "__main__":
    main()
