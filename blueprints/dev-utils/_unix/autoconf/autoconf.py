import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.69", "2.71"]:
            self.targets[
                ver
            ] = f"https://ftp.gnu.org/gnu/autoconf/autoconf-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"autoconf-{ver}"

        self.targetDigests["2.69"] = (
            ["64ebcec9f8ac5b2487125a86a7760d2591ac9e1d3dbd59489633f9de62a57684"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2.71"] = (
            ["f14c83cfebcc9427f2c3cea7258bd90df972d92eb26752da4ddad81c87a0faa4"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "Autoconf is an extensible package of M4 macros that produce shell scripts to automatically configure software source code packages."
        self.defaultTarget = "2.71"

    def setDependencies(self):
        self.buildDependencies["dev-utils/m4"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

    def postInstall(self):
        frozen = [
            "share/autoconf/autoconf/autoconf.m4f",
            "share/autoconf/autotest/autotest.m4f",
            "share/autoconf/m4sugar/m4sh.m4f",
            "share/autoconf/m4sugar/m4sugar.m4f",
        ]
        for f in frozen:
            fileName = os.path.join(self.installDir(), f)
            if os.path.exists(fileName):
                if not utils.deleteFile(fileName):
                    return False
        hardCoded = [
            os.path.join(self.installDir(), x)
            for x in [
                "bin/autoconf",
                "bin/autoheader",
                "bin/autom4te",
                "bin/autoreconf",
                "bin/autoscan",
                "bin/autoupdate",
                "bin/ifnames",
                "share/autoconf/autom4te.cfg",
            ]
        ]
        return self.patchInstallPrefix(
            hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot()
        )
