import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kactivities|KDE/4.8|'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.1/src/kactivities-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'kactivities-4.8.0'
        for ver in ['1', '2', '3', '4']:
            self.targets['4.8.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.' + ver + '/src/kactivities-4.8.' + ver + '.tar.xz'
            self.targetInstSrc['4.8.' + ver] = 'kactivities-4.8.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.shortDescription = "KDE Activity Manager"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
