#!/usr/bin/env python
#
# Copyright (c) 2013 by Tyler Riti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Based on code from Per Olofsson's PraatVersionFixer.py:
# https://github.com/autopkg/recipes/blob/master/Praat/PraatVersionFixer.py

import os.path
from Foundation import NSData, NSPropertyListSerialization, NSPropertyListMutableContainers

from autopkglib import Processor, ProcessorError


__all__ = ["FetchVersionFixer"]


class FetchVersionFixer(Processor):
    description = "Fixes Fetch version string."
    input_variables = {
        "app_path": {
            "required": True,
            "description": "Path to Fetch.app.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of Fetch.app.",
        },
    }

    __doc__ = description

    def read_bundle_info(self, path):
        """Read Contents/Info.plist inside a bundle."""

        plist_path = os.path.join(path, "Contents", "Info.plist")
        info, format, error = \
            NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
                NSData.dataWithContentsOfFile_(plist_path),
                NSPropertyListMutableContainers,
                None,
                None
            )
        if error:
            raise ProcessorError("Can't read %s: %s" % (plist_path, error))
        return info

    def main(self):
        app_path = self.env["app_path"]
        info = self.read_bundle_info(app_path)
        version = info["CFBundleShortVersionString"].split()[0]
        self.env["version"] = version
        self.output("Fixed Version: %s" % self.env["version"])


if __name__ == '__main__':
    processor = FetchVersionFixer()
    processor.execute_shell()
