# Music_Genre_Transfer


### Train & Test (only piano)
- Set up dataset
```
conda create -n {env_converter_name} -y python=3.5.4
source activate {env_converter_name}
pip install -r requirements_converter.txt
bash make_dataset.sh
```

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
source activate {env_converter_name}
bash make_pretrain_dataset.sh
```

- Start pretrain
```
source activate {env_dl_name}
patch -p0 < utils_patch.patch
python main.py --dataset_A_dir='classic' --dataset_B_dir='pop' --type='cyclegan' --model='full' --sigma_d=0 --phase='train' --input_nc=2 --output_nc=2 --epoch=100
```

- Set checkpoint directory
```
rm -rf checkpoint/BD_B2BD_D_full_0.0
mkdir -p checkpoint/BD_B2BD_D_full_0.0
mv checkpoint/classic2pop_full_0.0/* checkpoint/BD_B2BD_D_full_0.0
```

- Set up dataset
```
rm -rf datasets
source activate {env_converter_name}
bash make_dataset_2.sh
```


- Train
```
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='train' --epoch=20 --continue_train=True --input_nc=2 --output_nc=2
```

- Test
```
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='test' --which_direction='AtoB' --input_nc=2 --output_nc=2
python main.py --dataset_A_dir='BD_B' --dataset_B_dir='BD_D' --type='cyclegan' --model='full' --sigma_d=0 --phase='test' --which_direction='BtoA' --input_nc=2 --output_nc=2
```

### Demo
```
source activate {env_converter_name}
gdown https://drive.google.com/uc?id=1i_0AFIxCT-tOl8eauVt_mwiFwJK43xmz
tar -zxvf checkpoint.tar.gz
python demo.py
```
