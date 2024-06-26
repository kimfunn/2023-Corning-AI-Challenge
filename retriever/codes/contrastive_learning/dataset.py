import torch
from torch.utils.data import Dataset

class DataCollator():
    def __init__(self, tokenizer, args, mode='train'):
        self.tokenizer = tokenizer        
        self.args = args
        self.mode = mode
        
    def __call__(self, samples):
        if self.mode == 'train':
            sent1 = [s['sent1'] for s in samples]
            sent2 = [s['sent2'] for s in samples]          
            encoding = self.tokenizer(sent1, padding="max_length", truncation=True, return_tensors="pt", max_length=self.args.max_length)
            encoding_ = self.tokenizer(sent2, padding="max_length", truncation=True, return_tensors="pt", max_length=self.args.max_length)

            return_value = {
                    'input_ids': encoding['input_ids'],
                    'input_ids_': encoding_['input_ids'],
                    'attention_mask': encoding['attention_mask'],
                    'attention_mask_': encoding_['attention_mask'],
                    }
            
        elif self.mode == 'valid':
            sent1 = [s['sent1'] for s in samples]
            sent2 = [s['sent2'] for s in samples]
            score = [s['score'] for s in samples]

            encoding = self.tokenizer(
                sent1,
                padding="max_length",
                truncation=True,
                return_tensors="pt",
                max_length=self.args.max_length
            )
            
            encoding_ = self.tokenizer(
                sent2,
                padding="max_length",
                truncation=True,
                return_tensors="pt",
                max_length=self.args.max_length
            )     
        
            return_value = {
                'input_ids': encoding['input_ids'],
                'attention_mask': encoding['attention_mask'],
                'input_ids_': encoding_['input_ids'],
                'attention_mask_': encoding_['attention_mask'],
                'score' : torch.tensor(score, dtype=torch.long),
            }
        return return_value


class TrainDataset(Dataset):

    def __init__(self, sent1, sent2):
        self.sent1 = sent1
        self.sent2 = sent2
    
    def __len__(self):
        return len(self.sent1)
    
    def __getitem__(self, item):
        sent1 = str(self.sent1[item])
        sent2 = str(self.sent2[item])
        
        return {
            'sent1': sent1,
            'sent2': sent2,
        }
        
class ValidDataset(Dataset):

    def __init__(self, sent1, sent2, score):
        self.sent1 = sent1
        self.sent2 = sent2
        self.score = score
    
    def __len__(self):
        return len(self.sent1)
    
    def __getitem__(self, item):
        sent1 = str(self.sent1[item])
        sent2 = str(self.sent2[item])
        score = int(self.score[item])
        
        return {
            'sent1': sent1,
            'sent2': sent2,
            'score': score,
        }
     