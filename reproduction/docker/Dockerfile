# Source: https://github.com/TomMonks/treatment-centre-sim/blob/main/Dockerfile

# Use publicly available Linux-Miniconda image
# start with miniconda image
FROM continuumio/miniconda3:latest

# Create and set the working directory to the container make copy simpler
RUN mkdir /home/code
RUN mkdir /home/original_study
WORKDIR /home/code

# Copy all files across to container
COPY ./reproduction /home/code

# Copy jupyter config file
COPY ./reproduction/docker/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# Copy the files from original_study/ required for comparisons
COPY ./original_study/supp_tab2_reformat.csv /home/original_study/supp_tab2_reformat.csv
COPY ./original_study/supp_tab3_reformat.csv /home/original_study/supp_tab3_reformat.csv
COPY ./original_study/supp_tab4_reformat.csv /home/original_study/supp_tab4_reformat.csv
COPY ./original_study/supp_tab5_reformat.csv /home/original_study/supp_tab5_reformat.csv
COPY ./original_study/supp_tab6_reformat.csv /home/original_study/supp_tab6_reformat.csv

# Install anaconda, conda-forge and pip dependencies
RUN conda update conda && conda env create -f environment.yaml && conda clean -afy 

# Make RUN commands use the new environment (not really necessary here)...
SHELL ["conda", "run", "-n", "lim2020", "/bin/bash", "-c"]

# Declare port used by jupyter-lab
EXPOSE 80

# Launch JupyterLab
CMD jupyter-lab /home/code/