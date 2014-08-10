import datetime
from robofab.world import OpenFont
from robofab.interface.all.dialogs import AskString, GetFile, GetFileOrFolder
from fontTools.pens.cocoaPen import CocoaPen

def _drawGlyph(glyph):
    pen = CocoaPen(glyph.getParent())
    glyph.draw(pen)
    drawPath(pen.path)
    
pathsToFonts = []

fonts = [OpenFont(ufoPath) for ufoPath in pathsToFonts]
thisFont = fonts[0]

pageWidth = 595.276
pageHeight = 841.89
showGlyphCell = False
showMetrics = False
showName = True
showFrame = False
showCell = False
infoFontName = ''
fontKeys = thisFont.keys()
#fontKeys = ['a','b','c']

frameBackgroundColor = (.1, .3, .5, 0)
frameBorderColor = (1, 1, 1, 0)

glyphFillColor = (0, 0, 0, 1)
glyphStrokeColor= (0, 0, 0, 0.25)
glyphStrokeWidth = 0

cellBackgroundColor = (1, 1, 1, 0)
cellBorderColor = (0, 0, 0, 0)

glyphNameSize = 8
glyphNameColor = (0, 0, 0, 1)

metricsPointSize = 5
metricsFillColor = (0, 0, 0)

# number of columns
col = len(fonts)
# size of each glyph
pointSize = 48
# page margins: top right bottom left 
margins = (30, 20, 30, 20)
cellMargins = (0, 0, 0, 0)

innerWidth = pageWidth - (margins[1]+margins[3])
innerHeight = pageHeight - (margins[0]+margins[2]) 

cellRatio = 1.2
xLoc = 0.5
yLoc = 0.5
cellWidth = innerWidth/col
cellHeight = cellWidth * cellRatio
innerCellWidth = cellWidth - cellMargins[1] - cellMargins[3]
innerCellHeight = cellHeight - cellMargins[0] - cellMargins[2]

glyphsPerPage = col * int(innerHeight/(cellHeight))

glyphs = []
for glyphName in thisFont.lib.get('public.glyphOrder'):
    for aFont in fonts:
        aFontKeys = aFont.keys()
        if glyphName in aFontKeys:
            glyphs.append(aFont[glyphName])
        elif '.notdef' in aFontKeys:
            glyphs.append(aFont['.notdef'])
        else:
            glyphs.append(aFont['space'])
            
for i, glyph in enumerate(glyphs):
    
    thisFont = glyph.getParent()
    
    UPM = thisFont.info.unitsPerEm
    xHeight = thisFont.info.xHeight
    capHeight = thisFont.info.capHeight
    ascender = thisFont.info.ascender
    descender = thisFont.info.descender
    sc = pointSize / UPM
    
    i = i%glyphsPerPage
    
    if i == 0:
        newPage(pageWidth, pageHeight)
        
        if showFrame:
            ## page frame
            stroke(*frameBorderColor)
            fill(*frameBackgroundColor)
            rect(margins[3], margins[2], innerWidth, innerHeight)

        # defining margins and starting from top of the page
        translate(margins[3], margins[2]+innerHeight)
    
    save()
    
    lineCount = int(i/col)
    xPos = cellWidth*(i%col)
    yPos = cellHeight*(lineCount+1)
    
    if showCell:
        ## tracing glyph cell
        save()
        stroke(*cellBorderColor)
        fill(*cellBackgroundColor)
        strokeWidth(.25)
        rect(xPos+cellMargins[3], -yPos+cellMargins[0], innerCellWidth, innerCellHeight)   
        restore()
    
    ### glyph position in table
    translate(xPos+cellMargins[3]+((innerCellWidth*xLoc)-((glyph.width*xLoc)*sc)), -yPos+cellMargins[2]+((innerCellHeight*(1-yLoc))-(UPM*(1-yLoc)*sc)))
    
    ## drawing glyph

    ### shifting inside glyph box
    scale(sc)
    translate(0, -descender)
    
    if showGlyphCell:
        save()
        # bounding box
        stroke(0.75)
        strokeWidth(1)        
        rect(0, descender, glyph.width, UPM)
        # baseline
        stroke(0.5, 0.5, 0.75)
        strokeWidth(3)
        line((0, 0), (glyph.width,0))
        # xHeight
        stroke(0.75, 0.5, 0.5)
        strokeWidth(3)
        line((0, xHeight), (glyph.width, xHeight)) 
        # capHeight
        stroke(0.5, 0.75, 0.5)
        strokeWidth(3)
        line((0, capHeight), (glyph.width, capHeight)) 
        restore()
    
    stroke(*glyphStrokeColor)
    strokeWidth(glyphStrokeWidth)
    fill(*glyphFillColor)
    _drawGlyph(glyph)
    
    if showMetrics:
        save()
        scale(1/sc)
        stroke()
        fill(*metricsFillColor)
        font(infoFontName)
        fontSize(metricsPointSize)
        surrounding = ((innerCellWidth*xLoc)-((glyph.width*xLoc)*sc))
        textBox(str(int(glyph.leftMargin)), (-surrounding, (xHeight*sc)/2, surrounding, metricsPointSize), 'center')
        textBox(str(int(glyph.rightMargin)), (glyph.width*sc, (xHeight*sc)/2, surrounding, metricsPointSize), 'center')
        textBox(str(int(glyph.width)), (0, ((descender-100)*sc)-metricsPointSize, glyph.width*sc, metricsPointSize), 'center')
        restore()
    
    restore()
    
    if showName:
        save()
        translate(xPos, -yPos)
        fill(*glyphNameColor)
        font(infoFontName)
        fontSize(glyphNameSize)
        textBox(glyph.name.upper(), (0, cellMargins[2]+glyphNameSize, cellWidth, glyphNameSize), 'center')
        restore()

faceName = thisFont.info.familyName
styleNames = '-'.join([aFont.info.styleName for aFont in fonts])
ufoPath = thisFont.path
ufoFileName = ufoPath.split('/')[-1]
ufoFolder = ufoPath.rstrip(ufoFileName)
timestamp = datetime.datetime.now().strftime('%y%m%d')
PDFFileName = ufoFolder + '/' + timestamp + '_' + faceName + '_' + styleNames + '.pdf'

saveImage(PDFFileName)