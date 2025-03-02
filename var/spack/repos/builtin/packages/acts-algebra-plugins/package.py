# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ActsAlgebraPlugins(CMakePackage):
    """A portable linear algebra library with multiple backends that is part of
    the Acts ecosystem."""

    homepage = "https://github.com/acts-project/algebra-plugins"
    url = "https://github.com/acts-project/algebra-plugins/archive/refs/tags/v0.24.0.tar.gz"

    maintainers("stephenswat", "wdconinc")

    license("MPL-2.0", checked_by="stephenswat")

    version("0.26.2", sha256="0170f22e1a75493b86464f27991117bc2c5a9d52554c75786e321d4c591990e7")
    version("0.26.1", sha256="8eb1e9e28ec2839d149b6a6bddd0f983b0cdf71c286c0aeb67ede31727c5b7d3")
    version("0.26.0", sha256="301702e3d0a3d12e46ae6d949f3027ddebd0b1167cbb3004d9a4a5697d3adc7f")
    version("0.25.0", sha256="bb0cba6e37558689d780a6de8f749abb3b96f8cd9e0c8851474eb4532e1e98b8")
    version("0.24.0", sha256="f44753e62b1ba29c28ab86b282ab67ac6028a0f9fe41e599b7fc6fc50b586b62")

    depends_on("cxx", type="build")  # generated

    _cxxstd_values = (
        conditional("17", when="@:0.25"),
        conditional("20", when="@0:"),
        conditional("23", when="@0:"),
    )
    _cxxstd_common = {"values": _cxxstd_values, "multi": False, "description": "C++ standard used"}
    variant("cxxstd", default="17", when="@:0.25", **_cxxstd_common)
    variant("cxxstd", default="20", when="@0.26:", **_cxxstd_common)
    variant("eigen", default=False, description="Enables the Eigen plugin")
    variant("smatrix", default=False, description="Enables the SMatrix plugin")
    variant("vecmem", default=False, description="Enables the vecmem plugin")
    variant("vc", default=False, description="Enables the Vc plugin")
    variant("fastor", default=False, description="Enables the Fastor plugin")

    depends_on("cmake@3.14:", type="build")
    depends_on("vecmem@1.5.0:", when="+vecmem")
    depends_on("eigen@3.4.0:", when="+eigen")
    depends_on("vc@1.4.3:", when="+vc")
    depends_on("root@6.18.0:", when="+smatrix")
    depends_on("fastor@0.6.4:", when="+fastor")

    with when("+smatrix"):
        depends_on("root cxxstd=17", when="cxxstd=17")
        depends_on("root cxxstd=20", when="cxxstd=20")
        conflicts("cxxstd=23")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("ALGEBRA_PLUGINS_USE_SYSTEM_LIBS", True),
            self.define_from_variant("ALGEBRA_PLUGINS_INCLUDE_EIGEN", "eigen"),
            self.define_from_variant("ALGEBRA_PLUGINS_SETUP_EIGEN3", "eigen"),
            self.define_from_variant("ALGEBRA_PLUGINS_INCLUDE_SMATRIX", "smatrix"),
            self.define_from_variant("ALGEBRA_PLUGINS_INCLUDE_VC", "vc"),
            self.define_from_variant("ALGEBRA_PLUGINS_SETUP_VC", "vc"),
            self.define_from_variant("ALGEBRA_PLUGINS_INCLUDE_VECMEM", "vecmem"),
            self.define_from_variant("ALGEBRA_PLUGINS_SETUP_VECMEM", "vecmem"),
            self.define_from_variant("ALGEBRA_PLUGINS_INCLUDE_FASTOR", "fastor"),
            self.define_from_variant("ALGEBRA_PLUGINS_SETUP_FASTOR", "fastor"),
            self.define("ALGEBRA_PLUGINS_BUILD_TESTING", False),
            self.define("ALGEBRA_PLUGINS_SETUP_GOOGLETEST", False),
            self.define("ALGEBRA_PLUGINS_SETUP_BENCHMARK", False),
            self.define("ALGEBRA_PLUGINS_BUILD_BENCHMARKS", False),
        ]

        return args
