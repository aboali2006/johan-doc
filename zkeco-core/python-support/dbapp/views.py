#coding=utf-8
from django.template import Context, RequestContext, Template, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from data_utils import QueryData
from base.model_utils import GetModel
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
import os
from django.template import loader, Context
from utils import *
import datetime
import subprocess
from django.contrib.auth.decorators import login_required

BACKUP_IMMEDIATELY = 1
BACKUP_SCHEDULED = 2


def customSql(sql,action=True):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        if action:
            connection._commit()
        return cursor
    except:
        return None


def batchSql(sqls):
    for s in sqls:
        try:
            customSql(s)
            connection._commit()
#       print "OK1: ", s
        except:
            try:
                connection.close()
                customSql(s)
#       print "OK2: ", s
            except Exception, e:
#       print "SQL: ", s
#           print "ERROR: ", e.message
                pass

def createDefautValue():
    sqls=(
        "ALTER TABLE departments ADD CONSTRAINT sdf DEFAULT 1 FOR supdeptid",
        "ALTER TABLE userinfo ADD CONSTRAINT ddf DEFAULT 1 FOR defaultdeptid",
        "ALTER TABLE userinfo ADD CONSTRAINT tdf DEFAULT 1 FOR ATT",
        "ALTER TABLE userinfo ADD CONSTRAINT otdf DEFAULT 1 FOR OverTime",
        "ALTER TABLE userinfo ADD CONSTRAINT hdf DEFAULT 1 FOR Holiday",
        "ALTER TABLE userinfo ADD CONSTRAINT ldf DEFAULT 1 FOR Lunchduration",
        "ALTER TABLE userinfo ADD CONSTRAINT sepdf DEFAULT 1 FOR SEP",
        "ALTER TABLE userinfo ADD CONSTRAINT offdutydf DEFAULT 0 FOR OffDuty",
        "ALTER TABLE userinfo ADD CONSTRAINT DelTagdf DEFAULT 0 FOR DelTag",
        "ALTER TABLE userinfo ADD CONSTRAINT enamedf DEFAULT ' ' FOR name",
        "ALTER TABLE template ADD CONSTRAINT fiddf DEFAULT 0 FOR FingerID",
        "ALTER TABLE template ADD CONSTRAINT vdf DEFAULT 1 FOR Valid",
        "ALTER TABLE template ADD CONSTRAINT dtdf DEFAULT 0 FOR DelTag",
        "ALTER TABLE checkinout ADD CONSTRAINT stdf DEFAULT 'I' FOR checktype",
        "ALTER TABLE checkinout ADD CONSTRAINT vcedf DEFAULT 0 FOR verifycode",
        "ALTER TABLE checkexact ADD CONSTRAINT uidf DEFAULT 0 FOR UserID",
        "ALTER TABLE checkexact ADD CONSTRAINT ctdf DEFAULT 0 FOR CHECKTIME",
        "ALTER TABLE checkexact ADD CONSTRAINT ctydf DEFAULT 0 FOR CHECKTYPE",
        "ALTER TABLE checkexact ADD CONSTRAINT isdf DEFAULT 0 FOR ISMODIFY",
        "ALTER TABLE checkexact ADD CONSTRAINT idldf DEFAULT 0 FOR ISDELETE",
        "ALTER TABLE checkexact ADD CONSTRAINT icdf DEFAULT 0 FOR INCOUNT",
        "ALTER TABLE checkexact ADD CONSTRAINT icodf DEFAULT 0 FOR ISCOUNT",
        "ALTER TABLE holidays ADD CONSTRAINT hddf DEFAULT 1 FOR HolidayDay",
        "ALTER TABLE NUM_RUN_DEIL ADD CONSTRAINT siddf DEFAULT -1 FOR SchclassID",
        "ALTER TABLE NUM_RUN ADD CONSTRAINT oldiddf DEFAULT -1 FOR OLDID",
        "ALTER TABLE NUM_RUN ADD CONSTRAINT sddf DEFAULT '2000-1-1' FOR StartDate",
        "ALTER TABLE NUM_RUN ADD CONSTRAINT eddf DEFAULT '2099-12-31' FOR EndDate",
        "ALTER TABLE NUM_RUN ADD CONSTRAINT cedf DEFAULT 1 FOR Cyle",
        "ALTER TABLE NUM_RUN ADD CONSTRAINT usdf DEFAULT 1 FOR Units",
        "ALTER TABLE USER_OF_RUN ADD CONSTRAINT sdedf DEFAULT '1900-1-1' FOR StartDate",
        "ALTER TABLE USER_OF_RUN ADD CONSTRAINT ede1df DEFAULT '2099-12-31' FOR EndDate",
        "ALTER TABLE USER_OF_RUN ADD CONSTRAINT irndf DEFAULT 0 FOR ISNOTOF_RUN",
        "ALTER TABLE USER_SPEDAY ADD CONSTRAINT ssdf DEFAULT '1900-1-1' FOR StartSpecDay",
        "ALTER TABLE USER_SPEDAY ADD CONSTRAINT diddf DEFAULT -1 FOR DateID",
        "ALTER TABLE USER_SPEDAY ADD CONSTRAINT esddf DEFAULT '2099-12-31' FOR EndSpecDay",
        "ALTER TABLE USER_TEMP_SCH ADD CONSTRAINT otedf DEFAULT 0 FOR OverTime",
        "ALTER TABLE USER_TEMP_SCH ADD CONSTRAINT tedf DEFAULT 0 FOR Type",
        "ALTER TABLE USER_TEMP_SCH ADD CONSTRAINT fgdf DEFAULT 1 FOR Flag",
        "ALTER TABLE USER_TEMP_SCH ADD CONSTRAINT ssiddf DEFAULT -1 FOR SchclassID",
        "ALTER TABLE LeaveClass ADD CONSTRAINT mudf DEFAULT 1 FOR MinUnit",
        "ALTER TABLE LeaveClass ADD CONSTRAINT utdf DEFAULT 1 FOR Unit",
        "ALTER TABLE LeaveClass ADD CONSTRAINT rpdf DEFAULT 1 FOR RemaindProc",
        "ALTER TABLE LeaveClass ADD CONSTRAINT rcdf DEFAULT 1 FOR RemaindCount",
        "ALTER TABLE LeaveClass ADD CONSTRAINT rsdf DEFAULT '-' FOR ReportSymbol",
        "ALTER TABLE LeaveClass ADD CONSTRAINT coldf DEFAULT 0 FOR Color",
        "ALTER TABLE LeaveClass ADD CONSTRAINT cfydf DEFAULT 0 FOR Classify",
        "ALTER TABLE LeaveClass ADD CONSTRAINT dedudf DEFAULT 0 FOR Deduct",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT mutdf DEFAULT 1 FOR MinUnit",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT uitdf DEFAULT 0 FOR Unit",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT rpcdf DEFAULT 2 FOR RemaindProc",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT rctdf DEFAULT 1 FOR RemaindCount",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT rsldf DEFAULT '_' FOR ReportSymbol",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT dctdf DEFAULT 0 FOR Deduct",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT colodf DEFAULT 0 FOR Color",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT cifydf DEFAULT 0 FOR Classify",
        "ALTER TABLE LeaveClass1 ADD CONSTRAINT ltedf DEFAULT 0 FOR LeaveType",
        "ALTER TABLE SchClass ADD CONSTRAINT cindf DEFAULT 1 FOR CheckIn",
        "ALTER TABLE SchClass ADD CONSTRAINT coudf DEFAULT 1 FOR CheckOut",
        "ALTER TABLE SchClass ADD CONSTRAINT colordf DEFAULT 16715535 FOR Color",
        "ALTER TABLE SchClass ADD CONSTRAINT abdf DEFAULT 1 FOR AutoBind",
        "CREATE UNIQUE INDEX USERFINGER ON TEMPLATE(USERID, FINGERID)",
        "CREATE UNIQUE INDEX HOLIDAYNAME ON HOLIDAYS(HOLIDAYNAME)",
        "CREATE INDEX DEPTNAME ON DEPARTMENTS(DEPTNAME)",
        "CREATE UNIQUE INDEX EXCNOTE ON EXCNOTES(USERID, ATTDATE)",
        "ALTER TABLE iclock ADD CONSTRAINT accfundf DEFAULT 0 FOR AccFun",
        "ALTER TABLE iclock ADD CONSTRAINT tzadjdf DEFAULT 8 FOR TZAdj",
        "ALTER TABLE user_temp_sch ADD CONSTRAINT ovt default 0 FOR OverTime",
    )
    batchSql(sqls);

