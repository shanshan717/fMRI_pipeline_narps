import os

# 定义参与者ID列表
subs = ['014', '015', '017']

# 定义BIDS数据根目录、fMRIPrep输出目录和FreeSurfer license路径
bids_root_dir = "/media/7T/narps/bids"
bids_out_dir = "/media/7T/narps/fmriprep"
license_path = "/mnt/sdb1/Judge-fMRI/Scripts/ProcessingScripts/fMRIPrep/license.txt"
nthreads = 12

# 检查fMRIPrep的Docker镜像版本
print("Checking fMRIPrep version...")
os.system("docker run -rm -it nipreps/fmriprep --version")

# 循环遍历每个参与者并运行fMRIPrep
for sub in subs:
    # 构建Docker命令，指定BIDS目录、输出目录、license文件和处理设置
    cmd = f"""
    docker run --rm -it \
        -v {bids_root_dir}:/inputbids \
        -v {bids_out_dir}/fmriprep/sub-{sub}:/output \
        -v {license_path}:/license.txt \
        nipreps/fmriprep \
        /inputbids /output participant \
        --participant_label {sub} \
        --nthreads {nthreads} --omp-nthreads {nthreads} \
        --mem-mb 32000 --ignore slicetiming --ignore fieldmaps \
        --fs-license-file /license.txt \
        --verbose
    """
    # 打印并运行fMRIPrep命令
    print(f"Running fMRIPrep for subject {sub}")
    os.system(cmd)
