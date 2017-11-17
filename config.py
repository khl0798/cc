# -*- coding: utf-8 -*-

import re, argparse, os
import time

class Config(object):
    """设置各运行软件的path"""
    def __init__(self):
        # self.software = '/home/khl/software/software1'
        self.software = '/home/software'
        self.script_path = "/home/khl/dna/script"
        self.msi_path = "/home/khl/dna/script/msi/"
    def trim_path(self):
        trim_path = self.software + '/Trimmomatic-0.36/trimmomatic-0.36.jar'
        return trim_path

    def fastqc(self):
        fastqc = self.software + '/FastQC/fastqc'
        return fastqc

    def kseq_fastq_base(self):
        kseq_fastq_base = self.software + '/script/readfq/kseq_fastq_base'
        return kseq_fastq_base

    def q30(self):
        q30 = self.software + '/script/q30.py'
        return q30

    def ref(self):
        """version: hg19"""
        fasta = '/data/reference/human/hg19.2bit/hg19.fasta'
        return fasta

    def index(self):
        index = "@RG\\tID:1\\tLB:lib1\\tPL:ILLUMINA\\tSM:%s\\tPU:unit1"
        return index

    def QC_stat_tar(self):
        qc_stat_tar = self.software + '/script/QC_stat_tar.pl'
        return qc_stat_tar

    def gatk(self):
        gatk = self.software + '/GenomeAnalysisTK.jar'
        return gatk

    def picard(self):
        picard = self.software + '/picard.jar'
        return picard

    def intervals(self, step = None):
        interval_1000 = '/data/bed_file/WES/WES_split_probes/1000/'
        knowsites_vcf = '/data/reference/human/gatk_resource/dbsnp_138.hg19.vcf'
        golden_standard_indel_sites_vcf = '/data/reference/human/gatk_resource/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf'
        exon_panel_intervals = '/data/bed_file/WES/xgen-exome-research-panel-probes.intervals'  #wes
        indel_hg19_sites_vcf = '/data/reference/human/gatk_resource/1000G_phase1.indels.hg19.sites.vcf'
        if re.search('realigner', step.lower()):
            return exon_panel_intervals, indel_hg19_sites_vcf, golden_standard_indel_sites_vcf
        if re.search(r'hsmetrics', step.lower()):
            return exon_panel_intervals
        if re.search(r'recalibrator', step.lower()):
            return knowsites_vcf, indel_hg19_sites_vcf, golden_standard_indel_sites_vcf, exon_panel_intervals

    def samtools(self):
        samtools = self.software + '/samtools-1.3.1/samtools'
        return samtools

    def umi_tools(self):
        # umi_tools = '/usr/bin/umi_tools'
        umi_tools = "/home/khl/software/python/umi_tools-0.4.4-py2.7.egg/umi_tools/umi_tools.py"
        return umi_tools

    def trim_adapter(self):
        adapter_info = 'ILLUMINACLIP:/home/software/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10:36:TRUE LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36'
        return adapter_info

    def java(self):
        java_path = '/usr/bin/java'
        return java_path

    def python(self):
        python_path = '/usr/bin/python3.4'
        return python_path

    def python2(self):
        python_path = '/usr/bin/python'
        return python_path

    def perl(self):
        perl_path = "/usr/bin/perl"
        return perl_path

    def bwa(self, sample_name=None):
        bwa_path = '/usr/bin/bwa'
        if sample_name:
            bwa_mapping_info = "@RG\\tID:1\\tLB:lib1\\tPL:ILLUMINA\\tSM:%s\\tPU:unit1"%(sample_name)
        else:
            bwa_mapping_info = "@RG\\tID:1\\tLB:lib1\\tPL:ILLUMINA\\tSM:%s\\tPU:unit1"
        return bwa_path, bwa_mapping_info

    def sort_bam(self):
        sort_bam_path = self.software + '/sambamba_v0.6.6'
        return sort_bam_path

    def target_list(self):
        target_list = '/data/bed_file/WES/WES_split_probes/1000/target.list'
        return target_list

    def fusion_detect(self):
        exons_inter_gene_bed = '/home/software/sv_detect/factera-v1.4.4/exons_inter-gene.bed'
        hg19_2bit = '/home/software/sv_detect/factera-v1.4.4/hg19.2bit/hg19.2bit'
        return exons_inter_gene_bed, hg19_2bit

    def fusion_path(self):
        factera_path = "/home/khl/software/factera.pl"
        facteraFreq_path = "/home/software/script/facteraFreq.pl"
        return factera_path, facteraFreq_path

    def cnv_bed_pon(self, type = 'somatic'):
        if type == 'somatic':
            cnv_bed = "/data/DB/16gene_PoN/gatk4/16gene.padded.bed"
            cnv_150pon, cnv_75pon = "/data/DB/16gene_PoN/gatk4/150bp.pon", "/data/DB/16gene_PoN/gatk4/75bp.pon"
            return cnv_bed, cnv_150pon, cnv_75pon

    def cnv_path(self):
        cnv = '/home/software/script/gatk4_cnv.sh'
        return cnv

    def mutect_pon(self, analysis_type):
        pon_path = '/data/DB/mutect2_PoN/16gene/MuTect2_PON.vcf'
        wes_pon_path = '/data/DB/mutect2_PoN/wes/MuTect2_PON.vcf'
        if analysis_type == "W":
            return wes_pon_path
        else:
            return pon_path

    def assemble_path(self):
        assemble_path = "/home/software/migec-1.2.6/migec-1.2.6.jar"
        return assemble_path

    def db_snp(self):
        db_snp_path = "/data/reference/human/gatk_resource/dbsnp_138.hg19.vcf"
        return db_snp_path

    def gene16(self):
        gene16_vcf = "/data/bed_file/16gene/idt.intervals"
        return gene16_vcf

    def snpannotation(self):
        anno_sh = "/home/software/script/anno.sh"
        return anno_sh

    def germline_hypor(self):
        germline_hypor="/data/bed_file/7gene.target.intervals"
        return germline_hypor

    def module_path(self):
        """还没有加上snpannotation的模块文件路径， 各个模块的脚本路径"""
        qc_path = self.script_path + "/qc.py"
        mapping_path = self.script_path + "/mapping.py"
        preprocess_path = self.script_path + "/preprocess.py"
        mappingstat_path = self.script_path + "/mappingstat.py"
        mutect_path = self.script_path + "/mutect.py"
        fusion_cnv_path = self.script_path + "/fusion_detect.py"
        cnvplot_path = self.script_path + "/cnvplot.py"
        msi_path = self.script_path + "/msi.py"
        qcpdf_path = "/home/khl/dna/pdf_parse/test_nodejs.py"
        return [qc_path, mapping_path, preprocess_path, mappingstat_path, mutect_path, fusion_cnv_path, qcpdf_path, cnvplot_path, msi_path]

    def get_time_path(self):
        gettime = self.script_path + "/get_time.py"
        return gettime
    
    def umi_module_path(self):
        """umi 预处理 对应module的脚本"""
        samtools_path = '/home/khl/dna/samtools_merge.py'
        add_id_path = '/home/khl/dna/add_id.py'
        extract_fq_path = '/home/khl/dna/extract_fq.py'
        bam_sam_path = "/home/khl/dna/bam_sam.py"
        return samtools_path, add_id_path, extract_fq_path, bam_sam_path

    def umi_script(self):
        self.umi_script_path = "/data/zgd/umi/test/umi.pl"
        return self.umi_script_path

    def cnv_plot(self):
        """cnv 各脚本"""
        cnv_plot_sh = self.script_path + "/plot/16_cnv_plot.sh"
        cnv_plot_path = self.script_path  + "/plot/plot.pl"
        manhattan_path = self.script_path + "/plot/manhattan.R"
        return cnv_plot_sh, cnv_plot_path, manhattan_path


    def msi_script(self):
        self.test_msi = self.msi_path + "test_msi.sh"
        self.run_msi = self.msi_path + "run_msings.sh"
        return self.test_msi, self.run_msi

    def genotype_script(self):
        script = self.software + "/script/genotype_for_chemosites.sh"
        return script

    def genotype_path(self):
        module_path = self.script_path + "/genotype.py"
        return module_path

    def add_id_path(self):
        add_id = self.script_path + "/add_id.py"
        return add_id