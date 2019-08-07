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
# noinspection PyCompatibility
from queue import Queue, Empty
import threading
from threading import Thread
import multiprocessing

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
        self.img_list = []

    def download_image(self, dl_queue):
        """
        Download each image and save to the input dir
        :param dl_queue: download queue
        """
        while not dl_queue.empty():
            try:
                url = dl_queue.get(block=False)
                logp("Downloading image at URL " + url)
                img_filename = urlparse(url).path.split('/')[-1]
                dest_path = self.input_dir + os.path.sep + img_filename
                urlretrieve(url, self.input_dir + os.path.sep + img_filename)
                img_size = os.path.getsize(dest_path)
                self.img_list.append(img_filename)
                logp("Image [{size} bytes] saved to {path}.".format(size=img_size, path=dest_path))

                dl_queue.task_done()
            except Empty:
                logp("Queue empty")

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

        for url in img_url_list:
            # Download each image and save to the input dir
            logp("Downloading image at URL " + url)
            img_filename = urlparse(url).path.split('/')[-1]
            dest_path = self.input_dir + os.path.sep + img_filename
            urlretrieve(url, self.input_dir + os.path.sep + img_filename)
            img_size = os.path.getsize(dest_path)
            self.img_list.append(img_filename)
            logp("Image [{size} bytes] saved to {path}.".format(size=img_size, path=dest_path))
        end = time.perf_counter()

        self.img_list.append(None)

        logp("Downloaded {img:d} images in {time:f} seconds.".format(
            img=len(img_url_list), time=end - start
        ))

    def perform_resizing(self):
        """
        validate inputs
        :return: returns nothing if no input
        """
        os.makedirs(self.output_dir, exist_ok=True)

        logp("Beginning image resizing.")
        target_sizes = [32, 64, 128, 256]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()
        while True:
            filename = self.img_list[0]
            if filename:
                logp("Resizing image {file}.".format(file=filename))
                orig_img = Image.open(self.input_dir + os.path.sep + filename)
                for basewidth in target_sizes:
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
                logp("Done resizing image {file}.".format(file=filename))
                print(self.img_list)
            else:
                print(self.img_list)
                break

        end = time.perf_counter()
        logp("Created {img:d} thumbnails in {time:f} seconds.".format(
            img=num_images, time=end - start
        ))

    def resize_image(self, filename):
        """
        resize 1 image function
        :param filename: name of the image file
        """
        target_sizes = [32, 64, 128, 256]
        logp("Resizing image {file}.".format(file=filename))
        orig_img = Image.open(self.input_dir + os.path.sep + filename)
        for basewidth in target_sizes:
            img = orig_img
            # calculate target height of the resized image to maintain the aspect ratio
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            # perform resizing
            img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)

            # save the resized image to the output dir with a modified file name
            new_filename = os.path.splitext(filename)[0] + '_' + str(basewidth) + os.path.splitext(filename)[1]
            img.save(self.output_dir + os.path.sep + new_filename)

        os.remove(self.input_dir + os.path.sep + filename)
        logp("Done resizing image {file}.".format(file = filename))

    def make_thumbnails(self, img_url_list):
        """
        :param img_url_list: check the existing list
        """
        logp("START make_thumbnails")
        pool = multiprocessing.Pool()
        start = time.perf_counter()
        dl_queue = Queue()

        for img_url in img_url_list:
            dl_queue.put(img_url)

        num_dl_threads = 4
        for _ in range(num_dl_threads):
            thr = Thread(target=self.download_image, args=(dl_queue,))
            thr.start()
        dl_queue.join()

        start_resize = time.perf_counter()
        pool.map(self.resize_image, self.img_list)
        end_resize = time.perf_counter()

        end = time.perf_counter()
        pool.close()
        pool.join()
        logp("Created {th} thumbnails in {se} seconds.".format(
            th=str(len(self.img_list)), se=end_resize - start_resize
        ))
        logp("END make_thumbnails in {time:f} seconds".format(time=end - start))


def logp(stri):
    """
    Static function that only does logging and printing
    :param stri: strings to log and print
    """
    logging.info(stri)
    print(stri)
