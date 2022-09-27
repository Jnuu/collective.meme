# -*- coding: utf-8 -*-

from collective.memes import _
from plone import api
from plone.namedfile import field as namedfile
from plone.namedfile.file import NamedBlobFile, NamedBlobImage
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

import json
import os


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MemeRegisterView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('meme_register_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')
        return self.index()

class AddMemeRegisterView(BrowserView):
    def __init__(self, context, request):
        super(AddMemeRegisterView, self).__init__(context, request)

    def __call__(self):
        context = self.context
        tag = self.request.form.get('tag', None)
        content_title = self.request.form.get('file_name', None)
        file_ext = os.path.splitext(content_title)[1]
        file_data = self.request.form.get('file', None)
        meme_file = NamedBlobFile(data=file_data, filename=content_title)
        portal_catalog = getToolByName(context, 'portal_catalog')

        img_ext = ['.jpg', '.JPG', '.jpeg', '.png', '.gif', '.tif', '.tiff', '.bmp', '.webp', '.svg', '.jfif']
        vid_ext = ['.mp4', '.webm', '.ogg', '.ogv', '.avi', '.mov', '.wmv', '.flv', '.mpg', '.mpeg', '.3gp', '.3g2']

        Folder = portal_catalog(portal_type='Folder')
        if not Folder:
            return 'Folder'
        else:
            Folder = Folder[0].getObject()

        meme_obj = api.content.create(
            type='Meme',
            title=content_title,
            container=Folder,
            safe_id = True,
        )

        print(tag)

        if file_ext in img_ext:
            meme_file = NamedBlobImage(data=file_data, filename=content_title)
            setattr(meme_obj, 'meme_image', meme_file)
        elif file_ext in vid_ext:
            meme_file = NamedBlobFile(data=file_data, filename=content_title)
            setattr(meme_obj, 'meme_video', meme_file)
        else:
            return json.dumps({'status': 'error', 'msg': 'File type not supported'})


        setattr(meme_obj, 'description', tag)
        #index_list = ['memefile', 'description']
        #meme_obj.reindexObject(idxs=index_list)
        meme_obj.reindexObject()

        return json.dumps({'status': 'success', 'UUID':meme_obj.UID(), 'link': meme_obj.absolute_url(), 'title': meme_obj.title})