def initDB():

    #upgradeDB()
    #createDefautValue()
#   return
    if AttParam.objects.all().count()==0:
        AttParam(ParaName='MinsEarly',ParaValue="5").save()
        AttParam(ParaName='MinsLate',ParaValue="10").save()
        AttParam(ParaName='MinsNoBreakIn',ParaValue="60").save()
        AttParam(ParaName='MinsNoBreakOut',ParaValue="60").save()
        AttParam(ParaName='MinsNoIn',ParaValue="60").save()
        AttParam(ParaName='MinsNoLeave',ParaValue="60").save()
        AttParam(ParaName='MinsNotOverTime',ParaValue="60").save()
        AttParam(ParaName='MinsWorkDay',ParaValue="480").save()
        AttParam(ParaName='NoBreakIn',ParaValue="1012").save()
        AttParam(ParaName='NoBreakOut',ParaValue="1012").save()
        AttParam(ParaName='NoIn',ParaValue="1001").save()
        AttParam(ParaName='NoLeave',ParaValue="1002").save()
        AttParam(ParaName='OutOverTime',ParaValue="0").save()
        AttParam(ParaName='TwoDay',ParaValue="0").save()
        AttParam(ParaName='CheckInColor',ParaValue="16777151").save()
        AttParam(ParaName='CheckOutColor',ParaValue="12910591").save()
        AttParam(ParaName='DBVersion',ParaValue="1").save()
        AttParam(ParaName='InstallDate',ParaValue=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).save()
        AttParam(ParaName='ADMSDBVersion',ParaValue="202").save()

    if LeaveClass.objects.all().count()==0:
        LeaveClass(LeaveName="%s"%'Business leave',MinUnit=0.5,Unit=3,RemaindProc=1,RemaindCount=1,ReportSymbol='G',Classify=128).save()
        LeaveClass(LeaveName="%s"%'Sick leave',Unit=1,ReportSymbol='B',Color=3398744).save()
        LeaveClass(LeaveName="%s"%'Private affair leave',Unit=1,ReportSymbol='S',Color=8421631).save()
        LeaveClass(LeaveName="%s"%'Home leave',Unit=1,ReportSymbol='T',Color=16744576).save()
    if LeaveClass1.objects.all().count()==0:

        """ 将公出999从leaveclass1中移走,归到假类设置中"""
