from os import path
from xml.etree import ElementTree

from .BitmapConfig import *

BmpConfigNodeTag  = "BitmapConfiguration"
BitmapSlotNodeTag = "BitmapSlot"
ExtraFlagNodeTag  = "UserFlags"
NoAlphaNodeTag    = "ForceNoAlpha"


class XmlSerializer :
    """ Class holding an xmlPath and its xmlData tree, with a xmlBmpConfig corresponding to the xml traduction, and a modifiable bmpConfig """

    def __init__(self, sPath = "") :
        self.xmlPath = sPath
        self.bmpConfig = BitmapConfig()
        self.xmlBmpConfig = BitmapConfig()
        self.xmlData = None

    def IsDirty(self) :
        """ Tells if there is a difference between xml configs and modified config """
        return not compareBitmapConfig(self.bmpConfig, self.xmlBmpConfig)

    def Reconcile(self) :
        """ Reload the xml configuration in the modifiable config (also return true if there were already the same) """
        if not self.IsDirty() :
            return True
        self.bmpConfig = copyBitmapConfig(self.xmlBmpConfig)
        return False

    def ParseXmlTree(self) :
        """ Return false if the xml format is wrong """
         # Read the xml file
        try :
            self.xmlData = ElementTree.parse(self.xmlPath)
        except ElementTree.ParseError :
            print("[ERROR] Fail at parsing xml")
            return False
        # Verify root node
        rootNode = self.xmlData.getroot()
        if rootNode.tag != BmpConfigNodeTag :
            print("[ERROR] Wrong root node name.")
            return False
        # Get bitmap node (mandatory)
        bmpSlotNode = rootNode.find(BitmapSlotNodeTag)
        if bmpSlotNode is None :
            print("[ERROR] No mandatory bmp mat node found.")
            return False
        bmpSlot = bmpSlotNode.text
        if bmpSlot is None :
            print("[ERROR] Empty bmp mat node.")
            return False
        # Get user flags (optionnal)
        userFlagNode = rootNode.find(ExtraFlagNodeTag)
        if userFlagNode is None :
            userFlag = ""
        else :
            userFlag = userFlagNode.text
        # Get ForceNoAlpha (non defined if false)
        noAlphaNode = rootNode.find(NoAlphaNodeTag)
        if noAlphaNode is None :
            noAlpha = False
        else :
            noAlpha = (noAlphaNode.text.lower() == "true" or noAlphaNode.text == "1")
        # Save xml values
        self.xmlBmpConfig = BitmapConfig(findBitmapIndex(bmpSlot), userFlag, noAlpha)
        return True

    def UpdateXmlTree(self) :
        """ Write the bmpConfig in the xml tree (and so update the xml config). Also create the tree if needed """
        self.xmlBmpConfig = copyBitmapConfig(self.bmpConfig)
        # BitmapConfiguration
        if self.xmlData is None :
            self.xmlData = ElementTree.ElementTree(ElementTree.Element(BmpConfigNodeTag))
        rootNode = self.xmlData.getroot()
        # BitmapSlot
        bmpNode = rootNode.find(BitmapSlotNodeTag)
        if bmpNode is None :
           bmpNode = ElementTree.SubElement(rootNode, BitmapSlotNodeTag)
        bmpNode.text = BitmapList[self.bmpConfig.materialBitmap]
        # UserFlag
        userNode = rootNode.find(ExtraFlagNodeTag)
        if self.bmpConfig.userFlags != "" :
            if userNode is None :
                userNode = ElementTree.SubElement(rootNode, ExtraFlagNodeTag, {"Type": "_DEFAULT"})
            userNode.text = self.bmpConfig.userFlags
        elif not userNode is None :
            rootNode.remove(userNode)
        # ForceNoAlpha
        noAlphaNode = rootNode.find(NoAlphaNodeTag)
        if self.bmpConfig.forceNoAlpha :
            if noAlphaNode is None :
                noAlphaNode = ElementTree.SubElement(rootNode, NoAlphaNodeTag)
            noAlphaNode.text = "true"
        elif not noAlphaNode is None :
            rootNode.remove(noAlphaNode)
        return

    def Open(self, pXmlPath = None) :
        """ Return False if the file can't be opened (or wrong format) """
        if not pXmlPath is None :
            self.xmlPath = pXmlPath
        # Check path
        if not path.exists(self.xmlPath) :
            self.xmlBmpConfig = BitmapConfig()
            return False
        # Parse xml
        if not self.ParseXmlTree() :
            self.xmlBmpConfig = BitmapConfig()
            return False
        # Update modifiable bmpConfig
        self.Reconcile()
        return True

    def Save(self, pXmlPath = None) :
        """ Write the xml file on disc """
        # Use the parameter (needed to change the writing path for example)
        if not pXmlPath is None :
            self.xmlPath = pXmlPath
        # Check path
        if self.xmlPath is None or self.xmlPath == "" :
            print("[ERROR] Path for saving is empty.")
            return False
        # Update the xml with bmpConfig before writing
        self.UpdateXmlTree()
        if self.xmlData is None :
            print("[ERROR] Xml data to save is empty.")
            return False
        # Write the file
        try :
            with open(self.xmlPath, 'wb') as file :
                self.xmlData.write(file, encoding="utf-8")
        except :
            print("[ERROR] Error while writing the file.")
            return False
        return True
