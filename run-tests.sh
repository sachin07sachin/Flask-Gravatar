#!/bin/sh
#
# This file is part of Flask-Gravatar
# Copyright (C) 2015 CERN.
# Copyright (C) 2018 Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Flask-Gravatar is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

# 1. STYLE CHECK: Check docstrings against PEP 257 conventions.
pydocstyle flask_gravatar tests && \

# 2. FORMATTING CHECK: Verify and show differences in import sorting/grouping.
isort  -c --diff flask_gravatar && \

# 3. STYLE & ERROR CHECK: Comprehensive check for PEP 8 compliance and common errors (like unused variables).
# (This replaces the deprecated pytest-pep8 plugin.)
flake8 flask_gravatar tests && \

# 4. BUILD INTEGRITY: Ensure all necessary files are included in the source distribution package.
check-manifest --ignore ".travis-*" && \

# 5. DOCUMENTATION CHECK: Attempt to build documentation to catch errors/warnings in docs.
sphinx-build -qnNW docs docs/_build/html && \

# 6. FUNCTIONAL TEST: Execute the main unit and functional test suite.
# (Uses the modern, direct test runner command.)
pytest