#   LeaveClass1(LeaveID=999,LeaveName="%s"%'BL',MinUnit=0.5,Unit=3,RemaindProc=1,RemaindCount=1,ReportSymbol='G',LeaveType="3",Calc='if(AttItem(LeaveType1)=999,AttItem(LeaveTime1),0)+if(AttItem(LeaveType2)=999,AttItem(LeaveTime2),0)+if(AttItem(LeaveType3)=999,AttItem(LeaveTime3),0)+if(AttItem(LeaveType4)=999,AttItem(LeaveTime4),0)+if(AttItem(LeaveType5)=999,AttItem(LeaveTime5),0)').save()
        LeaveClass1(LeaveID=1000,LeaveName="%s"%'OK',MinUnit=0.5,Unit=3,RemaindProc=1,RemaindCount=0,ReportSymbol=' ',LeaveType="3").save()
        LeaveClass1(LeaveID=1001,LeaveName="%s"%'Late',MinUnit=10,Unit=2,RemaindProc=2,RemaindCount=1,ReportSymbol='>',LeaveType="3").save()
        LeaveClass1(LeaveID=1002,LeaveName="%s"%'Early',MinUnit=10,Unit=2,RemaindProc="2",RemaindCount="1",ReportSymbol='<',LeaveType="3").save()
        LeaveClass1(LeaveID=1003,LeaveName="%s"%'ALF',MinUnit="1",Unit="1",RemaindProc="1",RemaindCount="1",ReportSymbol='V',LeaveType="3").save()
        LeaveClass1(LeaveID=1004,LeaveName="%s"%'Absent',MinUnit="0.5",Unit="3",RemaindProc="1",RemaindCount="0",ReportSymbol='A',LeaveType="3").save()
        LeaveClass1(LeaveID=1005,LeaveName="%s"%'OT',MinUnit="1",Unit="1",RemaindProc="1",RemaindCount="1",ReportSymbol='+',LeaveType="3").save()
        LeaveClass1(LeaveID=1006,LeaveName="%s"%'OTH',MinUnit="1",Unit="1",RemaindProc="0",RemaindCount="1",ReportSymbol='=',LeaveType="0").save()
        LeaveClass1(LeaveID=1007,LeaveName="%s"%'Hol.',MinUnit="0.5",Unit="3",RemaindProc="2",RemaindCount="1",ReportSymbol='-',LeaveType="2").save()
        LeaveClass1(LeaveID=1008,LeaveName="%s"%'NoIn',MinUnit="1",Unit="4",RemaindProc="2",RemaindCount="1",ReportSymbol='[',LeaveType="2").save()
        LeaveClass1(LeaveID=1009,LeaveName="%s"%'NoOut',MinUnit="1",Unit="4",RemaindProc="2",RemaindCount="1",ReportSymbol=']',LeaveType="2").save()
        LeaveClass1(LeaveID=1010,LeaveName="%s"%'ROT',MinUnit="1",Unit="4",RemaindProc="2",RemaindCount="1",ReportSymbol='{',LeaveType="3").save()
        LeaveClass1(LeaveID=1011,LeaveName="%s"%'BOUT',MinUnit="1",Unit="4",RemaindProc="2",RemaindCount="1",ReportSymbol='}',LeaveType="3").save()
        LeaveClass1(LeaveID=1012,LeaveName="%s"%'OUT',MinUnit="1",Unit="1",RemaindProc="2",RemaindCount="1",ReportSymbol='L',LeaveType="3").save()
        LeaveClass1(LeaveID=1013,LeaveName="%s"%'FOT',MinUnit="1",Unit="1",RemaindProc="2",RemaindCount="1",ReportSymbol='F',LeaveType="3").save()

    if User.objects.all().count()==0:
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')


