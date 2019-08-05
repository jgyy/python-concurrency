"""
thumbnail_maker.py
"""
import time
import os
import logging
# noinspection PyCompatibility
from urllib.parse import urlparse
# noinspection PyCompatibility
from urllib.request import urlretrieve
import threading

import PIL
from PIL import Image

FORMAT = "[%(threadName)s, %(asctime)s, %(levelname)s] %(message)s"
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)


class ThumbnailMakerService:
    """
    thumbnail maker service class
    """
    def __init__(self, home_dir='.'):
        self.home_dir = home_dir
        self.input_dir = self.home_dir + os.path.sep + 'incoming'
        self.output_dir = self.home_dir + os.path.sep + 'outgoing'
        self.downloaded_bytes = 0
        self.dl_lock = threading.Lock()
        max_concurrent_dl = 4
        self.dl_sem = threading.Semaphore(max_concurrent_dl)

    def download_image(self, url):
        """
        download each image and save to the input dir
        :param url: the link for each image
        """
        with self.dl_sem:
            logp("downloading image at URL " + url)
            img_filename = urlparse(url).path.split('/')[-1]
            dest_path = self.input_dir + os.path.sep + img_filename
            urlretrieve(url, self.input_dir + os.path.sep + img_filename)
            img_size = os.path.getsize(dest_path)
            with self.dl_lock:
                self.downloaded_bytes += img_size
            logp("image [{size} bytes] saved to {path}".format(size=img_size, path=dest_path))

    def download_images(self, img_url_list):
        """
        :param img_url_list: validate inputs
        :return: nothing if there is no image
        """
        # validate inputs
        if not img_url_list:
            return
        os.makedirs(self.input_dir, exist_ok=True)

        logp("beginning image downloads")
        start = time.perf_counter()

        threads = []
        for url in img_url_list:
            thr = threading.Thread(target=self.download_image(url))
            thr.start()
            threads.append(thr)
        for thre in threads:
            thre.join()

        end = time.perf_counter()
        logp("downloaded {img:d} images in {time:f} seconds".format(
            img=len(img_url_list), time=end - start
        ))

    def perform_resizing(self):
        """
        validate inputs
        :return: returns nothing if no input
        """
        if not os.listdir(self.input_dir):
            return
        os.makedirs(self.output_dir, exist_ok=True)

        logp("beginning image resizing")
        target_sizes = [32, 64, 128, 256]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()
        for filename in os.listdir(self.input_dir):
            orig_img = Image.open(self.input_dir + os.path.sep + filename)
            print(filename)
            for basewidth in target_sizes:
                print(basewidth)
                img = orig_img
                # calculate target height of the resized image to maintain the aspect ratio
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                # perform resizing
                img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)

                # save the resized image to the output dir with a modified file name
                new_filename = os.path.splitext(filename)[0] + \
                    '_' + str(basewidth) + os.path.splitext(filename)[1]
                img.save(self.output_dir + os.path.sep + new_filename)

            os.remove(self.input_dir + os.path.sep + filename)
        end = time.perf_counter()

        logp("created {img:d} thumbnails in {time:f} seconds".format(
            img=num_images, time=end - start
        ))

    def make_thumbnails(self, img_url_list):
        """
        :param img_url_list: check the existing list
        """
        logp("START make_thumbnails")
        start = time.perf_counter()

        self.download_images(img_url_list)
        self.perform_resizing()

        end = time.perf_counter()
        logp("END make_thumbnails in {time:f} seconds".format(time=end - start))


def logp(stri):
    """
    Static function that only does logging and printing
    :param stri: strings to log and print
    """
    logging.info(stri)
    print(stri)
