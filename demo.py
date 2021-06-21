from flask import Flask, request, render_template
from model import cyclegan
from convert_single import converter
import tensorflow as tf
import numpy as np
import os
import argparse
import time

tf.set_random_seed(19)
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
app = Flask(__name__)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--dataset_dir', dest='dataset_dir', default='JAZZ2ROCK', help='path of the dataset')
parser.add_argument('--dataset_A_dir', dest='dataset_A_dir', default='JC_J', help='path of the dataset of domain A')
parser.add_argument('--dataset_B_dir', dest='dataset_B_dir', default='JC_C', help='path of the dataset of domain B')
parser.add_argument('--epoch', dest='epoch', type=int, default=100, help='# of epoch')
parser.add_argument('--epoch_step', dest='epoch_step', type=int, default=10, help='# of epoch to decay lr')
parser.add_argument('--batch_size', dest='batch_size', type=int, default=16, help='# images in batch')
parser.add_argument('--train_size', dest='train_size', type=int, default=1e8, help='# images used to train')
parser.add_argument('--load_size', dest='load_size', type=int, default=286, help='scale images to this size')
parser.add_argument('--fine_size', dest='fine_size', type=int, default=128, help='then crop to this size')
parser.add_argument('--time_step', dest='time_step', type=int, default=64, help='time step of pianoroll')
parser.add_argument('--pitch_range', dest='pitch_range', type=int, default=84, help='pitch range of pianoroll')
parser.add_argument('--ngf', dest='ngf', type=int, default=64, help='# of gen filters in first conv layer')
parser.add_argument('--ndf', dest='ndf', type=int, default=64, help='# of discri filters in first conv layer')
parser.add_argument('--input_nc', dest='input_nc', type=int, default=1, help='# of input image channels')
parser.add_argument('--output_nc', dest='output_nc', type=int, default=1, help='# of output image channels')
parser.add_argument('--lr', dest='lr', type=float, default=0.0002, help='initial learning rate for adam')
parser.add_argument('--beta1', dest='beta1', type=float, default=0.5, help='momentum term of adam')
parser.add_argument('--which_direction', dest='which_direction', default='AtoB', help='AtoB or BtoA')
parser.add_argument('--phase', dest='phase', default='train', help='train, test')
parser.add_argument('--save_freq', dest='save_freq', type=int, default=1000, help='save a model every save_freq iterations')
parser.add_argument('--print_freq', dest='print_freq', type=int, default=100, help='print the debug information every print_freq iterations')
parser.add_argument('--continue_train', dest='continue_train', type=bool, default=False, help='if continue training, load the latest model: 1: true, 0: false')
parser.add_argument('--checkpoint_dir', dest='checkpoint_dir', default='./checkpoint', help='models are saved here')
parser.add_argument('--sample_dir', dest='sample_dir', default='./samples', help='sample are saved here')
parser.add_argument('--test_dir', dest='test_dir', default='./test', help='test sample are saved here')
parser.add_argument('--log_dir', dest='log_dir', default='./log', help='logs are saved here')
parser.add_argument('--L1_lambda', dest='L1_lambda', type=float, default=10.0, help='weight on L1 term in objective')
parser.add_argument('--gamma', dest='gamma', type=float, default=1.0, help='weight of extra discriminators')
parser.add_argument('--use_midi_G', dest='use_midi_G', type=bool, default=False, help='select generator for midinet')
parser.add_argument('--use_midi_D', dest='use_midi_D', type=bool, default=False, help='select disciminator for midinet')
parser.add_argument('--use_lsgan', dest='use_lsgan', type=bool, default=False, help='gan loss defined in lsgan')
parser.add_argument('--max_size', dest='max_size', type=int, default=50, help='max size of image pool, 0 means do not use image pool')
parser.add_argument('--sigma_c', dest='sigma_c', type=float, default=1.0, help='sigma of gaussian noise of classifiers')
parser.add_argument('--sigma_d', dest='sigma_d', type=float, default=1.0, help='sigma of gaussian noise of discriminators')
parser.add_argument('--model', dest='model', default='base', help='three different models, base, partial, full')
parser.add_argument('--type', dest='type', default='cyclegan', help='cyclegan or classifier')

args = parser.parse_args()

input_midi_path = './demo/input/midi'
input_npy_path = './demo/input/npy'

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':
        midi = request.files['midi_in']
        if not os.path.exists(input_midi_path):
            os.makedirs(input_midi_path)
        midi.save(os.path.join(input_midi_path, midi.filename))

        if not midi:
            return render_template('index.html', status=False, text="No Files")

        npy, midi_name = converter(os.path.join(input_midi_path, midi.filename))

        if npy is None:
            return render_template('index.html', status=False, text="Error while converting midi to numpy")
        
        if not os.path.exists(input_npy_path):
            os.makedirs(input_npy_path)
        for f in os.listdir(input_npy_path):
            os.remove(os.path.join(input_npy_path, f))

        for i in range(npy.shape[0]):
            np.save(os.path.join(input_npy_path, '{}_{}.npy'.format(midi_name, i+1)), npy[i])

        with tf.Session() as sess:
            model = cyclegan(sess, args)
            out = model.demo(args)

        if out == False:
            return render_template('index.html', status=False, text="Load checkpoint failed")
        else:
            return render_template('index.html', status=True, text="Succesfully converted", file=out)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
