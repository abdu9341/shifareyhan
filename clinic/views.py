from django.db.models import Q
from django.shortcuts import render, HttpResponse,redirect
from user.views import login_required
from patient.models import BasicInfo
from user.models import User
from clinic.models import *
from django.http import StreamingHttpResponse
from django.utils import timezone
from io import BytesIO
import datetime
import xlwt


@login_required
def polyclinicDepartment(request):
    """门诊科室表"""

    user = User.objects.get(account=request.session['account'])

    departments = Department.objects.all()

    return render(request, 'clinic/polyclinicDepartment.html', locals())


@login_required
def addDepartment(request):
    """添加门诊科室表"""

    if request.method == 'POST':
        arabic_name = request.POST.get('arabic_name')
        name = request.POST.get('name')

        if Department.objects.filter(Q(arabic_name=arabic_name) | Q(name=name)):

            message = 'هذا العيادات موجود'

            return render(request, 'clinic/polyclinicDepartment.html', locals())

        else:

            Department.objects.create(arabic_name=arabic_name, name=name)

        return redirect('/polyclinicDepartment/')


@login_required
def editDepartment(request, department_id):
    """编辑门诊科室"""

    department = Department.objects.get(id=department_id)

    if request.method == 'POST':
        arabic_name = request.POST.get('arabic_name')
        name = request.POST.get('name')

        # 判断是否已存在这个科室
        exist = Department.objects.filter(arabic_name=arabic_name, name=name)

        if exist:
            if department.arabic_name == arabic_name and department.name == name:
                pass
            else:

                message = 'هذا العيادات موجود'

                return render(request, 'clinic/polyclinicDepartment.html', locals())

        department.arabic_name = arabic_name
        department.name = name
        department.save()

        return redirect('/polyclinicDepartment/')


@login_required
def deleteDepartment(request, department_id):
    """删除科室表"""

    department = Department.objects.get(id=department_id)
    department.delete()

    return redirect('/polyclinicDepartment/')


@login_required
def activeDepartment(request, department_id):
    """激活科室表"""

    department = Department.objects.get(id=department_id)
    department.status = True
    department.save()

    return redirect('/polyclinicDepartment/')


@login_required
def inactiveDepartment(request, department_id):
    """未激活科室表"""

    department = Department.objects.get(id=department_id)
    department.status = False
    department.save()

    return redirect('/polyclinicDepartment/')


@login_required
def polyclinicTimeForAdmin(request):
    """门诊排班表"""

    user = User.objects.get(account=request.session['account'])

    # today = datetime.date.today()  # 获取当前日期
    #
    # yesterday = today - datetime.timedelta(days=1)  # 获取前一天的日期

    departments = Department.objects.all()

    weeks = Week.objects.all()

    schedules = Schedule.objects.all().order_by('department__name')

    return render(request, 'clinic/polyclinicTimeForAdmin.html', locals())


@login_required
def addSchedule(request):
    """添加门诊排版"""

    user = User.objects.get(account=request.session['account'])

    schedules = Schedule.objects.all().order_by('department__name')

    departments = Department.objects.all()

    weeks = Week.objects.all()

    if request.method == 'POST':
        department_id = request.POST.get('department')
        week_id = request.POST.get('week')
        quantity = request.POST.get('quantity')
        start = request.POST.get('start')
        end = request.POST.get('end')
        time = request.POST.get('time')

        # 判断是否已存在这个排班
        if Schedule.objects.filter(department_id=department_id, week_id=week_id):

            message = 'هذا العيادات موجود'

            return render(request, 'clinic/polyclinicTimeForAdmin.html', locals())

        Schedule.objects.create(department_id=department_id, week_id=week_id, start=start,
                                quantity=quantity, end=end, time=time)

        # 更新对应科室的排班日期
        departmentObj = Department.objects.get(id=department_id)

        weekObj = Week.objects.get(id=week_id)

        if weekObj.name == 'saturday':
            departmentObj.saturday = True
            departmentObj.save()
        if weekObj.name == 'sunday':
            departmentObj.sunday = True
            departmentObj.save()
        if weekObj.name == 'monday':
            departmentObj.monday = True
            departmentObj.save()
        if weekObj.name == 'tuesday':
            departmentObj.tuesday = True
            departmentObj.save()
        if weekObj.name == 'wednesday':
            departmentObj.wednesday = True
            departmentObj.save()
        if weekObj.name == 'thursday':
            departmentObj.thursday = True
            departmentObj.save()

        return redirect('/polyclinicTimeForAdmin/')


