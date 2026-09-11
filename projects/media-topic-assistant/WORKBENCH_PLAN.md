# 创作工作台实施记录

用户已批准：单人本地网页，八助手，图文与口播/录屏/生活记录/混合视频，手动制作发布。完整交付三批功能。

## 实施与验收
- [x] 数据迁移、账号版本、素材、作品与稿件版本；保留旧选题入口。
- [x] 定位候选、策划、五种形式稿件、局部修改、包装、案例、SOP和复盘。
- [x] 六入口网页、编辑与导出、图片附件、排期与发布登记。
- [x] API回归、旧浏览器回归、新工作台浏览器流程、文档和复核。

最终验证（2026-09-11）：项目虚拟环境 pytest 71 passed；系统 Python 执行原 browser_check.py 和 studio_browser_check.py 均通过；代码差异空白检查通过。浏览器使用临时库和模拟模型，包含网络响应丢失重试、段落未保存输入保留、双作品发布隔离、最近定位候选和首页进度同步。

人工质量验收见 STUDIO_ACCEPTANCE.md；未调用真实模型。旧服务自动停止并重启被执行策略拦截，未执行实际个人数据库迁移；用户关闭旧服务并重新运行 start.cmd 后会自动备份升级。

Ruling: 在用户现有目录内仅修改 media-topic-assistant，便于双击原启动器使用；保留所有学习资料改动，不提交或推送。
Ruling: 所有新接口位于 /api/studio；旧 /api/* 保留。根页面新工作台，/topics 旧选题页面。

## 前后端契约（日期时间以 ISO 文本，日期 YYYY-MM-DD）
GET /api/studio/bootstrap => {profile,profile_versions,materials,works,reviews,weekly,templates}
profile={原Profile字段,goal,voice,boundaries,columns:string[],content_forms:string[],on_camera,weekly_hours,interview,confirmed,version,id,created_at}；weights是可配置方向到百分比的映射。
PUT /api/studio/profile 接受完整可编辑profile（不传id/version/created_at），保存新版本。
POST /api/studio/positioning {interview,request_id} => artifact（data.candidates有三个候选，每个字段 positioning,audience,pillars:string[],difference,voice,boundaries,columns:string[],tradeoff）。返回的候选仅建议，采用需PUT profile。
GET /api/studio/positioning => 已保存的定位候选artifact列表。
POST /api/studio/materials {title,kind:'亲身经历'|'外部参考'|'待验证想法',text,url:'',verification:'未核实'|'有参考来源，待核实'|'用户已亲测',missing:string[]} => material。
PUT /api/studio/materials/{id} 同上。GET /api/studio/materials => 列表。
POST /api/studio/materials/{id}/image 原始PNG/JPEG/WebP字节，Content-Type正确 => material（images:[{id,url,name}]）。图片仅保存预览，不发AI。
POST /api/studio/materials/{id}/analyze {request_id} => artifact（data.markdown和data.missing），GET材料响应带analyses列表。
POST /api/studio/works {title,topic_id:null,material_ids:[],request_id} => work。
GET /api/studio/works => 列表；GET /api/studio/works/{id} => work；PUT /api/studio/works/{id} {title,material_ids} => work。
work={id,title,topic_id,profile_snapshot,material_ids,created_at,updated_at,artifacts:[],variants:[],tasks:[]}。
variant={id,form:'图文'|'口播'|'录屏教程'|'生活记录'|'混合视频',platform,status,created_at,artifacts:[],publications:[]}。
POST /api/studio/works/{id}/variants {form,platform,request_id} => variant。
PATCH /api/studio/variants/{id} {status,platform} => variant，status为待策划/待补素材/写稿中/待制作/待发布/已发布/已复盘/暂停/放弃。
POST /api/studio/works/{id}/generate {kind:'brief'|'draft'|'revise'|'package'|'review',variant_id:null,source_id:null,instruction:'',section_index:null,page_count:6,duration_seconds:180,template:'',request_id} => artifact。
draft需要variant_id；revise需要source_id与section_index，只改对应section；package需要variant_id及source_id；review需要variant_id已有发布数据。
artifact={id,kind,work_id,variant_id,version,created_at,confirmed,data,context}。
data（brief/package/review/case/period_review）={markdown:string,missing:string[]}。
data（draft/revise）={titles:[3条],cover:string,intro:string,sections:[{heading,text,visual,seconds:number,subtitle,transition}],closing:string,publish_text:string,missing:string[]}。
POST /api/studio/works/{id}/artifacts {kind:'brief'|'draft'|'package'|'review',variant_id:null,source_id:null,data,request_id} 保存新人工版本，返回artifact。手动稿件允许markdown结构{markdown,missing:[]}或完整sections结构。
PATCH /api/studio/artifacts/{id} {confirmed:boolean}；确认版本不可覆盖，所有修改新建版本。
GET /api/studio/artifacts/{id}/export?format=md|csv => 下载文本（csv只支持分镜sections）。
POST /api/studio/works/{id}/sop {variant_id,request_id} => task[]，自动生成一次模板任务，再次调用返回已有。
PATCH /api/studio/tasks/{id} {done,due_date,estimated_hours,actual_hours} => task。
task={id,work_id,variant_id,title,done,due_date,estimated_hours,actual_hours}。
POST /api/studio/schedule {week_start:'YYYY-MM-DD'} => weekly，把未完成未排期任务按预算排入该周，超预算不排期。
GET /api/studio/weekly?week_start=... => {week_start,budget_hours,planned_hours,actual_hours,tasks:[],unscheduled:[]}。
GET /api/studio/works/{id}/tasks/export => CSV下载。
POST /api/studio/variants/{id}/publications {platform,published_at:'YYYY-MM-DD',observation_days:7,url:'',metrics:{views:null,likes:null,comments:null,saves:null,completion_rate:null},comments_text:'',reflection:'',actual_hours:null,request_id} => publication。
PUT /api/studio/publications/{id} 同上用于更新，request_id可省略。
GET /api/studio/reviews => review和period_review artifacts。
POST /api/studio/reviews/period {start_date,end_date,request_id} => artifact，以发布日范围按平台+形式+观察天数分组比较。
POST /api/studio/reviews/{id}/ideas {title,request_id} => 旧topic（显式采纳为待验证选题）。
所有生成请求幂等：同request_id相同body返回首次结果，不同body为409；失败不保存成功记录、不清空已有稿。资料快照保留，网页生成前先保存人工编辑。

## 质量默认
- 无密钥可手动完成编辑、素材、排期、发布、导出。
- 页数6/视频180秒可调；三标题方向为直观实用、问题、经历。
- 空指标null；复盘按平台、形式、观察周期分组；样本不足只提假设。
- 数据迁移使用SQLite备份及事务，失败回滚；不读取真实数据库用于测试。
