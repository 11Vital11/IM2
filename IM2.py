from random import random
import math
import matplotlib.pyplot as plt
import glob
import moviepy.editor as mpy
import pandas as pd


def path_searching():
    import os
    path = os.path.abspath(__file__)
    path = path.split('\\')
    path.remove(path[-1])
    path.append('')
    return '/'.join(path)


def update_df(position):
    df.loc[position] = lines_burden
    time_for_changing_of_n.append(round(t))
    return position + 1


N = 10  # число экспериментов
t_0 = 0   # начальнео время
t_end = 100   # конечное время
t = t_0
t_enter = 0  # время прихода
clients_number = 0    # количесвто клиентов
total_lines_member = 15  # верхнее ограничение на количество людей в очередях

lines_number = []
av_total_cost = []  # средние затраты за отказ за  все эксперименты
av_salary_cost = []   # средние затраты на зарплату за все эксперименты
av_ren = []   # среднее число отказов за все эксперименты




for lines in range(1, 10):  # идём по количеству линий
    total_cost = []
    ren = []
    salary_cost = []
    for j in range(N):
        lines_burden = [0 for i in range(lines)]   # нагрузка на линии
        service_time = [0 for i in range(lines)]   # время конца обслуживания заказа на линии
        t = t_0
        t_enter = 0
        clients_number = 0   # общее число клиентво
        total_line_work = [0 for i in range(lines)]   # общее число людей, обслуженых ан линии
        renouncement = 0  # отказы за один эксперимент
        while t < t_end:
            t += 0.05   # изменение модельного времени
            if t_enter <= t:   # время входа следующего клиента
                t_enter += -math.log(random())/1
                clients_number += 1
                if sum(lines_burden) <= total_lines_member:   # условие того, что количесвто людей в очередях меньше предельного значения
                    i_0 = lines_burden.index(min(lines_burden))
                    lines_burden[i_0] += 1
                else:
                    renouncement += 1
            for i in range(lines):   # идём по всем линиям
                if service_time[i] <= t and lines_burden[i] > 0:   # условие того, что обслуживание на линии i окончено и нагрузка на этой линии не равна 0,
                                                                    # то есть касса обслужила одного клиента
                    lines_burden[i] -= 1
                    total_line_work[i] += 1
                    service_time[i] = t - math.log(random()) * 4.5
                    i_0 = lines_burden.index(max(lines_burden))
                    if lines_burden[i_0] > lines_burden[i] + 1:   # условие перемещение человека из максимальной очереди в очередь i
                        lines_burden[i_0] -= 1
                        lines_burden[i] += 1
        while sum(lines_burden) != 0:  # обслуживание клиентов после окончания времени(новые клиенты не поступают)
            t += 0.05
            for i in range(lines):
                if service_time[i] <= t and lines_burden[i] > 0:
                    lines_burden[i] -= 1
                    total_line_work[i] += 1
                    service_time[i] = t - math.log(random()) * 4.5
                    i_0 = lines_burden.index(max(lines_burden))
                    if lines_burden[i_0] > lines_burden[i] + 1:
                        lines_burden[i_0] -= 1
                        lines_burden[i] += 1
        y = sum([(1 + lines - i) * total_line_work[i] for i in range(lines)])   # затраты за отказ(пропорциональны количеству людей, которых обслужила касса)
                                                                                # за один эксперимент(чем больше номер линии, тем меньше зарплата
        total_cost.append(y + 10 * renouncement)   # общий штраф(и за отказ и на зарплату)
        salary_cost.append(y)
        ren.append(renouncement)
    av_salary_cost.append(sum(salary_cost)/N)  # среднее число штрафов на зарплату  по всем эксперимента для фиксированного числа линий
    av_total_cost.append(sum(total_cost)/N)    # среднее число штрафов за отказ  по всем эксперимента для фиксированного числа линий
    av_ren.append(sum(ren)/N)   # среднее число отказов  по всем эксперимента для фиксированного числа линий
    lines_number.append(lines)
    print("Количество линий", lines, "Штраф", sum(total_cost)/N, "Среднее число отказов", sum(ren)/N, "Средние затраты на зарпалту", sum(salary_cost)/N)

