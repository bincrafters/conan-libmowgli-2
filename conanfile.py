#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class Libmowgli2Conan(ConanFile):
    name = "libmowgli-2"
    version = "2.1.3"
    description = "Generic runtime for atheme applications "
    url = "https://github.com/bincrafters/conan-libmowgli-2"
    homepage = "https://github.com/atheme/libmowgli-2"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_openssl": [True, False]}
    default_options = {'shared': False, 'fPIC': True, 'with_openssl': True}
    _source_subfolder = "source_subfolder"
    autotools = None

    def config_options(self):
        if self.settings.os == 'Windows':
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.with_openssl:
            self.requires.add("openssl/1.1.0l")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure_autotools(self):
        if not self.autotools:
            args = ['--disable-examples']
            args.extend(['--enable-shared', '--disable-static'] if self.options.shared else ['--enable-static', '--disable-shared'])
            args.append('--with-openssl' if self.options.with_openssl else '--without-openssl')
            self.autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            with tools.chdir(self._source_subfolder):
                self.autotools.configure(args=args)
        return self.autotools

    def build(self):
        autotools = self.configure_autotools()
        with tools.chdir(self._source_subfolder):
            autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self.configure_autotools()
        with tools.chdir(self._source_subfolder):
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
