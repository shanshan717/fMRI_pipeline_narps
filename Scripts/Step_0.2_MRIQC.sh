#!/bin/bash
# 定义BIDS数据的根目录和MRIQC的输出目录
bids_root_dir=/media/7T/narps/bids
output_dir=/media/7T/narps/MRIQC
nthreads=6
mem=24 # memory in GB

# 列出需要进行mriqc的参与者ID
participants=("036" "037" "038" "039" "040" "043" "044")

# 计算总参与者数量并初始化已处理计数，并非必须运行的代码
total=${#participants[@]}  
count=0  

# 显示当前进度，非必须运行的代码
progress_bar() {
  local progress=$1
  local total=$2
  local width=50  
  local percent=$(( progress * 100 / total ))
  local completed=$(( progress * width / total ))
  local remaining=$(( width - completed ))

  printf "["
  for ((i = 0; i < completed; i++)); do
    printf "="
  done
  for ((i = 0; i < remaining; i++)); do
    printf " "
  done
  printf "] %d%% (%d/%d)\r" $percent $progress $total
}

# 遍历每个参与者
for subj in "${participants[@]}"
do
  count=$((count + 1))  

  echo ""
  echo "Running MRIQC on participant: sub-$subj"
  echo ""

  # 创建输出目录
  if [ ! -d $output_dir ]; then
    mkdir -p $output_dir
  fi

  if [ ! -d $output_dir/sub-${subj} ]; then
    mkdir -p $output_dir/sub-${subj}
  fi

  # 使用Docker运行MRIQC（必须运行的代码）
  docker run -it --rm \
    -v $bids_root_dir:/data:ro \
    -v $output_dir/sub-${subj}:/out \
  ss/mriqc /data /out participant \
    --participant_label $subj \
    --n_proc $nthreads \
    --mem_gb $mem \
    --float32 \
    --ants-nthreads $nthreads \
    -w /out \
    --verbose-reports \
    --no-sub

  # 显示当前进度，非必须运行的代码
  progress_bar $count $total
  echo ""  
done

# 处理完成提示
echo "All participants processed."
