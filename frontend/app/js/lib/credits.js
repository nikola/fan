/**
 *  Application and third-party library credits.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.showLicenseTexts = function () {
    ka.state.currentPageMode = 'credits';

    $('#content').velocity('fadeOut', {duration: ka.settings.durationNormal, complete: function () {
        ka.state.licenses = ka.lib.getLicenseTexts().reverse();
        ka.state.licenseTextIndex = ka.state.licenses.length - 1;
        ka.lib.showNextLicense();
    }});
};


ka.lib.showNextLicense = function () {
    if (ka.state.licenseTextIndex > -1) {
        var licenseText = ka.state.licenses[ka.state.licenseTextIndex].trim();
        $('#boom-credit-text').html(licenseText)
            .velocity('fadeIn', {duration: ka.settings.durationNormal, display: 'flex', complete: function () {
                $('#boom-credit-text').velocity('fadeOut', {delay: 5000, duration: ka.settings.durationNormal, complete: function () {
                    ka.state.licenseTextIndex -= 1;

                    ka.lib.showNextLicense();
                }});
            }});
    } else {
        ka.lib.stopLicenseTextDisplay();
    }
};


ka.lib.stopLicenseTextDisplay = function () {
    $('#content').velocity('fadeIn', {duration: ka.settings.durationNormal, complete: function () {
        ka.state.currentPageMode = 'config';
    }});
};


ka.lib.getLicenseTexts = function () {
    return [

        (function () {/*
<span>ka-BOOM</span>
Copyright 2013-2014 Nikola Klaric.
<br>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

  , (function () {/*
<span>jQuery</span>
Copyright 2005, 2014 jQuery Foundation and other contributors.
<br>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
<br>
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
<br>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>quantize.js</span>
Copyright 2008 Nick Rabinowitz.
<br>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
<br>
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
<br>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>Velocity.js</span>
Copyright 2014 Julian Shapiro.
<br>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
<br>
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
<br>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>CEF Python</span>
Copyright (c) 2012-2013 Czarek Tomczak. Portions Copyright (c) 2008-2013 Marshall A.Greenblatt, 2006-2009 Google Inc. All rights reserved.
<br>
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
<br>
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
<br>
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
<br>
* Neither the name of Google Inc. nor the name Chromium Embedded Framework nor the name of CEF Python nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
<br>
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*var myString = (function () {/*
<span>SQLAlchemy</span>
Copyright (c) 2005-2014 the SQLAlchemy authors and contributors.
SQLAlchemy is a trademark of Michael Bayer.
<br>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
<br>
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
<br>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>requests</span>
Copyright 2014 Kenneth Reitz.
<br>
Licensed under the Apache License, Version 2.0 (the 'License'); you may not use this file except in compliance with the License. You may obtain a copy of the License at
<br>
http://www.apache.org/licenses/LICENSE-2.0
<br>
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>Font Awesome by Dave Gandy - http://fontawesome.io</span>
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>All movie metadata and artwork is fetched from TMDb - http://themoviedb.org</span>
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>ImageMagick</span>
Copyright 1999-2014 ImageMagick Studio LLC.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
<span>WebP encoder tool</span>
Copyright (c) 2010, Google Inc. All rights reserved.
<br>
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
<br>
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
<br>
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
<br>
* Neither the name of Google nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
<br>
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]
];
}
