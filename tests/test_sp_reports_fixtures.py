"""SP日报/小时真实脱敏集合；首次接入诊断不作为日常必填契约。"""
from __future__ import annotations

import asyncio
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from lingxingapi.ads import schema
from lingxingapi.ads.api import AdsAPI
from response_contract import validate_response
from sp_reports_contract import validate_sp_report_response, same_hour_rows
from sample_collection import load_collection, same_data
from test_sp_reports_requests import DAILY, HOURLY

COMPLETED = (
    ('SpCampaignReports','sp_campaign_reports'),
    ('SpPlacementReports','sp_placement_reports'),
    ('SpAdGroupReports','sp_ad_group_reports'),
    ('SpProductReports','sp_product_reports'),
    ('SpKeywordReports','sp_keyword_reports'),
    ('SpKeywordQueryReports','sp_keyword_query_reports'),
    ('SpTargetReports','sp_target_reports'),
    ('SpTargetQueryReports','sp_target_query_reports'),
)
DIRECTORY = Path(__file__).with_name('fixtures')/'ads/reports/sp'
HOURS = (
    ('SpCampaignHourData','sp_campaign_hour_data'), ('SpPlacementHourData','sp_placement_hour_data'),
    ('SpAdGroupHourData','sp_ad_group_hour_data'), ('SpProductHourData','sp_product_hour_data'),
    ('SpKeywordHourData','sp_keyword_hour_data'), ('SpTargetHourData','sp_target_hour_data'),
)


@pytest.mark.parametrize('method,prefix',COMPLETED)
def test_real_daily_complete_responses_dates_identifiers_and_pagination(method,prefix):
    manifest,records,responses=load_collection(DIRECTORY/(prefix+'-manifest.json'),'ads.'+method)
    before=deepcopy((manifest,records,responses))
    assert manifest['planned_requests']==13 and manifest['not_run']==[]
    assert len(records)+len(manifest.get('diagnostics',[]))==13
    for check in manifest['checks'].values():assert check['status'] in {'proved','observed'}
    for label,raw in responses.items():
        parsed=validate_response(raw,getattr(schema,method))
        assert parsed.response_count==len(raw['data'])
        assert parsed.total_count==raw['total']
        assert all(row['report_date']==records[label]['request']['report_date'] for row in raw['data'])
        profile=records[label]['request'].get('profile_id')
        if profile is not None:assert all(row['profile_id']==profile for row in raw['data'])
    relationships=manifest['relationships'];reference=responses[relationships['reference']]['data']
    assert len(reference)==4 and same_data(reference,responses[relationships['end_reference']]['data'])
    for kind in ('offset_pages','token_pages'):
        assert same_data([row for label in relationships[kind] for row in responses[label]['data']],reference)
    assert same_data(responses[relationships['token_control']]['data'],responses[relationships['token_conflict']]['data'])
    assert not same_data(reference[:2],reference[2:])
    assert (manifest,records,responses)==before


@pytest.mark.parametrize('method,prefix',COMPLETED)
def test_real_daily_fixture_replays_sdk_requests_with_published_cursor_source(method,prefix):
    _,records,responses=load_collection(DIRECTORY/(prefix+'-manifest.json'),'ads.'+method)
    _,url,discriminator=next(item for item in DAILY if item[0]==method)
    for label,record in records.items():
        request=deepcopy(record['request'])
        if record['next_token_from'] is not None:
            request['next_token']=responses[record['next_token_from']]['next_token']
        kwargs={**request,'sid':request.get('sid'),'profile_id':request.get('profile_id')}
        assert kwargs.pop('show_detail')==0
        for key,value in discriminator.items():assert kwargs.pop(key)==value
        signed=AsyncMock(return_value=responses[label])
        parsed=asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),**kwargs))
        signed.assert_awaited_once_with('POST',url,body=request,headers={'X-API-VERSION':'2'})
        assert isinstance(parsed,getattr(schema,method))


@pytest.mark.parametrize('method,prefix',HOURS)
def test_real_hourly_full_multisets_null_token_source_campaigns_and_original_response_order(method,prefix):
    manifest,records,responses=load_collection(DIRECTORY/(prefix+'-manifest.json'),'ads.'+method)
    before=deepcopy((manifest,records,responses))
    assert len(records)==manifest['planned_requests']==3 and manifest['not_run']==[]
    assert all(check['status']=='proved' for check in manifest['checks'].values())
    assert manifest['checks']['baseline_stability']['comparison']=='complete_rows_multiset'
    for label,raw in responses.items():
        assert raw['next_token'] is None
        parsed=validate_sp_report_response(raw,getattr(schema,method))
        assert parsed.model_dump()==getattr(schema,method).model_validate(raw).model_dump()
        assert all(row['report_date']==records[label]['request']['report_date'] for row in raw['data'])
        assert all(row['campaign_id']==records[label]['request']['campaign_id'] and 0<=row['hour']<=23 for row in raw['data'])
    assert same_hour_rows(responses['campaign-A']['data'],responses['reference-end']['data'])
    assert manifest['checks']['baseline_stability']['ordered_data_equal'] is same_data(responses['campaign-A']['data'],responses['reference-end']['data'])
    # initial_order_diagnostics是可选历史附注，本次checks和完整响应仍须满足以上断言。
    assert (manifest,records,responses)==before


@pytest.mark.parametrize('method,prefix',HOURS)
def test_real_hourly_fixture_replays_fixed_aggregation_without_pagination(method,prefix):
    _,records,responses=load_collection(DIRECTORY/(prefix+'-manifest.json'),'ads.'+method)
    _,url,aggregation=next(item for item in HOURLY if item[0]==method)
    for label,record in records.items():
        request=deepcopy(record['request']);kwargs=dict(request)
        assert record['next_token_from'] is None
        for key,value in aggregation.items():assert kwargs.pop(key)==value
        signed=AsyncMock(return_value=responses[label])
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),**kwargs))
        signed.assert_awaited_once_with('POST',url,body=request, headers={"X-API-VERSION": "2"})
