# -*- coding: utf-8 -*-
# @Time    : 2020-06-29 16:43
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : throttle.py            自定义访问频率
# @Software: PyCharm

import time
from rest_framework.throttling import BaseThrottle

visit_record = {}


class Throttles(BaseThrottle):  # 继承了这个类就不用自己定义wait了
    def allow_request(self, request, abc):  # 源码中规定必须有这个方法

        # 得到用户进来的IP地址 ,我们可也以用BaseThrottle这个类中的get_ident(request)来获得ip地址
        visit_ip = request.META.get("REMOTE_ADDR")
        ctime = time.time()
        if visit_ip not in visit_record:
            visit_record[visit_ip] = [ctime]
            return True
        if len(visit_record[visit_ip]) < 20:  # 修改这里就可以修改访问次数
            visit_record[visit_ip].insert(0, ctime)
            return True
        if (ctime - visit_record[visit_ip][-1]) > 60:
            visit_record[visit_ip].insert(0, ctime)
            visit_record[visit_ip].pop()

            return True
        return False
