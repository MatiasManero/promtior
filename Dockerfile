# Imagen base Ubuntu (Python 3.12 en repos oficiales). Ejecución con usuario no root.
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

# Python 3.12 + pip + venv + herramientas (repos oficiales de Ubuntu 24.04)
RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /app

# Ambiente virtual al mismo nivel que la aplicación (/app/.venv)
ENV VIRTUAL_ENV=/app/.venv
RUN python3 -m venv "$VIRTUAL_ENV" \
    && . "$VIRTUAL_ENV/bin/activate" \
    && pip install --upgrade pip
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Proyecto y dependencias dentro del venv
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Usuario no root para ejecutar la aplicación
RUN useradd --uid 1001 --gid 1000 --shell /bin/bash --create-home user \
    && mkdir -p /app/data \
    && chown -R user:user /app

EXPOSE 8000

USER user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
