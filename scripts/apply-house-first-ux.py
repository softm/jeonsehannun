"""One-time, guarded source migration. Does not access or migrate user data."""
from pathlib import Path

def required(text, old, new):
    if old not in text:
        raise SystemExit('Expected source fragment missing: '+old[:100])
    return text.replace(old, new)

app_path=Path('app.js')
app=app_path.read_text()
if 'function welcomeHouse()' in app:
    print('House-first UX is already applied.')
    raise SystemExit(0)

index=Path('index.html').read_text()
for old,new in {
    '내 계약 프로젝트':'살펴보는 집',
    '새 프로젝트 만들기':'다른 집 추가하기',
    '확인할 집마다 하나씩 관리하세요.':'집마다 메모와 확인한 내용을 모아둬요.',
    '프로젝트 목록':'살펴보는 집 목록',
    '＋ 새 프로젝트':'＋ 다른 집 추가',
    'MY JEONSE CHECKLIST':'내 집을 알아가는 기록',
    '계약보다 먼저,<br><em>확인부터.</em>':'마음에 둔 집,<br><em>하나씩 확인해요.</em>',
    '내 보증금을 지키기 위한 확인, 하나씩 놓치지 않도록.':'아는 것부터 적어두세요. 아직 모르는 것은 천천히 확인해요.',
    '첫 프로젝트 만들기 →':'다른 집 추가',
    '프로젝트 보기':'이 집의 기록',
    '단계별 점검':'확인할 내용',
    '변경 이력':'기록 모아보기',
    '후보 비교':'집 비교',
    '프로젝트와 서류':'집 기록과 서류',
    '전세한눈 v0.1':'전세한눈 v0.2',
}.items():
    index=required(index,old,new)
Path('index.html').write_text(index)

app=required(app,'function render(){const project=p();',"function render(){const project=p();document.querySelector('.shell').classList.toggle('no-homes',!all.length);document.querySelector('.tabs').hidden=!project&&tab!=='compare';")
app=required(app,"$('#hero-create').hidden=!!project;","$('#hero-create').hidden=!project;")
app=required(app,'계약보다 먼저,<br><em>확인부터.</em>','마음에 둔 집,<br><em>하나씩 확인해요.</em>')
app=required(app,'내 보증금을 지키기 위한 확인, 하나씩 놓치지 않도록.','아는 것부터 적어두세요. 아직 모르는 것은 천천히 확인해요.')
start=app.index("if(!project){$('#content').innerHTML=")
end=app.index("if(tab==='overview')overview(project);",start)
app=app[:start]+"if(!project){$('#content').innerHTML=welcomeHouse();return;}"+app[end:]
app=required(app,"$('#content').innerHTML=stats(project)+`<div class=\"layout\">","$('#content').innerHTML=houseActions(project)+stats(project)+`<div class=\"layout\">")
app=required(app,'현재 단계는 탐색할 수 있습니다. 단계를 바꿔도 미확인 항목은 사라지지 않습니다.','지금 내 상황을 선택하고, 아는 것부터 확인해요. 모르는 항목은 미확인으로 남겨두세요.')
app=required(app,'YOUR NEXT STEP','다음으로 살펴볼 내용')
app=required(app,'근거 기록</span>','확인해 둔 내용</span>')
app=required(app,'확인 기록과 변경 이력','이 집에 남긴 기록')
app=required(app,'현재 상태 기록</button>','지금까지의 기록 남기기</button>')
app=required(app,'후보 주택 비교','살펴보는 집 비교')
app=app.replace('먼저 프로젝트를 등록하세요.','먼저 살펴볼 집을 적어주세요.').replace('먼저 프로젝트를 등록해 주세요.','아직 보관할 집 기록이 없어요.')
app=app.replace('새 프로젝트로 복원','새 집 기록으로 가져오기').replace('개 프로젝트를 새 프로젝트로 복원','개 집 기록을 별도의 기록으로 가져오기')
app=app.replace('프로젝트 삭제 확인','집 기록 삭제 확인').replace('프로젝트와 서류 삭제','집 기록과 서류 삭제')
app=app.replace('프로젝트','집 기록')

