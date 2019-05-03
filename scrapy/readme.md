# get postion data from zhilian recruite

apply a multi-thread spider on some apis.

run:

```bash
sh ./run.sh
```

jupyter数据科学环境终端部署：

安装conda和jupyter之后，需要手动配置jupyter的多个kernel.

```bash
conda env create myenv --python=3.6
source activate myenv
conda isntall ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)" 
```
之后启动jupyter会自动绑定虚拟环境的kernel.