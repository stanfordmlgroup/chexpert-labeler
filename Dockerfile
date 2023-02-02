FROM continuumio/miniconda

RUN apt-get update --allow-releaseinfo-change
RUN mkdir -p /usr/share/man/man1
RUN apt-get install -y default-jre

WORKDIR /app/chexpert-labeler

RUN git clone https://github.com/ncbi-nlp/NegBio.git
ENV PYTHONPATH=NegBio:$PYTHONPATH

COPY environment.yml environment.yml
RUN conda env create -f environment.yml

# Copy chexpert-labeler (see .dockerignore)
COPY . .
RUN chmod +x ./entrypoint.sh

RUN ./entrypoint.sh python -m nltk.downloader universal_tagset punkt wordnet
RUN ./entrypoint.sh python -c "from bllipparser import RerankingParser; RerankingParser.fetch_and_load('GENIA+PubMed')"

# Run labeler on sample reports. This will download and cache CoreNLP in the docker image.
COPY sample_reports.csv .
RUN ./entrypoint.sh python label.py --reports_path sample_reports.csv --output_path labeled_reports.csv --verbose

ENTRYPOINT ["./entrypoint.sh"]
