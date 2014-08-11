import datetime
now = datetime.datetime.now().strftime('%d %B %Y - %H:%M')

def _drawGlyph(glyph):
    path = glyph.naked().getRepresentation("defconAppKit.NSBezierPath")
    drawPath(path)
    
def pageStamp((x, y), pageWidth, thisFont, infoFont):
    font(infoFont)
    fileName = thisFont.path.split('/')[-1]
    fontName = thisFont.info.familyName + u' – ' + thisFont.info.styleName
    save()
    fontSize(7)
    fill(0)
    translate(x, y/2)
    column = pageWidth/6
    textBox(fontName, (0, 0, 2*column, 10))
    textBox(fileName, (2*column, 0, 3*column, 10), 'center')
    textBox(now, (5*column, 0, column, 10), 'right')
    restore()

thisFont = CurrentFont()

pageWidth = 595.276
pageHeight = 841.89
showMetrics = True
showName = True
showFrame = False
showCell = False
showGlyphBox = False

frameBackgroundColor = (.1, .3, .5, .25)
frameBorderColor = (0, 0, 0, .75)

glyphFillColor = (0, 0, 0, 1)
glyphStrokeColor= (0, 0, 0, 0)
glyphStrokeWidth = 0

cellBackgroundColor = (.1, .3, .5, .25)
cellBorderColor = (0, 0, 0, .5)

glyphNameSize = 7
glyphNameColor = (0, 0, 0, 1)

metricsPointSize = 5
metricsFillColor = (0, 0, 0, 1)

# number of columns
col = 6
# size of each glyph
pointSize = 40
# font to display infos
infoFont = ''
# page margins: left top right bottom
margins = (20, 30, 20, 30)
boxMargins = (0, 0, 0, 0)

innerWidth = pageWidth - (margins[0]+margins[2])
innerHeight = pageHeight - (margins[1]+margins[3]) 

boxRatio = 1.5
xLoc = 0.5
yLoc = 0.5
boxWidth = innerWidth/col
boxHeight = boxWidth * boxRatio
innerBoxWidth = boxWidth - boxMargins[1] - boxMargins[3]
innerBoxHeight = boxHeight - boxMargins[0] - boxMargins[2]

UPM = thisFont.info.unitsPerEm
xHeight = thisFont.info.xHeight
capHeight = thisFont.info.capHeight
ascender = thisFont.info.ascender
descender = thisFont.info.descender
sc = pointSize / UPM

glyphsPerPage = col * int(innerHeight/(boxHeight))

glyphs = [thisFont[glyphName] for glyphName in thisFont.glyphOrder]

for i, glyph in enumerate(glyphs):
    
    i = i%glyphsPerPage
    
    if i == 0:
        newPage(pageWidth, pageHeight)
        pageStamp((margins[0], margins[3]), innerWidth, thisFont, infoFont)
        
        if showFrame:
            ## page frame
            stroke(*frameBorderColor)
            fill(*frameBackgroundColor)
            rect(margins[0], margins[3], innerWidth, innerHeight)

        # defining margins and starting from top of the page
        translate(margins[0], margins[3]+innerHeight)
    
    save()
    
    lineCount = int(i/col)
    xPos = boxWidth*(i%col)
    yPos = boxHeight*(lineCount+1)
    
    if showCell:
        ## tracing glyph cell
        save()
        stroke(*cellBorderColor)
        fill(*cellBackgroundColor)
        strokeWidth(.25)
        rect(xPos+boxMargins[3], -yPos+boxMargins[0], innerBoxWidth, innerBoxHeight)   
        restore()
    
    ### glyph position in table
    translate(xPos+boxMargins[3]+((innerBoxWidth*xLoc)-((glyph.width*xLoc)*sc)), -yPos+boxMargins[2]+((innerBoxHeight*(1-yLoc))-(UPM*(1-yLoc)*sc)))
    
    ## drawing glyph

    ### shifting inside glyph box
    scale(sc)
    translate(0, -descender)
    
    if showGlyphBox:
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
        font(infoFont)
        fontSize(metricsPointSize)
        surrounding = ((innerBoxWidth*xLoc)-((glyph.width*xLoc)*sc))
        textBox(str(int(glyph.leftMargin)), (-surrounding, (xHeight*sc)/2, surrounding, metricsPointSize), align='center')
        textBox(str(int(glyph.rightMargin)), (glyph.width*sc, (xHeight*sc)/2, surrounding, metricsPointSize), align='center')
        textBox(str(int(glyph.width)), (0, ((descender-100)*sc)-metricsPointSize, glyph.width*sc, metricsPointSize), 'center')
        restore()
    
    restore()
    
    if showName:
        save()
        translate(xPos, -yPos)
        fill(*glyphNameColor)
        font(infoFont)
        fontSize(glyphNameSize)
        textBox(glyph.name.upper(), (0, boxMargins[2]+glyphNameSize, boxWidth, glyphNameSize), 'center')
        restore()


fileName = thisFont.path.split('/')[-1]
ufoFolder = thisFont.path.rstrip(fileName) 

saveImage(ufoFolder + fileName + '_CHARSET.pdf')