from drawBot import *
from defconAppKit.tools.textSplitter import splitText
from time import time
import datetime
now = datetime.datetime.now().strftime('%d %B %Y - %H:%M')
    
def _drawGlyph(glyph):
    path = glyph.naked().getRepresentation("defconAppKit.NSBezierPath")
    drawPath(path)
    
# timestamp

def pagestamp():
    save()
    font('')
    fontSize(7)
    fill(0)
    translate(bounds[3], 20)
    tbwidth = (bounds[1])/6
    textBox(fontName, (0, 0, 2*tbwidth, 10))
    textBox(fileName, (2*tbwidth, 0, 3*tbwidth, 10), 'left')
    textBox(now, (5*tbwidth, 0, tbwidth, 10), 'right')    
    restore()
            
### ACTUAL SCRIPT START

f = CurrentFont()

fontName = f.info.familyName + u' – ' + f.info.styleName
fileName = f.path.split('/')[-1]
filePath = f.path.rstrip(fileName)
UPM = f.info.unitsPerEm
xHeight = f.info.xHeight
capHeight = f.info.capHeight
ascenders = f.info.ascender
descender = f.info.descender
fontKeys = f.keys()
getGroups = f.groups.findGlyph
kerning = f.kerning
cmap = f.getCharacterMapping()

## SETUP

# A4 = (595.276, 841.89)
pageWidth = 595.276
pageHeight = 841.89
PDFfolder = ''

margin = 40
pointSize = 12
lineHeight = 1.4
sc = pointSize/UPM
# bounds = top right bottom left
bounds = (pageHeight-(2*margin)-UPM*sc, pageWidth-(2*margin), margin, margin)

# This variable results in a interweaving of all glyphs in all sets, so be careful!
# If you have sizeable lists this may impact the execution time of the script.
# For instance, mixing a-z, A-Z and 0-9 takes approximately 5 seconds.
mix = True
##
useString = False
oneSetByPage = False
useKerning = True
showKerning = False
kerningColor = (0, 1, 1, 0, .5)

textToSet = u'whatever'

glyphNameSets = [
['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'ae', 'oe', 'eth', 'thorn'],    ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', 'AE', 'OE', 'Eth', 'Thorn'],
['one','two','three','four','five','six','seven','eight','nine'],
['one.LP','two.LP','three.LP','four.LP','five.LP','six.LP','seven.LP','eight.LP','nine.LP']
]

## MAKING THE GLYPHSET

# filter out glyphNames not present in font
glyphNameSets = [[gn for gn in gns if gn in fontKeys] for gns in glyphNameSets]
glyphSet = []
    
if not useString:
    kernGroups = {gn: getGroups(gn) for gns in glyphNameSets for gn in gns}
    kernGroups['space'] = getGroups('space')

    # concatenate each glyph of a list with each glyph of every other list
    start = time()

    if mix:
        for gns1 in glyphNameSets:
            for gns2 in glyphNameSets:
                if len(gns1) > 0 and len(gns2) > 0:
                    for gn1 in gns1:
                        for gn2 in gns2:
                            glyphSet.append(gn1)
                            glyphSet.append(gn2)
                        glyphSet.append('\n')
                    if oneSetByPage:
                        glyphSet.append('\nP')
                
    elif not mix:
        for gns in glyphNameSets:
            glyphSet += [gn for gn in gns]
            if oneSetByPage:
                glyphSet.append('\nP')
                continue
            glyphSet.append('\n')
        if oneSetByPage:
            glyphSet.pop()
        
    # clear glyphSet of trailing \n & \nP
    glyphSet = glyphSet[:-2]
    
    stop = time()
    print "glyphSet concatenation in %0.2f ms." % ((stop-start) * 1000)
            
elif useString:
    lines = textToSet.split('\n')
    for line in lines:    
        glyphSet += splitText(line, cmap)
        glyphSet.append('\n')
    singleGlyphs = set(glyphSet)
    kernGroups = {gn: getGroups(gn) for gn in glyphSet if gn != '\n'}
    kernGroups['space'] = getGroups('space')

# BUILDING/DRAWING PAGE/S

start = time()
xAdvance = yAdvance = 0

newPage(pageWidth, pageHeight)
pagestamp()
translate(bounds[3], bounds[2]+bounds[0])
kernFetchTime = 0
checkedPairs = 0
glyphDrawingTime = 0
previousGlyph = None

for i, glyphName in enumerate(glyphSet):
    
    if glyphName == ' ': glyphName = 'space'
    
    # new line
    if ((glyphName != '\n') and (glyphName != '\nP') and (xAdvance + f[glyphName].width*sc >= bounds[1])) or \
       (glyphName == '\n'):
    
        yAdvance += (UPM*lineHeight)*sc
        xAdvance = 0
        previousGlyph = None
    
    # new page
    if (yAdvance >= bounds[0]) or (glyphName == '\nP'):
        newPage(pageWidth, pageHeight)
        pagestamp()
        translate(bounds[3], bounds[2]+bounds[0])
        yAdvance = 0
        xAdvance = 0
        previousGlyph = None
    
    if (glyphName == '\n') or (glyphName == '\nP'):
        # new line or new page = skip the kern-fetching & drawing
        continue
        
    # Kerning
    kerningValue = 0    
    kernStart = time()
    
    if glyphName in kernGroups.keys():
        glyphGroups = kernGroups[glyphName]
        # filter out non kern groups
        glyphGroups = [group for group in glyphGroups if 'kern' in group]
    
        if (previousGlyph is not None) and useKerning:
        
            for group in glyphGroups:
                for prevGroup in previousGlyphGroups:
                    if kerning[(prevGroup,group)] is not None:
                        kerningValue = kerning[(prevGroup,group)] * sc
                            
    kernStop = time()
    kernFetchTime += (kernStop-kernStart) * 1000
    
    # Drawing
    save()
    translate(xAdvance + kerningValue, -yAdvance)

    scale(sc)
    #fill(0)
    if showKerning:
        cmykFill(*kerningColor)
        rect(0, -100, -kerningValue/sc, 1100)
    cmykFill(0, 0, 0, 1)
    glyphStart = time()
    glyph = f[glyphName]
    _drawGlyph(glyph)
    
    glyphStop = time()
    
    restore()
    
    xAdvance += (glyph.width*sc) + kerningValue
    previousGlyph = glyph
    previousGlyphGroups = glyphGroups

    glyphDrawingTime += (glyphStop-glyphStart) * 1000
    
    
stop = time()
print "page drawing in %0.2f ms." % ((stop-start) * 1000)
#print timecheck
print 'average glyph kerning fetched in %0.2f ms' % ((kernFetchTime/len(glyphSet)))
print 'average glyph drawing %0.2f ms, %s glyphs drawn' % ((glyphDrawingTime/len(glyphSet)), len(glyphSet))

fileURL = filePath + PDFfolder + fileName.rstrip('.ufo') + '.pdf'
saveImage(fileURL)