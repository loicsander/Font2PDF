# Font to PDF
## Scripts for Robofont & DrawBot
*DISCLAIMER*
*Robofont versions of these scripts will only work in Robofont v1.6, currently in beta, If you’re not on the beta, use [DrawBot](http://drawbot.readthedocs.org/en/latest/content/download.html)*

Here’s a series of scripts that will allow you to generate PDF files directly from a UFO file, that is, either an open font inside of Robofont, or a .ufo you load in DrawBot.


### makeProof.py

As the name indicates, this script is meant to produce proofing sheets. There’s a handful of parameters which can produce the following results (but not limited to):

+ **Print of listed glyphs**:
You provide a list, or lists (glyphNameSets) of glyphs. To have the script use the lists as reference, you must set useString to False. 
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-1.png)

+ **Print of mixed listed glyphs**:
In this case, the script still takes lists as reference but mixes all glyphs of all lists together recursively. Typically, this is meant to produce a spacing proof.
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-3.png)

+ **Print of a string**:
If useString is set to True, the script gets the glyphs to set from a string you provide (textToSet). 
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-2.png)

Basically, the script only sets type based on provided glyph names, so you it’s not limited to the use cases described here. Note, there’s obviously no word break support, this is not meant to be a proper typesetting substitute.

#### Variables
Here are the variables you might wanna change:
(point units)
+ **pageWidth**
+ **pageHeight**
+ **margin**
+ **pointSize**
+ **lineHeight**

(booleans)
+ **mix**: script makes lines of each glyph interwoven with all other glyphs in all lists. Therefore, you should be mindful of the size of your lists, or you’re in for a long wait.
+ **oneSetByPage**: sets all glyphs in a list (or mixed list) and sets next list on a new page.
+ **useKerning**
+ **showKerning**: visual display of kerning values
+ **kerningColor**: color of said visual display of kerning values (FIY: CMYK)

#### Infos
On each page, the script will also set the name of the typeface and the current style, as well as the full name of the .ufo file and a timestamp.

#### PDF Output
By Default, the script exports a PDF file of the same filename as the .ufo file. Optionaly, you can define a folder to store the PDF in, relatively to the .ufo’s path (change PDFfolder, ex: PDFfolder= '/PDF/'). The folder has to be there, the script won’t create it for you.

### compare-glyphs.py

This script takes in all given fonts (either a list of paths in DrawBot or takes all open fonts in Robofont) and makes a PDF file showing each glyph for all fonts side by side. It is akin to Ondrej Jób’s great [Font Inspector](http://urtd.net/projects/fontinspector/), only the output isn’t HTML but PDF and it’s not interactive. 

It takes it’s character set reference from the first font it can find. Typically, this is intended for master comparison in an interpolation scheme. Let’s say it’s the use case in which you’ll have no surprises (same family name & same number of characters in all fonts).

The script takes the first found font’s glyphOrder as a reference character set. But you can override it by defining your own list  (see fontKeys variable, line 22/25)

#### Page Layout

By default, the script outputs an A4 PDF. The number of columns is defined by the number of fonts input. The pointSize can be modified, it does not change dynamically based on the number of columns. It’s set to an average value yielding okay results up to 5/6 fonts compared. If you need more, you’ll have to change the pointSize yourself (you should figure it out).

![alt tag](http://www.akalollip.com/images/github/font2pdf/compare-glyphs-1.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/compare-glyphs-2.png)

You can customize the way glyphs are displayed to a certain extent. You have access to color definition for the glyph themselves (fill and stroke), the cell containing each glyph and background of the page frame (without margins).
Moreover, you can activate/deactivate display options:
+ **showGlyphBox**: the glyph’s bounding box and vertical metrics
+ **showMetrics**:  displaying metrics values (sidebearings and width)
+ **showName**: glyph name
+ **showCell**: displaying the glyph cell

#### UFO input in DrawBot
In DrawBot, the simplest way to get your UFOs in is to drag and drop the bunch of them:

![alt tag](http://www.akalollip.com/images/github/font2pdf/compare-glyphs-3.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/compare-glyphs-4.png)

#### PDF Output
The PDF file will start with a timestamp (year-month-day —> 140809) and contain the name of the family plus the names of the compared styles.