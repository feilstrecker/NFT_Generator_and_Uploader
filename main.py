from PIL import Image
import pandas as pd
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import warnings
import pyautogui
import random
warnings.filterwarnings('ignore')

class NFT_generator():

    def __init__(self):
        self.counter = 1
        path, dirs, files = next(os.walk("done"))
        self.total_nfts = len(files)

        # Itens list
        self.backgrounds = []
        self.bodies = []
        self.acessories = []
        self.hats = []

        # For generate nfts without accessory and hat
        self.acessories.append(Image.open('none.png'))
        self.hats.append(Image.open('none.png'))

    def Load(self):

        # Get the filenames
        elements = ['Backgrounds', 'Bodies', 'Acessories', 'Hats']

        self.background_img_name = []
        self.body_img_name = []
        self.acessory_img_name = ['None']
        self.hat_img_name = ['None']

        for element in elements:
            path, dirs, files = next(os.walk(f"items\\{element}"))

            if element == 'Backgrounds':
                self.background_img_name = files
            elif element == 'Bodies':
                self.body_img_name = files
            elif element == 'Acessories':
                self.acessory_img_name = files
            elif element == 'Hats':
                self.hat_img_name = files

        self.background_amount =  len(self.background_img_name)
        self.body_amount = len(self.body_img_name)
        self.acessory_amount = len(self.acessory_img_name)
        self.hat_amount = len(self.hat_img_name)
        # Lists to add informations into Properties on upload

        self.background_name = []
        self.body_name = []
        self.acessory_name = ['None']
        self.hat_name = ['None']

        self.background_color = []
        self.body_color = []
        self.acessory_color = ['None']
        self.hat_color = ['None']
        
        #         ---------------- Load the informations of itens ----------------

        # Backgrounds
        for filename in self.background_img_name:
            self.img_name = filename
            filename = filename.replace('.png', '')
            filename = filename.split('-')
                        
            if filename[0].count('_') > 0:
                self.item_name = filename[0].replace('_', ' ')
            else:
                self.item_name = filename[0]

            if filename[1].count('_') > 0:
                self.item_color = filename[1].replace('_', ' ')
            else:
                self.item_color = filename[1]

            self.background_name.append(self.item_name)    
            self.background_color.append(self.item_color)
        
        # Bodies
        for filename in self.body_img_name:
            self.img_name = filename
            filename = filename.replace('.png', '')
            filename = filename.split('-')
                        
            if filename[0].count('_') > 0:
                self.item_name = filename[0].replace('_', ' ')
            else:
                self.item_name = filename[0]

            if filename[1].count('_') > 0:
                self.item_color = filename[1].replace('_', ' ')
            else:
                self.item_color = filename[1]

            
            self.body_name.append(self.item_name)
            self.body_color.append(self.item_color)

        # Acessories
        for filename in self.acessory_img_name:
            self.img_name = filename
            filename = filename.replace('.png', '')

            if filename != 'None':
                filename = filename.split('-')

                if filename[0].count('_') > 0:
                    self.item_name = filename[0].replace('_', ' ')
                else:
                    self.item_name = filename[0]

                if filename[1].count('_') > 0:
                    self.item_color = filename[1].replace('_', ' ')
                else:
                    self.item_color = filename[1]

            else:
                self.item_name = 'None'
                self.item_color = 'None'
            
        
            self.acessory_name.append(self.item_name)
            self.acessory_color.append(self.item_color)  


        # Hats
            for filename in self.hat_img_name:
                self.img_name = filename
                filename = filename.replace('.png', '')
                filename = filename.split('-')
                
                if filename != 'None':
                    if filename[0].count('_') > 0:
                        self.item_name = filename[0].replace('_', ' ')
                    else:
                        self.item_name = filename[0]

                    if filename[1].count('_') > 0:
                        self.item_color = filename[1].replace('_', ' ')
                    else:
                        self.item_color = filename[1]
                else:
                    self.item_name = 'None'
                    self.item_color = 'None'

                self.hat_name.append(self.item_name)
                self.hat_color.append(self.item_color)
    
        
        # Total nfts Available
        self.total_nfts = self.background_amount * self.body_amount * (self.acessory_amount+1) * (self.hat_amount+1)
                
        #                          ---------------- Put itens in lists ----------------
        # Backgrounds
        for filename in self.background_img_name:
            self.backgrounds.append(Image.open(f'items\\Backgrounds\\{filename}'))

        # Bodys
        for filename in self.body_img_name:
            self.bodies.append(Image.open(f'items\\Bodies\\{filename}'))
        
        # acessorys
        for filename in self.acessory_img_name:
            self.acessories.append(Image.open(f'items\\Acessories\\{filename}'))

        # Hats
        for filename in self.hat_img_name:
            self.hats.append(Image.open(f'items\\Hats\\{filename}'))

        print(f'({self.total_nfts}) <- Available NFTS to generate')


        # Find index with the filename

        if type == 'background':
            return self.background_img_name.index(filename)

        elif type == 'body':
            return self.body_img_name.index(filename)

        elif type == 'acessory':
            return self.acessory_img_name.index(filename)

        elif type == 'hat':
            return self.hat_img_name.index(filename)

    def Add_rarity(self, item_name, item_color):
        # Add rarity to nfts
        # Load DataFrame
        self.df1 = pd.read_csv('Nft_information.csv', index_col=0)
        self.df1.reset_index(inplace=True, drop=True)

        # Get indexes with the item
        self.indexes = self.Find_indexes_with_item(item_name, item_color)

        if self.indexes:
            # Random remove
            print("type 'cancel' to cancel")
            self.percentage = (len(self.indexes)/self.total_nfts) * 100
            print(f"have ({len(self.indexes)}/{self.total_nfts})[{self.percentage:.2f}%] nfts with this item.")
            self.amount = (input((f'how many you want remove?\n')))
            if self.amount == 'cancel':
                os.system('cls')
                return
            if int(self.amount) > len(self.indexes):
                return print('amount to remove > already have')
            elif len(self.indexes) == 0:
                return print("don't have nfts with this item")

            
            for i in range(0, int(self.amount)):
                self.counter = 0
                self.choice = random.choice(self.indexes)
                for index in self.indexes:
                    if index == self.choice:
                        self.indexes.pop(self.counter)
                    self.counter += 1
                self.nft_name = self.df1['nft_name'][self.choice]

                # Remove into dataframe
                self.df1.drop(index=self.choice, axis=0, inplace=True)
                self.dataframe = self.df1
                self.Save_modifications()

                # Remove the file
                if os.path.exists(f'done\\{self.nft_name}'):
                    os.remove(f'done\\{self.nft_name}')
                print(f'deleted --> {self.nft_name} ({i+1}/{self.amount})')
        else:
            print(self.indexes)
            return print("Item not found")

    def Find_indexes_with_item(self, item_name, item_color):

        df = pd.read_csv('Nft_information.csv', index_col=0)
        item_types = ['background', 'body', 'acessory', 'hat']

        for item_type in item_types:

            get_item_type = df[df[item_type] == item_name].index.tolist()
            if get_item_type:
                inf = df[(df[item_type] == item_name) & (df[f'{item_type}_color'] == item_color)]
                indexes = inf.index.tolist()
                if indexes:
                    return indexes
        return None
        
    def Show_itens_rarity(self):


        with open('itens_config.txt', 'r') as arq:
            self.itens = arq.read()
            self.itens = self.itens.split('\n')
            del self.itens[0]
            
            # Split informations
            print('----------------------------------------')
            for item in self.itens:
                item = item.split(', ')
                self.item_name = item[2]
                self.item_color = item[3]

                item_indexes = self.Find_indexes_with_item(self.item_name, self.item_color)
                self.percentage = (len(item_indexes) / self.total_nfts) * 100

                sleep(0.2)
                print(f"[{self.percentage:.2f}%] {self.item_name} - {self.item_color}")
            print('----------------------------------------')

    def Save_modifications(self):
        # Save modifications into dataframe
        self.dataframe.to_csv('Nft_Information.csv', mode='w')

    def Run(self):
        # Run
        self.counter_background = 0

        for background in self.backgrounds:
            self.counter_body = 0

            for body in self.bodies:
                # Add background and body on the nft
                body_with_background = Image.alpha_composite(im1=background, im2=body)
                self.counter_acessory = 0

                for acessory in self.acessories:
                    # Add acessory on the nft
                    acessory_with_body = Image.alpha_composite(im1=body_with_background, im2=acessory)
                    self.counter_hats = 0

                    for hat in self.hats:
                        # Add hat on the nft
                        self.im_final = acessory_with_body
                        self.im_final = Image.alpha_composite(im1=acessory_with_body, im2=hat)

                        # ---------------------------- Add info to put in Properties on upload ----------------------------

                        # Get index of the item, into those lists with it informations
                        self.index_background = self.counter_background #self.Find_index('background', f'{self.background_img_name[self.counter_background]}')
                        self.index_body = self.counter_body #self.Find_index('body', f'{self.body_img_name[self.counter_body]}')

                        # Get the background name and it color
                        self.background_info = self.background_name[self.index_background]
                        self.background_info_color = self.background_color[self.index_background]

                        # Get the body name and it color
                        self.body_info = self.body_name[self.index_body]
                        self.body_info_color = self.body_color[self.index_body]

                        # On 0 have the "none.png"
                        # Get the acessory name and it color
                        if self.counter_acessory == 0:
                            self.acessory_info = 'None'
                            self.acessory_info_color = 'None'
                        else:
                            self.index_acessory = self.counter_acessory #self.Find_index('acessory', f'{self.acessory_img_name[self.counter_acessory]}')
                            self.acessory_info = self.acessory_name[self.index_acessory]
                            self.acessory_info_color = self.acessory_color[self.index_acessory]

                        # Get the hat name and it color
                        if self.counter_hats == 0:
                            self.hat_info = 'None'
                            self.hat_info_color = 'None'
                        else:
                            self.index_hat = self.counter_hats #self.Find_index('hat', f'{self.hat_img_name[self.counter_hats]}')
                            self.hat_info = self.hat_name[self.index_hat]
                            self.hat_info_color = self.hat_color[self.index_hat]

                        # Data for dataframe
                        self.nft_info = {
                            'nft_name':[f'nft{self.counter}.png'],
                            'background': [self.background_info] ,
                            'body': [self.body_info],
                            'acessory': [self.acessory_info],
                            'hat': [self.hat_info],
                            'background_color': [self.background_info_color],
                            'body_color': [self.body_info_color],
                            'acessory_color': [self.acessory_info_color],
                            'hat_color': [self.hat_info_color]

                        }
                        # Concatenate dataframes
                        self.df1 = pd.read_csv('Nft_information.csv', index_col=0)
                        self.df2 = pd.DataFrame(data=self.nft_info)
                        self.dataframe = pd.concat([self.df1, self.df2])
                        self.Save_modifications()
                        # Save the img
                        self.im_final.save(f'done\\nft{self.counter}.png')

                        print(f'✓ Created - NFT({self.counter}/{self.total_nfts})')
                    
                        self.counter += 1
                        self.counter_hats += 1
                        if self.counter_hats > self.hat_amount:
                            self.counter_hats = self.counter_hats - 1

                    self.counter_acessory += 1
                    if self.counter_acessory > self.acessory_amount:
                            self.counter_acessory = self.counter_acessory - 1

                self.counter_body += 1
            self.counter_background +=1
        print('<<-- Done -->>')

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

