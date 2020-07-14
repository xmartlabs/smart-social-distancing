#!/usr/bin/python3
import argparse
from multiprocessing import Process, Queue
import threading
from libs.config_engine import ConfigEngine
import logging

logger = logging.getLogger(__name__)


def start_engine(config):
    video_path = config.get_section_dict("App").get("VideoPath", None)
    if video_path:
        from libs.core import Distancing as CvEngine
        engine = CvEngine(config)
        engine.process_video(video_path)
    else:
        logger.warning('Skipping CVEngine as video_path is not set in config file')


def start_api(config, message_queue):
    from api.processor_api import ProcessorAPI
    api = ProcessorAPI(config, message_queue)
    api.start()

def update_config(process_engine, event, config):
    logger.info(event['data'])
    logger.info("Restarting CV Engine.")
    process_engine.terminate()
    process_engine.join()
    config.update_config(event['data'], event['options']['save_file'])
    process_engine = Process(target=start_engine, args=(config,))
    process_engine.start()
    logger.info("CV Engine restarted.")
    return process_engine

def main(config):
    logging.basicConfig(level=logging.INFO)
    if isinstance(config, str):
        config = ConfigEngine(config)


    process_engine = Process(target=start_engine, args=(config,))
    message_queue = Queue()
    process_api = Process(target=start_api, args=(config, message_queue))

    process_api.start()
    process_engine.start()
    logger.info("Services Started.")

    try:
        # Wait for messages
        while True:
            event = message_queue.get()
            if event is None:
                break
            if event['action'] == 'update_config':
                process_engine = update_config(process_engine, event, config)

    except KeyboardInterrupt:
        logger.info("Received interrupt. Terminating...")

    process_engine.terminate()
    process_engine.join()
    logger.info("CV Engine terminated.")
    process_api.terminate()
    process_api.join()
    logger.info("Processor API terminated.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    args = parser.parse_args()
    main(args.config)
