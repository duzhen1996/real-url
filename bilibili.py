# 获取哔哩哔哩直播的真实流媒体地址，默认获取直播间提供的最高画质
# qn=150高清
# qn=250超清
# qn=400蓝光
# qn=10000原画
import requests
import os


class BiliBili:

    def __init__(self, rid, qn):
        self.rid = rid
        self.qn = qn

    def get_real_url(self):
        # 先获取直播状态和真实房间号
        r_url = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'.format(self.rid)
        with requests.Session() as s:
            res = s.get(r_url).json()
        code = res['code']
        if code == 0:
            live_status = res['data']['live_status']
            if live_status == 1:
                room_id = res['data']['room_id']

                def u(pf):
                    f_url = 'https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl'
                    params = {
                        'cid': room_id,
                        'qn': self.qn,
                        'platform': pf,
                        'https_url_req': 1,
                        'ptype': 16
                    }
                    resp = s.get(f_url, params=params).json()
                    try:
                        durl = resp['data']['durl']
                        real_url = durl[-1]['url']
                        return real_url
                    except KeyError or IndexError:
                        raise Exception('获取失败')
                
                video_link = u('web')
                os.system("echo '%s' | pbcopy" % video_link)
                print("已复制到剪切板：")
                print(video_link)            
                return {
                    'flv_url': video_link,
                    'hls_url': u('h5')
                }

            else:
                raise Exception('未开播')
        else:
            raise Exception('房间不存在')


def get_real_url(rid, qn):
    try:
        bilibili = BiliBili(rid, qn)
        return bilibili.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    qn = [10000,150,150,250,400]
    r = input('请输入bilibili直播房间号：\n')
    rate = qn[int(input('输入清晰度（1流畅；2高清；3超清；4蓝光；0原画）：\n'))]
    get_real_url(r,rate)
