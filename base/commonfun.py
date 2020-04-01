import logging
import logging.config
import requests,json
from requests import exceptions
import unittest
from base.base import session_headers
CON_LOG='../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()

class Common(unittest.TestCase):
    # status_code响应状态码
    @classmethod
    def get_exception(self,url,msgs):
        try:
            res = requests.get(url,timeout =3, headers=session_headers)
            res.raise_for_status()  # 状态不是200会抛异常
        except exceptions.Timeout as e:  # 超时异常
            logging.info(e)
        # self.assertEqual(200, res.status_code)  # 超时不能使用该断言，否则会报错，因为没有得到res

        except exceptions.HTTPError as e:  # 状态500 进入该异常
            logging.info(e)
            self.assertEqual(200, res.status_code)  # 这个断言不能放在上面，如果放在前面断言(try里面)，考虑到返回状态200，也有可能是fail的用例

        else:
            msg = res.json()
            logging.info(msg['msg'])
            print(res.status_code)

            self.assertEqual(200, res.status_code)
            self.assertIn(msgs, msg['msg'])
            logging.info(msgs+'请求成功')