#初始化数据库
def init_db(request):
        #initDB()
        response = HttpResponse(mimetype='text/plain')
        response.write("Init db success!\n")
        return response
#备份数据库
#def backup_db(request):
#    pass

#还原数据库
def restore_db(request):

    from dbapp.models import DbBackupLog
    k =  request.GET.get('K',None)
    i= DbBackupLog.objects.get(pk=k)
    database_engine = settings.DATABASES["default"]["ENGINE"]
    database_user = settings.DATABASES["default"]["USER"]
    database_password = settings.DATABASES["default"]["PASSWORD"]
    database_name = settings.DATABASES["default"]["NAME"]
    database_host = settings.DATABASES["default"]["HOST"]
    #print database_engine,'-----------database_engine---------'
    if i:
        if i.successflag!='1':
            return getJSResponse('{ Info:"fail",msg:"'+ _(u'请选择已成功备份的记录!') +'"}')
        else:
            backup_file = ''
            cmd = ''
            if database_engine == "django.db.backends.mysql":
                backup_file = settings.APP_HOME+"\\tmp\\db_" +i.starttime.strftime("%Y%m%d%H%M%S") +'.sql'
                cmd = "mysql -u%s -p%s -h %s --database %s <%s"%(database_user,database_password,database_host,database_name,backup_file)
            elif database_engine == "sqlserver_ado":
                backup_file = settings.APP_HOME+"\\tmp\\db_" + i.starttime.strftime("%Y%m%d%H%M%S") +".bak"
                cmd = '''sqlcmd -U %s -P %s -S %s -Q "ALTER DATABASE zkeco SET OFFLINE WITH ROLLBACK IMMEDIATE;restore database %s from disk='%s';alter   database  zkeco  set   online"'''%(database_user,database_password,database_host,database_name,backup_file)
            else:
                backup_file = settings.APP_HOME+"\\tmp\\db_" + i.starttime.strftime("%Y%m%d%H%M%S") +".dmp"
                backup_file = "imp %s/%s@%s file='%s' full=y"%(database_user,database_password,database_name,backup_file)
            if not os.path.isfile(backup_file):
                return getJSResponse('{ Info:"fail",msg:"'+ _(u'备份文件不存在!') +'"}')
            else:
                #os.system("manage.py loaddata " + restore_file)
                #p = subprocess.Popen("manage.py loaddata "+backup_file,shell=True,stderr=subprocess.PIPE)
                #print backup_file,'--------------backup_file--------------'
                p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                p.wait()
                stderrdata = p.communicate()
                #print p.returncode,'-----------p.returncode---------'
                #print stderrdata,'-----------stderrdata-------------'
                if p.returncode!=0:
                    return getJSResponse('{ Info:"fail",msg:"'+ stderrdata +'"}')
                elif p.returncode==0:
                    return getJSResponse('{ Info:"OK" }')

    else:
        return getJSResponse('{ Info:"fail" }')


