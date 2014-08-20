# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os

import win32api

def _GetResources(hsrc, types=None, names=None, languages=None):
    """
    Get resources from hsrc.

    types = a list of resource types to search for (None = all)
    names = a list of resource names to search for (None = all)
    languages = a list of resource languages to search for (None = all)
    Return a dict of the form {type_: {name: {language: data}}} which
    might also be empty if no matching resources were found.
    """
    if types:
        types = set(types)
    if names:
        names = set(names)
    if languages:
        languages = set(languages)
    res = {}
    try:
        # logger.debug("Enumerating resource types")
        enum_types = win32api.EnumResourceTypes(hsrc)
        if types and not "*" in types:
            enum_types = filter(lambda type_:
                                type_ in types,
                                enum_types)
        for type_ in enum_types:
            # logger.debug("Enumerating resources of type %s", type_)
            enum_names = win32api.EnumResourceNames(hsrc, type_)
            if names and not "*" in names:
                enum_names = filter(lambda name:
                                    name in names,
                                    enum_names)
            for name in enum_names:
                # logger.debug("Enumerating resources of type %s name %s", type_, name)
                enum_languages = win32api.EnumResourceLanguages(hsrc,
                                                                type_,
                                                                name)
                if languages and not "*" in languages:
                    enum_languages = filter(lambda language:
                                            language in languages,
                                            enum_languages)
                for language in enum_languages:
                    data = win32api.LoadResource(hsrc, type_, name, language)
                    if not type_ in res:
                        res[type_] = {}
                    if not name in res[type_]:
                        res[type_][name] = {}
                    res[type_][name][language] = data
    except:
        pass
    return res


def run():
    location = os.path.join('dist', 'ka-BOOM.exe')

    # type_ = 24

    handle = win32api.LoadLibraryEx(location, None, 0x20) # LOAD_LIBRARY_AS_DATAFILE)
    res = _GetResources(handle, [24], [1], [0, '*'])
    win32api.FreeLibrary(handle)

    # UpdateManifestResourcesFromXMLFile
    # name = 1
    # languages = None
    # winresource.UpdateResourcesFromDataFile(dstpath, srcpath, RT_MANIFEST, names or [name], languages or [0, "*"])

    # UpdateResourcesFromDataFilee(dstpath, srcpath, names=None, languages=None)
    # type_ = RT_MANIFEST = 24

    # src = open(srcpath, "rb")
    # data = src.read()
    # src.close()
    # UpdateResources(dstpath, data, type_, names, languages)


    # UpdateResources(dstpath, data, type_, names=None, languages=None):
    # dstpath = ka-BOOM.exe
    # data = manifest content
    # type_ = 24
    # names = [1]
    # languages = [0, "*"]

    # add type_, names and languages not already present in existing resources
    if not 24 in res: #  and type_ != "*":
        res[24] = {}
    # if names:
        # for name in names:
    name = 1
    if not 1 in res[24]: # and name != "*":
        res[24][name] = []
        # if languages:
        # for language in languages:
        for language in [0, "*"]:
            if not language in res[24][1] and language != "*":
                res[24][1].append(language)
    # add resource to destination, overwriting existing resources

    with open('ka-BOOM.exe.manifest', 'rU') as fp:
        manifestXml = fp.read()

    hdst = win32api.BeginUpdateResource(location, 0)
    for type_ in res:
        for name in res[type_]:
            for language in res[type_][name]:
                win32api.UpdateResource(hdst, type_, name, manifestXml, language)
    win32api.EndUpdateResource(hdst, 0)

    import sys
    sys.exit()


    handle = win32api.LoadLibraryEx(location, None, 0x20)
    try:
        manifestXml = win32api.LoadResource(handle, 24, 1)
    except:
        with open('ka-BOOM.exe.manifest', 'rU') as fp:
            manifestXml = fp.read()
    finally:
        win32api.FreeLibrary(handle)

    if manifestXml is not None:
        handle = win32api.BeginUpdateResource(location, 0)
        win32api.UpdateResource(handle, 24, 1, manifestXml, 0)
        win32api.EndUpdateResource(handle, 0)


if __name__ == '__main__':
    run()
