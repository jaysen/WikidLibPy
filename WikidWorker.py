
# WikidWorker Module

import os,glob

def hasTopWikiFile(folder_path):
    return len(glob.glob(folder_path+'/*.wiki')) > 0

def hasWikiDataFolder(folder_path):
    return len(glob.glob(folder_path+'/data/*.wiki')) > 0

def hasWiki (folder_path):
    hasFolder = hasWikiDataFolder(folder_path) 
    hasTopFile = hasTopWikiFile(folder_path)
    return (hasTopFile and hasFolder)


#TESTS

from nose.tools import assert_equal

class FunctionTest(object):
    
    def test(self,func):        
        assert_equal(func('TestWiki'),True)
        assert_equal(func('NoTestWiki'),False)
        assert_equal(func('BadTestWiki'),False)      
        
        print str(func) + 'PASSED ALL TESTS'
                     
#run tests
t = FunctionTest()
t.test(hasWiki)