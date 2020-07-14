FROM python:3.8-slim

COPY --from=neuralet/smart-social-distancing:latest-frontend /frontend/build /srv/frontend

COPY ui/requirements.txt /ui/
WORKDIR /ui

RUN python3 -m pip install --upgrade pip setuptools==41.0.0 && pip install -r requirements.txt
COPY ui/ /ui
COPY libs/config_engine.py /ui/
COPY config-frontend.ini /ui/

EXPOSE 8000
ENV DEV_ALLOW_ALL_ORIGINS=True

ENTRYPOINT ["python3", "web_gui.py"]
CMD ["--config", "config-frontend.ini"]