# Replace the complete form rather than hiding required fields with CSS.
start=app.index('function projectForm(edit=false)')
end=app.index('\nfunction checkForm(',start)
form=r'''function projectForm(edit=false){
  const project=edit?p():null;
  open(edit?'집 정보 수정':'어떤 집을 살펴볼까요?',`<form id="project-form">
    <p class="hint">기억하기 쉬운 별칭 하나면 충분해요. 정확한 주소와 계약 내용은 나중에 채워도 괜찮아요.</p>
    <div class="field"><label for="p-name">집 별칭</label><input id="p-name" name="name" required maxlength="80" placeholder="예: 역 앞 빌라, 어제 본 302호" value="${esc(project?.name||'')}"></div>
    <details class="house-details" ${edit?'open':''}><summary>주소·보증금·일정도 적어두기 <span class="hint">선택</span></summary><div class="details-body">
    <div class="field"><label for="p-address">정확한 주소·동·호수</label><input id="p-address" name="address" maxlength="240" value="${esc(project?.address||'')}" placeholder="등기·대장과 대조할 정확한 주소"></div>
    <div class="grid-two"><div class="field"><label for="p-housing">주택 유형</label><select id="p-housing" name="housing">${HOUSING.map(v=>`<option ${((project?.housing||'아직 모름')===v)?'selected':''}>${v}</option>`).join('')}</select></div><div class="field"><label for="p-deposit">보증금 (원)</label><input id="p-deposit" name="deposit" inputmode="numeric" value="${project?.deposit??''}" placeholder="모르면 비워두세요"></div></div>
    <div class="field"><label for="p-phase">지금 내 상황</label><select id="p-phase" name="phase">${PHASES.map((v,i)=>`<option value="${i}" ${project?.phase===i?'selected':''}>${v}</option>`).join('')}</select></div>
    <div class="grid-two">${[['contractDate','계약일'],['balanceDate','잔금일'],['endDate','계약 만료일']].map(([k,l])=>`<div class="field"><label for="${k}">${l}</label><input type="date" id="${k}" name="${k}" value="${esc(project?.[k]||'')}"></div>`).join('')}</div>
    </div></details>
    <p class="hint">${edit?'주소·주택 유형을 바꾸면 기존 점검 상태는 미확인으로 되돌아갑니다. 메모·서류·이전 이력은 유지됩니다.':'기록은 이 기기의 이 브라우저에만 저장돼요. 집 별칭을 입력해도 정확한 주소가 확인된 것은 아니에요.'}</p>
    <div class="dialog-actions">${edit?'<button type="button" class="danger" id="delete-project">집 기록 삭제</button>':''}<button type="button" id="cancel-project">취소</button><button class="primary" type="submit">${edit?'수정 저장':'이 집 확인하기'}</button></div></form>`);
  $('#cancel-project').onclick=close;
  if(edit)$('#delete-project').onclick=()=>deleteProject(project);
  $('#project-form').onsubmit=e=>{e.preventDefault();const raw=Object.fromEntries(new FormData(e.target));act(async()=>{let value;if(project){value=structuredClone(project);const data=validateProject(raw);if(data.address!==value.address||data.housing!==value.housing){value.snapshots.unshift(snapshot(value));value.snapshots=value.snapshots.slice(0,20);value.checks={};log(value,'주소·주택 유형 변경으로 점검 상태 초기화');}Object.assign(value,data);log(value,'집 정보 수정');}else value=newProject(raw);await db.save(value);current=value.id;tab='overview';},{dialog:true});};
}
'''
app=app[:start]+form+app[end:]

