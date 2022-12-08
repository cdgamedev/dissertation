import pytesseract
import re

# important consts for program to know
IMAGE_COUNT = 165
DATASET_NAME = "Dataset 1 - 08.09.2022.csv"
INPUT_DATA_LOCATION = "output-screenshots"

# tesseract specific configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
custom_oem_psm_config = r'''
-c tessedit_char_whitelist="01234567890TierLvl,. "
-c preserve_interword_spaces=1x1
--oem 3 --psm 6'''

# ensure user knows they are about to overwrite all data from previously
i = input("Continuing will clear existing data. Would you like to continue? [Y/N] ")
if (i == "Y"):
    # clear all data
    output = open(DATASET_NAME, "w+")
    output.write("Page,EntryNo,Level,Tier,Cost,Date\n")
    output.close()
else:
    # exit program
    log = "Input not recognised. Exiting program."
    if (i == "N"):
        log = "Exiting program."
    
    print(log)
    exit()

# gem class to store info about gems
class Gem():
        
    # when creating a new class
    def __init__(self, page = "-", entry_no = "-", level = "-", tier= "-", cost="-", date="-"):
        self.page = page
        self.entry_no = entry_no
        self.level = level
        self.tier = tier
        self.cost = cost
        self.date = date
    
    # convert gem stucture to a string
    def __str__(self) -> str:
        return r"{0},{1},{2},{3},{4},{5}".format(self.id, self.page, self.entry_no, self.level, self.tier, self.cost, self.date)

# get the data in rows
def get_data_rows(ocr):
    # the minimum characters for the row to be counted
    min_row_characters = 10
    
    # split with regex of new line
    rows = re.split(r'\n+', ocr)
    
    # create a new array for cleaner rows
    filtered_rows = []
    
    # only get rows which are within the threshold
    for row in rows:
        #print(len(row))
        if (len(row) > min_row_characters):
            filtered_rows.append(row)
    
    # return the cleaned rows
    return filtered_rows

# function to get the gem data
# passes through the entry number
# passes through the row to get the data from
def get_gem_data(number, row):
    # get the row data by splitting entries with >=2 space characters
    row = re.split(r"\s{2,}", row)
    
    filter_level  = r'Level'
    filter_tier = r'er \d'
    filter_date = r'\d\d\d\d.\d\d.\d\d'
    filter_cost = '\d{1,3}[\,.]{1}\d{1,3}|\d{1,3}'
    
    # create a new gem using the page number and index number
    gem = Gem(page, number)
    
    # for all the cells in the row
    for cell in row:
        cell = cell.replace(',', '')
        
        # check through cell with each filter and process accordingly
        if re.search(filter_level, cell):
            gem.level = handle_level(cell)
        elif re.search(filter_tier, cell):
            gem.tier = handle_tier(cell)
        elif re.search(filter_date, cell):
            gem.date = handle_date(cell)
        elif re.search(filter_cost, cell):
            gem.cost = handle_cost(cell)
        else:
            print(r"Data issue: {0}".format(cell))
            
    return str(gem)

def handle_level(level):
    number = re.search('\d+', level).group(0)
    if (int(number) > 10):
        number = number[0]
    level = "Level " + number
    
    return level

def handle_tier(tier):
    return tier

def handle_date(date):
    return date

def handle_cost(cost):
    cost = re.sub('\D', '', cost)
    return cost

def parse_string_data(ocr):
    data_rows = get_data_rows(ocr)
    gem_list = []
    
    for i in range(len(data_rows)):
        row = data_rows[i]
        gem_list.append(get_gem_data(i + 1, row))
    
    output = open(DATASET_NAME, "a")
    
    output.write('\n'.join(gem_list))
    output.write('\n')
    
    output.close()
    
    return "[SUCCESS] {0}\n".format(page)

for page in range(1, IMAGE_COUNT + 1):
    page_id = r"page_{0}.png".format(page)
    ocr = pytesseract.image_to_string(r"{0}\{1}".format(INPUT_DATA_LOCATION, page_id), config=custom_oem_psm_config)
    
    text_data = parse_string_data(ocr)
    print(text_data)
    
output.close()