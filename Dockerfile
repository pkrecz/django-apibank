FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/home/apibank
ENV WDIR=$APP_HOME/app

RUN mkdir $APP_HOME
RUN mkdir $WDIR
RUN mkdir $WDIR/staticfiles
RUN mkdir $WDIR/mediafiles

WORKDIR $WDIR

COPY requirements.txt $WDIR

RUN pip install --no-cache-dir -r $WDIR/requirements.txt

COPY . $WDIR/

CMD ["gunicorn", "apibankproject.wsgi:application"]