@login_required
def editSchedule(request, schedule_id):
    """添加门诊排版"""

    schedules = Schedule.objects.all().order_by('department__name')

    departments = Department.objects.all()

    weeks = Week.objects.all()

    schedule = Schedule.objects.get(id=schedule_id)

    if request.method == 'POST':
        department_id = int(request.POST.get('department'))
        week_id = int(request.POST.get('week'))
        quantity = request.POST.get('quantity')
        start = request.POST.get('start')
        end = request.POST.get('end')
        time = request.POST.get('time')

        # 判断是否已存在这个排班
        exist = Schedule.objects.filter(department_id=department_id, week_id=week_id)
        # if schedule.department_id != department_id and schedule.week_id != week_id and exist:
        if exist:
            if schedule.department_id == department_id and schedule.week_id == week_id:
                pass
            else:

                message = 'هذا العيادات موجود'

                return render(request, 'clinic/polyclinicTimeForAdmin.html', locals())

        schedule.department_id = department_id
        schedule.week_id = week_id
        schedule.quantity = quantity
        schedule.start = start
        schedule.end = end
        schedule.time = time
        schedule.save()

        # 更新对应科室的排班日期
        departmentObj = Department.objects.get(id=department_id)

        weekObj = Week.objects.get(id=week_id)

        if weekObj.name == 'saturday':
            departmentObj.saturday = True
            departmentObj.save()
        if weekObj.name == 'sunday':
            departmentObj.sunday = True
            departmentObj.save()
        if weekObj.name == 'monday':
            departmentObj.monday = True
            departmentObj.save()
        if weekObj.name == 'tuesday':
            departmentObj.tuesday = True
            departmentObj.save()
        if weekObj.name == 'wednesday':
            departmentObj.wednesday = True
            departmentObj.save()
        if weekObj.name == 'thursday':
            departmentObj.thursday = True
            departmentObj.save()

        return redirect('/polyclinicTimeForAdmin/')


@login_required
def openSchedule(request, schedule_id):
    """开启排班"""

    schedule = Schedule.objects.get(id=schedule_id)
    schedule.status = True
    schedule.save()

    # 更新对应科室的排班日期
    departmentObj = schedule.department

    weekObj = schedule.week

    if weekObj.name == 'saturday':
        departmentObj.saturday = True
        departmentObj.save()
    if weekObj.name == 'sunday':
        departmentObj.sunday = True
        departmentObj.save()
    if weekObj.name == 'monday':
        departmentObj.monday = True
        departmentObj.save()
    if weekObj.name == 'tuesday':
        departmentObj.tuesday = True
        departmentObj.save()
    if weekObj.name == 'wednesday':
        departmentObj.wednesday = True
        departmentObj.save()
    if weekObj.name == 'thursday':
        departmentObj.thursday = True
        departmentObj.save()

    return redirect('/polyclinicTimeForAdmin/')


@login_required
def closeSchedule(request, schedule_id):
    """关闭排班"""

    schedule = Schedule.objects.get(id=schedule_id)
    schedule.status = False
    schedule.save()

    # 更新对应科室的排班日期
    departmentObj = schedule.department

    weekObj = schedule.week

    if weekObj.name == 'saturday':
        departmentObj.saturday = False
        departmentObj.save()
    if weekObj.name == 'sunday':
        departmentObj.sunday = False
        departmentObj.save()
    if weekObj.name == 'monday':
        departmentObj.monday = False
        departmentObj.save()
    if weekObj.name == 'tuesday':
        departmentObj.tuesday = False
        departmentObj.save()
    if weekObj.name == 'wednesday':
        departmentObj.wednesday = False
        departmentObj.save()
    if weekObj.name == 'thursday':
        departmentObj.thursday = False
        departmentObj.save()

    return redirect('/polyclinicTimeForAdmin/')


