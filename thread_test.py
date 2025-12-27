
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
import threading
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
        self.pos_window = False; self.handle_chrome = False
        self.__pause = []
        self.__typePerError = ''
        self.__getJob = 0; self.__dalam = []; self.__hide = 0; self.title = ''; self.id_storage_ttc2 = ''; self.countdownTTC1 = 0; self.countdownTTC2 = 0; self.login_time = 0; self.countdownTDS = 0;self.cache_count=''
        self.__block = 0; self.__click = False; self._upload = 0;self._addtiktop = 0; self.mail = ''; self.datniktiktop = {'status': 'success', 'uid': None, 'sec_uid': None}
        self.id_storage_ttc = ''
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

        # if isinstance(self.total, (int, float))  == False: self.total = 0
        self.total = int(self.total) if str(self.total).isdigit() else 0

    def openBrowser(self):
        for _ in  range(3):
            try:
                global EXTENSION_ID
                self.__updateValue()
                self.editCellByColumnName.emit(self.index, 'Status', f"🔄 Đang mở trình duyệt... Quá trình có thể mất vài giây!", self.parent.tableWidget, COLORS.GREEN)

                # Lấy vị trí cửa sổ Chrome (tọa độ và kích thước)
                try:
                    self.pos_window = get_next_win_pos()
                    self.indexChrome, self.xChrome, self.yChrome, self.wChrome, self.hChrome = self.pos_window
                except:
                    # Nếu không có vị trí trống, đặt mặc định
                    self.indexChrome, self.xChrome, self.yChrome, self.wChrome, self.hChrome = 0, 0, 0, 700, 1000

                # Cấu hình Chrome Options
                op = webdriver.ChromeOptions()
                # Danh sách các flags cấu hình
                chrome_flags = [
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    '--lang=vi-VN',
                    "--disable-blink-features=AutomationControlled",
                    "--ignore-certificate-errors",
                    "--no-default-browser-check",
                    f"--proxy-server={self.proxy}",
                    "--proxy-bypass-list=*.google.com;*.facebook.com;localhost;127.0.0.1",
                    "--disable-background-timer-throttling",
                    "--disable-renderer-backgrounding",
                    "--disable-backgrounding-occluded-windows",
                    "--mute-audio",
                ]
                op.add_argument(f'--force-device-scale-factor=0.1')
                for flag in chrome_flags:
                    op.add_argument(flag)
                # op.add_argument(f'--disable-features=DisableLoadExtensionCommandLineSwitch')
                self.editCellByColumnName.emit(self.index, 'Status', f"🔄 Đang mở trình duyệt | Proxy: {self.proxy}... Quá trình có thể mất vài giây!", self.parent.tableWidget, COLORS.GREEN)
                # op.add_argument(f'--proxy-server={self.proxy}')
                # op.add_argument("--disable-webrtc")
                logging.debug(self.proxy)
                op.page_load_strategy = "eager"         
                op.add_experimental_option("prefs", {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                })
            
                # Thiết lập Profile Chrome
                self.profile_path = os.path.join(PATHBROWSER, 'Profile', f'luong_{self.index + 1}')
                op.add_argument(f'--user-data-dir={self.profile_path}')
                
                # Tải Extensions
                try:
                    extension_dir = PATHEXTS
                    if os.path.exists(extension_dir):
                        extensions = [os.path.join(extension_dir, ext) for ext in os.listdir(extension_dir) if os.path.isdir(os.path.join(extension_dir, ext))]
                        if extensions:
                            op.add_argument(f'--load-extension={",".join(extensions)}')
                except Exception:
                    self.status = 'Bật Extension lên đi!!!!'
                # - - - - - - - - - - - - - - - - - - - - -

                # Khởi động trình duyệt
                op.binary_location = BINARY_LOCATION
                service = Service(PATHDRIVER+f'\\{BROWSER_TYPE}\\chromedriver.exe')
                self.driver = webdriver.Chrome(service=service ,  options=op )
                # self.driver.set_window_position(-3000, 0, self.wChrome, self.hChrome)
                try:
                    self.handle_chrome = get_handle_from_pid(get_chrome_pid_by_window_title(BROWSER_TYPE))
                    print(self.handle_chrome)
                    if self.handle_chrome: embedApi.embed_tab(self.handle_chrome, new=self.index)

                except Exception as e:
                    traceback.print_exc()
                # self.driver.set_window_rect(self.xChrome, self.yChrome, self.wChrome, self.hChrome)
                self.saved_handles = self.driver.window_handles.copy()
                # Cấu hình ActionChains
                self.actionChains = ActionChains(self.driver)
                self.editCellByColumnName.emit(self.index, 'Status', f"✅ Trình duyệt đã khởi động thành công!", self.parent.tableWidget, COLORS.GREEN)
                if len(self.proxy.split(':')) >= 3:
                # if EXTENSION_ID == '':
                    self.driver.get('chrome://inspect/#extensions');time.sleep(3)
                    for ext in self.driver.find_elements(By.CLASS_NAME, "row"):
                        if "Simple Proxy Switcher" in ext.text:
                            EXTENSION_ID = ext.find_element(By.CLASS_NAME, "url").text.split("//")[1].split("/")[0]
                            print("Extension ID:", EXTENSION_ID)
                            break
                    self.changeProxy('proxyOn')
                    debugger_url = self.driver.capabilities['goog:chromeOptions']['debuggerAddress']
                    logging.debug(F'Debugger Address: {debugger_url}')

                
        
                return True
            except Exception as e:
                try:threading.Thread(target=self.driver.quit, args=()).start()
                except:pass

                kill_profile_processes(self.profile_path)
                self.status = f'Open Browser Error [ {e} ]'
                self.editCellByColumnName.emit(self.index, 'Status', f"❌ Lỗi khởi động trình duyệt: {e}", self.parent.tableWidget, COLORS.RED)
                logging.error('Error', exc_info=True)
                time.sleep(random.randint(10,15))
        if self.pos_window in USED_POS: USED_POS.remove(self.pos_window)
        try:
            if self.handle_chrome: embedApi.unembed_tab(self.handle_chrome)
        except:pass

    def clickElement(self, typeBy: object, source: str, delay: int, click: bool):
        
        try:
            wait = WebDriverWait(self.driver, delay)
            element = wait.until(EC.element_to_be_clickable((typeBy, source)))
            if click:
                element.click()
                # actions = ActionChains(self.driver)
                # actions.move_to_element(element).click().perform()
            return True
        except:
            pass
        logging.debug(f"Type: {typeBy}, Source: {source} Không tìm thấy Element!!!")
        return False

    def checkInternet(self, type = 'chrome'):
        tele = True
        try:
            # Lấy tất cả các tab hiện tại
            current_handles = self.driver.window_handles
            # Chỉ chạy nếu có hơn 1 tab mở
            if len(current_handles) > 1:
                self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ] Phát hiện tab thừa, đang tiến hành đóng...',self.parent.tableWidget, COLORS.GREEN)    
                time.sleep(1)
                for handle in current_handles:
                    if handle not in self.saved_handles:
                        self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ]  {handle} phát hiện tab thừa, hãy đóng tab đó lại.',self.parent.tableWidget, COLORS.GREEN) 
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                        time.sleep(1)
                        try:
                            self.handle_chrome = get_handle_from_pid(get_chrome_pid_by_window_title(BROWSER_TYPE))
                            print(self.handle_chrome)
                            if self.handle_chrome: embedApi.embed_tab(self.handle_chrome, new=self.index)

                        except Exception as e:
                            traceback.print_exc()

                # Quay về tab chính (hoặc tab đầu tiên trong saved_handles)
                self.driver.switch_to.window(self.saved_handles[0])
        except Exception as e:
            self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ] Lỗi đóng tab thừa: {e}',self.parent.tableWidget, COLORS.RED)

        for t in range(50):
            try:
                self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ] Kiểm tra kết nối internet.',self.parent.tableWidget, COLORS.GREEN)
                if type == 'chrome':
                    try:
                        pagesrc = self.driver.page_source
                        
                        if 'Không thể truy cập trang web này' in pagesrc or 'Không có kết nối Internet. Vui lòng thử lại.' in pagesrc or 'Không có Internet' in pagesrc or 'Ôi, hỏng!' in pagesrc or 'Tải lại' in pagesrc or 'Access Denied' in pagesrc or self.clickElement(By.ID, 'reload-button', 1, False):
                            self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ] Mất kết nối internet :<',self.parent.tableWidget, COLORS.RED)
                            try:
                                self.driver.refresh();self.driver.set_page_load_timeout(30)
                            except:pass
                            try:
                                LOGIN_ACCOUNT.remove(self.index)
                            except:pass
                        else:
                            self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ] Kết nối internet ổn định.',self.parent.tableWidget, COLORS.GREEN)
                            break
                    except:
                        self.editCellByColumnName.emit(self.index, 'Status', F'[ {self.__typeStart} ] Ôi, hỏng refresh để tiếp tục!',self.parent.tableWidget, COLORS.RED)
                        time.sleep(5)
                        try:threading.Thread(target=self.driver.quit, args=()).start()
                        except:pass
                        # cmd = f'wmic process where "CommandLine like \'%%luong_{self.index+1}%%\'" delete'
                        # os.system(cmd)
                        # self.driver = None
                        time.sleep(15)
                        self.openBrowser()
                else:
                    try:
                        self.editCellByColumnName.emit(self.index, 'Status', 'Kiểm tra kết nối internet requests :>',self.parent.tableWidget, COLORS.GREEN)
                        rsp = requests.get('https://www.google.com/')
                        break
                    except:self.editCellByColumnName.emit(self.index, 'Status', 'Mất kết nối internet requests :<',self.parent.tableWidget, COLORS.RED)
                time.sleep(5);self.driver.set_page_load_timeout(30)
            except Exception as e: 
                self.__typeStart = 'INTERNET'
                error_detail = traceback.print_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)

    def changeProxy(self, type):
        try:
            if self.proxy != '':
                # extension://cmdfeicnmebicnedjjicmdhejennhhki/popup.html');self.driver.set_page_load_timeout(30);time.sleep
                self.driver.get(f'chrome-extension://{EXTENSION_ID}/popup.html');self.driver.set_page_load_timeout(30);time.sleep(1)
                self.editCellByColumnName.emit(self.index, 'Status', f'Kết nối Proxy: {self.proxy} - type: {type}',self.parent.tableWidget, COLORS.GREEN)
                if type == 'proxyOn':
                    # self.driver.execute_script(f'document.title = "PYTOURNES:PROXY_ON:{self.proxy}"')
                    if self.clickElement(By.NAME, 'import_proxy', 1, True):
                        self.driver.find_element(By.NAME, 'import_proxy').send_keys(self.proxy)
                        if self.clickElement(By.XPATH, "//button[contains(@class, 'saveProxy')]", 5, True):
                            pass
                    if self.clickElement(By.ID, 'heading_import', 1, True):
                        time.sleep(1)
                        self.driver.execute_script(f"""
                            var textarea = document.querySelector("textarea[name='import_proxy']");
                            if (textarea) {{
                                textarea.value = "";  // Xóa nội dung cũ
                                textarea.value = `{self.proxy}`;  // Nhập nội dung mới
                                textarea.dispatchEvent(new Event('input', {{ bubbles: true }})); // Kích hoạt sự kiện input
                            }}
                        """)

                        if self.clickElement(By.XPATH, "//button[contains(@class, 'saveProxy')]", 5, True):
                            pass


                    if self.clickElement(By.XPATH, "//a[contains(@class, 'proxy_select')]", 3, True):
                        return True
                elif type == 'proxyOff':
                    if self.clickElement(By.XPATH, "//button[contains(@class, 'resetProxy')]", 5, True):
                        return True
                    # self.driver.execute_script(f'document.title = "PYTOURNES:PROXY_OFF"')
                    
                self.driver.set_page_load_timeout(10);time.sleep(3)
            
        except Exception as e: logging.debug('Error', exc_info= True)

    def loginAccount(self):
        self.__typeStart = 'SINGUP'
        for _ in range(3):
            # self.adjustWindow(mode='restore')
            try:
                if 'Mật khẩu sai'  in self.status or 'Sai tài khoản hoặc mật khẩu' in self.status or 'Tài khoản của bạn đã bị đình chỉ.'  in self.status or 'Mật khẩu của bạn đã hết hạn và phải được thay đổi để giữ an toàn cho tài khoản.' in self.status or 'Người dùng không tồn tại' in self.status or 'Xác minh 2 bước' in self.status:
                    # time.sleep(3)
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚫 Tài khoản có vấn đề! Lý do: {self.status}!!!', self.parent.tableWidget, COLORS.BLUE)
                    # time.sleep(0.5)
                    # self.stopMining.emit(self.index)
                    # time.sleep(1)
                    self.__updateValue()
                    time.sleep(3)
                    self.deleteProfile()
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚫 Tài khoản có vấn đề! Lý do: {self.status}!!!', self.parent.tableWidget, COLORS.BLUE)
                    time.sleep(5)
                    self.initJobBrowser()
                    return
                self.editCellByColumnName.emit(self.index, 'Status', f"[ {_+1} ] 🔑 Đang đăng nhập tài khoản {self.mail}... Quá trình có thể mất vài phút!", self.parent.tableWidget, COLORS.GREEN)

                try:
                    if 'login' not in self.driver.current_url:
                        self.driver.get(self.url_tiktok+'login');self.driver.set_page_load_timeout(10);time.sleep(1)

                    if self.clickElement(By.XPATH, '//div[text()="Đăng nhập"]|//span[text()="Đăng nhập"]|//button[text()="Đăng nhập"]|//a[@data-e2e="nav-profile"]', 3, True):
                        if self.checkCookie(): return True
                        self.bypassCaptcha(30);time.sleep(5)
                        continue
                    xpath_method = (
                            "//div[text()='Sử dụng số điện thoại/email/tên người dùng']" # Khớp chính xác HTML bạn gửi
                                        # Cách tìm an toàn nhất
                        )
                    
                    if self.clickElement(By.XPATH, xpath_method, 15, True):
                        time.sleep(random.uniform(1, 2))
                        
                        # 2. Chọn tab Đăng nhập bằng email hoặc tên người dùng
                        xpath_email_tab = (
                            "//a[text()='Đăng nhập bằng email hoặc tên người dùng']"
                        )
                        
                        if self.clickElement(By.XPATH, xpath_email_tab, 15, True):
                            time.sleep(random.uniform(1, 2))
                            # --- NHẬP EMAIL/USERNAME ---
                            try:
                                # Tìm ô nhập liệu (thường là @name="username" hoặc @name="email")
                                input_user = self.driver.find_element(By.NAME, "username") 
                                input_user.click()
                                time.sleep(random.uniform(0.5, 1))
                                
                                self.human_type(input_user, self.uid) # Gõ như người thật
                                time.sleep(random.uniform(0.5, 1.2))
                            except:
                                # Trường hợp TikTok hiển thị name="email"
                                input_user = self.driver.find_element(By.NAME, "email")
                                input_user.click()
                                self.human_type(input_user, self.uid)

                            # --- NHẬP MẬT KHẨU ---
                            xpath_pass = '//input[@type="password"]|//input[@placeholder="Mật khẩu"]|//input[@placeholder="Password"]'
                            if self.clickElement(By.XPATH, xpath_pass, 15, False):
                                input_pass = self.driver.find_element(By.XPATH, xpath_pass)
                                input_pass.click()
                                time.sleep(random.uniform(0.3, 0.7))
                                self.human_type(input_pass, self.pwd)
                                time.sleep(random.uniform(1, 2))

                            # --- NHẤN ĐĂNG NHẬP ---
                            xpath_login_btn = (
                                '//button[@type="submit"]|'
                                '//div[text()="Đăng nhập"]|//span[text()="Đăng nhập"]|//button[text()="Đăng nhập"]|'
                                '//div[text()="Log in"]|//span[text()="Log in"]|//button[text()="Log in"]'
                            )
                            
                            # Sử dụng ActionChains để di chuyển chuột tới nút Login trước khi nhấn
                            login_btn = self.driver.find_element(By.XPATH, xpath_login_btn)
                            actions = ActionChains(self.driver)
                            actions.move_to_element(login_btn).pause(random.uniform(0.5, 1)).click().perform()
                            
                            # 3. Giải Captcha & Lấy Code
                            self.bypassCaptcha(5)
                            if self.clickElement(By.XPATH, '//input[@placeholder="Nhập mã gồm 6 chữ số"]', 1, False):
                                print(f" Đang đợi lấy mã xác thực...")
                                code = EmailFake().get_code(self.mail)
                                if code:
                                    time.sleep(random.uniform(2, 4))
                                    xpath_code_input = (
                                        '//input[@placeholder="Nhập mã gồm 6 chữ số"]'
                        
                                    )
                                    
                                    if self.clickElement(By.XPATH, xpath_code_input, 15, False):
                                        input_field = self.driver.find_element(By.XPATH, xpath_code_input)
                                        self.human_type(input_field, code)
                                        time.sleep(random.uniform(2, 3))
                                        
                                        # --- NHẤN TIẾP (NEXT) ---
                                        xpath_next = (
                                            '//div[text()="Tiếp"]|//span[text()="Tiếp"]|//button[text()="Tiếp"]|'
                                            '//div[text()="Next"]|//span[text()="Next"]|//button[text()="Next"]'
                                        )
                                        self.clickElement(By.XPATH, xpath_next, 15, True)
                                        self.bypassCaptcha(5)
                                        if self.checkCookie():
                                            print(f"Đăng nhập thành công!")
                                            return True
                                else:
                                    print(f"✘ Không lấy được mã code từ EmailFake")
                            else:
                                return True
                            return False
                except Exception as e: 
                    error_detail = traceback.print_exc()
                    self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
                    time.sleep(random.randint(3,5))
                    
            except Exception as e: 
                error_detail = traceback.print_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
                time.sleep(random.randint(3,5))   

    def bypassCaptcha(self, count = 8):
        if self.settings['TaskSettings']['Wifi']:self.checkInternet()
        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🔍 Kiểm tra Captcha TikTok...', self.parent.tableWidget, COLORS.GREEN)
        for t in range(count):
            try:
                if self.clickElement(By.XPATH, '//span[text()="Không thể xác minh. Vui lòng thử lại."]|//span[text()="Đã xảy ra lỗi ngoài dự kiến. Vui lòng thử lại."]|//span[text()="Failed to load hashcash captcha"]|//span[text()="networkErrorText [5101] [500]"]', 3, True):
                    self.clickElement(By.ID, 'captcha_refresh_button', 1, True)
                    continue
                
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {t+1}/{count} ] [ {self.__typeStart} ] 🔄 Đang xử lý Captcha...', self.parent.tableWidget, COLORS.ORANGE)
                self.__pageSource = self.driver.page_source
                    
                if 'Kéo thanh trượt để ghép hình' in self.__pageSource or 'Drag the slider' in self.__pageSource:
                    time.sleep(1)
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🖱️ Đang Kéo thanh trượt để ghép hình...', self.parent.tableWidget, COLORS.BLACK)
                    self.koleso()
                    time.sleep(3)
                    continue
                
                elif 'Xác minh để tiếp tục' in self.__pageSource or 'Kéo mảnh ghép vào đúng vị trí' in self.__pageSource or 'Verify to continue' in self.__pageSource or 'Drag the puzzle' in self.__pageSource:
                    time.sleep(1)
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🔐 Xác minh để tiếp tục...', self.parent.tableWidget, COLORS.BLACK)
                    self.slider()
                    time.sleep(3)
                    continue
                    
                elif 'Chọn 2 đối tượng có hình dạng giống nhau' in self.__pageSource or 'Select 2 objects that are the same shape' in self.__pageSource:
                    time.sleep(1)
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🖼️ Chọn 2 đối tượng có hình dạng giống nhau...', self.parent.tableWidget, COLORS.BLACK)
                    self.choose()
                    time.sleep(3)
                    continue
            
                else:
                   
                    if t >= count:
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ✅ Kiểm tra Captcha hoàn tất!', self.parent.tableWidget, COLORS.OLIVE)
                        return True
                
                if self.clickElement(By.XPATH, "//div[text()='Select']|//*[text()='OK']|//*[text()='Đã hiểu']",1,True):
                    pass
                if self.clickElement(By.XPATH, '//div[@type="error"]|//a[@data-e2e="nav-profile"]|//div[contains(text(), "Tài khoản của bạn đã bị cấm")]', 1, False):
                    # self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🔔 {self.status}', self.parent.tableWidget, COLORS.GREEN)
                    self.status = ''
                    if self.clickElement(By.XPATH, "//div[contains(text(), 'Tài khoản của bạn đã bị cấm')]", 1, False):
                        self.status = 'Tài khoản của bạn đã bị đình chỉ.'
                    else:
                        try:
                            div_element  = self.driver.find_element(By.XPATH, "//div[@type='error']")
                            text = div_element.find_element(By.TAG_NAME, 'span').text
                            self.status = text
                            self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ❌ Lỗi: {self.status}', self.parent.tableWidget, COLORS.RED)
                            self.editCellByColumnName.emit(self.index, 'Status', str(self.status), self.parent.tableWidget, COLORS.RED)
                            time.sleep(3)
                        except:pass
         

                    if 'Rất tiếc, đã xảy ra lỗi, vui lòng thử lại sau' in self.status or 'Bạn truy cập dịch vụ của chúng tôi quá thường xuyên.' in self.status or 'Lỗi máy chủ' in self.status:
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ❌ Lỗi: {self.status} !!!', self.parent.tableWidget, COLORS.RED)
                        self.deleteProfile(type = 'hongxoa')
                        time.sleep(3)
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🚫 Tài khoản có vấn đề! Lý do: {self.status}!!!', self.parent.tableWidget, COLORS.BLUE)
                        time.sleep(5)
                        self.initJobBrowser()
                        return
                     
                    return False
           
            except Exception as e: 
                self.__typeStart = 'CAPTCHA'
                error_detail = traceback.print_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            # return False

    def download_image_base64(self, url_cap, path_img):
        image_base64 = self.driver.execute_script(
                    """
                    return fetch(arguments[0])
                        .then(response => response.blob())
                        .then(blob => new Promise((resolve, reject) => {
                            const reader = new FileReader();
                            reader.onloadend = () => resolve(reader.result.split(',')[1]);
                            reader.onerror = reject;
                            reader.readAsDataURL(blob);
                        }));
                    """, url_cap
                )
        with open(path_img, "wb") as file:
            file.write(base64.b64decode(image_base64))
        return path_img

    def koleso(self):
        try:
            cap1 = self.driver.find_elements(By.XPATH, "//img[@alt='Captcha']")[0].get_attribute("src")
            cap2 = self.driver.find_elements(By.XPATH, "//img[@alt='Captcha']")[1].get_attribute("src")
            
            if cap1.startswith('blob:'): 
                border_path = os.path.join(PATHCAPTCHA, f'koleso_border_{self.index+1}.png')
                inside_path = os.path.join(PATHCAPTCHA, f'koleso_inside_{self.index+1}.png')

                border = dow_img_the_same(self.download_image_base64(cap1, border_path))
                inside = dow_img_the_same(self.download_image_base64(cap2, inside_path))

            else:
                border = dow_img_the_same(cap1)
                inside = dow_img_the_same(cap2)
           
            def smooth_drag_captcha(element, distance, step_count=20):
                """
                Thực hiện kéo captcha slider mượt mà theo khoảng cách distance.
                
                Parameters:
                    element: Phần tử slider cần kéo.
                    distance: Khoảng cách cần kéo (pixel).
                    step_count: Số bước di chuyển (mặc định là 20).
                """
                self.actionChains.click_and_hold(element)
                # Tạo easing curve với hàm cosine: chuyển động chậm đầu, nhanh giữa, chậm cuối
                easing = (1 - np.cos(np.linspace(0, np.pi, step_count + 1))) / 2
                # Tính khoảng cách di chuyển ở từng bước dựa trên easing curve
                steps = np.diff(easing) * distance
                for step in steps:
                    # Di chuyển theo bước tính được, làm tròn để tránh sai số pixel
                    self.actionChains.move_by_offset(int(round(step)), 0)
                    # Pause nhỏ ngẫu nhiên để tăng tính tự nhiên
                    self.actionChains.pause(random.uniform(0.01, 0.10))
                self.actionChains.release().perform()

            # Tính toán khoảng cách kéo captcha
            value = Koleso(border, inside).main()
            el_do_dai = self.driver.find_element(By.XPATH, "//*[contains(@class, 'cap-rounded-full')]")
            el = self.driver.find_element(By.XPATH, "//*[contains(@class, 'secsdk-captcha-drag-icon')]")

            size_do_dai = el_do_dai.size
            size_nut = el.size
            do_dai = size_do_dai['width'] - size_nut['width']  # Khoảng cách tối đa có thể kéo
            value = do_dai / 180 * value

            # Sử dụng hàm kéo mượt với khoảng cách đã tính được
            smooth_drag_captcha(el, value)
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(random.randint(3,5))
            self.clickElement(By.ID, 'captcha_refresh_button', 1, True)
            logging.error('Có lỗi xảy ra khi giải captcha xoay', exc_info=True)
        
    def slider(self):
        try:
            _bg         = self.driver.find_element(By.XPATH, "//img[@id='captcha-verify-image']")
            _slice      = self.driver.find_element(By.XPATH, '//img[@alt="Captcha"]') 

            bg_src = _bg.get_attribute('src')
            if bg_src and bg_src.startswith('blob:'):
                bg_path    = os.path.join(PATHCAPTCHA, f'slider_bg_{self.index+1}.png')
                slice_path = os.path.join(PATHCAPTCHA, f'slider_slice_{self.index+1}.png')
                self.download_image_base64(_bg.get_attribute("src"), bg_path)
                self.download_image_base64(_slice.get_attribute("src"), slice_path)

            else:
                self.editCellByColumnName.emit(self.index, 'Status', f'Báo admin để lấy xpath của IMG này!!!',self.parent.tableWidget, COLORS.RED)
                time.sleep(5)
                return False

            resultCapt = int(Slider(bg_path, slice_path).get_position() * 0.5) - 20
            
            el = self.driver.find_element(By.ID, "captcha_slide_button")
            if int(resultCapt) == 0:
                self.clickElement(By.ID, 'captcha_refresh_button', 1, True)
                return False
            
            def smooth_drag_captcha(element, distance, step_count=5):
                """
                Thực hiện kéo captcha slider mượt mà theo khoảng cách distance.

                Parameters:
                    element: Phần tử cần kéo (WebElement).
                    distance: Khoảng cách cần kéo (pixel).
                    step_count: Số bước di chuyển để đảm bảo mượt mà.
                """
                self.actionChains.click_and_hold(element)
                
                # Tạo easing curve với hàm cosine để di chuyển mượt mà
                easing = (1 - np.cos(np.linspace(0, np.pi, step_count + 1))) / 2
                steps = np.diff(easing) * distance  # Tính khoảng cách di chuyển cho từng bước

                for step in steps:
                    self.actionChains.move_by_offset(int(round(step)), 0)
                    self.actionChains.pause(random.uniform(0.3,0.35))  # Dừng ngẫu nhiên để tránh bị phát hiện

                self.actionChains.release().perform()

            smooth_drag_captcha(el, resultCapt)
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(random.randint(3,5))
            self.clickElement(By.ID, 'captcha_refresh_button', 1, True)
            logging.error('Có lỗi xảy ra khi giải captcha kéo', exc_info=True)
 
    def choose(self):
        try:
            logging.debug('Chọn 2 đối tượng có hình dạng giống nhau')
            path_img = os.path.join(PATHCAPTCHA, f'choose_{self.index+1}.png')
            if os.path.exists(path_img): os.remove(path_img)

            url_cap = None
            xpath = self.driver.find_elements(By.XPATH, '//img')
            for img in xpath:
                src = img.get_attribute("src")
                if 'captchaOpti_hCaptchaModal1_header' in img.get_attribute("alt") or 'rc-captcha' in src or 'blob' in src or 'data:image' in src:
                    url_cap = src
                    break
            
            if not url_cap:
                try:
                    url_cap = self.driver.execute_script("""
                        const urls = [];
                        document.querySelectorAll("img").forEach(img => {
                            if (img.src.startsWith("blob:")) urls.push(img.src);
                        });
                        return urls;
                    """)
                    if url_cap == []:
                        url_cap = None
                    url_cap = url_cap[0]
                        
                except:pass

            if not url_cap:
                self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ❌ Captcha image not found!!!", self.parent.tableWidget, COLORS.RED)
                time.sleep(1)
                return
            
            logging.debug('Chọn 2 đối tượng có hình dạng giống nhau [Download]')
            if url_cap.startswith('blob:'): 
                self.download_image_base64(url_cap, path_img)
            elif url_cap.startswith('data:image'):
                save_base64_image(url_cap, path_img)
            else:
                path_img = save_image_from_url(url_cap, PATHCAPTCHA, f'choose_{self.index+1}.png')
            logging.debug('Chọn 2 đối tượng có hình dạng giống nhau [Get Pos]')
            el =  self.driver.find_element('xpath', f"//img[@src='{url_cap}']")

          
            w, h = -el.size["width"], el.size["height"]
            processor = Choose(cv2.imread(path_img))
            point_1, point_2 = processor.solve(el.size['width'], el.size['height'])
            print(point_1, point_2)
            for x, y in [point_1, point_2]:
                self.actionChains.move_to_element_with_offset(el, w/2, h/2).move_by_offset(x, -h+y).click().perform()
                time.sleep(random.uniform(0.1, 1))

            for text in ["Xác nhận", "Confirm"]:
                if self.clickElement(By.XPATH, f'//div[text()="{text}"]', 1, True):
                    break
            if os.path.exists(path_img): os.remove(path_img)
            return True
        except Exception as e: 
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
            time.sleep(random.randint(3,5))
            self.clickElement(By.ID, 'captcha_refresh_button', 1, True)
            logging.error('Có lỗi xảy ra khi giải captcha chọn', exc_info=True)

    def public(self):
        self.editCellByColumnName.emit(
            self.index, 
            'Status', 
            f'🌍 Đang công khai danh sách đã thích cho tài khoản @{self.uid}...', 
            self.parent.tableWidget, 
            COLORS.GREEN
        )
        user_agent_mb = 'com.ss.android.ugc.trill/995 (Linux; U; Android 7.1.2; en_US; ASUS_Z01QD; Build/N2G48H; Cronet/77.0.3844.0)'
        url_open_tym = 'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/set/settings/?field=favorite_permission&value=0&os_api=25&device_type=ASUS_Z01QD&ssmix=a&manifest_version_code=995&dpi=240&carrier_region=VN&uoo=0&region=US&uuid=841023267387228&app_skin=white&app_name=trill&version_name=9.9.5&timezone_offset=-21600&ts=1664613812&ab_version=9.9.5&residence=VN&pass-route=1&pass-region=1&is_my_cn=0&current_region=VN&ac2=wifi&app_type=normal&ac=wifi&channel=googleplay&update_version_code=9950&_rticket=1664613812700&device_platform=android&iid=7149451393853081346&build_number=9.9.5&locale=en&op_region=VN&version_code=995&timezone_name=America%2FChicago&openudid=06ca0f001df50f81&sys_region=US&device_id=7149449994248144386&app_language=en&resolution=720*1280&device_brand=Asus&language=en&os_version=7.1.2&aid=1180&mcc_mnc=45204'
        url_open_tym_us = 'https://api16-normal-useast5.us.tiktokv.com/aweme/v1/user/set/settings/?field=favorite_permission&value=0&os_api=25&device_type=ASUS_Z01QD&ssmix=a&manifest_version_code=995&dpi=240&carrier_region=VN&uoo=0&region=US&uuid=841023267387228&app_skin=white&app_name=trill&version_name=9.9.5&timezone_offset=-21600&ts=1664613812&ab_version=9.9.5&residence=VN&pass-route=1&pass-region=1&is_my_cn=0&current_region=VN&ac2=wifi&app_type=normal&ac=wifi&channel=googleplay&update_version_code=9950&_rticket=1664613812700&device_platform=android&iid=7149451393853081346&build_number=9.9.5&locale=en&op_region=VN&version_code=995&timezone_name=America%2FChicago&openudid=06ca0f001df50f81&sys_region=US&device_id=7149449994248144386&app_language=en&resolution=720*1280&device_brand=Asus&language=en&os_version=7.1.2&aid=1180&mcc_mnc=45204'

        headers_tym = {
            'Cookie': self.cookieChrome,
            'User-Agent': user_agent_mb,
            'sdk-version':'1',
            'x-khronos':'1664613812',
            'x-ss-req-ticket':'1664613812698',
            'x-gorgon':'040120b94001dd2be7abff1f0507e32b7a9570ab0d00833543d9',
        }
        if 'store-country-code=us' in self.cookieChrome:
            logging.debug(requests.get(url_open_tym_us, headers=headers_tym).text)
        else:
            logging.debug(requests.get(url_open_tym, headers=headers_tym).text)

    def getPathImages(self):
        filePng = []
        for t in range(3):
            try:
                for root, dirs, files in os.walk(r'{}'.format(PATHDATA+'\\avatar')):
                    for file in files:
                        if file.endswith('.png'):
                            filePng.append(file)
                        elif file.endswith('.jpg'):
                            filePng.append(file)
                        elif file.endswith('.jpge'):
                            filePng.append(file)
                try:
                    return r"{}/{}".format(PATHDATA+'\\avatar', random.choice(filePng))
                except:pass
            except Exception as e:pass
        return False

    def merge_9_grid_temp(self, folder_path):
        import os
        import random
        from PIL import Image, ImageOps
        import tempfile
        valid_ext = [".jpg", ".jpeg", ".png", ".webp"]
        files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_ext]

        selected = random.sample(files, 9)

        bg = Image.open(os.path.join(folder_path, selected[0])).convert("RGB")
        W, H = bg.size
        final = bg.copy()

        cell_w = W // 3
        cell_h = H // 3

        imgs = [
            ImageOps.fit(Image.open(os.path.join(folder_path, f)).convert("RGB"), (cell_w, cell_h))
            for f in selected
        ]

        positions = [(c * cell_w, r * cell_h) for r in range(3) for c in range(3)]

        for img, pos in zip(imgs, positions):
            final.paste(img, pos)

        # tạo file tạm
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        final.save(tmp.name)
        tmp.close()

        return tmp.name  # trả file tạm để send_keys()

    def uploadAvt(self):
        # self.adjustWindow("restore")
        self.__typeStart = 'AVT'
        for t in range(3):
            self.bypassCaptcha(30)
            try:
                self.editCellByColumnName.emit(
                    self.index, 
                    'Status', 
                    f'🖼️ Đang cập nhật ảnh đại diện cho tài khoản @{self.uid}...', 
                    self.parent.tableWidget, COLORS.GREEN
                )
                self.driver.get('https://www.tiktok.com/profile');self.driver.set_page_load_timeout(10);time.sleep(3)
                self.clickElement(By.XPATH, '//button[text()="Đã hiểu"]|//div[text()="Đã hiểu"]|//span[text()="Đã hiểu"]',1, True)
                if self.clickElement(By.XPATH, '//button[@data-e2e="edit-profile-entrance"]|//div[text()="Sửa hồ sơ"]|//button[text()="Sửa hồ sơ"]|//span[text()="Sửa hồ sơ"]',15, True):
                    time.sleep(1)
                    avatar_folder = os.path.join(PATHDATA, "Images\\avatar")
                    self.pathAvt = self.merge_9_grid_temp(avatar_folder)
                    print(self.pathAvt)
                    self.driver.find_element(By.XPATH, "//input[contains(@class, 'InputUpload')]|//input[@type='file']").send_keys(self.pathAvt);time.sleep(2)
                    if self.clickElement(By.XPATH, '//button[text()="Apply"]|//button[text()="Đăng ký"]|//button[text()="Xác nhận"]',3, True):pass
                    if self.clickElement(By.XPATH, '//*[@data-e2e="edit-profile-save"]',5, True):
                        time.sleep(1)
                        self.clickElement(By.XPATH, '//*[@data-e2e="set-username-popup-confirm"]',5, True)
                        self.editCellByColumnName.emit(
                            self.index, 'Status', f'🖼️ Tài khoản @{self.uid} cập nhật thành công ảnh đại diện {self.pathAvt}.', self.parent.tableWidget, COLORS.GREEN)
                        time.sleep(5)
                        return True
            
            except Exception as e: 
                error_detail = traceback.format_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ERROR({error_detail})', self.parent.tableWidget, COLORS.RED)
                time.sleep(random.randint(5,8))
        return False
   
    def fetchInfo(self):
        global LOGIN_ACCOUNT
        try:
            for _ in range(3):
                self.__typeStart = 'FECT'
                if self.settings['TaskSettings']['Wifi']:self.checkInternet()
                if self.checkCookie():self.editCellByColumnName.emit(self.index, 'Status', f'⏳ Đăng nhập tài khoản TikTok [ {self.uid} ] thành công.',self.parent.tableWidget, COLORS.GREEN);return True
                self.__updateValue()
                # self.changeProxy('proxyOn');self.driver.set_page_load_timeout(30);time.sleep(1)
                
                if len(self.uid) >= 5 and len(self.pwd) >= 5:
                    self.loginAccount()
                else:
                    self.editCellByColumnName.emit(self.index, 'Status', f'❌ Tài khoản {self.uid} không hợp lệ!',self.parent.tableWidget, COLORS.BLUE)
                    self.__updateValue()
                    time.sleep(3);self.stopMining.emit(self.index)
                    return

                if self.checkCookie():self.editCellByColumnName.emit(self.index, 'Status', f'⏳ Đăng nhập tài khoản TikTok [ {self.uid} ] thành công.',self.parent.tableWidget, COLORS.GREEN);return True
                else:
                    try:
                        LOGIN_ACCOUNT.remove(self.index)
                    except:pass
                    # wait = random.randint(120,180)
                    # self.editCellByColumnName.emit(self.index, 'Status', f'❌ Đăng nhập tài khoản TikTok [ {self.uid} ] thất bại liên tiếp tiếp tục sau {wait}seconds!',self.parent.tableWidget, COLORS.GREEN)
                    # time.sleep(wait)
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ Đăng nhập tài khoản TikTok [ {self.uid} ] thất bại liên tiếp!!!',self.parent.tableWidget, COLORS.GREEN)
            time.sleep(0.5);self.stopMining.emit(self.index);time.sleep(1)
        except:pass
        return False
  
    def performAction(self):
        global LIST_CLICK
        for i in range(2):
            try:

                # Thử load URL với retry
                load_success = False
                for attempt in range(2):
                    self.__hide = 0
                    try:
                        self.driver.set_page_load_timeout(15)
                        self.driver.get(self.__link)
                        current = self.driver.current_url
                        print('Link là:',current)
                        if '@' in current:
                            m = re.search(r'/@([^/?]+)', current)
                            self.userjob = m.group(1) if m else None
                            self.driver.get(f'https://www.tiktok.com/search?q={self.userjob}&t=1766756391609')
                        load_success = True
                        break
                        
                    except Exception as e:
                        print(f"DEBUG: Thread {self.index} failed to load URL (attempt {attempt + 1}/2): {e}")
                        logging.error(f'ERROR {self.__link.upper()}', exc_info=True)
                        open('job_error.txt', 'a+', encoding='utf-8').write(f'{self.__typeStart}|{self.__link}\n')
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ❌ Chuyển link thất bại (lần {attempt + 1}/2): {self.__typeJob.upper()} | URL({self.__link}) | ERROR({e})', self.parent.tableWidget, COLORS.RED)
                        time.sleep(random.randint(2, 3))
                        self.__typePerError = 'Chuyển đến URL thất bại!!!'
                        
                # Remove thread sau khi hoàn thành load URL (thành công hoặc thất bại)
                if not load_success:
                    return True
                self.__dalam.append(self.__link)
                        
                # if self.clickElement(By.XPATH, "//div[contains(@class, 'css-u2vwc1-DivErrorWrapper')]|//*[text()='Đây là tài khoản riêng tư']|//*[text()='Video hiện không khả dụng']|//*[text()='Không thể xem video này tại quốc gia hoặc khu vực của bạn']v|//*[text()='Không thể tìm thấy tài khoản này']", 1, False):
                if self.clickElement(By.XPATH, "//*[text()='Không thể tìm thấy tài khoản này']", 1, False):
                    open('job_die.txt', 'a+', encoding='utf-8').write(f'{self.__typeStart}|{self.__link}\n')
                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Video hiện không khả dụng. Bạn đang tìm kiếm video? Hãy thử duyệt tìm các tác giả, hashtag và âm thanh thịnh hành của chúng tôi.', self.parent.tableWidget, COLORS.RED)
                    time.sleep(1)
                    self.__typePerError = 'Job không tồn tại!!!'
                    return False
                
                
                time.sleep(1)
                if 'love' in self.__typeJob:
                    try:
                        
                        try:
                            if self.clickElement(By.XPATH, '//*[@data-e2e="browse-username"]', 5, False):
                                titleUser = self.driver.find_element(By.XPATH, f'//*[@data-e2e="browse-username"]').text
                            else:
                                titleUser = ''
                                time.sleep(3)
                        except:
                            titleUser = ''
                            time.sleep(3)
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🕵️ Đang kiểm tra Status nút yêu thích của người dùng "{titleUser}"...', self.parent.tableWidget, COLORS.GREEN)
                        
                        if "rgb(254,44,85)" in self.driver.page_source:
                            self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Video đã làm, trùng lặp video', self.parent.tableWidget, COLORS.RED)
                            return True
                 
                        # Thực hiện like
                        for i in range(3):
                            try:
                                if self.clickElement(By.XPATH, "//*[@data-e2e='like-icon']|//*[@data-e2e='detail-photo']|//video", 5, False):
                                    body = self.driver.find_element(By.TAG_NAME, "body")
                                    
                                    # self.actionChains.move_to_element(body).click().send_keys('l').pause(0.2).double_click().perform()
                                    # self.actionChains.move_to_element(body).double_click().perform()   
                                    
                                    self.actionChains.move_to_element(body).pause(0.5).double_click().perform()
                                    break
                            except:
                                try:
                                    self.driver.find_element(By.XPATH, f"//*[@data-e2e='like-icon']").click()
                                    break
                                except:
                                    continue
                           
                        self.__typePerError = 'Nhấn yêu thích thành công.'
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🎉 Thành công! Đã yêu thích video của người dùng "{titleUser}".', self.parent.tableWidget, COLORS.GREEN)
                        time.sleep(1)
                        return True
                        
                    except Exception as e:
                        print(f"DEBUG: Thread {self.index} exception in love job: {e}")
                        logging.error(traceback.print_exc())
                        self.__hide = 1
                        self.bypassCaptcha(5)
                        return True
          
                elif 'follow' in self.__typeJob:
                    try:
                        print('User Job:',self.userjob)
                        self.bypassCaptcha(5)
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🕵️ Đang kiểm tra Status nút theo dõi...', self.parent.tableWidget, COLORS.GREEN)
                        if self.clickElement(By.XPATH,'//*[text()="Bạn không có tài khoản?"]|//*[text()="Bạn đã có tài khoản?"]|(//div[normalize-space(text())="Đăng nhập"])[1]',1,False):
                            self.fetchInfo()
                            return False
          
                        xpath_profile = f'//a[starts-with(@href, "/@{self.userjob}?") or @href="/@{self.userjob}"]'
                        print('Xpath Profile',xpath_profile)
                        if self.clickElement(By.XPATH, xpath_profile, 4, True):
                        
                            if self.clickElement(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/button/div/div[2]", 1, False):
                                print(f'[ {self.__typeStart} ] Người dùng @{self.userjob} đã được theo dõi từ trước.')
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Người dùng @{self.userjob} đã được theo dõi từ trước.', self.parent.tableWidget, COLORS.OLIVE)
                                time.sleep(1)
                                return True
                            if self.clickElement(By.XPATH, "//div[@id='main-content-others_homepage']//p[contains(., 'riêng tư')]", 1, False):
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Người dùng @{self.userjob} đây là tài khoản riêng tư.', self.parent.tableWidget, COLORS.BLACK)
                                time.sleep(1)
                                return True
                            if self.clickElement(By.XPATH, "//div[text()='Follow']|//button[text()='Follow']", 5, False):
                                el = self.driver.find_element(
                                    By.XPATH, "//div[text()='Follow']|//button[text()='Follow']"
                                )
                                self.actionChains.move_to_element(el).pause(0.2).click().perform()
                        
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🎉 Theo dõi thành công {self.__link}', self.parent.tableWidget, COLORS.GREEN)
                                print(f"Theo dõi thành công {self.__link}")
                                self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🎉 Thành công! Đã theo dõi tài khoản.', self.parent.tableWidget, COLORS.GREEN)
                                time.sleep(1)
                                return True
                       
                        if self.clickElement(By.XPATH, "//span[text()='Người dùng']|//div[text()='Người dùng']|//button[text()='Người dùng']", 1, True):
                            time.sleep(3)
                            for _ in range(3):
                                if self.clickElement(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/button/div/div[2]", 1, False):
                                    print(f'[ {self.__typeStart} ] Người dùng @{self.userjob} đã được theo dõi từ trước.')
                                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Người dùng @{self.userjob} đã được theo dõi từ trước.', self.parent.tableWidget, COLORS.OLIVE)
                                    time.sleep(1)
                                    return True
                                if self.clickElement(By.XPATH, "//div[@id='main-content-others_homepage']//p[contains(., 'riêng tư')]", 1, False):
                                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Người dùng @{self.userjob} đây là tài khoản riêng tư.', self.parent.tableWidget, COLORS.BLACK)
                                    time.sleep(1)
                                    return True
                                if self.clickElement(By.XPATH, xpath_profile, 4, True):
                                    el = self.driver.find_element(
                                        By.XPATH, "//div[text()='Follow']|//button[text()='Follow']"
                                    )
                                    self.actionChains.move_to_element(el).pause(0.2).click().perform()
                            
                                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🎉 Theo dõi thành công {self.__link}', self.parent.tableWidget, COLORS.GREEN)
                                    print(f"Theo dõi thành công {self.__link}")
                                    self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🎉 Thành công! Đã theo dõi tài khoản.', self.parent.tableWidget, COLORS.GREEN)
                                    time.sleep(1)
                                    return True
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] Không tìm thấy xpath Follow nào cả báo admin ngay lập tức!!!', self.parent.tableWidget, COLORS.GREEN)
                        time.sleep(3)
                        return True
                    except Exception as e:
                        print(f"DEBUG: Thread {self.index} exception in follow job: {e}")
                        logging.error(traceback.print_exc())
                        self.__hide = 1
                        self.bypassCaptcha(5)
                    return False
                
            except Exception as e:
                print(f"DEBUG: Thread {self.index} unexpected error: {e}")
                return True
            
    def js_click(self, element):
        """JavaScript click với error handling"""
        try:
            # Scroll element vào view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.3)
            
            # Click bằng JavaScript
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"JS click failed: {e}")
            return False       
    
    def startTTC1(self):
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
                logging.debug(f"{getXu} - {self.id_storage_ttc.rstrip(',')}")
                # formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # with open('logs.txt', 'a+', encoding='utf-8') as f:
                #     f.write(f'{formatted_datetime}: UID: {self.uid.upper()} | JOB_ID: {self.id_storage_ttc} | {getXu["mess"]} | {self.__typePerError} | TTC1\n')
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
                        # self.__updateValue()
                        self.deleteProfile(type='xoa')
                        time.sleep(5)
                        self.addCookie()
                        self.fetchInfo()
                        # self.initJobBrowser()
                        return
                    elif 'Bạn cần thêm nick vào hệ thống trước khi đặt' in getXu['mess']:
                        datnick = self.__apituongtaccheo.datNick(self.uid)
                        if datnick['status'] == 'error':
                            self.status = datnick['mess']
                            self.editCellByColumnName.emit(self.index, 'Status', str(self.status), self.parent.tableWidget, COLORS.RED)
                            time.sleep(0.5)
                            self.stopMining.emit(self.index)
                            time.sleep(1)
                            return
                    elif 'Bạn đã theo dõi' in getXu['mess']:
                        self.id_storage_ttc = ''

                    elif 'Vui lòng làm trên 8 nhiệm vụ mới nhận xu' in getXu['mess']:
                        self.editCellByColumnName.emit(self.index, 'Status', str(getXu['mess']), self.parent.tableWidget, COLORS.RED);time.sleep(0.5)
                        return
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
                        done = xu // (500 if 'love' in self.__typeJob else 1000)

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
                self.__startTTC1 = time.time()
                self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
                # self.__typeJob = 'love'
                self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
                # jobs = self.__apituongtaccheo.getJob(self.__typeJob)
                # logging.debug(jobs)
                # if 'spam sẽ văng tài khoản, đi làm nhiệm vụ khác quay lại sau!' in str(jobs):
                #     self.editCellByColumnName.emit(self.index, 'Status', str(jobs['error']), self.parent.tableWidget, COLORS.GREEN);
                #     if 'countdown' in str(jobs):
                #         self.countdownTTC1 = int(jobs['countdown'])
                #     return
                # "Chức năng get job spam"
              
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
                except:return
                logging.debug(jobs)
                self.total_jobs = len(jobs)
                for index, job in enumerate(jobs, start=1):
                    self.remaining_jobs = self.total_jobs - index
                    self.cache_count = len([x for x in self.id_storage_ttc.split(',') if x])
                    self.editCellByColumnName.emit(self.index, 'Status', f'Cache: {self.cache_count}-[ {self.__typeStart} ] 🚀 Bắt đầu nhiệm vụ loại: {self.__typeJob.upper()} ({index}/{self.total_jobs}) | Còn lại {self.remaining_jobs} nhiệm vụ...', self.parent.tableWidget, COLORS.GREEN)
                    self.__job_id, self.__link = job['idpost'], job['link']
                    self.userjob = self.__link
      
                    
                    # self.__link = f'https://www.tiktok.com/share/user/{self.idaccount}' 
                    self.__link = f'https://www.tiktok.com/search?q={self.userjob}&t=1766756391609' 
                    # if '@' not in self.__link: 
                    #     self.__link = self.url_tiktok+'@'+self.__link
                    #     self.link = f'https://m.tiktok.com/v/{self.__job_id}.html'
                    # else:

                    #     # self.__link1 = self.__link + '/' + self.__link
                    #     # self.__link2 = self.__link + '/' + self.__link + '/' + self.__job_id
                    #     # self.__link3 = 'https://www.tiktok.com/@' + self.__link + '/' + self.__link
                    #     self.__link4 = 'https://www.tiktok.com/@' + self.__link + '/' + self.__link + '/' + self.__job_id
                    #     # all_links    = [self.__link1, self.__link2, self.__link3, self.__link4]
                    #     # self.__link  = random.choice(all_links)
                    #     self._linkTop= self.link = f'https://m.tiktok.com/v/{self.__job_id}.html'
                    #     # self.__link = self.__link4
                    #     self.__link = 'https://www.tiktok.com/@' + self.__link

                    
                    if self.__link in self.__dalam:
                        self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] ⚠️ Nhiệm vụ ID {self.__job_id} đã hoàn thành trước đó! Bỏ qua nhiệm vụ này..." ,self.parent.tableWidget, COLORS.RED);time.sleep(1);continue


                    self.editCellByColumnName.emit(self.index, 'ToTal', str(self.total),self.parent.tableWidget, COLORS.GREEN)
                    self.editStatus.emit('jobs', '', 1)
                    if self.performAction():
                        self.id_storage_ttc += self.__job_id + ','
                        self.total += 1
                        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                        
                        if len(self.id_storage_ttc.split(',')) > self.settings['DelaySettings']['Cache']:
                            self.configureDelay('GetCoin')
                            nhanTienTTC1()
                    # else:
                    #     self.id_storage_ttc += self.__job_id + ','
                    # if self.total_jobs >= 5:
                    #     self.configureDelay('wait', delay=5)

                    self.configureDelay('NextJob')
                  
                if len(self.id_storage_ttc.split(',')) > self.settings['DelaySettings']['Cache']:
                    self.configureDelay('GetCoin')
                    nhanTienTTC1()
                # try:
                #     seconds = int(round(time.time() - self.__startTTC1, 1))
                #     self.editCellByColumnName.emit(self.index, 'Status', f"Cache: {self.cache_count}-[ {self.__typeStart} ] ✅ Hoàn thành toàn bộ {self.total_jobs} nhiệm vụ {self.__typeJob.upper()} trong {seconds} giây! 🚀", self.parent.tableWidget, COLORS.GREEN)
                #     if self.countdownTTC1 >= seconds:
                #         self.countdownTTC1 = self.countdownTTC1 - seconds
                #         # self.configureDelay('countdown', int(self.countdown))
                # except:traceback.print_exc()
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
                getXu = self.__apituongtaccheo2.getXu('love2', self.id_storage_ttc2.rstrip(','))
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
                    done = xu // (500 if 'love' in self.__typeJob else 1400)

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
                        datnick = self.__apituongtaccheo2.datNick(self.uid)
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
                    getXu = self.__apituongtaccheo2.getXu('love2', self.id_storage_ttc2.rstrip(','))
                    logging.debug(f"{getXu} - {self.id_storage_ttc2.rstrip(',')}")
                    
                self.editCellByColumnName.emit(self.index, 'Status', str(getXu['mess']), self.parent.tableWidget, COLORS.GREEN);time.sleep(3)
        
            try:
                self.__typeStart = 'TTC2'
                # self.__startTTC2 = time.time()
                self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
                self.__typeJob = 'love2'
                self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
                for i in range(4):
                    jobs = self.__apituongtaccheo2.getJob('love2')
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
                self.__job_id, self.__link = job['id'], job['link']
                
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
                                self.tyle = int(getXu['data']['xu_them'] / (8 * (500 if 'love' in self.__typeJob else 1400)) * 100)
                                self.editCellByColumnName.emit(self.index, 'Rate', f'{self.tyle}% V1', self.parent.tableWidget, COLORS.GREEN)
                                self.editCellByColumnName.emit(self.index, 'Job Info', str(self.dict_xuthem), self.parent.tableWidget, COLORS.GREEN)
                                self.editCellByColumnName.emit(self.index, 'Status', f"Thành công, bạn được cộng {getXu['data']['xu_them']} xu", self.parent.tableWidget, COLORS.GREEN)
                            
                delay_time = random.randint(6,9)
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
                self.deleteProfile()
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
                getXu = self.__apitanglikecheo.guiDuyet(self.__job_id,self.__typeJob, 0)
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
                self.__job_id, self.__link = job['job_id'], job['link']
                if self.__link in self.__dalam:
                    guiDuyet = self.__apiMIN.guiDuyet(self.__job_id, self.__typeJob, self.__hide)
                    self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] ⚠️ Nhiệm vụ ID {self.__job_id} đã được hoàn thành hoặc bỏ qua trước đó. Tiếp tục với nhiệm vụ tiếp theo...", self.parent.tableWidget, COLORS.RED)
                    return 
                if self.__typeJob == 'love':
                    self.__link = self.__link + '/' + self.__link
                else: self.__link = self.__link
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
        try:
            self.__typeStart = 'TIKTOP'
            self.editCellByColumnName.emit(self.index, 'Status', f"[ {self.__typeStart} ] 🔄 Đang nhận nhiệm vụ {self.__typeJob.upper()}... Vui lòng chờ!", self.parent.tableWidget, COLORS.GREEN)
            jobs = self.__apitiktop.getJob(1 if self.__typeJob == 'love' else 2)
            logging.debug(jobs)
            if jobs['status'] == 'success':

                self.__job_id, self.__link = jobs['task_execution_id'], jobs['links'][0]

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
                
                result = self.performAction()
                if result is True or result is False:
                    self.total += 1
                    for _ in range(5):
                        getXu = self.__apitiktop.guiDuyet(self.__job_id, 'check')
                        logging.debug(getXu)
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
                            self.editCellByColumnName.emit(self.index, 'Status', str(check), self.parent.tableWidget, COLORS.GREEN)
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
            try:
                self.proxyrq = open('proxy_requests.txt','r',encoding='utf-8').read().strip().split('\n')[self.index]
            except:self.proxyrq = ''
            self.__typeStart = 'ALL'
            try:
                if self.fetchInfo():
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
                                
                                self.__apituongtaccheo = TTC(access_token = self.token)
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
                                if 'Vui lòng thay avatar, ảnh này đã được sử dụng quá nhiều lần.' in str(cauHinhNoCaptcha):
                                    if self.uploadAvt():
                                        time.sleep(15)
                                        self._upload +=1
                                        if self._upload >=1:
                                            self.editCellByColumnName.emit(self.index, 'Status', f'[ TDSV1 ] ⚠️ Quá nhiều lần tải ảnh đại diện thất bại, bỏ qua cấu hình TDSV1 cho tài khoản {self.uid}.',self.parent.tableWidget, COLORS.RED)
                                            self.dict_add['tdsv1'] = True
                                            time.sleep(5)
                                            return
                                    return
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
                                    if 'change default avatar' in str(self.datniktiktop):
                                        self.uploadAvt()
                                        time.sleep(15)
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
                    self.__typeJob = 'follow'
                    self.__link = 'https://www.tiktok.com/@viplikemxh'
                    self.performAction()
                    # self.driver.get('https://www.tiktok.com/@viplikemxh');self.driver.set_page_load_timeout(30);time.sleep(3)
                    while True:
                        if self.fetchInfo():
                            try:
                                for t in range(20):
                                    # self.adjustWindow('minimize')
                                    
                                    if self.total >= 100 and self.dict_xuthem['ttc'] <= 500 and self.dict_xuthem['tdsv1'] <= 500 and self.dict_xuthem['tlc'] <= 6 and self.dict_xuthem['min'] <= 5:
                                        self.status = f'50 Mission failed | {self.dict_xuthem}'
                                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {self.status}', self.parent.tableWidget, COLORS.RED)
                                        self.__updateValue()
                                        time.sleep(3)
                                        self.deleteProfile()
                                        time.sleep(5)
                                        self.initJobBrowser()
                                        return
                                    if self.check_add_roi == 1:
                                        self.check_add_roi = 0
                                        self.status = f'Nick Da add bởi user khác'
                                        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {self.status}', self.parent.tableWidget, COLORS.RED)
                                        self.__updateValue()
                                        time.sleep(3)
                                        self.deleteProfile()
                                        time.sleep(5)
                                        self.initJobBrowser()
                                        return
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
                                                print('Nhiệm vụ chọn là:',self.__typeJob)
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
                                if self.__apituongtaccheo2.infoAccount()['user'] == '':
                                    self.editCellByColumnName.emit(self.index, 'Status', f'Tài khoản TTC2 bị đăng xuất!!!',self.parent.tableWidget, COLORS.RED)
                                    self.dict_add['ttc2'] = False
                                    time.sleep(5)
                            except:pass
                            time.sleep(5)
                else:
                    if self.uid == '':
                        self.editCellByColumnName.emit(self.index, 'Status', f'Tài khoản bị đăng xuất !!!',self.parent.tableWidget, COLORS.RED)
                        time.sleep(3)
                        self.deleteProfile()
                        time.sleep(3)
                        self.initJobBrowser()
                    self.editCellByColumnName.emit(self.index, 'Status', f'Không thể kiểm tra, đăng nhập tài khoản {self.uid} liên tiếp nhiều lần.', self.parent.tableWidget, COLORS.RED)
                    time.sleep(random.randint(60,120))
                    
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
        # self.editCellByColumnName.emit(self.index, 'ToTal', '',self.parent.tableWidget, COLORS.GREEN)
        self.editCellByColumnName.emit(self.index, 'Rate', '',self.parent.tableWidget, COLORS.GREEN)
        self.editCellByColumnName.emit(self.index, 'Job Info', '',self.parent.tableWidget, COLORS.GREEN)

        if self.uid == '':
            while True:
                try:
                    self.user_data = requests.get('https://pytournes.io.vn/api/get_users.php?count=1&admin_type=dtoandomain').json()
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
                        
                    else:
                        self.editCellByColumnName.emit(self.index, 'Status', str(self.user_data['message']), self.parent.tableWidget, COLORS.RED)
                        time.sleep(1);self.stopMining.emit(self.index);time.sleep(1)
                except Exception as e:
                    self.editCellByColumnName.emit(self.index, 'Status', f"💥 Lỗi khi lấy user: {str(e)}", self.parent.tableWidget, COLORS.RED)
                    pass
                time.sleep(random.randint(15,30))
        self.__updateValue();time.sleep(1)
        if 'sessionid' in self.cookieChrome:
            if len(self.cookieChrome) >= 50:
                self.sessionid = "sessionid=" + self.cookieChrome.split("sessionid=")[1].split(";")[0].strip()
            else:
                self.sessionid = self.cookieChrome
            self.addCookie()

        self.settings = json.loads(open(PATHSETTINGS, 'r', encoding="utf-8-sig").read())
        self.startALL()

    def run(self):  
        while True:
            if len(LOGIN_ACCOUNT) >= 5:
                self.editCellByColumnName.emit(self.index, 'Status', 'Đợi các luồng khác khởi động và đăng nhập tài khoản hoàn tất...', self.parent.tableWidget, COLORS.RED);time.sleep(3)
                time.sleep(1)
                continue    
            LOGIN_ACCOUNT.append(self.index)
            for i in range((len(LOGIN_ACCOUNT) -1)*15, 0, -1):
                self.editCellByColumnName.emit(self.index, 'Status', f'🔎 Đã tìm thấy slot trống! Trình duyệt sẽ khởi động sau {i} giây...', self.parent.tableWidget, COLORS.ORANGE)
                time.sleep(1)
            break
        
        if self.openBrowser():
            self.initJobBrowser()
      

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

    def adjustWindow(self, mode="restore"):
        if mode == "restore":
            self.driver.set_window_rect(self.xChrome, self.yChrome, self.wChrome, self.hChrome)

        elif mode == "minimize":
            if self.driver.get_window_size()['width'] >= 100:
                self.driver.minimize_window()

    def human_type(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3)) # Gõ như người thật

    def getCookie(self):
        try:
            self.cookieChrome = ""
            ck_get = self.driver.get_cookies()
            for value in ck_get:
                self.cookieChrome+=value['name']+'='+value['value']+";"
        except:self.cookieChrome = ''
    
    def checkCookie(self):
        try:
            self.clickElement(By.XPATH, '//button[text()="Thử lại"]|//div[text()="Thử lại"]|//span[text()="Thử lại"]|//button[text()="Đã hiểu"]|//div[text()="Đã hiểu"]|//span[text()="Đã hiểu"]', 1, True)
            self.__typeStart = 'COOKIE'
            if self.settings['TaskSettings']['Wifi']:self.checkInternet()
            self.getCookie()
            self.editCellByColumnName.emit(self.index, 'Status',  f'Kiểm tra bằng Page Source! (UID: {self.uid})', self.parent.tableWidget, COLORS.GREEN)
            try:
                if str(self.uid) not in str(self.driver.current_url):
                    self.driver.get(self.url_tiktok+'profile');self.driver.set_page_load_timeout(30)
                response        = self.driver.page_source
                uid             = response.split('"uid":"')[1].split('","nickName":"')[0]
                nick_name       = response.split('"nickName":"')[1].split('","signature":""')[0]
                uniqueId        = response.split('"uniqueId":"')[1].split('","')[0]
                followingCount        = response.split('"followingCount":"')[1].split('","')[0]
                # self.infoTikApi = {'live':True,'uid': uid, 'nickName': nick_name, 'uniqueId': uniqueId} 
                # print(self.infoTikApi)
    
                self.editCellByColumnName.emit(self.index, 'Passmail', f'{followingCount}',self.parent.tableWidget, COLORS.ORANGE)
                self.__updateValue()
                time.sleep(1)
                self.infoTikApi = {'live':True,'uid': uid, 'nickName': nick_name, 'uniqueId': uniqueId,"Folow:": followingCount} 
                print(self.infoTikApi)
                self.uid = uniqueId 
                # if int(followingCount) > 350:
                #     self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] {self.status}', self.parent.tableWidget, COLORS.RED)
                #     self.__updateValue()
                #     time.sleep(3)
                #     self.deleteProfile()
                #     time.sleep(5)
                #     self.initJobBrowser()
                #     return
                self.uid = uniqueId
                self.editCellByColumnName.emit(self.index, 'UID', str(self.infoTikApi['uniqueId']), self.parent.tableWidget, COLORS.GREEN)
                return True
            except Exception as e: 
                logging.error(f"An error occurred: {e}")
                error_detail = traceback.print_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({e})', self.parent.tableWidget, COLORS.RED)
                # if self.uid in self.driver.current_url:
                # if self.settings['TaskSettings']['Captcha']:self.bypassCaptcha(5)
                time.sleep(random.randint(3,5))
            self.editCellByColumnName.emit(self.index, 'Status',  f'Không kiểm tra được Page Source tiến hành kiểm tra Cookie! (UID: {self.uid})', self.parent.tableWidget, COLORS.GREEN)
            try:
                self.apiTikTok  = TikTok_Api(self.cookieChrome)
                self.infoTikApi = self.apiTikTok.infoAccounts()
                # print(self.infoTikApi)
                self.uid = self.infoTikApi['uniqueId']
                if self.infoTikApi['live']:
                    # self.editCellByColumnName.emit(self.index, 'UID', str(self.infoTikApi['uniqueId']), self.parent.tableWidget, COLORS.GREEN)
                    return True
            
            except Exception as e: 
                logging.error(f"An error occurred: {e}")
                error_detail = traceback.print_exc()
                self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({e})', self.parent.tableWidget, COLORS.RED)
                time.sleep(random.randint(3,5))
                
        except Exception as e: 
            logging.error(f"An error occurred: {e}")
            error_detail = traceback.print_exc()
            self.editCellByColumnName.emit(self.index, 'Status', f'❌ [ {self.__typeStart} ] ERROR({e})', self.parent.tableWidget, COLORS.RED)
            time.sleep(random.randint(3,5))

        self.editCellByColumnName.emit(self.index, 'Status',  f'Không kiểm tra được thông tin tài khoản!!! (UID: {self.uid})', self.parent.tableWidget, COLORS.RED)
        
        return False
    
    def addCookie(self):
        for _ in range(3):
            try:
                self.__updateValue();time.sleep(1)
                self.editCellByColumnName.emit(self.index, 'Status', f'Add cookie {self.sessionid}', self.parent.tableWidget, COLORS.ORANGE)
                time.sleep(1)
                # BẮT BUỘC: Phải vào trang web trước khi thêm cookie của trang đó
                if "tiktok.com" not in self.driver.current_url:
                    self.driver.get("https://www.tiktok.com/login");self.driver.set_page_load_timeout(15)
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
                self.editCellByColumnName.emit(self.index, 'Status', f'Add cookie {self.sessionid} hoàn tất.', self.parent.tableWidget, COLORS.ORANGE)
                # Sau khi thêm xong, refresh lại trang để nhận session mới
                self.driver.refresh()
                time.sleep(3)
                return True
            except:
                time.sleep(5)

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

    def deleteProfile(self, type = ''):
        """
            Xóa thư mục profile trình duyệt một cách kiên trì.
            Thử tối đa 30 lần, mỗi lần cách nhau 5 giây. 
            Cập nhật trạng thái UI và log nếu có lỗi.
        """
        self.clearCookies()
        # self.adjustWindow(mode = 'restore')
        self.__updateValue();time.sleep(1)
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('logs.txt', 'a+', encoding='utf-8') as f:
            f.write(f'{formatted_datetime}: UID: {self.uid.upper()} | Lý do: {self.status} | Luồng {self.index+1}\n')
        time.sleep(1)
        if type == '':
            self.editCellByColumnName.emit(self.index, 'UID', '',self.parent.tableWidget, COLORS.RED)
            self.editCellByColumnName.emit(self.index, 'Password', '',self.parent.tableWidget, COLORS.RED)
            self.editCellByColumnName.emit(self.index, '2FA', '',self.parent.tableWidget, COLORS.RED)
        
        self.__typeStart = 'BrowserClear'

        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🧹 Đang mở trang Clear Data...', self.parent.tableWidget, COLORS.ORANGE)
        self.driver.get('chrome://settings/clearBrowserData'); self.driver.set_page_load_timeout(30);time.sleep(2)

        actions = ActionChains(self.driver)

        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🧹 Lựa chọn thời gian', self.parent.tableWidget, COLORS.ORANGE)

        # Di chuyển đến vùng nút Clear Data
        for i in range(4):
            self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ➡ TAB lần {i+1}', self.parent.tableWidget, COLORS.BLUE)
            actions.send_keys(Keys.TAB)
            actions.perform()
            time.sleep(random.uniform(0.2, 0.4))

        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ✅ Mở lựa chọn thời gian', self.parent.tableWidget, COLORS.GREEN)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(1)

        # Di chuyển chọn phạm vi thời gian
        for i in range(4):
            self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ⬇ DOWN lần {i+1}', self.parent.tableWidget, COLORS.BLUE)
            actions.send_keys(Keys.DOWN)
            actions.perform()
            time.sleep(random.uniform(0.2, 0.4))

        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ✅ Xác nhận lựa chọn thời gian', self.parent.tableWidget, COLORS.GREEN)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(1)

        # Di chuyển đến nút xác nhận Clear
        for i in range(5):
            self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ➡ TAB lần {i+1} đến nút xác nhận', self.parent.tableWidget, COLORS.BLUE)
            actions.send_keys(Keys.TAB)
            actions.perform()
            time.sleep(random.uniform(0.2, 0.4))

        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] 🧹 Xác nhận xóa toàn bộ lịch sử...', self.parent.tableWidget, COLORS.ORANGE)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(3)
        self.driver.get('chrome://history/')
        self.editCellByColumnName.emit(self.index, 'Status', f'[ {self.__typeStart} ] ✅ Xóa toàn bộ lịch sử Browser hoàn tất.', self.parent.tableWidget, COLORS.GREEN)
        time.sleep(5)
        return True

    def stop(self):
        global USED_POS, LOGIN_ACCOUNT
        self.__updateValue()
        try:
            LOGIN_ACCOUNT.remove(self.index)
        except:pass
        if self.pos_window in USED_POS: USED_POS.remove(self.pos_window)
        # try:
        #     if self.handle_chrome: 
        #         threading.Thread(target=embedApi.unembed_tab, args=(self.handle_chrome, )).start() 
        # except:pass
        self.editCellByColumnName.emit(self.index, 'Status', f'Đã kết thúc, trước đó -> {self.status}', self.parent.tableWidget, COLORS.BLUE)
        try:threading.Thread(target=self.driver.quit, args=()).start()
        except:pass
        self.terminate()
