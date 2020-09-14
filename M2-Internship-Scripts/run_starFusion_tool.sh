#!/bin/bash
#Paths
star_out_dir="./outputs/output_star_aln"
CTAT_genome="./databases/CTAT_genome/GRCh37_gencode_v19_CTAT_lib_Oct012019.plug-n-play/ctat_genome_lib_build_dir"
out="outputs/star_fusion_outdir"
mkdir -p $out

for i in $( find outputs/output_star_aln/ -name "Chimeric.out.junction")
do
prefix=$(echo $i | cut -d '/' -f3)
results_dir=$out/$prefix
mkdir -p $results_dir

echo '#!/bin/bash' > $results_dir/starFusion_$prefix.sh
echo "STAR-Fusion --genome_lib_dir $CTAT_genome -J $i --output_dir $results_dir">> $results_dir/starFusion_$prefix.sh
echo "$results_dir/starFusion_$prefix.sh" >> STARFusion_scripts.txt
sbatch -o $results_dir/$prefix.cluster.out -p shortq $results_dir/starFusion_$prefix.sh
done
