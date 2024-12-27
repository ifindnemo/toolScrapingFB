from flask import Flask, request, jsonify
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from pymongo import MongoClient
import sys
import json

PASSWORD_SECRET = os.environ["PASSWORD_SECRET"]

MONGO_URI = os.environ['MONGODB']
client = MongoClient(MONGO_URI)
db = client['KPW']

resultCrawl = []

def fanpageCrawl(request_url, num_of_post, driver, date_time):
    driver.get(f'{request_url}')
    sleep(1)

    wait = WebDriverWait(driver, 5)
    idx=1
    maxidx = num_of_post + 1
    
    Crawl=[]
    a = 0
                
    while True:
        if idx == maxidx:
            return Crawl
        divs = driver.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
        dem=0
        for div in divs:
            if dem < idx:
                dem += 1
                continue #tránh thu thập dữ liệu bị trùng lặp ở mỗi vòng lặp
            driver.execute_script("arguments[0].scrollIntoView(true);", div)    
            #-------------------------------------------------------------------TEXT----------------------------------------------------------------------
            #tìm text
            text_content = ''
            try:
                XemThem = div.find_elements(By.CSS_SELECTOR, 'div[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"]')                          
                for i in XemThem:
                    if i.text =='Xem thêm':
                        i.click()
            except:
                pass

            try:
                text = div.find_element(By.CSS_SELECTOR, 'div.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a')
                
            except:
                try:
                    text = div.find_element(By.CSS_SELECTOR, 'div[class="x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3"]')
                except:
                    try:
                        text = div.find_element(By.CSS_SELECTOR, 'div[class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"]')
                    except:
                        print('Không có tìm thầy text')  
            text_content = text.text
            
            #-------------------------------------------------------------------COMMENT AND SHARE----------------------------------------------------------------------
            comment_num = ''
            share_num = ''
            #tìm số comment và share
            comment=div.find_elements(By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')
            count = 0
            
            for i in comment:
                count += 1
                    # Bỏ qua hai lần lặp đầu tiên
                if count <= 2:
                    continue
                #comment
                if count == 3:
                    print('comment:\n',i.text,'\n' )
                    comment_num = i.text
                #share
                else:
                    print('share:\n',i.text,'\n' )
                    share_num = i.text
            #------------------------------------------------------------------COMMENT----------------------------------------------------------------------
            comment_text =[]
            print('BÌNH LUẬN\n')

            try:
                buttons = div.find_element(By.CSS_SELECTOR, 'div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn"] div[role="button"]')           
                
                buttons.click()
                sleep(5)
                
                name_elements = driver.find_element(By.CSS_SELECTOR, "div.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x78zum5.xdt5ytf.x1iyjqo2.x1al4vs7 div.html-div.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1gslohp")
                # Lấy nội dung văn bản
                name_elements1 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Bình luận dưới"] div[style="text-align: start;"]')   
                while True:           
                    first_len = len(name_elements1)
                    name_elements1 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Bình luận dưới"] div[style="text-align: start;"]')                        
                    driver.execute_script("arguments[0].scrollIntoView(true);", name_elements1[-1])
                    new_len = len(name_elements1)
                    if new_len == first_len:
                        break
                sleep(5)

                
                #______________________________________nhấn vào thêm phản hồi______________________________________
                try:
                    while True:

                        themphanhoi = driver.find_elements(By.CSS_SELECTOR,'div[class="x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r x11i5rnm xat24cr x2lwn1j xeuugli xexx8yu x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xi81zsa x1q0g3np x1iyjqo2 xs83m0k xsyo7zv x1mnrxsn"]')
                        print('><'*50,len(themphanhoi))
                        for i in themphanhoi:
                            i.click()
                            sleep(0.5)
                        sleep(2)
                        if themphanhoi ==[]:
                            break
                except:
                    pass

                sleep(5)

                name_elements2 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Phản hồi bình luận"] div[style="text-align: start;"]')
                name_elements3 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label*="đáp lại phản hồi"] div[style="text-align: start;"]')
                # Tìm các phần tử có aria-label chứa một trong các từ khóa
                name_elements = (
                    name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Bình luận dưới"] div[style="text-align: start;"]') +
                    name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Phản hồi bình luận"] div[style="text-align: start;"]') +
                    name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label*="đáp lại phản hồi"] div[style="text-align: start;"]')
                )   
                print(len(name_elements))             
                sleep(5)

                #__________________________________________LẤY BÌNH LUẬN____________________________________________
                            
                comment_text = [name.text for name in name_elements]
                sleep(1)    
                # ________________CLOSE__________________
                close_mother = driver.find_element(By.CSS_SELECTOR,'div')
                close = close_mother.find_elements(By.CSS_SELECTOR,'div[aria-label="Đóng"]')
                close[0].click()            
                
            except:
                print('Lỗi ko co binh luan')

                
            # ------------------------------------------------------------------lIKE----------------------------------------------------------------------
            like_text = []
            buttons = div.find_elements(By.CSS_SELECTOR, "span[aria-label='Xem ai đã bày tỏ cảm xúc về tin này'] div[role='button']")

            # Lọc các phần tử có thuộc tính aria-label bắt đầu bằng "Thích"
            like_buttons = [button for button in buttons if button.get_attribute("aria-label").startswith("Thích")]
            try:
                like_buttons[0].click()
            except:
                pass
            sleep(3)
            divs = driver.find_elements(By.CSS_SELECTOR, '.html-div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x6s0dn4.x78zum5.x2lah0s.x1qughib.x879a55.x1n2onr6')


            for div in divs:
                input= '.x1i10hfl.xe8uvvx.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.xjyslct.xjbqb8w.x18o3ruo.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1heor9g.x1ypdohk.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.x1vjfegm.x3nfvp2.xrbpyxo.x1itg65n.x16dsc37'   
                like = div.find_elements(By.CSS_SELECTOR,input)
                for i in like:
                    like_text.append(i.get_attribute("aria-label"))
            
            close_mother = driver.find_element(By.CSS_SELECTOR,'div') 
            try:
                close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Đóng"]')))
                close.click()
            except:
                pass
                
            sleep(1)
            Crawl.append({'date-time': date_time, 'id': idx, 'Text-Content': text_content, 'Soluongcmt': len(name_elements), 'Soluongshare': share_num, 'Likedetails': like_text, 'Cmts': comment_text})
            idx+=1
            break

