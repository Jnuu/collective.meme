# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from collective.memes import _
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


# from collective.memes import _


class IMeme(model.Schema):
    """ Marker interface and Dexterity Python Schema for Meme
    """

    meme_image = namedfile.NamedBlobImage(
        title=_(u'Meme Image'),
        required=False,
    )

    meme_video = namedfile.NamedBlobFile(
        title=_(u'Meme Video'),
        required=False,
    )

    date = schema.Date(
        title=_(u'Date'),
        required=False,
    )

    


@implementer(IMeme)
class Meme(Container):
    """ Content-type class for IMeme
    """
