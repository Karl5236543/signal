
import pickle
import os
from src.constants import BOT_DUMPS_PATH


class BotDB:
    
    def make_file_path(self, label):
        return os.path.join(BOT_DUMPS_PATH, f'{label}.pickle')
    
    def save_bot(self, label, bot):
        file_path = self.make_file_path(label)
        
        with open(file_path, 'wb') as file:
            pickle.dump(bot, file)
            
    def load_bot(self, label):
        file_path = self.make_file_path(label)
        
        with open(file_path, 'rb') as file:
            return pickle.load(file)