extra=r'''
function welcomeHouse(){return `<section class="card house-welcome"><p class="subheading">복잡한 준비 없이 시작해요</p><h2>어떤 집을 살펴보고 있나요?</h2><p>집을 보며 느낀 점, 중개사에게 물어볼 것, 확인해 둔 서류를 한곳에 남겨요.</p><form id="start-house-form"><div class="field"><label for="start-house-name">집 별칭</label><input id="start-house-name" name="name" maxlength="80" required placeholder="예: 역 앞 빌라, 어제 본 302호" aria-describedby="start-house-hint"></div><p id="start-house-hint" class="hint">알아보기 쉬운 이름이면 충분해요. 정확한 주소·보증금·날짜는 나중에 적어주세요.</p><button class="primary" type="submit">이 집 확인하기 →</button></form><div class="welcome-secondary"><button class="text-btn" data-action="guide">집을 정하기 전, 확인 방법 먼저 보기 →</button><button class="text-btn" data-action="demo">가상 예시 둘러보기</button><button class="text-btn" data-action="restore">백업한 기록 가져오기</button></div></section><div class="welcome-flow"><article><span>01</span><h3>궁금한 것 적어두기</h3><p>보러 갔을 때 느낀 점이나 물어볼 것을 메모해요.</p></article><article><span>02</span><h3>하나씩 확인하기</h3><p>확인 방법을 읽고 직접 확인한 근거를 남겨요.</p></article><article><span>03</span><h3>다시 꺼내보기</h3><p>같은 브라우저에서 메모와 서류를 이어서 볼 수 있어요.</p></article></div><p class="hint">로그인·다른 기기와의 동기화는 아직 연결하지 않았어요. 중요한 기록은 백업해 주세요.</p>`;}
function houseActions(project){return `<section class="card house-actions"><div class="section-head"><div><p class="subheading">이 집을 알아가는 중</p><h2>오늘은 무엇을 남겨볼까요?</h2></div></div>${project.homeMemo?`<p class="house-note-text">${esc(project.homeMemo)}</p>`:'<p class="muted small">마음에 들었던 점이나 아직 물어보지 못한 것부터 적어두세요.</p>'}<div class="inline"><button class="primary" data-action="home-note">${project.homeMemo?'메모 이어쓰기':'메모 남기기'}</button><button data-tab="documents">서류 보관하기</button><button data-tab="checks">확인할 내용 보기</button></div><p class="hint">메모를 남겨도 점검 항목은 자동으로 확인 완료되지 않아요.${project.housing==='아직 모름'?' 주택 유형을 아직 몰라 다가구·단독주택의 추가 확인 항목도 함께 보여드려요.':''}</p></section>`;}
function homeNoteForm(){const project=p();if(!project)return;open('이 집에 메모 남기기',`<form id="home-note-form"><p class="hint">예: 채광이 좋았어요. 관리비에 무엇이 포함되는지 물어보기.</p><div class="field"><label for="home-note">오늘 본 내용·궁금한 점</label><textarea id="home-note" maxlength="4000" placeholder="생각나는 대로 편하게 적어주세요.">${esc(project.homeMemo||'')}</textarea></div><p class="hint">직접 확인한 근거는 ‘확인할 내용’에서 따로 기록할 수 있어요.</p><div class="dialog-actions"><button type="button" id="cancel-note">취소</button><button class="primary" type="submit">메모 저장</button></div></form>`);$('#cancel-note').onclick=close;$('#home-note-form').onsubmit=e=>{e.preventDefault();const text=$('#home-note').value;act(async()=>{const value=structuredClone(project);value.homeMemo=validateHomeMemo(text);log(value,'집 메모 수정');await db.save(value);},{dialog:true});};}
function browseGuide(){open('집을 정하기 전, 확인 방법부터',`<p class="hint">집을 추가하지 않아도 읽을 수 있어요. 이 화면을 보는 것만으로 확인 기록이 생기지는 않아요.</p>${PHASES.map((label,i)=>`<section class="guide-phase"><h3>${label}</h3>${CHECKS.filter(c=>c.phase===i).map(c=>`<details><summary>${c.title}</summary><p class="hint">${c.detail}${c.housing?' · '+c.housing.join(', ')+'에서 추가 확인':''}</p><ol class="guide-steps">${c.steps.map(s=>`<li>${s}</li>`).join('')}</ol><p class="small">${source(c.source)}</p></details>`).join('')}</section>`).join('')}<p class="hint">공식 안내로 이어지는 확인 가이드입니다. 자동 조회·법률 검토가 아닙니다.</p>`);}
document.addEventListener('submit',e=>{if(e.target.id!=='start-house-form')return;e.preventDefault();const name=new FormData(e.target).get('name');act(async()=>{const value=newProject({name,housing:'아직 모름',phase:0});await db.save(value);current=value.id;tab='overview';});});
'''
app=required(app,'validateProject,validateCheck,','validateProject,validateCheck,validateHomeMemo,')
app=required(app,'function handle(action){',"function handle(action){if(action==='home-note')homeNoteForm();if(action==='guide')browseGuide();")
app=app+extra
# Legacy activity labels are display-only; stored data and IDs remain untouched.
app=required(app,'${esc(h.text)}','${esc(h.text===\'프로젝트 생성\'?\'집을 살펴보기 시작함\':h.text)}')
app_path.write_text(app)

model=Path('model.js').read_text()
model=required(model,"HOUSING=['아파트'","HOUSING=['아직 모름','아파트'")
model=required(model,"CHECKS.filter(c=>!c.housing||c.housing.includes(p.housing))","CHECKS.filter(c=>p.housing==='아직 모름'||!c.housing||c.housing.includes(p.housing))")
model=required(model,'프로젝트 이름을 1~80자로 입력해 주세요.','집 별칭을 1~80자로 입력해 주세요.')
model=required(model,"guarantee:0,guaranteeNote:''","guarantee:0,guaranteeNote:'',homeMemo:''")
model=required(model,"log(p,'프로젝트 생성')","log(p,'집을 살펴보기 시작함')")
model=required(model,"p.name=(data.name+' (복원)').slice(0,80);","p.name=(data.name+' (복원)').slice(0,80);p.homeMemo=validateHomeMemo(raw.homeMemo);")
model=required(model,'백업에서 신규 프로젝트로 복원.','백업에서 새 집 기록으로 가져옴.')
model+="\nexport function validateHomeMemo(value){if(value===undefined||value===null)return '';if(typeof value!=='string'||value.length>4000)throw new Error('집 메모는 4,000자 이내의 글로 남겨주세요.');return value.trim();}\n"
Path('model.js').write_text(model)

css=r'''
/* House-first entry: keep internal record IDs while making the experience conversational. */
.shell.no-homes{grid-template-columns:1fr;max-width:1000px}.shell.no-homes .sidebar{display:none}.shell.no-homes main{width:100%}
.house-welcome{padding:32px;margin-bottom:22px}.house-welcome h2{font-size:25px;letter-spacing:-.6px}.house-welcome>p{color:var(--muted);font-size:14px}
#start-house-form{max-width:620px;margin-top:24px}#start-house-form .field{margin-bottom:8px}#start-house-form .primary{margin-top:4px}
.welcome-secondary{display:flex;gap:12px 22px;flex-wrap:wrap;border-top:1px solid var(--border);margin-top:25px;padding-top:16px}
.welcome-flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin:28px 0}.welcome-flow article{min-width:0}.welcome-flow span{color:var(--green);font-weight:750;font-size:12px}.welcome-flow h3{margin:8px 0;font-size:15px}.welcome-flow p{color:var(--muted);font-size:13px}
.house-details{border-top:1px solid var(--border);padding:14px 0}.house-details summary,.guide-phase summary{cursor:pointer;min-height:44px;line-height:1.7;padding:10px 0;font-weight:650}.details-body{padding-top:18px}
.house-actions{margin-bottom:24px;background:#fafff8}.house-actions .subheading{margin-bottom:5px}.house-actions .hint{margin:14px 0 0}.house-note-text{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px;max-height:180px;overflow:auto;border-left:3px solid #b4d0b9;padding:8px 14px;background:white}
.guide-phase{margin-bottom:24px}.guide-phase details{border-bottom:1px solid var(--border)}.guide-phase h3{color:var(--green)}
@media(max-width:700px){.house-welcome{padding:22px 18px}.house-welcome h2{font-size:22px}.welcome-flow{grid-template-columns:1fr;gap:12px}.welcome-flow article{padding:12px 0;border-bottom:1px solid var(--border)}.welcome-flow p{margin:0}.welcome-secondary{gap:4px}.welcome-secondary button{width:100%;text-align:left}#start-house-form .primary{width:100%}.house-actions .inline{gap:8px}.house-actions .inline button{font-size:13px}.shell.no-homes main{padding-top:24px}}
'''
with Path('styles.css').open('a') as f:f.write(css)

