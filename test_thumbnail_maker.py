"""
thumnbail maker script, may change the source
"""
from thumbnail_maker import ThumbnailMakerService

IMG_URLS = [
    'https://i.kinja-img.com/gawker-media/image/upload/s--jHAkq6mQ--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ccwlwicp2umrn1dnp2h1.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--7qH7m17g--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ofqe9ruxjn04komwar9o.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--ZelFOYrg--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/vdx7igcimjfcqhe1yfwy.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--L_vCdQkY--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/zwxmqlcov5otterd3837.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--3lZHtAvN--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/alscw3vhlcfzdkzfnz3e.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--4RWC_Q8y--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/juiqfgnxsnd8hztashdj.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--53FOkEHQ--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/rwsm1niblyxtdve1yuvq.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--8oh2GJ8---/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/d4mwn9uy4ednf1nyt44d.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--BNU4s31Q--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/r2fxeggcuapki9ze86g5.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--E9JvR6zD--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ycikkm50timeaevel40l.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--gXbd2e1V--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/jvp8ftnuptptzrkbmwwy.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--qXHAzcVS--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ant9bupe0imzmc7em6za.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--hVbrpwjH--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/k9jzpxlvcccaz4mzmwxt.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--Ie8pBtnS--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/zdux9lg2pierc8t6weay.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--mV5iGurd--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ywooldudzdkem6blteiw.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--pSC41gMP--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/buulcxrypashtjuqkisc.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--ROdOrqxj--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/muotybwrl9sm4s2jgoig.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--TqpTY9t6--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/or8j0njxkotoo0sve2jy.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--RPPFz0Qr--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/vteo9oglifm6uykzi90a.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--FgqaCeME--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ajs0pcmeh4ollbnt5gxw.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--FHzgs724--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/thok0ygjqbbucnocsb0h.jpg',
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
    'https://i.kinja-img.com/gawker-media/image/upload/s--V2d6coaQ--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/jy65mxlgcmau9xe6ahqj.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--XXMEFrPv--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/u99smdxbfdznyjn4ftso.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--D5S1EO7C--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/utejdsgttgmwblw7zera.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--UFBa0kpw--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/di1ucunfwa9gxy5lu2mh.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--vUgA6_-L--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/i1pzwzhvx4jj7mysu2bz.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--ZeHgo4MW--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/q6qmahfckjhawbtjbjkk.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--HWwzwQ1q--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/iofbudezbje6gnqddef1.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--0ISrJi5n--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/jkjhb3gv0qmieppvq0b2.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--ho5zOxOS--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/onx5yksjnr8ulmchw1nw.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--HEK5Si0z--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/s4vo17kcic5nctl9qwk6.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--sJJDHlcS--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/wsvwtlwjp62efu20dxbb.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--FACPTWC0--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/zeumriyb2xp29m2akvcx.jpg',
    'https://i.kinja-img.com/gawker-media/image/upload/s--sZs0RU_X--/c_scale,dpr_2.0,f_auto,fl_progressive,q_80,w_1600/ympzuvjshxjfoen6ax3h.jpg'
]


def test_thumbnail_maker():
    """
    to run the thumbnail maker function
    """
    tn_maker = ThumbnailMakerService()
    tn_maker.make_thumbnails(IMG_URLS)


if __name__ == '__main__':
    test_thumbnail_maker()
