from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema

_ = MessageFactory('collective.ptg.highslide')

class IHighSlideDisplaySettings(IBaseSettings):
    highslide_slideshowcontrols_position = schema.Choice(
        title=_(u"lable_highslide_slideshowcontrols_position",
            default=u"Highslide controls position"),
        description=_(u"description_highslide_slideshowcontrols_position",
            default=u"Choose the position of the slideshow controls. "
        ),
        default='bottom',
        vocabulary=SimpleVocabulary([
            SimpleTerm('top', 'top',
                _(u"label_highslide_slideshowcontrols_position_top",
                                    default=u"top")),
            SimpleTerm('middle', 'middle',
                _(u"label_highslide_slideshowcontrols_position_middle",
                                    default=u"middle")),
            SimpleTerm('bottom', 'bottom',
                _(u"label_highslide_slideshowcontrols_position_bottom",
                                    default=u"bottom")),
        ]))
    highslide_outlineType = schema.Choice(
        title=_(u"label_highslide_outlineType", default=u"Image outline type"),
        description=_(u"description_highslide_outlineType",
            default=u"The style of the border around the image. "
        ),
        default='drop-shadow',
        vocabulary=SimpleVocabulary([
            SimpleTerm('rounded-white', 'rounded-white',
                _(u"label_highslide_outlineType_rounded_white",
                                    default=u"Rounded White")),
            SimpleTerm('outer-glow', 'outer-glow',
                _(u"label_highslide_outlineType_outer_glow",
                                    default=u"Outer Glow")),
            SimpleTerm('drop-shadow', 'drop-shadow',
                _(u"label_highslide_outlineType_drop_shadow",
                                    default=u"Drop Shadow")),
            SimpleTerm('glossy-dark', 'glossy-dark',
                _(u"label_highslide_outlineType_glossy_dark",
                                    default=u"Glossy Dark")
            )
        ]))


class HighSlideDisplayType(BatchingDisplayType):

    name = u"highslide"
    schema = IHighSlideDisplaySettings
    description = _(u"label_highslide_display_type",
        default=u"Highslide - verify terms of use")
    userWarning = _(u"label_highslide_user_warning",
        default=u"You can only use the Highslide gallery for non-commercial "
                u"use unless you purchase a commercial license. "
                u"Please visit http://highslide.com/ for details."
    )
    typeStaticFilesRelative = '++resource++ptg.highslide'

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(base_url)s/highslide.css" />
""" % {'base_url': self.typeStaticFiles}

    def javascript(self):
        outlineType = "hs.outlineType = '%s';" % \
                            self.settings.highslide_outlineType
        wrapperClassName = ''

        if 'drop-shadow' in outlineType:
            wrapperClassName = 'dark borderless floating-caption'
            outlineType = ''
        elif 'glossy-dark' in outlineType:
            wrapperClassName = 'dark'
        if len(wrapperClassName) == 0:
            wrapperClassName = 'null'
        else:
            wrapperClassName = "'%s'" % wrapperClassName
        return u"""
<script type="text/javascript"
    src="%(base_url)s/highslide-with-gallery.js"></script>

<!--[if lt IE 7]>
<link rel="stylesheet" type="text/css"
  href="%(base_url)s/highslide-ie6.css" />
<![endif]-->

<script type="text/javascript">
hs.graphicsDir = '%(base_url)s/graphics/';
hs.align = 'center';
hs.transitions = ['expand', 'crossfade'];
hs.fadeInOut = true;
hs.dimmingOpacity = 0.8;
%(outlineType)s
hs.wrapperClassName = %(wrapperClassName)s;
hs.captionEval = 'this.thumb.alt';
hs.marginBottom = 105; // make room for the thumbstrip and the controls
hs.numberPosition = 'caption';
hs.autoplay = %(timed)s;
hs.transitionDuration = %(duration)i;
hs.addSlideshow({
    interval: %(delay)i,
    repeat: true,
    useControls: true,
    fixedControls: 'fit',
    overlayOptions: {
        position: '%(overlay_position)s center',
        opacity: .7,
        hideOnMouseOut: true
    },
    thumbstrip: {
        position: 'bottom center',
        mode: 'horizontal',
        relativeTo: 'viewport'
    }
});

var auto_start = %(start_automatically)s;
var start_image_index = %(start_index_index)i;

(function($){
$(document).ready(function() {
    var images = $('a.highslide');
    if(images.length <= start_image_index){
        start_image_index = 0;
    }
    if(auto_start){
        $(images[start_image_index]).trigger('click');
    }
});
})(jQuery);
</script>
        """ % {
            'outlineType': outlineType,
            'wrapperClassName': wrapperClassName,
            'delay': self.settings.delay,
            'timed': jsbool(self.settings.timed),
            'duration': self.settings.duration,
            'start_automatically': jsbool(
                self.settings.start_automatically or self.settings.timed),
            'start_index_index': self.start_image_index,
            'overlay_position': \
                self.settings.highslide_slideshowcontrols_position,
            'base_url': self.typeStaticFiles

        }
HighSlideSettings = createSettingsFactory(HighSlideDisplayType.schema)