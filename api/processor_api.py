import time
import numpy as np
from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from api.models.config_keys import *
import uvicorn
import os
import cv2 as cv
import logging

logger = logging.getLogger(__name__)

class ProcessorAPI:
    """
    The ProcessorAPI object implements a fastapi application that should allow configuring, starting and stopping processing,
    and viewing the video stream processed by this processor node.

    :param config: Is a ConfigEngine instance which provides necessary parameters.
    :param engine_instance:  A ConfigEngine object which store all of the config parameters. Access to any parameter
        is possible by calling get_section_dict method.
    """

    def __init__(self, config, message_queue):
        self.config = config
        self._host = self.config.get_section_dict("App")["Host"]
        self._port = int(self.config.get_section_dict("App")["Port"])
        self.message_queue = message_queue
        self.app = self.create_fastapi_app()

    @staticmethod
    def validate_video_path(video_uri):
        input_cap = cv.VideoCapture(video_uri)

        if input_cap.isOpened() :
            _, cv_image = input_cap.read()
            if np.shape(cv_image) == ():
                return False
        else:
            logger.error(f'failed to load video {video_uri}')
            return False

        input_cap.release()
        return True

    def validate_config(self, config):
        if 'App' in config.keys():
            if ('VideoPath' in config['App']) and (not self.validate_video_path(config['App']['VideoPath'])):
                return [False, 'video_path is invalid']

        return [True, '']

    def create_fastapi_app(self):
        # Create and return a fastapi instance
        app = FastAPI()

        if os.environ.get('DEV_ALLOW_ALL_ORIGINS', False):
            # This option allows React development server (which is served on another port, like 3000) to proxy requests
            # to this server.
            # WARNING: read this before enabling it in your environment:
            # https://medium.com/@stestagg/stealing-secrets-from-developers-using-websockets-254f98d577a0
            from fastapi.middleware.cors import CORSMiddleware
            app.add_middleware(CORSMiddleware, allow_origins='*', allow_credentials=True, allow_methods=['*'],
                               allow_headers=['*'])
        app.mount("/static", StaticFiles(directory="/repo/data/processor/static"), name="static")

        @app.put("/config")
        async def update_config(config_request: ConfigRequest):
            save_file = config_request.save_file
            config_request = config_request.dict(exclude_unset=True, exclude_none=True)
            config = config_request['config']

            is_valid, message = self.validate_config(config)
            if not is_valid:
                raise HTTPException(status_code=400, detail=message)

            self.message_queue.put({
                'action': 'update_config',
                'options': {'save_file': save_file},
                'data': config
            })
            return config_request

        return app

    def start(self):
        uvicorn.run(self.app, host=self._host, port=self._port, log_level='info', access_log=False)