def groupCrawl(request_url, num_of_post, driver, date_time):
    driver.get(f'{request_url}')
    sleep(1)

    wait = WebDriverWait(driver, 5)
    idx=1
    maxidx = num_of_post + 1
    
    Crawl=[]
    a = 0
    
    while True:
        if idx == maxidx:
            return Crawl
        divs = driver.find_elements(By.CSS_SELECTOR, 'div[class="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"]')
        dem=0
        for div in divs:
            if dem<idx:
                dem+=1
                continue #tránh thu thập dữ liệu bị trùng lặp ở mỗi vòng lặp 
            
            driver.execute_script("arguments[0].scrollIntoView(true);", div)

            #-------------------------------------------------------------------TEXT----------------------------------------------------------------------
            #tìm text
            text_content = ''
            try:
                XemThem = div.find_elements(By.CSS_SELECTOR, 'div[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"]')                          
                for i in XemThem:
                    if i.text =='Xem thêm':
                        i.click()
            except Exception as e:#--------------> SỬA
                print(f'Lỗi xảy ra: {e}')#--------------> SỬA
            try:
                text = div.find_element(By.CSS_SELECTOR, 'div[data-ad-rendering-role="story_message"]')
                
            except:
                try:
                    text = div.find_element(By.CSS_SELECTOR, 'div[class="x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3"]')
                except:
                    try:
                        text = div.find_element(By.CSS_SELECTOR, 'div[class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"]')
                    except:
                        print('Không có tìm thầy text')  
            text_content = text.text
            
            #-------------------------------------------------------------------COMMENT AND SHARE----------------------------------------------------------------------
            comment_num = '0'
            share_num = '0'

            try:
                comment_fat=div.find_element(By.CSS_SELECTOR, 'div[class="x9f619 x1ja2u2z x78zum5 x2lah0s x1n2onr6 x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj"]')
                comment = comment_fat.find_element(By.CSS_SELECTOR, 'div:nth-child(2)')
                comment_num = comment.text
                print('cm:',comment.text)
                
            except:
                print('k đếm được số bình luận')

            try:
                share = comment_fat.find_element(By.CSS_SELECTOR, 'div:nth-child(3)')
                share_num = share.text
                print('share:',share.text)
            except:
                print('k đếm được số share')
                
            #------------------------------------------------------------------COMMENT----------------------------------------------------------------------
            comment_text =[]
            print('BÌNH LUẬN\n')

            try:
                buttons = div.find_element(By.CSS_SELECTOR, 'div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn"] div[role="button"]')           
                
                buttons.click()
                sleep(5)
                
                name_elements = driver.find_element(By.CSS_SELECTOR, "div.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x78zum5.xdt5ytf.x1iyjqo2.x1al4vs7 div.html-div.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1gslohp")
                # Lấy nội dung văn bản
                name_elements1 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Bình luận dưới"] div[style="text-align: start;"]')   
                while True:           
                    first_len = len(name_elements1)
                    name_elements1 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Bình luận dưới"] div[style="text-align: start;"]')                        
                    driver.execute_script("arguments[0].scrollIntoView(true);", name_elements1[-1])
                    new_len = len(name_elements1)
                    if new_len == first_len:
                        break
                sleep(5)

                
                #______________________________________nhấn vào thêm phản hồi______________________________________
                try:
                    while True:

                        themphanhoi = driver.find_elements(By.CSS_SELECTOR,'div[class="x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r x11i5rnm xat24cr x2lwn1j xeuugli xexx8yu x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xi81zsa x1q0g3np x1iyjqo2 xs83m0k xsyo7zv x1mnrxsn"]')
                        for i in themphanhoi:
                            i.click()
                            sleep(0.5)
                        sleep(2)
                        if themphanhoi ==[]:
                            break
                except:
                    pass

                sleep(5)

                name_elements2 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Phản hồi bình luận"] div[style="text-align: start;"]')
                name_elements3 = name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label*="đáp lại phản hồi"] div[style="text-align: start;"]')
                # Tìm các phần tử có aria-label chứa một trong các từ khóa
                name_elements = (
                    name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Bình luận dưới"] div[style="text-align: start;"]') +
                    name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Phản hồi bình luận"] div[style="text-align: start;"]') +
                    name_elements.find_elements(By.CSS_SELECTOR, 'div[aria-label*="đáp lại phản hồi"] div[style="text-align: start;"]')
                )   
                print(len(name_elements))             
                sleep(5)

                    
                



                #__________________________________________LẤY BÌNH LUẬN____________________________________________
                comment_text = [name.text for name in name_elements]
                sleep(1)    
                # ________________CLOSE__________________
                close_mother = driver.find_element(By.CSS_SELECTOR,'div')
                close = close_mother.find_elements(By.CSS_SELECTOR,'div[aria-hidden="false"] div[aria-label="Đóng"]')#--------------> SỬA
                close[0].click()
                
            except:
                print('Lỗi ko co binh luan')

                
            # ------------------------------------------------------------------lIKE----------------------------------------------------------------------
            like_text = []
            buttons = div.find_elements(By.CSS_SELECTOR, "span[aria-label='Xem ai đã bày tỏ cảm xúc về tin này'] div[role='button']")

            # Lọc các phần tử có thuộc tính aria-label bắt đầu bằng "Thích"
            like_buttons = [button for button in buttons if button.get_attribute("aria-label").startswith("Thích")]
            # Đợi cho đến khi phần tử có thể được click
            try:
                like_buttons[0].click()
            except:
                pass
            sleep(3)
            divs = driver.find_elements(By.CSS_SELECTOR, '.html-div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x6s0dn4.x78zum5.x2lah0s.x1qughib.x879a55.x1n2onr6')


            for div in divs:
                input= '.x1i10hfl.xe8uvvx.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.xjyslct.xjbqb8w.x18o3ruo.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1heor9g.x1ypdohk.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.x1vjfegm.x3nfvp2.xrbpyxo.x1itg65n.x16dsc37'   
                like = div.find_elements(By.CSS_SELECTOR,input)
                for i in like:
                    like_text.append(i.get_attribute("aria-label"))
            # Đợi cho đến khi phần tử có thể được click
            
            close_mother = driver.find_element(By.CSS_SELECTOR,'div[aria-hidden="false"]') #--------------> SỬA
            try:
                close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Đóng"]')))
                
                close.click()
                
            except:
                pass
                
            sleep(1)
            Crawl.append({'date-time': date_time, 'id': idx, 'date-time': date_time, 'Text-Content': text_content, 'Soluongcmt': len(name_elements), 'Soluongshare': share_num, 'Likedetails': like_text, 'Cmts': comment_text})
            idx+=1
            break

