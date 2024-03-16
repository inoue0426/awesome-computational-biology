# Awesome Computational Biology [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A knowledge collection of databases, software and papers related to computational biology.

> Computational biology involves the development and application of data-analytical and theoretical methods,
> mathematical modelling and computational simulation techniques to the study of biological, ecological,
> behavioural, and social systems. - [Wikipedia](https://en.wikipedia.org/wiki/Computational_biology)

## Contents

- [Databases](#databases)
  - [scRNA](#scrna)
  - [Compound](#compound)
  - [Pathway](#pathway)
  - [Mass Spectra](#mass-spectra)
  - [Protein](#protein)
  - [Genome](#genome)
  - [Disease](#disease)
  - [Interaction](#interaction)
- [Preprocess](#preprocess)
- [Machine Learning Tasks and Models](#machine-learning-tasks-and-models)
  - [Drug Repurposing](#drug-repurposing)
  - [Drug Target Interaction](#drug-target-interaction)
  - [Compound Protein Interaction](#compound-protein-interaction)
- [Pre-trained embedding](#pre-trained-embedding)
- [LLM for biology](#llm-for-biology)

## Databases
### scRNA
- [Gene Expression Omnibus](https://www.ncbi.nlm.nih.gov/geo/) - Public functional genemics database.
- [Single Cell PORTAL](https://singlecell.broadinstitute.org/single_cell) - Public database for single cell RNA.
- [Single Cell Expression Atlas](https://www.ebi.ac.uk/gxa/sc/home) - Public database for single cell RNA.
### Compound
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) - One of the biggest chemical database such as compounds, genes and proteins.
- [ChEBI](https://www.ebi.ac.uk/chebi/) - Chemical database  focused on small chemical compounds.
- [ChEMBL](https://www.ebi.ac.uk/chembl/) - Database of bioactive molecules with drug-like properties.
- [ChemSpider](http://www.chemspider.com/) - Chemical structure database.
- [KEGG COMPOUND](https://www.genome.jp/kegg/compound/) - Collection of small molecules and biopolymers.
- [LIPID MAPS](https://www.lipidmaps.org/databases/lmsd/overview) - Database of lipids.
- [Rhea](https://www.rhea-db.org/) - Database of chemical reactions.
- [Drug Repurposing Hub](https://repo-hub.broadinstitute.org/repurposing#download-data) - Collections of drug repurposing data containing drug, moa, target etc.
### Pathway
- [PathwayCommons](https://www.pathwaycommons.org/) - Database of Pathways and Interactions.
- [KEGG PATHWAY](https://www.genome.jp/kegg/pathway.html) - Collection fo drawn pathway maps.
- [WikiPathways](https://wikipathways.org/) - Database of biological pathways.
### Mass Spectra
- [MassBank](http://www.massbank.jp/) - Open souce databases and tools for mass spectrometry reference spectra.
- [MoNA MassBank of North America](https://mona.fiehnlab.ucdavis.edu/) - Meta database of metabolite mass spectra, metadata and associated compounds.
### Protein
- [THE HUMAN PROTEIN ATLAS](https://www.proteinatlas.org/) - One of the biggest human protein database contained cells, tissues, and organs. 
- [PROTEIN DATA BANK](https://www.rcsb.org/) - Database of the 3D shapes of proteins, nucleic acids, and complex assemblies.
- [UniProt](https://www.uniprot.org/) - The collection of functional information on proteins.
- [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/api-docs) - Database of 3D protein structures.
### Genome
- [Human Genome Resources at NCBI](https://www.ncbi.nlm.nih.gov/projects/genome/guide/human/index.shtml) - Database of image, proteomics, transcriptomics and systems biology.
- [GenBank](https://www.ncbi.nlm.nih.gov/genbank/) - Database of genetic sequence offered by NCBI.
- [UCSC Genome Browser](https://genome.ucsc.edu/) - Genome blowser offered by UCSC.
- [cBioPortal](https://www.cbioportal.org/) - Database of Cancer Genomics. This has overall metaview for a lot of patients.
### Disease
- [KEGG DRUG](https://www.genome.jp/kegg/drug/) - Comprehensive drug information resource for approved drugs.
- [DrugBank](https://www.drugbank.com/) - A database of drug and target maintained by the University of Alberta.
### Interaction
- Drug Gene Interaction
  - [DGIdb](https://www.dgidb.org/) - A database of drug-gene interactions and the druggable genome.
  - [Comparative Toxicogenomics Database](http://ctdbase.org/) - A database of Chemical-gene interactions, Chemical-disease associations, Gene-disease associations, and Chemical-phenotype associations.
  - [SNAP](https://snap.stanford.edu/biodata/datasets/10002/10002-ChG-Miner.html#:~:text=Dataset%20information,or%20activation%20of%20the%20drug.) - A dataset which contains Drug-gene interactions. 
  - [Comparative Toxicogenomics Database](https://ctdbase.org/) - A database for drug-target interactions.
  - [Therapeutics Data Commons](https://tdcommons.ai/) - A database for a lot of tasks such as drug-target, drug-response, drug-drug interaction.
- Drug (-Cell line) Response
  - [NCI60](https://dtp.cancer.gov/discovery_development/nci-60/) A database which focus on 60 cancer cell lines with many drugs.
  - [Genomics of Drug Sensitivity in Cancer (GDSC)](https://www.cancerrxgene.org/) - A database of drug sensitibity which has 1000 human cancer cell lines and 100s compounds.
  - [Cancer Cell Line Encyclopedia](https://sites.broadinstitute.org/ccle/) - A database of cancer cell lines. This has 1000 cell lines.
- Chemical Protein Interaction
  - [STITCH](http://stitch.embl.de/) - A database of Chemical Protein Interaction.
  - [BindingDB](https://www.bindingdb.org/rwd/bind/index.jsp) - A database of compounds and targes.
- Protein-Protein Interaction
  - [STRING](https://string-db.org/) - Protein-Protein Interaction Networks for several organisms.
  - [BioGRID](https://thebiogrid.org/) - Database of Protein, Genetic and Chemical Interactions.
  - [HIPPIE](http://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/) - Human Protein-Protein Interaction database.

## Preprocess

- [Chemistry Development Kit](https://github.com/cdk/cdk) - A software of cheminformatics and Machine Learning.
- [RDKit](https://github.com/rdkit/rdkit) - A software of cheminformatics and Machine Learning.
- [Scanpy](https://scanpy.readthedocs.io/en/stable/) - scRNA analysis library in Python.
- [Seurat](https://satijalab.org/seurat/) - scRNA analysis library in R.

## Machine Learning Tasks and Models

### Drug Repurposing

- [DeepPurpose](https://github.com/kexinhuang12345/DeepPurpose) - A DL Library for Drug Repurposing and so on. 
- [DRKG](https://github.com/gnn4dr/DRKG) - A library for biological knowledge graph.

### Drug Target Interaction

- [NeoDTI](https://github.com/FangpingWan/NeoDTI) - A library for Drug Target Interaction.

### Compound Protein Interaction

- [MCPINN](https://github.com/mhlee0903/multi_channels_PINN) - A library for drug discovery using Compound Protein Interaction and Machine Learning.
- [TransformerCPI](https://github.com/lifanchen-simm/transformerCPI) - A library for Compound Protein Interaction prediction using Transformer.

## Pre-trained embedding

- [Evolutionary Scale Modeling](https://github.com/facebookresearch/esm) - a library for protein embeddings.
- [ChemBERTa-2](https://github.com/seyonechithrananda/bert-loves-chemistry) - a library for chemical embeddingg and prediction.

## LLM for biology

- [AI4Chem/ChemLLM-7B-Chat](https://huggingface.co/AI4Chem/ChemLLM-7B-Chat) - LLM for chemical and molecule science
- [BioGPT](https://github.com/microsoft/BioGPT) - LLM for Biomedical text generation



