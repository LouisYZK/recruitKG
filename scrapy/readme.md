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

关于几个实体提取和关系识别的版本：
- get_enti_and_know: 初始版本，使用复旦CN-DBpediaAPI 不能大规模调用，速度较慢
- get_enti_and_know_v2: 实现版本，更换成baidu-API实体识别，zhishi.meAPI关系提取。问题是前者有QPS限制，后者返回JSON设计不规范，需要编写大量规则提取，且有时访问失败。
- get_enti_and_know_api: v2版本封装成api调用
