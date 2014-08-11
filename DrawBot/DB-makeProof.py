from robofab.world import RGlyph
from defconAppKit.tools.textSplitter import splitText
from fontTools.pens.cocoaPen import CocoaPen
from time import time
import datetime
now = datetime.datetime.now().strftime('%d %B %Y - %H:%M')

### SETTINGS ####

ufoPath = ""

# (left, top, right, bottom)
margins = (50, 50, 50, 50)
preset = 'A4-P' # A4-L, A4-P, A3-L, A3-P
showFrame = False
footer = True

# if no folder or filename is defined
# and if PDF is set to True,
# script issues a PDF next to the font file
# width the same name and a _PROOF suffix
PDF = False
PDFfolder = None
PDFfileName = None

pointSize = 12
_line_Height = 1.4
tracking = 0

# use 3 values if you want RVB
# use 4 values if you wan CMYK
color = (0, 0, 0, 1)
# if you use transparency
# script will assume it’s to see the outline
# it’ll add stroke to the glyphs
alpha = 1

# usual suffix stuff: .small, .alt, etc.
suffix = []

useKerning = True
showKerning = False
showGlyphBox = False

useString = True
text2print = [
#    (text to print, wrapWords:True/False)
#    each new list element goes on a new page
#    (open('foo.txt').read(), True),
    ('Tart Tool\nATAVISME\nWhatever', True),
    ]
 
# if useString is set to False and mix is set to True
# script process glyphLists and interweaves all glyphs in all contained lists
mix = False   
glyphLists = [
    ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'ae', 'oe', 'eth', 'thorn'],    ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', 'AE', 'OE', 'Eth', 'Thorn'],
    ['one','two','three','four','five','six','seven','eight','nine'],
    ['one.LP','two.LP','three.LP','four.LP','five.LP','six.LP','seven.LP','eight.LP','nine.LP']
    ]

# font used for the page stamp
# has to be an installed font
# has to be name by it’s poscript name
# use installedFonts() to get the full list of installed fonts on your system
infoFont = ''

#################
#################

def _drawGlyph(thisFont, glyph):
    pen = CocoaPen(thisFont)
    glyph.draw(pen)
#    path = glyph.naked().getRepresentation("defconAppKit.NSBezierPath")
    drawPath(pen.path)

