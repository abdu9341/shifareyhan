from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from patient.models import BasicInfo
from user.models import User
from clinic.models import *
from datetime import datetime as time
import datetime


def polyclinicTimeForPatient(request):
    """门诊排班表"""

    system = System.objects.first()

    if system:
        pass
    else:
        system = System.objects.create()

    # today = datetime.date.today()  # 获取当前日期
    #
    # yesterday = today - datetime.timedelta(days=1)  # 获取前一天的日期

    # schedules = Schedule.objects.filter(status=True).order_by('-department__name')

    departments = Department.objects.filter(status=True).order_by('id')

    weeks = Week.objects.all()

    # 如果系统开着
    if system.status:

        return render(request, 'patient/polyclinicTimeForPatient.html', locals())

    else:

        return redirect('/notification/')


def reservation(request):
    """预定"""

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
        if start <= now_time.hour <= end and (day_num == 3 or day_num == 4):

            return render(request, 'patient/reservation.html', locals())

        else:

            return redirect('/polyclinicTimeForPatient/')
    else:

        return redirect('/notification/')


def newAppointment(request):
    today = datetime.date.today()

    now_time = datetime.datetime.now()  # 获取当前时间
    day_num = now_time.isoweekday()  # 当前天是这周的第几天

    if request.method == 'POST':
        name = request.POST.get('name')
        husband = request.POST.get('husband')
        age = request.POST.get('age')
        # address = request.POST.get('address')
        phone = request.POST.get('phone')
        # sex = request.POST.get('sex')
        # marriage = request.POST.get('marriage')
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
                        return redirect('/result/' + str(appointment.id))
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
                        appointmentObj = BasicInfo.objects.create(name=name, age=age, husband=husband,
                                                                  phone=phone, department=department,
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
                            return redirect('/result/' + str(appointmentObj.id))

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
                            return redirect('/result/' + str(appointmentObj.id))

                else:

                    message = 'نهاية !'

                    return render(request, 'patient/reservation.html', locals())

        else:

            return HttpResponse('لا يوجد عيادة لهذا القسم')


def result(request, basic_id):
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

    return render(request, 'patient/result.html', locals())


def editAppointment(request, basic_id):

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

                    return redirect('/result/' + str(appointment.id))

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

                            return redirect('/result/' + str(appointment_exist.id))

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

                        return redirect('/result/' + str(appointment.id))

                    else:  # 当已经预约的数量大于可预约的数量时， 不能预约

                        return HttpResponse('نهاية !')

    return render(request, 'patient/editAppointment.html', locals())


def notification(request):

    notifications = Notification.objects.all()

    return render(request, 'patient/notification.html', locals())
