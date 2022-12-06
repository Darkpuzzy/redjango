FROM python:3.9

EXPOSE 8080
RUN mkdir -p /usr/src/red-app/

WORKDIR /usr/src/red-app/

COPY ./ ./
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt