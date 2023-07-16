# for testing:
# from extract_text import *
#
# extract_text_from_pdf_using_pypdf("/Users/Yairkoren/Downloads/2111.07866.pdf")
#
# extract_text_from_webpage("https://bbc.com")
#
# extract_text_from_image("/Users/Yairkoren/Downloads/text_scan.png")
#
# extract_youtube_subtitles("azwt2pxn3UI") # Yuval Noah Harari: AI and the future of humanity | Frontiers Forum Live 2023
#
# extract_text_from_audio_file(path_to_wav_audio_file)
#
# extract_tables_from_pdf_with_pdfplumber("/Users/yairkoren/Downloads/2111.07866.pdf")


from pdfminer.high_level import extract_pages, extract_text

def extract_text_from_pdf_with_pdfminer(path_to_file: str, pages_to_process: str = 'all') :
    print(extract_text(path_to_file))
    # output=[]
    # for page_layout in extract_pages(path_to_file) :
    #     for element in page_layout:
    #         output.append(element)
    #         #print(element)
    # return output


from pix2text import Pix2Text

def extract_latex_from_formula_image(path_to_formula_image: str) :
    p2t = Pix2Text()
    text = p2t(path_to_formula_image)
    return text[0]['text']

# pip3 install tabula-py
# download java from https://www.java.com/en/download/
from tabula import read_pdf

# this will extract all tables from all pages if pages argument is blank
# tables is either a single table or a list of tables depending on the number of extracted tables
def extract_tables_from_pdf_with_tabula(path_to_file: str, pages_to_process: str = 'all') :
    acceptible_nan_rate = 0.1
    tables = read_pdf(path_to_file, pages=pages_to_process, multiple_tables=True)
    # drop tables that exceed acceptible_nan_rate
    valid_tables = tables #[ x for x in tables if x.isna().sum().sum() / x.size < acceptible_nan_rate ]
    return valid_tables


import pdfplumber

def extract_text_from_pdf_with_pdfplumnber(path_to_file: str, pages_to_process: str = 'all') :
    with pdfplumber.open(path_to_file) as pdf:
        page = pdf.pages[8]
        print(page.extract_text())

def extract_tables_from_pdf_with_pdfplumber(path_to_file: str, pages_to_process: str = 'all') :
    output = []
    acceptible_empty_rate = 0.1
    with pdfplumber.open(path_to_file) as pdf :
        for page in pdf.pages :
            tables = page.extract_tables()
            for table in tables :
                if table.count([''])/len(table) > acceptible_empty_rate :
                    continue
                output.append(table)
                for row in table:
                    print(row)
    return output

def extract_text_from_url(url: str) -> str :
    return url

import PyPDF2

def extract_text_from_pdf_using_pypdf(path_to_file: str) -> str :

    with open(path_to_file, 'rb') as pdf_file :
        reader = PyPDF2.PdfReader(pdf_file)
        # initialize output
        text = ''
        for i in range( len(reader.pages) ) :
            page = reader.pages[i]
            text += page.extract_text()

    return text


import requests
from bs4 import BeautifulSoup

def extract_text_from_webpage(url: str) -> str :

    # Make a request to the website
    r = requests.get(url)

    # Create an instance of the BeautifulSoup class to parse the page
    soup = BeautifulSoup(r.text, 'html.parser')

    # Use the 'get_text' method to extract all the text from the page
    text = soup.get_text()

    return text

import urllib
import feedparser

def get_paper_from_arxiv(query: str, attribute_type: str = 'all', max_results: str = 5) :
    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?'

    # attribute types:  'author':   'au',   'abstract':      'abs', 'comment': 'co', 'journal_reference': 'jr',
    #                   'category': 'cat',  'report_number': 'rn',  'title':   'ti', 'all_fields':        'all'

    query = urllib.parse.quote(query) # encode input in URL acceptable form (e.g. special space -> %20 escape sequence)

    query_url = f"{base_url}search_query={attribute_type}:{query}&start={0}&max_results={max_results}"

    # Parse the response using feedparser
    response = feedparser.parse(query_url)

    # Print each paper's title and the link to the pdf version
    for entry in response.entries:
        print("Title: ", entry.title)
        for link in entry.links:
            if link.type == 'application/pdf':
                print("Link: ", link.href)


# if errors occur, might need to uninstall pillow+PIL and the reinstall PIL
from PIL import Image
# to install tesseract with brew here's how to install brew: https://fb.workplace.com/groups/hack.of.the.day/permalink/1925865110834868/
# install tesseract: brew install tesseract
# to install python tesseract: pip3 install pytesseract pillow
import pytesseract

def extract_text_from_image(path_to_image_file: str) -> str :

    # Open an image file
    with Image.open(path_to_image_file) as image_file :
        text = pytesseract.image_to_string(image_file)

    return text

# brew install poppler
# brew install pdf2image
from pdf2image import convert_from_path

def convert_pdf_to_image(path_to_pdf: str) :
    pages = convert_from_path(path_to_pdf)
    for i, page in enumerate(pages) :
        page.save(f'out_{i}.jpg', 'JPEG')

