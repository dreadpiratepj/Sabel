import os

fo = open("icons.qrc", "w")
fo.write('<!DOCTYPE RCC><RCC version="1.0">\n')
fo.write("<qresource>\n")
for icons in os.listdir("Icons"):
    fo.write("<file>Icons/"+icons+"</file>\n")

fo.write('</qresource>\n')
fo.write('</RCC>')
fo.close()
os.popen("pyrcc4 icons.qrc -o icons.py")
print "resource created"

"""
gg = []
for icon in os.listdir("Icons"):
    gg.append(icon)
gg.sort()
for icon in gg:
    print "    "+icon.replace(".png", "")+" = "+"os_icon('%s')"%icon.replace(".png", "")
"""