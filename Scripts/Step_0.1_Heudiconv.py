import os

# 定义函数用于创建输出路径模板和文件类型
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    """
    创建BIDS格式输出路径的模板和文件类型。

    参数:
    - template: 字符串模板，用于定义输出路径
    - outtype: 输出文件类型（默认为 'nii.gz'）
    - annotation_classes: 其他注释类（可选）

    返回:
    - 模板、文件类型和注释类的元组
    """
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# 将DICOM序列信息映射为BIDS格式的字典
def infotodict(seqinfo):
    """
    根据扫描序列信息 (seqinfo) 创建BIDS格式的输出路径映射。

    参数:
    - seqinfo: 包含所有扫描序列信息的列表

    返回:
    - 包含序列ID和文件路径模板的字典
    """
    # 定义各类型扫描的BIDS路径模板
    taskrun1 = create_key('sub-{subject}/ses-1/func/sub-{subject}_ses-1_task-wordpic_run-1_bold')
    t1w = create_key('sub-{subject}/ses-1/anat/sub-{subject}_ses-1_run-1_T1w')
    dwi = create_key('sub-{subject}/ses-1/dwi/sub-{subject}_ses-1_run-1_dwi')

    # 初始化字典，存储每种类型的扫描序列ID
    info = {taskrun1: [], t1w: [], dwi: []}

    # 遍历所有扫描序列，匹配相应的模板
    for s in seqinfo:
        if '3_AxBOLD-1' in s.dcm_dir_name:
            info[taskrun1].append(s.series_id)  # 累积BOLD任务序列ID
        elif '5_Ax3DT1BRAVO' in s.dcm_dir_name:
            info[t1w].append(s.series_id)  # 累积T1加权结构扫描ID
        elif '7_AxDTI64Directions' in s.dcm_dir_name:
            info[dwi].append(s.series_id)  # 累积DTI扫描ID

    return info  # 返回映射结果

# 运行 Docker，将 DICOM 转换为 NIfTI 格式
docker run --rm -it \
    -v /Users/wu_script:/base \
    nipy/heudiconv:latest \
    -d /base/Dicom/sub-{subject}/ses-{session}/*/DICOM/*.dcm \
    -o /base/Nifti/ \
    -f /base/Nifti/code/heuristic.py \
    -s 04 -ss 001 -c dcm2niix --overwrite

# 读取 list.txt 中的被试ID，并批量转换
# 这里你需要新建一个list.txt 文件，并确保txt文件中包含每行一个被试ID
for i in $(cat list.txt)
do
    docker run --rm -it \
        -v /media/sign/85CF1F81B7C9895F/idmdata/wu_script:/base \
        nipy/heudiconv:latest \
        -d /base/Dicom/sub-{subject}/ses-{session}/*/*.dcm \
        -o /base/Nifti/ \
        -f /base/Nifti/code/heuristic.py \
        -s $i -ss 1 -c dcm2niix -b --overwrite
done
