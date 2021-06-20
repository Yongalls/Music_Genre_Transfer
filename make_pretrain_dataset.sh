#!/bin/sh

python convert_double_clean.py --midi_dir='./pretrain_data/Pop' --npy_dir='./pretrain_data_npy/Pop'
python convert_double_clean.py --midi_dir='./pretrain_data/Jazz' --npy_dir='./pretrain_data_npy/Jazz'
python convert_double_clean.py --midi_dir='./pretrain_data/Classic' --npy_dir='./pretrain_data_npy/Classic'

# make pretrain dataset folder
mkdir datasets
mkdir -p datasets/classic/train
mkdir -p datasets/pop/train
mkdir -p datasets/Mixed

# copy contents
cp ./pretrain_data_npy/Classic/* datasets/classic/train
cp ./pretrain_data_npy/Pop/* datasets/pop/train

cp ./pretrain_data_npy/Classic/* datasets/Mixed
cp ./pretrain_data_npy/Pop/* datasets/Mixed
cp ./pretrain_data_npy/Jazz/* datasets/Mixed
