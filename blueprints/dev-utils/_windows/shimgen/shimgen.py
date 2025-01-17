# -*- coding: utf-8 -*-

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0"]:
            self.targets[
                ver
            ] = f"https://files.kde.org/craft/3rdparty/shimgenerator/shimgenerator.KDECraft-{ver}.7z"
            self.targetInstSrc[ver] = "shimgenerator.KDECraft/shimgenerator"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.targetDigests["1.0"] = (
            ["3e8c2181f7816a1917188b690493271b1ff6bc07a281de1ff1ce8f1a0818042f"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "1.0"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