@login_required
def deleteSchedule(request, schedule_id):
    """删除门诊排版"""

    schedule = Schedule.objects.get(id=schedule_id)

    # 更新对应科室的排班日期
    departmentObj = schedule.department

    weekObj = schedule.week

    if weekObj.name == 'saturday':
        departmentObj.saturday = False
        departmentObj.save()
    if weekObj.name == 'sunday':
        departmentObj.sunday = False
        departmentObj.save()
    if weekObj.name == 'monday':
        departmentObj.monday = False
        departmentObj.save()
    if weekObj.name == 'tuesday':
        departmentObj.tuesday = False
        departmentObj.save()
    if weekObj.name == 'wednesday':
        departmentObj.wednesday = False
        departmentObj.save()
    if weekObj.name == 'thursday':
        departmentObj.thursday = False
        departmentObj.save()

    # 删除
    schedule.delete()

    return redirect('/polyclinicTimeForAdmin/')


@login_required
def reservationAdmin(request):
    """预定"""

    user = User.objects.get(account=request.session['account'])

    system = System.objects.first()

    if system:
        pass
    else:
        system = System.objects.create()

    start = system.start
    end = system.end

    today = datetime.date.today()
    # tomorrow = today + datetime.timedelta(days=1)
    now_time = datetime.datetime.now()  # 获取当前时间
    day_num = now_time.isoweekday()  # 当前天是这周的第几天

    # 明天的所有排班表
    if day_num == 7:
        schedules = Schedule.objects.filter(week__day_num=1, status=True)
    else:
        schedules = Schedule.objects.filter(week__day_num=day_num+1, status=True)

    basicInfos = BasicInfo.objects.filter(date=today)

    for schedule in schedules:
        schedule.count = basicInfos.filter(department=schedule.department.name).count()
        schedule.save()

    # 如果系统开着
    if system.status:
        # 当地时间从17:00到19:00进行预约
        if start <= now_time.hour <= end and day_num != 4:

            return render(request, 'clinic/reservationAdmin.html', locals())

        else:

            return redirect('/polyclinicTimeForAdmin/')
    else:

        return redirect('/notificationAdmin/')


