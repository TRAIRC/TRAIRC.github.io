import sys
import os
import time
import re

headline = ['#','##','###','####','#####','######']
title_sign_list = []
"""用于判断标题产生环境"""
titles_added_number = []
"""保存嵌入了编号的标题，用于产生新编号"""
is_continue = 'n'
suf = '.'

"""给某一行添加编号"""
def add_number_for_line(line_which_is_title,title_sign):
    global suf
    global is_continue
    global title_sign_list
    global titles_added_number
    title_sign_list.append(title_sign)
    if len(title_sign_list) == 1:#如果line_which_is_title是第一个标题
        titles_added_number.append(line_which_is_title.replace(title_sign + ' ',title_sign + ' 1. '))
        return titles_added_number[0]
    else:
        #当标题级别为一级(需要标号为1.,2.,3.,...)
        for title in titles_added_number[::-1]:
            number = title.lstrip().split(' ')[1]
            sign = title.lstrip().split(' ')[0]
            if len(number) == 2 and number.count('.') == 1:#如果发现一级标题(序号为1.,2.,3.,...)
                if len(title_sign) == len(sign):#如果line_which_is_title是一级标题（与发现的一级标题title级别相同）
                    titles_added_number.append(
                        line_which_is_title.replace(title_sign + ' ',title_sign + ' ' + str(int(number[:-1]) + 1) + '. '))
                    return titles_added_number[-1]
                elif len(title_sign) < len(sign):#如果line_which_is_title是一级标题（比发现的第一个一级标题级别更高）
                    if is_continue != 'y':
                        print('Markdown文件中的：\n' + title.strip() + '或\n' + line_which_is_title + "\n不规范\n建议将Markdown文件中的标题分级、规范地写好后再继续")
                        is_continue = input('是否忽略此类警告并继续？（y/n）')
                    if is_continue.strip().lower() == 'y':
                        titles_added_number.append(line_which_is_title.replace(title_sign + ' ',title_sign + ' ' + str(int(number[:-1]) + 1) + '. '))
                        return titles_added_number[-1]
                    elif is_continue.strip().lower() == 'n':
                        os._exit(0)
                    else:
                        print('接收到y/n以外的输入，默认退出')
                        os._exit(0)
                else:
                    break
        #当标题级别不是一级(序号不是1.,2.,3.,...)
        number = titles_added_number[-1].lstrip().split(' ')[1]
        if len(number) == 2 and number.count('.') == 1:#如果line_which_is_title的上一级标题为一级标题(序号为1.,2.,3.,...)
            titles_added_number.append(
                line_which_is_title.replace(
                    title_sign + ' ',title_sign + ' ' + number + '1' + suf + ' '))
            return titles_added_number[-1]
        elif len(title_sign_list[-1]) > len(title_sign_list[-2]):#如果line_which_is_title的上一个标题比它更高
            number = re.search('(.*\.\d+)[^\d]?$', number).group(1)
            titles_added_number.append(
                line_which_is_title.replace(
                    title_sign + ' ',title_sign + ' ' + number + '.1' + suf + ' '))
            return titles_added_number[-1]
        elif len(title_sign_list[-1]) == len(title_sign_list[-2]):#如果line_which_is_title与上一个标题等级别
            number_suf = re.search('(.*\.)(\d+)[^\d]?$', number).group(2)
            number_pre = re.search('(.*\.)(\d+)[^\d]?$', number).group(1)
            titles_added_number.append(
                line_which_is_title.replace(
                    title_sign + ' ',title_sign + ' ' + number_pre + str(int(number_suf) + 1) + suf + ' '))
            return titles_added_number[-1]
        elif len(title_sign_list[-1]) < len(title_sign_list[-2]):#如果line_which_is_title的上一个标题比它更低
            for title in titles_added_number[::-1]:
                number = title.lstrip().split(' ')[1]
                sign = title.lstrip().split(' ')[0]
                if len(number) == 2 and number.count('.') == 1:#如果先发现一级标题
                    if is_continue != 'y':
                        print('Markdown文件中的：\n' + title.strip() + '\n或\n' + line_which_is_title + "\n不规范\n建议将Markdown文件中的标题分级、规范地写好后再继续")
                        is_continue = input('是否忽略此类警告并继续？（y/n）')
                    if is_continue.strip() == 'y':
                        titles_added_number.append(line_which_is_title.replace(title_sign + ' ',title_sign + ' ' + str(int(number[:-1]) + 1) + '. '))
                        return titles_added_number[-1]
                    elif is_continue.strip() == 'n':
                        os._exit(0)
                    else:
                        print('接收到y/n以外的输入，默认退出')
                        os._exit(0)
                if len(sign) == len(title_sign):#如果找到等级别标题
                    number_suf = re.search('(.*\.)(\d+)[^\d]?$', number).group(2)
                    number_pre = re.search('(.*\.)(\d+)[^\d]?$', number).group(1)
                    titles_added_number.append(
                        line_which_is_title.replace(
                            title_sign + ' ',title_sign + ' ' + number_pre + str(int(number_suf) + 1) + suf + ' '))
                    return titles_added_number[-1]


"""给传入内容添加编号"""
def create_lines_with_number(lines_in_file):
    for i in range(len(lines_in_file)):
        title_sign = lines_in_file[i].lstrip().split(' ')
        if title_sign[0] in headline:
            lines_in_file[i] = add_number_for_line(lines_in_file[i],title_sign[0])
    return lines_in_file


