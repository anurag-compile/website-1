from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtail.wagtailcore.blocks import BooleanBlock
from wagtail.wagtailcore.blocks import CharBlock
from wagtail.wagtailcore.blocks import ChoiceBlock
from wagtail.wagtailcore.blocks import ListBlock
from wagtail.wagtailcore.blocks import PageChooserBlock
from wagtail.wagtailcore.blocks import RawHTMLBlock
from wagtail.wagtailcore.blocks import RichTextBlock
from wagtail.wagtailcore.blocks import StreamBlock
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailcore.blocks import TextBlock
from wagtail.wagtailcore.blocks import URLBlock

from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


''' Blocks '''


class LinkBlock(StructBlock):
    uri = CharBlock(required=True)
    text = CharBlock(required=True)

    class Meta:
        icon = 'link'


class CallToActionBlock(LinkBlock):
    button_icon = CharBlock(required=False)
    color = ChoiceBlock([('black', 'Black'),
                         ('white', 'White')],
                        required=True)
    size = ChoiceBlock([('lg', 'Large'),
                        ('md', 'Medium'),
                        ('sm', 'Small'),
                        ('xs', 'Extra Small')])

    class Meta:
        icon = 'link'
        template = 'blocks/call_to_action.html'


class CarouselFrame(StructBlock):
    headline = CharBlock(required=True,
                         help_text='The main, all caps text of the frame.')
    taglines = ListBlock(CharBlock(help_text='The smaller, regular cased text '
                                             'under the headline.'))
    image = ImageChooserBlock(required=True,
                              help_text='The image serving as the background '
                                        'of the frame. Minimum 1080 pixels '
                                        'wide.')
    color = ChoiceBlock(choices=[('dark', 'Dark'),
                                 ('light', 'Light')],
                        icon='cog')
    call_to_action = ListBlock(LinkBlock(),
                               required=False,
                               help_text='Large button to direct user to '
                                         'specific content. Last element '
                                         'has greatest emphasis.')
    signup_form = BooleanBlock(required=False,
                               help_text='Check to display an email '
                                         'signup form in this frame.')

    class Meta:
        icon = 'image'
        template = 'blocks/carousel_frame.html'


class ContentBlock(StructBlock):
    width = ChoiceBlock(choices=[('2', '2 columns'),
                                 ('3', '3 columns'),
                                 ('4', '4 columns'),
                                 ('5', '5 columns'),
                                 ('6', '6 columns'),
                                 ('7', '7 columns'),
                                 ('8', '8 columns'),
                                 ('9', '9 columns'),
                                 ('10', '10 columns'),
                                 ('11', '11 columns'),
                                 ('12', '12 columns')],
                        required=True,
                        help_text='Length in Bootstrap columns for '
                                  'display on desktop.')
    offset = ChoiceBlock(choices=[('2', '2 columns'),
                                  ('3', '3 columns'),
                                  ('4', '4 columns'),
                                  ('5', '5 columns'),
                                  ('6', '6 columns'),
                                  ('7', '7 columns'),
                                  ('8', '8 columns'),
                                  ('9', '9 columns'),
                                  ('10', '10 columns'),
                                  ('11', '11 columns'),
                                  ('12', '12 columns')],
                         required=False,
                         help_text='Offset in Bootstrap columns for '
                                   'display on desktop.')

    class Meta:
        icon = 'doc-empty'


class PromoParagraphBlock(ContentBlock):
    body = StreamBlock([('text', RichTextBlock()),
                        ('call_to_action', ListBlock(CallToActionBlock())),
                        ('spacer', ChoiceBlock(choices=[('15', '15 pixels'),
                                                        ('30', '30 pixels'),
                                                        ('45', '45 pixels'),
                                                        ('60', '60 pixels'),
                                                        ('75', '75 pixels'),
                                                        ('90', '90 pixels')],
                                               required=False))])
    class Meta:
        template = 'blocks/promo_paragraph.html'


class SkillBarBlock(ContentBlock):

    skills = ListBlock(StructBlock([('skill_percentage', CharBlock()),
                                    ('skill_name', CharBlock())]))
    class Meta:
        icon = 'media'
        template = 'blocks/skillbar.html'


class ContentRow(StreamBlock):
    title = CharBlock(required=False)
    promo_paragraph = PromoParagraphBlock()
    skillbar = SkillBarBlock()

    class Meta:
        icon = 'horizontalrule'
        template = 'blocks/content_row.html'


class QuoteBlock(StructBlock):
    quotation = CharBlock()
    author = CharBlock(required=False)
    title = CharBlock(required=False)

    class Meta:
        icon = 'openquote'


class QuotationsBlock(StructBlock):
    quotations = ListBlock(QuoteBlock())
    image = ImageChooserBlock(required=True,
                              help_text='The image serving as the background '
                                        'of the quotations. Minimum 1080 pixels '
                                        'wide.')
    color = ChoiceBlock([('light', 'Light'),
                         ('dark', 'Dark')])

    class Meta:
        icon = 'openquote'
        template = 'blocks/quotations.html'


'''Page models'''


class HomePage(Page):
    author = models.CharField(max_length=255, blank=True)
    body = StreamField([('heading', CharBlock(classname='full title')),
                        ('carousel', ListBlock(CarouselFrame(),
                                               icon='cogs',
                                               template='blocks/carousel.html',
                                               help_text='A horizontal '
                                                         'scrolling set '
                                                         'of images with text '
                                                         'overlaid.')),
                        ('content_row', ContentRow()),
                        ('quotations', QuotationsBlock()),
                        ('paragraph', RichTextBlock()),
                        ('image', ImageChooserBlock())], blank=True)

HomePage.content_panels = [FieldPanel('title',
                                      classname='full title'),
                           StreamFieldPanel('body')]
