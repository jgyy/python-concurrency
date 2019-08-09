"""
thumbnail_maker.py
"""
import time
import os
import logging
# noinspection PyCompatibility
from urllib.parse import urlparse
import multiprocessing
# noinspection PyCompatibility
import asyncio
import aiohttp
import aiofiles

import PIL
from PIL import Image

FORMAT = "[%(threadName)s, %(asctime)s, %(levelname)s] %(message)s"
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)


# noinspection PyCompatibility
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

    async def download_image_coro(self, session, url):
        """
        Download each image and save to the input dir
        :param session: download queue
        :param url: download size lock
        """
        logp("Downloading image at URL {url} and save to the input dir".format(url=url))
        img_file_name = urlparse(url).path.split('/')[-1]
        img_filepath = self.input_dir + os.path.sep + img_file_name

        async with session.get(url) as response:
            async with aiofiles.open(img_filepath, 'wb') as file:
                content = await response.content.read()
                await file.write(content)

        self.dl_size += os.path.getsize(img_filepath)
        self.img_queue.put(img_file_name)

    async def download_images_coro(self, img_url_list):
        """
        download images with async function
        :param img_url_list: the list of all image url
        """
        async with aiohttp.ClientSession() as session:
            for url in img_url_list:
                await self.download_image_coro(session, url)

    def download_images(self, img_url_list):
        """
        download images with concurrency and validate inputs
        :param img_url_list: validate inputs
        :return: nothing if there is no image
        """
        if not img_url_list:
            return
        os.makedirs(self.input_dir, exist_ok=True)

        logp("Beginning image downloads.")
        start = time.perf_counter()
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.download_images_coro(img_url_list))
        finally:
            loop.close()

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

        num_processes = multiprocessing.cpu_count()
        for _ in range(num_processes):
            pro = multiprocessing.Process(target=self.perform_resizing)
            pro.start()

        self.download_images(img_url_list)

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
