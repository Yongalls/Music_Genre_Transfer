# Music_Genre_Transfer

### Set Up Dataset
```
conda create -n {env_converter_name} -y python=3.5.4
source activate {env_converter_name}
pip install -r requirements_converter.txt
bash make_dataset.sh
```

### Train & Test
- Set up environment
```
conda create -n {env_dl_name} -y python=3.5.4
source activate {env_dl_name}
pip install -r requirements.txt
```

- Train
```
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='train'
```

- Test
```
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='test' --which_direction='AtoB'
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='test' --which_direction='BtoA'
```
