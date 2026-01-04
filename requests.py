# ////////////////////////////////////////////////////////////////////////////////
#
# AUTHOR            : DANG DINH TOAN
# NICKNAME          : PYTOURNES
# VERSION           : 1.0.0
# DATE              : October 2024
# PROJECT MADE WITH : Qt Designer and PyQt5
# DESCRIPTION       : This project demonstrates the use of PyQt5 with Qt Designer
# 
# CONTACT INFO
# ------------------------------------------------------------------------------
# Facebook  : https://www.facebook.com/trn.devpy
# Telegram  : https://t.me/trnmmo
# YouTube   : https://www.youtube.com/@trn.devpython
# Zalo      : https://zalo.me/0865894536
#
# ////////////////////////////////////////////////////////////////////////////////

from core import *
from utils.tiktok import *

THREAD_LOCK = threading.Lock()
class PhoneAutomation(QtCore.QThread):
    startMining          = QtCore.pyqtSignal(int, str, int)
    saveDataTable        = QtCore.pyqtSignal()
    editStatus           = QtCore.pyqtSignal(str, str, float)
    editCellByColumnName = QtCore.pyqtSignal(int, str, str, object, object)
    stopMining           = QtCore.pyqtSignal(int)
   
    def __init__(self, parent, index, totalThread):
        super().__init__()
        self.parent, self.index, self.totalThread = parent, index, totalThread
        self.port = 9222 + self.index
        self.pos_window = False; self.handle_chrome = False
        self.__pause = []
        self.__typePerError = ''
        self.__getJob = 0; self.__dalam = []; self.__hide = 0; self.title = ''; self.id_storage_ttc2 = ''; self.countdownTTC1 = 0; self.countdownTTC2 = 0; self.login_time = 0; self.countdownTDS = 0;self.cache_count=''
        self.__block = 0; self.__click = False; self._upload = 0;self._addtiktop = 0; self.mail = ''; self.datniktiktop = {'status': 'success', 'uid': None, 'sec_uid': None}
        self.id_storage_ttc = ''; self.fail_follow = 0
        self.dict_xuthem = {
            'ttc': 0,
            'tlc': 0,
            'tdsv1': 0,
            'tdsv2': 0,
            'tiktop': 0,
            'min': 0,
            }
        self.dict_add = {
            'ttc': False,
            'ttc2': False,
            'tlc': False,
            'tdsv1': False,
            'tdsv2': False,
            'tiktop': False,
            'min': False,
            }
        self.url_tiktok = 'https://www.tiktok.com/'
        self.status = 'Cảm ơn quý khách đã sử dụng phần mềm.'
        
    def __updateValue(self):
        acc = []
        for i in range(self.parent.tableWidget.columnCount()):
            try:
                acc += [self.parent.tableWidget.item(self.index, i).text()]
            except: acc += ['']
        self.uid, self.pwd, self.twofa, self.cookieChrome, self.mail, self.passmail , self.total, self.job_info, self.tyle, self.proxy, self.status = [x.strip() for x in acc[:11]]

        parts = self.proxy.split(':')
        if len(parts) >= 4:
            iport = ":".join(parts[:2])
            userpass = ":".join(parts[2:])
            self.proxyRequests = {
                'http': f'http://{userpass}@{iport}',
                'https': f'http://{userpass}@{iport}'
            }
        elif len(parts) >= 2:
            proxy_url = f'http://{self.proxy}'
            self.proxyRequests = {
                "http": proxy_url,
                "https": proxy_url
            }
        else:
            self.proxyRequests = ''  # Sử dụng None thay vì chuỗi rỗng
        self.total = int(self.total) if str(self.total).isdigit() else 0

        # if isinstance(self.total, (int, float))  == False: self.total = 0

    def openBrowser(self):
        for _ in range(3):
            try:
                self.__updateValue()

                self.editCellByColumnName.emit(
                    self.index, 'Status',
                    "🔄 Đang mở trình duyệt...",
                    self.parent.tableWidget, COLORS.GREEN
                )

                # ===============================
                # 1. Khởi tạo thông tin
                # ===============================
                
                self.profile_path = os.path.join(PATHBROWSER, 'Profile', f'luong_{self.index + 1}')

                os.makedirs(self.profile_path, exist_ok=True)

                # ===============================
                # 2. MỞ CHROME THẬT (KHÔNG SELENIUM)
                # ===============================
                extension_dir = PATHEXTS
                if os.path.exists(extension_dir):
                    extensions = [os.path.join(extension_dir, ext) for ext in os.listdir(extension_dir) if os.path.isdir(os.path.join(extension_dir, ext))]
                chrome_cmd = [
                    BINARY_LOCATION,
                    f"--remote-debugging-port={self.port}",
                    f"--user-data-dir={self.profile_path}",
                    f"--load-extension={','.join(extensions)}",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--disable-notifications",
                    "--disable-dev-shm-usage",
                    "--start-maximized",
                    f"--lang=vi-VN",
                    "--window-size=700,900",
                    # '--force-device-scale-factor=0.2'
                ]

                if self.proxy:
                    chrome_cmd.append(f"--proxy-server={self.proxy}")

                self.chrome_process = subprocess.Popen(chrome_cmd)
                time.sleep(3)

                # ===============================
                # 3. ATTACH SELENIUM
                # ===============================
                options = Options()
                options.add_experimental_option(
                    "debuggerAddress", f"127.0.0.1:{self.port}"
                )
                
               
                service = Service(PATHDRIVER+f'\\{BROWSER_TYPE}\\chromedriver.exe')
                self.driver = webdriver.Chrome(service=service, options=options)

              
                self.actionChains = ActionChains(self.driver)
             
                # try:
                #     self.handle_chrome = get_handle_from_pid(get_chrome_pid_by_window_title(BROWSER_TYPE))
                #     print(self.handle_chrome)
                #     if self.handle_chrome: embedApi.embed_tab(self.handle_chrome, new=self.index)

                # except Exception as e:
                #     traceback.print_exc()
                self.saved_handles = self.driver.window_handles.copy()
                

                self.editCellByColumnName.emit(
                    self.index, 'Status',
                    "✅ Trình duyệt đã khởi động thành công!",
                    self.parent.tableWidget, COLORS.GREEN
                )
                
                return True

            except Exception as e:
                try:
                    self.close_browser()
                except:
                    pass

                self.editCellByColumnName.emit(
                    self.index, 'Status',
                    f"❌ Lỗi mở trình duyệt: {e}",
                    self.parent.tableWidget, COLORS.RED
                )

                time.sleep(3)

        return False

    def startTTC1(self):
        global CONCURRENT_THREADS
        self.__typeStart = 'TTC1'
        try:
            self.cache_count = len(self.id_storage_ttc.split(','))
            if self.cache_count >= 50: self.id_storage_ttc = ''
            # try:
            #     seconds = int(round(time.time() - self.__startTTC1, 1))
            #     self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Countdown: còn {self.countdownTTC1 - seconds} giây', self.parent.tableWidget, COLORS.RED)
            #     logging.debug(f'Thời gian đếm ngược TTC: còn {self.countdownTTC1 - seconds} giây')
            #     if seconds > self.countdownTTC1:
            #         logging.info('Đếm ngược đã kết thúc. Chờ thêm 3 giây trước khi tiếp tục...')
            #         self.countdownTTC1 = 0
            #         time.sleep(3)
            #     else:
            #         logging.info(f'Vẫn còn thời gian: {self.countdownTTC1 - seconds} giây trước khi hết hạn.')
            #         return True
            # except:pass
            
            def nhanTienTTC1():
                getXu = self.__apituongtaccheo.getXu(self.__typeJob, self.id_storage_ttc.rstrip(','))
                print(f"{getXu} - {self.id_storage_ttc.rstrip(',')}")
             
                if getXu['status'] == 'success':
                    self.editStatus.emit('xuthem', 'tuongtaccheo', int(getXu['data']['xu_them']))
                    # if int(getXu['data']['xu_them']) <= 0:self.__block += 1
                    # else: self.__block = 0

                    self.dict_xuthem['ttc'] += int(getXu['data']['xu_them'])
                    
                    xu = int(getXu['data']['xu_them'])
                    jobs = self.id_storage_ttc.rstrip(",").split(",")
                    done = xu // (500 if 'love' in self.__typeJob else 1000)

                    self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                    self.editCellByColumnName.emit(self.index, 'Rate', f'{done}/{len(jobs)} C1', self.parent.tableWidget, COLORS.GREEN)
                    self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {xu} xu", self.parent.tableWidget, COLORS.GREEN)

                    self.id_storage_ttc = ''
                    self.__typeStart = 'TTC1'
                    # self.editCellByColumnName.emit(self.index, 'Status', f"Nghỉ 30s rồi làm tiếp", self.parent.tableWidget, COLORS.GREEN)
                    # time.sleep(30)
                    return True
                if getXu['status'] == 'error':
                    if 'Vui lòng công khai danh sách video đã thích trên tài khoản tiktok rồi quay lại nhận' in getXu['mess']:
                        # self.public()
                        time.sleep(3)
                        # getXu = self.__apituongtaccheo.getXu('love', self.id_storage_ttc.rstrip(','))
                        # return
                    elif 'Nhiệm vụ đã hết hạn, hãy làm các nhiệm vụ mới' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Rate', f'0/{len(self.id_storage_ttc.rstrip(",").split(","))} C1', self.parent.tableWidget, COLORS.GREEN)
                        self.id_storage_ttc = ''

                    elif 'Bạn chưa like video nào, hãy like video trước khi nhận xu' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Rate', f'0/{len(self.id_storage_ttc.rstrip(",").split(","))} C1', self.parent.tableWidget, COLORS.GREEN)
                        self.id_storage_ttc = ''
                    elif 'Bạn chưa theo dõi nick nào, hãy theo dõi trước khi nhận xu' in  getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {self.status}', self.parent.tableWidget, COLORS.RED)
                        
                        time.sleep(5)
                        self.editCellByColumnName.emit(self.index, 'Rate', f'Nhả', self.parent.tableWidget, COLORS.GREEN)
                        self.__typeStart = 'TTC1'
                        self.id_storage_ttc = ''
                        
                        # self.dict_add['ttc'] = False
                        return False
                    
                    elif 'Nick bị die rồi, hãy kiểm tra lại nick tiktok đi!' in getXu['mess']:
                        self.clearAcc()
                        time.sleep(5)
                        self.editCellByColumnName.emit(self.index, 'Rate', f'Die', self.parent.tableWidget, COLORS.GREEN)
                        self.initJobBrowser()
                        self.__typeStart = 'TTC1'
                        self.id_storage_ttc = ''
                        return False
                    
                    elif 'Bạn cần thêm nick vào hệ thống trước khi đặt' in getXu['mess']:
                        datnick = self.__apituongtaccheo.datNick(self.uid)
                        if datnick['status'] == 'error':
                            self.status = datnick['mess']
                            self.editCellByColumnName.emit(self.index, 'Status', str(self.status), self.parent.tableWidget, COLORS.RED)
                            time.sleep(0.5)
                            self.stopMining.emit(self.index)
                            time.sleep(1)
                            return True
                        
                    elif 'Bạn đã theo dõi' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Rate', f'FL-R', self.parent.tableWidget, COLORS.GREEN)
                        self.id_storage_ttc = ''
                        return True
                    
                    elif 'Vui lòng làm trên 8 nhiệm vụ mới nhận xu' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Status', str(getXu['mess']), self.parent.tableWidget, COLORS.RED);time.sleep(0.5)
                        return True
                    # elif 'Có lỗi xảy ra khi lấy nhận xu' not in getXu['mess']:
                    #     self.id_storage_ttc = ''
                if getXu['status'] == 'error2':
                    getXu = self.__apituongtaccheo.getXu('love', self.id_storage_ttc.rstrip(','))
                    logging.debug(f"{getXu} - {self.id_storage_ttc.rstrip(',')}")
                    if getXu['status'] == 'success':
                        self.editStatus.emit('xuthem', 'tuongtaccheo', int(getXu['data']['xu_them']))
                        # if int(getXu['data']['xu_them']) <= 0:self.__block += 1
                        # else: self.__block = 0

                        self.dict_xuthem['ttc'] += int(getXu['data']['xu_them'])
                        
                        xu = int(getXu['data']['xu_them'])
                        jobs = self.id_storage_ttc.rstrip(",").split(",")
                        done = xu // (500 if 'love' in self.__typeJob else 1400)

                        self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                        self.editCellByColumnName.emit(self.index, 'Rate', f'{done}/{len(jobs)} C1', self.parent.tableWidget, COLORS.GREEN)
                        self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {xu} xu", self.parent.tableWidget, COLORS.GREEN)

                        self.id_storage_ttc = ''
                self.editCellByColumnName.emit(self.index, 'Status', str(getXu['mess']), self.parent.tableWidget, COLORS.GREEN);time.sleep(3)
                
                # formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # with open('logs.txt', 'a+', encoding='utf-8') as f:
                #     f.write(f'{formatted_datetime}: UID: {self.uid.upper()} | JOB_ID: {self.id_storage_ttc} | {getXu["mess"]} | {self.__typePerError} | TTC1\n')
                
            try:
                self.__typeStart = 'TTC1'
                self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
                self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
               
              
                for t in range(10):
                    jobs = self.__apituongtaccheo.getJob(self.__typeJob)
                    logging.debug(jobs)
                    try:
                        if 'idpost' in str(jobs[0]):
                            break
                    except:pass
                    time.sleep(0.4)
               
                try:
                    if 'idpost' in str(jobs[0]):
                        pass
                except:
                    self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] 🔄 Không tìm thấy nhiệm vụ nào cả chờ 5-10s!", self.parent.tableWidget, COLORS.GREEN)
                    time.sleep(random.randint(5,10))
                    return

                logging.debug(jobs)
                self.total_jobs = len(jobs)
                for index, job in enumerate(jobs, start=1):
                    self.remaining_jobs = self.total_jobs - index
                    self.cache_count = len([x for x in self.id_storage_ttc.split(',') if x])
                    self.editCellByColumnName.emit(self.index, 'Status', f'Cache: {self.cache_count}-[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                    self.__job_id, self.__link ,self.idaccount= job['idpost'], job['link'], job['uid']
                                     
                    self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                    self.editStatus.emit('jobs', '', 1)
                    for _ in range(3):
                        try:
                            user_info       = get_user_info(str(self.__link), self.proxy)
                            if user_info == None:
                                self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] Không kiểm tra được thông tin @{self.__link}!!!" ,self.parent.tableWidget, COLORS.OLIVE);time.sleep(1)
                            else:
                                user_info   = get_user_by_cookie(str(self.__link), session=self.ss)

                            secUid          = user_info['secUid']
                            user_id         = user_info['user_id']
                            follow_info     = follow_user(user_id=user_id, sec_uid=secUid, cookie=self.cookieChrome, session=self.ss)
                            if follow_info:
                                self.id_storage_ttc += self.__job_id + ','
                                self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] Theo dõi thành công người dùng @{self.__link}" ,self.parent.tableWidget, COLORS.GREEN);time.sleep(1)
                                break
                        except:pass
                        time.sleep(random.randint(5,10))
                    else:
                        self.fail_follow += 1
                        self.editCellByColumnName.emit(self.index, 'Passmail', str(self.fail_follow) ,self.parent.tableWidget, COLORS.RED);time.sleep(1)
                        self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] Theo dõi người dùng @{self.__link} thất bại" ,self.parent.tableWidget, COLORS.RED);time.sleep(1)

                        
                    self.total += 1
                    
                    if len(self.id_storage_ttc.split(',')) > self.settings['DelaySettings']['Cache']:
                        self.configureDelay('GetCoin')
                        nhanTienTTC1()
                        return True

                    self.configureDelay(type='NextJob')
                    if self.dict_add['ttc'] == False:
                        return
                    
                if self.dict_add['ttc'] == False:
                    return
                
                if len(self.id_storage_ttc.split(',')) > self.settings['DelaySettings']['Cache']:
                    self.configureDelay('GetCoin')
                    nhanTienTTC1()
                    return True
                
     
            except: 
                    logging.error('Có lỗi xảy ra khi chạy TTC', exc_info=True)
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Có lỗi xảy ra bắt đầu lại sau 15s để tránh block Token...', self.parent.tableWidget, COLORS.RED)
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(3)    
 
    def startTTC2(self):
        self.__typeStart = 'TTC2'
        try:
            # try:
            #     seconds = int(round(time.time() - self.__startTTC2, 1))
            #     self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Countdown: còn {self.countdownTTC2 - seconds} giây', self.parent.tableWidget, COLORS.RED)
            #     logging.debug(f'Thời gian đếm ngược TTC: còn {self.countdownTTC2 - seconds} giây')
            #     if seconds > self.countdownTTC2:
            #         logging.info('Đếm ngược đã kết thúc. Chờ thêm 3 giây trước khi tiếp tục...')
            #         self.countdownTTC2 = 0
            #         time.sleep(3)
            #     else:
            #         logging.info(f'Vẫn còn thời gian: {self.countdownTTC2 - seconds} giây trước khi hết hạn.')
            #         return True
            # except:pass
            
            def nhanTien():
                getXu = self.__apituongtaccheo.getXu('love2', self.id_storage_ttc2.rstrip(','))
                logging.debug(f"{getXu} - {self.id_storage_ttc2.rstrip(',')}")
                # formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # with open('logs.txt', 'a+', encoding='utf-8') as f:
                #     f.write(f'{formatted_datetime}: UID: {self.uid.upper()} | JOB_ID: {self.__split_id[0]} | {getXu["mess"]} | {self.__typePerError} | TTC2\n')
                if getXu['status'] == 'success':
                    self.editStatus.emit('xuthem', 'tuongtaccheo', int(getXu['data']['xu_them']))
                    # if int(getXu['data']['xu_them']) <= 0:self.__block += 1
                    # else: self.__block = 0

                    self.dict_xuthem['ttc'] += int(getXu['data']['xu_them'])
                    
                    xu = int(getXu['data']['xu_them'])
                    jobs = self.id_storage_ttc2.rstrip(",").split(",")
                    done = xu // (700 if 'love' in self.__typeJob else 1400)

                    self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                    self.editCellByColumnName.emit(self.index, 'Rate', f'{done}/{len(jobs)} C2', self.parent.tableWidget, COLORS.GREEN)
                    self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {xu} xu", self.parent.tableWidget, COLORS.GREEN)

                    self.id_storage_ttc2 = ''

                if getXu['status'] == 'error':
                    if 'Vui lòng công khai danh sách video đã thích trên tài khoản tiktok rồi quay lại nhận' in getXu['mess']:
                        self.public()
                        return

                    elif 'Nhiệm vụ đã hết hạn, hãy làm các nhiệm vụ mới' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Rate', f'0/{len(self.id_storage_ttc2.rstrip(",").split(","))} C2', self.parent.tableWidget, COLORS.GREEN)
                        self.id_storage_ttc2 = ''

                    elif 'Bạn chưa like video nào, hãy like video trước khi nhận xu' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Rate', f'0/{len(self.id_storage_ttc2.rstrip(",").split(","))} C2', self.parent.tableWidget, COLORS.GREEN)
                        self.id_storage_ttc2 = ''
                       
                    elif 'Bạn cần thêm nick vào hệ thống trước khi đặt' in getXu['mess']:
                        datnick = self.__apituongtaccheo.datNick(self.uid)
                        if datnick['status'] == 'error':
                            self.status = datnick['mess']
                            self.editCellByColumnName.emit(self.index, 'Status', str(self.status), self.parent.tableWidget, COLORS.RED)
                            time.sleep(0.5)
                            self.stopMining.emit(self.index)
                            time.sleep(1)
                            return
                    elif 'Vui lòng làm trên 8 nhiệm vụ mới nhận xu' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Status', str(getXu['mess']), self.parent.tableWidget, COLORS.RED);time.sleep(0.5)
                        return
                    # elif 'Có lỗi xảy ra khi lấy nhận xu' not in getXu['mess']:
                    #     self.id_storage_ttc2 = ''
                if getXu['status'] == 'error2':   
                    getXu = self.__apituongtaccheo.getXu('love2', self.id_storage_ttc2.rstrip(','))
                    logging.debug(f"{getXu} - {self.id_storage_ttc2.rstrip(',')}")
                    
                self.editCellByColumnName.emit(self.index, 'Status', str(getXu['mess']), self.parent.tableWidget, COLORS.GREEN);time.sleep(3)
        
            try:
                self.__typeStart = 'TTC2'
                # self.__startTTC2 = time.time()
                self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
                self.__typeJob = 'love2'
                self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
                for i in range(4):
                    jobs = self.__apituongtaccheo.getJob('love2')
                    logging.debug(jobs)
                # if jobs == 7:return
                    if len(jobs)>1: break
                if jobs == [] or jobs == None or len(jobs) == 0: 
                    return
                try:
                    if 'idpost' in str(jobs[0]):
                        pass
                except:return
                # if 'spam sẽ văng tài khoản, đi làm nhiệm vụ khác quay lại sau!' in str(jobs):
                #     self.editCellByColumnName.emit(self.index, 'Status', str(jobs['error']), self.parent.tableWidget, COLORS.GREEN);
                #     if 'countdown' in str(jobs):
                #         self.countdown = int(jobs['countdown'])
                #     return
                
                self.total_jobs = len(jobs)
                for index, job in enumerate(jobs, start=1):
                    self.remaining_jobs = self.total_jobs - index
                    cache_count = len([x for x in self.id_storage_ttc2.split(',') if x])
                    self.editCellByColumnName.emit(self.index, 'Status', f'Cache: {cache_count}-[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                    self.__job_id, self.__link = job['idpost'], job['link']
                    numbers = re.findall(r'\d+(?:\.\d+)?', self.__link)

                    # Lọc ra số có nhiều hơn 5 chữ số
                    self.__split_id = [num for num in numbers if len(num.replace('.', '')) > 5]

                    if '@' not in self.__link: 
                        self.__link = self.url_tiktok+'@'+self.__link
                    else:
                        self.__link = 'https://www.tiktok.com/@' + self.__link + '/' + self.__link + '/' + self.__split_id[0]
                        # pass
                        # self.__link = self.__link+ '/' +self.__link
               
                    

                    # if self.__link in self.__dalam:
                    #     self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ⚠️ Nhiệm vụ ID {self.__job_id} đã hoàn thành trước đó! Bỏ qua nhiệm vụ này..." ,self.parent.tableWidget, COLORS.RED);time.sleep(1);continue
            

                    self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                    self.editStatus.emit('jobs', '', 1)
                    if self.performAction():
                        self.total += 1
                        self.id_storage_ttc2 += self.__job_id + ','
                        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                        
                    delay_time = random.randint(3,5)
                    self.configureDelay(type='NextJob',delay=delay_time )
                if len(self.id_storage_ttc2.split(',')) > self.settings['DelaySettings']['Cache']:
                    self.configureDelay('GetCoin')
                    nhanTien()
                
                # try:
                #     seconds = int(round(time.time() - self.__startTTC2, 1))
                #     self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ✅ Hoàn thành toàn bộ {self.total_jobs} nhiệm vụ {self.__typeJob.upper()} trong {seconds} giây! 🚀", self.parent.tableWidget, COLORS.GREEN)
                #     if self.countdownTTC2 >= seconds:
                #         self.countdownTTC2 = self.countdownTTC2 - seconds
                #         # self.configureDelay('countdown', int(self.countdown))
                # except:traceback.print_exc()
            except: 
                    logging.error('Có lỗi xảy ra khi chạy TTC', exc_info=True)
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Có lỗi xảy ra bắt đầu lại sau 15s để tránh block Token...', self.parent.tableWidget, COLORS.RED)
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(3)    

    def startTDSV2(self):
        self.__typeStart = "V2"
        try:
            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
            jobs = self.__apitraodoisubV2.getJob(self.__typeJob)
            logging.debug(jobs)
            if 'error' in str(jobs):
                self.editCellByColumnName.emit(self.index, 'Status', str(jobs['error']), self.parent.tableWidget, COLORS.GREEN)
                if jobs['error'] == 'Có lẽ tài khoản của bạn đã bị chặn tương tác, bạn đã làm thất bại quá nhiều lần!':
                    self.__pause.append('tdsv2')
                    return 
            if 'data' not in str(jobs) or jobs['data'] == [] or jobs['data'] == None: 
                return
            
            self.total_jobs = len(jobs['data'])
            for index, job in enumerate(jobs['data'], start=1):
                self.remaining_jobs = self.total_jobs - index
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                self.__job_id, self.__link, self.__count = job['id'], job['link'], job['count']
                if self.__count <= 10:
                    # guiDuyet = self.__apitraodoisubV2.guiDuyet(self.__job_id);time.sleep(5)
                    continue
                self.__link = self.__link + '/' + self.__link

                self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                self.editStatus.emit('jobs', '', 1)
                if self.performAction():
                    self.total += 1
                    guiDuyet = self.__apitraodoisubV2.guiDuyet(self.__job_id)
                    cache_message = guiDuyet.get('cache', 'Không có thông tin cache')
                    self.editCellByColumnName.emit(
                        self.index, 
                        'Status', 
                        f'[ {self.__typeStart} ] Làm nhiệm vụ thành công! Cache: {cache_message}', 
                        self.parent.tableWidget, 
                        COLORS.GREEN
                    )
                    logging.debug(guiDuyet)
                    if guiDuyet != None:
                        if  guiDuyet['cache'] >= self.settings['DelaySettings']['Cache']:
                            self.configureDelay('GetCoin')
                            getXu = self.__apitraodoisubV2.getXu()
                            if getXu['success'] == 200:
                                self.editStatus.emit('xuthem', 'traodoisubv2', int(getXu['data']['xu_them']))
                                self.dict_xuthem['tdsv2'] += getXu['data']['xu_them']
                                self.tyle = int(getXu['data']['xu_them'] / (self.settings['DelaySettings']['Cache'] * (300 if 'love' in self.__typeJob else 1400)) * 100)
                                self.editCellByColumnName.emit(self.index, 'Rate', f'{self.tyle}% V2', self.parent.tableWidget, COLORS.GREEN)
                                self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                                self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {getXu['data']['xu_them']} xu", self.parent.tableWidget, COLORS.GREEN)
                            
                
                self.configureDelay('NextJob')
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(3)
    
    def startTDSV1(self):
        if self.__apitraodoisubV1 == None:
            return
        self.__typeStart = 'V1'
        try:
            try:
                seconds = int(round(time.time() - self.__startTDS, 1))
                if seconds > self.countdownTDS:
                    self.countdownTDS = 0
                else:
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Countdown: còn {self.countdownTDS - seconds} giây', self.parent.tableWidget, COLORS.RED)
                    return True
            except Exception as e:
                self.countdownTDS = 0
                logging.error(traceback.print_exc())
            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
            jobs = self.__apitraodoisubV1.getJob(self.__typeJob)
            self.__startTDS = time.time()
            logging.debug(jobs)
            if 'error' in str(jobs):
                # {'error': 'Vui lòng cấu hình nick rồi quay lại sau nhé!'}
                if 'Vui lòng cấu hình nick rồi quay lại sau nhé!' in str(jobs):
                    self.editCellByColumnName.emit(self.index, 'Status', str(jobs['error']), self.parent.tableWidget, COLORS.GREEN)
                    self.dict_add['tdsv1'] = False
                    return
                
                if 'Vui lòng ấn NHẬN TẤT CẢ rồi sau đó tiếp tục làm nhiệm vụ để tránh lỗi!' in str(jobs):
                    getXu = self.__apitraodoisubV1.getXu(self.__typeJob)
                    logging.debug(getXu)
                    if getXu['success'] == 200:
                        self.editStatus.emit('xuthem', 'traodoisubv1', int(getXu['data']['xu_them']))
                        self.dict_xuthem['tdsv1'] += getXu['data']['xu_them']
                        self.tyle = int(getXu['data']['xu_them'] / (self.settings['DelaySettings']['Cache'] * (500 if 'love' in self.__typeJob else 1400)) * 100)
                        self.editCellByColumnName.emit(self.index, 'Rate', f'{self.tyle}% V1', self.parent.tableWidget, COLORS.GREEN)
                        self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                        self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {getXu['data']['xu_them']} xu", self.parent.tableWidget, COLORS.GREEN)
                    return 
                self.editCellByColumnName.emit(self.index, 'Status', str(jobs['error']), self.parent.tableWidget, COLORS.GREEN);
                if 'countdown' in str(jobs):
                    self.countdownTDS = int(jobs['countdown'])
                    return 

            elif 'data' not in str(jobs) or jobs['data'] == [] or jobs['data'] == None: return
    
            self.total_jobs = len(jobs['data'])
            for index, job in enumerate(jobs['data'], start=1):
                self.remaining_jobs = self.total_jobs - index
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                self.__job_id, self.__link, self.userjob = job['id'], job['link'] ,job['uniqueID']
                self.joblam = self.userjob.strip()
                self.__link = f'https://www.tiktok.com/search?q={self.joblam}' 
                # self.__link =   f'https://www.tiktok.com/search/user?q={self.userjob}'
                self.total += 1
                self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                self.editStatus.emit('jobs', '', 1)
                result = self.performAction()
                if result is True or result is False:
                    guiDuyet = self.__apitraodoisubV1.guiDuyet(self.__typeJob ,self.__job_id)
                    cache_message = guiDuyet.get('cache', 'Không có thông tin cache')
                    self.editCellByColumnName.emit(
                        self.index, 
                        'Status', 
                        f'[ {self.__typeStart} ] Làm nhiệm vụ thành công! Cache: {cache_message}', 
                        self.parent.tableWidget, 
                        COLORS.GREEN
                    )
                    logging.debug(guiDuyet)
                    if guiDuyet != None:
                        if guiDuyet['cache'] >= 8:
                            self.configureDelay('GetCoin')
                            getXu = self.__apitraodoisubV1.getXu(self.__typeJob)
                            if getXu['success'] == 200:
                                self.editStatus.emit('xuthem', 'traodoisubv1', int(getXu['data']['xu_them']))
                                self.dict_xuthem['tdsv1'] += getXu['data']['xu_them']
                                self.tyle = int(getXu['data']['xu_them'] / (8 * (500 if 'love' in self.__typeJob else 1000)) * 100)
                                self.editCellByColumnName.emit(self.index, 'Rate', f'{self.tyle}% V1', self.parent.tableWidget, COLORS.GREEN)
                                self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                                self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {getXu['data']['xu_them']} xu", self.parent.tableWidget, COLORS.GREEN)
                            
                delay_time = random.randint(5,9)
                self.configureDelay(type='NextJob',delay=delay_time )
            try:
                seconds = int(round(time.time() - self.__startTDS, 1))
                self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ✅ Hoàn thành toàn bộ {self.total_jobs} nhiệm vụ {self.__typeJob.upper()} trong {seconds} giây! 🚀", self.parent.tableWidget, COLORS.GREEN)
                if self.countdownTDS >= seconds:
                    self.countdownTDS = self.countdownTDS - seconds
                    # self.configureDelay('countdown', int(self.countdownTDS))
            except:traceback.print_exc()
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
    
    def startTLC(self):
        self.__typeStart = 'TLC'
        try:
            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
            jobs = self.__apitanglikecheo.getJob(self.__typeJob)
            logging.debug(jobs)

            if 'Chặn lấy job like 24h' in str(jobs) or self.__block >= 5:
                self.editCellByColumnName.emit(self.index, 'UID', '',self.parent.tableWidget, COLORS.RED)
                self.editCellByColumnName.emit(self.index, 'Password', '',self.parent.tableWidget, COLORS.RED)
                self.editCellByColumnName.emit(self.index, '2FA', '',self.parent.tableWidget, COLORS.RED)
                
                self.status = jobs['message']
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚫 Job Like đã bị khóa 24h! Lý do: BLOCK {self.__block} | {self.status}!!!', self.parent.tableWidget, COLORS.RED)
                self.__updateValue()
                time.sleep(3)
                self.clearAcc()
                time.sleep(5)
                self.initJobBrowser()
                
                return
        
            elif 'Gửi request nhận xu 5 đã làm trước khi thực hiện lấy thêm job' in str(jobs['message']):
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Gửi request nhận xu 5 đã làm trước khi thực hiện lấy thêm job ^^!',self.parent.tableWidget, COLORS.GREEN);time.sleep(3)
                getXu = self.__apitanglikecheo.guiDuyet('',self.__typeJob, 0)
                logging.debug(getXu)
                self.tyle = 0
                if 'coin_today' in str(getXu):
                    for i in getXu['data']:
                        self.editStatus.emit('xuthem', 'tanglikecheo', int(i['coin']))
                        self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {i['coin']} xu", self.parent.tableWidget, COLORS.GREEN)
                        self.tyle += 20
                        self.dict_xuthem['tlc'] += i['coin']
                    self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                    self.editCellByColumnName.emit(self.index, 'Rate', f'{self.tyle}% TLC', self.parent.tableWidget, COLORS.GREEN)
                return
            
            elif 'Trường id là id tiktok phải là id' in str(jobs):
                self.status = jobs['message']
                self.editCellByColumnName.emit(self.index, 'Status', str(jobs['message']), self.parent.tableWidget, COLORS.BLUE)
                time.sleep(0.5)
                self.stopMining.emit(self.index)
                time.sleep(1)
                return
            
            elif 'Tài khoản chưa được cấu hình' in str(jobs['message']) or 'Tài khoản chưa được cấu hình. Vui lòng thiết lập tài khoản trước khi tiếp tục!' in str(jobs['message']):
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {jobs["message"]}', self.parent.tableWidget, COLORS.GREEN)
                self.dict_add['tlc'] = False
                return 

            elif jobs['message'] == 'Hiện tại chưa có job, huhu đợi thôi ^^!' or 'Thao tác quá nhanh, mỗi request lấy job của mỗi tài khoản cách nhau 10s ^^!' in str(jobs) or 'data' not in str(jobs) or jobs['data'] == [] or jobs['data'] == None:
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {jobs["message"]}', self.parent.tableWidget, COLORS.GREEN)
                return
         
            
           
            self.total_jobs = len(jobs['data'])
            for index, job in enumerate(jobs['data'], start=1):
                self.remaining_jobs = self.total_jobs - index
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                
                self.__job_id, self.object_id, self.__link = job['job_id'], job['object_id'], job['link']
                # self.link = f'https://m.tiktok.com/v/{self.object_id}.html'
                
                # self.__link = f'https://www.tiktok.com/@username/video/{self.object_id}'
                
                self.__link = f'https://www.tiktok.com/@{self.__link}/video/{self.object_id}'
                if "www.." in self.__link or self.__link.startswith("https://.") or self.__link.startswith("http://"):
                    self.__link = self.__link.replace("https://.", "https://www.", 1).replace("www..", "www.").replace("http://", "https://", 1)
                elif not self.__link.startswith(("http://", "https://")):
                    self.__link = f'https://www.{self.__link}'
                elif "www." not in self.__link.split('/')[2]:
                    self.__link = self.__link.replace("https://", "https://www.", 1)

                self.editStatus.emit('jobs', '', 1)
                self.performAction()
                self.total += 1
                self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                getXu = self.__apitanglikecheo.guiDuyet(self.__job_id, self.__typeJob, 0)
                self.tyle = 0
                if 'coin_today' in str(getXu):
                    for i in getXu['data']:
                        self.editStatus.emit('xuthem', 'tanglikecheo', int(i['coin']))
                        if i['coin'] >= 6:
                            self.tyle += 20
                            self.dict_xuthem['tlc'] += i['coin']
                        self.editCellByColumnName.emit(self.index, 'Status', f"🎉 Thành công! Bạn vừa được cộng thêm {i['coin']} xu. Hiện tại Rate hoàn thành là {self.tyle}%.",self.parent.tableWidget, COLORS.GREEN)
                    # if self.tyle <= 0:
                    #     self.__block += 1
                    # else: 
                    #     self.__block = 0
                    time.sleep(1)
                    self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)

                    self.editCellByColumnName.emit(self.index, 'Rate', f'{self.tyle}% TLC', self.parent.tableWidget, COLORS.GREEN)
                        
                self.start_func  = time.time()
                
                self.configureDelay('NextJob')
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(3)
    
    def startMIN(self):
        self.__typeStart = 'MIN'
        try:
            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
            jobs = self.__apiMIN.getJob(self.__typeJob)
            logging.debug(jobs)
            if 'data' not in str(jobs) or jobs['data'] == [] or jobs['data'] == None: return
            self.total_jobs = len(jobs['data'])
            for index, job in enumerate(jobs['data'], start=1):
                self.remaining_jobs = self.total_jobs - index
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                self.__job_id, self.__link ,self.joblam = job['job_id'], job['link'] ,job['uid']
                if self.__link in self.__dalam:
                    guiDuyet = self.__apiMIN.guiDuyet(self.__job_id, self.__typeJob, self.__hide)
                    self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ⚠️ Nhiệm vụ ID {self.__job_id} đã được hoàn thành hoặc bỏ qua trước đó. Tiếp tục với nhiệm vụ tiếp theo...", self.parent.tableWidget, COLORS.RED)
                    return 
                if self.__typeJob == 'love':
                    self.__link = self.__link + '/' + self.__link
                else: self.__link = f'https://www.tiktok.com/search?q={self.joblam}'
                self.editStatus.emit('jobs', '', 1)
                self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                result = self.performAction()
                if result is True or result is False:
                    self.total += 1
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Báo cáo hoàn thành nhiệm vụ {self.__typeJob}.',self.parent.tableWidget, COLORS.GREEN)
                    guiDuyet = self.__apiMIN.guiDuyet(self.__job_id, self.__typeJob, self.__hide)
                    self.__cache = guiDuyet['cache']
                    logging.info(guiDuyet)
                    if self.__cache >= 6:
                        getXu = self.__apiMIN.getXu(self.__typeJob)
                        logging.info(getXu)
                        # [2025-01-11 07:41:17] | LEVEL: INFO | THREAD: Dummy-1 | MODULE: thread | FUNC: startMIN | LINE: 452| MESSAGE: {'success': True, 'message': 'Nhận 10 coin', 'coin_received': 10, 'data': '2/5'}
                        self.editStatus.emit('xuthem', 'min', int(getXu['coin_received']))
                        self.dict_xuthem['min'] += int(getXu['coin_received'])
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {getXu["message"]}',self.parent.tableWidget, COLORS.GREEN);time.sleep(2)
                        self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)

                        self.editCellByColumnName.emit(self.index, 'Rate', f'{getXu["data"]} MIN', self.parent.tableWidget, COLORS.GREEN)
           
                delay_time = random.randint(3,5)
                self.configureDelay(type='NextJob',delay=delay_time )
                # self.configureDelay('NextJob')
                
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(3)
    
    def startTIKTOP(self):
        if self.datniktiktop['uid'] == None:
            return
        try:
            self.__typeStart = 'TIKTOP'
            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
            jobs = self.__apitiktop.getJob(1 if self.__typeJob == 'love' else 2)
            logging.debug(jobs)
            if jobs['status'] == 'success':

                self.__job_id, self.__link ,self.userjob   = jobs['task_execution_id'], jobs['links'][2],jobs['entity_data']["username"].strip()
                self.joblam = self.userjob.strip()
                self.__link = f'https://www.tiktok.com/search/user?q={self.joblam}'

                try:
                    skip = open('skip_tiktop.txt','r',encoding='utf-8').read().strip().split('\n')
                except:
                    skip = []
                    open('skip_tiktop.txt','w',encoding='utf-8').close()
                if self.__link in self.__dalam or self.__link in skip:
                    closeJob = self.__apitiktop.guiDuyet(self.__job_id, 'hide')
                    self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ⚠️ Nhiệm vụ ID {self.__job_id} đã được hoàn thành hoặc bỏ qua trước đó. Tiếp tục với nhiệm vụ tiếp theo...", self.parent.tableWidget, COLORS.RED)
                    return 
                
                self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                self.editStatus.emit('jobs', '', 1)
                for _ in range(3):
                    try:
                        self.__dalam.append(self.__link)
                        user_info       = get_user_info(str(self.joblam), self.proxy)
                        if user_info == None:
                            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] Không kiểm tra được thông tin @{self.userjob}!!!" ,self.parent.tableWidget, COLORS.OLIVE);time.sleep(1)
                        else:
                            user_info   = get_user_by_cookie(str(self.joblam), session=self.ss)

                        if user_info.get('privateAccount'):
                            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] Người dùng @{self.userjob} đang ở chế độ riêng tư" ,self.parent.tableWidget, COLORS.BLACK);time.sleep(1)
                            break
                        secUid          = user_info['secUid']
                        user_id         = user_info['user_id']
                        follow_info     = follow_user(user_id=user_id, sec_uid=secUid, cookie=self.cookieChrome, session=self.ss)
                        if follow_info:
                            self.total += 1
                            self.id_storage_ttc += self.__job_id + ','
                            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] Theo dõi thành công người dùng @{self.userjob}" ,self.parent.tableWidget, COLORS.GREEN);time.sleep(1)
                            break
                    except:pass
                else:
                    self.fail_follow +=1
                    self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] Theo dõi người dùng @{self.userjob} thất bại" ,self.parent.tableWidget, COLORS.RED);time.sleep(1)
                try:
                    if user_info.get('privateAccount'):
                        self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] Người dùng @{self.__link} đang ở chế độ riêng tư" ,self.parent.tableWidget, COLORS.BLACK);time.sleep(1)
                        return 
                except:pass
                self.configureDelay('GetCoin')
                for _ in range(5):
                    getXu = self.__apitiktop.guiDuyet(self.__job_id, 'check')
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] GETXU: {getXu} Task ID: {self.__job_id} User: {self.joblam}', self.parent.tableWidget, COLORS.GREEN)
                    if getXu['status'] == 'success':
                        break
                    time.sleep(5)
                    

                for t in range(3):
                    check = self.__apitiktop.status_check_task(getXu['job_id'])
                    logging.debug(check)
                    if check['status'] == 'success':
                        self.editStatus.emit('xuthem', 'tiktop', 0.25 if self.__typeJob == 'love' else 0.30)
                        self.dict_xuthem['tiktop'] += 0.25 if self.__typeJob == 'love' else 0.30
                        self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                        self.editCellByColumnName.emit(self.index, 'Rate', f'1/1 TOP', self.parent.tableWidget, COLORS.GREEN)
                        self.editCellByColumnName.emit(self.index, 'Status', "✅ Hoàn thành nhiệm vụ! Bạn đã nhận được 0.25 xu.", self.parent.tableWidget, COLORS.GREEN)
                        break
                    
                    elif check['status'] == 'error':
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] CHECK: {check} Task ID: {self.__job_id} User: {self.joblam}', self.parent.tableWidget, COLORS.RED)
                    time.sleep(5)
                self.configureDelay('NextJob')
        except Exception as e: 
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({e})', self.parent.tableWidget, COLORS.RED)
            logging.debug('Error')
            try:
                if self.datniktiktop['uid'] == None:
                    self.dict_add['tiktop'] = False; self._addtiktop = 0
            except:
                self.dict_add['tiktop'] = False; self._addtiktop = 0
                time.sleep(3)
   
    def startALL(self):
        global LOGIN_ACCOUNT
        self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
        while True:
            # try:
            #     self.proxyrq = open('proxy_requests.txt','r',encoding='utf-8').read().strip().split('\n')[self.index]
            # except:self.proxyrq = ''
            self.__typeStart = 'ALL'
            try:
                    try:
                        LOGIN_ACCOUNT.remove(self.index)
                    except:pass

                    def setupThread():
                        if self.settings['EarningOptions']['TLC'] and self.dict_add['tlc'] == False:
                            self.dict_add['tlc'] = True
                            self.__apitanglikecheo = TLC(access_token = self.settings['WalletSettings']['TLC'])
                            login                  = self.__apitanglikecheo.infoAccount()
                            if login['success'] == False:
                                self.status = 'Kiểm tra lại tài khoản tanglikecheo.com!!!';return False
                            for attempt in range(1, 2): 
                                self.editCellByColumnName.emit(
                                    self.index, 
                                    'Status', 
                                    f'[ TLC ] ✅ Đang cấu hình tài khoản TikTok ({attempt}/100). Tiến trình đang diễn ra...', 
                                    self.parent.tableWidget, 
                                    COLORS.GREEN
                                )
                                datnick = self.__apitanglikecheo.datNick(self.uid)
                                logging.debug(datnick)
                                if datnick['success'] == False:
                                    self.editCellByColumnName.emit(self.index, 'Status', str(datnick['message']), self.parent.tableWidget, COLORS.RED)
                                    if 'Tài khoản chưa cập nhật avatar, hãy hãy cập nhật trước khi thêm!' in str(datnick['message']):
                                        self.uploadAvt()
                                        time.sleep(15)
                                        datnick = self.__apitanglikecheo.datNick(self.uid)
                                        logging.debug(datnick)
                                        if datnick['success']:
                                            self.dict_add['tlc'] = True
                                            break
                                        self.status = datnick['success']
                                        self.editCellByColumnName.emit(self.index, 'Status', str(datnick['message']), self.parent.tableWidget, COLORS.RED)
                                        time.sleep(0.5)
                                        self.stopMining.emit(self.index)
                                        time.sleep(1)
                                        return
                                    if 'Tài khoản không công khai video đã thích, hãy công khai trước khi thêm' in str(datnick['message']):
                                        self.public()
                                        continue
                                    if 'Tài khoản đã được thêm bởi 1 user khác, bạn không thể thêm lại' in str(datnick['message']):
                                        self.status = 'Tài khoản đã được thêm bởi 1 user khác, bạn không thể thêm lại'
                                        self.check_add_roi = 1
                                        # return
                                        return False
                                else:
                                    break
                                time.sleep(15)
                            
                        if self.settings['EarningOptions']['TTC'] and self.dict_add['ttc'] == False:
                            try:
                                self.token = open(PATHDATA+'\\tokenTTC.txt', 'r', encoding='utf-8').read().strip().split('\n')[self.index]
                                self.editCellByColumnName.emit(self.index, 'Token', str(self.token), self.parent.tableWidget, COLORS.BROWN)
                            except:
                                logging.error('Có lỗi xảy ra khi lấy TOKEN TTC', exc_info=True)
                                self.status = f'Vui lòng nhập Token TTC rồi chạy lại!!!'
                                self.editCellByColumnName.emit(self.index, 'Status', str(self.status), self.parent.tableWidget, COLORS.RED)
                                time.sleep(0.5)
                                self.stopMining.emit(self.index)
                                time.sleep(1)
                                return

                        
                            self.editCellByColumnName.emit(
                                self.index, 
                                'Status', 
                                f'[ TTC ] 🔑 Sử dụng token {self.token.upper()}. Bắt đầu cấu hình ban đầu...', 
                                self.parent.tableWidget, 
                                COLORS.RED
                            )
                            while True:
                                
                                self.__apituongtaccheo = TTC(access_token = self.token,proxy=self.proxy)
                                login                  = self.__apituongtaccheo.login()
                                status_icon = "✅" if login["status"] == "success" else "❌"
                                status_color = COLORS.GREEN if login["status"] == "success" else COLORS.RED
                                status_message = f"🎉 Thành công!" if login["status"] == "success" else f"💔 Thất bại: {login['mess']}"
                                self.editCellByColumnName.emit(
                                    self.index,
                                    'Status',
                                    f"[ TTC ] {status_icon} Đăng nhập bằng {self.token.upper()} | MESSAGE: {status_message}",
                                    self.parent.tableWidget,
                                    status_color
                                )
                                # logging.debug(login)
                                if login['status'] == 'success':
                                    
                                    break
                                time.sleep(3);self.editCellByColumnName.emit(self.index, 'Status', f'⏳ [ TTC ] Đăng nhập thất bại 💔. Chờ thử lại...', self.parent.tableWidget, COLORS.RED)
                                time.sleep(random.randint(12, 27))
                            for attempt in range(1, 2): 
                                self.editCellByColumnName.emit(
                                    self.index, 
                                    'Status', 
                                    f'[ TTC ] ✅ Đang cấu hình tài khoản TikTok ({attempt}/100). Tiến trình đang diễn ra...', 
                                    self.parent.tableWidget, 
                                    COLORS.GREEN
                                )
                                datnick = self.__apituongtaccheo.datNick(self.uid)
                                logging.debug(datnick)
                                if datnick['status'] == 'success':
                                    self.dict_add['ttc'] = True
                                    break
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ TTC ] ⚠️ Lần thử {attempt}/100: Cấu hình tài khoản {self.uid} thất bại. {datnick["mess"]}', self.parent.tableWidget, COLORS.RED)
                                time.sleep(random.randint(15, 30))
                            else:
                                self.status = 'Cấu hình tài khoản TTC thất bại'
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ TTC ] ❌ Không thể cấu hình tài khoản {self.uid} sau 100 lần thử.',self.parent.tableWidget, COLORS.RED)
                                return False
                        
                        if self.settings['EarningOptions']['TDSV1'] and self.dict_add['tdsv1'] == False:
                            try:
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ TDSV1 ] Cấu hình tài khoản {self.uid}',self.parent.tableWidget, COLORS.GREEN)
                                time.sleep(1)
                                try:
                                    self.tokentdsv1 = open(PATHDATA+'\\tokenTDS.txt', 'r', encoding='utf-8').read().strip().split('\n')[self.index]
                                    self.editCellByColumnName.emit(self.index, 'Token', str(self.tokentdsv1), self.parent.tableWidget, COLORS.BROWN)
                                except:
                                    logging.error('Có lỗi xảy ra khi lấy TOKEN TDSV1', exc_info=True)
                                    self.status = f'Vui lòng nhập TokenTDS rồi chạy lại!!!'
                                    self.editCellByColumnName.emit(self.index, 'Status', f'Vui lòng nhập TokenTDS rồi chạy lại!!!',self.parent.tableWidget, COLORS.GREEN)
                                    time.sleep(0.5);self.stopMining.emit(self.index);time.sleep(0.5)
                                    self.dict_add['tdsv1'] = True
                                    self.__apitraodoisubV1 = None
                                    return False
                                self.__apitraodoisubV1 = TDSV1(access_token = self.tokentdsv1, proxy= self.proxy)
                                cauHinhNoCaptcha       = self.__apitraodoisubV1.cauHinhNoCaptcha(self.uid)
                                print(cauHinhNoCaptcha)
                                logging.debug(cauHinhNoCaptcha)
                                # SAGE: {'status': 'success', 'mess': {'error': 'Vui lòng thay avatar, ảnh này đã được sử dụng quá nhiều lần.'}}
                                # if 'Vui lòng thay avatar, ảnh này đã được sử dụng quá nhiều lần.' in str(cauHinhNoCaptcha):
                                #     if self.uploadAvt():
                                #         time.sleep(15)
                                #         self._upload +=1
                                #         if self._upload >=1:
                                #             self.editCellByColumnName.emit(self.index, 'Status', f'[ TDSV1 ] ⚠️ Quá nhiều lần tải ảnh đại diện thất bại, bỏ qua cấu hình TDSV1 cho tài khoản {self.uid}.',self.parent.tableWidget, COLORS.RED)
                                #             self.dict_add['tdsv1'] = True
                                #             time.sleep(5)
                                #             return
                                #     return
                                if 'error' in str(cauHinhNoCaptcha):
                                    self.editCellByColumnName.emit(self.index, 'Status', str(cauHinhNoCaptcha),self.parent.tableWidget, COLORS.SILVER)
                                    time.sleep(1)
                                else:
                                    datnick = self.__apitraodoisubV1.cauHinh(cauHinhNoCaptcha['data']['id'])
                                    logging.debug(datnick)
                                    if 'success' in str(datnick):
                                        self.editCellByColumnName.emit(self.index, 'Status', f'[ TDSV1 ] Cấu hình tài khoản {self.uid} thành công.',self.parent.tableWidget, COLORS.GREEN)
                                        self.dict_add['tdsv1'] = True
                                        time.sleep(1)
                                        return True
                            except Exception as e:
                                logging.error('Lỗi cấu hình TDSV1', exc_info=True)
                            self.dict_add['tdsv1'] = True
                            self.__apitraodoisubV1 = None
                            
                        if self.settings['EarningOptions']['TIKTOP'] and self.dict_add['tiktop'] == False:
                            self._addtiktop +=1
                            if self._addtiktop >=5:
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ TIKTOP ] ⚠️ Quá nhiều lần tải ảnh đại diện thất bại, bỏ qua cấu hình TIKTOP cho tài khoản {self.uid}.',self.parent.tableWidget, COLORS.RED)
                                self.dict_add['tiktop'] = True
                                return
                            cookie_string = open(PATHDATA+'\\tiktop.txt', 'r', encoding='utf-8').read().strip().split('\n')[0]
                            
                            self.__apitiktop = TIKTOP(cookie_string)
                            for t in range(1):
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ TIKTOP ] Cấu hình tài khoản {self.uid} lần {t}',self.parent.tableWidget, COLORS.GREEN)
                                try:
                                    self.datniktiktop = self.__apitiktop.datNick(self.uid)
                                    print('Cấu hình tiktop',self.datniktiktop)
                                    self.editCellByColumnName.emit(self.index, 'Status', str(self.datniktiktop), self.parent.tableWidget, COLORS.GREEN)
                                    # if 'change default avatar' in str(self.datniktiktop):
                                    #     self.uploadAvt()
                                    #     time.sleep(15)
                                    if self.datniktiktop['uid'] != None:
                                        self.dict_add['tiktop'] = True
                                        break
                                except:pass
                                time.sleep(1)
                            else:  self.status = 'Cấu hình tài khoản TikTop thất bại';return False
                      
                        if self.settings['EarningOptions']['TDSV2'] and self.dict_add['tdsv2'] == False:
                            self.editCellByColumnName.emit(self.index, 'Status', f'[ TDSV2 ] Cấu hình tài khoản {self.uid}',self.parent.tableWidget, COLORS.GREEN)
                            self.dict_add['tdsv2'] = True
                            self.tokenTDS = self.settings['WalletSettings']['TDSV2']
                            self.__apitraodoisubV2 = TDSV2(access_token = self.tokenTDS)
                            login                  = self.__apitraodoisubV2.infoAccount()
                            # logging.debug(login)
                            if login['success'] != 200:
                                self.status = 'Kiểm tra lại tài khoản traodoisub.com!!!';return False
                            datnick = self.__apitraodoisubV2.datNick(str(self.uid))
                            logging.debug(datnick)
                            if datnick['success'] != 200:
                                self.status = datnick['msg']
                                return False

                        if self.settings['EarningOptions']['MIN'] and self.dict_add['min'] == False:
                            global ADD_ACCOUNTS
                            while True:
                                if len(ADD_ACCOUNTS) > 3:
                                    self.editCellByColumnName.emit(self.index, 'Status', 'Đợi các luồng khác cấu hình toàn tất...', self.parent.tableWidget, COLORS.RED);time.sleep(3)
                                    continue   
                                ADD_ACCOUNTS.append(self.index) 
                                break
                            
                            self.__apiMIN = MIN(self.settings['WalletSettings']['MIN'], self.uid)
                            for attempt in range(1, 2): 
                                self.datnik = self.__apiMIN.addTikTok()
                                logging.debug(self.datnik)
                                if self.datnik['success'] == True:      
                                    if 'is already config' in self.datnik['message'] or 'is config success' in self.datnik['message'] or 'thành công' in self.datnik['message'] or 'đã được config' in self.datnik['message']:
                                        self.dict_add['min'] = True
                                        if self.index in ADD_ACCOUNTS:ADD_ACCOUNTS.remove(self.index)
                                        break
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ MIN ] ⚠️ Lần thử {attempt}/100: Cấu hình tài khoản {self.uid} thất bại. {self.datnik["message"]}', self.parent.tableWidget, COLORS.RED)

                            else:
                                if self.index in ADD_ACCOUNTS:ADD_ACCOUNTS.remove(self.index)
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ MIN ] ❌ Không thể cấu hình tài khoản {self.uid}.',self.parent.tableWidget, COLORS.RED)
                                return False
                            
                            if self.index in ADD_ACCOUNTS:ADD_ACCOUNTS.remove(self.index)

                        return True
                    self.__updateValue();time.sleep(1)
                    # self.public()
                    setupThread()
                    while True:
                            try:
                                for t in range(20):
                                   
                                    self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())

                                    self.start_func  = time.time()
                                    # Thực hiện các điều kiện
                                    for key, funcs in {
                                        # 'TTC': [self.startTTC1, self.startTTC2],
                                        'TTC': [self.startTTC1],
                                        'TDSV1': [self.startTDSV1],
                                        'TDSV2': [self.startTDSV2],
                                        # 'TDSV2': [self.startTTC2],
                                        'TIKTOP': [self.startTIKTOP],
                                        'MIN': [self.startMIN],
                                        'TLC': [self.startTLC],
                                    }.items():
                                        if self.settings['EarningOptions'][key]:
                                            if self.dict_add.get(key, False) == False: checkAdd = setupThread()
                                            else: checkAdd = True

                                            if checkAdd:
                                                self.__typeJob = self.settings['TaskSettings']['Task'].lower()
                                                if ',' in self.__typeJob:
                                                    # self.__typeJob = random.choice(self.__typeJob.split(','))
                                                    self.__typeJob = 'follow'
                                                for func in funcs:
                                                    func()
                                                    

                                    self.__typeStart = 'ALL'
                                    
                                    if self.settings['TaskSettings']['Captcha']: self.bypassCaptcha(5)
                                    elapsed_time = int(round(time.time() - self.start_func))
                                    # remaining_time = min(10, max(0, elapsed_time - self.settings['DelaySettings']['WaitJob']))
                                    
                                    remaining_time = min(10, max(0, self.settings['DelaySettings']['WaitJob'] - elapsed_time))

                                    self.editCellByColumnName.emit(self.index, 'Status', f"Hoàn tất công việc: '{self.__typeJob}' | Thời gian thực hiện: {elapsed_time} giây | Thời gian chờ còn lại: {remaining_time} giây",self.parent.tableWidget, COLORS.RED)
                                    time.sleep(1)
                                    self.configureDelay('all', remaining_time)
                            except:pass
                            try:
                                if self.__apituongtaccheo.infoAccount()['user'] == '':
                                    self.editCellByColumnName.emit(self.index, 'Status', f'Tài khoản TTC bị đăng xuất!!!',self.parent.tableWidget, COLORS.RED)
                                    self.dict_add['ttc'] = False
                                    time.sleep(5)
                                # if self.__apituongtaccheo2.infoAccount()['user'] == '':
                                #     self.editCellByColumnName.emit(self.index, 'Status', f'Tài khoản TTC2 bị đăng xuất!!!',self.parent.tableWidget, COLORS.RED)
                                #     self.dict_add['ttc2'] = False
                                #     time.sleep(5)
                            except:pass
                            time.sleep(5)
               
                    
            except Exception as e: 
                logging.error(f"An error occurred: {e}")
                error_detail = traceback.print_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
                time.sleep(15)
        # else:
        #     self.editCellByColumnName.emit(self.index, 'Status', f'Không thể kiểm tra, đăng nhập tài khoản {self.uid} liên tiếp nhiều lần.', self.parent.tableWidget, COLORS.RED)
        #     time.sleep(0.5);self.stopMining.emit(self.index)
    
    def initJobBrowser(self):
        global LOGIN_ACCOUNT, USED_POS
        self.__updateValue()
        self.dict_xuthem = {'ttc': 0,'tlc': 0,'tdsv1': 0,'tdsv2': 0,'tiktop': 0,'min': 0,}
        self.dict_add = { 'ttc': False,'ttc2': False, 'tlc': False, 'tdsv1': False, 'tdsv2': False, 'tiktop': False, 'min': False, }
        self.__getJob = 0; self.__dalam = []; self.__hide = 0; self.title = ''; self.id_storage_ttc = ''; self.id_storage_ttc2='';self.countdownTTC1 = 0; self.countdownTTC2 = 0; self.login_time = 0; self.countdownTDS = 0
        self.__block = 0
        self.check_add_roi =0

        self.__updateValue()
        self.editCellByColumnName.emit(self.index, 'ToTal', '',self.parent.tableWidget, COLORS.GREEN)
        self.editCellByColumnName.emit(self.index, 'Rate', '',self.parent.tableWidget, COLORS.GREEN)
        self.editCellByColumnName.emit(self.index, 'Job Info', '',self.parent.tableWidget, COLORS.GREEN)
        self.editCellByColumnName.emit(self.index, 'Status', f"Khởi động luồng...", self.parent.tableWidget, COLORS.RED)
        if self.uid == '':
            while True:
                try:
                    self.user_data = requests.get('https://pytournes.io.vn/api/get_users.php?count=1&admin_type=domainAVT').json()
                    if self.user_data['status'] == 'success':
                        self.editCellByColumnName.emit(self.index, 'Status', f"✨ [ID: {self.user_data['data'][0]['id']}] Người dùng '{self.user_data['data'][0]['username']}' đã được tìm thấy, kiểm tra trạng thái tài khoản...", self.parent.tableWidget, COLORS.ORANGE)
                        # if checkLiveUID(username = self.user_data['data'][0]['username'], proxy = self.proxyRequests)['live']:
                        self.uid = self.user_data['data'][0]['username']
                        self.pwd = self.user_data['data'][0]['password']
                        self.twofa = self.user_data['data'][0]['twofa']
                        self.cookieChrome = self.user_data['data'][0]['cookie']
                        self.mail = self.user_data['data'][0]['mail']
                        self.passmail = self.user_data['data'][0]['passmail']
                        if len(self.cookieChrome) >= 50:
                            self.sessionid = "sessionid=" + self.cookieChrome.split("sessionid=")[1].split(";")[0].strip() + ";"
                        else:
                            self.sessionid = self.cookieChrome
                        self.editCellByColumnName.emit(self.index, 'UID', str(self.user_data['data'][0]['username']),self.parent.tableWidget, COLORS.ORANGE)
                        self.editCellByColumnName.emit(self.index, 'Password', str(self.user_data['data'][0]['password']),self.parent.tableWidget, COLORS.ORANGE)
                        self.editCellByColumnName.emit(self.index, '2FA', str(self.user_data['data'][0]['twofa']),self.parent.tableWidget, COLORS.ORANGE)
                        self.editCellByColumnName.emit(self.index, 'Cookie', str(self.user_data['data'][0]['cookie']),self.parent.tableWidget, COLORS.ORANGE)
                        self.editCellByColumnName.emit(self.index, 'Mail', str(self.user_data['data'][0]['mail']),self.parent.tableWidget, COLORS.ORANGE)
                        self.editCellByColumnName.emit(self.index, 'Status', f"✨ [ID: {self.user_data['data'][0]['id']}] Người dùng '{self.user_data['data'][0]['username']}' đã được tìm thấy. Status: live.", self.parent.tableWidget, COLORS.ORANGE)
                        self.saveDataTable.emit()
                        time.sleep(3)
                        break
                        
                    # else:
                    #     self.editCellByColumnName.emit(self.index, 'Status', str(self.user_data['message']), self.parent.tableWidget, COLORS.RED)
                    #     time.sleep(1);self.stopMining.emit(self.index);time.sleep(1)
                except Exception as e:
                    self.editCellByColumnName.emit(self.index, 'Status', f"💥 Lỗi khi lấy user: {str(e)}", self.parent.tableWidget, COLORS.RED)
                    pass
                time.sleep(random.randint(15,30))
        self.__updateValue();time.sleep(1)
        # print(cookie_str_to_dict(self.cookieChrome))
        
        if 'sessionid' in self.cookieChrome:
            if len(self.cookieChrome) >= 50:
                self.sessionid = "sessionid=" + self.cookieChrome.split("sessionid=")[1].split(";")[0].strip()
            else:
                self.sessionid = self.cookieChrome
            time.sleep(5)
        # try:
        for _ in range(3):
            try:
                self.editCellByColumnName.emit(self.index, 'Status', f'Kiểm tra Cookie {self.sessionid}', self.parent.tableWidget, COLORS.GREEN)
                check = check_login(cookie_str= self.cookieChrome.strip(), proxy=self.proxy)
                if check == 'ok':
                    self.editCellByColumnName.emit(
                        self.index, 'Status',
                        f'Cookie {self.sessionid} LIVE',
                        self.parent.tableWidget, COLORS.GREEN
                    )
                    break
                elif check == 'faild':
                    self.editCellByColumnName.emit(self.index, 'Status', f'Kiểm tra Cookie {self.sessionid} thất bại', self.parent.tableWidget, COLORS.RED)
                    
                elif check in ('proxy_die', 'proxy_timeout', 'proxy_blocked'):
                    self.status = 'Proxy lỗi, kiểm tra lại'
                    self.editCellByColumnName.emit(
                        self.index, 'Status',
                        self.status,
                        self.parent.tableWidget, COLORS.RED
                    )
                    return True

                else:
                    self.status = 'Cookie DIE'
                    self.editCellByColumnName.emit(
                        self.index, 'Status',
                        self.status,
                        self.parent.tableWidget, COLORS.RED
                    )
                    return True
            except Exception as e:
                print(e)
            time.sleep(random.randint(3,5))
        else:
            self.editCellByColumnName.emit(self.index, 'Status', f'Kiểm tra Cookie {self.sessionid} Die.', self.parent.tableWidget, COLORS.RED)
            time.sleep(random.randint(3,5))
            self.clearAcc()
            self.initJobBrowser()
       
        self.ss = requests.Session()
        if self.proxy == '':
            proxyDict = ''
        else:
            parts = self.proxy.split(':')
            if len(parts) >= 4:
                iport = ":".join(parts[:2])
                userpass = ":".join(parts[2:])
                proxyDict = {
                    'http': f'http://{userpass}@{iport}',
                    'https': f'http://{userpass}@{iport}'
                }
            elif len(parts) >= 2:
                proxy_url = f'http://{self.proxy}'
                proxyDict = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                
        self.ss.proxies.update(proxyDict)
        headers = {
            'Host': 'login-no1a.www.tiktok.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }

        data = {
            'aid': '1459',
        }
        for _ in range(10):
            try:
                response = self.ss.post(
                    f'https://login-no1a.www.tiktok.com/passport/web/store_region/',
                    data=data,
                    headers=headers,
                )
            except:
                pass
        self.ss.cookies.update(cookie_str_to_dict(self.cookieChrome))
        self.ss.cookies.update(response.cookies.get_dict())

        self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
        self.startALL()

    def run(self):  
        while True:
            if len(LOGIN_ACCOUNT) >= 5:
                self.editCellByColumnName.emit(self.index, 'Status', 'Đợi các luồng khác khởi động và đăng nhập tài khoản hoàn tất...', self.parent.tableWidget, COLORS.RED);time.sleep(3)
                time.sleep(1)
                continue    
            LOGIN_ACCOUNT.append(self.index)
            for i in range((len(LOGIN_ACCOUNT) -1)*5, 0, -1):
                self.editCellByColumnName.emit(self.index, 'Status', f'🔎 Đã tìm thấy slot trống! Trình duyệt sẽ khởi động sau {i} giây...', self.parent.tableWidget, COLORS.ORANGE)
                time.sleep(1)
            break
        
        
        self.initJobBrowser()
        # if self.openBrowser():
        #                     self.driver.get('https://www.tiktok.com/')
        #                     self.editCellByColumnName.emit(self.index, 'Status', f'Bị nhả lấy lại Cookie!!!', self.parent.tableWidget, COLORS.RED)
        #                     self.clearCookies()
        #                     self.addCookie()
        #                     self.getCookie()
        #                     self.kill_process_on_port()
        #                     time.sleep(1)

        self.__updateValue()
        time.sleep(3);self.stopMining.emit(self.index)
      
    def configureDelay(self, type, delay = 0):
        if type != 'countdown' and type != 'all' and delay == 0 and type != 'wait' and type != 'url':
            delay = self.settings['DelaySettings'][type]
        if delay > 0:
            if type == 'NextJob':
                textInfo = f'[ {self.__typeStart} ] 🚀 Đang chuẩn bị cho nhiệm vụ {self.__typeJob.upper()} tiếp theo...'
            elif type == 'GetCoin':
                textInfo = f'[ {self.__typeStart} ] 💰 Nhận xu nhiệm vụ {self.__typeJob.upper()} ngay sau đây...'
            elif type == 'WaitJob':
                textInfo = f'[ {self.__typeStart} ] ⏳ Hết nhiệm vụ {self.__typeJob.upper()} lần {self.__getJob}, đang chuẩn bị lấy nhiệm vụ mới...'
            elif type == 'countdown':
                textInfo = f'[ {self.__typeStart} ] ⏰ Countdown {delay}s, nhiệm vụ mới sẽ được lấy ngay sau...'
            elif type == 'tlc':
                textInfo = f'[ {self.__typeStart} ] ⌛ Đang chờ {delay}s, tìm nhiệm vụ mới sau...'
            elif type == 'all':
                textInfo = f'[ DELAY ] 🌀 Tạm nghỉ {delay}s, tiếp tục tìm nhiệm vụ mới ngay sau...'
                delay += 1
            elif type == 'wait':
                textInfo = f'[ {self.__typeStart} ] 🧠 Quá nhiều nhiệm vụ tạm nghỉ {delay}s, làm nhiệm vụ tiếp sau...'
            elif type == 'url':
                textInfo = f'[ {self.__typeStart} ] 🧠 Chuyển link thất bại tạm nghỉ {delay}s, làm nhiệm vụ tiếp sau...'


            for i in range(int(delay), 0, -1):
                self.editCellByColumnName.emit(self.index, 'Status', f'{textInfo} {i} giây còn lại... ⏳', self.parent.tableWidget, COLORS.GREEN)
                time.sleep(1)

    def clearAcc(self):
        self.editCellByColumnName.emit(self.index, 'UID', '',self.parent.tableWidget, COLORS.RED)
        self.editCellByColumnName.emit(self.index, 'Password', '',self.parent.tableWidget, COLORS.RED)
        self.editCellByColumnName.emit(self.index, '2FA', '',self.parent.tableWidget, COLORS.RED)
        self.editCellByColumnName.emit(self.index, 'Cookie', '',self.parent.tableWidget, COLORS.RED)
        self.editCellByColumnName.emit(self.index, 'Mail', '',self.parent.tableWidget, COLORS.RED)
        self.editCellByColumnName.emit(self.index, 'Passmail', '',self.parent.tableWidget, COLORS.RED)

        time.sleep(1);self.__updateValue();time.sleep(1)
    
    def clearCookies(self):
        # Xóa cookies
        self.driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        # Xóa cache
        self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
        # Thậm chí có thể xóa toàn bộ storage của website cụ thể
        self.driver.execute_cdp_cmd("Storage.clearDataForOrigin", {
            "origin": "*",
            "storageTypes": "all"
        })
        # self.driver.refresh();self.driver.set_page_load_timeout(30)
        # time.sleep(3)
    
    def getCookie(self):
        
        try:
            self.driver.refresh();self.driver.set_page_load_timeout(30);time.sleep(3)
            # self.cookieChrome = ""
            # ck_get = self.driver.get_cookies()
            # for value in ck_get:
            #     self.cookieChrome+=value['name']+'='+value['value']+";"
            # self.cookieChrome = self.cookieChrome.strip()
            # Thực thi JS để lấy chuỗi cookie
            cookie_str = self.driver.execute_script("return document.cookie")

            print(f"Cookie lấy được: {cookie_str}")
            self.cookieChrome = cookie_str.strip()
            self.editCellByColumnName.emit(self.index, 'Cookie', str(self.cookieChrome.strip()),self.parent.tableWidget, COLORS.ORANGE)
            time.sleep(1);self.__updateValue();time.sleep(1)
            input('Enter to close')

        except:self.cookieChrome = ''

    def addCookie(self):
        for _ in range(3):
            try:
                self.__updateValue();time.sleep(1)
                
                time.sleep(1)
                # BẮT BUỘC: Phải vào trang web trước khi thêm cookie của trang đó
                if "tiktok.com" not in self.driver.current_url:
                    self.driver.get("https://www.tiktok.com");self.driver.set_page_load_timeout(15)
                    time.sleep(2) # Đợi trang load nhẹ

                cookies = self.sessionid.split(";")
                for c in cookies:
                    if "=" in c:
                        try:
                            name, value = c.strip().split("=", 1)
                            self.driver.add_cookie({
                                "name": name,
                                "value": value,
                                "domain": ".tiktok.com", # Đảm bảo có dấu chấm phía trước
                                "path": "/",
                            })
                        except Exception as e:
                            print(f"❌ Lỗi thêm cookie {name}: {e}")
                # Sau khi thêm xong, refresh lại trang để nhận session mới
                self.driver.refresh()
                time.sleep(3)
                return True
            except:
                time.sleep(5)

    def kill_process_on_port(self):
        try:
            # Lệnh tìm PID đang chiếm port trên Windows
            # findstr :PORT tìm dòng chứa port, tokens=5 lấy giá trị PID ở cột cuối
            cmd = f'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :{self.port}\') do taskkill /F /PID %a /T'
            
            # Chạy lệnh ẩn (không hiện cửa sổ CMD đen)
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Xóa file SingletonLock của Profile (nguyên nhân gây crash khi port bị treo)
            lock_file = os.path.join(self.profile_path, "SingletonLock")
            if os.path.exists(lock_file):
                os.remove(lock_file)
                
        except Exception as e:
            print(f"Lỗi khi dọn dẹp port {self.port}: {e}")

    def stop(self):
        global USED_POS, LOGIN_ACCOUNT
        self.__updateValue()
        try:
            LOGIN_ACCOUNT.remove(self.index)
        except:pass
      
        self.editCellByColumnName.emit(self.index, 'Status', f'Đã kết thúc, trước đó -> {self.status}', self.parent.tableWidget, COLORS.BLUE)
     
        self.terminate()
