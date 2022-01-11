import os
import pandas as pd
from PIL import Image


class NFT_generator():

    def __init__(self):
        self.counter = 1
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

            if element == 'Background':
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
            print(filename)
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

            self.background_img_name.append(self.img_name)
            self.background_name.append(self.item_name)    
            self.background_color.append(self.item_color)
        
        # Bodies
        for filename in self.body_img_name:
            print(filename)
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

            self.body_img_name.append(self.img_name)
            self.body_name.append(self.item_name)
            self.body_color.append(self.item_color)

        # Acessories
        for filename in self.acessory_img_name:
            print(filename)
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
            
            self.acessory_img_name.append(self.img_name)
            self.acessory_name.append(self.item_name)
            self.acessory_color.append(self.item_color)  


        # Hats
            for filename in self.hat_img_name:
                print(filename)
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

                self.hat_img_name.append(self.img_name)
                self.hat_name.append(self.item_name)
                self.hat_color.append(self.item_color)
    
        
        # Total nfts Available
        self.total_nfts = self.background_amount * self.body_amount * (self.acessory_amount+1) * (self.hat_amount+1)
                
        #                          ---------------- Put itens in lists ----------------
        # Backgrounds
        self.backgrounds = self.background_img_name.copy()

        # Bodys
        self.bodies = self.body_img_name.copy()
        
        # acessorys
        self.acessories = self.acessory_img_name.copy()

        # Hats
        self.hats = self.hat_img_name.copy()

        print(f'({self.total_nfts}) <- Available NFTS to generate')
    
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
                        self.index_background = self.Find_index('background', f'{self.background_filename}{self.counter_background + 1}.png')
                        self.index_body = self.Find_index('body', f'{self.body_filename}{self.counter_body + 1}.png')

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
                            self.index_acessory = self.Find_index('acessory', f'{self.acessory_filename}{self.counter_acessory}.png')
                            self.acessory_info = self.acessory_name[self.index_acessory]
                            self.acessory_info_color = self.acessory_color[self.index_acessory]

                        # Get the hat name and it color
                        if self.counter_hats == 0:
                            self.hat_info = 'None'
                            self.hat_info_color = 'None'
                        else:
                            self.index_hat = self.Find_index('hat', f'{self.hat_filename}{self.counter_hats}.png')
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

p1 = NFT_generator()
p1.Load()