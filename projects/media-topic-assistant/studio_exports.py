import csv
import io


def markdown(artifact):
    data = artifact['data']
    if 'markdown' in data:
        body = data['markdown']
    elif 'candidates' in data:
        body = '\n\n'.join(f'## 方向 {i + 1}\n' + '\n'.join(f'- {k}：{v}' for k, v in c.items()) for i, c in enumerate(data['candidates']))
    else:
        body = '# 标题候选\n' + '\n'.join(f'- {t}' for t in data['titles'])
        body += f'\n\n## 封面\n{data["cover"]}\n\n## 引入\n{data["intro"]}'
        for i, s in enumerate(data['sections']):
            body += f'\n\n## {i + 1}. {s["heading"]}\n{s["text"]}\n\n画面：{s["visual"]}\n\n时长：{s["seconds"]} 秒\n\n字幕：{s["subtitle"]}\n\n转场：{s["transition"]}'
        body += f'\n\n## 结尾\n{data["closing"]}\n\n## 发布正文\n{data["publish_text"]}'
    if data.get('missing'):
        body += '\n\n## 待补素材与待验证信息\n' + '\n'.join('- ' + item for item in data['missing'])
    return body + f'\n\n---\n版本 {artifact["version"]} · {artifact["created_at"]}\n'


def csv_text(headers, rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream)
    writer.writerow(headers)
    for row in rows:
        # Do not allow pasted user/model strings to become spreadsheet formulas.
        writer.writerow([("'" + str(x)) if isinstance(x, str) and x.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else x for x in row])
    return '\ufeff' + stream.getvalue()


def storyboard(artifact):
    return csv_text(['序号', '段落', '正文或台词', '画面或操作', '秒数', '字幕', '转场'],
                    [[i + 1, s['heading'], s['text'], s['visual'], s['seconds'], s['subtitle'], s['transition']] for i, s in enumerate(artifact['data']['sections'])])


def task_csv(tasks):
    return csv_text(['任务', '完成', '日期', '预计小时', '实际小时'], [[t['title'], '是' if t['done'] else '否', t['due_date'], t['estimated_hours'], t['actual_hours']] for t in tasks])
