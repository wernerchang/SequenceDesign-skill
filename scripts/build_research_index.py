"""Build the stage-0 task denominator from the visually checked source contents."""
import json
from pathlib import Path

groups=[
('1','research/chapter-01.md',[(1,'反馈移位寄存器'),(7,'反馈逻辑函数'),(13,'线性与非线性反馈移位寄存器'),(17,'有向图工具'),(27,'de Bruijn-Good图'),(33,'周期性与圈'),(41,'纯轮换与补轮换'),(53,'变量独立判据')],59),
('2','research/chapters-02-03.md',[(59,'线性反馈序列'),(61,'线性序列周期性'),(65,'圈长分布与圈数'),(78,'m序列'),(81,'m序列伪随机性'),(90,'线性递归方程求解'),(94,'序列采样'),(100,'线性综合')],123),
('3','research/chapters-02-03.md',[(123,'非线性分析'),(138,'M序列'),(153,'非线性综合')],167),
('4','research/chapters-04-05.md',[(167,'相关函数一般性质'),(173,'m序列互相关'),(178,'Gold序列族'),(183,'其他序列族'),(187,'低非周期自相关'),(193,'互补序列'),(201,'多相序列'),(210,'二元正交序列族')],220),
('5','research/chapters-04-05.md',[(220,'组合及相关特性'),(223,'布尔组合'),(228,'模二和复码'),(233,'解析计算相关'),(237,'功率谱密度')],249),
('6','research/chapters-06-appendix.md',[(249,'伪码测距'),(257,'导航'),(271,'伪码多址'),(281,'数据加乱'),(290,'噪声发生器'),(301,'数据保密')],307),
('7','research/chapters-06-appendix.md',[(307,'多维阵列基本概念'),(314,'最大面积基块'),(347,'最大容积基块'),(356,'其他周期平面综合'),(364,'周期平面应用')],371)]
tasks=[]
for chapter,dest,sections,end in groups:
    for i,(start,title) in enumerate(sections):
        stop=(sections[i+1][0] if i+1<len(sections) else end)
        tasks.append(dict(task_id=f'T{chapter}.{i+1}',source_section=f'§{chapter}.{i+1}',title=title,
                          printed_start=start,printed_end_inclusive=stop,
                          pdf_start=start+7,pdf_end_inclusive=stop+7,
                          boundary_note='section transitions can share a page; end includes transition page',
                          research_destination=dest,expected_output='问题、条件、机制、证明链、例子、自由度和边界',
                          importance='core',candidate_ids=[],extraction_status='not_started'))
for i,(start,end,title) in enumerate([(371,374,'不可约多项式表'),(374,377,'不可约三项式表'),(377,380,'本原多项式表'),(380,380,'GF(q)本原多项式表'),(380,389,'五级M序列反馈函数表')],1):
    tasks.append(dict(task_id=f'TA{i}',source_section=f'附表{i}',title=title,
                      printed_start=start,printed_end_inclusive=end,pdf_start=start+7,pdf_end_inclusive=end+7,
                      research_destination='research/chapters-06-appendix.md',
                      expected_output='表格用途、编码及使用约束；逐项转录与复算另列',importance='reference',
                      candidate_ids=[],extraction_status='not_started'))
Path('research/tasks.json').write_text(json.dumps(dict(schema_version=1,origin='PDF目录第6–7页；正文研究核对',
       scope='43正文小节+5附表；参考文献只登记来源角色',tasks=tasks),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Built',len(tasks),'source-derived tasks; no extraction pass asserted')
