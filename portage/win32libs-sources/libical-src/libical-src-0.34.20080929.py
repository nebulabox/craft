import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'libical'
        self.targets['0.40'] = 'http://downloads.sourceforge.net/freeassociation/libical-0.40.tar.gz'
        self.targetInstSrc['0.40'] = 'libical-0.40'
        self.defaultTarget = '0.40'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW right now."
            exit( 1 )


    
    def unpack( self ):
        print "libical unpack called for %s" % self.subinfo.buildTarget
        # do the svn fetch/update
        if self.buildTarget == 'svnHEAD':
            repo = 'https://freeassociation.svn.sourceforge.net/svnroot/freeassociation/trunk/'
            if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
                self.svnFetch( repo + self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
            else:
                return False
            utils.cleanDirectory( self.workdir )
        else:
            return base.baseclass.unpack( self )
        return True

    def compile( self ):
        if self.buildTarget == 'svnHEAD':
            if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
                self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
            else:
                return False
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libical" )
        self.createImportLibs( "libicalss" )
        self.createImportLibs( "libicalvcal" )

        self.doPackaging( "libical", "0.34-0", True )

        return True

if __name__ == '__main__':
    subclass().execute()