opt = lines_number[av_total_cost.index(min(av_total_cost))]   # оптимальное количество линий

print("Оптимальное количество линий", opt,
      "соответствующий штраф", min(av_total_cost),
      "Количество отказов", math.floor(av_ren[av_total_cost.index(min(av_total_cost))]),
      "Суммарные затраты на зарплату", av_salary_cost[av_total_cost.index(min(av_total_cost))])


df = pd.DataFrame(data=[[0 for i in range(opt)]], columns=[f'{i + 1}' for i in range(opt)])
system_state_index = 0
time_for_changing_of_n = []

for lines in range(opt, opt + 1):  # прогон оптимального количесвта линий
    lines_burden = [0 for i in range(lines)]   # нагрузка на линии
    system_state_index = update_df(system_state_index)
    service_time = [0 for i in range(lines)]   # время конца обслуживания заказа на линии
    t = t_0
    t_enter = 0
    clients_number = 0   # общее число клиентво
    total_line_work = [0 for i in range(lines)]   # общее число людей, обслуженых ан линии
    while t < t_end:
        t += 0.05   # изменение модельного времени
        if t_enter <= t:   # время входа следующего клиента
            t_enter += -math.log(random())/1
            clients_number += 1
            if sum(lines_burden) <= total_lines_member:   # условие того, что количесвто людей в очередях меньше предельного значения
                i_0 = lines_burden.index(min(lines_burden))
                lines_burden[i_0] += 1
                system_state_index = update_df(system_state_index)
        for i in range(lines):   # идём по всем линиям
            if service_time[i] <= t and lines_burden[i] > 0:   # условие того, что обслуживание на линии i окончено и нагрузка на этой линии не равна 0,
                                                                # то есть касса обслужила одного клиента
                lines_burden[i] -= 1
                system_state_index = update_df(system_state_index)
                total_line_work[i] += 1
                service_time[i] = t - math.log(random()) * 4.5
                i_0 = lines_burden.index(max(lines_burden))
                if lines_burden[i_0] > lines_burden[i] + 1:   # условие перемещение человека из максимальной очереди в очередь i
                    lines_burden[i_0] -= 1
                    lines_burden[i] += 1
                    system_state_index = update_df(system_state_index)
    while sum(lines_burden) != 0:  # обслуживание клиентов после окончания времени(новые клиенты не поступают)
        t += 0.05
        for i in range(lines):
            if service_time[i] <= t and lines_burden[i] > 0:
                lines_burden[i] -= 1
                system_state_index = update_df(system_state_index)
                total_line_work[i] += 1
                service_time[i] = t - math.log(random()) * 4.5
                i_0 = lines_burden.index(max(lines_burden))
                if lines_burden[i_0] > lines_burden[i] + 1:
                    lines_burden[i_0] -= 1
                    lines_burden[i] += 1
                    system_state_index = update_df(system_state_index)




df['time'] = time_for_changing_of_n
df = df.set_index('time')
plt.style.use('fivethirtyeight')
length = len(df.index)
path_of_project = path_searching()  # ищет путь к файлу
for i in range(2, length):  # начиная со 2ой строчки до df
    print(length)
    print(i)
    ax = df.iloc[i-1:i].plot.bar(figsize=(12, 12), linewidth=5, color=['k', 'r', 'g', 'b', 'c', '#B88BAC', '#827498'])
    ax.set_ylim(0, 10)
    ax.set_xlabel('Lines')
    ax.set_ylabel('Clients')
    ax.set_title("Modeling of the bank process", fontsize=18)
    ax.legend(loc='upper left', frameon=False)
    ax.grid(axis='x')
    fig = ax.get_figure()
    fig.savefig(path_of_project+f"png2/{1000+i}.png")

gif_name = f'bank_process.gif'
fps = 240
file_list = glob.glob(path_of_project+"png2/*.png")
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif(path_of_project+"{}.gif".format(gif_name), fps=fps)






