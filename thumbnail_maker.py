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
from threading import Thread, Lock
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
        self.img_queue = multiprocessing.JoinableQueue()
        self.dl_size = 0
        self.resized_size = multiprocessing.Value('i', 0)

    def download_image(self, dl_queue, dl_size_lock):
        """
        Download each image and save to the input dir
        :param dl_queue: download queue
        :param dl_size_lock: download size lock
        """
        while not dl_queue.empty():
            try:
                url = dl_queue.get(block=False)
                logp("Downloading image at URL {url} and save to the input dir".format(url=url))
                img_file_name = urlparse(url).path.split('/')[-1]
                img_filepath = self.input_dir + os.path.sep + img_file_name
                urlretrieve(url, img_filepath)
                with dl_size_lock:
                    self.dl_size += os.path.getsize(img_filepath)
                self.img_queue.put(img_file_name)

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
            logp("Image [{size} bytes] saved to {path}.".format(size=img_size, path=dest_path))
        end = time.perf_counter()

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
        resolutions = [16, 32, 64, 128, 256, 512]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()
        while True:
            file_name = self.img_queue.get()
            if file_name:
                logp("Resizing image {}.".format(file_name))
                orig_img = Image.open("{}{}{}".format(self.input_dir, os.path.sep, file_name))
                for base_width in resolutions:
                    image = orig_img
                    # calculate target height of resized image to maintain the aspect ratio
                    w_percent = base_width / float(image.size[0])

                    # Perform resizing
                    image = image.resize(
                        (base_width, int(float(image.size[1]) * float(w_percent))),
                        PIL.Image.LANCZOS
                    )

                    # save the resized image to the output dir with a modified file name
                    new_filename = os.path.splitext(file_name)[0] + \
                        '_' + str(base_width) + os.path.splitext(file_name)[1]
                    out_filepath = self.output_dir + os.path.sep + new_filename
                    image.save(out_filepath)

                    with self.resized_size.get_lock():
                        self.resized_size.value += os.path.getsize(out_filepath)

                os.remove(self.input_dir + os.path.sep + file_name)
                logp("Done resizing image {file}.".format(file=file_name))
                self.img_queue.task_done()
            else:
                self.img_queue.task_done()
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
        target_sizes = [16, 32, 64, 128, 256, 512]
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
            new_filename = os.path.splitext(filename)[0] + '_' + str(basewidth) + \
                os.path.splitext(filename)[1]
            img.save(self.output_dir + os.path.sep + new_filename)

        os.remove(self.input_dir + os.path.sep + filename)
        logp("Done resizing image {file}.".format(file=filename))

    def make_thumbnails(self, img_url_list):
        """:param img_url_list: check the existing list"""
        logp("START make_thumbnails")
        start = time.perf_counter()

        dl_queue = Queue()
        dl_size_lock = Lock()

        for img_url in img_url_list:
            dl_queue.put(img_url)

        num_dl_threads = 4
        for _ in range(num_dl_threads):
            thr = Thread(target=self.download_image, args=(dl_queue, dl_size_lock))
            thr.start()

        num_processes = multiprocessing.cpu_count()
        for _ in range(num_processes):
            pro = multiprocessing.Process(target=self.perform_resizing)
            pro.start()

        dl_queue.join()
        for _ in range(num_processes):
            self.img_queue.put(None)

        end = time.perf_counter()
        logp("END make_thumbnails in {time:f} seconds".format(time=end - start))
        logp("Initial size of downloads: [{init}]. Final size of images: [{final}]".format(
            init=self.dl_size, final=self.resized_size.value
        ))


def logp(stri):
    """
    Static function that only does logging and printing
    :param stri: strings to log and print
    """
    logging.info(stri)
    print(stri)
