import argparse
import logging


def cli():
    parser = argparse.ArgumentParser(description="Process a video from YouTube or a local file.")
    parser.add_argument("--youtube", help="URL to a YouTube video to process.", type=str)
    parser.add_argument("--local", help="Path to a local video file to process.", type=str)
    args = parser.parse_args()
    logging.debug(f"Supplied args: {args}")
    return args
