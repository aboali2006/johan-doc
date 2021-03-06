# -*- coding: utf-8 -*-
'''
定义了用户操作日志记录模型
'''
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from model_admin import ModelAdmin, CACHE_EXPIRE
#basetranslation import ugettext_lazy as _

ADDITION = 1
CHANGE = 2
DELETION = 3
OTHER_ACTION = 4
LOGIN = 5

class LogEntryManager(models.Manager):
        def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
                e = self.model(None, None, user_id, content_type_id, smart_unicode(object_id), object_repr[:200], action_flag, change_message)
                e.save(force_insert=True)
        def log_action_other(self, user_id, object, change_message=''):
                obj=None
                obj_str=""
                if isinstance(object, models.Model):
                        content_type_id=ContentType.objects.get_for_model(object.__class__).pk
                        obj=object.pk
                        obj_str=u"%s"%object
                else:
                        content_type_id=ContentType.objects.get_for_model(object).pk
                self.log_action(user_id, content_type_id, obj, obj_str, OTHER_ACTION, change_message)
from operation import  Operation
class LogEntry(models.Model):
        action_time = models.DateTimeField(_(u'动作时间'), auto_now=True)
        user = models.ForeignKey(User, verbose_name=_(u"用户"), null=True, related_name="logentryofuser")
        content_type = models.ForeignKey(ContentType, verbose_name=_(u"对象类型"), blank=True, null=True, related_name="logentryofct")
        object_id = models.CharField(_(u'对象ID'), max_length=100, blank=True, null=True)
        object_repr = models.CharField(_(u'对象描述'), max_length=200)
        action_flag = models.PositiveSmallIntegerField(_(u'动作标识'), choices=
                ((ADDITION, _(u"增加")),
                 (CHANGE,   _(u"修改")),
                 (DELETION, _(u"删除")),
                 (OTHER_ACTION, _(u"其他")),
                 (LOGIN, _(u"登录"))
                )
        )
        change_message = models.CharField(_(u'改变消息'), max_length=512, blank=True)
        objects = LogEntryManager()
        
        #初始化表
        @staticmethod
        def clear():
            LogEntry.objects.all().delete()

        class dataexport(Operation):
            help_text=_(u"数据导出") #导出
            verbose_name=_(u"导出")
            visible=False
            def action(self):
                    pass
        def __repr__(self):
                return smart_unicode(self.action_time)
        
        def __unicode__(self):
                return u"[%s]%s: %s %s"%(self.action_time, self.user, self.get_action_flag_display(), self.object_repr)

        def is_addition(self):
                return self.action_flag == ADDITION

        def is_change(self):
                return self.action_flag == CHANGE

        def is_deletion(self):
                return self.action_flag == DELETION

        def get_edited_object(self):
                "Returns the edited object represented by this log entry"
                return self.content_type.get_object_for_this_type(pk=self.object_id)

        class Admin(ModelAdmin):
                query_fields=['user__username','content_type__name','action_flag']
                list_display=('user','action_time|fmt_datetime','content_type', 'object_repr', 'action_flag', 'change_message')
                list_filter=('action_time', 'user', 'action_flag', 'content_type')
                disabled_perms=["change_logentry","add_logentry","delete_logentry"]
                read_only=True
                menu_index=10000
        class Meta:
                verbose_name = _(u'日志记录')
                verbose_name_plural = _(u'日志记录')
                db_table = 'action_log'
                ordering = ('-action_time',)
        


