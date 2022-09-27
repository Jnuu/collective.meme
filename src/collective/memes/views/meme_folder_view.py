# -*- coding: utf-8 -*-

from collective.memes import _
from Products.Five.browser import BrowserView
from datetime import date
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.namedfile.file import NamedBlobFile
from Products.CMFCore.utils import getToolByName
from typing import Container

import json

class MemeFolderView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('meme_folder_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')
        return self.index()

    def get_memes(self):
        base_query = {}
        results = []
        portal_catalog = getToolByName(self, 'portal_catalog')
        base_query['portal_type'] = ('Meme')
        items = portal_catalog(base_query)

        for item in items:
            results.append(item)

        return results

