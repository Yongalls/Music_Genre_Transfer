# Music_Genre_Transfer

### Set Up Dataset
```
conda create -n {env_converter_name} -y python=3.5.4
source activate {env_converter_name}
pip install -r requirements_converter.txt
bash make_dataset.sh
```

### Train & Test (only piano)
- Set up environment
```
conda create -n {env_dl_name} -y python=3.5.4
source activate {env_dl_name}
pip install -r requirements.txt
```

- Download checkpoint file
```
gdown https://drive.google.com/uc?id=1dgbup3s6DfoZxREoZl8TmRTs9Djl_bZe
tar -zxvf checkpoint.tar.gz
```

- Train
```
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='train' --epoch=20 --continue_train=True
```

- Test
```
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='test' --which_direction='AtoB'
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='test' --which_direction='BtoA'
```

### Train & Test (piano & enssemble)
#### Start with clean state
- Make pretrain dataset
```
rm -rf datasets
bash make_pretrain_dataset.sh
```

- Start pretrain
```
patch -p0 < utils_patch.patch
python main.py --dataset_A_dir='classic' --dataset_B_dir='pop' --type='cyclegan' --model='full' --sigma_d=0 --phase='train' --input_nc=2 --output_nc=2 --epoch=10
```