@login_required
def newAppointmentAdmin(request):

    today = datetime.date.today()

    now_time = datetime.datetime.now()  # 获取当前时间
    day_num = now_time.isoweekday()  # 当前天是这周的第几天

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        department = request.POST.get('department')

        # 用户提交的部门对象
        if day_num == 7:
            schedules = Schedule.objects.filter(department__name=department, week__day_num=1)
        else:
            schedules = Schedule.objects.filter(department__name=department, week__day_num=day_num+1)

        # 已经预约的数量
        count = BasicInfo.objects.filter(department=department, date=today).count()

        if schedules:
            for schedule in schedules:

                if count < schedule.quantity:

                    # 判断当前病人在当天同一个部门是否预约两次
                    appointment = BasicInfo.objects.filter(name=name, age=age, department=department,
                                                           date=today).first()
                    if appointment:
                        # url = reverse('result', args=str(appointment.id))

                        # return redirect(url)
                        return redirect('/resultAdmin/' + str(appointment.id))
                    # 判断同一个用户设备是否预约两次
                    # mac = Mac.objects.filter(mac=mac, date=today)
                    #
                    # if mac:
                    #
                    #     return HttpResponse('يمكن للهاتف المحمول تحديد موعد مرة واحدة فقط في اليوم')

                    else:
                        # 当天当前科室的最后的预约
                        last = BasicInfo.objects.filter(department=department, date=today).order_by('order').last()

                        # 创建新的预约
                        appointmentObj = BasicInfo.objects.create(name=name, age=age, address=address,
                                                                  phone=phone, sex=sex, marriage=marriage,
                                                                  department=department,
                                                                  department_arabic=schedule.department.arabic_name)

                        if last:
                            # 预约顺序
                            appointmentObj.order = last.order + 1

                            # timeOfArrival[0:2]是上个病人到达时间的时钟数
                            tempHour = int(last.timeOfArrival[0:2])

                            # timeOfArrival[3:5]是上个病人到达时间的分钟数
                            tempMinute = int(last.timeOfArrival[5:7])

                            # 要到达医院的时间
                            tempMinute += schedule.time

                            if tempMinute >= 60:
                                tempMinute -= 60
                                tempHour += 1

                            if tempHour < 10:
                                tempHour = '0' + str(tempHour)
                            else:
                                tempHour = str(tempHour)

                            if tempMinute < 10:
                                tempMinute = '0' + str(tempMinute)
                            else:
                                tempMinute = str(tempMinute)

                            appointmentObj.timeOfArrival = tempHour + ' : ' + tempMinute

                            appointmentObj.save()

                            # url = reverse('result', args=str(appointmentObj.id))

                            # return redirect(url)
                            return redirect('/resultAdmin/' + str(appointmentObj.id))

                        else:
                            # 预约顺序
                            appointmentObj.order = 1

                            # departmentObj.start[0:2]门诊开始时间的时钟数
                            tempHour = schedule.start[0:2]

                            # departmentObj.start[3:5]门诊开始时间的分钟数
                            tempMinute = schedule.start[3:5]

                            # 要到达医院的时间
                            appointmentObj.timeOfArrival = tempHour + ' : ' + tempMinute

                            appointmentObj.save()

                            # url = reverse('result', args=str(appointmentObj.id))

                            # return redirect(url)
                            return redirect('/resultAdmin/' + str(appointmentObj.id))

                else:

                    message = 'نهاية !'

                    return render(request, 'clinic/reservationAdmin.html', locals())

        else:

            return HttpResponse('لا يوجد عيادة لهذا القسم')


@login_required
def resultAdmin(request, basic_id):

    user = User.objects.get(account=request.session['account'])

    appointment = BasicInfo.objects.get(id=basic_id)

    now_time = datetime.datetime.now()  # 获取当前时间
    day_num = now_time.isoweekday()  # 当前天是这周的第几天

    if day_num == 7:
        schedules = Schedule.objects.filter(week__day_num=1)
    else:
        schedules = Schedule.objects.filter(week__day_num=day_num+1)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # 预约日期
    date = tomorrow

    return render(request, 'clinic/resultAdmin.html', locals())


