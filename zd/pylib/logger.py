import logging
import os
from pathlib import Path

this_file_path = Path(os.path.abspath(__file__))
logger = logging.getLogger()
logging.basicConfig(filename=os.path.join(this_file_path.parent, '..', 'log', 'kitelog.log'),
                    level=logging.DEBUG,
                    filemode='a',
                    format='%(asctime)s: %(filename)s: %(message)s')
