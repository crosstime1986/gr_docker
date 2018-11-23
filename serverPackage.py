#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, os, requests, shutil
from collections import namedtuple

GameArgs = namedtuple('GameArgs', ['folder_path', 'agent_id', 'site_id', 'game_id', 'version'])


class App:
    """
    App 类 只支并发打包
    """

    def __init__(self, game_args=None):
        """
        构造方法
        :param GameArgs game_args: 
        """
        self.channel_file = '{s.folder_path}/game_{s.site_id}/assets/grConfig.ini'
        self.channel_history_file = '{s.folder_path}/channel_history.txt'
        self.sign_pem_path = '{s.folder_path}/key.x509.pem'
        self.sign_pk8_path = '{s.folder_path}/key.pk8'
        self.new_temp_apk = '{s.folder_path}/game_{s.site_id}_temp.apk'
        self.new_apk = '{s.folder_path}/{game_name}_{s.site_id}.apk'
        self.old_apk = '{s.folder_path}/game_{s.site_id}/dist/game.apk'

        # 反编的路径
        if game_args.version != '' or game_args.version == None:
            self.demo_decompile_path = '{s.folder_path}/game/'
        else:
            self.demo_decompile_path = '{s.folder_path}/game-%s/' % game_args.version
        self.target_decompile_path = '{s.folder_path}/game_{s.site_id}'

        # 回编命令
        self.build_command = '/usr/local/bin/apktool b ' + self.target_decompile_path

        # 重签命令
        self.sign_command = 'java -jar /data/www/c.gaore.com/signapk.jar ' + \
                            self.sign_pem_path + ' ' + self.sign_pk8_path + \
                            " " + self.old_apk + " " + self.new_temp_apk

        game_name = os.path.basename(game_args.folder_path)
        for i in self.__dict__:
            setattr(self, i, self.__dict__[i].format(s=game_args, game_name=game_name))
        self.info = game_args

    def sendStatus(self, success=False):
        """
        远程通知 c.gaore.com 打包成功，刷新CDN
        :param success: 
        :return: 
        """
        try:
            url = "http://c.gaore.com/updatepack.php"
            params = self.info._asdict()
            params['state'] = 1 if success else 0
            r = requests.get(url, params, timeout=5)
            if r.status_code == 200:
                self.message('发送成功 ' + r.url)
        except Exception as e:
            print(e)

    def writeInfo(self):
        """
        写入渠道号和广告位号
        :return: 
        """
        result = False
        with open(self.channel_file, 'w') as fd:
            fd.write('%s-%s' % (self.info.agent_id, self.info.site_id))
            fd.close()

        if not result:
            return result

        exists = os.path.exists(self.channel_history_file)
        with open(self.channel_history_file, 'a+') as fd:
            fd.write(('\r\n' if exists else '') + self.info.agent_id + ',' + self.info.site_id)
            fd.close()
            self.message('write history finish')
            result = True

        return result

    def renameApkFile(self):
        """
        临时包改名
        :return: 
        """
        if os.path.exists(self.new_temp_apk):
            if os.path.exists(self.new_apk):
                os.remove(self.new_apk)
            os.rename(self.new_temp_apk, self.new_apk)
            self.message('renameFile finish:' + self.new_apk)
        else:
            print('file not exists')


    def message(self, msg=''):
        """
        写信息
        :param msg: 
        :return: 
        """
        print('==%s==' % msg)

    def copytree(self):
        """
        复制反编目录，如果目标目录存在那，等于在打包中，相等于锁的机制
        :return: 
        """
        if not os.path.exists(self.target_decompile_path):
            if os.path.exists(self.demo_decompile_path):
                shutil.copytree(self.demo_decompile_path, self.target_decompile_path)
            else:
                print('demo directory is noe exists!!')
                exit(-1)
        else:
            print('compile directory is exists!!')
            exit(-1)

    def removetree(self):
        if os.path.exists(self.target_decompile_path):
            shutil.rmtree(self.target_decompile_path, True)

    def run(self):
        """
        开始打包
        :return: 
        """
        self.copytree()
        self.writeInfo()

        self.message('package start ' + self.build_command)
        os.system(self.build_command)
        self.message('package finish')

        self.message('signed start ')
        print(self.sign_command)
        os.system(self.sign_command)
        self.message('signed finish ')

        self.renameApkFile()
        self.removetree()
        self.sendStatus(True)
        self.message('操作完成')


if __name__ == '__main__':
    args = GameArgs._make(sys.argv[1:])
    app = App(args)
    app.run()
