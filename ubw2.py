import requests, re, os, logging
from reportlab.pdfgen import canvas
from PIL import Image

# Params

FILLLEVEL = {
    'cover' : 3,
    'legal_info' : 3,
    'main' : 6,
    'index' : 5,
}

PREFIX = {
    'cover' : 'cov',
    'legal_info' : 'leg',
    'index' : '!',
    'main' : ''
}

def file_list_sort(l):
    for i in range(len(l)):
            l[i] = l[i].split('.')    
            l[i][0] = int(l[i][0])
    l.sort()
    for i in range(len(l)):
            l[i][0] = str(l[i][0])
            l[i] = l[i][0] + '.' + l[i][1]
    return l

class Downloader():
    def __init__(self, reader_addr, save_path, debug = True):

        self.debug = debug
        self.reader_addr = reader_addr
        self.save_path = save_path.rstrip('/') + '/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        # create logger
        self.logger = logging.getLogger('downloader')
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        self.ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(self.ch)

        self.logger.info('Analyzing, please wait ...')

        # Verify save path
        if not os.path.isdir(self.save_path):
            self.logger.error("Error: invalid save path")
            return None

        # Analyze image link
        r = requests.get(self.reader_addr)
        contents = r.text.encode('utf-8')
        if self.debug:
            if os.path.exists(self.save_path + 'log') != True:
                os.mkdir(self.save_path + 'log')
            file = open(self.save_path + 'log/reader.html', 'w+')
            file.write(contents)

        match = re.search(r"(var str\=\')(.*)(\')", contents)
        #match = re.search(r".*var str(.*)\'.*", str1)
        if match:
            result = match.group(0)
            trimmed = result.lstrip("var str='")
            trimmed = trimmed.rstrip("'")
            self.link = trimmed
            self.logger.info('Resource link extracted:' + self.link)
        else:
            self.logger.error('Analysis failed. No match found.')

        self.logger.debug('Init OK.')

    def _getSingle(self, prefix, fill_level, page):

        self.logger.info('Requesting Image:' + prefix + str(page))
        request =  requests.get(self.link + prefix + str(page).zfill(fill_level) + '.jpg')
        if request.headers.get('Content-length'):
            contents = request.content
            if prefix == '':
                prefix = 'main'
            if os.path.exists(self.save_path + prefix) != True:
                os.mkdir(self.save_path + prefix)
            file = open(self.save_path + prefix + '/' + str(page) + '.jpg', 'wb+')
            file.write(contents)
            log = 'Image ' + prefix + str(page) + " requested."
            self.logger.info(log)
            success = True

        else:
            log = 'Failed to download image ' + prefix + str(page) + "."
            self.logger.warning(log)
            success = False

        if self.debug:
            log_file = open(self.save_path + 'log/log.txt', 'a')
            log_file.write(log + '\n')

        return success

    def download(self, page_type, start_page = 1, end_page = None):

        if end_page == None:
            success = True
            page = start_page
            while(success):
                self.logger.warning('Predict mode on!')
                success = self._getSingle(PREFIX[page_type], FILLLEVEL[page_type], page)
                page = page + 1

        else:
            for page in range(start_page, end_page + 1):
                self._getSingle(PREFIX[page_type], FILLLEVEL[page_type], page)

class Merge:
    def __init__(self, pdf_file_name, size = None):
        self.canvas = canvas.Canvas(pdf_file_name, size)

    def addPage(self, img_file_name):
        self.canvas.drawImage(img_file_name, 0, 0)
        self.canvas.showPage()

    def save(self):
        self.canvas.save()


def mergeAll(img_save_path, book_save_path):
    print("Making PDF, please wait...")
    img_save_path = img_save_path.rstrip('/') + '/'
    if os.path.isfile(img_save_path + 'main/1.jpg'):
        sample_img = Image.open(img_save_path + 'main/1.jpg')
        page_size = sample_img.size
        merger = Merge(book_save_path, size = page_size)
    else:
        return False

    job_list = ['cover', 'legal_info', 'index', 'main']

    for job in job_list:
        prefix = PREFIX[job]
        suffix = ''
        if job == 'main':
            prefix = 'main'
        file_list = file_list_sort(os.listdir(img_save_path + prefix))
        for file in file_list:
            path = img_save_path + prefix + '/' + file
            merger.addPage(path)      

    merger.save()
    print("PDF generated successfully!")



if __name__ == '__main__':
    print('====================UBW2 Lite Beta Version====================')
    print('\n')
    reader_name = raw_input('Input the reader address of the book:\n')
    save_path = raw_input('Specify the name of the destination directory:\n')
    book_name = raw_input("Input the name(format: directory/name) of the book(optional): Press Enter to skip\n")
    begin_page = input("Input the beginning page number: Must be a number\n")
    end_page = input("Input the ending page number: 0/Number\n")
    if book_name == '':
        book_name = 'book.pdf'
    if end_page == 0:
        end_page = None
    raw_input("Info collecting done. Press ENTER to trace.")
    print('====================Trace On!====================')
        

    downloader = Downloader(reader_name, save_path)
    downloader.download('cover')
    downloader.download('legal_info')
    downloader.download('index')
    downloader.download('main', start_page = begin_page, end_page = end_page)
    mergeAll(save_path, book_name)
        
    