for name in ['privacy.html','data-status.html']:
    path=Path(name);s=path.read_text().replace('프로젝트','집 기록');path.write_text(s)

# Keep the existing regression suite, only adapting its user-facing entry and labels.
tests=Path('e2e/app.spec.js').read_text()
a=tests.index('async function create(');b=tests.index('\nasync function openAddress',a)
tests=tests[:a]+'''async function create(page,name='E2E 검증용 집'){await page.goto('./');await expect(page.locator('#save-status')).not.toContainText('연결하고');await page.locator('#start-house-name').fill(name);await page.locator('#start-house-form').getByRole('button').click();await expect(page.locator('#project-title')).toHaveText(name);await page.locator('#edit-project').click();await page.getByLabel('정확한 주소·동·호수',{exact:true}).fill('테스트 주소 · 실제 매물 아님');await page.getByRole('button',{name:'수정 저장',exact:true}).click();await expect(page.getByRole('dialog')).not.toBeVisible();}
'''+tests[b:]
for old,new in [('프로젝트 이름 *','집 별칭'),('프로젝트 만들기','이 집 확인하기'),('새 프로젝트로 복원','새 집 기록으로 가져오기'),('변경 이력','기록 모아보기'),('현재 상태 기록','지금까지의 기록 남기기')]:
    tests=tests.replace(old,new)
Path('e2e/app.spec.js').write_text(tests)

Path('docs/HOUSE-FIRST-UX.md').write_text('''# 집을 알아가는 기록 중심 UX

사용자 피드백: 프로젝트를 만드는 느낌보다 자연스럽게 기록하고 확인하는 분위기.

- 사용자 화면에서 프로젝트를 만들도록 요구하지 않는다. 내부 ID·IndexedDB·기존 백업 포맷은 유지한다.
- 첫 화면에서 집 별칭 하나를 적고 바로 확인 화면으로 들어간다. 별칭은 공식 주소가 아니며 주소 확인으로 처리하지 않는다.
- 다른 집 추가도 별칭 하나로 시작한다. 주소·금액·일정은 선택 입력이며 접힌 영역에서 추가한다.
- 주택 유형 초기값은 ‘아직 모름’. 모르는 상태에서 아파트로 단정하거나 다가구 확인 항목을 누락하지 않는다.
- 집을 정하기 전에도 확인 방법을 읽을 수 있다. 가이드 열람만으로 기록을 생성하지 않는다.
- 집별 자유 메모를 추가한다. 메모 저장은 확인 완료와 별개다. 메모는 새로고침·백업/가져오기에서 보존한다.
- 저장 버튼으로 확정된 기록만 저장 완료로 표시한다. 자동 저장·계정 동기화로 표현하지 않는다.
- 미확인·위험·재확인 표시, 근거 없는 확인 차단, 개인정보·로컬 저장 안내를 유지한다.
- 기존 기록을 초기화하거나 저장소 이름·버전을 변경하지 않는다.

실제 전문가 회의나 법률 검수 완료를 의미하지 않는 제품 UX 변경 기록이다.
''')
print('Prepared house-first UI, guest guide, notes and regression selectors; user storage unchanged.')