@login_required
def editAppointmentAdmin(request, basic_id):

    user = User.objects.get(account=request.session['account'])

    today = datetime.date.today()

    now_time = datetime.datetime.now()  # 获取当前时间
    day_num = now_time.isoweekday()  # 当前天是这周的第几天

    # 明天的所有排班表
    if day_num == 7:
        schedules = Schedule.objects.filter(week__day_num=1, status=True)
    else:
        schedules = Schedule.objects.filter(week__day_num=day_num + 1, status=True)

    basicInfos = BasicInfo.objects.filter(date=today)

    for schedule in schedules:
        schedule.count = basicInfos.filter(department=schedule.department.name).count()
        schedule.save()

    appointment = BasicInfo.objects.get(id=basic_id)

    if request.method == 'POST':

        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        sex = request.POST.get('sex')
        marriage = request.POST.get('marriage')
        department = request.POST.get('department')

        # 用户提交的部门对象
        if day_num == 7:
            scheduleObjs = Schedule.objects.filter(department__name=department, week__day_num=1)
        else:
            scheduleObjs = Schedule.objects.filter(department__name=department, week__day_num=day_num + 1)

        if scheduleObjs:
            for schedule in scheduleObjs:

                if appointment.department == department:  # 如果没有改变部门

                    appointment.name = name
                    appointment.age = age
                    appointment.address = address
                    appointment.phone = phone
                    appointment.sex = sex
                    appointment.marriage = marriage
                    appointment.save()

                    return redirect('/resultAdmin/' + str(appointment.id))

                else:  # 如果部门改变了
                    # 已经预约的数量
                    count = BasicInfo.objects.filter(department=department, date=today).count()

                    # 用户提交的部门对象
                    departmentObj = Department.objects.get(name=department)

                    if count < schedule.quantity:  # 当已经预约的数量小于可预约的数量时,

                        appointment_exist = BasicInfo.objects.filter(name=name, age=age, department=department,
                                                                     date=today).first()

                        if appointment_exist:  # 如果已经存在当前科室的预约，直接返回已存在的预约信息

                            # 删除这次的预约
                            appointment.delete()

                            return redirect('/resultAdmin/' + str(appointment_exist.id))

                        else:

                            # 当天当前科室的最后的预约
                            last = BasicInfo.objects.filter(department=department, date=today).order_by('order').last()

                            appointment.name = name
                            appointment.age = age
                            appointment.address = address
                            appointment.phone = phone
                            appointment.sex = sex
                            appointment.marriage = marriage
                            appointment.department = department
                            appointment.department_arabic = schedule.department.arabic_name
                            appointment.save()

                            if last:
                                # 预约顺序
                                appointment.order = last.order + 1

                                # timeOfArrival[0:2]是上个病人到达时间的时钟数
                                tempHour = int(last.timeOfArrival[0:2])

                                # timeOfArrival[3:5]是上个病人到达时间的分钟数
                                tempMinute = int(last.timeOfArrival[5:7])

                                # 要到达医院的时间
                                tempMinute += schedule.time

                                if tempMinute >= 60:
                                    tempMinute -= 60
                                    tempHour += 1

                                if tempHour < 10:
                                    tempHour = '0' + str(tempHour)
                                else:
                                    tempHour = str(tempHour)

                                if tempMinute < 10:
                                    tempMinute = '0' + str(tempMinute)
                                else:
                                    tempMinute = str(tempMinute)

                                appointment.timeOfArrival = tempHour + ' : ' + tempMinute

                                appointment.save()

                            else:
                                appointment.order = 1

                                # departmentObj.start[0:2]门诊开始时间的时钟数
                                tempHour = schedule.start[0:2]

                                # departmentObj.start[3:5]门诊开始时间的分钟数
                                tempMinute = schedule.start[3:5]

                                # 要到达医院的时间
                                appointment.timeOfArrival = tempHour + ' : ' + tempMinute

                                appointment.save()

                        return redirect('/resultAdmin/' + str(appointment.id))

                    else:  # 当已经预约的数量大于可预约的数量时， 不能预约

                        return HttpResponse('نهاية !')

    return render(request, 'clinic/editAppointmentAdmin.html', locals())


@login_required
def systemTime(request):
    """系统时间"""

    user = User.objects.get(account=request.session['account'])

    system = System.objects.first()

    if system:
        pass
    else:
        System.objects.create()
        system = System.objects.first()

    notifications = Notification.objects.all()

    return render(request, 'clinic/systemTime.html', locals())


@login_required
def openEditSystemTime(request, system_id):
    """开启编辑系统时间"""

    system = System.objects.get(id=system_id)
    system.isEdit = True
    system.save()

    return redirect('/systemTime/')


@login_required
def editSystemTime(request, system_id):
    """编辑系统时间"""

    system = System.objects.get(id=system_id)

    if request.method == 'POST':
        start = int(request.POST.get('start'))
        end = int(request.POST.get('end'))

        system.start = start
        system.end = end
        system.isEdit = False
        system.save()

        return redirect('/systemTime/')


