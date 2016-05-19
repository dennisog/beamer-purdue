#!/bin/bash
#
# make_zip.sh --- create downloadable .zip files for the beamer-purdue theme.
#
# Copyright (c) 2016 Dennis Ogbe <dogbe@purdue.edu>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

REPO="$(cd $(dirname "$0")/..; pwd)"
TMPD=$(mktemp -d)
[[ $? != "0" ]] && exit 1
cd "$TMPD"
git clone "$REPO" . >/dev/null 2>&1
[[ $? != "0" ]] && exit 1
THEMES=( "gold" "white" )
for THEME in "${THEMES[@]}"; do
  ! [[ -d "$THEME" ]] && exit 1
  cd "$THEME"
  cp "$REPO/README.org" .
  zip -r --exclude "*preview*" - . 2>/dev/null | cat > "$REPO/dl/beamer-purdue-$THEME.zip"
  [[ $? != "0" ]] && exit 1
  cd ..
done
cd "$REPO"
[[ -d "$TMPD" ]] && rm -rf "$TMPD"
