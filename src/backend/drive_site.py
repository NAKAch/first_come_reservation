from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

class DriveSite:
    def __init__(self, url, user_id, user_password, park, lots):
        self.url = url
        self.driver = webdriver.Chrome()
        self.user_id = user_id
        self.user_password = user_password
        self.park = park
        self.lots = lots

    def open_page_and_switch_to_main_frame(self):
        """指定のURLを開き、メインフレームに切り替える"""
        self.driver.get(self.url)
        self.driver.switch_to.frame('MainFrame')

    def select_park(self):
        """公園を選択する処理"""
        self.driver.find_element(By.LINK_TEXT, 'テニス').click()
        self.driver.find_element(By.LINK_TEXT, '京都市左京区').click()
        self.driver.find_element(By.NAME, 'btn_next').click()

        if self.park == '岡崎':
            self.driver.find_element(By.XPATH, '/html/body/form/div[2]/center/table[4]/tbody/tr/td/table/tbody/tr[1]/td[2]/input').click()
        elif self.park == '宝':
            self.driver.find_element(By.XPATH, '/html/body/form/div[2]/center/table[4]/tbody/tr/td/table/tbody/tr[3]/td[6]/input').click()

    def select_date(self, year, month, day):
        """指定された年月日のコートを選択"""
        try:
            year_element = self.driver.find_element(By.XPATH, f"//td[@class='clsCalYear']/a[contains(text(), '{year}年')]")
            year_element.click()
        except NoSuchElementException:
            pass  # すでに選択されている場合はスキップ

        try:
            month_element = self.driver.find_element(By.XPATH, f"//td[@class='clsCalMonth']/a[contains(text(), '{month}月')]")
            month_element.click()
        except NoSuchElementException:
            pass  # すでに選択されている場合はスキップ

        day_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, f"//a[text()='{day}']"))
        )
        self.driver.find_element(By.XPATH, f"//a[text()='{day}']")
        day_element.click()

    def select_time_slot(self, lot):
        """時間枠を選択"""
        time_xpath_dict = {
            "8~10": '/html/body/form/div[2]/div[2]/left/left/table[3]/tbody/tr[5]/td[1]',
            "10~12": '/html/body/form/div[2]/div[2]/left/left/table[3]/tbody/tr[5]/td[2]',
            "0~2": '/html/body/form/div[2]/div[2]/left/left/table[3]/tbody/tr[5]/td[3]',
            "2~4": '/html/body/form/div[2]/div[2]/left/left/table[3]/tbody/tr[5]/td[4]',
            "4~6": '/html/body/form/div[2]/div[2]/left/left/table[3]/tbody/tr[5]/td[5]',
            "6~9": '/html/body/form/div[2]/div[2]/left/left/table[3]/tbody/tr[5]/td[6]'
        }
        time_xpath = time_xpath_dict[lot[1]]
        koma_elements = self.driver.find_elements(By.XPATH, time_xpath)
        return koma_elements

    def switch_to_new_window(self, original_window):
        """新しいウィンドウに切り替える"""
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                print(f"新しいウィンドウに切り替えました: {window_handle}")
                break

    def switch_back_to_original_window(self, original_window):
        """元のウィンドウに切り替え戻す"""
        self.driver.switch_to.window(original_window)
        self.driver.switch_to.frame('MainFrame')
        print("元のウィンドウに戻りました。")

    def reserve_court(self, koma_elements, lot):
        """予約可能なコートを選択"""
        original_window = self.driver.current_window_handle
        for koma_element in koma_elements:
            try:
                a_element = koma_element.find_element(By.TAG_NAME, "a")
                img_element = a_element.find_element(By.TAG_NAME, "img")
                alt_text = img_element.get_attribute("alt")

                if alt_text == "予約可能":
                    print(f"{lot[0]}の{lot[1]}は予約可能です。クリックします。")
                    a_element.click()  # 予約可能ならクリック
                    self.switch_to_new_window(original_window)
                    court_elements = self.driver.find_elements(By.XPATH, "//td[@class='clsKoma']/a/img[@alt='予約可能 ']/ancestor::td")
                    if court_elements:
                        first_available_court = court_elements[0]
                        first_available_court.find_element(By.TAG_NAME, "a").click()
                        close_button = self.driver.find_element(By.XPATH, "//input[@alt='この画面を閉じる']")
                        close_button.click()
                    self.switch_back_to_original_window(original_window)
                    return "予約可能"
                elif alt_text == "予約不可":
                    print(f"{lot[0]}の{lot[1]}は予約不可です。")
                    return "予約不可"
                elif alt_text == "抽選予約画面へ移動":
                    print(f"{lot[0]}の{lot[1]}は抽選のみ可能です。")
                    return "抽選のみ可"
            except NoSuchElementException:
                pass
        return False
    
    def login(self):
        """ユーザIDとパスワードでログインを試行し、結果を返す"""
        login_status = None  # ログイン状態の管理用変数

        try: # ログイン画面に遷移した場合の処理
            try:
                # ユーザIDとパスワードを入力
                blank_of_user_id = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/center/table/tbody/tr[1]/td/input'))
                )
                blank_of_user_id.send_keys(self.user_id)

                password_input = self.driver.find_element(By.XPATH, '/html/body/form/div[2]/center/table/tbody/tr[2]/td/input')
                password_input.send_keys(self.user_password)

                # 「OK」ボタンをクリック
                self.driver.find_element(By.CSS_SELECTOR, 'input.clsImage[name="btn_ok"]').click()

                # 1b. IDまたはパスワードが間違っている場合を確認
                try:
                    error_message = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ResultMsg'))
                    )
                    if "ＩＤまたはパスワードが間違っています。" in error_message.text:
                        print("IDまたはパスワードが間違っています。")
                        login_status = "invalid_credentials"
                        return login_status

                except:
                    pass  # エラーメッセージがない場合は次のステップに進む
                
                time.sleep(1)
                
                # 1c. 無効なIDでアラートが表示される場合
                try:
                    alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                    alert.accept()
                    print("無効なユーザーIDです。")
                    login_status = "invalid_user_id"
                    time.sleep(1)
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.clsImage[name="btn_LogOut"]'))
                    ).click()
                    return login_status

                except:
                    pass  # アラートが存在しない場合はログイン成功とみなす

                # 1a. ログイン成功
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.clsImage[name="btn_next"]'))
                ).click()
                print("ログインに成功しました。")
                login_status = "success"
                return login_status

            except NoSuchElementException:
                # すでにログイン済みの場合
                print("すでにログイン済みです。")
                login_status = "already_logged_in"
                return login_status

        except:
            login_status = "another error"
            return login_status

    def comfirm_reservation(self):
        """予約確認画面で予約を確定する"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.clsImage[name="btn_toroku"]'))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.clsImage[name="btn_cmd"]'))
        ).click()

        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.accept()
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.accept()

    def login_and_confirm(self):
        """ユーザIDとパスワードでログイン"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.clsImage[name="btn_ok"]'))
        ).click()

        login_status = self.login()

        if login_status == "success" or login_status == "already_logged_in":
            self.comfirm_reservation()
        elif login_status == "invalid_credentials":
            return "invalid_credentials"
        elif login_status == "invalid_user_id":
            return "invalid_user_id"
        elif login_status == "another error":
            return "another error"

        # 予約確認画面へ戻る
        back_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "btn_back"))
        )
        back_button.click()
        return login_status

    def handle_exceptions(self, e):
        """例外処理"""
        print(f"処理中にエラーが発生しました: {str(e)}")

    def quit_driver(self):
        """ドライバーの終了処理"""
        self.driver.quit()

    def drive(self):
        results = []
        try:
            self.open_page_and_switch_to_main_frame()
            self.select_park()

            for lot in self.lots:
                year, month, day = lot[0].split('年')[0], lot[0].split('年')[1].split('月')[0], lot[0].split('月')[1].split('日')[0]
                self.select_date(year, month, day)

                koma_elements = self.select_time_slot(lot)
                reserved = self.reserve_court(koma_elements, lot)

                if reserved=="予約可能":
                    login_status = self.login_and_confirm()
                    if login_status == "success" or login_status == "already_logged_in":
                        print(f"{lot[0]}の{lot[1]}を予約しました。")
                        results.append([self.user_id, lot[0], lot[1],"予約完了"])
                    elif login_status == "invalid_credentials":
                        print(f"{lot[0]}の{lot[1]}は予約できませんでした。")
                        results.append([self.user_id, lot[0], lot[1],"IDorパスワードの間違い"])
                        continue
                    elif login_status == "invalid_user_id":
                        print(f"{lot[0]}の{lot[1]}は予約できませんでした。")
                        results.append([self.user_id, lot[0], lot[1],"コートカード無効"])
                        continue
                    elif login_status == "another error":
                        print(f"{lot[0]}の{lot[1]}は予約できませんでした。")
                        results.append([self.user_id, lot[0], lot[1],"その他のエラー"])
                        continue
                elif reserved=="予約不可":
                    print(f"{lot[0]}の{lot[1]}は予約できませんでした。")
                    results.append([self.user_id, lot[0], lot[1],"予約不可"])
                elif reserved=="抽選のみ可":
                    print(f"{lot[0]}の{lot[1]}は抽選のみ可能です。")
                    results.append([self.user_id, lot[0], lot[1],"抽選のみ可"])

        except Exception as e:
            self.handle_exceptions(e)
        finally:
            self.quit_driver()
            print("ドライバーを終了しました。")
            # result examle: [['E00057145', '2024年10月20日', '10~12', '予約不可'], ['E00057145', '2024年10月20日', '0~2', '予約不可']] 
            return results