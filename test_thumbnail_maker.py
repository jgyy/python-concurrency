"""
thumnbail maker script, may change the source
"""
from thumbnail_maker import ThumbnailMakerService

IMG_URLS = [
    'https://i.kinja-img.com/gawker-media/image/upload/s--gXbd2e1V--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/jvp8ftnuptptzrkbmwwy.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--RPPFz0Qr--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/vteo9oglifm6uykzi90a.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--FHzgs724--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/thok0ygjqbbucnocsb0h.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--FgqaCeME--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ajs0pcmeh4ollbnt5gxw.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--XhHj4A_x--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/dee608xivehmprkchnhx.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--C3g1bWMZ--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/rfn9ykjpcnaxuyfqwzf9.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--yR0DdAoE--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/m7vmbgzimblv4su9m2kb.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--9rg3INuV--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/lbkhmc8mvaz7ve0w2j5q.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--DzuAg0e2--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/gzdeepkdu9xik9dbhsux.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--rsurpTHL--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/zmxjrzddhnrd2u9oogln.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--ZL0yx1Ky--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/eolrqijtojpctifrruus.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--s0_a10yn--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/rnjkov3ygfnlouzbblsz.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--kfwsjd-S--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/zjwrlnjnt4joucs92av7.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--SX6NJkRp--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/bmy8w7gyegwa6l06ocn5.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--6VGkwAXX--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ynsxzkpy4nhzjhp6bo2z.jpg',
    'https://dl.dropboxusercontent.com/s/rjuggi2ubc1b3bk/pexels-photo-317156.jpeg',
    'https://dl.dropboxusercontent.com/s/cpaog2nwplilrz9/pexels-photo-317383.jpeg',
    'https://dl.dropboxusercontent.com/s/16x2b6ruk18gji5/pexels-photo-320007.jpeg',
    'https://dl.dropboxusercontent.com/s/xqzqzjkcwl52en0/pexels-photo-322207.jpeg',
    'https://dl.dropboxusercontent.com/s/frclthpd7t8exma/pexels-photo-323503.jpeg',
    'https://dl.dropboxusercontent.com/s/7ixez07vnc3jeyg/pexels-photo-324030.jpeg',
    'https://dl.dropboxusercontent.com/s/1xlgrfy861nyhox/pexels-photo-324655.jpeg',
    'https://dl.dropboxusercontent.com/s/v1b03d940lop05d/pexels-photo-324658.jpeg',
    'https://dl.dropboxusercontent.com/s/ehrm5clkucbhvi4/pexels-photo-325520.jpeg',
    'https://dl.dropboxusercontent.com/s/l7ga4ea98hfl49b/pexels-photo-333529.jpeg',
    'https://dl.dropboxusercontent.com/s/rleff9tx000k19j/pexels-photo-341520.jpeg'
]


def test_thumbnail_maker():
    """
    to run the thumbnail maker function
    """
    print("Starting of Test Thumbnail Maker.")
    tn_maker = ThumbnailMakerService()
    print("To commense making of thumbnails.")
    tn_maker.make_thumbnails(IMG_URLS)
    print("Completed making of thumbnails.")


if __name__ == '__main__':
    test_thumbnail_maker()
