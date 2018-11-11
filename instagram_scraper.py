from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
import shutil
from time import sleep
from xlsxwriter import Workbook

class Instagram:
    def __init__(self, target_username, username=None , password=None):
        self.target_username = target_username
        self.username = username
        self.password = password
        self.main_url = 'https://www.instagram.com'
        self.images = []
        self._error = False
        
        with webdriver.Chrome() as self.driver:
            if self.username is not None:
                self.log_in()
            if not self._error:
                self.open_target_profile()
                self.close_dialog_box()
                self.no_of_posts()
            if not self._error:
                self.scroll_down()
            if not self._error:
                self.download_images()


    def log_in(self):
        """ Logs in into own instagram account """
        PAGE_PAUSE_TIME = 3
        KEY_PAUSE_TIME = 1
        self.driver.get(self.main_url)
        sleep(PAGE_PAUSE_TIME)

        try:
            log_in_button = self.driver.find_element_by_link_text('Log in')
            log_in_button.click()
            sleep(PAGE_PAUSE_TIME)
        except Exception:
            self._error = True
            print('Unable to find login button')
        else:
            try:
                user_name_input = self.driver.find_element_by_xpath('//input[@aria-label="Phone number, username, or email"]')
                user_name_input.send_keys(self.username)
                sleep(KEY_PAUSE_TIME)

                password_input = self.driver.find_element_by_xpath('//input[@aria-label="Password"]')
                password_input.send_keys(self.password)
                sleep(KEY_PAUSE_TIME)

                user_name_input.submit()
                sleep(KEY_PAUSE_TIME)

            except Exception:
                print('Some exception occurred while trying to find username or password field')
                self._error = True


    def open_target_profile(self):
        """ Opens the target username profile """
        try: 
            self.driver.get(self.main_url + '/' + self.target_username + '?hl=en')
            sleep(2)
        except Exception:
            self._error = True
            print('Target profile not found.')
    

    def close_dialog_box(self):
        """ Close popup dialog box """
        try:
            close_button = self.driver.find_element_by_xpath('//button[@class="Ls00D coreSpriteDismissLarge Jx1OT"]')
            close_button.click()
            sleep(1)
        except Exception:
            pass


    def scroll_down(self):
        """ Scroll down the images of target username and get image source """
        SCROLL_PAUSE_TIME = 2
        try:
            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                for image in soup.find_all('img'):
                    self.images.append(image)
                self.images = list(set(self.images))
                
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                sleep(SCROLL_PAUSE_TIME)
                
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        except Exception:
            self._error = True
            print(Exception + ': Error occured while trying to scroll down.')


    def download_images(self):
        """ Download the image captions and images of target username """
        print('Number of images found:', len(self.images))

        if len(self.images) > self.posts:
            folder = os.path.join('instaPhotos', self.target_username)
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            # Downloading captions
            print('Writing captions to excel..')    
            self.write_captions_to_excel(self.images, folder)
            
            # Downloading images
            for index, image in enumerate(self.images):
                filename = 'image-' + str(index + 1) + '.jpg'
                image_path = os.path.join(folder, filename)
                link = image['src']
                response = requests.get(link, stream=True)
                try:
                    print('Downloading image', index + 1)
                    with open(image_path, 'wb') as file:
                        shutil.copyfileobj(response.raw, file)
                except Exception:
                    print(Exception)
                    print('Could not download image number', index + 1)
                    print('Image Link -->', link)
        
        else:
            self._error = True
            print('Error: Number of images found is not equal to number of posts. Exiting...')


    def write_captions_to_excel(self, images, folder):
        """ Download image captions and write to excel """
        with Workbook(os.path.join(folder, 'captions.xlsx')) as workbook:
            worksheet = workbook.add_worksheet()
            row = 0
            worksheet.write(row, 0, 'Image name')
            worksheet.write(row, 1, 'Caption')
            
            for index, image in enumerate(images):
                row += 1
                column = 0
                filename = 'image-' + str(index + 1) + '.jpg'
                try:
                    caption = image['alt']
                except KeyError:
                    caption = 'No caption exists'
                for item in (filename, caption):
                    worksheet.write(row, column, item)
                    column += 1


    def no_of_posts(self):
        """ Get the number of posts of target username """
        no_of_posts = self.driver.find_element_by_xpath('//a[text()=" posts"]').text
        no_of_posts = no_of_posts.replace(' posts', '')
        no_of_posts = no_of_posts.replace(',', '')
        self.posts = int(no_of_posts)