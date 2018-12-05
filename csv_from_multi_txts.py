import os
import csv
# Start with loading in our txt files and examening them

def csv_from_txts(path, filename='text.csv'):
    
    txts = [f for f in os.listdir(path) if f.endswith('.txt')]
    with open(path+filename, 'a', newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        for txt in txts:
            with open(path+txt, 'r') as txt_file:
                content = txt_file.readline()
                writer.writerow([os.path.basename(txt), content])

    print(f'All files in {path} processed and saved as {filename}')

csv_from_txts('movie_reviews/datasets/aclImdb/test/testr/', 'test.csv')
