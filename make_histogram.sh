rm -rf histograms/
mkdir histograms

rm analysis_result.txt
python analysis_midi.py --midi_dir='./MIDI/datasets/BD_B'
python analysis_midi.py --midi_dir='./MIDI/datasets/BD_D'
echo "our dataset"
python histogram.py
mv histogram.png histograms/ours_entire.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./old_dataset/Classic'
python analysis_midi.py --midi_dir='./old_dataset/Jazz'
python analysis_midi.py --midi_dir='./old_dataset/Pop'
echo "original dataset"
python histogram.py
mv histogram.png histograms/original_entire.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./MIDI/datasets/BD_B/train'
echo "our dataset ballad train"
python histogram.py
mv histogram.png histograms/ours_ballad_train.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./MIDI/datasets/BD_D/train'
echo "our dataset dance train"
python histogram.py
mv histogram.png histograms/ours_dance_train.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./MIDI/datasets/Mixed'
echo "our dataset mixed"
python histogram.py
mv histogram.png histograms/ours_mixed.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./old_dataset/Classic'
echo "original dataset classic"
python histogram.py
mv histogram.png histograms/original_classic.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./old_dataset/Jazz'
echo "original dataset jazz"
python histogram.py
mv histogram.png histograms/original_jazz.png

rm analysis_result.txt
python analysis_midi.py --midi_dir='./old_dataset/Pop'
echo "original dataset pop"
python histogram.py
mv histogram.png histograms/original_pop.png
