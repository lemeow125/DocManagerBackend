FROM python:3.13.0-bullseye

ENV PYTHONBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . /app/
ADD . /app/
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/start.sh

# Install packages
RUN apt update && apt install -y graphviz libgraphviz-dev graphviz-dev
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Expose port 8000 for the web server
EXPOSE 8000

ENTRYPOINT [ "/app/scripts/start.sh" ]