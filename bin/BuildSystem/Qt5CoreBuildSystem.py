#
# copyright (c) 2012 Hannah von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules

from BuildSystem.QMakeBuildSystem import *


class Qt5CoreBuildSystem( QMakeBuildSystem ):
    def __init__( self ):
        QMakeBuildSystem.__init__( self )
        if not craftSettings.getboolean("QtSDK", "Enabled", False):
            utils.putenv( "QMAKESPEC", os.path.join( CraftStandardDirs.craftRoot( ), 'mkspecs', self.platform ) )


    def install( self, options = "" ):
        """implements the make step for Qt projects"""
        imageDir = self.imageDir( )
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            imageDir = imageDir[2:]
        options += f" INSTALL_ROOT={imageDir} install"
        if not QMakeBuildSystem.install( self, options ):
            return False
        if OsUtils.isWin():
            badPrefix = os.path.join( self.installDir( ), CraftStandardDirs.craftRoot( )[ 3: ] )
        else:
            badPrefix = os.path.join( self.installDir( ), CraftStandardDirs.craftRoot( )[1:] )
            print(badPrefix)
        if CraftStandardDirs.craftRoot( )[ 3: ] != "" and os.path.exists( badPrefix ):
            for subdir in os.listdir( badPrefix ):
                utils.moveFile( os.path.join( badPrefix, subdir ), self.installDir( ) )
            utils.rmtree( badPrefix )

        if OsUtils.isWin():
            if os.path.exists( os.path.join( self.installDir( ), "bin", "mkspecs" ) ):
                utils.moveFile( os.path.join( self.installDir( ), "bin", "mkspecs" ),
                                os.path.join( self.installDir( ), "mkspecs" ) )
        return True





