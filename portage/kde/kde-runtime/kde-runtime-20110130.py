import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-runtime'
        self.svnTargets['komobranch'] = 'branches/work/komo/kdebase/runtime'
        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = 'komobranch'
        else:
            self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/libssh'] = 'default'
        if compiler.isMinGW_WXX():
            self.dependencies['win32libs-bin/libbfd'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

        if self.isTargetBuild():
            self.subinfo.options.configure.defines += "-DKDEBASE_DISABLE_MULTIMEDIA=ON "
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "
        
        automoc = os.path.join(self.mergeDestinationDir(), "lib", "automoc4", "Automoc4Config.cmake")
        if not os.path.exists(automoc):
            utils.warning("could not find automoc in <%s>" % automoc)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += " -DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
            % automoc.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