def main():
    # Extract information from the request
    request_url = request.form.get('group_url')
    num_of_post = int(request.form.get('num_of_post'))
    typeCrawl = request.form.get('type_crawl')
    date_time = request.form.get('date_time')
    
    # Cấu hình chế độ headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chạy chế độ headless
    chrome_options.add_argument("--disable-gpu")  # Tắt GPU tăng tương thích headless
    chrome_options.add_argument("--window-size=1920,1080")  # Kích thước cửa sổ trình duyệt
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Giảm phát hiện tự động hóa
    chrome_options.add_argument("--no-sandbox")  # Dành cho môi trường không có GUI
    chrome_options.add_argument("--disable-dev-shm-usage")  # Giảm sử dụng bộ nhớ chia sẻ
    chrome_options.add_argument("--enable-unsafe-webgl")  # Cho phép sử dụng WebGL không an toàn
    chrome_options.add_argument("--disable-software-rasterizer")  # Tắt rasterizer phần mềm
    chrome_options.add_argument("--log-level=3")  # Tắt các cảnh báo không cần thiết
    chrome_options.add_argument("--silent")  # Tắt các cảnh báo không cần thiết
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Khởi tạo trình duyệt Chrome
    driver = webdriver.Chrome(options=chrome_options)
    sleep(1)

    try:
        # 2️⃣ Mở trang Facebook
        driver.get("https://www.facebook.com/")
        sleep(5)

        # 3️⃣ Tải cookie từ MongoDB và thêm vào trình duyệt
        cookies_collection = db['cookies']
        cookies = cookies_collection.find()
        
        for cookie in cookies:
            cookie.pop('_id', None)
            driver.add_cookie(cookie)
        
        # 4️⃣ Tải lại trang Facebook để xác thực bằng cookie
        driver.refresh()
        sleep(5)

        print("Đăng nhập tự động thành công bằng cookie!")
        
        if typeCrawl == 'group':
            resultCrawl = groupCrawl(request_url, num_of_post, driver, date_time)
        elif typeCrawl == 'fanpage':
            resultCrawl = fanpageCrawl(request_url, num_of_post, driver, date_time)
        else:
            resultCrawl = []
        
        db['Crawl'].insert_many(resultCrawl)
        
        # Xóa '_id'
        for document in resultCrawl:
            document.pop('_id', None)
            
        print(json.dumps(resultCrawl))
        driver.quit()

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    request_url = sys.argv[1]
    num_of_post = int(sys.argv[2])
    typeCrawl = sys.argv[3]
    date_time = sys.argv[4]
    main(request_url, num_of_post, typeCrawl, date_time)
