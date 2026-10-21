import test from 'node:test';
import assert from 'node:assert/strict';
import {CHECKS} from '../data.js';
import {newProject,activeChecks,summary,validateHomeMemo,normalizeImported} from '../model.js';
test('별칭 하나로 집 기록 시작, 주소·보증금은 미확인',()=>{const p=newProject({name:'역 앞 빌라',housing:'아직 모름',phase:0});assert.equal(p.address,'');assert.equal(p.deposit,null);assert.equal(p.homeMemo,'');assert.equal(summary(p).verified,0);});
test('유형을 모르면 다가구 항목도 누락하지 않음',()=>{const p=newProject({name:'처음 본 집',housing:'아직 모름',phase:0});assert.equal(activeChecks(p).length,CHECKS.length);});
test('메모는 기존 형식의 백업에서도 선택 필드',()=>{const p=newProject({name:'기존 집',housing:'아파트',phase:0});delete p.homeMemo;assert.equal(normalizeImported(p).homeMemo,'');p.homeMemo='다시 물어볼 것';assert.equal(normalizeImported(p).homeMemo,p.homeMemo);});
test('메모 자료형·길이 검증, 사용자 글은 데이터로 유지',()=>{assert.equal(validateHomeMemo('  <img src=x>  '),'<img src=x>');assert.throws(()=>validateHomeMemo({}));assert.throws(()=>validateHomeMemo('가'.repeat(4001)));});
