import os,glob
import mmap

from WikidWorker import hasWiki
"""
WikidWiki Class
WikidPad Extensions and Helper library for WikidPad. Incorporates the older projects:WikidSets, WikidTags, etc.
Version 1.0
Remote: https://github.com/jaysen/WikidLibPy.git

"""

class WikidWiki(object):
    """class for working with a wikidpad wiki from the filesystem."""

    def __init__(self,folder_path):
        """Construct a WikidWiki class using the folder_path as string."""
        # raise error if folder path doesn't exist or contains no wiki:
        if not os.path.exists(folder_path):
            raise Exception("folder " + folder_path + " does not exist!")
        if not hasWiki(folder_path):
            raise Exception("folder " + folder_path + " does not contain a wiki!")

        #set attributes:
        self.rootfolder = folder_path
        self.datafolder = os.path.join(folder_path,'data')
        self.readFileSystem()
        
    def readFileSystem(self):
        """Populates the PageName attributes of WikidWiki class from the filesystem"""
        self.pageNames = self.getAllPages()
        self.pageNamesSet = set(self.pageNames)
        self.pageCount = len(self.pageNames)
    
    def __extractWikiFileNamesFromPath(self,wikiFilePath):
        filename = os.path.split(wikiFilePath)[1]
        return os.path.splitext(filename)[0]

    def __getFilePathFromPageName(self,pageName):
        filename = os.path.join(self.datafolder,"%s.wiki" % pageName)
        return filename    
    
    """ GET_PAGES Methods:"""
    
    def getAllPages(self):
        """Returns a list of Pages found in data folder."""
        filePathList = glob.glob(self.datafolder +'/*.wiki')
        return [self.__extractWikiFileNamesFromPath(x) for x in filePathList]
    
    def getPagesByFunction(self,matchFunction,matchValue=""):
        """ Passed a match function and a match value to filter pages
            Returns list of pageNames that return true when processed by function matchFunction(matchValue,pagename)
        """
        self.pageNames = self.getAllPages()
        if matchValue:
            return [x for x in self.pageNames if matchFunction(matchValue,x)]
        else:
            return [x for x in self.pageNames if matchFunction(x)]            

    def doesPageContainStringLowMem(self,pageName,srchstr):
        filepath = self.__getFilePathFromPageName(pageName)
        
        if os.stat(filepath).st_size > 0:
            f = open(filepath)
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return s.find(srchstr) != -1
        return False
    
    def doesPageContainString(self,pageName,srchstr):
        filepath = self.__getFilePathFromPageName(pageName)
        return srchstr in open(filepath).read()

    def getPagesBySearchStr(self,srchstr):
        """Returns list of pageNames that contain the srchstr in their content"""
        return [x for x in self.pageNames if self.doesPageContainString(x,srchstr)]  
    
    def getPagesBySearchStrLowMem(self,srchstr):
        """Returns list of pageNames that contain the srchstr in their content"""
        return [x for x in self.pageNames if self.doesPageContainStringLowMem(x,srchstr)] 
    
    def getPagesSetUnion(self,pn1,pn2):
        """Returns the union of pageName lists pn1 and pn2"""
        ps1 = set(pn1)
        ps2 = set(pn2)
        return ps1 | ps2
    
    def getPagesSetIntersection(self,pn1,pn2):
        """Returns the intersection of pageName lists pn1 and pn2"""
        ps1 = set(pn1)
        ps2 = set(pn2)
        return ps1 & ps2

    def getPagesSetDifference(self,pn1,pn2):
        """Returns the difference of pageName lists pn1 and pn2"""
        ps1 = set(pn1)
        ps2 = set(pn2)
        return ps1 - ps2

    def getPagesSetSymmetricDifference(self,pn1,pn2):
        """Returns the symmetric difference (those in one or the other, but not both) of pageName lists pn1 and pn2"""
        ps1 = set(pn1)
        ps2 = set(pn2)
        return ps1 ^ ps2
    
    def getPagesByTag(self, tag):
        """Passed a single tag and returns all pages containing that tag."""
        return self.getPagesBySearchStr("[tag:%s]" % tag)

    def getPagesByTags(self, tags):
        """Passed a list of tags and returns all pages containing ALL those tags."""
        pages = self.pageNames
        for t in tags:
            pages = self.getPagesSetIntersection(pages,self.getPagesByTag(t))
        return pages

    def getPagesWithNoTag(self):
        """Gets all pages containing NO tag."""
        return self.getPagesSetDifference(self.pageNames,self.getPagesBySearchStr("[tag"))

    def getPagesByCategory(self, cat):
        """Passed a single category and returns all pages containing that category link."""
        return self.getPagesBySearchStr(" Category%s" % cat.capitalize())

    def getPagesByCategories(self, cats):
        """Passed a list of categories and returns all pages containing ALL those category links."""
        pages = self.pageNames
        for c in cats:
            pages = self.getPagesSetIntersection(pages,self.getPagesByCategory(c))
        return pages
    
    def getPagesByCatOrTag(self, val):
        """Returns all pages with either tag or category = val"""
        return self.getPagesSetUnion(self.getPagesByTag(val),self.getPagesByCategory(val))
    