def Gui():
    decision = ''
    while decision != 'exit':
        decision = input(
            "--- type 'exit' to exit ---\n"
            '1 - nft generator ->\n'
            '2 - nft uploader ->\n'
            '3 - nft rarity ->\n'
            '4 - show nfts rarity ->\n'
            )
        
        # Generate nfts
        if decision == '1':
            os.system('cls')
            p1 = NFT_generator()
            print("<------ Option: Generate Nfts ------>\n")
            p1.Load()
            decision = input('Are you sure? (Y/N)')
            if decision == 'N':
                return
            p1.Run()

        # Upload nfts
        elif decision == '2':
            os.system('cls')
            p1 = NFT_Uploader()
            print("<------ Option: Upload Nfts ------>\n")

            nft_name = input('nft name: ')
            nft_description = input('nft description: ')
            start_number = int(input('start nft number: '))
            finish_number = int(input('finish nft number: '))

            p1.Open_chrome()
            p1.Connect_chrome()
            collection_name = input('collection name: ')

            dataframe = pd.read_csv('Nft_information.csv', index_col=0)
            filenames = dataframe['nft_name'].to_list()

            for i in range(start_number, finish_number):
                choice = random.choice(filenames)
                index = filenames.index(choice)
                del filenames[index]
                p1.Run(choice, f'{nft_name} #{i}', nft_description, collection_name) 

        # Rarity nfts
        elif decision == '3':
            os.system('cls')
            p1 = NFT_generator()
            print("<------ Option: Rarity Nfts ------>\n")
            p1.Add_rarity(input('Item name: '), input('Item color: '))

        # Print rarity of nfts
        elif decision == '4':
            os.system('cls')
            p1 = NFT_generator()
            p1.Show_itens_rarity()
            
Gui()