"""生成添加了标题编号的文件"""
def create_markdown_file_with_number(f,file_name):
    lines_in_file = []
    lines_in_file_with_number = []
    lines_in_file = f.readlines()
    f.close()
    lines_in_file_with_number = create_lines_with_number(lines_in_file)
    # 根据原文件名生成标题添加了序号的文件的文件名
    markdown_file_with_number = os.getcwd() + '\\' + file_name[::-1].split('.',1)[1][::-1] + '_withNum.md'
    if not os.path.exists(markdown_file_with_number):
        with open(markdown_file_with_number, 'w+',encoding='utf-8') as f:
            for line in lines_in_file_with_number:
                f.write(line)
            print('文件已生成')
    else:
        print('文件名重复，请修改文件'+ markdown_file_with_number +'的文件名后重试')
import sys
import os
import time

headline = ['#','##','###','####','#####','######']
lines_in_file = []

"""生成目录列表中的某一项"""
def creat_directory_line(line,headline_mark,i):
    if headline_mark == '#':
        return '<a href="#' + str(i) + '">' + line[2:-1] + "</a>  \n"
    elif headline_mark == '##':
        #&emsp;为Markdown中的一种缩进，这里不直接用空格作为缩进是因为多个空格一起出现可能会生成代码块，引发歧义
        return '&emsp;<a href="#' + str(i) + '">' + line[3:-1] + "</a>  \n"
    elif headline_mark == '###':
        return '&emsp;&emsp;<a href="#' + str(i) + '">' + line[4:-1] + "</a>  \n"
    elif headline_mark == '####':
        return '&emsp;&emsp;&emsp;<a href="#' + str(i) + '">' + line[5:-1] + "</a>  \n"
    elif headline_mark == '#####':
        return '&emsp;&emsp;&emsp;&emsp;<a href="#' + str(i) + '">' + line[6:-1] + "</a>  \n"
    elif headline_mark == '######':
        return '&emsp;&emsp;&emsp;&emsp;&emsp;<a href="#' + str(i) + '">' + line[7:-1] + "</a>  \n"

"""生成目录列表"""
def creat_directory(f):
    i = 0
    directory = []
    directory.append('<a name="index">**Index**</a>\n')
    for line in f:
        lines_in_file.append(line)
    f.close()
    length = len(lines_in_file)
    for j in range(length):
        splitedline = lines_in_file[j].lstrip().split(' ')
        if splitedline[0] in headline:
            #如果为最后一行且末尾无换行（防最后一个字被去除）
            if j == length - 1 and lines_in_file[j][-1] != '\n':
                directory.append(creat_directory_line(lines_in_file[j] + '\n',splitedline[0],i) + '\n')
                lines_in_file[j] = lines_in_file[j].replace(splitedline[0] + ' ',splitedline[0] + ' ' + '<a name="' + str(i) + '">')[:] + '</a><a style="float:right;text-decoration:none;" href="#index">[Top]</a>' + "\n"
                i = i + 1
            else:
                directory.append(creat_directory_line(lines_in_file[j],splitedline[0],i))
                lines_in_file[j] = lines_in_file[j].replace(splitedline[0] + ' ',splitedline[0] + ' ' + '<a name="' + str(i) + '">')[:-1] + '</a><a style="float:right;text-decoration:none;" href="#index">[Top]</a>' + "\n"
                i = i + 1
    return directory

"""以目录列表为参数生成添加目录的文件"""
def creat_file_with_toc(f,file_name):
    directory = creat_directory(f)
    lines_in_file = []
    lines_in_file_with_number = []
    f=open(file_name,'r',encoding='utf-8')
    lines_in_file = f.readlines()
    #print(lines_in_file)
    f.close()
    lines_in_file_with_number = create_lines_with_number(lines_in_file)
    # 根据原文件名生成标题添加了序号的文件的文件名
    markdown_file_with_number = os.getcwd() + '\\' + file_name[::-1].split('.', 1)[1][::-1] + '_withNum.md'
    if not os.path.exists(markdown_file_with_number):
        with open(markdown_file_with_number, 'w+',encoding='utf-8') as f:
            for directory_line in directory:
                f.write(directory_line)
            for line in lines_in_file_with_number:
               # print(line)
                f.write(line)
            print('文件已生成')
    else:
        print('文件名重复，请修改文件'+'file_with_toc.md'+'的文件名后重试')

if __name__=='__main__':
    file_name = ''
    #如果未传入文件名
    if len(sys.argv) < 2:
        path = os.getcwd()
        file_and_dir = os.listdir(path)
        md_file = []
        for item in file_and_dir:
            if item.split('.')[-1].lower() in ['md','mdown','markdown'] and os.path.isfile(item):
                md_file.append(item)
        if len(md_file) != 0:
            print('当前目录下的Markdown文件：')
            for file in md_file:
                print(file)
            file_name = input('请输入文件名(含后缀)\n')
        else:
            print('该目录下无Markdown文件，即将退出...')
            time.sleep(2)
            os._exit(0)
    else:
        file_name = sys.argv[1]
    if os.path.exists(file_name) and os.path.isfile(file_name):
        with open(file_name,'r',encoding='utf-8') as f:
            creat_file_with_toc(f,file_name)

    else:
        msg = "未找到文件"
        print(msg)