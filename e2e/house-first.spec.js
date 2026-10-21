import {test,expect} from '@playwright/test';
async function ready(page){await page.goto('./');await expect(page.locator('#save-status')).not.toContainText('연결하고');}
async function start(page,name='역 앞에서 본 집'){await ready(page);await page.locator('#start-house-name').fill(name);await page.locator('#start-house-form').getByRole('button').click();await expect(page.locator('#project-title')).toHaveText(name);}

test('첫 화면은 프로젝트 없이 별칭 하나로 시작',async({page})=>{
  await ready(page);
  await expect(page.locator('body')).not.toContainText('프로젝트');
  await expect(page.getByRole('heading',{name:'어떤 집을 살펴보고 있나요?'})).toBeVisible();
  await expect(page.locator('#start-house-form input:visible')).toHaveCount(1);
  await page.screenshot({path:'test-results/screenshots/house-first-welcome-desktop.png',fullPage:true});
  await page.locator('#start-house-name').fill('역 앞 빌라');
  await page.locator('#start-house-form').getByRole('button').click();
  await expect(page.locator('#project-title')).toHaveText('역 앞 빌라');
  await expect(page.locator('#project-subtitle')).toContainText('주소 미입력');
  await expect(page.locator('#project-subtitle')).toContainText('아직 모름');
  await expect(page.locator('.check-list .done')).toHaveCount(0);
  await expect(page.locator('.house-actions')).toContainText('다가구·단독주택');
});

test('집 추가 없이 확인 방법을 읽을 수 있음',async({page})=>{
  await ready(page);
  await page.getByRole('button',{name:'집을 정하기 전, 확인 방법 먼저 보기 →',exact:true}).click();
  await expect(page.getByRole('dialog')).toContainText('기록이 생기지는 않아요');
  await expect(page.locator('.guide-phase')).toHaveCount(6);
  await page.locator('.guide-phase summary').first().click();
  await expect(page.locator('.guide-phase details').first().locator('ol')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('.project-btn')).toHaveCount(0);
  await page.reload();
  await expect(page.locator('#start-house-form')).toBeVisible();
});

test('다른 집은 별칭만 입력, 추가 정보는 접혀 있음',async({page})=>{
  await start(page,'첫 집');
  await page.locator('#hero-create').click();
  await expect(page.locator('#project-form input:visible')).toHaveCount(1);
  await expect(page.locator('#p-address')).not.toBeVisible();
  await page.getByLabel('집 별칭',{exact:true}).fill('둘째 집');
  await page.getByRole('button',{name:'이 집 확인하기',exact:true}).click();
  await expect(page.locator('.project-btn')).toHaveCount(2);
  await expect(page.locator('#project-title')).toHaveText('둘째 집');
});

test('집 메모는 새로고침·백업 가져오기 후 유지하고 확인 상태는 바꾸지 않음',async({page})=>{
  await start(page);
  await page.getByRole('button',{name:'메모 남기기',exact:true}).click();
  const text='채광이 좋았어요. 관리비에 포함된 항목 물어보기.\n<img src=x onerror=alert(1)>';
  await page.getByLabel('오늘 본 내용·궁금한 점',{exact:true}).fill(text);
  await page.getByRole('button',{name:'메모 저장',exact:true}).click();
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.locator('.house-note-text')).toHaveText(text);
  await expect(page.locator('.house-note-text img')).toHaveCount(0);
  await expect(page.locator('.check-list .done')).toHaveCount(0);
  await page.reload();
  await expect(page.locator('.house-note-text')).toHaveText(text);
  await page.locator('#backup').click();
  const download=page.waitForEvent('download');
  await page.getByRole('button',{name:'기록만 백업',exact:true}).click();
  const path=await (await download).path();
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await page.locator('#import-file').setInputFiles(path);
  await page.getByRole('button',{name:'새 집 기록으로 가져오기',exact:true}).click();
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.locator('.house-note-text')).toHaveText(text);
  await expect(page.locator('.project-btn')).toHaveCount(2);
});

test('기존 백업은 새 저장 구조 없이 그대로 가져옴',async({page})=>{
  await ready(page);
  const data={format:'jeonsehannun-backup',version:1,bundles:[{project:{id:'legacy-id',name:'예전에 보던 집',address:'가상 주소',housing:'아파트',phase:0,deposit:null,checks:{},documents:[],history:[],snapshots:[],guarantee:0,guaranteeNote:''},files:[]}]};
  await page.locator('#import-file').setInputFiles({name:'legacy.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(data))});
  await page.getByRole('button',{name:'새 집 기록으로 가져오기',exact:true}).click();
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.locator('#project-title')).toContainText('예전에 보던 집');
  await expect(page.getByRole('button',{name:'메모 남기기',exact:true})).toBeVisible();
});

test('모바일 처음 화면과 집 메모 흐름 가로 넘침 없음',async({page})=>{
  await page.setViewportSize({width:390,height:844});
  await ready(page);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.screenshot({path:'test-results/screenshots/house-first-welcome-mobile.png',fullPage:true});
  await page.locator('#start-house-name').fill('어제 본 302호');
  await page.locator('#start-house-form').getByRole('button').click();
  await expect(page.locator('#project-title')).toHaveText('어제 본 302호');
  await page.getByRole('button',{name:'메모 남기기',exact:true}).click();
  await page.getByLabel('오늘 본 내용·궁금한 점',{exact:true}).fill('계단과 창문 상태 다시 확인하기');
  await page.getByRole('button',{name:'메모 저장',exact:true}).click();
  await expect(page.getByRole('dialog')).not.toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.screenshot({path:'test-results/screenshots/house-first-notes-mobile.png',fullPage:true});
});
