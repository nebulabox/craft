import info


class subinfo(info.infoclass):
    def setTargets(self):
        arch = "32"
        if craftCompiler.isX64():
            arch = "64"
        for ver in ["1.9.0"]:
            self.targets[ver] = f"https://files.kde.org/craft/3rdparty/gpgme/mingw_{arch}/gcc/Release/gpgme-src-{ver}-windows-mingw_{arch}-gcc.7z"
            # self.targetDigestUrls[ ver ] = f"http://files.kde.org/craft/3rdparty/gpgme/gpgme-src-{compiler.architecture()}-{ver}-mingw-w64.7z.sha256"

        self.shortDescription = "GnuPG cryptography support library (runtime)"
        self.defaultTarget = '1.9.0'

    def setDependencies(self):
        self.runtimeDependencies['virtual/base'] = 'default'
        if craftCompiler.isGCCLike():
            self.runtimeDependencies["autotools/gpgme-src"] = "default"
        else:
            self.runtimeDependencies["win32libs/mingw-crt4msvc"] = "default"
            self.runtimeDependencies['win32libs/assuan2'] = 'default'
            self.runtimeDependencies["win32libs/gpg-error"] = "default"


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class BinPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, not craftCompiler.isGCCLike(), classA=BinPackage)
