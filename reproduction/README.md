# Reproduction README

## Model summary

> Lim CY, Bohn MK, Lippi G, Ferrari M, Loh TP, Yuen K, Adeli K, Horvath AR **Staff Rostering, Split Team Arrangement, Social Distancing (Physical Distancing) and Use of Personal Protective Equipment to Minimize Risk of Workplace Transmission During the COVID-19 Pandemic: A Simulation Study**. *Clinical Biochemistry* 86:15-22 (2020). <https://doi.org/10.1016/j.clinbiochem.2020.09.003>.

This is a discrete-event simulation modelling the transmission of COVID-19 in laboratory. It examines the proportion of staff infected in scenarios varying the: number of shifts per day; number of staff per shift; overall staff pool; shift patterns; secondary attack rate of the virus; introduction of protective measures (social distancing and personal protective equipment). The model is created using Python.

## Scope of the reproduction

In this assessment, we attempted to reproduce 9 items: 4 figures and 5 tables.

## Reproducing these results

### Repository overview

```{bash}
├── docker
│   └──  ...
├── outputs
│   └──  ...
├── scripts
│   └──  ...
├── tests
│   └──  ...
├── environment.yaml
└── README.md
```

* `docker/` - Instructions for creation of Docker container.
* `outputs/` - Output files from the model.
* `scripts/` - Code for the model and for reproducing items from the scope.
* `tests/` - Test to check that model produces consistent results with our reproduction.
* `environment.yaml` - Instructions for creation of python environment.
* `README.md` - This file!

### Step 1. Set up environment

#### Option A: Conda/mamba environment

A `conda`/`mamba` environment has been provided. To create this environment on your machine, you should run this command in your terminal: `conda env create -f environment.yaml`.

You can then use this environment in your preferred IDE, such as VSCode (where you will be asked to select the kernel/interpreter). You can activate it in the terminal by running `conda activate lim2020`.

You can run either of these commands also using `mamba` instead (e.g. `mamba activate lim2020`).

#### Option B: Build local docker image

A `Dockerfile` is provided, which you can use to build the Docker image. The docker image will include the correct version of Python and the packages, and an installation of jupyterlab which you can run from your browser. It will also include the scripts and outputs from this directory.

For this option (and option C), you'll need to ensure that `docker` is installed on your machine.

To create the docker image and then open jupyter lab:

1. In the terminal, navigate to parent directory of the `reproduction/` folder
2. Build the image: `sudo docker build --tag lim2020 . -f ./reproduction/docker/Dockerfile`
3. Create a docker container from that image and open jupyter lab: `(sleep 2 && xdg-open http://localhost:8080) & sudo docker run -it -p 8080:80 --name lim2020_docker lim2020`

#### Option C: Pull pre-built docker image

A pre-built image is available on the GitHub container registry. To use it:

1. Create a Personal Access Token (Classic) for your GitHub account with `write:packages` and `delete:packages` access
2. On terminal, run `sudo docker login ghcr.io -u githubusername` and enter your sudo password (if prompted), followed by the token just generated (which acts as your GitHub password)
3. Download the image: `sudo docker pull ghcr.io/pythonhealthdatascience/lim2020`
4. Create container and open RStudio: `(sleep 2 && xdg-open http://localhost:8080) & sudo docker run -it -p 8080:80 --name lim2020_docker ghcr.io/pythonhealthdatascience/lim2020:latest`

### Step 2. Running the model

#### Option A: Execute the notebooks

To run all the model scenarios, open and execute the provided `ipynb` files in `scripts/`. You can do so within your preferred IDE (e.g. VSCode, JupyterLab).

#### Option B: Pytest

Two of the model scenarios have been included as tests within `tests/`. You can run these by executing the following command from your terminal whilst in the `reproduction/` directory with the `lim2020` environment active:

`pytest`

This will run the two scenarios and compare the results against those we have saved. Although this will not produce any figures from the paper, and will not run all the scenarios, it will allow you to check if you are getting results consistent with our reproduction, on your own machine.

Once the tests begin to run, you should see information indicating the test has started, but then should expect to see no further updates to the screen until both tests have completed.

Example of output when start tests:

```{bash}
=========================================================================== test session starts ============================================================================
platform linux -- Python 3.8.5, pytest-7.4.4, pluggy-1.0.0
rootdir: /home/amy/Documents/stars/stars-reproduce-lim-2020/reproduction
plugins: xdist-3.6.1
collected 2 items                                                                                                                                                          

tests/test_model.py .. 
```

Example of finished tests (if both tests passed):

```{bash}
============= 2 passed, 9 warnings in 395.17s (0:06:35) =============
```


## Reproduction specs and runtime

This reproduction was conducted on an Intel Core i7-12700H with 32GB RAM running Ubuntu 22.04.4 Linux.

On that machine, running all scenarios from scratch, the total run time is **49 minutes and 17 seconds**.

Run time for the tests was **6 minutes 35 seconds**.

## Citation

To cite the original study, please refer to the reference above. To cite this reproduction, please refer to the CITATION.cff file in the parent folder.

## License

This repository is licensed under the MIT License.