class TypeSetter(object):
    
    def __init__(self, thisFont):
        if thisFont is None:
            return
        self.thisFont = thisFont    
        self.cmap = thisFont.getCharacterMapping()
        self.getGroups = thisFont.groups.findGlyph
        self.kerning = thisFont.kerning
        self.preset = 'A4-P'
        self.type = {
            'size':96,
            '_line_Height':1.4,
            'tracking': 0,
            'color': (0, 0, 0, 1),
            'alpha': 1
            }
        self.canvas = {
            'posSize':(0, 0, 300, 500),
            # left top right bottom
            'margins':(0, 0, 0, 0),
            'scale':1,
            'preset': self.presetFormat
            }
        self.settings = {
            'suffix': [],
            'infoFont': None,
            'useKerning': False,
            'showKerning': False,
            'showGlyphBox': False,
            'showFrame': False
            }
        self.formats = {
            # sizes in points
            'A4-P':(595.276, 841.89),
            'A4-L':(841.89, 595.276),
            'A3-P':(841.89, 1190.551),
            'A3-L':(1190.551, 841.89)
            }
            
            
    def showFrame(self):
        stroke(.75)
        fill()
        rect(*self.canvas['posSize'])
        stroke()
        
        
    def pageStamp(self):
        font(self.settings['infoFont'])
        x, y, width, height = self.canvas['posSize']
        fileName = self.fileInfo()[1]
        fontName = self.thisFont.info.familyName + u' – ' + self.thisFont.info.styleName
        save()
        fontSize(7)
        fill(0)
        translate(x, y/2)
        column = width/7
        textBox(fontName, (0, 0, 2*column, 10))
        textBox(fileName, (2*column, 0, 3*column, 10), 'center')
        textBox(now, (5*column, 0, 2*column, 10), 'right')
        restore()
      
            
    def presetFormat(self, reference):
        if self.formats.has_key(reference):
            left, top, right, bottom = self.canvas['margins']
            pageSize = self.formats[reference]
            self.canvas['posSize'] = (left, bottom, pageSize[0]-(left+right), pageSize[1]-(bottom+top))
            self.preset = reference
            
    def fileInfo(self):
        thisFont = self.thisFont
        fileName = thisFont.path.split('/')[-1]
        filePath = thisFont.path.rstrip(fileName)
        return filePath, fileName
        
        
    def savePDF(self, name=None, path=None):
        fileInfo = self.fileInfo()
        if name is None:
            name = fileInfo[1].rstrip('.ufo')
        if path is None:
            path = fileInfo[0]
        path.rstrip('/')
        name.lstrip('/')
        fileToSave = path + '/' + name + '_PROOF' + '.pdf'
        saveImage(fileToSave)
        
        
    def getKernGroups(self, glyphRecord):
        thisFont = self.thisFont
        getGroups = self.getGroups
        fontKeys = thisFont.keys()
        glyphRecord = set(glyphRecord)
        return {gn:getGroups(gn) for gn in glyphRecord if gn in fontKeys}
        
    
    def stringToGlyphs(self, text):
        glyphRecord = []
        cmap = self.cmap
        text = unicode(text, 'utf8')
        lines = text.split('\n')
        for line in lines:    
            glyphRecord += splitText(line, cmap)
            glyphRecord.append('\n')
        glyphRecord.pop()     
        return glyphRecord


    def set(self, glyphInput, keepWords=False):
        thisFont = self.thisFont
        kerning = self.kerning
        fontKeys = thisFont.keys()
        if isinstance(glyphInput, str):
            glyphRecord = self.stringToGlyphs(glyphInput)
        elif isinstance(glyphInput, list):
            glyphRecord = glyphInput

        suffixes = self.settings['suffix']
        if len(suffixes) > 0:
            for i, glyphName in enumerate(glyphRecord):                  
                for suffix in suffixes:
                    if glyphName + suffix in fontKeys:
                        glyphRecord[i] = glyphName + suffix

        kernGroups = self.getKernGroups(glyphRecord)
        nbrOfGlyphs = len(glyphRecord)
        UPM = thisFont.info.unitsPerEm
        descender = thisFont.info.descender
        ascender = thisFont.info.ascender
        capHeight = thisFont.info.capHeight
        xHeight = thisFont.info.xHeight
        
        pointSize = self.type['size']
        _line_Height = self.type['_line_Height'] 
        tracking = self.type['tracking'] 
        color = self.type['color'][0:]
        alpha = self.type['alpha']
        x, y, width, height = self.canvas['posSize']
        
        sc = pointSize/UPM
        xAdvance = yAdvance = 0
        kerningValue = 0
        # exceed allowance: to which extent can a word go beyond bounds
        eA = 0.97
        wordLetterOffset = 0
        spaceWidth = thisFont['space'].width
        glyphGroups = []
        previousGlyph = None
        previousGlyphGroups = []
        wordGlyph = RGlyph()
        wordGlyph.name = ''
        glyphDrawingTime = 0
        wordKerning = []
       
        useKerning = self.settings['useKerning'] 
        showKerning = self.settings['showKerning'] 
        showGlyphBox = self.settings['showGlyphBox'] 
        showFrame = self.settings['showFrame']
        pageStamp = self.settings['pageStamp']

        newPage(*self.formats[self.preset])

        if showFrame: self.showFrame()
        if pageStamp: self.pageStamp()

        # compensate for upward y coordinates
        xPos = x
        yPos = y + height - ((UPM+descender)*sc)
        translate(xPos, yPos)

        for i, glyphName in enumerate(glyphRecord):
            
            # filtering missing glyphs
            if (glyphName not in fontKeys) and (glyphName != '\n'):
                if '.notdef' in fontKeys:
                    glyphName = '.notdef'
                else: continue
          
            # skip spaces at the start of a new line  
            if (glyphName == 'space') and (xAdvance == 0) and (wordLetterOffset == 0):
                continue
            
            if glyphName != '\n':
                glyph = thisFont[glyphName]
            
            # check for need of a new line
            if ((glyphName == '\n') and (not keepWords)) or \
               (xAdvance + (glyph.width*sc*eA) >= width):
                xAdvance = 0
                kerningValue = 0
                yAdvance += (UPM*_line_Height)*sc
                _newLine = False
                previousGlyph = None
                previousGlyphGroups = None
                if (glyphName == '\n'):
                    continue
                    
            # kerning
            if glyphName in kernGroups.keys():
                glyphGroups = kernGroups[glyphName]
                # filter out non kern groups
                glyphGroups = [group for group in glyphGroups if ('MMK' in group) or ('kern' in group)]

                if (previousGlyph is not None) and useKerning:
                    for group in glyphGroups:
                        for prevGroup in previousGlyphGroups:
                            if kerning[(prevGroup,group)] is not None:
                                kerningValue = kerning[(prevGroup,group)]
                
            glyphStart = time()
                
            # if word wrap
            if keepWords:
                # add each glyph of a word to the wordGlyph and skip the drawing
                # add metrics of each glyph to the wordGlyph
                if (glyphName != 'space') and (glyphName != '\n') and (i < nbrOfGlyphs-1):
                    
                    # draw kerning if word wrap
                    if showKerning and (kerningValue != 0):
                        save()
                        scale(sc)
                        fill(1, 0, 0, 0.5)
                        thisKern = BezierPath()
                        thisKern.moveTo((wordLetterOffset, descender))
                        thisKern.lineTo((wordLetterOffset, ascender))
                        thisKern.lineTo((wordLetterOffset + kerningValue, ascender))
                        thisKern.lineTo((wordLetterOffset + kerningValue, descender))
                        thisKern.closePath()
                        wordKerning.append(thisKern)
                        restore()
                    
                    wordGlyph.appendGlyph(glyph, (wordLetterOffset + kerningValue, 0))
                    wordGlyph.width += (glyph.width + tracking + kerningValue)
                    wordGlyph.name += glyphName
                    wordLetterOffset += (glyph.width + tracking + kerningValue)
                    previousGlyph = glyph
                    previousGlyphGroups = glyphGroups
                    kerningValue = 0
                    
                    continue
                    
                # when a space is hit, or if it’s the end of the text
                # the wordglyph is passed as main glyph to be drawn
                # check if the word doesn’t exceed boundaries
                elif (glyphName == 'space') or (glyphName == '\n') or (i == nbrOfGlyphs-1):
                    if (i == nbrOfGlyphs-1) and (glyphName != '\n'):
                        wordGlyph.appendGlyph(glyph, (wordLetterOffset + kerningValue, 0))
                        wordGlyph.width += (glyph.width + tracking)
                        wordGlyph.name += glyphName
                    if glyphName != '\n':
                        previousGlyph = glyph
                        previousGlyphGroups = glyphGroups
                    glyph = wordGlyph
                    wordGlyph = RGlyph()
                    wordGlyph.name = ''
                    wordLetterOffset += tracking + kerningValue
                    if (xAdvance + (glyph.width*sc*eA) >= width):
                        xAdvance = 0  
                        kerningValue = 0
                        yAdvance += (UPM*_line_Height)*sc
                        
            # check for need of a new page   
            if yAdvance + (UPM*sc) >= height:
                newPage()
                if showFrame: self.showFrame()
                if pageStamp: self.pageStamp()
                translate(xPos, yPos)
                xAdvance = 0
                yAdvance = 0
                kerningValue = 0
            
            
            # Drawing, yay!
            save()
            if not keepWords:
                translate(xAdvance + (kerningValue*sc), -yAdvance)
            elif keepWords:
                translate(xAdvance, -yAdvance)
            scale(sc)
            
            # draw kerning if no word wrap
            if showKerning:
                save()
                fill(1, 0, 0, 0.5)
                if not keepWords:
                    if kerningValue > 0:
                        fill(.2, .9, 0, 0.5)
                    rect(0, descender, -kerningValue, UPM)
                elif keepWords:
                    for kern in wordKerning:
                        drawPath(kern)
                wordKerning = []
                restore()
                
            # draw glyphBox
            if showGlyphBox:
                glyphWidth = glyph.width
                save()
                fill()
                stroke(.5)
                rect(0, descender, glyphWidth, UPM)
                for h, c in [(0, (.5,)), (xHeight,(.5, .9, 0)), (capHeight,(.1, .4, .9))]:
                    stroke(*c)
                    line((0, h), (glyphWidth, h))
                restore()
                
            # glyph color    
            if len(color) == 3: 
                fill(*color + (alpha,))
                if alpha < 1: stroke(*color)
            elif len(color) == 4: 
                cmykFill(*color + (alpha,))
                if alpha < 1: cmykStroke(*color)
            else:
                fill(0)
                if alpha < 1:stroke(0)
            
            _drawGlyph(thisFont, glyph)
            
            if not keepWords:
                xAdvance += (glyph.width + tracking + kerningValue)*sc
                kerningValue = 0
                previousGlyph = glyph
                previousGlyphGroups = glyphGroups
            elif keepWords and (glyphName != '\n'):
                xAdvance += (wordLetterOffset + spaceWidth + kerningValue)*sc
                wordLetterOffset = 0 
                kerningValue = 0
                previousGlyph = glyph
                previousGlyphGroups = glyphGroups
            elif keepWords and (glyphName == '\n'):
                xAdvance = 0
                kerningValue = 0
                wordLetterOffset = 0
                yAdvance += (UPM*_line_Height)*sc
                previousGlyph = None
                previousGlyphGroups = None
            
            restore()
            
            glyphStop = time()
            glyphDrawingTime += (glyphStop-glyphStart) * 1000
            
        print 'average glyph drawing %0.2f ms, total %0.2f ms, %s glyphs drawn' % (glyphDrawingTime/nbrOfGlyphs, glyphDrawingTime, nbrOfGlyphs)

