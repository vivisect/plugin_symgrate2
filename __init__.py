#!/usr/bin/env python3

import sys
import time
import logging
from binascii import hexlify
from PyQt5.QtWidgets import QInputDialog, QMessageBox

import vivisect
from vqt.common import ACT
from vqt.main import idlethread
from envi.threads import firethread

from .Symgrate2 import Symgrate2

logger = logging.getLogger('vivisect.ext.%s' % __name__)
print("logger.getEffectiveLevel(): %r" % logger.getEffectiveLevel())


LEN = 18
BATCHSIZE = 0x3f

def getFunctionPrefix(vw, fva):
    """Returns the first LEN bytes of a function as ASCII."""
    B = vw.readMemory(fva, LEN)
    
    if len(B) != LEN:
        return ""
        
    return hexlify(B)


@firethread
def searchFunction(vw, fva):
    """Searches for one function."""
    try:
        logging.warning("\nsearchFunction: 0x%x" % fva)
        count = 0
        curname = vw.getName(fva)
        pre = getFunctionPrefix(vw, fva)
        nmdict = Symgrate2().queryfn(pre)

        if nmdict is not None:
            newname = nmdict.get('Name')
            if curname is None or curname == "sub_%.8x" % fva: #built-in symbol we can likely overwrite
                cmt = str(nmdict.get('Filename'))

                vw.makeName(fva, newname.strip())
                vw.vprint("Symgrate2 Query:  Found name: %s" % newname)
                information("Symgrate2 Query", "Found name: %s" % newname)
            else:
                vw.vprint("Symgrate2 Query: " +\
                        "Identified as %s, but existing user name is %s so not auto-setting."% (newname, curname))
                warning("Symgrate2 Query", 
                        "Identified as %s, but existing user name is %s so not auto-setting."% (newname, curname))
        else:
            warning("Symgrate2 Query", "Unknown function: 0x%x." % fva)

    except Exception as e:
        import traceback
        traceback.print_exc()
        vw.vprint("Symgrate2 Query Failed: %r" % e)


@firethread
def allfunction_searchbg(vw):
    """Searches for all functions in the background."""
    try:
        start = time.time()

        logger.info("allfunction_searchbg")
        matches=0

        # batch up the functions into one request
        reqdict = {}
        for fva in vw.getFunctions():
            logger.warning("  0x%x", fva)
            fsize = vw.getFunctionMeta(fva, 'Size')
            if fsize is None or fsize < 18:
                continue
            reqdict[hex(fva)] = getFunctionPrefix(vw, fva)

        vw.vprint("\nSearching Symgrate for %d functions" % len(reqdict))
        namesdict = Symgrate2().queryfns(reqdict)

        # parse and handle all the results
        for strfva, nmdict in namesdict.items():
            fva = int(strfva, 0)
            curname = vw.getName(fva)
            cmt = str(nmdict.get('Filename'))
            newname = nmdict.get("Name").strip()

            if not len(newname):
                vw.vprint("Symgrate2: Result %r not valid." % nmdict)
                continue

            # now do the thing...
            if curname is None or curname == "sub_%.8x" % fva: #built-in symbol we can likely overwrite
                vw.makeName(fva, newname.strip())
                vw.vprint("Symgrate2: Setting function name at 0x%x to %s" % (fva, newname))
                matches += 1

                curcmnt = vw.getComment(fva)
                if curcmnt is not None and cmt in curcmnt:
                    # skip adding a comment twice, or a blank comment
                    continue

                if curcmnt is not None:
                    vw.setComment(fva, "(%s) / %s" % (cmt, curcmnt))
                else:
                    vw.setComment(fva, cmt)

            else:
                vw.vprint("Symgrate2: Function %s at 0x%x was already named by the user, refusing to override with Symgrate2 result: %s"\
                        % (curname, fva, newname))

        deltat = time.time() - start
        vw.vprint("Symgrate2: Searched %d functions and found %d matches in %.3f seconds." % (len(reqdict), matches, deltat))

    except Exception as e:
        import traceback
        traceback.print_exc()
        vw.vprint("Symgrate2 Query Failed: %r" % e)


def ctxMenuHook(vw, va, expr, menu, parent, nav):
    '''
    Context Menu handler (adds options as we wish)
    '''
    try:
        fva = vw.getFunction(va)
        if fva == va:
            # we're right clicking on a function
            menu.addAction('Symgrate2 Function Search', ACT(searchFunction, vw, fva))

    except Exception as e:
        import traceback
        traceback.print_exc()

@idlethread
def vivExtension(vw, vwgui):
    vwgui.vqAddMenuField('&Plugins.&Symgrate2.&AutoAnalyze', allfunction_searchbg, (vw,))
    vw.addCtxMenuHook('Symgrate2', ctxMenuHook)


@idlethread
def warning(msg, info):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('Warn: %s' % msg)
    msgbox.setInformativeText(info)
    msgbox.setIcon(QMessageBox.Warning)
    msgbox.exec_()

@idlethread
def information(msg, info):
    msgbox = QMessageBox()
    msgbox.setWindowTitle('%s' % msg)
    msgbox.setInformativeText(info)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.exec_()

