#!/bin/bash

## 运行该脚本，执行heudiconv读取DICOM文件信息

# -v：挂载数据存储地址
# -d：输入的路径，从/base开始，使用*表示不同的protocols
# -f：指定convertall来转换.tsv文件并读取原始信息
# -s：指定被试编号
# -ss：指定session编号
# 可以根据需要修改{subject}和{session}的值

docker run --rm -it -v /Users/wu_script:/base nipy/heudiconv:latest \
-d /base/Dicom/sub-{subject}/ses-{session}/*/DICOM/*.dcm \
-o /base/Nifti/ -f convertall -s 04 -ss 001 -c none --overwrite

