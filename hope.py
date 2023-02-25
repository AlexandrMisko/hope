from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from HTMLTable import HTMLTable
import yagmail

web = Firefox()
web.get("https://cas.s.zzu.edu.cn/cas/login?service=https%3A%2F%2Fjw.v.zzu.edu.cn%2Feams%2Fsso%2Flogin.action%3FtargetUrl%3Dbase64aHR0cHM6Ly9qdy52Lnp6dS5lZHUuY24vZWFtcy9ob21lLmFjdGlvbg%3D%3D")
time.sleep(10)
# 输入账号
web.find_element(By.ID, "username").send_keys("201984110313", Keys.ENTER)
# 输入密码
web.find_element(By.ID, "password").send_keys("Szxad96!", Keys.ENTER)
time.sleep(10)
# 点击我的成绩
web.find_element(By.CSS_SELECTOR, '.expand > ul:nth-child(2) > div:nth-child(1) > li:nth-child(19) > a:nth-child(1)').click()
time.sleep(5)
# 点击所有学期成绩
web.find_element(By.CLASS_NAME, 'toolbar-item-ge0').click()
time.sleep(5)
el = web.find_element(By.XPATH, '/html/body/table/tbody/tr/td[3]/div/div/div[3]/div[3]/table/tbody/tr[63]').text
el = el.split(' ')
add = el.pop(0)
el[0] = add + ' ' + el[0]
el.insert(6, ' ')

table_name = "该死的电力工程"
table = HTMLTable(caption=table_name)

# 设置标题
table.append_header_rows((('学年学期', '课程代码', '课程序号', '课程名称', '课程类别', '学分', '期末成绩', '补考成绩', '总评成绩', '最终', '绩点'),))
# 设置数据
table.append_data_rows((tuple(el),))
# 标题样式
caption_style = {
    'text-align': 'center',
    'cursor': 'pointer'
}
table.caption.set_style(caption_style)
# 设置边框
border_style = {
    'border-color': '#000',
    'border-width': '1px',
    'border-style': 'solid',
    'border-collapse': 'collapse',
    # 同时设置了表格居中
    'margin': 'auto',
}
table.set_style(border_style)
# 单元格边框
table.set_cell_style(border_style)
# 设置单元格样式
cell_style = {
        'text-align': 'center',
        'padding': '4px',
        'background-color': '#ffffff',
        'font-size': '0.95em',
    }
table.set_cell_style(cell_style)
# 表头样式
header_cell_style = {
    'text-align': 'center',
    'padding': '4px',
    'background-color': 'coral',
    'color': '#FFFFFF',
    'font-size': '0.95em',
    }
table.set_header_cell_style(header_cell_style)
# 如果成绩小于60则标红
for row in table.iter_data_rows():
    for i in range(6, 10):
        try:
            if int(row[i].value) < 60:
                row[i].set_style({
                    'background-color': '#ffdddd',
                })
        except Exception as e:
            print(e)

html = table.to_html()
print(html)
yag = yagmail.SMTP(user='1586924294@qq.com', password='xrpalckormpjjijh', host='smtp.qq.com')
yag.send(to='1586924294@qq.com', subject='成绩提醒！', contents=html)
