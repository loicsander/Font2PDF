# Font to PDF
## Script for Robofont
(will only work in Robofont 1.6, currently in beta)

Here’s a series of scripts that allow you to generate PDF files directly from a UFO file, that is, either an open font inside of Robofont, or a .ufo you load in DrawBot.

### makeProof.py

As the name indicates, this script is meant to produce proofing sheets. There’s a handful of parameters which can produce the following results (but not limited to):

+ **Print of listed glyphs**
You provide a list, or lists (glyphNameSets) of glyphs. To have the script use the lists as reference, you must set useString to False. 
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-1.png)

+ **Print of mixed listed glyphs**
In this case, the script still takes lists as reference but mixes all glyphs of all lists together recursively. Typically, this is meant to produce a spacing proof.
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-3.png)

+ **Print of a string**
If useString is set to True, the script gets the glyphs to set from a string you provide (textToSet). 
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-2.png)

Basically, the script only sets type based on provided glyph names, so you it’s not limited to the use cases described here. Note, there’s obviously no word break support, this is not meant to be a proper typesetting substitute.

#### PDF Output
By Default, the script exports a PDF file of the same filename as the .ufo file. Optionaly, you can define a folder to store the PDF in, relatively to the .ufo’s path (change PDFfolder, ex: PDFfolder= '/PDF/'). The folder has to be there, the script won’t create it for you.