# pip3 install fitz
# pip3 install pymupdf
import fitz  # this is pymupdf

def extract_images_from_pdf(path_to_pdf) :
    pdf_file = fitz.open(path_to_pdf)
    pdf_filename = os.path.basename(path_to_pdf)
    pdf_filename_no_extension = os.path.splitext(pdf_filename)[0]
    path_to_output_dir = os.path.dirname(path_to_pdf) # output is in the same directory as the pdf file

    for page_idx in range(len(pdf_file)):
        for img_idx, image in enumerate( pdf_file.get_page_images(page_idx) ) :
            # Extract the image object number
            xref = image[0]
            # Extract image
            base_image = pdf_file.extract_image(xref)
            # Store image bytes
            image_bytes = base_image['image']
            # Generate image file name
            image_name = pdf_filename_no_extension + '.' + 'p' + str(page_idx) + '.' + str(img_idx) + '.' + base_image['ext']
            #Save image
            with open(os.path.join(path_to_output_dir, image_name) , 'wb') as image_file :
                image_file.write(image_bytes)
                image_file.close()


# to convert audio file formats into wav (required for SpeechRecognition) :
# brew install ffmpeg
# then e.g., ffmpeg -i input.m4a output.wav
# or pip3 install pydub to do the conversion in python

# for speech recognition
# pip3 install SpeechRecognition
import speech_recognition as sr

def extract_text_from_audio_file(path_to_audio_file: str) -> str :
    # create an instance of the recognizer
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(path_to_audio_file) as audio_file :
        # read the entire audio file
        audio = r.record(audio_file)

    # use Google's speech recognition
    text = r.recognize_google(audio)

    return text

# pip3 install youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
# The video ID is the string after "v=" in the YouTube video URL

def extract_youtube_subtitles(video_id: str) -> str :
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    list_of_text_entries = []

    for entry in transcript :
        list_of_text_entries.append(entry['text'])
        list_of_text_entries.append("\n")
    return "".join(list_of_text_entries)

# pip3 install moviepy
# need ffmpeg installed for audio extraction from video and audio format conversion

from moviepy.editor import VideoFileClip

def extract_audio_from_video(path_to_input_video_file: str, path_to_output_audio_file: str) -> str :
    video = VideoFileClip(path_to_input_video_file)
    video.audio.write_audio(path_to_output_audio_file)

# need pydub for audio conversion in python (uses ffmpeg)
from pydub import AudioSegment
import os.path

def convert_audio_format(path_to_input_audio_file: str, path_to_output_audio_file: str) :
    output_file_extension = os.path.splitext(path_to_output_audio_file)[1][1:] # second index removes leading "."
    input_file_extension = os.path.splitext(path_to_input_audio_file)[1][1:]
    sound = AudioSegment.from_file(path_to_input_audio_file, format=input_file_extension)
    sound.export(path_to_output_audio_file, format=output_file_extension)


from pytube import YouTube

def download_audio_from_youtube(youtube_video_url: str, path_to_output_directory: str = '') :
    if path_to_output_directory == "" :
        path_to_output_directory = os.getcwd()
    youtube = YouTube(youtube_video_url)
    audio = youtube.streams.filter(only_audio=True).first()
    audio.download(path_to_output_directory)
    path_to_output_file = os.path.join(path_to_output_directory, audio.default_filename)
    return path_to_output_file

def download_video_from_youtube(youtube_video_url: str, path_to_output_directory: str = '') -> str:
    if path_to_output_directory == "" :
        path_to_output_directory = os.getcwd()
    youtube = YouTube(youtube_video_url)
    video = youtube.streams.first()  # Get the first available stream (usually the highest resolution)
    video.download(path_to_output_directory)
    path_to_output_file = os.path.join(path_to_output_directory, audio.default_filename)
    return path_to_output_file

# ask chatGPT:
# (1) how to create a google cloud service account (for the credentials file) - may need special permissions from Meta
# (2) What pip3 installable libraries are required for getting text from gdocs

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# the gdoc url is https://docs.google.com/document/d/{gdoc_id}/edit.
def extract_text_from_gdoc(gdoc_id: str) -> str :

    # need to create and enable Google drive API for the account/organization
    # need to create API key files
    path_to_credentials_file = "/Users/yairkoren/hackamonth/yair-392307-9e243d3a1ebc.json"
    # Load the credentials from the 'service_account.json' file
    creds = Credentials.from_service_account_file(path_to_credentials_file)

    # Build the service
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Get the metadata of the Google Docs file
    file = drive_service.files().get(fileId=gdoc_id).execute()

    # If the Google Docs file is not a plain text file, export it as plain text
    if file['mimeType'] != 'text/plain' :
        request = drive_service.files().export_media(fileId=gdoc_id, mimeType='text/plain')
        text = request.execute()
    else:
        document = docs_service.documents().get(documentId=document_id).execute()
        text = ' '.join([element['textRun']['content'] for element in document['body']['content']])

    return text
