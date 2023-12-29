# Copyright (c) Meta, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04 
# nividia/cuda:11.1.1-cudnn8-devel-ubuntu18.04 is the latest version of CUDA that supports PyTorch 1.4.0
# for PyTorch 2.0.0 and above, use nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04 

# Installing the required packages
RUN apt update -y
# apt update -y is required to update the package list
RUN apt install -y git curl
# git and curl are required to download the ParlAI repo and Anaconda installer

# Installing Anaconda
WORKDIR /root 
RUN curl https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh -o anaconda_installer.sh
RUN bash anaconda_installer.sh -b -p
# -b is for batch mode, -p is for the installation path
ENV PATH="/root/anaconda3/bin:$PATH"

# Installing recommmended pre-requirements
RUN conda install "pytorch<1.13.0,>=1.4.0" torchvision torchaudio -c pytorch-lts -c nvidia
# "pytorch<1.13.0, >=1.4.0" means that the version of PyTorch should be greater than or equal to 1.4.0 and less than 1.13.0
RUN pip install spacy==3.2.4 tokenizers pandas transformers fairseq contractions boto3==1.17.95 botocore==1.20.95

# Configuring packages for English
RUN python -m spacy download en_core_web_sm
RUN echo "import nltk; nltk.download(\"stopwords\"); nltk.download(\"punkt\")" > nltk_dl_script.py
RUN python nltk_dl_script.py

# Download the ParlAI Github repo
RUN git clone https://github.com/facebookresearch/ParlAI.git ~/ParlAI

# Running ParlAI install
RUN cd ~/ParlAI && \
    pip install -r docker_requirements.txt && \
    python setup.py develop

CMD ["parlai", "party"]
# parlai party is the command to run the ParlAI party mode
