# Font to PDF
## Scripts for Robofont & DrawBot
*DISCLAIMER*
*Robofont versions of these scripts will only work in Robofont v1.6, currently in beta, If you’re not on the beta, use [DrawBot](http://drawbot.readthedocs.org/en/latest/content/download.html)*

Here’s a series of scripts that will allow you to generate PDF files directly from a UFO file, that is, either an open font inside of Robofont, or a .ufo you load in DrawBot.


## makeProof.py

As the name indicates, this script is meant to produce proofing sheets. You can feed text, or glyphs, to the script by two means. Either you provide strings (text), or lists of glyphs.

```python
# strings
useString = True
text2print = [
	(open('foo.txt').read(), True),
	('Tart Tool\nATAVISME\nWhatever', True),
    ]
 
# glyph lists
mix = True   
glyphLists = [
	['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],    ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
```

#### Strings
If you provide strings (even if only one), you should put them in a list. Each item in the list is an indication that you want this text set on a separate page.
For each defined string, you must also define a boolean in the form of a tuple —> ('abc123', True). This boolean determines if words are to be wrapped or if text is broken in lines anywhere (not respect for words).
Working with strings makes it easy to import text, which you can do through a separate text file.

if strings or lists are used is determined by:

```python
useString = True # or False
```

#### Lists
If you work with lists (which will allow you to use specific glyph names), the same happens. Each item of the list is set on a separate page, except if the mix variable is set to True. In that case, all lists are mixed to produce a typical spacing sheet (abacadaeafaga…) . You should be mindful of the size and number of your lists if you intend to mix them; otherwise it could take a little while…

![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-9.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-4.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-5.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-6.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-7.png)
![alt tag](http://www.akalollip.com/images/github/font2pdf/makeProofingSheets-8.png)

#### Options

Independently of the input method you choose, there’s a bunch of parameters you can define. They’re all gathered at the top of the script for convenience.

##### Page definition
```python
margins = (50, 50, 50, 50)
preset = 'A4-P'
showFrame = False
footer = True
```
There are presets to defined size and orientation of the page. By default, I added A4 & A3 as base formats, but you can add yours yourself (see .formats in the TypeSetter class). For each format, you can chose between portrait or landscape orientation (A4-P or A4-L). You also have control over the size of margins and if you want a footer applied to the pages (displaying the name of the typeface + style, name of the ufo file and date.

##### Page output
```python
PDF = True
PDFfolder = '/myFolder/'
PDFfileName = 'myFile'
```
If you set the PDF variable to True, the script issues a PDF file with a name identical to the source ufo file,  and a _PROOF suffix. Except if you specify the filename you wish. You can also specify a target folder which by default is the same as the ufo.

##### Type
```python
pointSize = 96
_line_Height = 1.3
tracking = 0
color = (0, 0, 0, 1)
alpha = 1
```

NB: depending on how you input color, it will be RGB or CMYK (3 or 4 parameters). You can define alpha transparency separately, which results in a revealing of the outline (the script adds stroke to the outline automatically if alpha transparency is < 1.

##### Features
```python
suffix = []
```
You can define suffixes for substitution of glyphs (.small, .alt, etc.)

```python
useKerning = True
showKerning = True
showGlyphBox = False
```

These variable names are quite straightforward I think. showGlyphBox displays the bounding box of glyphs as well as their vertical metrics.

##### Misc
```python
infoFont = ''
```
Here you can define the name of a font for the footer information. The name has to be a postscript name, you can get the full list of installed fonts with the installedFonts() function of DrawBot (it provides you with the names you have to use so that DrawBot use the proper font).

## compare-glyphs.py

This script takes in all given fonts (either a list of paths to UFO files in DrawBot or takes all open fonts in Robofont) and makes a PDF file showing each glyph for all fonts side by side. It does a similar job to Ondrej Jób’s great [Font Inspector](http://urtd.net/projects/fontinspector/), only the output isn’t HTML but PDF and it’s not interactive. 

It takes it’s character set reference from the first font it can find. Typically, this is intended for master comparison in an interpolation scheme. Let’s say it’s the use case in which you’ll have no surprises (same family name & same number of characters in all fonts).

The script takes the first found font’s glyphOrder as a reference character set. But you can override it by defining your own list  (see userGlyphKeys variable, line 40/36)

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

## charset.py

A simpler variation of compare-glyphs.py that outputs a pdf with all glyphs of a single font. Same options apply (showMetrics, etc.).

![alt tag](http://www.akalollip.com/images/github/font2pdf/charset-1.png)