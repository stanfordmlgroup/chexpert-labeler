FROM continuumio/miniconda

# Install Java
# https://yarnaudov.com/fix-java-jdk-jre-debian-ubuntu-install.html
RUN apt-get update --allow-releaseinfo-change
RUN mkdir -p /usr/share/man/man1
RUN apt-get install -y default-jre


WORKDIR /app/chexpert-labeler

# Install prerequisites
RUN git clone https://github.com/ncbi-nlp/NegBio.git
ENV PYTHONPATH=NegBio:$PYTHONPATH

COPY environment.yml environment.yml
RUN conda env create -f environment.yml

# Copy chexpert-labeler (see .dockerignore)
COPY . .
RUN chmod +x ./entrypoint.sh

RUN ./entrypoint.sh python -m nltk.downloader universal_tagset punkt wordnet
RUN ./entrypoint.sh python -c "from bllipparser import RerankingParser; RerankingParser.fetch_and_load('GENIA+PubMed')"

ENTRYPOINT ["./entrypoint.sh"]
