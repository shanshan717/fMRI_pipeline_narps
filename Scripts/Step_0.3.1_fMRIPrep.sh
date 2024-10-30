# 定义路径
# 原始bids数据的目录
bids_root_dir=/home/ss/ds001734_demo/BIDS
# 输出结果目录
bids_root_out=/home/ss/ds001734_demo/BIDS
# 工作目录
bids_root_dir_output_wd4singularity=/home/ss/ds001734_demo/BIDS/BIDS_WD
mkdir $bids_root_dir_output_wd4singularity
# 接受命令行传入的被试编号
subj=$1
# 定义线程数
nthreads=12

# 创建输出和工作目录
if [ ! -d $bids_root_out/derivatives ]; then
   mkdir $bids_root_out/derivatives
fi
if [ ! -d $bids_root_dir_output_wd4singularity/derivatives ]; then
  mkdir $bids_root_dir_output_wd4singularity/derivatives
fi

#运行 fmriprep
echo ""
echo "Running fmriprep on participant: sub-$subj"
echo ""

# 创建fmriprep相关目录
if [ ! -d $bids_root_out/derivatives/fmriprep ]; then
    mkdir $bids_root_out/derivatives/fmriprep
fi

if [ ! -d $bids_root_out/derivatives/fmriprep/sub-${subj} ]; then
    mkdir $bids_root_out/derivatives/fmriprep/sub-${subj}
fi
if [ ! -d $bids_root_dir_output_wd4singularity/derivatives/fmriprep ]; then
    mkdir $bids_root_dir_output_wd4singularity/derivatives/fmriprep
fi

if [ ! -d $bids_root_dir_output_wd4singularity/derivatives/fmriprep/sub-${subj} ]; then
    mkdir $bids_root_dir_output_wd4singularity/derivatives/fmriprep/sub-${subj}
fi

# 运行fmriprep
docker run --rm -it -v $bids_root_dir_output_wd4singularity/derivatives/fmriprep/sub-${subj}:/wd \
    -v $bids_root_dir:/inputbids \
    -v $bids_root_out/derivatives/fmriprep/sub-${subj}:/output \
    -v /home/ss/ds001734_demo/:/freesurfer_license \
    nipreps/fmriprep \
    /inputbids /output participant\
    --participant_label ${subj} \
    -w /wd \
    --nprocs 6 \
    --nthreads $nthreads \
    --omp-nthreads $nthreads \
    --mem-mb 32000 \
    --fs-license-file /freesurfer_license/license.txt \
    --output-spaces T1w MNI152NLin6Asym MNI152NLin2009cAsym \
    --ignore slicetiming \
    --return-all-components \
    --notrack --verbose \
    --skip-bids-validation --debug all --stop-on-first-crash --resource-monitor --cifti-output 91k