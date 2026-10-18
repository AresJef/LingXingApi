"""视频模型类型边界；非空name/url仅为明确标记的离线构造用例。"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from lingxingapi.ads import schema
from lingxingapi.fields import StrOrNone2Blank
from sp_entities_contract import validate_sp_entity_response


def synthetic_video():
    return {'asset_id':'amzn1.assetlibrary.asset1.a001','asset_version':'version_v1',
            'headline':'Synthetic title','description':'Synthetic description','name':None,'url':None}


def test_independent_video_model_uses_existing_blank_converter_and_required_fields():
    assert not hasattr(schema,'SpProductVideo')
    for name in ('name','url'):
        assert schema.SpProductVideoDetail.model_fields[name].annotation is StrOrNone2Blank
    raw=synthetic_video();before=deepcopy(raw);parsed=schema.SpProductVideoDetail.model_validate(raw)
    assert raw==before and parsed.name==parsed.url==''
    for field in schema.SpProductVideoDetail.model_fields:
        assert schema.SpProductVideoDetail.model_fields[field].is_required()
        missing=deepcopy(raw);del missing[field]
        with pytest.raises(ValidationError):schema.SpProductVideoDetail.model_validate(missing)


@pytest.mark.parametrize('name,url',[('synthetic.mp4','https://example.test/synthetic.mp4'),('',''),('  name  ','  url  ')])
def test_synthetic_nonnull_name_and_url_are_preserved_by_existing_type(name,url):
    row=schema.SpProductVideoDetail.model_validate(synthetic_video()|{'name':name,'url':url})
    assert row.name==name and row.url==url


@pytest.mark.parametrize('key',['asset_id','asset_version','headline','description'])
def test_four_video_strings_do_not_accept_null(key):
    with pytest.raises(ValidationError):schema.SpProductVideoDetail.model_validate(synthetic_video()|{key:None})


def test_real_complete_frozen_video_page_checks_all_five_hundred_rows_and_twelve_elements():
    p=Path(__file__).with_name('fixtures')/'ads/basic/sp/sp_products-video-evidence.json'
    wrapper=json.loads(p.read_bytes());raw=wrapper['response'];before=deepcopy(raw)
    assert wrapper['source']=='local_raw' and wrapper['endpoint']=='ads.SpProducts'
    parsed=validate_sp_entity_response(raw,schema.SpProducts)
    assert raw==before and len(parsed.data)==parsed.response_count==500
    assert sum(bool(row.video_details) for row in parsed.data)==6
    videos=[video for row in parsed.data for video in row.video_details]
    assert len(videos)==12
    for row,model in zip(raw['data'],parsed.data,strict=True):
        for wire,video in zip(row['video_details'],model.video_details,strict=True):
            assert set(wire)=={'asset_id','asset_version','headline','description','name','url'}
            assert wire['name'] is wire['url'] is None
            assert video.name==video.url==''
            assert all(getattr(video,key)==wire[key] for key in ('asset_id','asset_version','headline','description'))
    typical=parsed.data[179].video_details[0]
    for field,info in schema.SpProductVideoDetail.model_fields.items():
        assert info.is_required() and info.description and info.examples==[getattr(typical,field)]
