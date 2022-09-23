# tesseract_ocr
 
The task was to scrape data from FINRA's website for all Case IDs/Awards between the years 2007 and 2012(inclusive of both): https://www.finra.org/arbitration-mediation/arbitration-awards
The task was split into multiple files for two reasons: 
1) Some of the information can be extracted directly from the website by using the requests package.
2) The detailed information about each case is available only in the pdfs attached with each Case ID/Award.
3) Each pdf is several pages long and containes scanned images of the transcripts of that particular case. Hence, OCR needs to be performed on each pdf, convert it to text and look for specific fields/ information required to populate the database.
