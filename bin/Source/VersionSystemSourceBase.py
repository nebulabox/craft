#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from Source.SourceBase import *


class VersionSystemSourceBase(SourceBase):
    """abstract base class for version system support"""

    def __init__(self):
        CraftCore.debug.trace("VersionSystemSourceBase __init__")
        SourceBase.__init__(self)

    def getUrl(self, index):
        """get the url at position 'index' from a ';' separated list of urls"""
        CraftCore.debug.trace("VersionSystemSourceBase getUrl")
        u = self.subinfo.svnTarget()
        if u.find(";") == -1:
            if index == 0:
                return u
            else:
                return None
        # urls are a list
        urls = u.split(";")
        if index >= len(urls):
            return None

        u = urls[index]
        return u

    def splitUrl(self, url):
        """split url into real url and url option. the delimiter is '#'"""
        CraftCore.debug.trace("VersionSystemSourceBase splitUrl")
        if url.find("#") != -1:
            return url.split("#")
        return [url, ""]

    def __repositoryBaseUrl(self):
        """this function return the base url to the KDE repository"""
        CraftCore.debug.trace("VersionSystemSourceBase __repositoryBaseUrl")
        # @todo move to SvnSource
        server = CraftCore.settings.get(
            "General", "KDESVNSERVER", "svn://anonsvn.kde.org"
        )

        return server + "/home/kde/"

    def unpack(self):
        CraftCore.debug.trace("VersionSystemSourceBase unpack")
        self.enterBuildDir()

        CraftCore.log.debug("cleaning %s" % self.buildDir())
        self.cleanBuild()
        ret = self.applyPatches()
        if CraftCore.settings.getboolean("General", "EMERGE_HOLD_ON_PATCH_FAIL", False):
            return ret
        return True

    def repositoryUrlCount(self):
        """return the number of provided repository url's. Multiple repository urls' are delimited by ';'"""
        CraftCore.debug.trace("VersionSystemSourceBase repositoryUrlCount")
        if not self.subinfo.hasSvnTarget():
            return 0
        u = self.subinfo.svnTarget()
        if u.find(";") == -1:
            return 1
        urls = u.split(";")
        return len(urls)

    def repositoryUrl(self, index=0):
        """this function returns the full url into a version system based repository at position 'index'.
        See @ref repositoryUrlCount how to define multiple repository urls."""
        CraftCore.debug.trace("VersionSystemSourceBase repositoryUrl")
        if self.subinfo.hasSvnTarget():
            u1 = self.getUrl(index)
            (u, _) = self.splitUrl(u1)
            # check relative kde url
            # @todo this is svn specific - move to SvnSource
            if u.find("://") == -1 and utils.getVCSType(u) == "svn":
                url = self.__repositoryBaseUrl() + u
            else:
                url = u
            if url.startswith("["):
                url = url[url.find("]", 1) + 1 :]
            return url
        else:
            return False

    def repositoryUrlOptions(self, index=0):
        """this function return options for the repository url at position 'index'.
        Options for a repository url are defined by adding '#' followed by the specific option.
        """
        CraftCore.debug.trace("VersionSystemSourceBase repositoryUrlOptions")
        if self.subinfo.hasSvnTarget():
            u = self.getUrl(index)
            (dummy, option) = self.splitUrl(u)
            return option
        return None

    def checkoutDir(self, dummyIndex=0) -> Path:
        CraftCore.debug.trace("VersionSystemSourceBase checkoutDir")
        if ("ContinuousIntegration", "SourceDir") in CraftCore.settings:
            return CraftCore.settings.get("ContinuousIntegration", "SourceDir")
        if self.subinfo.hasSvnTarget():
            sourcedir = Path(CraftStandardDirs.gitDir()) / self.package.path
        else:
            CraftCore.log.critical("svnTarget property not set for this target")

        if self.subinfo.targetSourceSuffix() != None:
            sourcedir = Path("%s-%s" % (sourcedir, self.subinfo.targetSourceSuffix()))

        return sourcedir.absolute()

    def sourceDir(self, index=0) -> Path:
        CraftCore.debug.trace("VersionSystemSourceBase sourceDir")
        if ("ContinuousIntegration", "SourceDir") in CraftCore.settings:
            return CraftCore.settings.get("ContinuousIntegration", "SourceDir")

        sourcedir = self.checkoutDir(index)

        if self.subinfo.hasTargetSourcePath():
            sourcedir = sourcedir / self.subinfo.targetSourcePath()

        CraftCore.log.debug("using sourcedir: %s" % sourcedir)
        return sourcedir.absolute()

    def sourceRevision(self):
        CraftCore.debug.trace("VersionSystemSourceBase sourceRevision")
        if self.subinfo.isCachedBuild:
            return None
        if not os.path.exists(self.sourceDir()):
            # as we are using the cahce we don't have the git clone present
            return "latest"
        return self.sourceVersion()
