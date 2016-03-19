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
        self.pageNames = self.getAllPageNames()
        self.pageNamesSet = set(self.pageNames)
        self.pageCount = len(self.pageNames)
    
    def __extractWikiFileNamesFromPath(self,wikiFilePath):
        filename = os.path.split(wikiFilePath)[1]
        return os.path.splitext(filename)[0]

    def __getFilePathFromPageName(self,pageName):
        filename = os.path.join(self.datafolder,"%s.wiki" % pageName)
        return filename    
    
    def getAllPageNames(self):
        """Returns a list of PageNames found in data folder."""
        filePathList = glob.glob(self.datafolder +'/*.wiki')
        return [self.__extractWikiFileNamesFromPath(x) for x in filePathList]
    
    def getMatchingPageNamesByFunction(self,matchFunction,matchValue=""):
        """ Passed a match function and a match value to filter pages
            Returns list of pageNames that return true when processed by function matchFunction(matchValue,pagename)
        """
        self.pageNames = self.getAllPageNames()
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

    def getPageNamesContainingSearchString(self,srchstr):
        """Returns list of pageNames that contain the srchstr in their content"""
        return [x for x in self.pageNames if self.doesPageContainString(x,srchstr)]  
    
    def getPageNamesContainingSearchStringLowMem(self,srchstr):
        """Returns list of pageNames that contain the srchstr in their content"""
        return [x for x in self.pageNames if self.doesPageContainStringLowMem(x,srchstr)] 