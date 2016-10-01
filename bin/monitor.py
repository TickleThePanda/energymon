#! /usr/bin/python3

import signal
import sys

from gpiozero import MCP3008
from time import sleep

from datetime import datetime

from queue import Queue
import threading

def signal_handler(signal, frame):
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

readingQueue = Queue();

class Reading:
  def __init__(self, time, cR, vR):
    self.time = time
    self.cR = cR
    self.vR = vR
  def __str__(self):
    return "%s,%s,%s" % (self.time, self.cR, self.vR)

def reader():
  while True:
    with MCP3008(channel=1) as reading:
      current = reading.value
    with MCP3008(channel=2) as reading:
      voltage = reading.value
    time = datetime.now()

    reading = Reading(time, current, voltage)

    readingQueue.put(reading)

def writer():
  while True:
    print(readingQueue.get(), readingQueue.qsize())


readerThread = threading.Thread(target=reader)
readerThread.daemon = True
readerThread.start()

writerThread = threading.Thread(target=writer)
writerThread.daemon = True
writerThread.start()

readerThread.join()
writerThread.join()
