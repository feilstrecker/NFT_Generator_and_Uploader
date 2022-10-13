# Imports
import pyautogui
import os
import pandas as pd
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import chromedriver_autoinstaller

class NFT_Uploader():

    def __init__(self):
        self.dataframe = pd.read_csv('Nft_Information.csv')
        self.already_used = False
        self.by = {
            'tag': By.TAG_NAME,
            'class': By.CLASS_NAME,
            'id': By.ID
        }
        chromedriver_autoinstaller.install()

    def open_chrome(self):
        # Open Chrome
        self.main_directory = os.path.join(os.sys.path[0])
        subprocess.Popen([
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + self.main_directory + "/chrome_profile",], shell=True,)

    def connect_chrome(self):
        # Connect selenium to chrome
        self.options = Options()
        self.options.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(
                executable_path="chromedriver.exe", chrome_options=self.options)
        self.driver.get("https://opensea.io/login")
    
    def find_by(self, by, tag, value, attribute=False, send_keys=False, fail_exit=True):
        # Example: self.find_by('tag', 'input', 'dd/mm/aaaa', attribute='placeholder')
        by = self.by[by]
        c = 0

        found = False

        while found == False:
            try:
                elements = self.driver.find_elements(by, tag)
                for element in elements:
                    if attribute:
                        if element.get_attribute(attribute) == value:
                            if send_keys:
                                element.send_keys(send_keys)
                            else:
                                element.click()
                            found = True
                            break
                    else:
                        if element.text == value:
                            if send_keys:
                                element.send_keys(send_keys)
                            else:
                                element.click()
                            found = True
                            break
                c += 1
                if c == 5:
                    print(f'falha ao encontrar:\n{by}\n{tag}\n{value}')
                    if fail_exit:
                        exit()
                    else:
                        c = 0
                sleep(0.5)
                    
            except Exception:
                pass
        return True

    def go_to_collection_create(self, collection_name):
            self.driver.get(f"https://opensea.io/collection/{collection_name}/assets/create")
            sleep(1.5)

    def send_image(self, img_path):
        # Click to image uploader
        self.find_by(by='tag', tag='div', value='Select an image, video, audio or 3D model file', attribute='aria-label')
        sleep(1)
        pyautogui.write(img_path, interval=0.05)
        pyautogui.press('return')
        sleep(0.1)
        print('img - ok')

    def send_nft_name(self, nft_name):
        # Put NFT name.
        sleep(0.5)
        self.find_by(by='tag', tag='input', value='Item name', attribute='placeholder', send_keys=nft_name, fail_exit=False)
        print('nft name - ok')

    def send_nft_description(self, nft_description):
        # Put description.
        sleep(0.5)
        self.find_by(by='tag', tag='textarea', value='description', attribute='id', send_keys=nft_description, fail_exit=False)
        print('description - ok')

    def click_to_create(self):
        sleep(0.5)
        self.find_by(by='tag', tag='button', value='Create')
        
        print('Create - click')
        os.system('pause')

    def send_item_info(self, item_name, item_color, close=False):
        sleep(0.5)
        if self.already_used == False:

            # Open Properties
            self.find_by(by='tag', tag='button', value='Add properties', attribute='aria-label')

            # Send name of item
            self.elements = self.driver.find_elements(By.TAG_NAME, 'input')
            for element in self.elements:
                if element.get_attribute('placeholder') == 'Character' and element.get_attribute('value') == '':
                    element.send_keys(item_name)

            # Send color of item
            
            self.elements = self.driver.find_elements(By.TAG_NAME, 'input')
            for element in self.elements:
                if element.get_attribute('placeholder') == 'Male' and element.get_attribute('value') == '':
                    element.send_keys(item_color)
                    self.already_used = True
                                   
        else:
            # Click to add more
            self.find_by(by='tag', tag='button', value='Add more')
            sleep(0.5)

            # Send name of item
            #self.find_by(by='tag', tag='input', value='Character', attribute='placeholder', send_keys=item_name)
            self.elements = self.driver.find_elements(By.TAG_NAME, 'input')
            for element in self.elements:
                if element.get_attribute('placeholder') == 'Character' and element.get_attribute('value') == '':
                    element.send_keys(item_name)

            # Send color of item
            self.elements = self.driver.find_elements(By.TAG_NAME, 'input')
            for element in self.elements:
                if element.get_attribute('placeholder') == 'Male' and element.get_attribute('value') == '':
                    element.send_keys(item_color)

        if close == True:
            # Click to save
            self.find_by(by='tag', tag='button', value='Save')
            self.already_used = False
            return

    def query(self, colum, img_name):
        for index, value in self.dataframe.iterrows():
            if self.dataframe['nft_name'][index] == img_name:
                return self.dataframe[colum][index]
        
    def run(self, filename, nft_name, nft_description, collection_name):
        # Variables
        self.nft_filename = filename
        self.nft_description = nft_description
        self.nft_name = nft_name

        # Get name
        self.background_name = self.query('background', self.nft_filename)
        self.body_name = self.query('body', self.nft_filename)
        self.acessory_name = self.query('acessory', self.nft_filename)
        self.hat_name = self.query('hat', self.nft_filename)

        # Get Color
        self.background_color = self.query('background_color', self.nft_filename)
        self.body_color = self.query('body_color', self.nft_filename)
        self.acessory_color = self.query('acessory_color', self.nft_filename)
        self.hat_color = self.query('hat_color', self.nft_filename)
        
        # Go to collection
        self.go_to_collection_create(collection_name)
        # Send the img nft
        self.send_image(f"{self.nft_filename}")
        # Send nft name
        self.send_nft_name(self.nft_name)
        # Send nft description
        self.send_nft_description(self.nft_description)
        # Send background info
        self.send_item_info(self.background_name, self.background_color)
        # Send body info
        self.send_item_info(self.body_name, self.body_color)
        # Send acessory info
        self.send_item_info(self.acessory_name, self.acessory_color)
        # Send hat info
        self.send_item_info(self.hat_name, self.hat_color, close=True)
        # Create
        self.click_to_create()
