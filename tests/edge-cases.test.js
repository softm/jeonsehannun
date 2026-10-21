import test from 'node:test';import assert from 'node:assert/strict';import {newProject,normalizeImported,parseMoney,validDate,today} from '../model.js';
test('null 보증금 백업도 정상 복원',()=>{const p=newProject({name:'빈 금액',housing:'아파트',phase:0,deposit:null});assert.equal(normalizeImported(p).deposit,null);});
test('undefined 보증금은 미입력',()=>assert.equal(parseMoney(undefined),null));
test('실제 달력 날짜를 검증',()=>{assert.equal(validDate('2026-02-30'),false);assert.equal(validDate('2026-13-01'),false);assert.equal(validDate('2026-10-22'),true);});
test('한국 시간 날짜 경계를 사용',()=>assert.equal(today('2026-10-21T17:00:00Z'),'2026-10-22'));
