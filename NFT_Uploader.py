import pyautogui
import os
import pandas as pd
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

class NFT_Uploader():

    def __init__(self):
        self.dataframe = pd.read_csv('Nft_Information.csv')
        self.already_used = False

    def Open_chrome(self):
        # Open Chrome
        self.main_directory = os.path.join(os.sys.path[0])
        subprocess.Popen([
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + self.main_directory + "/chrome_profile",], shell=True,)

    def Connect_chrome(self):
        # Connect selenium to chrome
        self.options = Options()
        self.options.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(
                executable_path="chromedriver.exe", chrome_options=self.options)
        self.driver.get("https://opensea.io/login")
    
    def Go_to_collection_create(self, collection_name):
            self.driver.get(f"https://opensea.io/collection/{collection_name}/assets/create")
            sleep(1.5)

    def Send_image(self, img_path):
        # Click to image uploader
        self.elements = self.driver.find_elements_by_tag_name('div')
        for element in self.elements:
            if element.get_attribute('aria-label') == 'Select an image, video, audio or 3D model file':
                element.click()
                sleep(1)
                pyautogui.write(img_path, interval=0.05)
                pyautogui.press('return')
                sleep(0.1)
                print('img - ok')

    def Send_nft_name(self, nft_name):
        # Put NFT name.
        sleep(0.5)
        self.elements = self.driver.find_elements_by_tag_name('input')
        for element in self.elements:
            if element.get_attribute('placeholder') == 'Item name':
                element.send_keys(nft_name)
                print('nft name - ok')

    def Send_nft_description(self, nft_description):
        # Put description.
        sleep(0.5)
        self.elements = self.driver.find_elements_by_tag_name('textarea')
        for element in self.elements:
            if element.get_attribute('id') == 'description':
                element.send_keys(nft_description)
                print('description - ok')

    def Click_to_create(self):
        sleep(0.5)
        self.elements = self.driver.find_elements_by_tag_name('button')
        for element in self.elements:
            if element.text == 'Create':
                element.click()
                print('Create - click')

    def Send_item_info(self, item_name, item_color, close=False):
        sleep(0.5)
        if self.already_used == False:

            # Open Properties
            self.elements = self.driver.find_elements_by_tag_name('button')
            for element in self.elements:
                if element.get_attribute('aria-label') == 'Add properties':
                    element.click()

                    # Send name of item
                    self.elements = self.driver.find_elements_by_tag_name('input')
                    for element in self.elements:
                        if element.get_attribute('placeholder') == 'Character' and element.get_attribute('value') == '':
                            element.send_keys(item_name)

                            # Send color of item
                            self.elements = self.driver.find_elements_by_tag_name('input')
                            for element in self.elements:
                                if element.get_attribute('placeholder') == 'Male' and element.get_attribute('value') == '':
                                    element.send_keys(item_color)
                                    self.already_used = True
                                   
        else:
            # Click to add more
            self.elements = self.driver.find_elements_by_tag_name('button')
            for element in self.elements:
                if element.text == 'Add more':
                    element.click()
                    sleep(0.5)

                    # Send name of item
                    self.elements = self.driver.find_elements_by_tag_name('input')
                    for element in self.elements:
                        if element.get_attribute('placeholder') == 'Character' and element.get_attribute('value') == '':
                            element.send_keys(item_name)

                            # Send color of item
                            self.elements = self.driver.find_elements_by_tag_name('input')
                            for element in self.elements:
                                if element.get_attribute('placeholder') == 'Male' and element.get_attribute('value') == '':
                                    element.send_keys(item_color)

        if close == True:
        # Click to save
            self.elements = self.driver.find_elements_by_tag_name('button')
            for element in self.elements:
                if element.text == 'Save':
                    element.click()
                    self.already_used = False
                    return

    def Query(self, colum, img_name):
        for index, value in self.dataframe.iterrows():
            if self.dataframe['nft_name'][index] == img_name:
                return self.dataframe[colum][index]
        
    def Run(self, filename, nft_name, nft_description, collection_name):
        # Variables
        self.nft_filename = filename
        self.nft_description = nft_description
        self.nft_name = nft_name

        # Get name
        self.background_name = self.Query('background', self.nft_filename)
        self.body_name = self.Query('body', self.nft_filename)
        self.acessory_name = self.Query('acessory', self.nft_filename)
        self.hat_name = self.Query('hat', self.nft_filename)

        # Get Color
        self.background_color = self.Query('background_color', self.nft_filename)
        self.body_color = self.Query('body_color', self.nft_filename)
        self.acessory_color = self.Query('acessory_color', self.nft_filename)
        self.hat_color = self.Query('hat_color', self.nft_filename)
        
        # Go to collection
        self.Go_to_collection_create(collection_name)
        # Send the img nft
        self.Send_image(f"{self.nft_filename}")
        # Send nft name
        self.Send_nft_name(self.nft_name)
        # Send nft description
        self.Send_nft_description(self.nft_description)
        # Send background info
        self.Send_item_info(self.background_name, self.background_color)
        # Send body info
        self.Send_item_info(self.body_name, self.body_color)
        # Send acessory info
        self.Send_item_info(self.acessory_name, self.acessory_color)
        # Send hat info
        self.Send_item_info(self.hat_name, self.hat_color, close=True)
        # Create
        self.Click_to_create()
