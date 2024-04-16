FROM mambaorg/micromamba:1.5.8 AS micromamba

USER root
RUN apt update && apt install -y git
USER $MAMBA_USER

COPY --chown=$MAMBA_USER:$MAMBA_USER . .

RUN micromamba install --yes --name "base" --file "environment.yml"
RUN micromamba clean --all --yes

# ENV PATH "/opt/conda/bin:${PATH}"
