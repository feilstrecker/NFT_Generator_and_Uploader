# Imports
import os
import random
import pandas as pd
from NFT_Generator import NFT_generator
from NFT_Uploader import NFT_Uploader

def Gui():
    # Menu
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
            if decision == 'Y' or 'y':
                p1.Run()
            os.system('cls')

        # Upload nfts
        elif decision == '2':
            os.system('cls')
            p1 = NFT_Uploader()
            print("<------ Option: Upload Nfts ------>\n")

            # Read the dataframe
            dataframe = pd.read_csv('Nft_information.csv', index_col=0)
            # Get the nft name to type into opensea "nft_name #nft_number"
            nft_name = input('nft name: ')
            # Get the nft description
            nft_description = input('nft description: ')
            # standard start number
            start_number = 1
            # Get how many nfts have
            finish_number = len(dataframe['nft_name'].to_list())

            # Auto open chrome and connect it into selenium
            p1.Open_chrome()
            p1.Connect_chrome()
            print('(log in your wallet before)')
            # Get the collection name
            collection_name = input('collection name: ')

            # Read the dataframe and get the filenames
            dataframe = pd.read_csv('Nft_information.csv', index_col=0)
            filenames = dataframe['nft_name'].to_list()

            for i in range(start_number, finish_number):
                # Get a random nft
                choice = random.choice(filenames)
                index = filenames.index(choice)
                # Del to don't repeat the same nft
                del filenames[index]
                # Run
                p1.Run(choice, f'{nft_name} #{i}', nft_description, collection_name) 

        # Rarity nfts
        elif decision == '3':
            os.system('cls')
            p1 = NFT_generator()
            print("<------ Option: Rarity Nfts ------>\n")
            # Change the item rarity with it name and it color
            p1.Add_rarity(input('Item name: '), input('Item color: '))

        # Print rarity of nfts
        elif decision == '4':
            os.system('cls')
            p1 = NFT_generator()
            p1.Show_itens_rarity()
            
Gui()
