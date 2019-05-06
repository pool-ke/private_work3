from configs import settings

from Util import FileUtil
from Util import HBaseUtil
from Util import MapFileUtil
from Util import DumpFileUtil
from os.path import join

import pickle
import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

def getImage(imageId):
    if not FileUtil.exists(join(settings.images_cache_folder,imageId)):
        mapFileId=HBaseUtil.getMapFileId(imageId)
        logging.info(mapFileId)
        if mapFileId is None:
            logging.error('404')
            return '404'
        if FileUtil.exists(join(settings.mapfile_cache_folder,mapFileId)):
            print (111)
            DumpFileUtil.readMapFile(mapfileId)
        else:
            DumpFileUtil.readMapFileFromHdfs(mapFileId)
    folder_path=settings.images_cache_folder
    logging.info(folder_path)

if __name__ == '__main__':
    imageID="CAE_train_image-0_1_180328162225_OK.bmp"
    getImage(imageID)