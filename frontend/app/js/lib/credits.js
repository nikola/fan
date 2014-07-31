/**
 *  Application and third-party library credits.
 *
 *  @author Nikola Klaric (nikola@generic.company)
 *  @copyright Copyright (c) 2013-2014 Nikola Klaric
 */
; var ka = ka || {}; if (!('lib' in ka)) ka.lib = {};


ka.lib.showLicenseTexts = function () {
    $('#content').velocity('fadeOut', {duration: 360, complete: function () {
        ka.state.currentPageMode = 'credits';

        ka.state.licenses = ka.lib.getLicenseTexts();
        ka.state.licenseTextIndex = ka.state.licenses.length - 1;
        ka.lib.showNextLicense();
    }});
};


ka.lib.showNextLicense = function () {
    if (ka.state.licenseTextIndex > -1) {
        $('#boom-credit-text').text(ka.state.licenses[ka.state.licenseTextIndex])
            .velocity('fadeIn', {duration: 360, complete: function () {
                $('#boom-credit-text').velocity('fadeOut', {delay: 5000, duration: 360, complete: function () {
                    ka.state.licenseTextIndex -= 1;

                    ka.lib.showNextLicense();
                }});
            }});
    } else {
        $('#content').velocity('fadeIn', {duration: 360, complete: function () {
            ka.state.currentPageMode = 'config';
        }});
    }
};


ka.lib.getLicenseTexts = function () {
    return [
    (function () {/*
jQuery
Copyright 2005, 2014 jQuery Foundation and other contributors.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
quantize.js
Copyright 2008 Nick Rabinowitz.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
Velocity.js
Copyright 2014 Julian Shapiro.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
CEF Python
Copyright (c) 2012-2013 Czarek Tomczak. Portions Copyright
(c) 2008-2013 Marshall A.Greenblatt, 2006-2009 Google Inc.
All rights reserved.

Redistribution and use in source and binary forms, with
or without modification, are permitted provided that the
following conditions are met:

* Redistributions of source code must retain the above
  copyright notice, this list of conditions and the
  following disclaimer.

* Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the
  following disclaimer in the documentation and/or other
  materials provided with the distribution.

* Neither the name of Google Inc. nor the name Chromium
  Embedded Framework nor the name of CEF Python nor the
  names of its contributors may be used to endorse or
  promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*var myString = (function () {/*
SQLAlchemy
Copyright (c) 2005-2014 the SQLAlchemy authors and contributors.
SQLAlchemy is a trademark of Michael Bayer.

SQLAlchemy was created by Michael Bayer.

Major contributing authors include:

- Michael Bayer <mike_mp@zzzcomputing.com>
- Jason Kirtland <jek@discorporate.us>
- Gaetan de Menten <gdementen@gmail.com>
- Diana Clarke <diana.joan.clarke@gmail.com>
- Michael Trier <mtrier@gmail.com>
- Philip Jenvey <pjenvey@underboss.org>
- Ants Aasma <ants.aasma@gmail.com>
- Paul Johnston <paj@pajhome.org.uk>
- Jonathan Ellis <jbellis@gmail.com>

For a larger list of SQLAlchemy contributors over time, see:

http://www.sqlalchemy.org/trac/wiki/Contributors

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
requests
Copyright 2014 Kenneth Reitz.

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]

    , (function () {/*
Font Awesome by Dave Gandy - http://fontawesome.io
*/}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]
];
}