def get_chioce_data_widget(request, app_label, model_name):
    '''
    对象选择部件ajax返回
    '''
    from widgets import form_field, check_limit
    import sys
    model=GetModel(app_label, model_name)
    multiple=request.GET.get('multiple', False) #---是否多选
    depttree=request.GET.get('depttree', False) #---是否为选择部门
    c = sys.modules['mysite.personnel.models.depttree']
    if depttree:
        dept_treeview = getattr(c,'dept_treeview')
        return HttpResponse(dept_treeview())
    field=None
    m=sys.modules[model.__module__]
    for p in dir(m):
        try:
            mp=getattr(m,p)
            if issubclass(mp, models.ForeignKey) and not multiple:
                field=mp()
                break
            elif issubclass(mp, models.ManyToManyField) and multiple:
                field=mp(model)
                break
        except:
            pass
    if field is None:
        if multiple:
            field=models.ManyToManyField(model)
        else:
            field=models.ForeignKey(model)

    w_name=request.GET.get('name', '%s'%model.__name__)
    qs, cl=QueryData(request, model)

    ZDeptMultiChoiceDropDownWidget = getattr(c,'ZDeptMultiChoiceDropDownWidget')
    ZDeptChoiceFlatWidget = getattr(c,'ZDeptChoiceFlatWidget')

    flat=request.GET.get('flat', "True")
    wg=request.GET.get('widget', False)
    if (model.__name__=="Department" or model.__name__=="Area") and multiple  and  flat=="False":   #---------------------改点
        f=form_field(field,widget=ZDeptMultiChoiceDropDownWidget)
    elif wg:
        f=form_field(field,widget=locals()[wg])
    else:
        f=form_field(field)
    html=f.widget.render(w_name, model.objects.none())
    return HttpResponse(html)


def option(request,usr,catalog):
    from base.options import OptionForm
    from django.core.cache import cache
    if usr.is_anonymous():
        return HttpResponse("session_fail_or_no_permission")
    if request.method=='POST':
            f=OptionForm(catalog,usr, request.POST)
            if f.is_valid(): # All validation rules pass Process the data in form.cleaned_data
                    try:
                            f.save()
                            k="user_id_%s"%usr.pk
                            cache.delete(k)
                    except Exception, e: #保存失败
                            import traceback; traceback.print_exc()
                            from data_edit import NON_FIELD_ERRORS
                            f.errors[NON_FIELD_ERRORS]=u'<ul class="errorlist"><li>%s</li></ul>'%e
                    else:
                            cache.delete(u"%s_%s"%(usr.username,"menu_list"))
                            if request.is_ajax():
                                    return getJSResponse('{ Info:"OK" }')
    else:
            f=OptionForm(catalog,usr)
    return render_to_response(['user_option_form.html','data_edit.html'],
            {'form':f, 'title':_(u'个人选项')},
            context_instance=RequestContext(request))


