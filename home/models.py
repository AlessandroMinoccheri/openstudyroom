from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django import forms
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, \
        RichTextBlock, RawHTMLBlock, IntegerBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.signals import page_published
from wagtailmenus.models import MenuPage
from puput.models import EntryPage, BlogPage
import requests
import random
from fullcalendar.models import AvailableEvent, GameRequestEvent


@register_snippet
@python_2_unicode_compatible  # provide equivalent __unicode__ and __str__ methods on Python 2
class Advert(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
        FieldPanel('body', classname="full"),
    ]

    def __str__(self):
        return self.title


@register_snippet
@python_2_unicode_compatible  # provide equivalent __unicode__ and __str__ methods on Python 2
class Quote(models.Model):
    text = models.TextField(blank=True, null=True, max_length=100)
    source= models.TextField(blank=True, null=True, max_length=20)
    panels = [
        FieldPanel('text'),
        FieldPanel('source'),
    ]

    def __str__(self):
        return self.text[0:30]

# Global Streamfield definition


class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class WgoAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('right', 'Right'), ('left', 'Left'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"

class WgoBlock(StructBlock):
    sgf = DocumentChooserBlock()
    alignment = WgoAlignmentChoiceBlock()
    width = IntegerBlock(default=700)
    class Meta:
        icon = "placeholder"
        template = "wgo/wgoblock.html"


class MyStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")
    wgo = WgoBlock(label="wgo")


class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        entries = EntryPage.objects.live().order_by('-date')[0:3]
        blog_page = BlogPage.objects.all().first()
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['entries'] = entries
        context['blog_page'] = blog_page
        quote = random.choice(Quote.objects.all())
        context['quote'] = quote
        '''
        user = request.user
        if user.is_authenticated and user.is_league_member:
            now = timezone.now()
            opponents = user.get_opponents()
            if opponents is False:
                context['should_join'] = True
            else:
                availables = AvailableEvent.objects.filter(
                    end__gte=now,
                    user__in=opponents
                ).order_by('start')[:5]
                context['availables'] = availables
                online_opponents = list(filter(
                    lambda user: user.is_online(),
                    opponents
                ))
                context['online_opponents'] = online_opponents
                game_requests = GameRequestEvent.objects.filter(
                    receivers=user,
                    end__gte=now
                ).count()
                context['game_requests'] = game_requests
            me_available = AvailableEvent.objects.filter(
                user=user,
                end__gte=now
            ).exists()
            context['me_available'] = me_available
            '''
        return context


class FullWidthPage(MenuPage):
    body = StreamField(MyStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

class RightSidebarPage(MenuPage):
    body = StreamField(MyStreamBlock(), blank=True)

    content_panels = Page.content_panels + [

        StreamFieldPanel('body'),
    ]

class LeftSidebarPage(MenuPage):
    body = StreamField(MyStreamBlock(), blank=True)

    content_panels = Page.content_panels + [

        StreamFieldPanel('body'),
    ]

class StreamFieldEntryPage(EntryPage):
    streamfield = StreamField(MyStreamBlock(), blank=True)
    content_panels = EntryPage.content_panels + [
        StreamFieldPanel('streamfield')
    ]
BlogPage.subpage_types.append(StreamFieldEntryPage)


# Let everyone know when a new page is published
def send_to_discord(sender, **kwargs):
    instance = kwargs['instance']
    # Only post new post. No updates.
    if instance.first_published_at != instance.last_published_at:
        return

    if settings.DEBUG:
        discord_url = 'http://example.com/' # change this for local test
    else:
        with open('/etc/discord_hook_url.txt') as f:
            discord_url = f.read().strip()

    excerpt = render_to_string(
        'home/includes/excerpt.html',
        {'entry': instance}
    )
    # I tryed to convert excerpt to markdown using tomd without success
    values = {
        "content": "Breaking news on OSR website !",
        "embeds": [{
            "title": instance.title,
            "url": "https://openstudyroom.org" + instance.url,
            "description": excerpt,
        }]
    }
    r = requests.post(discord_url, json=values)
    r.raise_for_status()


# Register two receivers
page_published.connect(send_to_discord, sender=EntryPage)
page_published.connect(send_to_discord, sender=StreamFieldEntryPage)
