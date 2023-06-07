#!/usr/bin/env python3

import signal
import sys
import os
import time
from ingestor import Ingestor

if __name__ == "__main__":

  # Define a signal handler to handle termination signals
  def signal_handler(signal, frame):
    ingestor.stop()
    sys.exit(0)

  # Register signal handlers for termination signals
  signal.signal(signal.SIGINT, signal_handler)  # SIGINT: Ctrl+C
  signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM: OS Termination signal

  try:
    ingestor = Ingestor()
    ingestor.start()

  except KeyboardInterrupt:
    # Handle a keyboard interrupt (Ctrl+C) gracefully
    signal_handler(signal.SIGINT, None)

  