def sys_option(request):
    from base.options import SYSPARAM
    from dbapp.urls import dbapp_url, surl
    from base import get_all_app_and_models
    from django.core.urlresolvers import reverse

    model_url=reverse(sys_option)
    apps=get_all_app_and_models()
    is_ajax=request.REQUEST.get("a",None)
    #if request.is_ajax():#ie6中没用
    if is_ajax:
        return option(request,None,SYSPARAM)
    if request.method=='GET':
        return render_to_response('sys_option.html',
            RequestContext(request, {
            'surl': surl,
            'dbapp_url': dbapp_url,
            'MEDIA_URL': settings.MEDIA_ROOT,
            "current_app":'base',
            'apps':apps,
            'model_url':model_url,
            'menu_focus':'sys_option',
        }))

def user_option(request):
    from base.options import PERSONAL
    return option(request,request.user,PERSONAL)

#验证在当前时间的一个小时内只能备份一次数据库
@login_required
def backup_db_validate(request, type):
    from dbapp.models import DbBackupLog
    from base.backup import get_backup_path
    path = get_backup_path()
    if path == "":
        return getJSResponse('{ Info:"null"}')
    if not os.path.exists(path):
        return getJSResponse('{Info:"notexist"}')
    
    #type = int(request.REQUEST.get("type", 0))
    if int(type) == BACKUP_IMMEDIATELY:
        end_dt = datetime.datetime.now()
        start_dt = (end_dt+datetime.timedelta(hours=-settings.DB_DBCKUP_STEPTIME))
        cc = DbBackupLog.objects.filter(starttime__range=(start_dt,end_dt))
        if cc :
            return getJSResponse('{ Info:"fail"}')
        else:
            return getJSResponse('{ Info:"OK" }')
    else:
        return getJSResponse('{ Info:"OK" }')



def getBackupsched(request):
    from base.options import PersonalOption
    i=PersonalOption.objects.filter(user=request.user,option__name="backup_sched")
    if i:
        starttime,inc= i[0].value.split("|")
        return getJSResponse('{Info:"OK",starttime:"' + starttime +'",inc:"' + inc+'"}')
    else:
        return getJSResponse('{Info:"fail"}')


def get_init_db_data(request):
    import json
    from urls import surl
    t=loader.get_template("init_models.html")
    json_html=t.render(Context({}))
    py_dict=json.loads(json_html)
    #过滤配置文件中配置了不让显示的项
    dict_filter={}
    try:
        for k in py_dict:
            dict_filter[k]={}
            for kk in py_dict[k]:
                list_models= []
                for ee in py_dict[k][kk]:
                    app_label,model_name=ee.split(".")
                    if settings.APP_CONFIG[app_label][model_name]!="False" and [e for e in settings.INSTALLED_APPS if e.split(".")[-1]==app_label]:
                        list_models.append(ee)
                if len(list_models)!=0:
                    dict_filter[k][kk]=list_models
            if not dict_filter[k]:
                dict_filter.pop(k)
    except:
        import traceback;traceback.print_exc()

    #print  dict_filter
    #print 'dict_filter-------------------------'
    return getJSResponse(json.dumps(dict_filter))

def update_process(request):
    
    try:
        from django.utils.encoding import smart_str
        from django.utils.simplejson  import dumps
        from django.db import connection
    
        datas = request.POST.get("datas")
        if datas == "":
            return HttpResponse("")
        datas = datas.split(",")
        list_id = '('
        for i  in datas:
            list_id = list_id+i+','
        list_id = list_id[0:-1]
        list_id = list_id+')'
        sql = "select id,successflag from dbbackuplog where id in %s and successflag in ('1','2')"%list_id
        #print sql,'-----------sql'
        cursor = connection.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        #print smart_str(dumps(ret)),'-----------------ret'
        return HttpResponse(smart_str(dumps(ret)))
    except:
        import traceback
        traceback.print_exc()
    