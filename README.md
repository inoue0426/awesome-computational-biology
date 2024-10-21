# Awesome Computational Biology [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A knowledge collection of databases, software and papers related to computational biology.

> Computational biology involves the development and application of data-analytical and theoretical methods,
> mathematical modelling and computational simulation techniques to the study of biological, ecological,
> behavioural, and social systems. - [Wikipedia](https://en.wikipedia.org/wiki/Computational_biology)

## Contents

- [Modalities](#modalities)
  - [Sequencing]()
  - [Imaging]()
  - [Other]()
- [Databases](#databases)
  - [Expression](#RNA)
  - [Mutations](#Mutations)
  - [Other](#other)
  - [Compound](#compound)
  - [Pathway](#pathway)
  - [Mass Spectra](#mass-spectra)
  - [Protein](#protein)
  - [Genome](#genome)
  - [Disease](#disease)
  - [Interaction](#interaction)
  - [Clinical Trial](#clinical-trial)
  - [Cell Line](#cellline)
  - [Ontologies](#onto)
- [DataFormat and API](#api)
- [Tools](#preprocess)
  - [Package suites](#package-suites)
  - [Data Tools](#data-tools)
    - [Downloading](#downloading)
    - [Compressing](#compressing)
  - [Data Processing](#data-processing)
    - [Command Line Utilities](#command-line-utilities)
  - [Next Generation Sequencing](#next-generation-sequencing)
    - [Workflow Managers](#workflow-managers)
    - [Pipelines](#pipelines)
    - [Sequence Processing](#sequence-processing)
    - [Data Analysis](#data-analysis)
    - [Sequence Alignment](#sequence-alignment)
      - [Pairwise](#pairwise)
      - [Multiple Sequence Alignment](#multiple-sequence-alignment)
      - [Clustering](#clustering)
    - [Quantification](#quantification)
    - [Variant Calling](#variant-calling)
      - [Structural variant callers](#structural-variant-callers)
    - [BAM File Utilities](#bam-file-utilities)
    - [VCF File Utilities](#vcf-file-utilities)
    - [GFF BED File Utilities](#gff-bed-file-utilities)
    - [Variant Simulation](#variant-simulation)
    - [Variant Prediction/Annotation](#variant-predictionannotation)
    - [Python Modules](#python-modules)
      - [Data](#data)
      - [Tools](#tools)
    - [Assembly](#assembly)
    - [Annotation](#annotation)
  - [Long-read sequencing](#long-read-sequencing)
    - [Long-read Assembly](#long-read-assembly)
  - [Visualization](#visualization)
    - [Genome Browsers / Gene Diagrams](#genome-browsers--gene-diagrams)
    - [Circos Related](#circos-related)
- [Models](#machine-learning-tasks-and-models)
  - [Drug Response Prediction](#drug-response-prediction)
  - [Drug Repurposing](#drug-repurposing)
  - [Drug Target Interaction](#drug-target-interaction)
  - [Compound Protein Interaction](#compound-protein-interaction)
  - [Pre-trained embedding](#pre-trained-embedding)
  - [LLM for biology](#llm-for-biology)
- [Simulations](#simu)
- [Benchmark](#bench)
- [Labs and Topics](#labs)
- [Companies](#companies)
- [Other topics](./biomecha.md)
- [Learning Resources](#learning-resources)
  - [Becoming a Bioinformatician](#becoming-a-bioinformatician)
  - [Bioinformatics on GitHub](#bioinformatics-on-github)
  - [Sequencing](#sequencing)
  - [RNA-Seq](#rna-seq)
  - [ChIP-Seq](#chip-seq)
  - [YouTube Channels and Playlists](#youtube-channels-and-playlists)
  - [Blogs](#blogs)
  - [Miscellaneous](#miscellaneous)
- [Online networking groups](#online-networking-groups)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

# Modalities

## Sequencing

- [RNAseq]
   - [scRNAseq]
   - [10x]
   - [nanopore]
   - [...]
   - 5'
   - 3'
   - polyA
   - ...
   - in situ
   - spatial RNAseq
   - liveseq
   - ...
- [DNAseq]
   - WES
   - WGS
   - Targeted-seq
   - 
- [ChIP-seq]
- HIC-seq
  - microCHIP
  - scHICseq
- [Multimodal]
  - 
 
## Imaging

- Expansion Imaging

- antibody fluorescence
  - ...
- cryoEM
  - ...  
- electron microscopy
  - ...
- calcium imaging
  - ...
- spatial RNAseq (see #spatialRNAseq)
- 

## Other

- Mass Spec
  - MS-MS
  - MS ..

# Databases
## Expression
- [Gene Expression Omnibus](https://www.ncbi.nlm.nih.gov/geo/) - Public functional genomics database.
- [Single Cell PORTAL](https://singlecell.broadinstitute.org/single_cell) - Public database for single cell RNA.
- [Single Cell Expression Atlas](https://www.ebi.ac.uk/gxa/sc/home) - Public database for single cell RNA.
- [CellxGene]() -
- 
## Compound
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) - One of the biggest chemical database such as compounds, genes and proteins.
- [ChEBI](https://www.ebi.ac.uk/chebi/) - Chemical database  focused on small chemical compounds.
- [ChEMBL](https://www.ebi.ac.uk/chembl/) - Database of bioactive molecules with drug-like properties.
- [ChemSpider](http://www.chemspider.com/) - Chemical structure database.
- [KEGG COMPOUND](https://www.genome.jp/kegg/compound/) - Collection of small molecules and biopolymers.
- [LIPID MAPS](https://www.lipidmaps.org/databases/lmsd/overview) - Database of lipids.
- [Rhea](https://www.rhea-db.org/) - Database of chemical reactions.
- [Drug Repurposing Hub](https://repo-hub.broadinstitute.org/repurposing#download-data) - Collections of drug repurposing data containing drug, moa, target etc.
- [Therapeutic Target Database](https://idrblab.net/ttd/full-data-download) - collections of drug-target, target-disease, and drug-disease dataset.
- [ZINC ligand discovery database](https://zinc.docking.org/) - Free database of commercially-available compounds for virtual screening.
- [MoleculeNet](http://moleculenet.ai/) - Benchmark for molecular machine learning.
- [Ames Mutagenicity dataset](https://www.sciencedirect.com/science/article/abs/pii/S0166354220302412) - Dataset for predicting mutagenicity.
- [ADCdb](https://www.antibody-drug.com/) - Database for antibody-drug conjugates.
## Pathway
- [PathwayCommons](https://www.pathwaycommons.org/) - Database of Pathways and Interactions.
- [KEGG PATHWAY](https://www.genome.jp/kegg/pathway.html) - Collection fo drawn pathway maps.
- [WikiPathways](https://wikipathways.org/) - Database of biological pathways.
## Mass Spectra
- [MassBank](http://www.massbank.jp/) - Open souce databases and tools for mass spectrometry reference spectra.
- [MoNA MassBank of North America](https://mona.fiehnlab.ucdavis.edu/) - Meta database of metabolite mass spectra, metadata and associated compounds.
## Protein
- [THE HUMAN PROTEIN ATLAS](https://www.proteinatlas.org/) - One of the biggest human protein database contained cells, tissues, and organs. 
- [PROTEIN DATA BANK](https://www.rcsb.org/) - Database of the 3D shapes of proteins, nucleic acids, and complex assemblies.
- [UniProt](https://www.uniprot.org/) - The collection of functional information on proteins.
- [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/api-docs) - Database of 3D protein structures.
- [RCSB Protein Data Bank (PDB)](https://www.rcsb.org/) - Repository of 3D structural data of large biological molecules.
- [Critical Assessment of Structure Prediction (CASP)](https://predictioncenter.org/) - Experiment for advancing the methods of predicting protein structure from sequence.
- [Uniclust](https://uniclust.mmseqs.com/) - Collection of clustered protein sequence databases.
- [CATH database](https://www.cathdb.info/) - Hierarchical classification of protein domain structures.
## Genome
- [Human Genome Resources at NCBI](https://www.ncbi.nlm.nih.gov/projects/genome/guide/human/index.shtml) - Database of image, proteomics, transcriptomics and systems biology.
- [GenBank](https://www.ncbi.nlm.nih.gov/genbank/) - Database of genetic sequence offered by NCBI.
- [UCSC Genome Browser](https://genome.ucsc.edu/) - Genome blowser offered by UCSC.
- [cBioPortal](https://www.cbioportal.org/) - Database of Cancer Genomics. This has overall metaview for a lot of patients.
- [10x Genomics Dataset](https://www.10xgenomics.com/resources/datasets) - Collection of single-cell datasets.
- [The Genotype-Tissue Expression (GTEx)](https://gtexportal.org/home/) - Resource for studying human gene expression and regulation.
- [Dependency Map (DepMap)](https://depmap.org/portal/) - Genome-wide CRISPR-Cas9 screens in cancer cell lines.
- [Catalogue Of Somatic Mutations In Cancer (COSMIC)](https://cancer.sanger.ac.uk/cosmic) - Comprehensive resource for exploring somatic mutations in human cancers.
- [MGnify](https://www.ebi.ac.uk/metagenomics/) - Free resource for archiving, analysis, and browsing of metagenomic and metatranscriptomic data.
- [JASPAR](http://jaspar.genereg.net/) - Open-access database of curated, non-redundant transcription factor binding profiles.
## Disease
- [KEGG DRUG](https://www.genome.jp/kegg/drug/) - Comprehensive drug information resource for approved drugs.
- [DrugBank](https://www.drugbank.com/) - A database of drug and target maintained by the University of Alberta.
## Interaction
- Drug Gene Interaction
  - [DGIdb](https://www.dgidb.org/) - A database of drug-gene interactions and the druggable genome.
  - [Comparative Toxicogenomics Database](http://ctdbase.org/) - A database of Chemical-gene interactions, Chemical-disease associations, Gene-disease associations, and Chemical-phenotype associations.
  - [SNAP](https://snap.stanford.edu/biodata/datasets/10002/10002-ChG-Miner.html#:~:text=Dataset%20information,or%20activation%20of%20the%20drug.) - A dataset which contains Drug-gene interactions. 
  - [Therapeutics Data Commons](https://tdcommons.ai/) - A database for a lot of tasks such as drug-target, drug-response, drug-drug interaction.
- Drug (-Cell line) Response
  - [NCI60](https://dtp.cancer.gov/discovery_development/nci-60/) A database which focus on 60 cancer cell lines with many drugs.
  - [Genomics of Drug Sensitivity in Cancer (GDSC)](https://www.cancerrxgene.org/) - A database of drug sensitibity which has 1000 human cancer cell lines and 100s compounds.
  - [Cancer Cell Line Encyclopedia](https://sites.broadinstitute.org/ccle/) - A database of cancer cell lines. This has 1000 cell lines.
  - [CellMiner Cross Database (CellMinerCDB)](https://discover.nci.nih.gov/cellminercdb/) - Integration of multiple cancer cell line databases.
- Chemical Protein Interaction
  - [STITCH](http://stitch.embl.de/) - A database of Chemical Protein Interaction.
  - [BindingDB](https://www.bindingdb.org/rwd/bind/index.jsp) - A database of compounds and targes.
  - [PDBBind](http://www.pdbbind.org.cn/) - Database of experimentally measured binding affinity data for biomolecular complexes.
  - [CrossDocked2020](https://arxiv.org/abs/2001.01037) - Large-scale dataset for machine learning in structure-based virtual screening.
- Protein-Protein Interaction
  - [STRING](https://string-db.org/) - Protein-Protein Interaction Networks for several organisms.
  - [BioGRID](https://thebiogrid.org/) - Database of Protein, Genetic and Chemical Interactions.
  - [HIPPIE](http://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/) - Human Protein-Protein Interaction database.
- Knowledge Graph
  - [Drug Mechanism Database (DrugMechDB)](https://github.com/SuLab/DrugMechDB/tree/2.0.1): database of the mechanism of action from a drug to a disease.
  - [DRKG](https://github.com/gnn4dr/DRKG) - A library for biological knowledge graph.
### Clinical Trial
- [ClinicalTrials.gov](https://clinicaltrials.gov/) - Database of privately and publicly funded clinical studies.
- [ICD10](https://icd.who.int/browse10/2019/en) - International Classification of Diseases, 10th revision.
- [EU Drug Regulating Authorities Clinical Trials DB (EudraCT)](https://eudract.ema.europa.eu/) - European database of clinical trials.
- [MIMIC-IV](https://mimic.mit.edu/) - Freely accessible critical care database.


# API and data modalities
- [PubMed esearch](https://www.nlm.nih.gov/dataguide/edirect/esearch.html): API for searching articles in PubMed.


# Tools

## Preprocess

- [Chemistry Development Kit](https://github.com/cdk/cdk) - A software of cheminformatics and Machine Learning.
- [RDKit](https://github.com/rdkit/rdkit) - A software of cheminformatics and Machine Learning.
- [Scanpy](https://scanpy.readthedocs.io/en/stable/) - scRNA analysis library in Python.
- [Seurat](https://satijalab.org/seurat/) - scRNA analysis library in R.

## Package suites

Package suites gather software packages and installation tools for specific languages or platforms. We have some for bioinformatics software.

- **[Bioperl](https://github.com/bioperl/bioperl-live)** - International association of users & developers of open source Perl tools for bioinformatics, genomics and life sciences. [ [paper-2002](https://doi.org/10.1101%2Fgr.361602) | [web](https://bioperl.org) ]

- **[Bioconductor](https://github.com/Bioconductor)** - A plethora of tools for analysis and comprehension of high-throughput genomic data, including 1500+ software packages. [ [paper-2004](https://link.springer.com/article/10.1186/gb-2004-5-10-r80) | [web](https://www.bioconductor.org) ]

- **[Biopython](https://github.com/biopython/biopython)** - Freely available tools for biological computing in Python, with included cookbook, packaging and thorough documentation. Part of the [Open Bioinformatics Foundation](http://open-bio.org/). Contains the very useful [Entrez](https://biopython.org/DIST/docs/api/Bio.Entrez-module.html) package for API access to the NCBI databases. [ [paper-2009](https://pubmed.ncbi.nlm.nih.gov/19304878) | [web](https://biopython.org) ]

- **[Bioconda](https://github.com/bioconda)** - A channel for the [conda package manager](http://conda.pydata.org/docs/intro.html) specializing in bioinformatics software. Includes a repository with 3000+ ready-to-install (with `conda install`) bioinformatics packages. [ [paper-2018](https://pubmed.ncbi.nlm.nih.gov/29967506) | [web](https://bioconda.github.io) ]

- **[BioJulia](https://github.com/BioJulia)** - Bioinformatics and computational biology infastructure for the Julia programming language. [ [web](https://biojulia.net) ]
- **[Rust-Bio](https://github.com/rust-bio/rust-bio)** - Rust implementations of algorithms and data structures useful for bioinformatics. [ [paper-2016](http://bioinformatics.oxfordjournals.org/content/early/2015/10/06/bioinformatics.btv573.short?rss=1) ]
- **[SeqAn](https://github.com/seqan/seqan3)** - The modern C++ library for sequence analysis.
- **[(Poly)merase](https://github.com/TimothyStiles/poly)** - A Go library and command line utility for engineering organisms.
- **[Biocaml](https://github.com/biocaml/biocaml)** - Biocaml aims to be a high-performance user-friendly library for Bioinformatics.

## Data Tools

### Downloading
- **[GGD](https://github.com/gogetdata/ggd-cli)** - Go Get Data; A command line interface for obtaining genomic data. [ [web](https://gogetdata.github.io) ]
- **[SRA-Explorer](https://github.com/ewels/sra-explorer)** - Easily get SRA download links and other information. [ [web](https://sra-explorer.info) ]

### Compressing
- **[Genozip](https://github.com/divonlan/genozip)** - A compressor of common genomic file formats (BAM, CRAM, FASTQ, VCF etc). [ [web](https://genozip.com/?utm_source=Awesome-Bioinformatics) | [paper-2021](https://www.researchgate.net/publication/349347156_Genozip_-_A_Universal_Extensible_Genomic_Data_Compressor) ]

## Data Processing

### Command Line Utilities

- **[Bioinformatics One Liners](https://github.com/stephenturner/oneliners)** - Git repo of useful single line commands.
- **[BioNode](https://github.com/bionode/bionode)** - Modular and universal bioinformatics, Bionode provides pipeable UNIX command line tools and JavaScript APIs for bioinformatics analysis workflows. [ [web](http://bionode.io) ]
- **[bioSyntax](https://github.com/bioSyntax/bioSyntax)** - Syntax Highlighting for Computational Biology file formats (SAM, VCF, GTF, FASTA, PDB, etc...) in vim/less/gedit/sublime. [ [paper-2018](https://pubmed.ncbi.nlm.nih.gov/30134911) | [web](http://www.bioSyntax.org) ]
- **[CSVKit](https://github.com/wireservice/csvkit)** - Utilities for working with CSV/Tab-delimited files. [ [web](https://csvkit.readthedocs.io/en/latest) ]
- **[csvtk](https://github.com/shenwei356/csvtk)** - Another cross-platform, efficient, practical and pretty CSV/TSV toolkit. [ [web](https://bioinf.shenwei.me/csvtk) ]
- **[datamash](https://git.savannah.gnu.org/gitweb/?p=datamash.git)** - Data transformations and statistics. [ [web](http://www.gnu.org/software/datamash) ]
- **[easy_qsub](https://github.com/shenwei356/easy_qsub)** - Easily submitting PBS jobs with script template. Multiple input files supported.
- **GNU Parallel** - General parallelizer that runs jobs in parallel on a single multi-core machine. [Here](https://www.biostars.org/p/63816/) are some example scripts using GNU Parallel. [ [web](http://www.gnu.org/software/parallel) ]
- **[grabix](https://github.com/arq5x/grabix)** - A wee tool for random access into BGZF files.
- **[gsort](https://github.com/brentp/gsort)** - Sort genomic files according to a specified order.
- **[tabix](https://github.com/samtools/tabix)** - Table file index. [ [paper-2011](https://pubmed.ncbi.nlm.nih.gov/21208982) ]
- **[wormtable](https://github.com/wormtable/wormtable)** - Write-once-read-many table for large datasets.
- **[zindex](https://github.com/mattgodbolt/zindex)** - Create an index on a compressed text file.

## Next Generation Sequencing

### Workflow Managers

- **[BigDataScript](https://github.com/pcingola/BigDataScript)** - A cross-system scripting language for working with big data pipelines in computer systems of different sizes and capabilities. [ [paper-2014](https://pubmed.ncbi.nlm.nih.gov/25189778) | [web](https://pcingola.github.io/BigDataScript) ]
- **[Bpipe](https://github.com/ssadedin/bpipe)** - A small language for defining pipeline stages and linking them together to make pipelines. [ [web](http://docs.bpipe.org) ]
- **[Common Workflow Language](https://github.com/common-workflow-language/common-workflow-language)** - a specification for describing analysis workflows and tools that are portable and scalable across a variety of software and hardware environments, from workstations to cluster, cloud, and high performance computing (HPC) environments. [ [web](http://www.commonwl.org) ]
- **[Cromwell](https://github.com/broadinstitute/cromwell)** - A Workflow Management System geared towards scientific workflows. [ [web](https://cromwell.readthedocs.io) ]
- **[Galaxy](https://github.com/galaxyproject)** - a popular open-source, web-based platform for data intensive biomedical research. Has several features, from data analysis to workflow management to visualization tools. [ [paper-2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6030816) | [web](https://galaxyproject.org) ]
- **[Nextflow](https://github.com/nextflow-io/nextflow) (recommended)** - A fluent DSL modelled around the UNIX pipe concept, that simplifies writing parallel and scalable pipelines in a portable manner. [ [paper-2018](https://pubmed.ncbi.nlm.nih.gov/29412134) | [web](http://nextflow.io) ]
- **[redun](https://github.com/insitro/redun)** - A python-based workflow manager.
- **[Ruffus](https://github.com/cgat-developers/ruffus)** - Computation Pipeline library for python widely used in science and bioinformatics. [ [paper-2010](https://pubmed.ncbi.nlm.nih.gov/20847218) | [web](http://www.ruffus.org.uk) ]
- **[SciPipe](https://github.com/scipipe/scipipe)** - Workflow library embedded in the Go programming language, focusing on supporting complex workflow constructs, compiling to a single binary, providing powerful file naming and comprehensive audit reports for every output [ [paper-2019](https://pubmed.ncbi.nlm.nih.gov/31029061/) | [web](https://scipipe.org/) ]
- **[SeqWare](https://github.com/SeqWare/seqware)** - Hadoop Oozie-based workflow system focused on genomics data analysis in cloud environments. [ [paper-2010](https://pubmed.ncbi.nlm.nih.gov/21210981) | [web](https://seqware.github.io) ]
- **[Snakemake](https://bitbucket.org/snakemake)** - A workflow management system in Python that aims to reduce the complexity of creating workflows by providing a fast and comfortable execution environment. [ [paper-2018](https://pubmed.ncbi.nlm.nih.gov/29788404) | [web](https://snakemake.readthedocs.io) ]
- **[Workflow Descriptor Language](https://github.com/broadinstitute/wdl)** - Workflow standard developed by the Broad. [ [web](https://software.broadinstitute.org/wdl) ]

### Pipelines

- **[Awesome-Pipeline](https://github.com/pditommaso/awesome-pipeline)** - A list of pipeline resources.
- **[Bactopia](https://github.com/bactopia/bactopia/)** - A flexible pipeline, built with Nextflow, for the complete analysis of bacterial genomes. [ [web](https://bactopia.github.io/) ]
- **[Bacannot](https://github.com/fmalmeida/bacannot)** - A generic but comprehensive bacterial annotation pipeline, built with Nextflow, with nice graphical options for investigating results. [ [web](https://bacannot.readthedocs.io/en/latest/?badge=latest) ]
- **[bcbio-nextgen](https://github.com/chapmanb/bcbio-nextgen)** - Batteries included genomic analysis pipeline for variant and RNA-Seq analysis, structural variant calling, annotation, and prediction. [ [web](https://bcbio-nextgen.readthedocs.io) ]
- **[R-Peridot](https://github.com/pentalpha/r-peridot)** - Customizable pipeline for differential expression analysis with an intuitive GUI. [ [web](http://www.bioinformatics-brazil.org/r-peridot) ]
- **[ngs-preprocess](https://github.com/fmalmeida/ngs-preprocess)** - A pipeline for preprocessing short and long sequencing reads, built with Nextflow. [ [web](https://ngs-preprocess.readthedocs.io/en/latest/?badge=latest) ]

### Sequence Processing

Sequence Processing includes tasks such as demultiplexing raw read data, and trimming low quality bases.

- **[AfterQC](https://github.com/OpenGene/AfterQC)** - Automatic Filtering, Trimming, Error Removing and Quality Control for fastq data. [ [paper-2017](https://pubmed.ncbi.nlm.nih.gov/28361673) ]
- **[FastQC](https://github.com/s-andrews/FastQC)** - A quality control tool for high throughput sequence data. [ [web](http://www.bioinformatics.babraham.ac.uk/projects/fastqc) ]
- **[Fastqp](https://github.com/mdshw5/fastqp)** - FASTQ and SAM quality control using Python.
- **[Fastx Tookit](https://github.com/agordon/fastx_toolkit)** - FASTQ/A short-reads pre-processing tools: Demultiplexing, trimming, clipping, quality filtering, and masking utilities. [ [web](http://hannonlab.cshl.edu/fastx_toolkit) ]
- **[MultiQC](https://github.com/ewels/MultiQC)** - Aggregate results from bioinformatics analyses across many samples into a single report. [ [paper-2016](https://pubmed.ncbi.nlm.nih.gov/27312411) | [web](http://multiqc.info) ]
- **[SeqFu](https://github.com/telatin/seqfu2)** - Sequence manipulation toolkit for FASTA/FASTQ files written in Nim. [ [paper-2021](https://www.mdpi.com/2306-5354/8/5/59) | [web](https://telatin.github.io/seqfu2/) ]
- **[SeqKit](https://github.com/shenwei356/seqkit)** - A cross-platform and ultrafast toolkit for FASTA/Q file manipulation in Golang. [ [paper-2016](https://pubmed.ncbi.nlm.nih.gov/27706213) | [web](https://bioinf.shenwei.me/seqkit) ]
- **[seqmagick](https://github.com/fhcrc/seqmagick)** - file format conversion in Biopython in a convenient way. [ [web](http://seqmagick.readthedocs.io) ]
- **[Seqtk](https://github.com/lh3/seqtk)** - Toolkit for processing sequences in FASTA/Q formats.
- **[smof](https://github.com/incertae-sedis/smof)** - UNIX-style FASTA manipulation tools.

### Data Analysis

The following items allow for scalable genomic analysis by introducing specialized databases.

- **[Hail](https://github.com/hail-is/hail)** - Scalable genomic analysis.
- **[GLNexus](https://github.com/dnanexus-rnd/GLnexus)** - Scalable gVCF merging and joint variant calling for population sequencing projects. [ [paper-2018](https://www.biorxiv.org/content/10.1101/343970v1.abstract) ]

### Sequence Alignment

#### Pairwise

- **[Bowtie 2](https://github.com/BenLangmead/bowtie2)** - An ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. [ [paper-2012](https://pubmed.ncbi.nlm.nih.gov/22388286) | [web](http://bowtie-bio.sourceforge.net/bowtie2) ]
- **[BWA](https://github.com/lh3/bwa)** - Burrow-Wheeler Aligner for pairwise alignment between DNA sequences.
- **[WFA](https://github.com/smarco/WFA)** - the wavefront alignment algorithm (WFA) which expoit sequence similarity to speed up alignment [ [paper-2020](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btaa777/5904262) ]
- **[Parasail](https://github.com/jeffdaily/parasail)** - SIMD C library for global, semi-global, and local pairwise sequence alignments [ [paper-2016](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-0930-z) ]
- **[MUMmer](https://github.com/mummer4/mummer)** -  A system for rapidly aligning entire genomes, whether in complete or draft form. [ [paper-1999](http://mummer.sourceforge.net/MUMmer.pdf) | [paper-2002](http://mummer.sourceforge.net/MUMmer2.pdf) | [paper-2004](http://mummer.sourceforge.net/MUMmer3.pdf) | [web](http://mummer.sourceforge.net) ]
- **[DIAMOND](https://github.com/bbuchfink/diamond)** - An ultrafast protein aligner for `blastp` and `blastx` like searches. [ [paper-2021](https://www.nature.com/articles/s41592-021-01101-x) ]

#### Multiple Sequence Alignment

- **[POA](https://github.com/ljdursi/poapy)** - Partial-Order Alignment for fast alignment and consensus of multiple homologous sequences. [ [paper-2002](https://academic.oup.com/bioinformatics/article/18/3/452/236691) ]

#### Clustering

- **[MMseqs2](https://github.com/soedinglab/MMseqs2)** - Ultra-fast, sensitive search and clustering suite for protein and nucleotide sequence sets. [ [paper-2017](https://www.nature.com/articles/nbt.3988) | [paper-2018](https://www.nature.com/articles/s41467-018-04964-5) ]

### Quantification

- **[Cufflinks](https://github.com/cole-trapnell-lab/cufflinks)** - Cufflinks assembles transcripts, estimates their abundances, and tests for differential expression and regulation in RNA-Seq samples. [ [paper-2010](https://www.nature.com/articles/nbt.1621) ]
- **[RSEM](https://github.com/deweylab/RSEM)** - A software package for estimating gene and isoform expression levels from RNA-Seq data. [ [paper-2011](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-323) | [web](http://deweylab.github.io/RSEM/) ]

### Variant Calling

- **[DeepVariant](https://github.com/google/deepvariant)** - Deep learning-based variant caller [ [paper-2018](https://rdcu.be/7Dhl) ]
- **[freebayes](https://github.com/ekg/freebayes)** - Bayesian haplotype-based polymorphism discovery and genotyping. [ [web](http://arxiv.org/abs/1207.3907) ]
- **[GATK](https://github.com/broadgsa/gatk)** - Variant Discovery in High-Throughput Sequencing Data. [ [web](https://software.broadinstitute.org/gatk) ]
- **[Octopus](https://github.com/luntergroup/octopus)** - A polymorphic bayesian genotyping model with wide applicability. [ [paper-2021](https://www.nature.com/articles/s41587-021-00861-3) ]
- **[bcftools](https://github.com/samtools/bcftools)** - samtools/bcftools are a suite of tools for manipulating NGS data and can be used to call variants. [ [paper-2009](https://pubmed.ncbi.nlm.nih.gov/19505943) | [web](http://htslib.org) ]
#### Structural variant callers

- **[Delly](https://github.com/dellytools/delly)** - Structural variant discovery by integrated paired-end and split-read analysis. [ [paper-2012](https://pubmed.ncbi.nlm.nih.gov/22962449) ]
- **[lumpy](https://github.com/arq5x/lumpy-sv)** - lumpy: a general probabilistic framework for structural variant discovery. [ [paper-2014](https://link.springer.com/article/10.1186/gb-2014-15-6-r84) ]
- **[manta](https://github.com/Illumina/manta)** - Structural variant and indel caller for mapped sequencing data. [ [paper-2015](https://pubmed.ncbi.nlm.nih.gov/26647377) ]
- **[gridss](https://github.com/PapenfussLab/gridss)** - GRIDSS: the Genomic Rearrangement IDentification Software Suite. [ [paper-2017](https://pubmed.ncbi.nlm.nih.gov/29097403) ]
- **[smoove](https://github.com/brentp/smoove)** - structural variant calling and genotyping with existing tools, but,smoothly.

### BAM File Utilities

- **[Bamtools](https://github.com/pezmaster31/bamtools)** - Collection of tools for working with BAM files. [ [paper-2011](https://academic.oup.com/bioinformatics/article/27/12/1691/255399) ]
- **[bam toolbox](https://github.com/AndersenLab/bam-toolbox)** MtDNA:Nuclear Coverage; BAM Toolbox can output the ratio of MtDNA:nuclear coverage, a proxy for mitochondrial content.
- **[mergesam](https://github.com/DarwinAwardWinner/mergesam)** - Automate common SAM & BAM conversions.
- **[mosdepth](https://github.com/brentp/mosdepth)** - fast BAM/CRAM depth calculation for WGS, exome, or targeted sequencing. [ [paper-2017](https://pubmed.ncbi.nlm.nih.gov/29096012/) ]
- **[SAMstat](https://github.com/TimoLassmann/samstat)** - Displaying sequence statistics for next-generation sequencing. [ [paper-2010](https://academic.oup.com/bioinformatics/article/27/1/130/201972) | [web](http://samstat.sourceforge.net) ]
- **[Somalier](https://github.com/brentp/somalier)** - Fast sample-swap and relatedness checks on BAMs/CRAMs/VCFs/GVCFs. [ [paper-2020](https://pubmed.ncbi.nlm.nih.gov/32664994) ]
- **[Telseq](https://github.com/zd1/telseq)** - Telseq is a tool for estimating telomere length from whole genome sequence data. [ [paper-2014](https://academic.oup.com/nar/article/42/9/e75/1249448) ]

### VCF File Utilities

- **[bcftools](https://github.com/samtools/bcftools)** - Set of tools for manipulating VCF files. [ [paper-2016](https://pubmed.ncbi.nlm.nih.gov/26826718) | [paper-2017](https://pubmed.ncbi.nlm.nih.gov/28205675) | [web](http://samtools.github.io/bcftools) ]
- **[vcfanno](https://github.com/brentp/vcfanno)** - Annotate a VCF with other VCFs/BEDs/tabixed files. [ [paper-2016](https://pubmed.ncbi.nlm.nih.gov/27250555) ]
- **[vcflib](https://github.com/vcflib/vcflib)** - A C++ library for parsing and manipulating VCF files.
- **[vcftools](https://github.com/vcftools/vcftools)** - VCF manipulation and statistics (e.g. linkage disequilibrium, allele frequency, Fst). [ [paper-2011](https://pubmed.ncbi.nlm.nih.gov/21653522) ]

### GFF BED File Utilities

- **[AGAT](https://github.com/NBISweden/AGAT)** - Suite of tools to handle gene annotations in any GTF/GFF format. [ [web](https://agat.readthedocs.io/en/latest/?badge=latest) ]
- **[gffutils](https://github.com/daler/gffutils)** - GFF and GTF file manipulation and interconversion. [ [web](http://daler.github.io/gffutils) ]
- **[BEDOPS](https://bedops.readthedocs.io/en/latest/index.html)** - The fast, highly scalable and easily-parallelizable genome analysis toolkit. [ [paper-2012](https://academic.oup.com/bioinformatics/article/28/14/1919/218826) ]
- **[Bedtools2](https://github.com/arq5x/bedtools2)** - A Swiss Army knife for genome arithmetic. [ [paper-2010](https://pubmed.ncbi.nlm.nih.gov/20110278) | [paper-2014](https://pubmed.ncbi.nlm.nih.gov/25199790) | [web](https://bedtools.readthedocs.io) ]

### Variant Simulation

- **[Bam Surgeon](https://github.com/adamewing/bamsurgeon)** - Tools for adding mutations to existing `.bam` files, used for testing mutation callers. [ [web](https://popmodels.cancercontrol.cancer.gov/gsr/packages/bamsurgeon) ]
- **[wgsim](https://github.com/lh3/wgsim)** - **Comes with samtools!** - Reads simulator. [ [web](https://popmodels.cancercontrol.cancer.gov/gsr/packages/wgsim) ]

### Variant Prediction/Annotation

- **[SIFT](https://github.com/teamdfir/sift)** - Predicts whether an amino acid substitution affects protein function. [ [paper-2003](https://pubmed.ncbi.nlm.nih.gov/12824425) | [web](http://sift.jcvi.org) ]
- **[SnpEff](https://github.com/pcingola/SnpEff)** - Genetic variant annotation and effect prediction toolbox. [ [paper-2012](https://www.tandfonline.com/doi/full/10.4161/fly.19695) | [web](https://pcingola.github.io/SnpEff) ]
- **[Ensembl VEP](https://anaconda.org/bioconda/ensembl-vep)** - The VEP determines the effect of your variants (SNPs, insertions, deletions, CNVs or structural variants) on genes, transcripts, and protein sequence, as well as regulatory regions. [ [paper-2016](https://doi.org/10.1186/s13059-016-0974-4) | [web](http://www.ensembl.org/info/docs/tools/vep/index.html) ]


### Python Modules

#### Data

- **[cruzdb](https://github.com/brentp/cruzdb)** - Pythonic access to the UCSC Genome database. [ [paper-2013](https://academic.oup.com/bioinformatics/article/29/23/3003/248468) ]
- **[pyensembl](https://github.com/openvax/pyensembl)** - Pythonic Access to the Ensembl database. [ [web](https://pyensembl.readthedocs.io/en/latest/pyensembl.html) ]
- **[bioservices](https://github.com/cokelaer/bioservices)** - Access to Biological Web Services from Python. [ [paper-2013](https://academic.oup.com/bioinformatics/article/29/24/3241/194040) | [web](http://bioservices.readthedocs.io) ]

#### Tools

- **[cyvcf](https://github.com/arq5x/cyvcf)** - A port of [pyVCF](https://github.com/jamescasbon/PyVCF) using Cython for speed.
- **[cyvcf2](https://github.com/brentp/cyvcf2)** - Cython + HTSlib == fast VCF parsing; even faster parsing than pyVCF. [ [paper-2017](https://pubmed.ncbi.nlm.nih.gov/28165109) | [web](https://brentp.github.io/cyvcf2) ]
- **[pyBedTools](https://github.com/daler/pybedtools)** - Python wrapper for [bedtools](https://github.com/arq5x/bedtools). [ [paper-2011](https://pubmed.ncbi.nlm.nih.gov/21949271) | [web](http://daler.github.io/pybedtools) ]
- **[pyfaidx](https://github.com/mdshw5/pyfaidx)** - Pythonic access to FASTA files.
- **[pysam](https://github.com/pysam-developers/pysam)** - Python wrapper for [samtools](https://github.com/samtools/samtools). [ [web](https://pysam.readthedocs.io/en/latest/api.html) ]
- **[pyVCF](https://github.com/jamescasbon/PyVCF)** - A VCF Parser for Python. [ [web](http://pyvcf.readthedocs.org/en/latest/index.html) ]

### Assembly
- **[SPAdes](https://github.com/ablab/spades)** - SPAdes (St. Petersburg genome assembler) is an assembly toolkit containing various assembly pipelines and the de-facto standard for prokaryotic genome assemblies.
- **[SKESA](https://github.com/ncbi/SKESA)** - SKESA is a de-novo sequence read assembler for microbial genomes. It uses conservative heuristics and is designed to create breaks at repeat regions in the genome. This leads to excellent sequence quality without significantly compromising contiguity.

### Annotation
- **[Prokka](https://github.com/tseemann/prokka)** - Prokka: rapid prokaryotic genome annotation. Prokka is one of the most cited annotation command line tools for microbial genome annotations.
- **[Bakta](https://github.com/oschwengers/bakta)** - Bakta is a tool for the rapid & standardized annotation of bacterial genomes & plasmids. It provides dbxref-rich and sORF-including annotations in machine-readable JSON & bioinformatics standard file formats for automatic downstream analysis.

## Long-read sequencing

### Long-read Assembly

- **[canu](https://github.com/marbl/canu)** - A single molecule sequence assembler for genomes large and small.
- **[flye](https://github.com/fenderglass/Flye)** - De novo assembler for single molecule sequencing reads using repeat graphs. 
- **[hifiasm](https://github.com/chhylp123/hifiasm)** - A haplotype-resolved assembler for accurate Hifi reads.
- **[wtdbg2](https://github.com/ruanjue/wtdbg2)** -  A fuzzy Bruijn graph approach to long noisy reads assembly

## Visualization

### Genome Browsers / Gene Diagrams

The following tools can be used to visualize genomic data or for constructing customized visualizations of genomic data including sequence data from DNA-Seq, RNA-Seq, and ChIP-Seq, variants, and more.

- **[Squiggle](https://github.com/Lab41/squiggle)** - Easy-to-use DNA sequence visualization tool that turns FASTA files into browser-based visualizations. [ [paper-2018](https://pubmed.ncbi.nlm.nih.gov/30247632) | [web](https://squiggle.readthedocs.io/en/latest/) ]
- **[biodalliance](https://github.com/dasmoth/dalliance)** - Embeddable genome viewer. Integration data from a wide variety of sources, and can load data directly from popular genomics file formats including bigWig, BAM, and VCF.
  [ [paper-2011](https://pubmed.ncbi.nlm.nih.gov/21252075) | [web](http://www.biodalliance.org) ]
- **[BioJS](https://github.com/biojs/biojs)** - BioJS is a library of over hundred JavaScript components enabling you to visualize and process data using current web technologies. [ [paper-2014](https://pubmed.ncbi.nlm.nih.gov/25075290/) | [web](http://biojs.net/) ]
- **[Circleator](https://github.com/jonathancrabtree/Circleator)** - Flexible circular visualization of genome-associated data with BioPerl and SVG. [ [paper-2014](https://pubmed.ncbi.nlm.nih.gov/25075113) ]
- **[DNAism](https://github.com/drio/dnaism)** - Horizon chart D3-based JavaScript library for DNA data. [ [paper-2016](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-0891-2) | [web](http://drio.github.io/dnaism/) ]
- **[IGV js](https://github.com/igvteam/igv)** - Java-based browser. Fast, efficient, scalable visualization tool for genomics data and annotations. Handles a large variety of formats. [ [paper-2019](https://pubmed.ncbi.nlm.nih.gov/31099383) | [web](https://software.broadinstitute.org/software/igv) ]
- **[Island Plot](https://github.com/lairdm/islandplot)** - D3 JavaScript based genome viewer. Constructs SVGs. [ [paper-2015](https://pubmed.ncbi.nlm.nih.gov/25916842/) ]
- **[JBrowse](https://github.com/GMOD/jbrowse)** - JavaScript genome browser that is highly customizable via plugins and track customizations. [ [paper-2016](https://pubmed.ncbi.nlm.nih.gov/27072794) | [web](http://jbrowse.org/) ]
- **[PHAT](https://github.com/chgibb/PHAT)** - Point and click, cross platform suite for analysing and visualizing next-generation sequencing datasets. [ [paper-2018](https://pubmed.ncbi.nlm.nih.gov/30561651) | [web](https://chgibb.github.io/PHATDocs) ]
- **[pileup.js](https://github.com/hammerlab/pileup.js)** - JavaScript library that can be used to generate interactive and highly customizable web-based genome browsers. [ [paper-2016](https://pubmed.ncbi.nlm.nih.gov/27153605) ]
- **[scribl](https://github.com/chmille4/Scribl)** - JavaScript library for drawing canvas-based gene diagrams. [ [paper-2012](https://pubmed.ncbi.nlm.nih.gov/23172864) | [web](http://chmille4.github.io/Scribl) ]
- **Lucid Align** - A modern sequence alignment viewer. [ [web](https://lucidalign.com) ]

### Circos Related

- **[Circos](https://github.com/vigsterkr/circos)** - Perl package for circular plots, which are well suited for genomic rearrangements. [ [paper-2009](https://pubmed.ncbi.nlm.nih.gov/19541911) | [web](http://circos.ca) ]
- **ClicO FS** - An interactive web-based service of Circos. [ [paper-2015](https://pubmed.ncbi.nlm.nih.gov/26227146) ]
- **OmicCircos** - R package for circular plots for omics data. [ [paper-2014](https://pubmed.ncbi.nlm.nih.gov/24526832) | [web](http://www.bioconductor.org/packages/release/bioc/html/OmicCircos.html) ]
- **J-Circos** - A Java application for doing interactive work with circos plots. [ [paper-2014](https://pubmed.ncbi.nlm.nih.gov/25540184) | [web](http://www.australianprostatecentre.org/research/software/jcircos) ]
- **[rCircos](https://bitbucket.org/henryhzhang/rcircos/src/master/)** - R package for circular plots. [ [paper-2013](https://pubmed.ncbi.nlm.nih.gov/23937229) | [web](http://watson.nci.nih.gov/cran_mirror/web/packages/RCircos/index.html) ]
- **[fujiplot](https://github.com/mkanai/fujiplot)** - A circos representation of multiple GWAS results. [ [paper-2018](https://www.nature.com/articles/s41588-018-0047-6) ]

## Machine Learning Tasks and Models

## Drug Response Prediction
- [drGAT](https://github.com/inoue0426/drGAT): A model for drug response prediction with gene explainability with attention mechanism.

### Drug Repurposing

- [DeepPurpose](https://github.com/kexinhuang12345/DeepPurpose) - A DL Library for Drug Repurposing. 

### Drug Target Interaction

- [NeoDTI](https://github.com/FangpingWan/NeoDTI) - A library for Drug Target Interaction.

### Compound Protein Interaction

- [MCPINN](https://github.com/mhlee0903/multi_channels_PINN) - A library for drug discovery using Compound Protein Interaction and Machine Learning.
- [TransformerCPI](https://github.com/lifanchen-simm/transformerCPI) - A library for Compound Protein Interaction prediction using Transformer.

### Pre-trained embedding

- [Evolutionary Scale Modeling](https://github.com/facebookresearch/esm) - a library for protein embeddings.
- [ChemBERTa-2](https://github.com/seyonechithrananda/bert-loves-chemistry) - a library for chemical embeddingg and prediction.

### LLM for biology

- [AI4Chem/ChemLLM-7B-Chat](https://huggingface.co/AI4Chem/ChemLLM-7B-Chat) - LLM for chemical and molecule science
- [BioGPT](https://github.com/microsoft/BioGPT) - LLM for Biomedical text generation
- [GeneGPT](https://github.com/ncbi/GeneGPT) - LLM for biomedical information with several API.
- [GenePT](https://github.com/yiqunchen/GenePT) - foundation LLM for single cell data
- [scPRINT](https://github.com/cantinilab/scPRINT) - scPRINT is pretrained on 50M cells to denoise and perform zero imputation of any single cell RNAseq profile.


## Simulations

- [SERGIO]
- [BoolODE]
- [GENEnetWeaver]



## Learning Resources

### Becoming a Bioinformatician

- [What is a bioinformatician](http://blog.fejes.ca/?p=2418)
- [Bioinformatics Curriculum Guidelines: Toward a Definition of Core Competencies](http://www.ploscompbiol.org/article/info:doi%2F10.1371%2Fjournal.pcbi.1003496)
- [Top N Reasons To Do A Ph.D. or Post-Doc in Bioinformatics/Computational Biology](http://caseybergman.wordpress.com/2012/07/31/top-n-reasons-to-do-a-ph-d-or-post-doc-in-bioinformaticscomputational-biology/)
- [A 10-Step Guide to Party Conversation For Bioinformaticians](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2013-14-1-104) - Here is a step-by-step guide on how to convey concepts to people not involved in the field when asked the question: 'So, what do you do?'
- [A History Of Bioinformatics (In The Year 2039)](https://www.youtube.com/watch?v=uwsjwMO-TEA) - A talk by C. Titus Brown on his take of looking back at bioinformatics from the year 2039. His notes for this talk can be found [here](http://ivory.idyll.org/blog/2014-bosc-keynote.html).
- [A farewell to bioinformatics](https://madhadron.com/science/farewell_to_bioinformatics.html) - A critical view of the state of bioinformatics.
- [A Series of Interviews with Notable Bioinformaticians](http://www.acgt.me/blog/2014/3/25/101-questions-a-new-series-of-interviews-with-notable-bioinformaticians) - Dr. Keith Bradnam "thought it might be instructive to ask a simple series of questions to a bunch of notable bioinformaticians to assess their feelings on the current state of bioinformatics research, and maybe get any tips they have about what has been useful to their bioinformatics careers."
- [Open Source Society University on Bioinformatics](https://github.com/ossu/bioinformatics) - Solid path for those of you who want to complete a Bioinformatics course on your own time, for free, with courses from the best universities in the World.
- [Rosalind](http://rosalind.info/) - Rosalind is a platform for learning bioinformatics through problem solving.
- [A guide for the lonely bioinformatician](http://www.opiniomics.org/a-guide-for-the-lonely-bioinformatician/) - This guide is aimed at bioinformaticians, and is meant to guide them towards better career development.
- [A brief history of bioinformatics](https://doi.org/10.1093/bib/bby063)

### Bioinformatics on GitHub

- [Awesome-alternative-splicing](https://github.com/HussainAther/awesome-alternative-splicing) - List of resources on alternative splicing including software, databases, and other tools.
- [Awesome AI-based Protein Design](https://github.com/opendilab/awesome-AI-based-protein-design) - A collection of research papers for AI-based protein design.

### Sequencing

- [Next-Generation Sequencing Technologies - Elaine Mardis (2014)](https://youtu.be/6Is3W7JkFp8) [1:34:35] - Excellent (technical) overview of next-generation and third-generation sequencing technologies, along with some applications in cancer research.
- [Annotated bibliography of \*Seq assays](https://liorpachter.wordpress.com/seq/) - List of ~100 papers on various sequencing technologies and assays ranging from transcription to transposable element discovery.
- [For all you seq... (PDF)](http://www.illumina.com/content/dam/illumina-marketing/documents/applications/ngs-library-prep/ForAllYouSeqMethods.pdf) (3456x5471) - Massive infographic by Illumina on illustrating how many sequencing techniques work. Techniques cover protein-protein interactions, RNA transcription, RNA-protein interactions, RNA low-level detection, RNA modifications, RNA structure, DNA rearrangements and markers, DNA low-level detection, epigenetics, and DNA-protein interactions. References included.

### RNA-Seq

- [Review papers on RNA-seq (Biostars)](https://www.biostars.org/p/52152/) - Includes lots of seminal papers on RNA-seq and analysis methods.
- [Informatics for RNA-seq: A web resource for analysis on the cloud](https://github.com/griffithlab/rnaseq_tutorial) - Educational resource on performing RNA-seq analysis in the cloud using Amazon AWS cloud services. Topics include preparing the data, preprocessing, differential expression, isoform discovery, data visualization, and interpretation.
- [RNA-seqlopedia](http://rnaseq.uoregon.edu/) - RNA-seqlopedia provides an awesome overview of RNA-seq and of the choices necessary to carry out a successful RNA-seq experiment.
- [A survey of best practices for RNA-seq data analysis](http://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-0881-8) - Gives awesome roadmap for RNA-seq computational analyses, including challenges/obstacles and things to look out for, but also how you might integrate RNA-seq data with other data types.
- [Stories from the Supplement](https://www.youtube.com/watch?v=5NiFibnbE8o) [46:39] - Dr. Lior Pachter shares his stories from the supplement for well-known RNA-seq analysis software CuffDiff and [Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/) and explains some of their methodologies.
- [List of RNA-seq Bioinformatics Tools](https://en.wikipedia.org/wiki/List_of_RNA-Seq_bioinformatics_tools) - Extensive list on Wikipedia of RNA-seq bioinformatics tools needed in analysis, ranging from all parts of an analysis pipeline from quality control, alignment, splice analysis, and visualizations.
- [RNA-seq Analysis](https://github.com/crazyhottommy/RNA-seq-analysis) - [@crazyhottommy](https://github.com/crazyhottommy)'s notes on various steps and considerations when doing RNA-seq analysis.

### ChIP-Seq

- [ChIP-seq analysis notes from Tommy Tang](https://github.com/crazyhottommy/ChIP-seq-analysis) - Resources on ChIP-seq data which include papers, methods, links to software, and analysis.

### YouTube Channels and Playlists

- [Current Topics in Genome Analysis 2016](https://www.genome.gov/12514288/current-topics-in-genome-analysis-2016-course-syllabus-handouts-and-videos/) - Excellent series of fourteen lectures given at NIH about current topics in genomics ranging from sequence analysis, to sequencing technologies, and even more translational topics such as genomic medicine.
- [GenomeTV](https://www.youtube.com/user/GenomeTV) - "GenomeTV is NHGRI's collection of official video resources from lectures, to news documentaries, to full video collections of meetings that tackle the research, issues and clinical applications of genomic research."
- [Leading Strand](https://www.youtube.com/user/LeadingStrand) - Keynote lectures from Cold Spring Harbor Laboratory (CSHL) Meetings. More on [The Leading Strand](http://theleadingstrand.cshl.edu/).
- [Genomics, Big Data and Medicine Seminar Series](https://www.youtube.com/playlist?list=PLqLDR0CTP9_pboZCk6gR9Zn4kW7h9XWJI) - "Our seminars are dedicated to the critical intersection of GBM, delving into 'bleeding edge' technology and approaches that will deeply shape the future."
- [Rafael Irizarry's Channel](https://www.youtube.com/user/RafalabChannel/videos) - Dr. Rafael Irizarry's lectures and academic talks on statistics for genomics.
- [NIH VideoCasting and Podcasting](https://www.youtube.com/user/nihvcast) - "NIH VideoCast broadcasts seminars, conferences and meetings live to a world-wide audience over the Internet as a real-time streaming video." Not exclusively genomics and bioinformatics video but many great talks on domain specific use of bioinformatics and genomics.

### Blogs

- [ACGT](http://www.acgt.me/) - Dr. Keith Bradnam writes about this "thoughts on biology, genomics, and the ongoing threat to humanity from the bogus use of bioinformatics acroynums."
- [Opiniomics](http://www.opiniomics.org/) - Dr. Mick Watson write on bioinformatics, genomes, and biology.
- [Bits of DNA](https://liorpachter.wordpress.com/) - Dr. Lior Pachter writes review and commentary on computational biology.
- [it is NOT junk](http://www.michaeleisen.org/blog/) - Dr. Michael Eisen writes "a blog about genomes, DNA, evolution, open science, baseball and other important things"
- [#!/perl/bioinfo](https://bioinfoperl.blogspot.com) - The Computational and Structural Biology group at EEAD-CSIC writes, in Spanish and English, about ideas and code for plant genomics, computational and structural biology problems.

### Miscellaneous

- [The Leek group guide to genomics papers](https://github.com/jtleek/genomicspapers/) - Expertly curated genomics papers to get up to speed on genomics, RNA-seq, statistics (used in genomics), software development, and more.
- [A New Online Computational Biology Curriculum](https://doi.org/10.1371/journal.pcbi.1003662) - "This article introduces a catalog of several hundred free video courses of potential interest to those wishing to expand their knowledge of bioinformatics and computational biology. The courses are organized into eleven subject areas modeled on university departments and are accompanied by commentary and career advice."
- [How Perl Saved the Human Genome Project](http://www.foo.be/docs/tpj/issues/vol1_2/tpj0102-0001.html) - An anecdote by Lincoln D. Stein on the importance of the Perl programming language in the Human Genome Project.
- [Educational Papers from Nature Biotechnology and PLoS Computational Biology](https://liacs.leidenuniv.nl/~hoogeboomhj/mcb/nature_primer.html) - Page of links to primers and short educational articles on various methods used in computational biology and bioinformatics.
- [The PeerJ Bioinformatics Software Tools Collection](https://peerj.com/collections/45-bioinformatics-software/) - Collection of tools curated by Keith Crandall and Claus White, aimed at collating the most interesting, innovative, and relevant bioinformatics tools articles in PeerJ.

## Online networking groups

- [Bioinformatics (on Discord)](https://discord.com/invite/3uxbPns) - a Discord server for general bioinformatics
- [r-bioinformatics](https://www.reddit.com/r/bioinformatics/comments/7ndwm1/rbioinformatics_slack_channel_and_an_open_call/) - the official Slack workspace of r/bioinformatics ([send a direct message to apfejes on reddit](https://www.reddit.com/message/compose/?to=apfejes&subject=Request%20to%20join%20the%20r/bioinformatics%20Slack%20group&message=I%20would%20like%20to%20request%20to%20join%20the%20r/bioinformatics%20Slack%20group))
- [BioinformaticsGRX](https://bioinformaticsgrx.es/) - A community of bioinformaticians based in Granada, Spain
- [Comunidad de Desarolladores de Software en Bioinformática](https://comunidadbioinfo.github.io/) - A community of bioinformaticians centered in Latin America
- [COMBINE](https://combine.org.au/) - An Austrialian group for bioinformatics students
