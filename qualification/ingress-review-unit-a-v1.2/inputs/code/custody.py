"""Offline custody verification; no semantic admission or runtime authority."""
import base64, hashlib, json, pathlib, sys

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def verify_stream(raw, expected):
    require(sha(raw)==expected,'ORDERED_STREAM_DRIFT')

def verify_pair(brain_raw, producer_raw, expected_brain, expected_producer):
    require(sha(brain_raw)==expected_brain,'BRAIN_DOCUMENT_DRIFT')
    require(sha(producer_raw)==expected_producer,'PRODUCER_DOCUMENT_DRIFT')
    doc=json.loads(brain_raw); p=doc['proposal']; epi=json.loads(producer_raw)
    require(p['epistemaddy_proposal_sha256']==sha(producer_raw),'FULL_PROPOSAL_BINDING')
    require(base64.b64decode(p['epistemaddy_proposal_utf8_base64'],validate=True)==producer_raw,'FULL_PROPOSAL_BYTES')
    payload=dict(p)
    del payload['epistemaddy_proposal_sha256'];del payload['epistemaddy_proposal_utf8_base64']
    require(epi['content']==payload,'PRODUCER_CONTENT_BINDING')
    raw=base64.b64decode(p['source_record_utf8_base64'],validate=True)
    require(sha(raw)==p['source_exact_record_sha256'],'SOURCE_RECORD_BINDING')
    source=json.loads(raw)
    require(p['source_normalization_profile']=='epistemaddy-python-json-v1-not-RFC8785','UNKNOWN_NORMALIZATION_PROFILE')
    normalized=json.dumps(source,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    require(sha(normalized)==p['source_normalized_record_sha256'],'NORMALIZED_SOURCE_BINDING')
    require(source['candidate_id']==p['source_candidate_id'],'CANDIDATE_ID_BINDING')
    require(source['record_version']==p['source_record_version'],'CANDIDATE_VERSION_BINDING')
    identity='atlas:'+p['database_sha256']+':'+p['source_candidate_id']+':'+str(p['source_record_version'])
    require(epi['source_identity']==identity and epi['subject_identity']==identity,'SUBJECT_BINDING')
    require(epi['identity']=='epistemaddy-proposal:'+sha((identity+':'+sha(raw)).encode()),'PROPOSAL_ID_BINDING')
    require(epi['producer']=='epistemaddy.VerticalSlice.propose','PRODUCER_BINDING')
    require(epi['scope']=='offline-atlas-review:'+p['database_sha256'],'SCOPE_BINDING')
    require(epi['jurisdiction']=='offline-candidate-review' and epi['operation']=='submit-noncanonical-candidate','OPERATION_BINDING')
    require(epi['lineage']==[identity],'LINEAGE_BINDING')
    require(epi['provenance']==['database-sha256:'+p['database_sha256'],'record-sha256:'+sha(raw)],'PROVENANCE_BINDING')
    require(epi['contract']==p['adapter_profile'] and epi['temporal_context'] is None,'CONTRACT_BINDING')
    require(p['canonical_membership'] is False and p['governing_baseline_adopted'] is False,'UNAUTHORIZED_PROMOTION')
    require(p['authority_resolution']=='UNRESOLVED' and p['visibility_resolution']=='UNRESOLVED','UNAUTHORIZED_RESOLUTION')
    return p['source_candidate_id'],p['source_record_version']

def verify_output(root, expected_report):
    report_raw=(root/'qualification.json').read_bytes()
    require(sha(report_raw)==expected_report,'QUALIFICATION_RECEIPT_DRIFT')
    report=json.loads(report_raw)
    brain=(root/'proposals.jsonl').read_bytes();producer=(root/'epistemaddy-proposals.jsonl').read_bytes()
    verify_stream(brain,report['proposal_stream_sha256'])
    verify_stream(producer,report['epistemaddy_proposal_stream_sha256'])
    rows=brain.splitlines();epis=producer.splitlines();pins=report['document_sha256']
    require(len(rows)==len(epis)==len(pins)==report['candidate_proposals']==2736,'INCOMPLETE_STREAM')
    seen=set()
    for raw,epi,pin in zip(rows,epis,pins):
        identity=verify_pair(raw,epi,pin,sha(epi))
        require(identity not in seen,'DUPLICATE_IDENTITY');seen.add(identity)
    return {'verified_pairs':len(seen),'canonical_admission':False}

if __name__=='__main__':
    print(json.dumps(verify_output(pathlib.Path(sys.argv[1]),sys.argv[2])))
