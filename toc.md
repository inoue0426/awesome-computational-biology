# Computers for Biology and Medicine

Every listed elements must come with:

1. Working link to what it is (a code / database / video / website).
2. A short description of what it is.
3. A list of topics that it belongs to if different from the ones listed with its parent

## Annotations

### Topics:

- biomachanics
- sequencing
- imaging
- neuroscience
- comp genomics
- single cell omics
- proteomics and structural biology
- health informatics
- machine learning
- AI for biology
- Bio / tech
- Research

### Scales:

1. molecule
2. cell
3. tissue
4. organ
5. organism
6. population
7. ecosystem

## Table of Contents

- [Modalities](#modalities)
  - [Sequencing](#sequencing)
  - [Imaging](#imaging)
  - [Other](#other)
- [Databases](#databases)
  - [Expression](#expression)
  - [Compound](#compound)
  - [Pathway](#pathway)
  - [Mass Spectra](#mass-spectra)
  - [Protein](#protein)
  - [Genome](#genome)
  - [Disease](#disease)
  - [Interaction](#interaction)
    - [Clinical Trial](#clinical-trial)
- [Tools](#tools)
  - [API and data management](#api-and-data-formats)
    - [Downloading](#downloading)
    - [Compressing](#compressing)
  - [Preprocessing](./preprocessing.md)
    - [Sequencing](./preprocessing.md#sequencing)
    - [Imaging](./preprocessing.md#imaging)
    - [Neuroscience](./preprocessing.md#neuroscience)
    - [Biomechanics](./preprocessing.md#biomechanics)
    - [Text and Knowledge](./preprocessing.md#text-and-knowledge)
  - [Package suites](#package-suites)
  - [Workflow Managers](#workflow-managers)
    - [Pipelines](#pipelines)
  - [Analysis](./analysis.md)
    - [sequencing](./analysis.md#sequencing)
    - [imaging](./analysis.md#imaging)
    - [neuroscience](./analysis.md#neuroscience)
    - [biomechanics](./analysis.md#biomechanics)
    - [text and knowledge](./analysis.md#text-and-knowledge)
  - [Machine Learning Tasks and Models](./README.md)
    - [small molecules](./ml-mol.md)
      - [Drug Response Prediction](./ml-mol.md#drug-response-prediction)
      - [Drug Repurposing](./ml-mol.md#drug-repurposing)
      - [Drug Target Interaction](./ml-mol.md#drug-target-interaction)
      - [Compound Protein Interaction](./ml-mol.md#compound-protein-interaction)
      - [Pre-trained embedding](./ml-mol.md#pre-trained-embedding)
    - [LLMs](./llms.md)
      - [text]
      - [sequence]
      - [RNA-cell]
      - [imaging]
      - [multimodal]
    - [Single Cell Omics](#single-cell-omics)
      - [Spatial Omics](#spatial-omics)
        - [Spatial Transcriptomics](#spatial-transcriptomics)
        - [Cell-Cell Communications (CCC)](#cell-cell-communications-ccc)
        - [Spatial Proteomics](#spatial-proteomics)
      - [Single Cell RNA-Seq](#single-cell-rna-seq)
      - [Single Cell ATAC-Seq](#single-cell-atac-seq)
      - [Single Cell Methylation](#single-cell-methylation)
      - [Single Cell Protein](#single-cell-protein)
      - [Single Cell Multi-omics](#single-cell-multi-omics)
    - [Genomics](./ml-genomics.md)
      - [Single Nucleotide Polymorphism (SNP)](./ml-genomics.md#single-nucleotide-polymorphism-snp)
      - [Copy Number Variation (CNV)](./ml-genomics.md#copy-number-variation-cnv)
      - [Variant Calling](./ml-genomics.md#variant-calling)
      - [Structural variant callers](./ml-genomics.md#structural-variant-callers)
      - [Variant Annotation](./ml-genomics.md#variant-annotation)
      - [Variant Prediction](./ml-genomics.md#variant-prediction)
    - [Imaging](./ml-imaging.md)
      - [Image Analysis](./ml-imaging.md#image-analysis)
      - [Image Segmentation](./ml-imaging.md#image-segmentation)
      - [Image Classification](./ml-imaging.md#image-classification)
      - [Image Retrieval](./ml-imaging.md#image-retrieval)
    - [Neuroscience](./ml-neuroscience.md)
      - [Electrophysiology](./ml-neuroscience.md#electrophysiology)
      - [Optical Imaging](./ml-neuroscience.md#optical-imaging)
      - [Behavioral Data](./ml-neuroscience.md#behavioral-data)
    - [Biomechanics](./ml-biomechanics.md)
      - [Muscle Mechanics](./ml-biomechanics.md#muscle-mechanics)
      - [Movement Analysis](./ml-biomechanics.md#movement-analysis)
      - [Force Measurement](./ml-biomechanics.md#force-measurement)
    - [Text and Knowledge](./ml-networks.md)
      - [Text Embedding](./ml-networks.md#text-embedding)
      - [Knowledge Graph](./ml-networks.md#knowledge-graph)
      - [Text Generation](./ml-networks.md#text-generation)
  - [Simulations](./simulations.md)
- [Benchmarks](./benchmarks.md)
  - [Single Cell Benchmarks](./benchmarks.md#single-cell-benchmarks)
  - [Genomics Benchmarks](./benchmarks.md#genomics-benchmarks)
  - [Imaging Benchmarks](./benchmarks.md#imaging-benchmarks)
  - [Neuroscience Benchmarks](./benchmarks.md#neuroscience-benchmarks)
  - [Biomechanics Benchmarks](./benchmarks.md#biomechanics-benchmarks)
  - [Text and Knowledge Benchmarks](./benchmarks.md#text-and-knowledge-benchmarks)
- [Visualization](./visualization.md)
  - [Single Cell Visualization](./visualization.md#single-cell-visualization)
  - [Genomics Visualization](./visualization.md#genomics-visualization)
  - [Imaging Visualization](./visualization.md#imaging-visualization)
  - [Neuroscience Visualization](./visualization.md#neuroscience-visualization)
  - [Biomechanics Visualization](./visualization.md#biomechanics-visualization)
  - [Text and Knowledge Visualization](./visualization.md#text-and-knowledge-visualization)
- [Learning Resources](./learning-resources.md)
  - [Becoming a Bioinformatician](./learning-resources.md#becoming-a-bioinformatician)
  - [Bioinformatics on GitHub](./learning-resources.md#bioinformatics-on-github)
  - [Sequencing](./learning-resources.md#sequencing)
  - [RNA-Seq](./learning-resources.md#rna-seq)
  - [ChIP-Seq](./learning-resources.md#chip-seq)
  - [YouTube Channels and Playlists](./learning-resources.md#youtube-channels-and-playlists)
  - [Blogs](./learning-resources.md#blogs)
  - [Miscellaneous](./learning-resources.md#miscellaneous)
- [Events and online groups](./online-networking-groups.md)
- [Research Groups and topics](./research-groups.md)
  - [Biology](./research-groups.md#biology)
  - [Computational Biology](./research-groups.md#computational-biology)
  - [Health Informatics](./research-groups.md#health-informatics)
  - [Imaging](./research-groups.md#imaging)
  - [Neuroscience](./research-groups.md#neuroscience)
  - [Biomechanics](./research-groups.md#biomechanics)
  - [Text and Knowledge](./research-groups.md#text-and-knowledge)
  - [Other](./research-groups.md#other)
- [Companies and startups](./companies.md)