from robofab.world import OpenFont        

thisFont = OpenFont(ufoPath) 

typeSetter = TypeSetter(thisFont)
typeSetter.canvas['margins'] = margins
typeSetter.canvas['preset'](preset)

typeSetter.type['size'] = pointSize
typeSetter.type['_line_Height'] = _line_Height
typeSetter.type['tracking'] = tracking
typeSetter.type['color'] = color
typeSetter.type['alpha'] = alpha

typeSetter.settings['suffix'] = suffix
typeSetter.settings['infoFont'] = infoFont
typeSetter.settings['useKerning'] = useKerning
typeSetter.settings['showKerning'] = showKerning
typeSetter.settings['showGlyphBox'] = showGlyphBox
typeSetter.settings['showFrame'] = showFrame
typeSetter.settings['pageStamp'] = footer

start = time()

if useString:
    for string, wrapWords in text2print:
        typeSetter.set(string, wrapWords)
        
elif not useString:
    
    if mix:
        glyphSet = []
        fontKeys = thisFont.keys()
        for gl1 in glyphLists:
            for gl2 in glyphLists:
                if len(gl1) > 0 and len(gl2) > 0:
                    for gn1 in gl1:
                        if gn1 in fontKeys:
                            for gn2 in gl2:
                                if gn2 in fontKeys:
                                    glyphSet.append(gn1)
                                    glyphSet.append(gn2)
                            glyphSet.append('\n')
        typeSetter.set(glyphSet)
    elif not mix:        
        for glyphSet in glyphLists:
            typeSetter.set(glyphSet)

stop = time()
print 'page set in %0.2f ms' % ((stop-start)*1000)

if PDF: typeSetter.savePDF(PDFfileName, PDFfolder)