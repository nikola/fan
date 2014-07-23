# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
import pylzma

from OpenSSL import crypto


TARGET_MODULE = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'backend', 'filters', 'de8926be7f2d430fad66927ffadc9f9d')


if __name__ == '__main__':
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.set_version(0x2)
    cert.get_subject().CN = 'Nikola Klaric'
    cert.set_serial_number(int(time.time() * 10000))
    cert.gmtime_adj_notBefore(-3600 * 48)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)

    cert.add_extensions([
        crypto.X509Extension('subjectAltName', False, 'IP:127.0.0.1'),
        crypto.X509Extension('extendedKeyUsage', False, 'serverAuth'),
    ])

    cert.sign(k, 'sha1')

    privateKey = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
    certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    pem = (privateKey + certificate).strip()

    compressed = pylzma.compress(pem)

    # with open(TARGET_MODULE, 'rU') as fp:
    #     content = fp.read()

    # content = re.compile(r'(?<=CERTIFICATE = ).*?(?=\n)').sub("'%s'" % encoded, content)

    with open(TARGET_MODULE, 'wb') as fp:
        # fp.write(content)
        fp.write(compressed)
