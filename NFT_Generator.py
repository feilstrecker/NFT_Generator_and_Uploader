from PIL import Image
import pandas as pd
import os
import random
from time import sleep

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
        # Resize the none.png to concatenate nfts more later
        self.Resize_img()        
        # Clean dataframe
        self.Clean_dataframe()
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
                
        #             ---------------- Put itens in lists with PIL lib ----------------
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
        
        print('loaded sucesfully')
        print(f'({self.total_nfts}) <- Available NFTS to generate')

    def Find_indexes_with_item(self, item_name, item_color):
        # Find indexes of nfts with the called item

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

    def Clean_dataframe(self):
        # Clean the dataframe to new data
        columns = [
            'nft_name',
            'background',
            'body',
            'acessory',
            'hat',
            'background_color',
            'body_color',
            'acessory_color',
            'hat_color'
        ]
        self.dataframe = pd.DataFrame(columns=columns)
        self.Save_modifications()

    def Resize_img(self):
        # Resize 'none.png' to same size of items to don't generate any errors on contenate imgs
        path, dirs, files = next(os.walk("items\\Backgrounds"))

        img = Image.open(f'items\\Backgrounds\\{files[0]}')
        img_size = img.size
        none_img = Image.open('none.png')
        resized_img = none_img.resize(img_size)
        resized_img.save('none.png', 'PNG')
        print('resized the none.png...')

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

    def Show_itens_rarity(self):
        # Print the items and it rarities
        elements = ['Backgrounds', 'Bodies', 'Acessories', 'Hats']
        
        for element in elements:
            path, dirs, files = next(os.walk(f"items\\{element}"))

            for file in files:
                file = file.replace('.png', '')
                file = file.split('-')
                self.item_name = file[0].replace('_', ' ')
                self.item_color = file[1].replace('_', ' ')
                item_indexes = self.Find_indexes_with_item(self.item_name, self.item_color)
                
                if item_indexes and self.total_nfts > 0:
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
                        self.index_background = self.counter_background
                        self.index_body = self.counter_body

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
                            self.index_acessory = self.counter_acessory
                            self.acessory_info = self.acessory_name[self.index_acessory]
                            self.acessory_info_color = self.acessory_color[self.index_acessory]

                        # Get the hat name and it color
                        if self.counter_hats == 0:
                            self.hat_info = 'None'
                            self.hat_info_color = 'None'
                        else:
                            self.index_hat = self.counter_hats
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
                        self.dataframe.reset_index(inplace=True, drop=True)
                        self.Save_modifications()
                        # Save the img
                        self.im_final.save(f'done\\nft{self.counter}.png')

                        print(f'+ Created - NFT({self.counter}/{self.total_nfts})')
                    
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

p1 = NFT_generator()