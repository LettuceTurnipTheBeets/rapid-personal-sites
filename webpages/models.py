import os
import re

from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, \
    StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.blocks import TextBlock, StructBlock, RichTextBlock, \
    StreamBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from .helpers import generate_image_url


class BodyStreamBlock(StreamBlock):
    heading = CharBlock(icon="title", classname="heading")
    subheading = CharBlock(icon="title", classname="subheading")
    paragraph = RichTextBlock(icon="pilcrow", classname="paragraph")
    image = ImageChooserBlock(icon="image")
    document = DocumentChooserBlock(icon="doc-full-inverse")


class WebPage(Page):
    """
    The WebPage class is the base Page model for all web pages. It should be
    generic enough to support most requirements for static pages.
    Fields:
    template_path - The path to the template used to render the page. This path
    should be a relative path starting with the name of the website the page
    is assigned to. For example, if the website is example.com, an appropriate
    template_name value would be 'example_com/about.html'
    body - A StreamField that accepts headings, subheadings, paragraphs, images
    and documents. See http://docs.wagtail.io/en/v1.5.2/topics/streamfield.html
    for more information about StreamFields. See
    https://github.com/torchbox/wagtaildemo/blob/master/demo/templates/demo/includes/streamfield.html
    for an example template that renders each block_type (i.e. heading,
    subheading, paragraph, etc...)
    sections - Sections are an array of content values that each have a title,
    content, and image value.
    images - Images are an array of images related to the page.
    """

    template_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='A path to the template to use to render the page.'
    )

    body = StreamField(
        BodyStreamBlock(),
        blank=True,
        null=True,
        help_text='The primary content for the page.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('template_path'),
        StreamFieldPanel('body'),
        InlinePanel('sections', label="Sections"),
        InlinePanel('images', label="Images")
    ]

    def get_template(self, request):
        if self.template_path:
            template = self.template_path
        else:
            template = 'web_page.html'

        if os.path.isfile('./websites/{}/templates/{}'.format(re.sub('\.', '_', request.site.hostname), template)):
            template = 'websites/%s/templates/%s' % (
                re.sub('\.', '_', request.site.hostname),
                template
            )
        else:
            template = 'webpages/templates/{}'.format(template)

        return template


class Section(Orderable):
    page = ParentalKey(WebPage, related_name='sections')
    title = models.CharField(
        max_length=255,
        help_text='The section title.'
    )
    content = RichTextField(
        null=True,
        blank=True,
        help_text='The section content.'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The section image.'
    )
    panels = [
        FieldPanel('title'),
        FieldPanel('content'),
        ImageChooserPanel('image'),
    ]


class Images(Orderable):
    page = ParentalKey(WebPage, related_name='images')
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='A thumbnail image.'
    )
    full_size = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='A full size image.'
    )
    caption = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='A caption for the image.'
    )
    meta = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Any extra information for the image.'
    )

    @property
    def full_size_url(self):
        if self.full_size:
            return generate_image_url(self.full_size, 'original')
        return None

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return generate_image_url(self.thumbnail, 'original')
        return None

    panels = [
        ImageChooserPanel('thumbnail'),
        ImageChooserPanel('full_size'),
        FieldPanel('caption'),
        FieldPanel('meta')
    ]