@login_required
def openSystem(request, system_id):
    """开启系统"""

    system = System.objects.get(id=system_id)
    system.status = True
    system.save()

    return redirect('/systemTime/')


@login_required
def closeSystem(request, system_id):
    """关闭系统"""

    system = System.objects.get(id=system_id)
    system.status = False
    system.save()

    return redirect('/systemTime/')


@login_required
def notificationAdmin(request):

    user = User.objects.get(account=request.session['account'])
    notifications = Notification.objects.all()

    return render(request, 'clinic/notificationAdmin.html', locals())


@login_required
def addNotification(request):

    if request.method == "POST":  # 请求方法为POST时，进行处理

        title = request.POST.get('title')
        text = request.POST.get('text')

        # 创建通知
        Notification.objects.create(title=title, text=text)

        return redirect('/systemTime/')


@login_required
def editNotification(request, notification_id):

    notification = Notification.objects.get(id=notification_id)

    if request.method == "POST":  # 请求方法为POST时，进行处理

        title = request.POST.get('title')
        text = request.POST.get('text')

        # 更新通知
        notification.title = title
        notification.text = text
        notification.save()

        return redirect('/systemTime/')


@login_required
def deleteNotification(request, notification_id):
    """删除通知"""

    notification = Notification.objects.get(id=notification_id)
    notification.delete()

    return redirect('/systemTime/')


@login_required
def excel(request):

    user = User.objects.get(account=request.session['account'])

    today = datetime.date.today()  # 获取当前日期

    yesterday = today - datetime.timedelta(days=1)  # 获取前一天的日期

    today = datetime.date.today()
    now_time = datetime.datetime.now()  # 获取当前时间
    day_num = now_time.isoweekday()  # 当前天是这周的第几天

    # 今天的所有排班表
    # if day_num == 7:
    #     schedules = Schedule.objects.filter(week__day_num=1, status=True)
    # else:
    schedules = Schedule.objects.filter(week__day_num=day_num, status=True)

    return render(request, 'clinic/excel.html', locals())


@login_required
def toExcel(request):
    """导出excel文件"""

    today = datetime.date.today()  # 获取当前日期

    yesterday = today - datetime.timedelta(days=1)  # 获取前一天的日期

    basicInfo = BasicInfo.objects.filter(date=yesterday)

    if basicInfo:
        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf8')

        # 添加第一页数据表
        ws = wb.add_sheet(u"appointment")

        # 写入表头
        ws.write(0, 0, u'Name')
        ws.write(0, 1, u'Age')
        ws.write(0, 2, u'Sex')
        ws.write(0, 3, u'Marriage')
        ws.write(0, 4, u'Address')
        ws.write(0, 5, u'Phone')
        ws.write(0, 6, u'Department')
        ws.write(0, 7, u'Date')
        ws.write(0, 8, u'Arabic')
        ws.write(0, 9, u'Order')
        ws.write(0, 10, u'TimeOfArrival')

        # 写入每一行对应的数据
        excel_row = 1
        for info in basicInfo:
            ws.write(excel_row, 0, info.name)
            ws.write(excel_row, 1, info.age)
            ws.write(excel_row, 2, info.sex)
            ws.write(excel_row, 3, info.marriage)
            ws.write(excel_row, 4, info.address)
            ws.write(excel_row, 5, info.phone)
            ws.write(excel_row, 6, info.department)
            ws.write(excel_row, 7, info.date.strftime("%Y-%m-%d"))
            ws.write(excel_row, 8, info.department_arabic)
            ws.write(excel_row, 9, info.order)
            ws.write(excel_row, 10, info.timeOfArrival)

            excel_row += 1

        # 实现下载
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)

        response = StreamingHttpResponse(output)
        response['content_type'] = 'application/vnd.ms-excel'
        response['charset'] = 'utf-8'
        response['Content-Disposition'] = 'attachment; filename="{0}.xls"'.format(
            timezone.datetime.now().strftime('%Y%m%d%H%M'))

        return response

    else:
        return HttpResponse('There are no products !')
