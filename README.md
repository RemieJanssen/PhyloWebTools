# PhyloWebTools
Web-based tools for phylogenetic networks

## Run

First build and activate the conda environment defined in `envs/phylo-web-tools.source.yml`.
Then run the tool with the command `flask run`.

## Dev

### Conda lock
Lock/pin the package versions
```
cd ./envs
conda env update -f ./phylo-web-tools.source.yml
conda activate phylo-web-tools
conda env export > phylo-web-tools.yml
```